#!/usr/bin/env python3
"""뉴스 JSON → 반도체 종목 뉴스레터 HTML (GitHub Actions 무인 발행용).

fetch_news.py 의 출력 JSON을 받아:
  - 게이트(휴장/수집실패) 체크
  - Claude API(Messages)로 종목별 호재·악재 분석 + HTML 생성
  - newsletter/{YYYY}/{MM}/{YYYYMMDD}-반도체.html 저장 + index.html upsert

환경변수:
  ANTHROPIC_API_KEY  (필수)
  ANTHROPIC_MODEL    (선택, 기본 claude-opus-4-8 / 비용 절감 시 claude-sonnet-4-6)
  NEWSLETTER_DIR     (선택, 기본 50-my-work/.../newsletter)

사용법:
  python3 generate_newsletter.py news.json
  python3 fetch_news.py --sort date | python3 generate_newsletter.py -
"""

import os
import re
import sys
import json
import datetime

KST = datetime.timezone(datetime.timedelta(hours=9))
DEFAULT_DIR = "50-my-work/Part06-스킬만들기/실습27-검색API스킬/newsletter"
MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-opus-4-8")

PROMPT = """당신은 한국 반도체 보유종목 일일 뉴스레터를 만드는 편집자입니다.
아래 뉴스 JSON을 분석해 **모바일 반응형 HTML 뉴스레터 한 장**을 생성하세요.
출력은 **순수 HTML만** — 코드펜스(```)나 설명 문장 없이 `<!DOCTYPE html>`로 시작합니다.

## 분석 규칙
- 종목별로 호재/악재 분류 + **근거가 된 기사 원문 문장 1개를 반드시 인용**. 인용 못 하면 태그 금지(중립 처리).
- 🟢호재 / 🔴악재 / 🟡복합 / ⚪중립(인사·MOU·단순동향 또는 판단 애매할 때). 단정 표현 금지.
- item의 `unverified: true`(C급 단독)면 이슈에 "(미확인)" 표기.
- 뉴스 0건 종목도 빼지 말고 "오늘 관련 뉴스 없음" 회색 카드(class="card empty").
- 오늘의 PICK 1종목((뉴스 건수 × 호재/악재 강도)) + 이유 1줄. 전 종목 ⚪/0건이면 PICK 생략.
- macro[] 근거로 TL;DR 3줄(① 호재요인 ② 악재요인 ③ 이번 주 관전 포인트).
- 종목 카드는 중요순(뉴스 많은 순→호재→악재→복합→중립→0건).
- 컴플라이언스: "지금 사야"·"목표가" 금지. 호재/악재 = 뉴스 논조 분류이지 투자 판단 아님.
- 면책 문구를 **헤더 아래·PICK 안·푸터** 3곳에 넣는다.

## 사용할 CSS 클래스 (스타일은 ../../assets/style.css 가 제공)
헤더(header/.date/.headline/.period/.disc-top), PICK(.pick/.tag/.name/.scode/.why/.mini),
TL;DR(.tldr h2/ul li span), 종목(.stocks/.sec-title/.card[.empty/.amber]/.chead/.sig/.sname/.scode/
.badge[.b-red/.b-green/.b-amber/.b-gray]/.cnt/.issue/.unconf/.link), 아카이브(.archive a → ../../index.html),
푸터(footer/.disc). 신호등 이모지는 🟢🔴🟡⚪.

## HTML 골격 (이 구조를 채우세요)
<!DOCTYPE html>
<!-- generated_at: {GENERATED_AT} -->
<html lang="ko"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>반도체 종목 뉴스레터 · {DATE}</title>
<link rel="stylesheet" href="../../assets/style.css"></head>
<body><div class="wrap">
  <header> 날짜·기간·한줄시황 + .disc-top 면책 한 줄 </header>
  <div class="pick"> 오늘의 PICK + .mini 소형 면책 </div>
  <div class="tldr"> TL;DR 3줄 </div>
  <div class="stocks"> 종목 카드들(중요순) </div>
  <div class="archive"><a href="../../index.html">← 지난 뉴스레터 모아보기</a></div>
  <footer> 발행시각·출처 + .disc 면책 전문 </footer>
</div></body></html>

면책 전문: "본 뉴스레터는 공개된 뉴스 기사를 AI로 요약한 정보 제공용입니다. 투자 권유·매수/매도 추천이 아니며, 정보의 정확성을 보장하지 않습니다. 투자 판단과 손익은 본인에게 귀속됩니다."

## 뉴스 JSON
{NEWS_JSON}
"""


def load_input(arg):
    raw = sys.stdin.read() if arg == "-" else open(arg, encoding="utf-8").read()
    return json.loads(raw)


def gate(data):
    """발행 가능 여부. (publish: bool, reason: str)"""
    if data.get("market_closed"):
        return False, f"휴장일({data.get('market_closed_reason')}) — 발행 스킵"
    if data.get("has_error") and data.get("total_unique", 0) == 0:
        return False, f"수집 실패({data.get('errors')}) — 발행 스킵"
    return True, ""


def call_claude(data):
    import anthropic  # 지연 import — 결정론 로직은 SDK 없이도 동작
    client = anthropic.Anthropic()  # ANTHROPIC_API_KEY from env
    gen = data.get("generated_at", datetime.datetime.now(KST).isoformat())
    date = gen[:10]
    prompt = (PROMPT
              .replace("{GENERATED_AT}", gen)
              .replace("{DATE}", date)
              .replace("{NEWS_JSON}", json.dumps(data, ensure_ascii=False)))
    # 긴 HTML 출력 → 스트리밍으로 타임아웃 방지
    with client.messages.stream(
        model=MODEL,
        max_tokens=32000,
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        msg = stream.get_final_message()
    html = "".join(b.text for b in msg.content if b.type == "text").strip()
    # 혹시 코드펜스로 감싸면 제거
    html = re.sub(r"^```[a-zA-Z]*\n|\n```$", "", html).strip()
    return html, date


def save(html, date, base):
    yyyy, mm, dd = date[:4], date[5:7], date[8:10]
    out_dir = os.path.join(base, yyyy, mm)
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"{yyyy}{mm}{dd}-반도체.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return path, f"{yyyy}/{mm}/{yyyy}{mm}{dd}-반도체.html"


def headline_of(html):
    m = re.search(r'class="headline">(.*?)<', html)
    return m.group(1).strip() if m else "오늘의 반도체 브리핑"


def upsert_index(base, rel_link, date, headline):
    """index.html 맨 위에 오늘치 링크 추가 (같은 날짜 중복 금지)."""
    index = os.path.join(base, "index.html")
    wd = "월화수목금토일"[datetime.date(int(date[:4]), int(date[5:7]), int(date[8:10])).weekday()]
    li = (f'    <li><a href="{rel_link}"><span class="d">{date} ({wd})</span>'
          f'<span class="t">{headline}</span></a></li>')
    if not os.path.exists(index):
        html = (f'<!DOCTYPE html>\n<html lang="ko"><head><meta charset="UTF-8">'
                f'<meta name="viewport" content="width=device-width, initial-scale=1.0">'
                f'<title>반도체 종목 뉴스레터 · 모아보기</title>'
                f'<link rel="stylesheet" href="assets/style.css"></head><body><div class="wrap">'
                f'<h1>📈 반도체 종목 뉴스레터</h1>'
                f'<ul id="list">\n    <!-- NEWEST -->\n{li}\n</ul>'
                f'<footer>정보 제공용 · 투자 권유 아님</footer></div></body></html>\n')
        open(index, "w", encoding="utf-8").write(html)
        return
    content = open(index, encoding="utf-8").read()
    # 같은 날짜 링크 이미 있으면 그 줄을 교체(멱등성)
    pat = re.compile(rf'^.*<span class="d">{re.escape(date)} .*$\n?', re.M)
    content = pat.sub("", content)
    content = content.replace("<!-- NEWEST -->", f"<!-- NEWEST -->\n{li}", 1)
    open(index, "w", encoding="utf-8").write(content)


def main():
    if len(sys.argv) < 2:
        print("usage: generate_newsletter.py <news.json | ->", file=sys.stderr)
        sys.exit(2)
    base = os.environ.get("NEWSLETTER_DIR", DEFAULT_DIR)
    data = load_input(sys.argv[1])

    publish, reason = gate(data)
    if not publish:
        print(f"SKIP: {reason}")
        sys.exit(0)

    html, date = call_claude(data)
    path, rel = save(html, date, base)
    upsert_index(base, rel, date, headline_of(html))
    print(f"PUBLISHED: {path}")


if __name__ == "__main__":
    main()
