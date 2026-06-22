<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-03-19 | Updated: 2026-03-19 -->

# fastcampus-cc

## Purpose
패스트캠퍼스 수강생이 실제로 사용하는 학습용 Claude Code 워크스페이스다. 강의의 성공 여부는 이 폴더가 문서의 약속을 실제로 구현하고 있는지에 크게 좌우된다.

## Key Files
| File | Description |
|------|-------------|
| `README.md` | 학생용 시작 가이드. |
| `CLAUDE.md` | 학습용 기본 컨텍스트 파일. |
| `progress.json` | 진행률과 레벨 상태 저장용 파일. |
| `.claude/settings.json` | Claude Code 설정 파일. |

## Subdirectories
| Directory | Purpose |
|-----------|---------|
| `.claude/` | 스킬, 커맨드, 설정. |
| `mock-data/` | 실습용 샘플 데이터. |
| `my-work/` | 학생이 만든 결과물을 쌓는 작업 공간. |
| `references/` | 예시와 참고 자료. |
| `rules/` | 학습용 규칙 문서. |

## For AI Agents

### Working In This Directory
- 학생이 직접 치게 되는 슬래시 명령과 README의 안내가 실제로 맞아야 한다.
- 실습에서 참조하는 샘플 파일, 커맨드, 스킬 이름이 실제로 존재하는지 확인한 뒤 문서를 수정한다.
- 존재하지 않는 명령을 README나 실습 문서에 남겨두지 않는다.
- `my-work/`와 `.claude/skills/` 중 어디에 학생 작업물을 저장할지 일관되게 유지한다.

### Testing Requirements
- Part별 실습 시연 경로는 실제로 이 워크스페이스에서 재현 가능한지 확인한다.
- `progress.json`을 읽는 기능을 만들면 실제 필드명과 일치시킨다.
- 커맨드/스킬을 추가하면 README도 같이 갱신한다.

## Dependencies

### Internal
- `30-practice-design/`
- `35-session-test/`
- `80-open-clo/`

<!-- MANUAL: Any manually added notes below this line are preserved on regeneration -->
