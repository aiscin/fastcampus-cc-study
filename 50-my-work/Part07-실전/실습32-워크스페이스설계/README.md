# 실습 32 — 워크스페이스 설계 (Part 07 Clip 1)

- **날짜**: 2026-07-04
- **모드/모델**: Claude Code · Opus 4.8 (검토: kkirikkiri Agent Teams + Codex 크로스모델)
- **결과물**: `설계도.md` (v3.1 — 설계도 + 아키타입 카탈로그 10종 + 가드 7종 계약) · `하네스검토-토론종합-2026-07-04.md` (검토 리포트)

## 검토·개선 이력 (하네스 "검증·갭 메우기" 루프 실습)
1. **닥터 4종 끝장 토론** (kkirikkiri Agent Teams, Opus) — 지시층·강제층·침투·감사 4관점 적대 검토. 감사관 단독 78/B가 관점 충돌로 **C+**까지 강등(강제층 88→46 자기수정). P0 4·가드 6종 도출 → v2 반영.
2. **Codex 크로스모델 재검토** (build≠review family) — v2의 설계 오류 3건(G-A PostToolUse 차단불가·G-B 백업우회·복사≠실행) 적발 → v3 교정.
3. **Codex 2·3차** — v3의 요약↔상세 자기모순 + /audit 낙제계약 정합 → v3.1. **최종 CLOSED, 빌드 GO.**

## 무엇을 만들었나
"**워크스페이스 빌더 (메타하네스)**" 설계도 — 대화·요청서로 새 워크스페이스를 설계·점검·생성하는 작업실.

- **아키타입**: 개발(메타) — 카탈로그 10종(핵심6+선택3+메타1)을 골라 찍어냄
- **지시 층**: /new-workspace + 하네스 닥터 4종 + /audit, "자연어 우선 활성" 규칙
- **강제 층**: 가드 7종 (per-run 쓰기잠금 · inbox 반입/반출 스캔 · 스킬복사 게이트 · 실행 게이트 · 위험신호 확인 · 자식 PII · gitignore 순서)
- **6칸 트리**: `00-inbox → 10-standards → 20-blueprints → 30-drafts → 40-output → 90-archive`
- 인터뷰 확정 4가지(상호작용·출력·완성도·스킬재사용) + fastcampus-cc 이식 요소 9종 반영

## v3.2 추가 (2026-07-08 · 반복운영 관점)
설계도를 실사용 반복 관점에서 재검토해 3건 반영(설계도 B-3):
- **G-H 플러그인 상속 deny 스탬프** — 마켓플레이스 플러그인은 복사 없이 자식에 전역 상속되어 게이트를 우회 → 자식 settings.json에 deny로 스탬프.
- **Clip 2 MVP 슬라이스** — 아키타입1(리서치)+가드3(G-B·G-E·G-F)+/audit로 한 바퀴 완주 후 증분.
- **가드 발화 로그** — 가드가 막은 기록을 `guard-log.jsonl`에 남겨 "사고 나면 늘린다" 피드백 루프 완성.

관련 워크스페이스 자산도 함께 만듦:
- `20-references/skill-capabilities.json` — 스킬 16종 능력 매니페스트(G-C/G-G 원장) + 플러그인 상속 목록
- `30-templates/research-profiles/` — deep-research 인터뷰 건너뛰기용 쿼리 프로파일 3종
- `20-references/tools/verify_citations.py` — 딥리서치 인용 실측 검증
- `.claude/commands/skill-checkup.md` — 스킬 가벼운 정기 점검 커맨드
- `CLAUDE.md` "플러그인·스킬 운영 규칙" — 위 자산들을 반복작업에 물리는 지시층

## 다음
Clip 2 — 빌더 안에 닥터 4종 + /audit + /new-workspace를 만들어 이 설계도를 실제 워크스페이스로 찍는다. **MVP 슬라이스(아키타입1+가드3)로 착수.**
