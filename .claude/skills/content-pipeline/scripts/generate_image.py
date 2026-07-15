#!/usr/bin/env python3
"""카드뉴스 이미지 생성 — content-pipeline 파이프라인 [3]단계 (결정론 영역).

02-plan.json의 style_lock + 카드별 image_prompt를 읽어 OpenAI 이미지 API를 호출하고,
1088x1360으로 받아 1080x1350(4:5)으로 crop해서 images/card-NN.png로 저장한다.

매번 같은 입력 → 같은 절차(API 호출·crop)를 보장하려고 스크립트로 분리했다.
카피·기획(무엇을 그릴지)은 SKILL.md(AI)가 02-plan.json에 담고, 여기선 그대로 실행만 한다.

사용법:
  python3 generate_image.py <plan.json 폴더> [--quality low|medium|high] [--only 1,3,5]

키: 프로젝트 루트 .env의 OPENAI_API_KEY 자동 로드.
"""
import argparse, base64, json, os, re, sys
from pathlib import Path


def load_key():
    # 스크립트 기준 프로젝트 루트(.env)를 위로 훑어 찾는다
    env_key = os.environ.get("OPENAI_API_KEY")
    if env_key:
        return env_key
    here = Path(__file__).resolve()
    for parent in [here] + list(here.parents):
        env = parent / ".env"
        if env.is_file():
            for line in env.read_text(encoding="utf-8").splitlines():
                m = re.match(r"\s*OPENAI_API_KEY\s*=\s*(.+)", line)
                if m:
                    return m.group(1).strip().strip('"').strip("'")
    sys.exit("✗ OPENAI_API_KEY를 .env나 환경변수에서 못 찾음")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("workdir", help="02-plan.json이 있는 폴더")
    ap.add_argument("--quality", default=None, help="low|medium|high (기본: plan의 api_defaults)")
    ap.add_argument("--only", default=None, help="일부 카드만: 예 1,3,5")
    args = ap.parse_args()

    work = Path(args.workdir).expanduser().resolve()
    plan = json.loads((work / "02-plan.json").read_text(encoding="utf-8"))
    ad = plan.get("api_defaults", {})
    model = ad.get("model", "gpt-image-2")
    size = ad.get("size", "1088x1360")
    quality = args.quality or ad.get("quality", "low")
    crop_w, crop_h = (int(x) for x in ad.get("crop_to", "1080x1350").split("x"))

    only = None
    if args.only:
        only = {int(x) for x in args.only.split(",")}

    from openai import OpenAI
    from PIL import Image
    import io

    client = OpenAI(api_key=load_key())
    img_dir = work / "images"
    img_dir.mkdir(exist_ok=True)

    cards = [c for c in plan["cards"] if only is None or c["card_no"] in only]
    print(f"▶ {len(cards)}장 생성 시작 (model={model}, size={size}, quality={quality})")

    for c in cards:
        n = c["card_no"]
        prompt = c["image_prompt"]
        # style_lock이 프롬프트에 안 박혀 있으면 뒤에 붙여 톤 고정
        if plan.get("style_lock") and plan["style_lock"][:40] not in prompt:
            prompt = f"{prompt} {plan['style_lock']}"
        try:
            resp = client.images.generate(
                model=model, prompt=prompt, size=size, quality=quality,
                background=ad.get("background", "opaque"),
            )
            raw = base64.b64decode(resp.data[0].b64_json)
            im = Image.open(io.BytesIO(raw)).convert("RGB")
            # 중앙 crop → 4:5
            W, H = im.size
            left = max(0, (W - crop_w) // 2)
            top = max(0, (H - crop_h) // 2)
            im = im.crop((left, top, left + crop_w, top + crop_h))
            out = img_dir / f"card-{n:02d}.png"
            im.save(out)
            print(f"  ✓ card-{n:02d}  {c.get('title','')[:22]}")
        except Exception as e:
            print(f"  ✗ card-{n:02d} 실패: {type(e).__name__}: {str(e)[:160]}")

    print(f"완료 → {img_dir}")


if __name__ == "__main__":
    main()
