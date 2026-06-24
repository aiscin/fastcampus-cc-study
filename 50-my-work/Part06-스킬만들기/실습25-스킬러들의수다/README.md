# 실습25 — skillers-suda로 만든 `ideation-funnel` 스킬

| 항목 | 내용 |
|---|---|
| 완료 | 2026-06-22 |
| 클립 | Part 06 / Clip 4 (skillers-suda) |
| 모델 | Claude Opus 4.8 |
| 모드 | 기본 (대화형) |
| 만든 스킬 | **ideation-funnel** (아이디어 깔때기) |
| 제작 도구 | skillers-suda (4 전문가 인터뷰) |

## 무엇을 만들었나

막연한 한 줄 생각을 **"지금 바로 클로드코드로 만들 수 있는 것"**으로 좁혀주는 아이데이션 스킬.
skillers-suda가 4명의 전문가(기획자·사용자·전문가·검수자)를 실제로 병렬 소집해 분석 → 그 결과로 SKILL.md 초안을 만들고, 직접 테스트·반복 개선으로 디벨롭했다.

## 최종 7단계 워크플로우

```
1 발산        막연한 생각 → 3개 질문으로 의도 좁히기 (+ 입력 방어)
2 레퍼런스 검토  로컬 스캔 + 외부 딥리서치(본문 fetch·교차검증·신뢰도 A~E)
3 후보 3개     난이도 태그 붙인 "만들 거리" 후보
4 선택        review 체크포인트
4.5 전문가 검토  도메인 전문가 3~4명 + Critic(refute) 병렬 검토 → 개선 채택
5 명세+다듬기   추가 인터뷰 → 명세서 → 의도대로 수정 루프
6 핸드오프      구현 단계·첫 명령어·수용 기준 든 문서 저장
```

## 구성 파일

- `skill-source/SKILL.md` — 7단계 본문 (검증 9 PASS / 0 FAIL)
- `skill-source/references/reference-scan-guide.md` — Step 2 (deep-research 방법론)
- `skill-source/references/expert-review-guide.md` — Step 4.5 (kkirikkiri 응용)
- `skill-source/references/handoff-template.md` — Step 6 형식
- `skill-source/evals/evals.json` — 트리거 테스트 5종
- 활성본: `.claude/skills/ideation-funnel/`

## 실전 테스트 — 튀르키예 신혼여행 릴스 대본기

실제로 스킬을 끝까지 돌려 `ideation/20260622-1803-turkiye-honeymoon-reels/` 생성:
- 실행마다 폴더 분리(타임스탬프) → 반복해도 안 섞임
- `resource/`에 레퍼런스 검토 + deep-research 보고서·노트 저장
- 실제 WebSearch+fetch로 "잘되는 정보형 릴스 구성" 검증 수치 확보(훅 2~3초·길이 15~30초·자막 48~60px 등)
- 핸드오프 문서까지 산출

## 발견·개선 (직접 테스트로 잡은 것)

1. 플러그인 스킬 스캔 glob이 헛돌던 버그 → `*/*/*` 깊이로 수정(실측 검증)
2. "중간에 멈춰도 자산" 원칙이 단계에 안 묶임 → draft append 명시
3. 한 줄 Next Step → 상세 핸드오프 문서로 격상
4. 실행마다 폴더 분리 + resource/ 추가
5. 레퍼런스 검토에 deep-research 방법론 도입
6. 전문가 팀 검토(Step 4.5) — kkirikkiri 알맹이만 경량 차용

## Part 5 자산 사슬

- `deep-research`(실습23) → Step 2 레퍼런스 검토 방법론으로 재활용
- kkirikkiri(Part 04) → Step 4.5 동적 전문가 팀 패턴 응용

## 메타 흐름 회고

"그냥 만들어줘"가 아니라 skillers-suda 인터뷰 → 직접 테스트 → 6차례 반복 보완으로,
처음 한 줄 아이디어가 레퍼런스 딥리서치·다전문가 검토·개인화까지 갖춘 스킬로 자랐다.
SKILL.md를 쓴 건 클로드코드지만, 어떻게 물어보고 어떻게 굴려보느냐가 결과를 갈랐다.
