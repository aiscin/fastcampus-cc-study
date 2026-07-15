#!/usr/bin/env python3
"""render_cards.py — card-news.html의 각 .card를 PNG로 캡처 (미리보기·발행용).

사용: python3 render_cards.py <workdir> [--only 3,4,6]
출력: <workdir>/preview/card-NN.png (1080x1350 상당, 2x)
"""
import sys, argparse
from pathlib import Path

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("workdir")
    ap.add_argument("--only",default=None)
    args=ap.parse_args()
    work=Path(args.workdir).resolve()
    html=work/"card-news.html"
    prev=work/"preview"; prev.mkdir(exist_ok=True)
    only=set(int(x) for x in args.only.split(",")) if args.only else None

    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b=p.chromium.launch()
        # 카드 max-width 480 → 배율 2.25로 정확히 1080x1350 출력 (인스타 권장)
        pg=b.new_page(viewport={"width":1100,"height":1400}, device_scale_factor=2.25)
        pg.goto(html.as_uri())
        # woff2 웹폰트가 완전히 로드된 뒤 캡처 (폴백 폰트로 찍히는 것 방지)
        pg.evaluate("document.fonts.ready")
        pg.wait_for_function("document.fonts.status === 'loaded'")
        pg.wait_for_timeout(400)
        cards=pg.locator(".card")
        n=cards.count()
        for i in range(n):
            no=i+1
            if only and no not in only: continue
            cards.nth(i).screenshot(path=str(prev/f"card-{no:02d}.png"))
            print(f"✓ card-{no:02d}")
        b.close()
    print(f"→ {prev}")

if __name__=="__main__":
    main()
