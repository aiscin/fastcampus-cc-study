#!/usr/bin/env python3
"""장소 좌표 → 한 장의 동선 지도 PNG.

TourAPI 가 주는 좌표(mapx=경도, mapy=위도)를 받아 OpenStreetMap 타일 위에
번호 마커 + Day 별 경로선을 그려 한 장의 지도 이미지로 저장한다.
추가 설치 없이 requests + PIL + matplotlib(폰트) 만 사용.

입력 (JSON, --input 파일 또는 stdin):
  [
    {"name": "금오산도립공원", "mapx": "128.34", "mapy": "36.10", "day": 1},
    {"name": "금리단길",       "mapx": "128.33", "mapy": "36.12", "day": 1},
    {"name": "도리사",         "mapx": "128.40", "mapy": "36.20", "day": 2}
  ]
  - mapx/mapy: TourAPI 좌표(경도/위도). day: 같은 day 끼리 입력 순서대로 선을 잇는다.

사용:
  python3 make_map.py --input places.json --out map.png --title "구미 2박3일"
  cat places.json | python3 make_map.py --out map.png

출력: PNG 저장 + JSON {"image": 경로, "zoom": Z, "legend": [{n,name,day}]} (stdout).
번호↔장소명 매핑(legend)을 가이드에 표로 함께 넣으면 된다 (지도엔 번호만 표기).
"""
import os
import io
import sys
import json
import math
import argparse

import requests
from PIL import Image, ImageDraw, ImageFont

TILE = 256
DAY_COLORS = [
    (220, 50, 50), (40, 110, 210), (40, 160, 70),
    (230, 140, 20), (150, 60, 180), (20, 160, 170),
]


def latlon_to_tilexy(lat, lon, z):
    n = 2 ** z
    x = (lon + 180.0) / 360.0 * n
    lat_r = math.radians(lat)
    y = (1.0 - math.log(math.tan(lat_r) + 1 / math.cos(lat_r)) / math.pi) / 2.0 * n
    return x, y


def choose_zoom(lats, lons, max_span_tiles=4):
    for z in range(15, 8, -1):
        xs = [latlon_to_tilexy(la, lo, z)[0] for la, lo in zip(lats, lons)]
        ys = [latlon_to_tilexy(la, lo, z)[1] for la, lo in zip(lats, lons)]
        if (max(xs) - min(xs) <= max_span_tiles) and (max(ys) - min(ys) <= max_span_tiles):
            return z
    return 11


def fetch_tile(z, x, y):
    url = f"https://tile.openstreetmap.org/{z}/{x}/{y}.png"
    r = requests.get(url, headers={"User-Agent": "trip-advisor-skill/1.0 (study)"}, timeout=15)
    r.raise_for_status()
    return Image.open(io.BytesIO(r.content)).convert("RGBA")


def load_font(size):
    import matplotlib
    p = os.path.join(os.path.dirname(matplotlib.__file__),
                     "mpl-data", "fonts", "ttf", "DejaVuSans-Bold.ttf")
    try:
        return ImageFont.truetype(p, size)
    except Exception:
        return ImageFont.load_default()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", help="장소 JSON (없으면 stdin)")
    p.add_argument("--out", default="route-map.png")
    p.add_argument("--title", default="")
    args = p.parse_args()

    raw = open(args.input, encoding="utf-8").read() if args.input else sys.stdin.read()
    try:
        places = json.loads(raw)
    except ValueError:
        print(json.dumps({"error": "입력 JSON 파싱 실패"}, ensure_ascii=False))
        sys.exit(1)

    # 좌표 유효한 것만
    pts = []
    for pl in places:
        try:
            lon, lat = float(pl["mapx"]), float(pl["mapy"])
        except (KeyError, ValueError, TypeError):
            continue
        if lat and lon:
            pts.append({"name": pl.get("name", "?"), "lat": lat, "lon": lon,
                        "day": int(pl.get("day", 1))})
    if not pts:
        print(json.dumps({"error": "유효한 좌표가 없음 (mapx/mapy 확인)"}, ensure_ascii=False))
        sys.exit(1)

    lats = [q["lat"] for q in pts]
    lons = [q["lon"] for q in pts]
    z = choose_zoom(lats, lons)

    # 타일 범위 (1칸 여백)
    txs = [latlon_to_tilexy(la, lo, z)[0] for la, lo in zip(lats, lons)]
    tys = [latlon_to_tilexy(la, lo, z)[1] for la, lo in zip(lats, lons)]
    x0, x1 = int(math.floor(min(txs))) - 1, int(math.floor(max(txs))) + 1
    y0, y1 = int(math.floor(min(tys))) - 1, int(math.floor(max(tys))) + 1

    canvas = Image.new("RGBA", ((x1 - x0 + 1) * TILE, (y1 - y0 + 1) * TILE), (240, 240, 240, 255))
    try:
        for tx in range(x0, x1 + 1):
            for ty in range(y0, y1 + 1):
                tile = fetch_tile(z, tx, ty)
                canvas.paste(tile, ((tx - x0) * TILE, (ty - y0) * TILE))
    except requests.RequestException as e:
        print(json.dumps({"error": f"지도 타일 다운로드 실패: {e}"}, ensure_ascii=False))
        sys.exit(1)

    draw = ImageDraw.Draw(canvas)

    def px(lat, lon):
        tx, ty = latlon_to_tilexy(lat, lon, z)
        return ((tx - x0) * TILE, (ty - y0) * TILE)

    # Day 별 경로선 (입력 순서대로)
    days = sorted({q["day"] for q in pts})
    for day in days:
        seq = [q for q in pts if q["day"] == day]
        color = DAY_COLORS[(day - 1) % len(DAY_COLORS)]
        coords = [px(q["lat"], q["lon"]) for q in seq]
        if len(coords) >= 2:
            draw.line(coords, fill=color + (230,), width=5, joint="curve")

    # 마커 + 번호 (전체 입력 순서로 1..N)
    font = load_font(20)
    legend = []
    for i, q in enumerate(pts, 1):
        x, y = px(q["lat"], q["lon"])
        color = DAY_COLORS[(q["day"] - 1) % len(DAY_COLORS)]
        r = 15
        draw.ellipse([x - r, y - r, x + r, y + r], fill=color + (255,),
                     outline=(255, 255, 255, 255), width=3)
        tw = draw.textlength(str(i), font=font)
        draw.text((x - tw / 2, y - 11), str(i), fill=(255, 255, 255, 255), font=font)
        legend.append({"n": i, "name": q["name"], "day": q["day"]})

    # 제목
    if args.title:
        tf = load_font(26)
        draw.rectangle([0, 0, canvas.width, 38], fill=(0, 0, 0, 160))
        draw.text((10, 6), args.title, fill=(255, 255, 255, 255), font=tf)

    canvas.convert("RGB").save(args.out, "PNG")
    print(json.dumps({"image": args.out, "zoom": z, "legend": legend},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
