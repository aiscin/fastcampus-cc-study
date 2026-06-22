# Clip 8 — 오디오/영상 → 문서 ★ audio-to-doc (회의록 메인 + 유튜브 시연 우회) (실습 29, 30분)

> 페르소나 메모 — A(마케터): 회의 많음 / B(PO): 액션 추출 핵심 / C(영업): 고객 미팅 → 후속 액션

> ⚙️ 도구 결정 (테스트 검증 완료) — **Gemini API(`gemini-3.5-flash`)** 로 전사 + 화자 분리. whisper 로컬 대신 Gemini로 가는 이유는 §도구 선택 참고.

## 자동 셋업

```bash
mkdir -p ~/fastcampus-cc/50-my-work/Part06-스킬만들기/실습29-회의록자동화스킬/
mkdir -p ~/fastcampus-cc/.claude/skills/audio-to-doc/{scripts,references}/
which ffmpeg >/dev/null 2>&1 && echo "✓ ffmpeg OK" || echo "ℹ brew install ffmpeg yt-dlp 필요"
which yt-dlp >/dev/null 2>&1 && echo "✓ yt-dlp OK" || echo "ℹ brew install yt-dlp 필요 (유튜브 시연용)"
grep -qiE "^gemini" ~/fastcampus-cc/.env 2>/dev/null && echo "✓ Gemini 키 .env 확인" || echo "ℹ .env 에 GEMINI_API_KEY=... 등록 필요 → 아래 '사전 준비' 따라하기 (aistudio.google.com/apikey)"
echo "✓ 진도 폴더 + audio-to-doc 스킬 폴더 (scripts + references) 준비 완료"
```

## 도구 선택 — 왜 Gemini인가 (테스트로 검증)

같은 유튜브 4분 음성(유퀴즈 김대식 교수)으로 직접 비교한 결과:

| 기준 | **Gemini 3.5 Flash** | WhisperKit (로컬) | whisper-diarization |
|------|:---:|:---:|:---:|
| 설치 (PyTorch X) | ✅ curl만 | ✅ `brew` | ❌ torch+NeMo 무거움 |
| 화자 분리 품질 | ✅ 진행자/게스트/나레이션까지 구별 | ✅ 음성 기반 | ✅ 음성 기반 |
| 한국어 전사 | ✅ "러브(Lobe)·CES·캣트리스" 정확 | ○ | ○ |
| 개인정보 (로컬) | ❌ 오디오 구글 전송 | ✅ 외부 X | ✅ 외부 X |
| 긴 회의(최대 9.5h) | ✅ 한 번에 | △ 분할 | △ 분할 |
| 비용 | 무료 한도 | 무료 | 무료 |

- **2.5 → 3.5 개선 확인**: 2.5는 짧은 리액션을 별도 화자로 과분리했으나, **3.5는 진행자·게스트 2명을 정확히 가르고 삽입된 VCR 나레이션까지 제3 화자로 음성 톤으로 구별**. 회의 2~3인 정도는 실용적.
- **갈림길은 단 하나** — "오디오를 외부(구글)로 보내도 되는가". 민감한 사내 회의면 로컬(WhisperKit)이 정답이지만, 본 클립은 **설치 0 + 품질 + 긴 영상 한 번에** 를 우선해 **Gemini**로 진행.
- **API 키**: `~/fastcampus-cc/.env` 에 `GEMINI_API_KEY=...` 로 보관 (clip-06 네이버 키와 같은 패턴). 발급은 아래 '사전 준비 — Gemini API 키 발급' 따라하기.

## 사전 준비 — Gemini API 키 발급 (따라하기)

Gemini는 무료 한도가 있어 카드 등록 없이 바로 쓸 수 있다. 아래를 그대로 따라 하면 된다.

1. **Google AI Studio 접속** — https://aistudio.google.com/apikey (구글 계정 로그인)
2. **`Create API key`** (API 키 만들기) 클릭 → 새 프로젝트면 `Create API key in new project` 선택
3. 생성된 키 **복사** (`AIza...`로 시작하는 문자열). ⚠️ 비밀번호 같은 것 — 화면 캡처·공유 금지
4. **`.env`에 저장** — 강의 워크스페이스 루트 `~/fastcampus-cc/.env` 에 한 줄 추가:
   ```
   GEMINI_API_KEY=AIza여기에_복사한_키
   ```
   (clip-06 네이버 키와 같은 패턴. `.env`는 `.gitignore`에 있어 깃에 안 올라감 — 확인할 것)
5. **등록 확인** (값은 안 보이게):
   ```bash
   grep -qiE "^gemini" ~/fastcampus-cc/.env && echo "✓ Gemini 키 등록됨" || echo "✗ 아직 없음"
   ```

> 입력 가이드는 명령형 대신 의문문으로 — "Gemini 키를 .env에 넣으려는데 어떻게 해?" 처럼 물어보면 클로드코드가 정리·등록·검증까지 해 준다. (키 값 자체는 본인이 발급해서 줘야 함 — 클로드코드가 만들 수 없음)

**무료 한도 주의** — gemini-3.5-flash 무료 티어는 분당/일일 요청 수 제한이 있다. 회의 1~2건 테스트엔 충분. 한도 초과 시 잠시 후 재시도하거나 유료 결제 연결.

## 브리핑

**회의록이 메인 적용**. 시연용 회의 오디오 없어서 **유튜브로 우회 — 본인 회의 녹음에 그대로 적용 가능**.

```
[사전 준비] 유튜브 추출용 yt-dlp + ffmpeg (brew, 파이썬 X) + Gemini API 키 1개 (.env). 시연 오디오 없을 때 유튜브 우회 패턴 안내

[STEP 1] 워크플로우 잡기
   "오디오로 된 녹음 파일을 텍스트로 전환해서 요약 정리를 하려는데, 어떻게 워크플로우를 구성해야 할까?"
   → 단계별 워크플로우 정리
[STEP 2] 보완 + 실행 가능 단계 정의
   정리된 단계 살펴보고 보완 → 입력 5 유형 자동 판별·템플릿 분리·전사 도구 선택(Gemini vs 로컬) 등 클로드코드가 실제로 할 수 있는 단계로 정의
   (여기서 "화자 분리는 어떤 도구가 되나" 직접 조사·테스트 → Gemini 3.5 결정까지가 모범 흐름)
[STEP 3] 스킬로 만들기
   audio-to-doc 스킬 + scripts/extract_audio.sh (yt-dlp 추출) + scripts/transcribe_gemini.py (Gemini Files API 전사+화자분리) + references/templates.md
[STEP 4] 만든 스킬로 테스트·검증 (유튜브 시연 우회)
   유퀴즈 김대식교수 인터뷰 → 화자 분리 + 5 유형 자동 판별 확인
[STEP 5] 본인 회의 녹음 응용 + 5 유형 (회의·강의·팟캐스트·인터뷰·발표) 활용
```

**핵심 메시지** — 그냥 'audio-to-doc 스킬 만들어줘' 하지 마세요. **'오디오로 된 녹음 파일을 텍스트로 전환해서 요약 정리를 하려는데, 어떻게 워크플로우를 구성해야 할까?'**로 출발. 회의록만이 아니라 **5 유형 자동 판별** (화자 수·Q&A 패턴·안건/결정 키워드로 판별)까지 워크플로우에서 자연스럽게 잡힙니다. **화자 분리 도구를 정하는 과정 자체가 메타 흐름의 모범** — 공식 문서 조사(OpenAI Whisper는 화자 분리 X 확인) → 후보 비교(Gemini/WhisperKit/whisper-diarization) → 실제 음성으로 테스트 → 최신 모델까지 확인하고 결정.

**시연 우회 명시 (사용자 의도)**: "회의록 메인 → 시연 오디오 없어서 유튜브로 → 본인 회의 녹음에 그대로 적용"

**5 유형 자동 판별** (Gemini 프롬프트로 판별):

| 유형 | 판별 기준 | 출력 템플릿 |
|------|----------|----------|
| 회의 | 다수 화자 + 안건·결정 키워드 | 안건 / 결정사항 / 액션아이템 표 |
| 강의/컨퍼런스 | 단일 화자 + 개념 설명 | 핵심 개념 + 섹션별 요약 |
| 팟캐스트/대담 | 2-3 화자 + 자유 대화 | 주제별 구간 + 화자별 의견 |
| 인터뷰 | 질문자 + 답변자 (Q&A) | Q&A 구조 + 발언 하이라이트 |
| 발표/세미나 | 단일 화자 + 주장-근거 | 주장-근거-Q&A |

**개인정보 주의 한 줄**: Gemini는 클라우드 API라 오디오가 구글로 전송됩니다. 사내 대외비 회의는 로컬(WhisperKit) 대안을 안내 — 본 클립은 간편함·품질·긴 영상 한 번에 처리를 우선해 Gemini 채택.

**Part 5 자산 사슬**: 실습 19 study-progress (통합) + 실습 21 trash-guard.

**clip-03 비교·분석·디벨롭 사이클 재사용** — 만든 audio-to-doc 스킬도 본인 사례로 라이프사이클 적용 가능.

## 스크립트 분리 (CH03 모범 — 결정론은 코드로)

| 파일 | 언어 | 역할 |
|------|------|------|
| `scripts/extract_audio.sh` | Bash | yt-dlp로 유튜브 음성 추출 + ffmpeg 16kHz mono wav 변환 (+긴 영상 트림 옵션) |
| `scripts/transcribe_gemini.py` | Python | Gemini Files API 업로드 → `gemini-3.5-flash` 전사+화자분리 호출 → 텍스트 반환 |
| `references/templates.md` | (문서) | 5 유형별 출력 양식 |

전사·업로드·API 호출은 매번 같아야 하므로 스크립트로 분리(같은 입력→같은 결과). **유형 판별·요약은 SKILL.md 본문(AI 영역)** 으로 자유도 확보.

## 단계 안내

| Phase | 내용 |
|------|------|
| A (2분) | 도입 — 회의록 메인 + 유튜브 시연 우회 |
| 사전 준비 | yt-dlp + ffmpeg (brew) + **Gemini API 키 발급 따라하기 → `.env`에 `GEMINI_API_KEY` 저장** + 적용 매트릭스 (회의록 메인 + 5 유형) |
| B-1 (3분) | STEP 1 워크플로우 잡기 — "녹음 파일을 텍스트로 전환해서 요약 정리하려는데 어떻게 구성해야 할까?" |
| B-2 (5분) | STEP 2 보완 + 화자 분리 도구 조사·테스트 → Gemini 3.5 결정 (5 유형 자동 판별·템플릿 분리) |
| B-3 (5분) | STEP 3 audio-to-doc 스킬화 + extract_audio.sh + transcribe_gemini.py 분리 |
| B-4 (6분) | STEP 4 만든 스킬로 테스트·검증 (유튜브 시연 우회) — 유퀴즈 인터뷰 화자 분리 확인 |
| B-5 (4분) | STEP 5 본인 회의 녹음 응용 + 페르소나별 5 유형 활용 |
| C (1분) | 마무리 — 한 스킬이 5 유형 처리 |
| D (1분) | WRAP |

## WRAP

1. 결과물 검증 — `audio-to-doc/SKILL.md` + `scripts/extract_audio.sh` + `scripts/transcribe_gemini.py` + `references/templates.md` + 시연 산출 1~2건 + (본인 회의 1건)
2. README — 5 유형 표 + "회의록 메인, 유튜브 시연 우회" 메시지 + 도구 선택(Gemini 3.5) 근거 한 줄
3. progress.json — `practice_completed`에 29, `skills_created`에 `audio-to-doc`
4. 회고 — "본인 회의·영상 콘텐츠 한 줄"
5. 다음 — "clip-09 모닝 브리핑 (Part 5 GWS + /nopal + 슬래시 커맨드)"
