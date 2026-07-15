#!/usr/bin/env python3
"""여행 촬영본 인덱스 생성: PowerShell 목록(TSV) → 기기별 시간 규칙 적용 → clip-index.csv.

사용:
  python3 index_clips.py --listing listing.tsv --tz-offset -6 --out clip-index.csv

listing.tsv 형식 (탭 구분): FullName \t Length(bytes) \t LastWriteTime(yyyy-MM-dd HH:mm:ss)
--tz-offset: 현지시각 = 한국시각 + offset (튀르키예 = -6)

기기별 규칙(2026-07-07 실측): 삼성 파일명=현지시각 / 아이폰·드론 파일명≈한국시각 /
고프로 LWT=백업일(무의미) / 카메라 IMG_nnnn은 LWT로 추정(신뢰 낮음).
상세: references/clip-index-guide.md
"""
import argparse
import csv
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path, PureWindowsPath

VIDEO_EXT = {".mp4", ".mov", ".avi", ".mts"}
PHOTO_EXT = {".jpg", ".jpeg", ".png", ".heic", ".dng"}

SAMSUNG = re.compile(r"(20\d{6})_(\d{6})")          # 20260525_052721
IPHONE = re.compile(r"(20\d{6})(\d{6})_IMG")        # 20260527234628_IMG_6136
DJI = re.compile(r"dji_fly_(20\d{6})_(\d{6})")      # dji_fly_20260528_195154


def parse_ts(d: str, t: str) -> datetime:
    return datetime.strptime(d + t, "%Y%m%d%H%M%S")


def classify(path: str, lwt: datetime, tz: int):
    """(device, local_time, korea_time, confidence) — 시각 불명이면 None."""
    name = PureWindowsPath(path).name  # Windows 경로(\) 리스팅을 리눅스에서 처리
    if m := DJI.search(name):
        kst = parse_ts(m.group(1), m.group(2))
        return "드론", kst + timedelta(hours=tz), kst, "중"
    if m := IPHONE.search(name):
        kst = parse_ts(m.group(1), m.group(2))
        return "아이폰", kst + timedelta(hours=tz), kst, "중"
    if m := SAMSUNG.search(name):
        local = parse_ts(m.group(1), m.group(2))
        return "삼성폰", local, local - timedelta(hours=tz), "상"
    if "고프로" in path or name.upper().startswith("G"):
        return "고프로", None, None, "불명(내용으로 판정)"
    return "카메라/기타", lwt + timedelta(hours=tz), lwt, "하(LWT 추정)"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--listing", required=True)
    ap.add_argument("--tz-offset", type=int, required=True,
                    help="현지시각 = 한국시각 + offset (튀르키예 -6)")
    ap.add_argument("--out", default="clip-index.csv")
    args = ap.parse_args()

    rows = []
    for line in Path(args.listing).read_text(encoding="utf-8-sig").splitlines():
        parts = line.strip().split("\t")
        if len(parts) != 3:
            continue
        full, size, lwt_s = parts
        ext = PureWindowsPath(full).suffix.lower()
        if ext not in VIDEO_EXT | PHOTO_EXT:
            continue
        try:
            lwt = datetime.strptime(lwt_s, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            continue
        device, local, kst, conf = classify(full, lwt, args.tz_offset)
        rows.append({
            "path": full,
            "name": PureWindowsPath(full).name,
            "type": "video" if ext in VIDEO_EXT else "photo",
            "device": device,
            "local_time": local.strftime("%Y-%m-%d %H:%M") if local else "",
            "korea_time": kst.strftime("%Y-%m-%d %H:%M") if kst else "",
            "confidence": conf,
            "size_mb": round(int(size) / 1048576, 1),
            "low_quality": 1 if "low_quality" in full.lower() else "",
        })

    rows.sort(key=lambda r: (r["local_time"] or "9999", r["name"]))
    with open(args.out, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"OK {len(rows)} files -> {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
