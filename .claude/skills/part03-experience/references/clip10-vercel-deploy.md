# Clip 10: Vercel 배포 — 내 포트폴리오 인터넷에 올리기

> Part 03 / Ch 04 / 실습 13 / ~20분
> 패턴: 자동 셋업 → 영상 보면서 같이 따라하기 → "완료" → WRAP
> 대응 클립: `30-practice-design/part-03-체험하기/clip-10-Vercel배포.md`
> 모범답안: `50-my-work/Part03-체험하기/실습13-Vercel배포/p3-c09-따라하기.md`

---

## 자동 셋업 (진행 안내 출력 직전 스킬이 즉시 Bash로 실행)

```bash
# 1) 워크스페이스 루트 자동 감지
WS="$(pwd)"
while [ "$WS" != "/" ] && [ ! -f "$WS/CLAUDE.md" ]; do WS="$(dirname "$WS")"; done
if [ "$WS" = "/" ]; then
  WS="$(pwd)"
  while [ "$WS" != "/" ] && [ ! -d "$WS/40-mock-data" ]; do WS="$(dirname "$WS")"; done
fi
[ "$WS" = "/" ] && { echo "⚠ 워크스페이스 루트 못 찾음"; exit 1; }
echo "워크스페이스: $WS"

# 2) 경로
DEST="$WS/50-my-work/Part03-체험하기/실습13-Vercel배포"
SRC="$WS/50-my-work/Part03-체험하기/실습12-포트폴리오수정"

mkdir -p "$DEST"
cd "$DEST"

# 3) Clip 9 결과물(portfolio-final.html) 통째 복사
if [ -d "$SRC" ]; then
  cp -r "$SRC"/* ./ 2>/dev/null
  rm -f README.md
fi

echo "=== 결과 ==="
ls -la
```

**셋업 결과 한 줄 안내**:
- portfolio-final.html 있음 → "✓ 실습13-Vercel배포 폴더 준비 완료. Clip 9에서 만든 portfolio-final.html 가져왔어요. 이제 Vercel 가입 + 배포로 갑니다."
- 없으면 portfolio.html이라도 → "✓ 폴더 준비 완료. portfolio-final.html이 없어 1차 portfolio.html을 가져왔어요."
- 둘 다 없음 → "⚠ Clip 8/9 결과물 없네요. 먼저 Clip 8/9부터 진행해주세요."

---

## 진행 안내 (스킬이 한 메시지로 출력)

```
Clip 10 — Vercel 배포를 시작합니다. (Part 03 마지막)

■ 오늘 할 거
Clip 9의 portfolio-final.html →
  • 공개 URL https://[프로젝트명].vercel.app
한 사이클로 만듭니다.

로컬 file:///… 주소를 진짜 인터넷 주소로 바꾸는 작업입니다.

■ 진행 방식
영상에서 STEP 1~5 순서대로 실습이 진행됩니다.
영상 일시정지·재생 자유롭게 하면서 본인 워크스페이스에서 같이 따라하세요.

■ STEP 흐름

  STEP 1. 작업 폴더 진입 + Vercel 가입 (스킬이 폴더+portfolio-final.html 자동 준비 완료)
    이미 셋업된 폴더: 50-my-work/Part03-체험하기/실습13-Vercel배포/
    그대로 이 채팅창에서 STEP 2부터 진행.
    + 브라우저: https://vercel.com/signup (영상 일시정지 30초)
      Continue with Email 또는 Continue with GitHub — 무료, 신용카드 X.

  STEP 2. 1단계 질문하기 (B) — "할 수 있어? 어떻게 해?"
    "이 HTML(portfolio-final.html)을 인터넷에 진짜 주소로 올리고 싶거든.
     너가 배포해주려면 어떻게 해야 하냐? 할 수 있냐?"
    클로드코드가 호스팅 옵션 펼침 (Vercel · Netlify · GitHub Pages · Cloudflare 비교).

  STEP 3. 2단계 기획하기 (U) — "단계별 흐름"
    "좋아. 그중 가장 빠른 방법으로 가자. Vercel이 좋다면 단계별로 어떻게 진행될지 흐름 보여줘.
     내가 직접 해야 하는 부분이랑 너가 자동으로 처리할 부분 구분해서."
    클로드코드가 흐름 펼침: CLI 설치 → index.html 복사 → Magic Link 인증 (메일 클릭)
                  → vercel deploy --prod → URL 출력.

  STEP 4. 3단계 만들기 (I) — 배포 실행
    "그 흐름대로 진행해줘. Vercel CLI 설치부터 배포까지.
     Magic Link 인증은 내가 메일 확인할 거니까 거기서 멈추고 알려줘."
    Vercel CLI 설치 허락 시 Y → 인증 단계에서 메일 클릭 → 자동 재개 → URL 출력.

  STEP 5. 4+5단계 검토 + 부분 수정 (L+D)
    URL 브라우저에서 열기 → 데스크톱·스마트폰 둘 다 확인.
    선택 부분 수정: "프로젝트 이름을 [원하는이름]으로 바꿔서 재배포. 다른 건 그대로"

■ 시작
1. 영상 시작 → STEP 1부터 따라가기
2. 영상 끝나면 이 채팅창에 "완료" 또는 "/wrap" 입력 → 결과물 자동 정리

※ Vercel 가입은 무료. 신용카드 필요 없음.
※ Magic Link 메일 안 오면 스팸함 확인.
```

---

## 자유 실습 (스킬 SLEEP)

**WRAP 트리거**: `완료` / `/wrap` / `끝` / `다음 클립`
**도움 요청 트리거**: `막혔어요` / `도와줘`

### 도움 안내

```
어디서 막히셨어요?

  • portfolio-final.html 못 찾음 → Clip 9 폴더에서 cp 다시 실행
  • Vercel 가입 안 됨 → https://vercel.com/signup 다시 시도 (Email 또는 GitHub)
  • vercel: command not found → "npm install -g vercel 실행" 안내
  • 설치 권한 에러 → "sudo 없이 npm 글로벌 경로 설정"
  • Magic Link 메일 안 옴 → 스팸함 확인. 또는 터미널에 표시된 Continue in browser 링크 직접 복사
  • 배포 후 URL 404 → "portfolio-final.html을 index.html로 복사 후 재배포"
  • CSS/JS 적용 안 됨 → "외부 파일 참조 없이 모두 index.html 인라인으로 재생성"
  • 프로젝트 이름 중복 → "숫자/년도 추가. 예: -2026"

여전히 막히면 더 구체적으로 알려주세요.
```

---

## WRAP

### 1. 파일 검증

`50-my-work/Part03-체험하기/실습13-Vercel배포/` 안 + 브라우저에서 점검:
- `https://[프로젝트명].vercel.app` URL 발급 + 실제로 열림
- 데스크톱 + 스마트폰 양쪽에서 정상 표시 (선택 권장)

URL 없으면 "STEP 4 배포 안 됐어요. 지금 진행할까요?" 한 번 확인.

### 2. README.md 자동 작성

```markdown
# 실습 13 — Vercel 배포 (포트폴리오 공개 URL)

- 완료: {ISO 8601}
- 모델: {claude --version}
- 모드: {Auto / Accept-edits / Default}

## 진행 방식
영상 보면서 실습 (STEP 1~5).

## 5단계 사이클
- 1 질문하기 (B): "배포 어떻게 할 수 있어?"
- 2 기획하기 (U): 호스팅 옵션 비교 → Vercel 단계 받기
- 3 만들기 (I): CLI 설치 → 인증 → 배포 → URL
- 4 검토하기 (L): URL 열림 / 데스크톱·스마트폰
- 5 개선하기 (D): "프로젝트 이름 [X]로 재배포"

## 결과물
- 공개 URL: {입력 — https://[name].vercel.app}

## 핵심 발견
{자유 입력한 한 줄}

## 다음
Part 03 종료 — 데이터·콘텐츠·포트폴리오까지 전부 대화로 만들어 본 클립 모음 완료.
```

### 3. progress.json 업데이트

```json
{
  "practice_completed": [..., "실습 13"],
  "completed_chapters": [..., "Ch 04"],
  "completed_parts": [..., "Part 03"],
  "current_clip": null,
  "last_activity": "{ISO 8601}"
}
```

### 4. 다음 안내

```
✓ 실습 13 (Vercel 배포) 완료. Part 03 종료.
  공개 URL: {입력한 URL}

Part 03에서 만든 결과물 — 분석 답변·차트·보고서·대시보드·리서치·카드뉴스·영상·포트폴리오·공개 URL — 모두 대화로 만들었습니다.
```

---

## EDGE CASES

| 상황 | 대응 |
|---|---|
| portfolio-final.html 없음 | "Clip 9 폴더에서 복사하세요" + cp 명령 |
| Vercel CLI 설치 실패 | "npm 글로벌 권한 설정" 안내 |
| Magic Link 메일 안 옴 | 스팸함 확인 / 터미널 링크 직접 복사 |
| 배포 후 404 | "portfolio-final.html을 index.html로 복사 후 재배포" |
| 한글 파일명 배포 실패 | "영문으로 정리 후 재배포" |
| 프로젝트 이름 중복 | "숫자/년도 추가" 안내 |
| 부분 수정인데 전체 다시 배포 | "다른 건 그대로" 명시 누락 |
| `완료` 입력 후 URL 없음 | "어느 STEP에서 멈췄나요?" 확인 |
