-- =============================================================
-- TrendBoard — Supabase 전체 스키마 (실행 가능)
-- =============================================================
-- 레퍼런스 앱(gptaku-trend)의 실제 마이그레이션 13종을 단일 파일로 정리.
-- 실제 동작 코드와 100% 일치하도록 작성(video_details 뷰 컬럼명·content_type/sentiment
-- ·verify_password RPC·admin_password seed 포함). 클로드코드에게 "이 schema.sql을
-- Supabase에 적용해줘"라고 시키면 된다.
-- 적용: Supabase Dashboard → SQL Editor → 전체 붙여넣고 Run.
-- =============================================================

-- 확장
CREATE EXTENSION IF NOT EXISTS pgcrypto;        -- 비밀번호 해시(crypt/gen_salt)
CREATE EXTENSION IF NOT EXISTS pg_cron;         -- 매시간 자동 수집 (Free 티어 미지원 시 외부 cron)
CREATE EXTENSION IF NOT EXISTS pg_net;          -- cron에서 Edge Function 호출

-- 공통: updated_at 자동 갱신 트리거 함수
CREATE OR REPLACE FUNCTION public.update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SET search_path = public;

-- -------------------------------------------------------------
-- 1. channels — 모니터링 대상 YouTube 채널
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.channels (
  id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  platform_channel_id TEXT NOT NULL UNIQUE,           -- UCxxxxxxxx
  name                TEXT NOT NULL,
  thumbnail_url       TEXT,
  subscriber_count    BIGINT DEFAULT 0,
  avg_views           BIGINT DEFAULT 0,               -- 최근 30일 평균 조회수 (Outlier 기준)
  category            TEXT NOT NULL DEFAULT 'AI',     -- 채널 분류(필터용). 실제 앱 기본값 'AI'
  url                 TEXT NOT NULL,
  is_active           BOOLEAN NOT NULL DEFAULT true,
  created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TRIGGER update_channels_updated_at
  BEFORE UPDATE ON public.channels
  FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();

-- -------------------------------------------------------------
-- 2. videos — 채널의 개별 영상
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.videos (
  id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  channel_id        UUID NOT NULL REFERENCES public.channels(id) ON DELETE CASCADE,
  platform_video_id TEXT NOT NULL UNIQUE,             -- YouTube videoId
  title             TEXT NOT NULL,
  description       TEXT,
  thumbnail_url     TEXT,
  duration          INTEGER NOT NULL DEFAULT 0,       -- 초 단위
  format            TEXT NOT NULL DEFAULT 'long',     -- 'shorts'(≤60s) | 'long'
  published_at      TIMESTAMPTZ,
  created_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at        TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- (성능 개선용 — 실제 마이그레이션엔 없으나 LATERAL 뷰/조회 성능에 도움)
CREATE INDEX IF NOT EXISTS idx_videos_channel_id ON public.videos(channel_id);
CREATE INDEX IF NOT EXISTS idx_videos_published_at ON public.videos(published_at DESC);

CREATE TRIGGER update_videos_updated_at
  BEFORE UPDATE ON public.videos
  FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();

-- -------------------------------------------------------------
-- 3. video_snapshots — 매시간 수집되는 지표 시계열
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.video_snapshots (
  id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  video_id     UUID NOT NULL REFERENCES public.videos(id) ON DELETE CASCADE,
  views        BIGINT NOT NULL DEFAULT 0,
  likes        BIGINT NOT NULL DEFAULT 0,
  comments     BIGINT NOT NULL DEFAULT 0,
  collected_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_snapshots_video_collected
  ON public.video_snapshots(video_id, collected_at DESC);   -- 최신 스냅샷 LATERAL 조회 가속

-- -------------------------------------------------------------
-- 4. content_summaries — AI(Gemini) 요약/키워드/태그 (영상당 1개)
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.content_summaries (
  id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  video_id     UUID NOT NULL REFERENCES public.videos(id) ON DELETE CASCADE,
  summary      TEXT,
  keywords     TEXT[] DEFAULT '{}',                   -- ["gpt-5","벤치마크"] (소문자 정규화)
  content_tags TEXT[] DEFAULT '{}',                   -- ["Free","Numbers"]
  content_type TEXT,                                  -- 영상 유형 (Gemini 산출)
  sentiment    TEXT,                                  -- positive|neutral|negative
  created_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE(video_id)
);

CREATE TRIGGER update_content_summaries_updated_at
  BEFORE UPDATE ON public.content_summaries
  FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();

-- -------------------------------------------------------------
-- 5. trend_topics — 키워드 트렌드 집계 (extract-trends가 채움)
--    참고: Trends 화면은 이 테이블 대신 video_details에서 실시간 집계함.
--    이 테이블은 extract-trends가 기록·보관(향후 활용·이력용).
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.trend_topics (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  keyword       TEXT NOT NULL,
  mention_count INTEGER NOT NULL DEFAULT 0,
  video_count   INTEGER NOT NULL DEFAULT 0,
  growth_rate   NUMERIC(10,2) NOT NULL DEFAULT 0,     -- 이전 기간 대비 %
  period_start  TIMESTAMPTZ NOT NULL,
  period_end    TIMESTAMPTZ NOT NULL,
  created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE(keyword, period_start, period_end)
);

-- -------------------------------------------------------------
-- 6. strategy_results — AI 콘텐츠 전략 결과
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.strategy_results (
  id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  insights       TEXT[] NOT NULL DEFAULT '{}',
  strategies     JSONB  NOT NULL DEFAULT '[]',
  title_formulas TEXT[] NOT NULL DEFAULT '{}',
  avoid          TEXT[] NOT NULL DEFAULT '{}',
  period_days    INTEGER NOT NULL DEFAULT 14,
  category       TEXT NOT NULL DEFAULT '전체',
  created_at     TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- -------------------------------------------------------------
-- 7. admin_settings — 키/값 설정 (Gemini 키, 관리자 비번, 모델/프롬프트, 카테고리)
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.admin_settings (
  id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  key        TEXT UNIQUE NOT NULL,
  value      TEXT NOT NULL,
  updated_at TIMESTAMPTZ DEFAULT now()
);

-- 관리자 비밀번호 초기값 (실제 앱 기본: trendboard2026 — 운영 시 즉시 변경)
INSERT INTO public.admin_settings (key, value)
VALUES ('admin_password', crypt('trendboard2026', gen_salt('bf')))
ON CONFLICT (key) DO NOTHING;

-- 저장되는 다른 key(런타임/Admin UI가 채움):
--   gemini_api_key, max_videos_per_channel(기본 50),
--   ai_model_tags(기본 gemini-2.5-flash-lite), ai_model_strategy(기본 gemini-2.5-flash),
--   prompt_tags, prompt_summary, prompt_strategy, categories(JSON 배열)

-- =============================================================
-- 비밀번호 RPC (SECURITY DEFINER — manage-settings / verify-admin이 호출)
-- =============================================================
CREATE OR REPLACE FUNCTION public.verify_password(input_password TEXT, stored_hash TEXT)
RETURNS BOOLEAN
LANGUAGE sql SECURITY DEFINER SET search_path = public, extensions
AS $$ SELECT stored_hash = crypt(input_password, stored_hash); $$;

CREATE OR REPLACE FUNCTION public.change_admin_password(current_pw TEXT, new_pw TEXT)
RETURNS BOOLEAN
LANGUAGE plpgsql SECURITY DEFINER SET search_path = public, extensions
AS $$
DECLARE stored TEXT;
BEGIN
  SELECT value INTO stored FROM public.admin_settings WHERE key = 'admin_password';
  IF stored IS NULL OR stored <> crypt(current_pw, stored) THEN
    RETURN false;
  END IF;
  UPDATE public.admin_settings
     SET value = crypt(new_pw, gen_salt('bf')), updated_at = now()
   WHERE key = 'admin_password';
  RETURN true;
END;
$$;

-- =============================================================
-- video_details — 프론트엔드가 읽는 통합 뷰 (실제 마이그레이션 #11과 동일)
-- 영상 + 채널 + "가장 최신 스냅샷"(LATERAL) + AI 요약을 한 번에 조인.
-- 프론트는 이 뷰만 select 하고 지표(Score/배율/V·S)는 JS에서 계산.
-- 주의: 영상 PK는 v.id를 video_id 이름으로 노출. snapshot 시각은 snapshot_at.
-- =============================================================
DROP VIEW IF EXISTS public.video_details;
CREATE VIEW public.video_details AS
SELECT
  v.id                AS video_id,
  v.platform_video_id,
  v.title,
  v.description,
  v.thumbnail_url,
  v.format,
  v.duration,
  v.published_at,
  v.channel_id,
  c.name              AS channel_name,
  c.thumbnail_url     AS channel_thumbnail_url,
  c.platform_channel_id,
  c.subscriber_count,
  c.avg_views         AS channel_avg_views,
  c.category          AS channel_category,
  s.views,
  s.likes,
  s.comments,
  s.collected_at      AS snapshot_at,
  cs.summary,
  cs.keywords,
  cs.content_tags,
  cs.content_type,
  cs.sentiment
FROM public.videos v
JOIN public.channels c ON c.id = v.channel_id
LEFT JOIN LATERAL (
  SELECT vs.views, vs.likes, vs.comments, vs.collected_at
  FROM public.video_snapshots vs
  WHERE vs.video_id = v.id
  ORDER BY vs.collected_at DESC
  LIMIT 1
) s ON true
LEFT JOIN public.content_summaries cs ON cs.video_id = v.id;

-- =============================================================
-- RLS — 개인용 MVP. 대부분 공개 읽기. admin_settings 민감 키만 차단.
-- =============================================================
ALTER TABLE public.channels          ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.videos            ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.video_snapshots   ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.content_summaries ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.trend_topics      ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.strategy_results  ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.admin_settings    ENABLE ROW LEVEL SECURITY;

-- 공개 읽기/쓰기 (채널/영상/지표/요약/트렌드/전략 — 개인용)
DO $$
DECLARE t TEXT;
BEGIN
  FOREACH t IN ARRAY ARRAY['channels','videos','video_snapshots','content_summaries','trend_topics','strategy_results']
  LOOP
    EXECUTE format('CREATE POLICY "public read %1$s"   ON public.%1$I FOR SELECT USING (true);', t);
    EXECUTE format('CREATE POLICY "public insert %1$s" ON public.%1$I FOR INSERT WITH CHECK (true);', t);
    EXECUTE format('CREATE POLICY "public update %1$s" ON public.%1$I FOR UPDATE USING (true);', t);
    EXECUTE format('CREATE POLICY "public delete %1$s" ON public.%1$I FOR DELETE USING (true);', t);
  END LOOP;
END $$;

-- admin_settings: 비민감 키만 anon 읽기. gemini_api_key / admin_password는 차단.
-- INSERT/UPDATE 정책 없음 → anon 쓰기 불가. 쓰기는 service_role(manage-settings) 경유만.
CREATE POLICY "Read non-sensitive settings" ON public.admin_settings
  FOR SELECT USING (key NOT IN ('admin_password', 'gemini_api_key'));

-- =============================================================
-- 끝. 적용 후 Table Editor에서 7개 테이블 + video_details 뷰 확인.
-- AI 요약을 쓰려면 앱 Admin 페이지에서 gemini_api_key를 저장한다.
-- =============================================================
