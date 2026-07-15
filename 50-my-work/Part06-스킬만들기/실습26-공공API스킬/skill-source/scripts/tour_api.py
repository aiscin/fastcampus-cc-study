#!/usr/bin/env python3
"""TourAPI 호출 스크립트 — 한국관광공사 국문관광정보 (KorService2).

매번 똑같이 가져와야 하는 API 호출·JSON 정리만 담당한다.
일정 배치·가이드 글쓰기는 SKILL.md(AI)가 맡는다.

사용:
  python3 tour_api.py keyword  "부산"         [--rows 10]   # 장소명 검색
  python3 tour_api.py festival "20260701"     [--rows 10]   # 이 날짜 이후 열리는 축제
  python3 tour_api.py area     "구미"          [--rows 15]   # 지역 관광지 (시군구 자동 해석)
  python3 tour_api.py food     "구미"          [--rows 15]   # 지역 음식점 (사진 포함)
  python3 tour_api.py stay     "구미"          [--rows 15]   # 지역 숙박 (사진 포함)
  python3 tour_api.py detail   "126508"                     # contentId 공통 상세
  python3 tour_api.py intro    "2766562" --type 39          # 메뉴·영업시간(39)/체크인(32)/운영(12)
  python3 tour_api.py images   "126508"      [--rows 5]     # 추가 사진 목록

출력: JSON (stdout). 호출 실패 시 {"error": "..."} 와 종료코드 1.
"""
import os
import sys
import json
import argparse

import requests

BASE = "http://apis.data.go.kr/B551011/KorService2"

# 지역명 → areaCode (자주 쓰는 것만; 나머지는 area 액션 결과로 확인)
AREA_CODES = {
    "서울": 1, "인천": 2, "대전": 3, "대구": 4, "광주": 5, "부산": 6,
    "울산": 7, "세종": 8, "경기": 31, "강원": 32, "충북": 33, "충남": 34,
    "경북": 35, "경남": 36, "전북": 37, "전남": 38, "제주": 39,
}


def load_key():
    """프로젝트 루트 .env 에서 TOURAPI_SERVICE_KEY 를 읽는다."""
    key = os.environ.get("TOURAPI_SERVICE_KEY")
    if key:
        return key
    # 스크립트 기준 상위로 올라가며 .env 탐색
    here = os.path.dirname(os.path.abspath(__file__))
    for _ in range(6):
        env_path = os.path.join(here, ".env")
        if os.path.exists(env_path):
            with open(env_path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("#") or "=" not in line:
                        continue
                    k, v = line.split("=", 1)
                    if k.strip() == "TOURAPI_SERVICE_KEY":
                        return v.strip()
        here = os.path.dirname(here)
    return None


def call(endpoint, extra):
    key = load_key()
    if not key or key == "YOUR_KEY_HERE":
        return {"error": ".env 의 TOURAPI_SERVICE_KEY 가 설정되지 않았습니다."}
    params = {
        "serviceKey": key,        # requests 가 자동 인코딩 → 디코딩 키 사용
        "MobileOS": "ETC",
        "MobileApp": "TripAdvisor",
        "_type": "json",
        "numOfRows": extra.pop("rows", 10),
        "pageNo": 1,
    }
    params.update(extra)
    url = f"{BASE}/{endpoint}"
    try:
        r = requests.get(url, params=params, timeout=15)
    except requests.RequestException as e:
        return {"error": f"네트워크 오류: {e}"}
    if r.status_code != 200:
        return {"error": f"HTTP {r.status_code}", "body": r.text[:300]}
    try:
        data = r.json()
    except ValueError:
        # 인증 실패 등은 XML 에러로 돌아온다
        return {"error": "JSON 파싱 실패 (키/파라미터 확인)", "body": r.text[:300]}
    # 표준 응답에서 아이템만 추려서 반환
    try:
        body = data["response"]["body"]
        items = body.get("items")
        items = items.get("item", []) if isinstance(items, dict) else []
        return {"total": body.get("totalCount", 0), "items": items}
    except (KeyError, TypeError):
        return {"error": "예상과 다른 응답 구조", "raw": data}


def _strip(s):
    return s.replace("시", "").replace("군", "").replace("구", "").strip()


def geocode(name):
    """지역명 → (areaCode, sigunguCode). '구미' 같은 시군구면 부모 도까지 찾는다.
    광역시/도 이름이면 (areaCode, None)."""
    if name in AREA_CODES:
        return str(AREA_CODES[name]), None
    nm = _strip(name)
    for area in AREA_CODES.values():
        res = call("areaCode2", {"areaCode": area, "rows": 50})
        if res.get("error"):
            continue
        for it in res.get("items", []):
            sg = it.get("name", "")
            if name in sg or _strip(sg) == nm:
                return str(area), it.get("code")
    return None, None


def area_params(region, extra):
    """지역명을 areaCode(+sigunguCode)로 풀어 areaBasedList2 파라미터를 만든다.
    arrange=O → 대표이미지 있는 항목 우선(제목순)."""
    code = AREA_CODES.get(region)
    if code:
        params = {"areaCode": code}
    else:
        ac, sg = geocode(region)
        if not ac:
            return None
        params = {"areaCode": ac}
        if sg:
            params["sigunguCode"] = sg
    params.update({"arrange": "O"})
    params.update(extra)
    return params


def main():
    p = argparse.ArgumentParser()
    p.add_argument("action", choices=[
        "keyword", "festival", "area", "stay", "food", "detail", "intro", "images"])
    p.add_argument("value")
    p.add_argument("--rows", type=int, default=10)
    p.add_argument("--type", default="12",
                   help="contentTypeId (intro 용: 12관광지/15축제/32숙박/39음식점)")
    args = p.parse_args()

    rows = args.rows
    if args.action == "keyword":
        out = call("searchKeyword2", {"keyword": args.value, "rows": rows})
    elif args.action == "festival":
        out = call("searchFestival2", {"eventStartDate": args.value, "rows": rows})
    elif args.action in ("area", "stay", "food"):
        type_map = {"area": "12", "stay": "32", "food": "39"}
        params = area_params(args.value, {"contentTypeId": type_map[args.action], "rows": rows})
        if params is None:
            out = {"error": f"지역을 찾지 못함: {args.value} (시군구명을 확인하세요)"}
        else:
            out = call("areaBasedList2", params)
    elif args.action == "detail":
        out = call("detailCommon2", {"contentId": args.value, "rows": 1})
    elif args.action == "intro":
        # 운영시간·메뉴·체크인 등 (타입별 필드 다름). --type 으로 지정.
        out = call("detailIntro2", {
            "contentId": args.value, "contentTypeId": args.type, "rows": 1})
    elif args.action == "images":
        out = call("detailImage2", {
            "contentId": args.value, "imageYN": "Y", "rows": rows})

    print(json.dumps(out, ensure_ascii=False, indent=2))
    if isinstance(out, dict) and out.get("error"):
        sys.exit(1)


if __name__ == "__main__":
    main()
