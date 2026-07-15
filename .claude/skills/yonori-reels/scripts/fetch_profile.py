#!/usr/bin/env python3
"""인스타그램 웹 프로필 API 수집 (로그인 불필요).

사용: python3 fetch_profile.py --username travel_yonori --out data/profile-raw.json
종료 코드: 0 성공 / 2 차단(401·403·429 — 수동 캡션 폴백 필요) / 1 기타 오류
"""
import argparse
import json
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone

API = "https://i.instagram.com/api/v1/users/web_profile_info/?username={username}"
HEADERS = {
    "x-ig-app-id": "936619743392459",
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/125.0 Safari/537.36"
    ),
}


def fetch(username: str) -> dict:
    req = urllib.request.Request(API.format(username=username), headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def extract(raw: dict) -> dict:
    user = raw["data"]["user"]
    followers = user["edge_followed_by"]["count"]
    media = user.get("edge_owner_to_timeline_media", {})
    posts = []
    for edge in media.get("edges", []):
        node = edge["node"]
        caps = node.get("edge_media_to_caption", {}).get("edges", [])
        caption = caps[0]["node"]["text"] if caps else ""
        views = node.get("video_view_count")
        posts.append({
            "type": node.get("__typename"),          # GraphVideo=릴스/영상, GraphSidecar=캐러셀
            "caption": caption,
            "video_views": views,
            "likes": node.get("edge_liked_by", {}).get("count"),
            "comments": node.get("edge_media_to_comment", {}).get("count"),
            "taken_at": node.get("taken_at_timestamp"),
            "shortcode": node.get("shortcode"),
            "viral_ratio": round(views / followers, 2) if views and followers else None,
        })
    return {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "username": user.get("username"),
        "biography": user.get("biography"),
        "followers": followers,
        "total_posts": media.get("count"),
        "posts": posts,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--username", default="travel_yonori")
    ap.add_argument("--out", default="data/profile-raw.json")
    args = ap.parse_args()

    try:
        raw = fetch(args.username)
    except urllib.error.HTTPError as e:
        if e.code in (401, 403, 429):
            print(f"BLOCKED: HTTP {e.code} — 인스타 차단. 수동 캡션 폴백 필요 "
                  f"(조회수 없음 → 성과 신호 분석 비활성)", file=sys.stderr)
            return 2
        print(f"HTTP {e.code}: {e.reason}", file=sys.stderr)
        return 1
    except Exception as e:  # 네트워크·타임아웃·JSON 오류
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    try:
        data = extract(raw)
    except (KeyError, TypeError) as e:
        # 비공식 API — 응답 구조가 바뀐 경우
        print(f"SCHEMA_CHANGED: 응답 구조가 예상과 다름 ({e}). "
              f"API 스키마 변화 가능성 — 스크립트 수정 필요", file=sys.stderr)
        return 1

    import os
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(json.dumps({
        "ok": True, "out": args.out, "followers": data["followers"],
        "posts_collected": len(data["posts"]),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
