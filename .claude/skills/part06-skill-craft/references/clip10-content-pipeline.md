# Clip 10 — 콘텐츠 파이프라인 ★ Part 06 마지막 — 6 STEP 풀 파이프라인 (실습 31, 30분)

> 페르소나 메모 — A(마케터): 콘텐츠 30분 → 5분 직관 / B(PO): 다단계 통합 흐름 / C(영업): 자료 → 영상 자동 제안

## 자동 셋업

```bash
mkdir -p ~/fastcampus-cc/50-my-work/Part06-스킬만들기/실습31-콘텐츠파이프라인스킬/
mkdir -p ~/fastcampus-cc/.claude/skills/content-pipeline/references/
# 사전 리서치 자산(카드뉴스 통합 가이드 + 이미지 프롬프트 생성기)을 새 스킬 references로 복사
ASSETS=~/fastcampus-cc/.claude/skills/part06-skill-craft/references/clip10-assets
if [ -d "$ASSETS" ]; then
  cp -n "$ASSETS/card-news-guide.md" "$ASSETS/image-prompt-generator.md" \
     ~/fastcampus-cc/.claude/skills/content-pipeline/references/ 2>/dev/null
  echo "✓ 사전 리서치 자산 2종 → content-pipeline/references/ 복사 (card-news-guide·image-prompt-generator)"
else
  echo "ℹ 사전 리서치 자산 없음 — STEP 1 딥리서치로 가이드부터 생성"
fi
which node >/dev/null 2>&1 && echo "✓ Node.js OK" || echo "ℹ Node.js 필요 (Remotion 영상 빌드용)"
python3 -c "import openai" 2>/dev/null && echo "✓ openai SDK OK" || echo "ℹ pip install openai 필요 (이미지·TTS 둘 다 OpenAI API)"
grep -q "OPENAI_API_KEY=." ~/fastcampus-cc/.env 2>/dev/null && echo "✓ OPENAI_API_KEY OK" || echo "ℹ .env에 OPENAI_API_KEY 필요 (이미지+TTS 공용 키 1개)"
# 재호출할 스킬 확인 (리서치는 deep-research 스킬을 재호출)
for s in deep-research; do
  if [ -f ~/fastcampus-cc/.claude/skills/${s}/SKILL.md ]; then
    echo "✓ ${s} 확인 (재호출 가능)"
  else
    echo "⚠ ${s} 없음 — 해당 clip 먼저 또는 WebSearch fallback"
  fi
done
echo "✓ 진도 폴더 + content-pipeline 스킬 폴더 준비 완료"
```

## 브리핑

**Part 06 마지막 ★ 가장 큰 통합**. Part 03 30분 작업이 5분으로 + 풀 파이프라인이 "있는 스킬은 재호출, 없는 기능은 자체 스크립트"로 단계를 묶는다.

```
[STEP 1] 워크플로우 잡기
   "특정 주제로 리서치해서 영상까지 콘텐츠를 한 번에 만들려는데, 어떻게 워크플로우를 구성해야 할까?"
   → 단계별 워크플로우 정리 (리서치 → 기획 → 이미지 → HTML → TTS → 영상 순으로 잡힘)
[STEP 2] 보완 + 실행 가능 단계 정의
   정리된 단계 살펴보고 보완 → "이미 있는 스킬은 재호출, 없는 기능은 스크립트로 자체 제작"으로 단계 정의:
   · 리서치 = deep-research 스킬 재호출 (이미 만든 자산)
   · 이미지 = 나노바나나 이미지 스킬이 없으므로 자체 스크립트로 제작 (OpenAI 이미지 API)
   · TTS = 자체 스크립트 (OpenAI TTS API)
   · 영상 = Remotion(9x16) 빌드
   → 이미지·TTS가 같은 OpenAI 키 1개를 공유 + 체크포인트(AskUserQuestion)
   ※ 교훈: "다른 스킬을 부른다"가 핵심이 아니라, 있으면 재호출·없으면 자체 제작을 판단하는 게 핵심
[STEP 3] 스킬로 만들기
   content-pipeline 스킬 + 체크포인트 패턴
[STEP 4] 만든 스킬로 테스트·검증 (벚꽃 명소)
   ① Step 1·2 리서치 + 기획 → ② Step 3·4 이미지 + B&W 매거진 HTML → ③ Step 5·6 TTS + Remotion 9x16 영상
[STEP 5] Part 06 9 스킬 + Part 5 자산 6종 통합 정리 ★ Part 06 마무리
```

**핵심 메시지** — 그냥 'content-pipeline 스킬 만들어줘' 하지 마세요. **'리서치부터 영상까지 콘텐츠를 한 번에 만들려는데, 어떻게 워크플로우를 구성해야 할까?'**로 출발. Part 03 자료리서치/카드뉴스/리모션 매번 따로 했던 3개 작업을 **한 스킬로 묶어** 5분에 끝남 (영상 빌드 시간 별도). **있는 스킬은 재호출, 없는 기능은 자체 스크립트로** — deep-research(재호출) + 이미지 자체 스크립트(OpenAI) + TTS 자체 스크립트(OpenAI) + Remotion. 이미지·TTS 모두 OpenAI 키 1개로 통합. Part 06 가장 큰 통합.

**6 STEP 풀 파이프라인**:

```
주제 한 마디
   ↓
[1] 딥리서치 (deep-research 스킬 재호출, 폴백 WebSearch) → 01-리서치-보고서.md
[2] 카드뉴스 기획 (유형·장수·핵심 메시지) → 02-카드뉴스-기획서.md
[3] 이미지 생성 (자체 스크립트 generate_image.py, OpenAI 이미지 API) → images/card-01~12.png
[4] HTML 카드뉴스 (B&W 에디토리얼 매거진 1080x1350) → card-news.html
[5] TTS 스크립트 — 카드(씬) 1장 = 섹션 1개 구조로 작성 (## 헤더로 씬 구분) → 05-tts-script.md
[6] 음성: OpenAI TTS로 씬별로 끊어 변환 → 카드별 mp3 + 재생시간(card-timings.json)
    → 그 타이밍으로 Remotion이 카드마다 길이를 맞춰 9x16 영상 빌드 → audio/cards/*.mp3 + output.mp4
```

**체크포인트 패턴**: 각 단계마다 AskUserQuestion으로 "OK 다음 갈까요?" — 자동만이 아닌 협업.

**시연 주제**: 벚꽃 명소 (my-work 실제 산출 정합)

**Part 06 9 스킬 + Part 5 자산 6종 = 본인 평생 도구** — 본 클립이 강의 후 활용 가이드의 출발점.

**Part 5 자산 사슬**: Part 5 모든 자산 + Part 06 deep-research (재호출) + 자체 OpenAI 이미지·TTS 스크립트(나노바나나 이미지 스킬이 없어 직접 제작) + Part 03 clip-10 Remotion 프로젝트

## 단계 안내

| Phase | 내용 |
|------|------|
| A (2분) | 도입 — Part 06 마지막 ★ |
| B-1 (3분) | STEP 1 워크플로우 잡기 — "리서치부터 영상까지 한 번에 만들려는데 어떻게 구성해야 할까?" + Part 03 통합 메시지 |
| B-2 (4분) | STEP 2 보완 + 클로드코드가 실제로 할 수 있는 단계로 정의 (각 단계가 다른 스킬·도구 호출 + 체크포인트) |
| B-3 (5분) | STEP 3 content-pipeline 스킬화 + 체크포인트 패턴 |
| B-4 (6분) | STEP 4-① 테스트·검증 (벚꽃 명소) Step 1·2 (리서치 + 기획) |
| B-5 (5분) | STEP 4-② Step 3·4 (이미지 + HTML 매거진) |
| B-6 (3분) | STEP 4-③ Step 5·6 (OpenAI TTS + Remotion 9x16) |
| B-7 (2분) | STEP 5 Part 06 9 스킬 + Part 5 통합 정리 |
| C (1분) | Part 06 마무리 — 본인 평생 도구 |
| D (1분) | WRAP — Part 06 전체 |

## WRAP — Part 06 전체 정리

1. 결과물 검증:
   - `content-pipeline/SKILL.md`
   - `벚꽃명소-{날짜}/` 폴더의 6 파일 (research·기획·images·card-news.html·tts-script·output.mp4)
   - audio/ (OpenAI TTS 카드별 mp3) + Remotion 9x16 영상(output.mp4)
   - `.claude/skills/`에 **9 스킬 모두 존재** 확인
2. README.md 자동 — Part 06 9 스킬 표 + Part 5 자산 사슬 매트릭스
3. progress.json:
   - `practice_completed`에 31
   - `skills_created` 9개 전부 (deep-research / trip-advisor / naver-news / fashion-trend / audio-to-doc / morning-briefing / content-pipeline + skillers-suda 자동 생성 1개 + 비교·개선 사이클은 메타)
   - `completed_parts`에 "Part 06" 추가
4. **Part 06 전체 회고** — "가장 응용하고 싶은 스킬 1개 + 본인 일 어디에"
5. 다음 — "Part 07 실전 활용 (만든 스킬을 실전 프로젝트에 박는 파트)"
