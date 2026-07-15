#!/usr/bin/env python3
"""
verify_citations.py — 딥리서치 보고서의 인용을 '선언'이 아니라 '장치'로 검증한다.

deep-research의 Phase 6 체크리스트("All URLs are accessible", "No orphan citations")는
LLM이 스스로 "확인했다"고 말하는 구조라 실제 검증이 아니다. 이 스크립트가 실측한다:

  1) 본문 마크다운에서 URL을 뽑아 실제로 살아있는지 HTTP 확인 (dead link)
  2) sources.jsonl(있으면)의 출처 중 본문에서 한 번도 인용 안 된 것 = 고아 출처
  3) 본문이 인용한 URL이 sources.jsonl에 없으면 = 미등록 인용

사용:
  python3 verify_citations.py <보고서.md 또는 폴더> [--sources sources.jsonl] [--timeout 8]

결과는 stdout에 JSON, 사람용 요약은 stderr. dead link가 있으면 exit 1.
"""
import sys
import os
import re
import json
import argparse
import urllib.request
import urllib.error

URL_RE = re.compile(r'https?://[^\s\)\]\>"\'`]+')


def collect_md_files(target):
    if os.path.isfile(target):
        return [target]
    files = []
    for root, _, names in os.walk(target):
        for n in names:
            if n.endswith(".md"):
                files.append(os.path.join(root, n))
    return files


def extract_urls(files):
    urls = {}
    for f in files:
        try:
            with open(f, encoding="utf-8") as fh:
                text = fh.read()
        except Exception:
            continue
        for m in URL_RE.finditer(text):
            u = m.group(0).rstrip(".,;")
            urls.setdefault(u, []).append(os.path.basename(f))
    return urls


def load_sources(path):
    if not path or not os.path.exists(path):
        return []
    out = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return out


def check_url(url, timeout):
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status < 400, r.status
    except urllib.error.HTTPError as e:
        # HEAD 막는 서버 많음 → GET로 재시도
        if e.code in (403, 405):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=timeout) as r:
                    return r.status < 400, r.status
            except Exception as e2:
                return False, getattr(e2, "code", "ERR")
        return False, e.code
    except Exception:
        return False, "ERR"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target", help="보고서 .md 파일 또는 폴더")
    ap.add_argument("--sources", help="sources.jsonl 경로", default=None)
    ap.add_argument("--timeout", type=int, default=8)
    ap.add_argument("--no-net", action="store_true", help="URL 생존 확인 건너뛰기(고아/미등록만 검사)")
    args = ap.parse_args()

    files = collect_md_files(args.target)
    if not files:
        print("검사할 .md 파일을 찾지 못했습니다.", file=sys.stderr)
        sys.exit(2)

    body_urls = extract_urls(files)
    sources = load_sources(args.sources)
    source_urls = {s.get("url", "").rstrip(".,;") for s in sources if s.get("url")}

    dead = []
    if not args.no_net:
        for u in body_urls:
            ok, status = check_url(u, args.timeout)
            if not ok:
                dead.append({"url": u, "status": status, "in": body_urls[u]})

    orphan = sorted(source_urls - set(body_urls)) if source_urls else []
    unregistered = sorted(set(body_urls) - source_urls) if source_urls else []

    report = {
        "files_scanned": len(files),
        "urls_in_body": len(body_urls),
        "sources_registered": len(source_urls),
        "dead_links": dead,
        "orphan_sources": orphan,
        "unregistered_citations": unregistered,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))

    print("\n=== 인용 검증 요약 ===", file=sys.stderr)
    print(f"본문 URL {len(body_urls)}개 / 등록 출처 {len(source_urls)}개", file=sys.stderr)
    print(f"깨진 링크: {len(dead)}개", file=sys.stderr)
    if source_urls:
        print(f"고아 출처(등록됐지만 미인용): {len(orphan)}개", file=sys.stderr)
        print(f"미등록 인용(본문엔 있지만 출처목록에 없음): {len(unregistered)}개", file=sys.stderr)
    if dead:
        print("\n깨진 링크:", file=sys.stderr)
        for d in dead:
            print(f"  [{d['status']}] {d['url']}", file=sys.stderr)

    sys.exit(1 if dead else 0)


if __name__ == "__main__":
    main()
