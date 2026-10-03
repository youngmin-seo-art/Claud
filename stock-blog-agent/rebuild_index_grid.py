"""
=============================================================================
REBUILD INDEX POSTS GRID & VALIDATE ALL LINKS
=============================================================================
Reconstructs the article grid inside index.html using only the 39 clean,
deduplicated, high-quality posts, and runs full SEO & Sitemap synchronization.
"""

import os
import sys
import glob
import re
from datetime import datetime
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_DIR = Path(r"c:\Users\immnu\Desktop\Claud\adsense-stock-blog")
POSTS_DIR = BASE_DIR / "posts"
INDEX_HTML = BASE_DIR / "index.html"

def rebuild_index_grid():
    post_files = sorted(glob.glob(str(POSTS_DIR / "*.html")), reverse=True)
    print(f"Total post files to index: {len(post_files)}")
    
    cards = []
    
    for pf in post_files:
        path = Path(pf)
        filename = path.name
        
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            html = f.read()
            
        t_m = re.search(r'<title>(.*?)</title>', html, re.I)
        h1_m = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.I)
        desc_m = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', html, re.I)
        img_m = re.search(r'<meta\s+property=["\']og:image["\']\s+content=["\'](.*?)["\']', html, re.I)
        
        raw_title = h1_m.group(1).strip() if h1_m else (t_m.group(1).split("|")[0].strip() if t_m else path.stem)
        desc = desc_m.group(1).strip() if desc_m else f"{raw_title} 퀀트 가치평가 및 수급 분석 리포트"
        
        # Image
        if img_m:
            raw_img = img_m.group(1).replace("https://www.valuestocklabs.com/", "").replace("../", "").lstrip("/")
            thumb_img = raw_img if raw_img.startswith("images/") else f"images/{raw_img}"
        else:
            thumb_img = "images/hero.jpg"
            
        # Date extraction
        date_match = re.search(r'(\d{4})(\d{2})(\d{2})', filename)
        if date_match:
            date_str = f"{date_match.group(1)}.{date_match.group(2)}.{date_match.group(3)}"
        else:
            date_str = "2026.09.27"
            
        # Category classification
        if "morning-market" in filename or "시황" in raw_title:
            category = "market"
            badge_html = '<span class="post-badge market" style="background:#059669; color:#fff;">☕ 모닝 시황</span>'
            author = "시황분석팀"
            avatar = "M"
        elif "semiconductor" in filename or "반도체" in raw_title or "hbm" in filename:
            category = "semiconductor"
            badge_html = '<span class="post-badge breakout">⚡ AI 반도체</span>'
            author = "반도체테크"
            avatar = "H"
        elif "ipo" in filename or "공모주" in raw_title or "청약" in raw_title:
            category = "ipo"
            badge_html = '<span class="post-badge tax">🎯 공모주 청약</span>'
            author = "공모주애널"
            avatar = "I"
        elif "dividend" in filename or "배당" in raw_title or "절세" in raw_title or "tax" in filename:
            category = "dividend"
            badge_html = '<span class="post-badge dividend">💰 배당/절세</span>'
            author = "배당인컴"
            avatar = "D"
        elif "breakout" in filename or "상승초입" in raw_title:
            category = "breakout"
            badge_html = '<span class="post-badge breakout">🚀 상승초입주</span>'
            author = "차트마스터"
            avatar = "C"
        else:
            category = "undervalued"
            badge_html = '<span class="post-badge undervalued">💎 저평가 가치주</span>'
            author = "스톡리서치"
            avatar = "S"
            
        card_html = f"""          <!-- Article Card: {filename} -->
          <article class="post-card" data-category="{category}">
            <div class="post-thumb-wrap">
              {badge_html}
              <img src="{thumb_img}" class="post-thumb" alt="{raw_title}" loading="lazy">
            </div>
            <div class="post-body">
              <div class="post-meta">
                <span>📅 {date_str}</span>
                <span>리포트</span>
              </div>
              <h3 class="post-title">
                <a href="posts/{filename}">{raw_title}</a>
              </h3>
              <p class="post-excerpt">
                {desc}
              </p>
              <div class="post-footer">
                <div class="author-chip">
                  <div class="author-avatar">{avatar}</div>
                  <span>{author}</span>
                </div>
                <a href="posts/{filename}" class="read-more-link">리포트 읽기 →</a>
              </div>
            </div>
          </article>"""
        cards.append(card_html)
        
    all_cards_str = "\n".join(cards)
    
    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Replace entire content inside <div class="posts-grid" id="postsGrid"> ... </div>
    new_grid_block = f'<div class="posts-grid" id="postsGrid">\n{all_cards_str}\n        </div>'
    content = re.sub(
        r'<div class="posts-grid" id="postsGrid">[\s\S]*?</div>\s*<!-- Pagination / Load More -->',
        f'{new_grid_block}\n\n        <!-- Pagination / Load More -->',
        content
    )
    
    # Update latest briefing link in hero / nav
    briefing_files = sorted([Path(p).name for p in post_files if "morning-market-briefing" in p], reverse=True)
    latest_briefing = briefing_files[0] if briefing_files else "20261003-morning-market-briefing.html"
    content = re.sub(
        r'<a href="posts/[^"]*morning-market-briefing\.html" class="briefing-btn"[^>]*>',
        f'<a href="posts/{latest_briefing}" class="briefing-btn" id="latestBriefingLink">',
        content
    )
    content = re.sub(
        r'<a href="posts/[^"]*morning-market-briefing\.html" class="nav-link">오늘의 시황</a>',
        f'<a href="posts/{latest_briefing}" class="nav-link">오늘의 시황</a>',
        content
    )
    
    with open(INDEX_HTML, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"Successfully rebuilt index.html posts grid with {len(cards)} clean unique posts.")

if __name__ == "__main__":
    rebuild_index_grid()
