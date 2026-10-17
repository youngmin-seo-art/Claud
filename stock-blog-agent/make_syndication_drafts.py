"""
=============================================================================
SYNDICATION DRAFTS (make_syndication_drafts.py)
valuestocklabs 글을 네이버 블로그 / 티스토리에 올릴 '요약 초안'으로 만듭니다.
=============================================================================
원칙:
  - 전문 복사 금지. 네이버는 같은 글을 유사문서로 보고 양쪽 노출을 떨어뜨립니다.
  - 초안 = 요약 + 목차 + 핵심 포인트 제목 + 원문 링크(UTM 포함).
  - 자동 '생성'만 하고 '발행'은 사람이 검토 후 직접 붙여넣습니다.

대상:
  기업분석·가이드형 글만 (시황 브리핑·뉴스 재가공 글은 수명이 짧아 제외).

결과물 (저장소 루트 기준):
  syndication/drafts/<글 파일명>/naver.txt    ← 네이버 블로그 에디터에 붙여넣기
  syndication/drafts/<글 파일명>/tistory.html ← 티스토리 'HTML 모드'에 붙여넣기
  syndication/README.md                       ← 초안 목록 (최신순)

사용법:
  python make_syndication_drafts.py                     # 대상 글 전체 (이미 만든 초안은 건너뜀)
  python make_syndication_drafts.py posts/파일명.html    # 특정 글만
  python make_syndication_drafts.py --force             # 기존 초안도 다시 생성
"""

import re
import sys
import html as html_lib
from pathlib import Path
from urllib.parse import quote

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = ROOT / "adsense-stock-blog" / "posts"
OUT_DIR = ROOT / "syndication"
DRAFTS_DIR = OUT_DIR / "drafts"
DOMAIN = "https://www.valuestocklabs.com"

# 이 단어가 파일명에 있으면 대상
INCLUDE = ("기업분석", "가치주", "guide", "stocks", "tax-saving", "krx", "screening", "스크리닝", "상승초입주")
# 이 단어가 파일명에 있으면 제외 (시황·브리핑)
EXCLUDE = ("시황", "morning", "브리핑")


def is_target(name):
    low = name.lower()
    return not any(x in low for x in EXCLUDE) and any(x in low for x in INCLUDE)


def text(fragment):
    return html_lib.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", fragment))).strip()


def meta(html, key):
    m = re.search(rf'<meta\s+(?:name|property)=["\']{re.escape(key)}["\']\s+content=(["\'])(.*?)\1', html, re.I | re.S)
    return html_lib.unescape(m.group(2)).strip() if m else ""


def parse(path):
    html = path.read_text(encoding="utf-8")
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
    title = text(h1.group(1)) if h1 else text(re.search(r"<title>(.*?)</title>", html, re.S).group(1)).split("|")[0].strip()
    headings = [re.sub(r"^\d+\.\s*", "", text(h)) for h in re.findall(r"<h2[^>]*>(.*?)</h2>", html, re.S)]
    points = []
    for label in re.findall(r"<li[^>]*>\s*<strong>(.*?)</strong>", html, re.S):
        label = text(label).rstrip(":： ")
        if 4 <= len(label) <= 40 and label not in points:
            points.append(label)
    keywords = [k.strip() for k in meta(html, "keywords").split(",") if k.strip() and "valuestocklabs" not in k.lower()]
    date = re.match(r"(\d{4})(\d{2})(\d{2})", path.name)
    return {
        "title": title,
        "desc": meta(html, "description") or meta(html, "og:description"),
        "image": meta(html, "og:image"),
        "headings": [h for h in headings if h][:8],
        "points": points[:5],
        "tags": keywords[:10],
        "date": f"{date.group(1)}-{date.group(2)}-{date.group(3)}" if date else "",
    }


def link(path, source):
    return f"{DOMAIN}/posts/{quote(path.name)}?utm_source={source}&utm_medium=blog&utm_campaign=syndication"


def naver_text(p, url):
    lines = [
        f"[제목] {p['title']}",
        "",
        f"[대표 이미지] {p['image']}  ← 다운로드해서 첫 이미지로 넣기",
        "",
        "─" * 20,
        "",
        p["desc"],
        "",
        "📌 이번 분석에서 다루는 내용",
    ]
    lines += [f"{i}. {h}" for i, h in enumerate(p["headings"], 1)]
    if p["points"]:
        lines += ["", "🔎 핵심 포인트"]
        lines += [f"• {pt}" for pt in p["points"]]
    lines += [
        "",
        "✍️ (여기에 내 생각 2~3문장 직접 추가 — 네이버는 원문과 다른 '내 의견'이 있어야 유사문서로 안 묶입니다)",
        "",
        "👉 PER·PBR 상세 수치, 적정주가 계산, 리스크 분석 전문은 아래 원문에서 확인하세요.",
        url,
        "",
        "─" * 20,
        "※ 본 글은 투자 권유가 아니며, 모든 투자 판단과 책임은 투자자 본인에게 있습니다.",
        "",
        "[태그] " + " ".join("#" + t.replace(" ", "") for t in p["tags"]),
    ]
    return "\n".join(lines) + "\n"


def tistory_html(p, url):
    e = html_lib.escape
    parts = [
        f"<!-- 제목: {e(p['title'])} -->",
        f"<!-- 태그: {e(', '.join(p['tags']))} -->",
        f'<p><img src="{e(p["image"])}" alt="{e(p["title"])}"></p>' if p["image"] else "",
        f"<p>{e(p['desc'])}</p>",
        "<h3>📌 이번 분석에서 다루는 내용</h3>",
        "<ol>" + "".join(f"<li>{e(h)}</li>" for h in p["headings"]) + "</ol>",
    ]
    if p["points"]:
        parts += ["<h3>🔎 핵심 포인트</h3>", "<ul>" + "".join(f"<li>{e(pt)}</li>" for pt in p["points"]) + "</ul>"]
    parts += [
        "<p><!-- 여기에 내 의견 2~3문장 추가 --></p>",
        f'<p>👉 상세 수치와 적정주가 계산 전문: <a href="{e(url)}" target="_blank" rel="noopener">{e(p["title"])} - Value Stock Labs</a></p>',
        '<p style="font-size:0.9em;color:#888">※ 본 글은 투자 권유가 아니며, 모든 투자 판단과 책임은 투자자 본인에게 있습니다.</p>',
    ]
    return "\n".join(x for x in parts if x) + "\n"


def write_readme():
    rows = []
    for d in sorted(DRAFTS_DIR.iterdir(), reverse=True) if DRAFTS_DIR.exists() else []:
        if (d / "naver.txt").exists():
            first = (d / "naver.txt").read_text(encoding="utf-8").splitlines()[0].replace("[제목] ", "")
            rows.append(f"| {first} | [naver.txt](drafts/{quote(d.name)}/naver.txt) | [tistory.html](drafts/{quote(d.name)}/tistory.html) |")
    OUT_DIR.mkdir(exist_ok=True)
    (OUT_DIR / "README.md").write_text(
        "# 네이버 블로그 · 티스토리 요약 초안\n\n"
        "새 기업분석 글이 배포되면 자동으로 만들어집니다. **검토 후 직접 붙여넣어 발행**하세요.\n\n"
        "- 네이버: `naver.txt` 내용을 에디터에 붙여넣고, 대표 이미지를 첫 사진으로 올린 뒤 '내 의견' 줄을 채우세요.\n"
        "- 티스토리: 글쓰기 → 우측 상단 `기본모드` → `HTML` 로 바꾼 뒤 `tistory.html` 을 붙여넣으세요.\n"
        "- 원문 링크에 UTM이 붙어 있어 GA4에서 `syndication` 캠페인으로 유입을 확인할 수 있습니다.\n\n"
        "| 글 | 네이버 | 티스토리 |\n|---|---|---|\n" + "\n".join(rows) + "\n",
        encoding="utf-8",
    )


def main(argv):
    force = "--force" in argv
    files = [a for a in argv if not a.startswith("--")]
    if files:
        paths = [POSTS_DIR / Path(f).name for f in files]
    else:
        paths = sorted(POSTS_DIR.glob("*.html"))

    made = 0
    for path in paths:
        if not path.exists() or not is_target(path.name):
            continue
        out = DRAFTS_DIR / path.stem
        if out.exists() and not force:
            continue
        p = parse(path)
        out.mkdir(parents=True, exist_ok=True)
        (out / "naver.txt").write_text(naver_text(p, link(path, "naver_blog")), encoding="utf-8")
        (out / "tistory.html").write_text(tistory_html(p, link(path, "tistory")), encoding="utf-8")
        made += 1
        print(f"[생성] {path.name}")

    write_readme()
    print(f"[완료] 새 초안 {made}개")


if __name__ == "__main__":
    main(sys.argv[1:])
