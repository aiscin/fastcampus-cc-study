---
name: audio-to-doc
description: 녹음 파일이나 유튜브 영상의 음성을 텍스트로 전사하고 화자를 분리해서 유형별(회의·강의·팟캐스트·인터뷰·발표) 요약 문서로 만든다. "회의록 만들어줘", "녹음 정리해줘", "이 영상 요약해줘", "유튜브 전사해줘", "오디오 텍스트로 바꿔줘", "인터뷰 정리해줘", "강의 노트 만들어줘", "음성 받아쓰기", transcribe audio, meeting notes from recording 요청에 사용. 사용자가 오디오/영상 파일이나 유튜브 링크를 주고 정리·요약·전사를 원하면, 명시적으로 "스킬"을 언급하지 않아도 이 스킬을 쓴다. (Gemini API — 오디오가 Google로 전송되므로 대외비는 사전 확인 필요)
---

# audio-to-doc

> 녹음/영상의 음성을 전사 + 화자 분리하고, 내용 유형을 판별해 알맞은 양식으로 요약 문서를 만든다.

전사·업로드·API 호출은 매번 같아야 하므로 **스크립트(결정론)** 로 분리하고, 유형 판별·요약은 **이 문서(AI 판단)** 로 처리한다. 같은 오디오면 같은 전사가 나오고, 정리 품질은 맥락에 맞게 유연해진다.

## 사전 요건

- `ffmpeg` (오디오 변환), 유튜브일 때만 `yt-dlp` (음성 추출)
- 워크스페이스 루트 `.env` 에 `GEMINI_API_KEY=...` (발급: https://aistudio.google.com/apikey)
- 키가 없으면 `transcribe_gemini.py` 가 설정 안내를 출력하고 멈춘다.

## 워크플로우

### Step 1: 입력 확인 + 개인정보 동의 (review)

입력이 **유튜브 URL** 인지 **로컬 오디오 파일** 인지 확인한다. 둘 다 아니면 무엇을 정리할지 되묻는다.

전사는 Gemini API를 쓰므로 **오디오가 Google 서버로 전송된다.** 대외비·개인정보가 포함될 수 있으니, 실행 전에 사용자에게 한 번 알리고 진행 동의를 받는다. 긴 파일은 비용이 든다는 점도 함께 알린다 — 오디오 1초당 토큰 32개(1시간 ≈ 11만 토큰)라 무료 한도를 한 파일로 소진할 수 있다.

### Step 2: 오디오 확보 (script)

`scripts/extract_audio.sh` 를 실행한다. 유튜브면 음성을 내려받고, 로컬 파일이면 그대로 받아 **둘 다 16kHz mono mp3 로 통일**한다.

```bash
bash scripts/extract_audio.sh "<URL 또는 파일경로>" "<출력디렉토리>"
```

마지막 줄에 변환된 오디오 경로가 출력된다. 이 경로를 다음 단계로 넘긴다. 추출/변환 실패 메시지가 나오면(삭제된 영상·손상 파일 등) 사용자에게 그대로 전하고 멈춘다.

### Step 3: 전사 + 화자 분리 (script)

`scripts/transcribe_gemini.py` 를 실행한다. 파일 크기로 inline(20MB 미만)/Files API(20MB 이상)를 **자동 분기**하고, `gemini-3.5-flash` 로 전사 + 화자 분리 + `MM:SS` 타임스탬프를 받는다.

```bash
python3 scripts/transcribe_gemini.py "<오디오경로>" "<출력디렉토리>"
```

stdout으로 `{speaker_count, speakers, segments:[{speaker,time,text}], raw_txt}` JSON이 온다. 원문 전사는 `transcript_raw.txt` 와 `transcript_raw.json` 에 먼저 저장되므로, 이후 단계가 실패해도 전사 결과는 남는다. 큰 파일은 업로드·처리에 1~3분 걸릴 수 있다(진행 표시가 stderr로 나옴).

### Step 4: 유형 판별 (prompt)

전사·화자 정보를 읽고 5유형 중 하나로 판별한다 — 기준은 `references/templates.md` 의 판별 표(화자 수 + Q&A 패턴 + 안건/결정 키워드).

- 회의 / 강의·컨퍼런스 / 팟캐스트·대담 / 인터뷰 / 발표·세미나

판별이 애매하면(발표+Q&A 혼합, 비공식 잡담 등) **판별 결과를 사용자에게 먼저 보여주고 이대로 갈지 확인**한다. 엉뚱한 양식이 적용되면 사용자가 수동으로 다시 정리해야 하므로, 애매할 때 한 번 확인하는 편이 낫다.

### Step 5: 유형별 요약 문서 생성 (generate)

`references/templates.md` 의 해당 유형 양식으로 마크다운 문서를 만든다. 공통 헤더(한줄 요약·날짜·화자 수·분량)를 먼저 두고, 유형 양식을 채운다.

- **액션 아이템은 체크박스 `- [ ]`** 로 (Notion·Obsidian 붙여쓰기).
- 화자 1명이면 화자 분리 섹션 생략·"단일 화자" 표기, 3명 이상이면 분리 정확도가 낮을 수 있다는 한 줄 고지.
- 결과는 `{출력디렉토리}/{제목}-{날짜}.md` 로 저장하고 경로를 알린다.

## 설정 (가변 요소)

| 설정 | 기본값 | 변경 방법 |
|------|--------|-----------|
| 모델 | `gemini-3.5-flash` | `transcribe_gemini.py` 의 `MODEL` |
| inline/Files 분기 | 20MB | `transcribe_gemini.py` 의 `INLINE_LIMIT` |
| 전사 언어 | 한국어 | `transcribe_gemini.py` 의 `PROMPT` |
| 출력 유형 | 자동 판별(5종) | 사용자가 "회의록으로" 처럼 지정 가능 |

## 자주 막히는 곳

- **키 없음/형식 오류** — `.env` 의 `GEMINI_API_KEY` 확인. AI Studio 키는 보통 `AIza...` 로 시작.
- **429 한도 초과** — 잠시 후 재시도하거나 유료 키 연결. 긴 파일은 토큰을 많이 쓴다.
- **유튜브 실패** — 멤버십·지역제한·삭제 영상은 못 받는다. `yt-dlp --update` 로 갱신 후 재시도.
- **전사는 됐는데 요약 실패** — `transcript_raw.txt` 가 이미 저장돼 있으니 그걸로 이어서 정리한다.

## References

- **`references/templates.md`** — 5유형 판별 기준 + 유형별 출력 양식

## Scripts

- **`scripts/extract_audio.sh`** — yt-dlp 음성 추출(URL일 때) + ffmpeg 16kHz mono 변환. 로컬/URL 자동 분기.
- **`scripts/transcribe_gemini.py`** — 20MB 기준 inline/Files API 분기, Gemini 전사+화자분리, 구조화 JSON + 원문 보존.
