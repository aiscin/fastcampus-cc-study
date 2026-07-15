#!/usr/bin/env python3
"""
crawl_kream.py — KREAM 키워드 트렌드 수집 (결정론 단계)

키워드 하나를 받아 남성/여성 인기순 URL을 조립하고, curl_cffi safari TLS 위장으로
봇 차단을 우회해 상품 50개를 6컬럼(브랜드·상품명·가격·관심·리뷰·거래)으로 수집한다.
분석·리포트는 SKILL.md(AI)가 맡고, 이 스크립트는 "같은 입력 → 같은 데이터"만 보장한다.

사용:
  python3 crawl_kream.py "반팔티" --gender both --outdir ./artifacts
  python3 crawl_kream.py "맨투맨" --gender female

의존성: curl_cffi, beautifulsoup4  (없으면 자동 설치 시도)
"""
import sys, os, re, json, argparse, datetime, subprocess, urllib.parse

def ensure_deps():
    try:
        import curl_cffi, bs4  # noqa
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "-q",
                        "curl_cffi", "beautifulsoup4", "--break-system-packages"], check=False)

ensure_deps()
from curl_cffi import requests as creq
from bs4 import BeautifulSoup

SORT = {"male": "male_popularity", "female": "female_popularity"}
LABEL = {"male": "남성", "female": "여성"}


def fetch(keyword, gender):
    """curl_cffi safari TLS 위장으로 KREAM 검색 페이지 수집. (KREAM은 이 방식에 1회 성공 — 검증됨)"""
    kw = urllib.parse.quote(keyword)
    url = f"https://kream.co.kr/search?keyword={kw}&tab=products&sort={SORT[gender]}"
    root = "https://kream.co.kr/"
    r = creq.get(url, impersonate="safari", headers={"Referer": root}, timeout=25)
    if r.status_code != 200 or "product_card" not in r.text:
        raise RuntimeError(f"수집 실패 status={r.status_code} (차단 가능성) — gender={gender}")
    return r.text, url


def grab_label(parts, label):
    """라벨('관심'/'리뷰'/'거래') 바로 다음 토큰을 집는다. 위치가 밀려도 라벨 기준이라 안정적."""
    for i, p in enumerate(parts):
        if p == label or p.endswith(label):
            if i + 1 < len(parts):
                return parts[i + 1]
    return ""


def parse(html):
    soup = BeautifulSoup(html, "html.parser")
    rows = []
    for c in soup.select("[class*='product_card']"):
        parts = [p.strip() for p in c.get_text("|", strip=True).split("|") if p.strip()]
        if len(parts) < 3:
            continue
        brand = parts[0]
        price_i = next((i for i, p in enumerate(parts) if re.search(r"\d[\d,]*원", p)), None)
        price = parts[price_i] if price_i is not None else "-"
        name = " ".join(parts[1:price_i]) if price_i and price_i > 1 else parts[1]
        name = re.sub(r"\s+", " ", name).strip()
        rows.append({
            "brand": brand, "name": name, "price": price,
            "wish": grab_label(parts, "관심"),
            "review": grab_label(parts, "리뷰"),
            "trade": grab_label(parts, "거래"),
        })
    return rows


def to_markdown(keyword, gender, rows, date):
    from collections import Counter
    out = [f"# KREAM {LABEL[gender]} 인기순 — '{keyword}' ({date})\n",
           f"> 출처: kream.co.kr · sort={SORT[gender]} · 수집: curl_cffi safari TLS",
           f"> 총 {len(rows)}개 · 6컬럼\n",
           "| 순위 | 브랜드 | 상품명 | 가격 | 관심 | 리뷰 | 거래 |",
           "|---|---|---|---|---|---|---|"]
    for i, r in enumerate(rows, 1):
        out.append(f"| {i} | {r['brand']} | {r['name']} | {r['price']} | {r['wish']} | {r['review']} | {r['trade']} |")
    cnt = Counter(r["brand"] for r in rows)
    out.append(f"\n## {LABEL[gender]} 인기 브랜드 집계\n\n| 브랜드 | 상품 수 |\n|---|---|")
    for b, n in cnt.most_common():
        out.append(f"| {b} | {n} |")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description="KREAM 키워드 트렌드 수집")
    ap.add_argument("keyword", nargs="?", default="반팔티", help="검색 키워드 (기본: 반팔티)")
    ap.add_argument("--gender", choices=["male", "female", "both"], default="both")
    ap.add_argument("--outdir", default="./artifacts", help="저장 폴더 (기본: ./artifacts)")
    args = ap.parse_args()

    date = datetime.date.today().isoformat()
    genders = ["male", "female"] if args.gender == "both" else [args.gender]
    os.makedirs(args.outdir, exist_ok=True)

    result = {"keyword": args.keyword, "date": date, "files": []}
    for g in genders:
        html, url = fetch(args.keyword, g)
        rows = parse(html)
        if not rows:
            raise RuntimeError(f"상품 0개 파싱 — 키워드 '{args.keyword}' 결과 없음? (gender={g})")
        path = os.path.join(args.outdir, f"kream-{args.keyword}-{LABEL[g]}-{date}.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(to_markdown(args.keyword, g, rows, date))
        result["files"].append({"gender": g, "count": len(rows), "path": path, "url": url})
        print(f"✓ {LABEL[g]} {len(rows)}개 → {path}", file=sys.stderr)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
