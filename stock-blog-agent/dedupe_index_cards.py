"""
=============================================================================
INDEX CARD DEDUPE (dedupe_index_cards.py)
index.html 글 목록에서 '같은 글을 가리키는 중복 카드'를 정리합니다.
=============================================================================
문제:
  예전 자동 발행 과정에서 원본 파일이 없는 카드들이 기존 글 하나로
  연결되어, 제목은 서로 다른데 링크는 같은 카드가 수십 개 생겼습니다.
  (예: 9월 모닝 브리핑 카드 다수 → 20260926-morning-market-briefing.html)
  검색엔진에는 '제목과 내용이 다른 링크'로 보여 품질 평가에 불리합니다.

동작:
  1. 링크 대상 파일이 아예 없는 카드는 제거
  2. 같은 파일을 가리키는 카드가 여러 개면, 실제 글 제목과 가장 잘 맞는
     카드 1개만 남기고 나머지는 제거
  3. 기존 index.html은 index.html.bak 으로 백업

사용법:
  python dedupe_index_cards.py          # 실제 적용
  python dedupe_index_cards.py --dry    # 무엇이 지워질지 미리보기만
"""

import re
import sys
import html as html_lib
from pathlib import Path

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent.parent / "adsense-stock-blog"
INDEX_HTML = BASE_DIR / "index.html"
POSTS_DIR = BASE_DIR / "posts"

# 카드 앞의 주석과 들여쓰기까지 한 덩어리로 잡아서 깔끔하게 제거
CARD_RE = re.compile(
    r'(?:[ \t]*<!--[^>]*-->\s*)?[ \t]*<article class="post-card".*?</article>[ \t]*\n?',
    re.DOTALL,
)


def norm(text):
    text = html_lib.unescape(text or "")
    text = text.split("|")[0]
    return re.sub(r"[\s\W_]+", "", text).lower()


def page_title(filename):
    try:
        html = (POSTS_DIR / filename).read_text(encoding="utf-8")
    except Exception:
        return ""
    m = re.search(r"<title>(.*?)</title>", html, re.DOTALL | re.IGNORECASE)
    return m.group(1) if m else ""


def card_info(card):
    href = re.search(r'href="posts/([^"#?]+)"', card)
    title = re.search(r'class="post-title">\s*<a[^>]*>(.*?)</a>', card, re.DOTALL)
    return (href.group(1) if href else None,
            re.sub(r"<[^>]+>", "", title.group(1)).strip() if title else "")


def score(card_title, real_title, href=""):
    a, b = norm(card_title), norm(real_title)
    if not a or not b:
        return 0
    if a == b:
        return 3
    if a in b or b in a:
        return 2
    # 카드 제목의 'MM월 DD일'이 파일명 날짜와 같으면 같은 글
    fd = re.match(r"\d{4}(\d{2})(\d{2})", href)
    cd = re.search(r"(\d{1,2})월\s*(\d{1,2})일", card_title)
    if fd and cd and (int(fd.group(1)), int(fd.group(2))) == (int(cd.group(1)), int(cd.group(2))):
        return 2
    # 앞 20글자가 같으면 같은 글로 간주
    return 1 if a[:20] == b[:20] else 0


def main(dry=False):
    html = INDEX_HTML.read_text(encoding="utf-8")
    cards = list(CARD_RE.finditer(html))
    print(f"[*] 전체 카드: {len(cards)}개")

    groups = {}
    remove = []
    for i, m in enumerate(cards):
        href, title = card_info(m.group(0))
        if href is None:
            continue  # 포스트 링크가 없는 카드(도구 등)는 건드리지 않음
        if not (POSTS_DIR / href).exists():
            remove.append((i, f"파일 없음: {href} | {title}"))
            continue
        groups.setdefault(href, []).append((i, title))

    for href, items in groups.items():
        if len(items) == 1:
            continue
        real = page_title(href)
        # 점수가 가장 높은 카드, 동점이면 위쪽(최신) 카드를 남김
        keep = max(items, key=lambda it: (score(it[1], real, href), -it[0]))
        print(f"   = 유지: {href[:40]} | {keep[1][:60]}")
        for it in items:
            if it is not keep:
                remove.append((it[0], f"중복 → {href[:50]} | {it[1]}"))

    remove_idx = {i for i, _ in remove}
    print(f"[*] 제거 대상: {len(remove_idx)}개 / 남는 카드: {len(cards) - len(remove_idx)}개")
    for _, why in sorted(remove):
        print("   -", why[:110])

    if dry or not remove_idx:
        return

    out, pos = [], 0
    for i, m in enumerate(cards):
        if i in remove_idx:
            out.append(html[pos:m.start()])
            pos = m.end()
    out.append(html[pos:])

    INDEX_HTML.with_suffix(".html.bak").write_text(html, encoding="utf-8")
    INDEX_HTML.write_text("".join(out), encoding="utf-8")
    print(f"[성공] index.html 정리 완료 (백업: index.html.bak)")


if __name__ == "__main__":
    main(dry="--dry" in sys.argv)
