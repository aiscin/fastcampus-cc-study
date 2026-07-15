import { Composition } from "remotion";
import { CardReel, FPS } from "./CardReel";
import timings from "./timings.json";

const PAD = 0.35; // 씬 사이 여유(초)
const total = timings.scenes.reduce((a: number, s: any) => a + s.sec + PAD, 0) + 0.6;

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="CardReel"
      component={CardReel}
      durationInFrames={Math.ceil(total * FPS)}
      fps={FPS}
      width={1080}
      height={1350}
    />
  );
};
