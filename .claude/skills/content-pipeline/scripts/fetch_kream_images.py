#!/usr/bin/env python3
"""fetch_kream_images.py — KREAM 인기순 상품 썸네일 URL 수집 + 선택 다운로드.

content-pipeline [3.5] 실사진 하이브리드용. 기존 crawl_kream.py가 표만 긁었으므로,
여기선 상품 카드의 브랜드·상품명 + 썸네일 이미지 URL을 함께 수집한다.
개인 학습·포트폴리오 용도 전제 · 저장 파일에 출처(KREAM) 캡션 의무.

사용:
  # 1) 목록만: 남·여 인기순 상품+이미지URL을 products.json으로
  python3 fetch_kream_images.py "반팔티" --list --outdir <workdir>
  # 2) 특정 순위 다운로드: 남성 1위, 여성 1위 등
  python3 fetch_kream_images.py "반팔티" --download male:1,4 female:1,5 --outdir <workdir>
"""
import sys, os, re, json, argparse, urllib.parse, subprocess

def ensure():
    try:
        import curl_cffi, bs4  # noqa
    except ImportError:
        subprocess.run([sys.executable,"-m","pip","install","-q","curl_cffi","beautifulsoup4","--break-system-packages"], check=False)
ensure()
from curl_cffi import requests as creq
from bs4 import BeautifulSoup

SORT={"male":"male_popularity","female":"female_popularity"}
LABEL={"male":"남성","female":"여성"}

def fetch(keyword, gender):
    kw=urllib.parse.quote(keyword)
    url=f"https://kream.co.kr/search?keyword={kw}&tab=products&sort={SORT[gender]}"
    r=creq.get(url, impersonate="safari", headers={"Referer":"https://kream.co.kr/"}, timeout=25)
    if r.status_code!=200 or "product_card" not in r.text:
        raise RuntimeError(f"수집 실패 status={r.status_code} gender={gender}")
    return r.text

def img_of(card):
    """상품 카드 내 썸네일 URL 추출 (lazy-load 대비 data-src 우선)."""
    for im in card.select("img"):
        for attr in ("data-src","data-original","src"):
            v=im.get(attr,"")
            if v and re.search(r"\.(jpg|jpeg|png|webp)", v, re.I) and "product" in v.lower() or (v and "pstatic" in v):
                return v.split("?")[0]
    # picture > source
    s=card.select_one("source")
    if s and s.get("srcset"):
        return s["srcset"].split()[0].split("?")[0]
    return ""

def parse(html):
    soup=BeautifulSoup(html,"html.parser")
    out=[]
    for c in soup.select("[class*='product_card']"):
        parts=[p.strip() for p in c.get_text("|",strip=True).split("|") if p.strip()]
        if len(parts)<2: continue
        brand=parts[0]
        price_i=next((i for i,p in enumerate(parts) if re.search(r"\d[\d,]*원",p)),None)
        name=" ".join(parts[1:price_i]) if price_i and price_i>1 else parts[1]
        out.append({"brand":brand,"name":re.sub(r"\s+"," ",name).strip(),"img":img_of(c)})
    return out

def download(url, path):
    r=creq.get(url, impersonate="safari", headers={"Referer":"https://kream.co.kr/"}, timeout=25)
    if r.status_code==200 and r.content:
        open(path,"wb").write(r.content); return True
    return False

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("keyword",nargs="?",default="반팔티")
    ap.add_argument("--outdir",default=".")
    ap.add_argument("--list",action="store_true")
    ap.add_argument("--download",nargs="*",default=[],help="예: male:1,4 female:1,5")
    args=ap.parse_args()

    data={}
    for g in ("male","female"):
        rows=parse(fetch(args.keyword,g))
        data[g]=rows
        print(f"✓ {LABEL[g]} {len(rows)}개 (이미지 있는 것 {sum(1 for r in rows if r['img'])}개)", file=sys.stderr)

    os.makedirs(args.outdir, exist_ok=True)
    if args.list or not args.download:
        p=os.path.join(args.outdir,"products.json")
        json.dump(data, open(p,"w",encoding="utf-8"), ensure_ascii=False, indent=2)
        print(f"→ 목록 저장 {p}")
        # 미리보기
        for g in ("male","female"):
            print(f"\n[{LABEL[g]} TOP5]")
            for i,r in enumerate(data[g][:5],1):
                print(f"  {i}. {r['brand']} {r['name'][:30]} | img={'O' if r['img'] else 'X'}")

    if args.download:
        pdir=os.path.join(args.outdir,"images","products"); os.makedirs(pdir,exist_ok=True)
        for spec in args.download:
            g,ranks=spec.split(":")
            for rk in ranks.split(","):
                idx=int(rk)-1
                if idx<0 or idx>=len(data[g]): continue
                r=data[g][idx]
                if not r["img"]:
                    print(f"  ✗ {g}#{rk} 이미지 URL 없음"); continue
                ext=os.path.splitext(r["img"])[1] or ".jpg"
                out=os.path.join(pdir,f"{g}-{int(rk):02d}{ext}")
                ok=download(r["img"],out)
                print(f"  {'✓' if ok else '✗'} {g}#{rk} {r['brand']} {r['name'][:24]} → {out if ok else '실패'}")

if __name__=="__main__":
    main()
