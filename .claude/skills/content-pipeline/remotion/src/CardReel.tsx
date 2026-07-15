import React from "react";
import {
  AbsoluteFill, Audio, Sequence, staticFile,
  interpolate, useCurrentFrame, continueRender, delayRender,
} from "remotion";
import timings from "./timings.json";
import cards from "./cards.json"; // { css, cards: string[] } — card-news.html에서 추출

export const FPS = 30;
const PAD = 0.35;
const RED = "#E8002D";

// public 서빙 경로로 치환 (/fonts, /images → staticFile prefix)
const PREFIX = staticFile("__p__").replace("__p__", "");
const fixUrls = (s: string) =>
  s.split("/fonts/").join(PREFIX + "fonts/").split("/images/").join(PREFIX + "images/");

// @font-face는 JS(FontFace API)로 직접 로드하므로 CSS에서 제거 (fonts.ready 행 방지)
const CSS = fixUrls((cards as any).css).replace(/@font-face\s*\{[^}]*\}/g, "");
const CARD_HTML = (cards as any).cards.map(fixUrls);

const FONTS: [string, number, string][] = [
  ["Pretendard", 400, "Pretendard-Regular.woff2"],
  ["Pretendard", 600, "Pretendard-SemiBold.woff2"],
  ["Pretendard", 700, "Pretendard-Bold.woff2"],
  ["Pretendard", 900, "Pretendard-Black.woff2"],
  ["BlackHanSans", 400, "BlackHanSans-Regular.ttf"],
];

const OVERRIDE = `
  .scene-card{ width:1080px; height:1350px; position:relative; }
  .scene-card .card{ max-width:none !important; width:1080px !important; height:1350px !important;
    border-radius:0 !important; box-shadow:none !important; }
`;

// ── 이징 ──
const clamp = (x: number) => Math.max(0, Math.min(1, x));
const easeOut = (p: number) => 1 - Math.pow(1 - clamp(p), 3);
const rise = (t: number, d: number, dur = 0.55, dist = 46) => {
  const e = easeOut((t - d) / dur);
  return `opacity:${e};transform:translateY(${(1 - e) * dist}px)`;
};
const pop = (t: number, d: number, dur = 0.5) => {
  const e = easeOut((t - d) / dur);
  return `opacity:${e};transform:scale(${0.84 + 0.16 * e})`;
};
const grow = (t: number, d: number, dur = 0.9) => {
  const e = easeOut((t - d) / dur);
  return `transform:scaleX(${e})`;
};

const useFonts = () => {
  const [handle] = React.useState(() => delayRender("fonts", { timeout: 60000 }));
  React.useEffect(() => {
    (async () => {
      try {
        await Promise.all(FONTS.map(async ([fam, w, file]) => {
          const ff = new FontFace(fam, `url(${staticFile("fonts/" + file)})`, { weight: String(w) });
          await ff.load();
          (document as any).fonts.add(ff);
        }));
      } catch (e) { /* 실패해도 진행 */ }
      continueRender(handle);
    })();
  }, [handle]);
};

// 씬별 프레임 구동 등장 효과 (JSX 계산 → 프레임 정확)
const animCss = (uid: string, t: number) => `
  .${uid} .kicker,.${uid} .num{${rise(t, 0.05)}}
  .${uid} h2{${rise(t, 0.18, 0.6)}}
  .${uid} .sub{${rise(t, 0.42)}}
  .${uid} .toc{${rise(t, 0.42, 0.6)}}
  .${uid} .stage{opacity:${easeOut((t - 0.48) / 0.4)}}
  .${uid} .stage>.prod:nth-child(1){${pop(t, 0.5)}}
  .${uid} .stage>.prod:nth-child(2){${pop(t, 0.66)}}
  .${uid} .prow .p:nth-child(1){${pop(t, 0.55, 0.45)}}
  .${uid} .prow .p:nth-child(2){${pop(t, 0.68, 0.45)}}
  .${uid} .prow .p:nth-child(3){${pop(t, 0.81, 0.45)}}
  .${uid} .prow .p:nth-child(4){${pop(t, 0.94, 0.45)}}
  .${uid} .hero .big{${pop(t, 0.5, 0.6)}}
  .${uid} .trio .t:nth-child(1){${pop(t, 0.5)}}
  .${uid} .trio .t:nth-child(2){${pop(t, 0.64)}}
  .${uid} .trio .t:nth-child(3){${pop(t, 0.78)}}
  .${uid} .fill{${grow(t, 0.6)};transform-origin:left center}
  .${uid} .rankbadge.m{${pop(t, 0.6)}}
  .${uid} .rankbadge.f{${pop(t, 0.78)}}
  .${uid} .body,.${uid} .link,.${uid} .cap,.${uid} .note,.${uid} .src{${rise(t, 0.55)}}
  .${uid} .cta{${pop(t, 0.95, 0.6)}}
`;

const Scene: React.FC<{ scene: any; html: string; durF: number }> = ({ scene, html, durF }) => {
  const frame = useCurrentFrame();
  const t = frame / FPS;
  const uid = `sc${scene.no}`;
  const op = interpolate(frame, [0, 6, durF - 6, durF], [0, 1, 1, 0], {
    extrapolateLeft: "clamp", extrapolateRight: "clamp",
  });
  return (
    <AbsoluteFill style={{ opacity: op, alignItems: "center", justifyContent: "center" }}>
      <style dangerouslySetInnerHTML={{ __html: animCss(uid, t) }} />
      <div className={`scene-card ${uid}`} dangerouslySetInnerHTML={{ __html: html }} />
      <Audio src={staticFile(scene.file)} />
    </AbsoluteFill>
  );
};

export const CardReel: React.FC = () => {
  useFonts();
  const frame = useCurrentFrame();

  let acc = 0;
  const seqs = (timings.scenes as any[]).map((s) => {
    const from = Math.round(acc * FPS);
    const durF = Math.round((s.sec + PAD) * FPS);
    acc += s.sec + PAD;
    return { s, from, durF, html: CARD_HTML[s.no - 1] };
  });
  const totalF = seqs.reduce((a, x) => Math.max(a, x.from + x.durF), 0);
  const prog = interpolate(frame, [0, totalF], [0, 100], { extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{ background: "#000" }}>
      <style dangerouslySetInnerHTML={{ __html: CSS + OVERRIDE }} />
      {seqs.map(({ s, from, durF, html }) => (
        <Sequence key={s.no} from={from} durationInFrames={durF}>
          <Scene scene={s} html={html} durF={durF} />
        </Sequence>
      ))}
      <AbsoluteFill style={{ justifyContent: "flex-start" }}>
        <div style={{ height: 8, width: `${prog}%`, background: RED }} />
      </AbsoluteFill>
      {(timings as any).bgm ? <Audio src={staticFile("bgm.mp3")} volume={0.16} /> : null}
    </AbsoluteFill>
  );
};
