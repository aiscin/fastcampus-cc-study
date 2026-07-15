# TrendBoard 실제 빌드 프로세스 — 소스 코드 분석 기반

> 레퍼런스 앱(`ideation-workspace/10-inbox/gptaku-trend`)의 **실제 소스 코드**(Edge Function 8 +
> 페이지 9 + 마이그레이션 13)를 분석해 "이 앱이 실제로 어떤 순서·의존성으로 만들어지는가"를 정리한 문서.
> PRD 추정이 아니라 **동작하는 코드가 근거.** 빌드가이드(04)와 데이터모델(02)의 부정확한 부분도 여기서 교정.

---

## 1. 한눈에 보는 전체 구조

```
[데이터 생산: 백엔드 — Supabase Edge Functions]
  fetch-channel ──> channels
  collect-data ──> videos + video_snapshots + channels.avg_views
       │ (HTTP 체인)
       ├─> generate-tags ──> content_summaries     (Gemini)
       └─> extract-trends(7) , extract-trends(30) ──> trend_topics
  generate-strategy ──> strategy_results            (Gemini, 별도 트리거)
  manage-settings / verify-admin ──> admin_settings (비번·키 관리)

[데이터 저장: PostgreSQL]
  7 테이블 + video_details 뷰(통합 조인) + RPC 2(비번)

[데이터 소비: 프론트 — React 7페이지]
  Overview · Channels · Videos · Outliers · Trends · Strategy · Admin
  → 분석 4페이지(Overview/Videos/Outliers/Trends)는 전부 video_details 뷰 1개를 읽음
  → 지표(Score/배율/V·S)는 전부 프론트 JS에서 계산 (DB에 저장 안 함)
```

핵심 통찰 3가지:
- **자동화 진입점은 `collect-data` 하나.** cron이 이것만 부르면 태깅·트렌드까지 체인으로 연쇄.
- **`video_details` 뷰가 프론트의 단일 소스.** 이 뷰가 0순위 — 없으면 어떤 화면도 데이터가 없다.
- **지표는 DB가 아니라 프론트에서 계산.** 뷰는 원천값(views, channel_avg_views, subscriber_count)만 준다.

---

## 2. 데이터 흐름 (실제 체인)

### 매시간 자동 (cron → collect-data 1콜)
```
collect-data
  1) channels(is_active=true) 조회
  2) 각 채널: uploads 재생목록(UC→UU) → playlistItems.list(50개씩 페이지네이션)
     → videos.list(50개 콤마조인, part=snippet,statistics,contentDetails)
  3) videos UPSERT(platform_video_id) + video_snapshots INSERT(views/likes/comments)
     - 증분 모드: 이미 가진 영상을 만나면 그 지점까지만(hitExisting)
     - 초기 모드: 영상 0개거나 force_full이면 최대 max_videos_per_channel(기본 50)개
  4) channels.avg_views UPDATE = 최근 30일 발행 영상들의 "각 영상 최신 스냅샷 views" 평균
  ── 체인 (HTTP, Bearer service_role) ──
  5) POST generate-tags        → 요약 없는 영상을 Gemini로 태깅 → content_summaries UPSERT
  6) POST extract-trends {7}   → 키워드 빈도/성장률 집계 → trend_topics UPSERT
  7) POST extract-trends {30}
```

### 온디맨드 (Admin/페이지 버튼)
```
fetch-channel       ← 채널 등록 시 (channels UPSERT)
collect-data{channel_id} ← 채널 등록 직후 그 채널만 즉시 수집
generate-tags       ← Admin/Videos에서 "AI 요약 재생성"
generate-strategy   ← Strategy 페이지 "전략 생성" (video_details + trend_topics 읽어 Gemini)
manage-settings/verify-admin ← Admin 로그인·설정 저장
```

### 프론트 읽기
```
Overview/Videos/Outliers ─ select * from video_details
Trends ─ select(keywords 등) from video_details → 클라이언트에서 기간별 실시간 집계
         (※ trend_topics 테이블이 아니라 뷰에서 직접 집계)
Strategy ─ select * from strategy_results (생성은 generate-strategy)
Admin ─ manage-settings(read/save) + 각종 count
```

---

## 3. 의존성 위상정렬 (무엇을 먼저)

데이터가 흐르는 순서 = 빌드 순서.

```
channels
  → videos → video_snapshots          (collect-data가 채움)
           → content_summaries        (generate-tags가 채움, Gemini 키 필요)
  → video_details 뷰  = videos+channels+최신snapshot+content_summaries
  → trend_topics                      (extract-trends)
  → strategy_results                  (generate-strategy, 위 전부 전제)
admin_settings + RPC(verify_password)  = 모든 비번/키/모델 설정의 기반
```

함수 빌드 선후:
| 만들 함수 | 먼저 있어야 할 것 |
|----------|------------------|
| fetch-channel | channels 테이블 + `YOUTUBE_API_KEY` |
| collect-data | channels(등록된 활성 채널) + videos/video_snapshots 테이블 |
| generate-tags | videos(데이터 존재) + content_summaries + `gemini_api_key`(admin_settings) |
| extract-trends | content_summaries.keywords 채워짐 |
| generate-strategy | video_details 뷰 + trend_topics + strategy_results + gemini 키 |
| manage-settings/verify-admin | admin_settings + verify_password RPC |

---

## 4. 구현 의존 순서 — 무엇을 먼저 만들어야 하는가 (참고용)

> ⚠️ 이건 **소스의 빌드 의존 순서**(논리적 선후관계)다. 수강생이 따라하는 **워크플로우 STEP**(show-me-the-prd →
> kkirikkiri → 연결·배포)은 `04-빌드가이드.md`에 있다 — 번호 체계가 다르니 혼동하지 말 것.
> 아래는 강사가 "무엇이 무엇에 의존하는지"를 이해하고, kkirikkiri 생성 결과를 검증할 때 쓰는 사양 순서다.

### B0. 프로젝트 골격
- Vite+React+TS + shadcn/ui 다크 테마 + 사이드바 7메뉴 + 라우팅
- 사이드바: Overview(/) · Channels(/channels) · Videos(/videos) · Outliers(/outliers) · Trends(/trends) · Content Strategy(/strategy) · Admin(/admin), 하단 카테고리 Select
- 프로바이더: QueryClient → Tooltip → Toaster → BrowserRouter → **CategoryProvider** → Routes
- ✅ 검증: 7메뉴 라우팅 + 다크 테마 + 모바일 햄버거

### B1. Supabase 연결 + 스키마
- `.env.local`: `VITE_SUPABASE_URL`, `VITE_SUPABASE_PUBLISHABLE_KEY`(=anon)
- `assets/schema.sql` 적용 → 7테이블 + **video_details 뷰** + RPC 2 + admin_password seed
- ✅ 검증: Table Editor 7테이블 + `select * from video_details`(빈 결과라도 에러 없이)

### B2. Admin + 설정 관리 (Gemini 키 통로)
- `manage-settings`(service_role로 admin_settings R/W) + `verify-admin`(로그인/비번변경)
- Admin 페이지: 자체 로그인 카드 → `verify-admin` → 이후 모든 요청 body에 `password` 재전달
- 설정: gemini_api_key, ai_model_tags(기본 gemini-2.5-flash-lite), ai_model_strategy(기본 gemini-2.5-flash), max_videos_per_channel, 프롬프트 3종, 카테고리 CRUD
- ✅ 검증: 로그인 후 Gemini 키 저장 → anon으로 `gemini_api_key` select 시 안 보임(RLS)
- ⚠️ 기본 비번 `trendboard2026` 즉시 변경

### B3. 채널 등록
- `fetch-channel`(YouTube channels.list, handle/channelId 추출) + Channels 페이지(카드 그리드, URL 검증, Bulk Add, 활성토글, 삭제, 카테고리)
- 등록 직후 `collect-data{channel_id}` 즉시 호출
- ✅ 검증: URL 입력 → 채널 카드(이름/구독자/썸네일)

### B4. 수집 엔진 (collect-data)
- §2의 collect-data 로직: UC→UU, playlistItems→videos, UPSERT+snapshot, avg_views 재계산, 증분/초기 분기
- ✅ 검증: videos·video_snapshots에 행, channels.avg_views > 0, Shorts/Long 구분
- ⚠️ `search.list` 금지(100 units), `playlistItems.list`(1 unit)

### B5. Outliers 대시보드 (핵심 화면)
- video_details 읽기 → 프론트 지표 계산(§5 공식) → 요약 카드 4 + 12컬럼 정렬/필터 + Tier + content_tags 배지 + 페이지네이션 + CSV
- ✅ 검증: Score 내림차순, Ch.Avg 배율 초록, Format 필터, Tier "#1 of N"

### B6. AI 태깅 (generate-tags) — ※ summarize-videos 아님
- `generate-tags`: 요약 없는 영상 batch(기본 20) → Gemini(JSON) → content_summaries UPSERT(keywords/content_tags/summary/content_type/sentiment)
- collect-data 체인 끝에 generate-tags 호출 연결
- ✅ 검증: content_summaries에 행, Outliers/Videos에 키워드 컬러 배지
- ⚠️ 429 rate limit: 15초 대기 후 재시도, 호출 간 1.5초 sleep

### B7. Trends + extract-trends + Overview
- `extract-trends`: 기간 3분할(현재/직전), 키워드 빈도+growth_rate → trend_topics
- Trends 페이지: **video_details에서 클라이언트 실시간 집계**(기간 탭 24h/3D/7D/30D), 바 차트 + 랭킹
- Overview: 요약 카드 4 + 7일 Score 라인차트 + Recent Outliers
- ✅ 검증: 키워드 랭킹+성장률, 기간 탭, Overview 카드/차트

### B8. 배포 + 매시간 cron
- GitHub + Vercel(프론트, anon 키만) / Edge Function 배포 + Secrets(YOUTUBE_API_KEY, SERVICE_ROLE_KEY)
- pg_cron: 매시간 collect-data 1콜(→ 체인 자동). Free 막히면 cron-job.org
- ✅ 검증: 공개 URL, 다음 정시 자동 갱신

### B9. (선택) Strategy + 폴리싱
- `generate-strategy`(video_details outlier 상위 + trend_topics → Gemini → strategy_results) + Strategy 페이지
- 빈 상태/로딩 Skeleton/에러 토스트 일관화
- ✅ 검증: 전략 카드(인사이트/전략/제목공식/회피)

---

## 5. 핵심 로직·공식 (실제 코드 그대로)

```ts
// ── 프론트 지표 (Outliers.tsx / Videos.tsx) ──
const chAvgMultiplier = avgViews > 0 ? views / avgViews : 0;          // 채널 평균 대비 배율
const vsRatio         = subs > 0 ? (views / subs) * 100 : 0;          // 구독자 대비 %
// ★ Outlier Score = 배율×10 + V/S Ratio  (※ 빌드가이드 초안의 "(views/avg)*10"은 +vsRatio 누락)
const outlierScore    = avgViews > 0 ? (views / avgViews) * 10 + vsRatio : vsRatio;
const isOutlier       = chAvgMultiplier >= 1.5;   // Mega: >= 5.0
// Tier: keywords[0]로 그룹핑 → 그룹 내 outlierScore 내림차순 순위 "#1 of N"
// New This Week: published_at >= startOfWeek(월요일 시작)
```

```ts
// ── collect-data ──
uploadsPlaylistId = "UU" + platform_channel_id.slice(2);   // UCxxx → UUxxx
duration(sec) = PT(H)(M)(S) 정규식 파싱;  format = duration <= 60 ? "shorts" : "long";
avg_views = 최근 30일 발행 영상들의 (각 영상 최신 스냅샷 views) 평균;  // Math.round
```

```ts
// ── extract-trends ──
growth_rate = prevCount === 0 ? 100 : ((cur - prev) / prev) * 100;   // 소수 2자리
video_count = 고유 video_id 수;
```

```
// ── Gemini 호출 (generate-tags / generate-strategy) ──
POST https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key=...
generate-tags:     model=gemini-2.5-flash-lite, temperature=0.3
generate-strategy: model=gemini-2.5-flash,      temperature=0.5
키/모델/프롬프트는 admin_settings에서 읽음 (코드 하드코딩 아님)
content_tags 7종: Numbers/Free/Question/Time/Money/Success/Change
```

---

## 6. 기존 가이드 교정 항목 (이 분석으로 드러난 차이)

| # | 위치 | 기존(틀림) | 실제(교정) | 상태 |
|---|------|-----------|-----------|------|
| 1 | assets/schema.sql | video_details에 `v.id`, `collected_at`, content_type/sentiment 없음 | `v.id AS video_id`, `collected_at AS snapshot_at`, content_type·sentiment 포함 | ✅ **수정 완료** |
| 2 | schema.sql | content_summaries에 content_type/sentiment 없음 | 추가 | ✅ **수정 완료** |
| 3 | schema.sql | channels.category 기본 '전체' | 실제 `'AI'` NOT NULL | ✅ **수정 완료** |
| 4 | schema.sql | strategy_results에 period_days/category 없음, RPC·seed 없음 | 추가 | ✅ **수정 완료** |
| 5 | 02·04 문서 | outlierScore = (views/avg)*10 | **(views/avg)*10 + vsRatio** | ✅ **수정 완료** |
| 6 | 04 STEP 6 | AI 요약 = summarize-videos | 실제 체인은 **generate-tags** (summarize는 레거시) | ✅ **수정 완료** |
| 7 | 04 STEP 4 | 채널당 10개 수집 | 실제 기본 **50개**(max_videos_per_channel) + 증분/초기 분기 | ✅ **수정 완료** |
| 8 | 04 STEP 7 | Trends가 trend_topics 읽음 | 실제 **video_details에서 클라이언트 집계** | ✅ **수정 완료** |
| 9 | 04 전반 | 수집 주기 "매시간" | 실제 cron 주기는 자유(매시간 권장) — 체인 진입점 collect-data 1콜 | ✅ **반영** |
| 10 | 04 | 사이드바 5~6 메뉴 | 실제 **7메뉴**(+Content Strategy, +Admin) + 카테고리 Select | ✅ **수정 완료** |

> 03·05·06의 함수 목록(generate-tags/verify-admin)·env 변수명(`VITE_SUPABASE_PUBLISHABLE_KEY`)도 함께 정합화 완료.
> `trendboard-build-guide/` 전체가 레퍼런스 앱 실제 코드와 일치한다.

---

## 7. PRD엔 없던 실제 기능 (참고)

- **카테고리 시스템**(CategoryContext) — 전역, 모든 분석 페이지를 채널 카테고리로 필터
- **Tier 랭킹** — 키워드 그룹 내 순위
- **Bulk 채널 등록** — 줄단위 URL 일괄, 진행률
- **CSV export**(Videos/Outliers), **배치 재생성**(Admin), **AI 프롬프트 라이브 편집**(Admin)
- **sentiment/content_type** 표시
- **모바일/데스크톱 분기 렌더**(Videos/Outliers는 카드 vs 테이블 별도 마크업)
- 미사용 잔재: `Index.tsx`(라우터 미연결), `NavLink.tsx`(미참조), `summarize-videos`(generate-tags로 대체)
