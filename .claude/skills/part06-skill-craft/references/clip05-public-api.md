# Clip 5 — 공공 API 스킬 ★ TourAPI 여행 가이드 + 스크립트 분리 모범 (실습 26, 20분)

> 페르소나 메모 — A(마케터): API 활용신청 10분 대기 시간 안내 / B(PO): .env 보관 직관 / C(영업): 본인 일 외부 데이터 연결 응용

## 자동 셋업

```bash
mkdir -p ~/fastcampus-cc/50-my-work/Part06-스킬만들기/실습26-공공API스킬/
mkdir -p ~/fastcampus-cc/.claude/skills/trip-advisor/scripts/
python3 -c "import requests" 2>/dev/null && echo "✓ Python requests OK" || echo "ℹ pip install requests 필요"
echo "✓ 진도 폴더 + trip-advisor 스킬 폴더 (scripts 포함) 준비 완료"
```

## 브리핑

**공공데이터포털 TourAPI 첫 패턴 + 스크립트 분리 모범**. 시연 — 부산 2박3일 여행 가이드 자동 생성.

```
[사전 준비] TourAPI 활용신청 + .env에 TOURAPI_SERVICE_KEY 보관 (공공데이터포털, 약 10분 자동 승인 — 그동안 다른 작업)

[STEP 1] 워크플로우 잡기
   "공공 API로 여행 정보 가져와서 여행 가이드 만들려는데, 어떻게 워크플로우를 구성해야 할까?"
   → 단계별 워크플로우 정리
[STEP 2] 보완 + 실행 가능 단계 정의
   정리된 단계 살펴보고 보완 → 클로드코드가 실제로 할 수 있는 단계로 다듬기 (TourAPI 호출 액션·결정론 단계 분리)
[STEP 3] 스킬로 만들기
   trip-advisor 스킬 만들기 — scripts/tour_api.py 분리 (Python + requests)
[STEP 4] 만든 스킬로 테스트·검증
   "부산 여행 코스 짜줘" 호출 → 종합 여행 가이드 마크다운 자동 생성
[STEP 5] 본인 업계 공공 API 응용 (미세먼지/부동산/환율/교통)
```

**핵심 메시지** — 그냥 'TourAPI 스킬 만들어줘' 하지 마세요. **'공공 API로 여행 정보 가져와서 여행 가이드 만들려는데, 어떻게 워크플로우를 구성해야 할까?'**로 출발. clip-01 §STEP 3 'AI 의존 vs 결정론' 첫 적용 사례 — **AI에게 맡길 건 문서로 자유도, 코드화할 건 코드로 안정성**.

**`tour_api.py` 5 액션**: keyword (관광지 검색) / festival (축제) / area (지역) / stay (숙박) / detail (상세). http:// 프로토콜 사용 (TourAPI 공식 스펙).

**Part 5 자산 사슬**: 실습 21 trash-guard hook (.env 안전).

## 단계 안내

| Phase | 내용 |
|------|------|
| A (1.5분) | 도입 — TourAPI 첫 외부 API + 스크립트 분리 |
| 사전 준비 | TourAPI 활용신청 + `.env` 보관 (자동 승인 10분 대기 안내) |
| B-1 (3분) | STEP 1 워크플로우 잡기 — "여행 가이드 만들려는데 어떻게 구성해야 할까?" |
| B-2 (3분) | STEP 2 보완 + 클로드코드가 실제로 할 수 있는 단계로 정의 (TourAPI 액션 + 결정론 단계 분리) |
| B-3 (5분) | STEP 3 trip-advisor 스킬화 + `scripts/tour_api.py` 분리 |
| B-4 (4분) | STEP 4 만든 스킬로 테스트·검증 — "부산 여행 코스 짜줘" |
| B-5 (2분) | STEP 5 본인 일 응용 + 공공데이터포털 평생 활용 |
| C (1분) | 마무리 — 공공 API + 스크립트 분리 손에 |
| D (0.5분) | WRAP |

## WRAP

1. 결과물 검증 — `trip-advisor/SKILL.md` + `scripts/tour_api.py` + `.env` + `실습26/부산-여행가이드-{날짜}.md`
2. README — TourAPI 패턴 + scripts 분리 이유 + 본인 업계 공공 API 1개 후보
3. progress.json — `practice_completed`에 26, `skills_created`에 `trip-advisor`
4. 회고 — "본인 일 공공 API 한 줄"
5. 다음 — "clip-06 검색 API → 뉴스레터 HTML"
