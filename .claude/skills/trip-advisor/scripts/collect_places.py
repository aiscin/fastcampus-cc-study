#!/usr/bin/env python3
"""블로그·유튜브 장소 후보 → TourAPI 검증·정형화·신뢰도 점수.

AI(SKILL.md)가 블로그/유튜브를 읽고 뽑은 "장소 후보"를 받아서,
각 장소를 TourAPI searchKeyword2 로 조회해 정형 데이터(좌표·주소·사진)를
붙이고, 신뢰도 점수로 정렬한다. 매번 같은 입력 → 같은 결과.

입력 (JSON, --input 파일 또는 stdin):
  [
    {"name": "흰여울문화마을", "mentions": 5},
    {"name": "감천문화마을",   "mentions": 4},
    {"name": "어느카페",       "mentions": 1}
  ]
  - name:     블로그/유튜브에서 추출한 장소 이름
  - mentions: 몇 개의 글/영상에 등장했나 (큐레이션 신뢰 신호)

사용:
  python3 collect_places.py --input candidates.json [--area 부산]
  cat candidates.json | python3 collect_places.py --area 부산

출력 (JSON, 점수 내림차순):
  각 장소에 api_found / addr1 / mapx / mapy / firstimage / contentid /
  contenttypeid / tel / score / verdict 부착.

verdict 기준:
  ⭐필수   : 여러 글 등장(mentions>=3) + API 매칭
  ○추천    : API 매칭 (mentions 1~2)
  🔸블로그만: API 에 없음 (개인 신상 가게 등) — 버리지 말고 따로 표기
"""
import os
import sys
import json
import argparse
from difflib import SequenceMatcher

# 같은 폴더의 tour_api.call() 재사용
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tour_api import call  # noqa: E402


def norm(s):
    return "".join(s.split()).lower()


def best_match(name, items, area=""):
    """API 결과 중 이름이 가장 비슷한 항목과 유사도(0~1)를 반환.
    area 가 주어지면 주소(addr1)에 지역명이 든 항목만 후보로 좁힌다."""
    if area:
        scoped = [it for it in items if area in (it.get("addr1") or "")]
        if scoped:
            items = scoped
    target = norm(name)
    best, best_ratio = None, 0.0
    for it in items:
        title = it.get("title", "")
        ratio = SequenceMatcher(None, target, norm(title)).ratio()
        # 부분 포함이면 가산 (블로그 "광안리 더베이101" vs API "더베이101")
        if target in norm(title) or norm(title) in target:
            ratio = max(ratio, 0.85)
        if ratio > best_ratio:
            best, best_ratio = it, ratio
    return best, best_ratio


# 출처 등급 가중치 (research-method.md 의 여행용 A~E).
# E(협찬/광고)는 점수를 깎아 광고성 장소를 끌어내린다.
GRADE_WEIGHT = {"A": 3, "B": 2, "C": 1, "D": 0, "E": -3}


def score(mentions, api_found, match_ratio, grade=""):
    """큐레이션(mentions) + 검증(API) + 출처 등급 결합 점수."""
    s = mentions * 2
    if api_found:
        s += 5 + round(match_ratio * 3, 1)
    s += GRADE_WEIGHT.get(grade.upper(), 0)
    return round(s, 1)


def verdict(mentions, api_found, grade=""):
    if not api_found:
        return "🔸블로그만"
    if grade.upper() == "E":
        return "⚠️광고의심"
    if mentions >= 3:
        return "⭐필수"
    return "○추천"


def resolve(cand, area):
    name = cand.get("name", "").strip()
    sources = cand.get("sources", [])          # [{"url":..,"date":..}] (선택)
    # mentions 없으면 출처 개수로 유추 (교차검증 신호)
    mentions = int(cand.get("mentions", len(sources) or 1))
    grade = cand.get("grade", "")              # A~E (선택)
    # 장소명만 검색어로 던진다 (지역명 접두어·areaCode 둘 다 KorService2 에선
    # 검색을 0건으로 만든다). 지역은 결과 주소(addr1)로 best_match 가 거른다.
    res = call("searchKeyword2", {"keyword": name, "rows": 10})
    if res.get("error"):
        # API 호출 자체 실패 → 그대로 전파 (키 미활성 등)
        return {"_api_error": res["error"]}

    items = res.get("items", [])
    match, ratio = best_match(name, items, area) if items else (None, 0.0)
    api_found = match is not None and ratio >= 0.5

    out = {
        "name": name,
        "mentions": mentions,
        "grade": grade.upper() or None,
        "sources": sources,
        "api_found": api_found,
        "match_ratio": round(ratio, 2),
        "score": score(mentions, api_found, ratio, grade),
        "verdict": verdict(mentions, api_found, grade),
    }
    if api_found:
        out.update({
            "title": match.get("title"),
            "addr1": match.get("addr1"),
            "mapx": match.get("mapx"),
            "mapy": match.get("mapy"),
            "firstimage": match.get("firstimage"),
            "tel": match.get("tel"),
            "contentid": match.get("contentid"),
            "contenttypeid": match.get("contenttypeid"),
        })
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", help="후보 JSON 파일 (없으면 stdin)")
    p.add_argument("--area", default="", help="지역명 (검색 정확도 보강)")
    args = p.parse_args()

    try:
        raw = open(args.input, encoding="utf-8").read() if args.input else sys.stdin.read()
    except FileNotFoundError:
        print(json.dumps({"error": f"입력 파일 없음: {args.input}"}, ensure_ascii=False))
        sys.exit(1)
    try:
        candidates = json.loads(raw)
    except ValueError:
        print(json.dumps({"error": "입력 JSON 파싱 실패"}, ensure_ascii=False))
        sys.exit(1)

    # 한 장소가 실패해도 전체를 중단하지 않는다 (실패 격리).
    # 단 절반 이상 실패하면 키·네트워크 문제로 보고 중단.
    results, errors = [], 0
    for cand in candidates:
        r = resolve(cand, args.area)
        if "_api_error" in r:
            errors += 1
            results.append({"name": cand.get("name"), "api_found": False,
                            "verdict": "🔸API오류", "score": 0,
                            "error": r["_api_error"]})
            continue
        results.append(r)

    if candidates and errors >= len(candidates) / 2:
        print(json.dumps(
            {"error": f"후보 {len(candidates)}개 중 {errors}개 조회 실패 — "
                      "TourAPI 키 미활성(401) 또는 네트워크 문제일 수 있음",
             "places": results}, ensure_ascii=False, indent=2))
        sys.exit(1)

    results.sort(key=lambda x: x["score"], reverse=True)
    out = {"count": len(results), "places": results}
    if errors:
        out["warning"] = f"{errors}개 장소 조회 실패 (🔸API오류로 표기, 나머지는 정상)"
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
