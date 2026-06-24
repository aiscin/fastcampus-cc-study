#!/usr/bin/env python3
"""네이버 검색 API 뉴스 수집 — 반도체 종목 뉴스레터용.

결정론 영역만 담당한다:
  - 워치리스트/매크로 키워드는 watchlist.json(외부 config)에서 로드 (코드 수정 없이 종목 변경)
  - 기간 자동 계산 (화~금=전일 1일 / 월=금·토·일 3일)
  - 종목·매크로 키워드 검색 (HTTP 에러 구분 + 재시도 + rate limit)
  - 종목 태깅 + 정규식 경계 매칭으로 오태깅 차단 ("이노테크홀" 같은 합성어 제외)
  - 기간 필터 + 중복 제거(URL/제목) + HTML 클린
  - 매체 등급(A/B/C) 분류 + unverified 플래그 + 매크로 상한·등급정렬

호재/악재 판단·요약·HTML 디자인은 AI(SKILL.md)가 한다. 이 스크립트는
"종목별로 분류된 깨끗한 뉴스 JSON"까지만 책임진다.

종료 코드: 0=정상(부분 에러는 has_error 플래그) / 1=수집 전체 실패(데이터 0건+에러)

사용법:
  python3 fetch_news.py                 # 워치리스트 전체, 기간 자동
  python3 fetch_news.py --sort sim      # 관련도순 (기본 date=최신순)
  python3 fetch_news.py --days 3        # 기간 강제 지정 (자동계산 무시)
출력: stdout 에 JSON
"""

import os
import sys
import json
import re
import html
import time
import argparse
import datetime
import urllib.parse
import urllib.request
import urllib.error

# 매체 등급 (증권 분석가 제안) — 도메인 일부만, 나머지는 C(기타).
MEDIA_GRADE = {
    "A": ["한국경제", "매일경제", "연합뉴스", "조선비즈", "서울경제", "이데일리", "머니투데이",
           "hankyung", "mk.co.kr", "yna.co.kr", "biz.chosun", "sedaily", "edaily", "mt.co.kr"],
    "B": ["전자신문", "디일렉", "지디넷", "ZDNET", "IT조선", "아이뉴스24",
           "etnews", "thelec", "zdnet", "inews24"],
}

NAVER_NEWS_API = "https://openapi.naver.com/v1/search/news.json"
KST = datetime.timezone(datetime.timedelta(hours=9))

# 종목명 뒤에 붙을 수 있는 한국어 조사 (경계 매칭에서 허용) — "이노테크의" 통과, "이노테크홀" 차단
PARTICLES = (
    "은|는|이|가|을|를|의|에|와|과|도|만|로|으로|에서|에게|한테|부터|까지|처럼|"
    "보다|라고|이라|란|이란|마저|조차|밖에|뿐|및|와의|과의|에도|로의"
)


def load_config():
    """watchlist.json(스킬 루트) 로드. 없으면 에러."""
    here = os.path.abspath(os.path.dirname(__file__))
    path = os.path.normpath(os.path.join(here, "..", "watchlist.json"))
    if not os.path.exists(path):
        return None, f"watchlist.json 을 찾을 수 없습니다: {path}"
    with open(path, encoding="utf-8") as f:
        cfg = json.load(f)
    if not cfg.get("watchlist"):
        return None, "watchlist.json 에 watchlist 항목이 비어 있습니다."
    return cfg, None


def load_env():
    """프로젝트 루트 .env 에서 네이버 키를 읽는다 (trip-advisor 패턴 재사용)."""
    cid = os.environ.get("NAVER_CLIENT_ID")
    sec = os.environ.get("NAVER_CLIENT_SECRET")
    if cid and sec:
        return cid, sec
    here = os.path.abspath(os.path.dirname(__file__))
    for _ in range(6):
        env_path = os.path.join(here, ".env")
        if os.path.exists(env_path):
            with open(env_path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    k, v = line.split("=", 1)
                    if k.strip() == "NAVER_CLIENT_ID":
                        cid = v.strip()
                    elif k.strip() == "NAVER_CLIENT_SECRET":
                        sec = v.strip()
            break
        here = os.path.dirname(here)
    return cid, sec


def auto_period_days(today=None):
    """요일 기반 조회 기간(일) 자동 계산.
    월요일(0) → 3일(금·토·일 포함), 화~금 → 1일(전일), 토·일 → 1일(수동 실행 대비).
    """
    today = today or datetime.datetime.now(KST)
    return 3 if today.weekday() == 0 else 1


def market_closed_info(d):
    """증시 휴장 여부 + 사유 + 판정 신뢰도.
    - 주말 / 법정공휴일(holidays 라이브러리, 음력·대체·임시 자동) / 증시 전용(근로자의날·연말폐장)
    - holidays 미설치 환경에서도 죽지 않고 주말+증시전용만 판정(fallback)하고 flag로 알린다.
    반환: (closed: bool, reason: str|None, check: "ok" | "weekday-only-fallback")
    """
    wd = d.weekday()
    if wd == 5:
        return True, "토요일", "ok"
    if wd == 6:
        return True, "일요일", "ok"
    # 증시 전용 휴장 (법정공휴일 아님 — 라이브러리로는 안 잡힘)
    if d.month == 5 and d.day == 1:
        return True, "근로자의날(증시 휴장)", "ok"
    if d.month == 12 and d.day == 31:
        return True, "연말 폐장일(증시 휴장)", "ok"
    try:
        import holidays  # noqa: PLC0415
        kr = holidays.SouthKorea(years=d.year)
        if d in kr:
            return True, kr.get(d), "ok"
        return False, None, "ok"
    except Exception:  # noqa: BLE001  라이브러리 없음 → 공휴일은 못 거름
        return False, None, "weekday-only-fallback"


def grade_media(name):
    for g, names in MEDIA_GRADE.items():
        if any(n in (name or "") for n in names):
            return g
    return "C"


def clean(text):
    text = re.sub(r"<[^>]+>", "", text or "")
    return html.unescape(text).strip()


def domain_of(url):
    m = re.search(r"https?://([^/]+)/", url or "")
    return m.group(1) if m else ""


def name_present(name, text):
    """종목명이 text 에 '경계' 단위로 등장하는지 (오태깅 차단).
    앞: 한글/영숫자가 아니어야 함. 뒤: 조사이거나 비(한글/영숫자)여야 함.
    → "이노테크의 증거금률"(조사) 통과 / "이노테크홀"(합성어) 차단.
    """
    pat = rf"(?<![가-힣A-Za-z0-9]){re.escape(name)}(?:{PARTICLES}|(?![가-힣A-Za-z0-9]))"
    return re.search(pat, text) is not None


def search(query, cid, sec, display=100, sort="date", retries=3):
    """검색. 성공 시 (data, None), 실패 시 (None, 에러설명)."""
    q = urllib.parse.quote(query)
    url = f"{NAVER_NEWS_API}?query={q}&display={display}&sort={sort}"
    req = urllib.request.Request(url, headers={
        "X-Naver-Client-Id": cid,
        "X-Naver-Client-Secret": sec,
    })
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                return json.load(r), None
        except urllib.error.HTTPError as e:
            if e.code == 429:
                msg = "일일 호출한도(또는 QPS) 초과"
            elif e.code in (401, 403):
                msg = "인증 오류 — API 키를 확인하세요"
            elif e.code >= 500:
                msg = f"네이버 서버 오류({e.code})"
            else:
                msg = f"HTTP {e.code}"
            if e.code in (429, 500, 502, 503) and attempt < retries - 1:
                time.sleep(0.5 * (2 ** attempt))  # 지수 백오프
                continue
            return None, msg
        except urllib.error.URLError as e:
            if attempt < retries - 1:
                time.sleep(0.5 * (2 ** attempt))
                continue
            return None, f"네트워크 오류: {e.reason}"
        except Exception as e:  # noqa: BLE001
            return None, str(e)
    return None, "재시도 모두 실패"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sort", default="date", choices=["date", "sim"])
    ap.add_argument("--days", type=int, default=None, help="조회 기간(일). 미지정 시 요일 기반 자동")
    args = ap.parse_args()

    cfg, cfg_err = load_config()
    if cfg_err:
        print(json.dumps({"has_error": True, "error": cfg_err}, ensure_ascii=False))
        sys.exit(1)

    cid, sec = load_env()
    if not cid or not sec:
        print(json.dumps({"has_error": True,
                          "error": ".env 의 NAVER_CLIENT_ID / NAVER_CLIENT_SECRET 가 없습니다."},
                         ensure_ascii=False))
        sys.exit(1)

    watchlist = cfg["watchlist"]
    macro_keywords = cfg.get("macro_keywords", [])
    macro_max = cfg.get("macro_max_items", 20)

    now = datetime.datetime.now(KST)
    closed, closed_reason, holiday_check = market_closed_info(now.date())
    days = args.days if args.days is not None else auto_period_days(now)
    cutoff = now - datetime.timedelta(days=days)
    # period_label: 자동(월요일 3일)일 때만 주말 표기, 그 외엔 N일 표기
    if args.days is None and days == 3:
        period_label = "금·토·일(주말 포함)"
    elif days == 1:
        period_label = "전일"
    else:
        period_label = f"최근 {days}일"

    targets = [(s["name"], s["code"]) for s in watchlist] + [(kw, None) for kw in macro_keywords]

    seen = {}        # url -> item
    errors = []
    for query, code in targets:
        data, err = search(query, cid, sec, sort=args.sort)
        time.sleep(0.12)  # rate limit 방어 (QPS)
        if err:
            errors.append(f"'{query}' 검색 실패: {err}")
            continue
        for it in data.get("items", []):
            try:
                pub = datetime.datetime.strptime(it["pubDate"], "%a, %d %b %Y %H:%M:%S %z")
            except (KeyError, ValueError):
                continue
            if pub < cutoff:
                continue
            link = it.get("originallink") or it.get("link") or ""
            key = link or it.get("title", "")
            tag = code or "_macro"
            if key in seen:
                if tag not in seen[key]["tags"]:
                    seen[key]["tags"].append(tag)
                continue
            dom = domain_of(link)
            grade = grade_media(dom)
            seen[key] = {
                "title": clean(it.get("title", "")),
                "summary": clean(it.get("description", "")),
                "link": link if link.startswith(("http://", "https://")) else "",
                "pubDate": pub.isoformat(),
                "hours_ago": round((now - pub).total_seconds() / 3600, 1),
                "source_domain": dom,
                "media_grade": grade,
                "unverified": grade == "C",   # C급 단독 → AI가 "(미확인)" 표기
                "tags": [tag],
            }

    # 종목별 그룹핑 — 정규식 경계 매칭으로 오태깅 최종 차단
    code_to_name = {s["code"]: s["name"] for s in watchlist}
    by_stock = {s["code"]: {"name": s["name"], "code": s["code"], "items": []} for s in watchlist}
    macro_items = []
    for art in seen.values():
        haystack = art["title"] + " " + art["summary"]
        placed = False
        for tag in art["tags"]:
            if tag in by_stock and name_present(code_to_name[tag], haystack):
                by_stock[tag]["items"].append(art)
                placed = True
        if not placed and "_macro" in art["tags"]:
            macro_items.append(art)

    for v in by_stock.values():
        v["items"].sort(key=lambda a: a["pubDate"], reverse=True)
    # 매크로: 최신순 정렬 후, 안정정렬로 등급(A→B→C) 우선 → 상한 truncate
    grade_rank = {"A": 0, "B": 1, "C": 2}
    macro_items.sort(key=lambda a: a["pubDate"], reverse=True)
    macro_items.sort(key=lambda a: grade_rank.get(a["media_grade"], 3))
    macro_items = macro_items[:macro_max]

    out = {
        "generated_at": now.isoformat(),
        "weekday": now.strftime("%a"),
        "market_closed": closed,                 # True면 증시 휴장 → 발송 스킵 권장
        "market_closed_reason": closed_reason,
        "holiday_check": holiday_check,           # "weekday-only-fallback"면 공휴일 미판정
        "period_days": days,
        "period_label": period_label,
        "sort": args.sort,
        "total_unique": len(seen),
        "stocks": list(by_stock.values()),
        "macro": macro_items,
        "macro_truncated_to": macro_max,
        "errors": errors,
        "has_error": bool(errors),
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))

    # 데이터 0건 + 에러 = 수집 전체 실패 → exit 1 (자동 루틴이 인지)
    if len(seen) == 0 and errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
