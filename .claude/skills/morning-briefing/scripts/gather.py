#!/usr/bin/env python3
"""morning-briefing 메일·일정 수집 (결정론 영역).

gws CLI를 호출해 Gmail 안 읽은 메일과 오늘 캘린더 일정을 가져온다.
광고성 메일 필터는 매번 같아야 하므로 여기 규칙으로 고정한다.
AI(SKILL.md)는 이 스크립트가 넘긴 정리된 데이터에서 답장 우선순위 판단·요약만 한다.

사용:  python3 gather.py [--mail-limit 10]
출력:  stdout에 JSON, gws 실패 시 errors[]에 기록.
전제:  gws CLI 설치 + Google OAuth 인증 완료(Part 5 실습20).
"""
import subprocess
import json
import sys
import re
import argparse
import datetime
import urllib.request
import urllib.parse

# 날씨 위치 (기본 서울). 바꾸려면 이 좌표만 수정.
WEATHER_LAT = 37.5665
WEATHER_LON = 126.9780

# Open-Meteo weather_code → 한글 (옷차림 문구는 AI가 기온 보고 판단)
WX_CODE = {
    0: "맑음", 1: "대체로 맑음", 2: "구름 조금", 3: "흐림",
    45: "안개", 48: "짙은 안개", 51: "약한 이슬비", 53: "이슬비", 55: "강한 이슬비",
    61: "약한 비", 63: "비", 65: "강한 비", 66: "어는 비", 67: "강한 어는 비",
    71: "약한 눈", 73: "눈", 75: "많은 눈", 77: "싸락눈",
    80: "약한 소나기", 81: "소나기", 82: "강한 소나기",
    85: "약한 눈보라", 86: "눈보라", 95: "천둥번개", 96: "우박 동반 뇌우", 99: "강한 우박 뇌우",
}


def get_weather():
    """Open-Meteo 무료 API(키 불필요)로 오늘 날씨. 실패 시 None."""
    url = "https://api.open-meteo.com/v1/forecast?" + urllib.parse.urlencode({
        "latitude": WEATHER_LAT, "longitude": WEATHER_LON,
        "current": "temperature_2m,weather_code",
        "daily": "temperature_2m_max,temperature_2m_min,weather_code,precipitation_probability_max",
        "timezone": "Asia/Seoul", "forecast_days": 1,
    })
    with urllib.request.urlopen(url, timeout=10) as r:
        d = json.load(r)
    cur = d.get("current", {})
    day = d.get("daily", {})
    code = (day.get("weather_code") or [0])[0]
    return {
        "now_temp": cur.get("temperature_2m"),
        "high": (day.get("temperature_2m_max") or [None])[0],
        "low": (day.get("temperature_2m_min") or [None])[0],
        "condition": WX_CODE.get(code, "정보없음"),
        "rain_prob": (day.get("precipitation_probability_max") or [None])[0],
    }

# 광고성 판정 — 발신자/제목/카테고리 3중. 은행·시스템 보안 알림 오탐을 막기 위해
# no-reply만으로는 광고 판정하지 않고, 프로모션 카테고리나 광고 키워드와 함께일 때만 거른다.
AD_SENDER = re.compile(r"(newsletter|no-?reply@.*(shop|deal|sale|mkt|marketing|news)|marketing@|hello@(news|send|mail))", re.I)
AD_SUBJECT = re.compile(r"(\(광고\)|\[AD\]|\[광고\]|할인|쿠폰|이벤트|세일|sale|% off|free spins|clearance|구독|newsletter)", re.I)
# 이 발신자/키워드는 광고로 보이지만 중요할 수 있어 보존(오탐 방지)
KEEP_HINT = re.compile(r"(보안|인증|로그인|결제|명세|영수증|배송|예약|계약|견적|급여|세금|경고|알림장|verification|security|invoice|receipt)", re.I)


def gws(args):
    """gws CLI 호출 → dict 반환. 실패 시 예외."""
    out = subprocess.run(["gws"] + args, capture_output=True, text=True, timeout=30)
    if out.returncode != 0:
        raise RuntimeError(out.stderr.strip() or f"gws exit {out.returncode}")
    # gws는 'Using keyring backend' 등을 첫 줄에 찍을 수 있어 JSON 시작부터 파싱
    txt = out.stdout
    start = txt.find("{")
    if start < 0:
        raise RuntimeError("gws 응답에 JSON 없음")
    return json.loads(txt[start:])


def header(msg, name):
    for h in msg.get("payload", {}).get("headers", []):
        if h["name"].lower() == name.lower():
            return h["value"]
    return ""


def classify_ad(frm, subj, labels):
    """광고성 True/False. 보존 힌트가 있으면 무조건 False."""
    if KEEP_HINT.search(subj) or KEEP_HINT.search(frm):
        return False
    if "CATEGORY_PROMOTIONS" in labels:
        return True
    if AD_SENDER.search(frm) or AD_SUBJECT.search(subj):
        return True
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mail-limit", type=int, default=10)
    args = ap.parse_args()

    errors = []
    result = {"weather": None, "unread_total": None, "mails": [], "ads_filtered": 0,
              "events": [], "conflicts": [], "is_monday": False,
              "week_events": None, "week_conflicts": [], "errors": errors}

    # --- 날씨 (키 불필요) ---
    try:
        result["weather"] = get_weather()
    except Exception as e:
        errors.append(f"날씨 수집 실패: {e}")

    # --- 메일 ---
    try:
        # 안 읽은 총 개수(추정)
        lst = gws(["gmail", "users", "messages", "list", "--params",
                   json.dumps({"userId": "me", "q": "is:unread in:inbox",
                               "maxResults": args.mail_limit * 3})])
        result["unread_total"] = lst.get("resultSizeEstimate")
        ids = [m["id"] for m in lst.get("messages", [])]
        kept = 0
        for mid in ids:
            if kept >= args.mail_limit:
                break
            try:
                msg = gws(["gmail", "users", "messages", "get", "--params",
                           json.dumps({"userId": "me", "id": mid, "format": "metadata",
                                       "metadataHeaders": ["From", "Subject", "Date"]})])
            except Exception as e:
                errors.append(f"메일 {mid} 조회 실패: {e}")
                continue
            frm = header(msg, "From")
            subj = header(msg, "Subject")
            date = header(msg, "Date")
            labels = msg.get("labelIds", [])
            if classify_ad(frm, subj, labels):
                result["ads_filtered"] += 1
                continue
            result["mails"].append({"from": frm, "subject": subj, "date": date,
                                    "snippet": msg.get("snippet", "")[:140]})
            kept += 1
    except Exception as e:
        errors.append(f"메일 수집 실패(gws 인증/네트워크 확인): {e}")

    # --- 일정 (KST) ---
    def fetch_events(tmin, tmax):
        ev = gws(["calendar", "events", "list", "--params",
                  json.dumps({"calendarId": "primary", "timeMin": tmin, "timeMax": tmax,
                              "singleEvents": True, "orderBy": "startTime", "maxResults": 50})])
        out = []
        for e in ev.get("items", []):
            s = e.get("start", {})
            en = e.get("end", {})
            out.append({
                "time": s.get("dateTime", s.get("date", "")),
                "end": en.get("dateTime", en.get("date", "")),
                "summary": e.get("summary", "(제목없음)"),
                "location": e.get("location", ""),
            })
        return out

    def find_conflicts(events):
        """시작~종료가 겹치는 일정 쌍을 찾는다(종일 일정 제외)."""
        timed = [e for e in events if "T" in e["time"] and "T" in e["end"]]
        conflicts = []
        for i in range(len(timed)):
            for j in range(i + 1, len(timed)):
                a, b = timed[i], timed[j]
                # a.start < b.end and b.start < a.end → 겹침 (문자열 ISO 비교로 충분)
                if a["time"] < b["end"] and b["time"] < a["end"]:
                    conflicts.append({"a": a["summary"], "a_time": a["time"],
                                      "b": b["summary"], "b_time": b["time"]})
        return conflicts

    try:
        today = datetime.date.today()
        result["is_monday"] = today.weekday() == 0
        tmin = f"{today.isoformat()}T00:00:00+09:00"
        tmax = f"{today.isoformat()}T23:59:59+09:00"
        result["events"] = fetch_events(tmin, tmax)
        result["conflicts"] = find_conflicts(result["events"])

        # 월요일이면 이번 주(월~일) 전체도 함께
        if result["is_monday"]:
            week_end = today + datetime.timedelta(days=6)
            wmin = tmin
            wmax = f"{week_end.isoformat()}T23:59:59+09:00"
            result["week_events"] = fetch_events(wmin, wmax)
            result["week_conflicts"] = find_conflicts(result["week_events"])
    except Exception as e:
        errors.append(f"일정 수집 실패: {e}")

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
