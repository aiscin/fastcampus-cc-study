#!/usr/bin/env python3
"""daily-news 수집 스크립트 (결정론 영역).

네이버 검색 API엔 '헤드라인' 엔드포인트가 없어, 분야별 대표어를 다중 검색한 뒤
제목 토큰 자카드 유사도로 같은 사건을 군집화한다. 여러 매체가 보도한 사건일수록
군집이 커지므로 '보도량 = 오늘의 중요도'로 근사한다.

AI(SKILL.md)가 할 일은 이 스크립트가 뽑은 상위 후보에서 최종 선별·요약·톤 조정뿐이다.
연예/포토/스포츠 화보성 기사는 여기서 제거한다(여러 매체가 같은 행사를 찍어 보도량이
부풀려지는 오탐 방지).

환경변수: NAVER_CLIENT_ID, NAVER_CLIENT_SECRET
사용:  python3 fetch_daily_news.py [--top N] [--per-cat M]
출력:  stdout에 JSON, 에러는 stderr + has_error:true
"""
import os
import sys
import json
import re
import html
import argparse
import urllib.parse
import urllib.request
import urllib.error

CID = os.environ.get("NAVER_CLIENT_ID")
CSEC = os.environ.get("NAVER_CLIENT_SECRET")

# 분야별 대표 검색어 — 헤드라인 엔드포인트 부재를 분야 검색으로 근사
CATEGORIES = {
    "정치": "정치",
    "경제": "경제",
    "사회": "사회",
    "IT/과학": "IT 과학",
    "세계": "국제",
    "속보": "속보",
}

# 제목에 이게 있으면 연예/화보/스포츠 단순 사진 기사 → 중요 뉴스 아님
FLUFF_PATTERNS = [
    r"\[?포토", r"HD포토", r"화보", r"레드카펫", r"엑's", r"ST포토", r"[ST포토]",
    r"포토엔", r"포토타임", r"직캠", r"movie", r"개봉박두", r"컴백",
    r"셀카", r"인증샷", r"뒤태", r"몸매", r"섹시", r"청순",
]
FLUFF_RE = re.compile("|".join(FLUFF_PATTERNS), re.IGNORECASE)

# 군집 대표 토큰 계산 시 버릴 흔한 단어
STOP = set(
    "속보 종합 단독 오늘 어제 관련 위해 그는 대한 있다 했다 밝혔다 대해 이번 "
    "지난 오전 오후 기자 뉴스 사진 영상 그것 이것 우리 대통령".split()
)


def strip_tags(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip()


def tokens(title):
    t = re.sub(r"[^\w가-힣 ]", " ", title)
    return {w for w in t.split() if len(w) >= 2 and w not in STOP}


def fetch(query, display=30):
    url = "https://openapi.naver.com/v1/search/news.json?" + urllib.parse.urlencode(
        {"query": query, "display": display, "sort": "date"}
    )
    req = urllib.request.Request(
        url,
        headers={"X-Naver-Client-Id": CID, "X-Naver-Client-Secret": CSEC},
    )
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.load(r).get("items", [])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--top", type=int, default=5, help="반환할 상위 뉴스 수")
    ap.add_argument("--per-cat", type=int, default=2, help="한 분야가 결과를 독식하지 않도록 분야당 상한")
    args = ap.parse_args()

    if not CID or not CSEC:
        print(json.dumps({
            "has_error": True,
            "errors": ["NAVER_CLIENT_ID/SECRET 환경변수가 없습니다. 프로젝트 루트 .env를 source 하세요."],
            "top": [],
        }, ensure_ascii=False))
        sys.exit(1)

    errors = []
    all_items = []
    seen = set()
    for cat, q in CATEGORIES.items():
        try:
            for it in fetch(q):
                link = it.get("originallink") or it.get("link")
                title = strip_tags(it.get("title", ""))
                if not link or link in seen:
                    continue
                if FLUFF_RE.search(title):
                    continue  # 연예/화보성 제거
                seen.add(link)
                all_items.append({
                    "cat": cat,
                    "title": title,
                    "desc": strip_tags(it.get("description", ""))[:200],
                    "link": link,
                    "pub": it.get("pubDate", ""),
                    "tok": tokens(title),
                })
        except urllib.error.HTTPError as e:
            errors.append(f"{cat} 검색 실패(HTTP {e.code}) — 키/호출한도 확인")
        except Exception as e:
            errors.append(f"{cat} 검색 실패: {e}")

    # 군집: 토큰 자카드로 같은 사건 묶기 (교집합 2개 이상 + 유사도 0.3 이상)
    clusters = []
    for it in all_items:
        placed = False
        for c in clusters:
            rep = c["items"][0]
            inter = len(it["tok"] & rep["tok"])
            union = len(it["tok"] | rep["tok"]) or 1
            if inter >= 2 and inter / union >= 0.3:
                c["items"].append(it)
                c["cats"].add(it["cat"])
                placed = True
                break
        if not placed:
            clusters.append({"items": [it], "cats": {it["cat"]}})

    # 보도량(군집 크기) → 분야 다양성 순
    clusters.sort(key=lambda c: (len(c["items"]), len(c["cats"])), reverse=True)

    # 분야 균형: 같은 분야가 결과를 독식하지 않도록 per-cat 상한
    result = []
    cat_count = {}
    for c in clusters:
        rep = max(c["items"], key=lambda x: len(x["title"]))
        cat = rep["cat"]
        if cat_count.get(cat, 0) >= args.per_cat and len(result) < args.top:
            continue
        cat_count[cat] = cat_count.get(cat, 0) + 1
        result.append({
            "title": rep["title"],
            "coverage": len(c["items"]),
            "cats": sorted(c["cats"]),
            "desc": rep["desc"][:160],
            "link": rep["link"],
        })
        if len(result) >= args.top:
            break

    print(json.dumps({
        "has_error": bool(errors) and not result,
        "errors": errors,
        "total_collected": len(all_items),
        "clusters": len(clusters),
        "top": result,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
