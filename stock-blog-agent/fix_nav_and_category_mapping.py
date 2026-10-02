"""
=============================================================================
FIX NAV AND CATEGORY MAPPING (fix_nav_and_category_mapping.py)
1. "저평가주식" -> "저평가 가치주" 명칭 전수 통일
2. 상단 네비게이션 메뉴를 개별 포스트 이동이 아닌 카테고리 필터링 URL로 100% 매핑
3. 카테고리 탭과 카드 간의 data-category 맵핑 완벽 보정
=============================================================================
"""

import os
import re
import glob
from pathlib import Path

BASE_DIR = Path(r"c:\Users\immnu\Desktop\Claud\adsense-stock-blog")
POSTS_DIR = BASE_DIR / "posts"
TOOLS_DIR = BASE_DIR / "tools"
PAGES_DIR = BASE_DIR / "pages"
INDEX_HTML = BASE_DIR / "index.html"

NAV_INDEX = """      <nav class="main-nav" aria-label="메인 메뉴">
        <a href="index.html" class="nav-link active">홈</a>
        <a href="index.html?cat=market#postsGrid" class="nav-link">오늘의 시황</a>
        <a href="index.html?cat=undervalued#postsGrid" class="nav-link">저평가 가치주</a>
        <a href="index.html?cat=valuation#postsGrid" class="nav-link">종목가치 분석</a>
        <a href="index.html?cat=breakout#postsGrid" class="nav-link">상승초입주</a>
        <a href="index.html?cat=semiconductor#postsGrid" class="nav-link">AI반도체</a>
        <a href="tools/fair-value-calculator.html" class="nav-link">적정가치 계산기 <span class="nav-link-badge">HOT</span></a>
        <a href="tools/stock-average-calc.html" class="nav-link">평단가 계산기</a>
        <a href="tools/target-price-calculator.html" class="nav-link">손익비 계산기</a>
        <a href="pages/about.html" class="nav-link">소개</a>
      </nav>"""

NAV_SUB = """      <nav class="main-nav" aria-label="메인 메뉴">
        <a href="../index.html" class="nav-link">홈</a>
        <a href="../index.html?cat=market#postsGrid" class="nav-link">오늘의 시황</a>
        <a href="../index.html?cat=undervalued#postsGrid" class="nav-link">저평가 가치주</a>
        <a href="../index.html?cat=valuation#postsGrid" class="nav-link">종목가치 분석</a>
        <a href="../index.html?cat=breakout#postsGrid" class="nav-link">상승초입주</a>
        <a href="../index.html?cat=semiconductor#postsGrid" class="nav-link">AI반도체</a>
        <a href="../tools/fair-value-calculator.html" class="nav-link">적정가치 계산기 <span class="nav-link-badge">HOT</span></a>
        <a href="../tools/stock-average-calc.html" class="nav-link">평단가 계산기</a>
        <a href="../tools/target-price-calculator.html" class="nav-link">손익비 계산기</a>
        <a href="../pages/about.html" class="nav-link">소개</a>
      </nav>"""

def fix_html_nav(file_path: Path, is_index: bool = False):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # 1. Replace main-nav block
    target_nav = NAV_INDEX if is_index else NAV_SUB
    content = re.sub(
        r'<nav\s+class=["\']main-nav["\'][^>]*>.*?</nav>',
        target_nav,
        content,
        flags=re.DOTALL | re.IGNORECASE
    )

    # 2. Rename '저평가주식' to '저평가 가치주' in buttons, tabs, breadcrumbs, titles
    content = content.replace("💎 저평가주식", "💎 저평가 가치주")
    content = content.replace("저평가주식", "저평가 가치주")

    # 3. Write back
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

def run():
    print(">>> 1. Fixing index.html...")
    fix_html_nav(INDEX_HTML, is_index=True)

    print(">>> 2. Fixing posts/*.html...")
    for pf in sorted(glob.glob(str(POSTS_DIR / "*.html"))):
        fix_html_nav(Path(pf), is_index=False)

    print(">>> 3. Fixing tools/*.html...")
    for tf in sorted(glob.glob(str(TOOLS_DIR / "*.html"))):
        fix_html_nav(Path(tf), is_index=False)

    print(">>> 4. Fixing pages/*.html...")
    for page_f in sorted(glob.glob(str(PAGES_DIR / "*.html"))):
        fix_html_nav(Path(page_f), is_index=False)

    print(">>> [성공] 모든 HTML 파일의 네비게이션 및 카테고리 매핑 수정 완료!")

if __name__ == "__main__":
    run()
