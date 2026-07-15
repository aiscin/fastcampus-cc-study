---
name: content-pipeline
description: This skill should be used when the user wants to research a topic and turn it into a card-news (and optionally a short video) — 키워드나 요청 한 마디로 딥리서치부터 카드뉴스·영상까지 만든다. Triggers include "○○ 카드뉴스 만들어줘", "○○ 조사해서 카드뉴스로", "○○ 콘텐츠 만들어줘", "○○ 트렌드 정리해서 카드뉴스", "make a card-news about ○○", "research ○○ and make content". It runs deep research to gather and cross-check sources, then plans and publishes an evidence-based card-news as images and HTML — 매번 손으로 하던 리서치·기획·디자인을 한 번에 끝내기 위해. Use this skill whenever the user wants to create a card-news, content, or trend summary about a topic, even if they don't explicitly mention "스킬" or "skill".
---

# content-pipeline — 리서치 → 카드뉴스 → (옵션) 영상

> 주제 한 마디를 받아 딥리서치로 자료를 모으고, 검증된 근거로 카드뉴스를 만들어 이미지·HTML로 발행한다. 요청 시 나레이션·BGM을 붙여 세로 영상까지 이어간다.

이 스킬은 **오케스트레이터**다. 결정론 작업(API 호출·크롭·타이밍·렌더)은 `scripts/`가 맡고, 창작 작업(기획·카피·레이아웃)은 이 문서의 지시대로 Claude가 맡는다. 스크립트는 이 스킬 폴더(`.claude/skills/content-pipeline/`) 기준이며, 모든 스크립트는 **작업 폴더 경로를 인자로** 받는다.

핵심 설계 이유:
- **있으면 재호출, 없으면 자체 제작** — 리서치는 이미 검증된 `deep-research` 스킬을 재호출한다(중복 구현 방지). 이미지·음성·BGM·영상은 전용 스킬이 없으므로 자체 스크립트로 만든다.
- **결정론은 스크립트, 창작은 문서** — 같은 입력에 같은 결과가 나와야 하는 단계만 코드로 뺀다. 그래야 재현성이 보장된다.
- **카드뉴스까지 자동** — Step 1~5는 확인 없이 이어서 실행한다. 사용자를 매 단계 붙잡지 않기 위해서다. 단, 이미지 과금 직전(Step 4)과 영상 진입 직전(Step 5 종료)에서만 멈춘다.

## 준비 (Step 0)

작업 폴더를 만들고 환경을 점검한다. 주제에서 짧은 슬러그를 뽑아 `{워크스페이스}/50-my-work/Part06-스킬만들기/실습31-콘텐츠파이프라인스킬/{주제}-{YYYY-MM-DD}/` 를 만든다.

To set up, run `bash .claude/skills/content-pipeline/scripts/setup.sh "<주제>"`. 이 스크립트는 폴더를 만들고, `.env`의 `OPENAI_API_KEY` 유무와 `python3`/`node`/`ffmpeg`/`Pretendard·BlackHanSans 폰트`를 점검해 결과를 한 줄로 보고한다. 폰트가 없으면 스크립트가 Windows 폰트(맑은고딕·Segoe UI Emoji)나 다운로드로 자동 확보한다.

키가 없으면 발급 방법을 안내하되, 리서치·기획·HTML(Step 1·2·5)은 키 없이도 되므로 이미지 단계 전까지는 진행한다.

## Step 1 — 딥리서치 (재호출)

**타입: api_mcp + review.** 주제로 자료를 조사한다. `deep-research` 스킬을 재호출한다(자연어로 "○○ 딥리서치해줘"를 내부 호출). `deep-research`가 없으면 WebSearch로 폴백하고, 유망 URL은 WebFetch로 본문을 가져와 교차검증한다. 결과를 `01-리서치.md`로 저장한다.

검증 없이 다음으로 넘기지 않는다 — 출처 신뢰도와 상충 정보를 한 번 훑어, 카드뉴스에 넣을 사실만 남긴다. 데이터에 한계가 있으면(예: 통계의 표본·기간 제약) 그 한계를 기록해 둔다. 나중에 카드에 정직성 캡션으로 반영하기 위해서다.

## Step 2 — 카드뉴스 기획

**타입: rag + prompt.** `references/card-news-guide.md`를 읽고 그 틀에 맞춰 기획한다. 결정 순서: (1) 유형 판별(정보형/홍보형/뉴스형, 가이드 §3 결정 트리) → (2) 후킹 제목(가이드 §3 후킹 7유형) → (3) 장수(정보형 8~10장) → (4) 장별 1메시지 카피 + 연결어 → (5) **데이터 정직성 필터**(리서치 한계를 왜곡하는 표현 제거, 필요한 카드엔 주의 캡션).

기획을 `02-plan.json`으로 저장한다. 스키마는 `references/image-prompt-generator.md`의 SSOT를 따른다: `topic·audience·type·style_lock·cards[]`(각 `card_no·role·title·subtitle·key_message·image_prompt`). `image_prompt`는 카드별 배경 장면을 자연어로 쓰되, `style_lock`(예: 흑백 에디토리얼 + 포인트색 1개)을 **매 카드에 그대로 반복**해 톤을 고정한다. 텍스트는 이미지에 굽지 않는다 — HTML 레이어가 얹는다.

제목·구성이 주제의 핵심을 담았는지 사용자에게 한 번 확인한다(간단 확인은 자연 대화로 충분하다).

## Step 3 — 이미지 생성

**타입: script.** `python3 .claude/skills/content-pipeline/scripts/generate_image.py "<작업폴더>" --quality low` 로 **저화질 초안부터** 뽑는다. 초안 톤을 확인하고(사용자 승인) 좋으면 `--quality medium`으로 최종만 재생성한다. 이 순서가 과금 방어의 핵심이다 — 잘못된 톤으로 고화질을 대량 생성하면 비용이 샌다. 표지 1장만 먼저 뽑아 톤을 잡고 나머지를 배치로 가는 것을 기본으로 한다.

**실제 상품·사물 사진이 필요한 주제일 때만**(예: 쇼핑·제품 트렌드) `scripts/fetch_kream_images.py` 같은 수집 스크립트로 실사진 하이브리드를 쓴다. 이때는 저작권 게이트를 반드시 통과한다 — 발행 용도(개인·포트폴리오 vs 공개)를 먼저 확인하고, 실제 브랜드 이미지엔 "출처" 캡션을 명시한다. 일반 주제는 AI 이미지만으로 충분하다.

## Step 4 — 카드뉴스 HTML + PNG

**타입: prompt + script.** `02-plan.json`의 이미지 위에 카피를 레이어로 얹은 `card-news.html`을 작성한다. 폰트는 **제목 Black Han Sans + 본문 Pretendard**(둘 다 `remotion/public/fonts` 또는 작업폴더 `fonts/`에 @font-face로 임베드), 정보전달을 위해 **핵심 숫자를 히어로 크기로, 비율은 미니 막대로** 시각화한다. 카드는 1080×1350(4:5), 색은 2~3개 + 포인트색 10% 규칙. 레이아웃은 절대 위치 3구간(제목/스테이지/설명)으로 겹침을 막는다.

HTML을 PNG로 렌더한다: `python3 .claude/skills/content-pipeline/scripts/render_cards.py "<작업폴더>"`. playwright 크로미움으로 각 `section.card`를 1080×1350으로 캡처해 `preview/card-01~NN.png`를 만든다. 한글이 깨지지 않게 스크립트가 폰트 로드를 기다린다.

**여기까지가 자동 실행 범위다.** 카드뉴스 완성 후 결과를 요약하고 "영상까지 이어갈까요?"만 물어본다(AskUserQuestion). 영상은 무겁고 시간이 걸리므로 기본은 여기서 멈춘다.

## Step 5~8 — 영상화 (요청 시에만)

사용자가 영상을 원하면 이어간다.

- **Step 5 나레이션 (prompt):** 씬=카드 1:1, 각 3~5초 짧은 대본을 `05-tts-script.md`에 `## 씬 N` 헤더로 쓴다. 톤(반말/존댓말)·목소리를 확인한다.
- **Step 6 음성·타이밍 (script):** `python3 .../scripts/tts_and_timing.py "<작업폴더>" --voice nova` → 씬별 mp3 + `card-timings.json`.
- **Step 7 BGM (script, 선택):** `bash .../scripts/gen_bgm.sh "<작업폴더>/bgm.mp3"` — 저작권 무관 앰비언트. 넣을지 확인.
- **Step 8 영상 (script):** `bash .../scripts/make_video.sh "<작업폴더>"` → `card-news.html`을 Remotion이 라이브 렌더하며 등장 효과(제목·숫자·막대·제품)를 입히고, 음성·자막·BGM을 합쳐 4:5 `output.mp4`를 만든다.

**환경 폴백(재현성)** — `make_video.sh`/`render_cards.py`는 (1) Remotion 전용 브라우저 다운로드가 막히면 playwright 크로미움을 재사용하고 (2) WSL에서 낮은 포트가 타임아웃 나면 빈 높은 포트를 자동 지정하며 (3) 폰트는 FontFace API로 직접 로드해 한글 깨짐·행(hang)을 막는다. 이 폴백은 스크립트에 내장돼 있으니 그대로 호출하면 된다.

## References
- **`references/card-news-guide.md`** — 카드뉴스 제작 도메인 지식(유형 결정 트리·후킹·레이아웃 정량값). Step 2에서 읽는다.
- **`references/image-prompt-generator.md`** — 02-plan.json 스키마 + gpt-image-2 프롬프트 규칙(STYLE_LOCK). Step 2·3에서 참조.

## Scripts
- **`scripts/setup.sh`** — 폴더 생성 + 환경·폰트 점검 (Step 0)
- **`scripts/generate_image.py`** — plan.json → OpenAI 이미지 + crop (Step 3)
- **`scripts/fetch_kream_images.py`** — (옵션) 실제 상품 썸네일 수집 (Step 3, 상품 주제만)
- **`scripts/render_cards.py`** — card-news.html → 카드 PNG (Step 4)
- **`scripts/tts_and_timing.py`** — 나레이션 → 씬 음성 + 타이밍 (Step 6)
- **`scripts/gen_bgm.sh`** — 저작권 무관 앰비언트 BGM 합성 (Step 7)
- **`scripts/make_video.sh`** — 카드·음성·BGM → 4:5 영상 (Step 8)

## Assets
- **`remotion/`** — 라이브 HTML 카드 렌더 + 등장 효과(CardReel.tsx). `make_video.sh`가 사용. 컨텍스트에 로드하지 않는다.

## Settings (가변 요소)
| 설정 | 기본값 | 변경 방법 |
|------|--------|-----------|
| 이미지 톤 | 흑백 + 포인트색 1개 | Step 2에서 `style_lock` 수정, 또는 사용자에게 확인 |
| 이미지 화질 | low(초안)→medium(최종) | `generate_image.py --quality` |
| 나레이션 톤/목소리 | 반말 / nova | Step 5에서 확인, `tts_and_timing.py --voice` |
| BGM | 켬(잔잔한 앰비언트) | `gen_bgm.sh` 실행 여부 |
| 영상 비율 | 4:5 (1080×1350) | Remotion `Root.tsx` 치수 |
| 실사진 하이브리드 | 끔(AI 이미지만) | 상품 주제일 때 `fetch_kream_images.py` |
