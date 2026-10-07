import os
import shutil
import json
import re
from pathlib import Path

# Paths
WORKSPACE = Path(r"c:\Users\immnu\Desktop\Claud")
SOURCE_DIR = WORKSPACE / "blog new agent" / "output" / "현대글로비스-가치주-기업분석"
BLOG_DIR = WORKSPACE / "adsense-stock-blog"
DEST_IMAGES_DIR = BLOG_DIR / "images" / "hyundai-glovis"
POSTS_DIR = BLOG_DIR / "posts"
FILENAME = "20261008-현대글로비스-가치주-기업분석-영업익-2조-돌파와-2026년-밸류에이션-총정리.html"
TARGET_HTML_PATH = POSTS_DIR / FILENAME

# 1. Create image dir & copy images
DEST_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
src_images = SOURCE_DIR / "images"
for img_file in src_images.glob("*.png"):
    shutil.copy2(img_file, DEST_IMAGES_DIR / img_file.name)
    print(f"Copied image: {img_file.name} -> {DEST_IMAGES_DIR}")

# 2. Read final.html from source
with open(SOURCE_DIR / "final.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# 3. Update image paths in HTML from ./images/ to ../images/hyundai-glovis/
# and enhance header navigation and SEO head without changing the page's format/styling
html_content = html_content.replace('src="./images/', 'src="../images/hyundai-glovis/')
html_content = html_content.replace('src="images/', 'src="../images/hyundai-glovis/')

# Ensure brand logo links back to blog home
html_content = html_content.replace('<a href="#" class="brand-logo">ValueStock<span>Labs</span></a>', '<a href="../index.html" class="brand-logo">ValueStock<span>Labs</span></a>')
html_content = html_content.replace('<span class="badge-preview">Preview Mode</span>', '<a href="../index.html" class="badge-preview" style="text-decoration:none;">홈으로</a>')

# Add SEO meta tags and AdSense to head if not present
seo_head = """  <meta name="description" content="연간 영업이익 2조 원을 돌파하며 역대 최고 실적을 쓴 현대글로비스(086280). 글로벌 PCTC 선복 부족 수혜, 비계열 매출 53% 확대, 보스턴 다이내믹스 지분 가치 및 파격적인 주주환원 정책까지 2026년 가치투자 핵심 포인트를 완벽 정리합니다.">
  <meta name="keywords" content="현대글로비스, 현대글로비스 주가, 086280, PCTC 선복, 보스턴 다이내믹스, 로보틱스, 정의선, 지배구조 개편, 저평가 가치주, 배당성향, 밸류업">
  <meta name="author" content="ValueStockLabs 리서치팀">
  <link rel="canonical" href="https://www.valuestocklabs.com/posts/20261008-현대글로비스-가치주-기업분석-영업익-2조-돌파와-2026년-밸류에이션-총정리.html">
  <link rel="icon" type="image/x-icon" href="../favicon.ico">
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="Value Stock Labs">
  <meta property="og:title" content="현대글로비스 주가 전망 및 기업분석: 영업익 2조 돌파와 2026년 밸류에이션 총정리 (086280)">
  <meta property="og:description" content="연간 영업이익 2조 원을 돌파하며 역대 최고 실적을 쓴 현대글로비스. 글로벌 PCTC 선복 부족 수혜, 비계열 매출 53% 확대, 보스턴 다이내믹스 지분 가치 및 파격적인 주주환원 정책까지 완벽 정리합니다.">
  <meta property="og:image" content="https://www.valuestocklabs.com/images/hyundai-glovis/thumbnail.png">
  <meta property="og:url" content="https://www.valuestocklabs.com/posts/20261008-현대글로비스-가치주-기업분석-영업익-2조-돌파와-2026년-밸류에이션-총정리.html">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="현대글로비스 주가 전망 및 기업분석: 영업익 2조 돌파와 2026년 밸류에이션 총정리 (086280)">
  <meta name="twitter:description" content="연간 영업이익 2조 원을 돌파하며 역대 최고 실적을 쓴 현대글로비스 핵심 투자 포인트 총정리">
  <meta name="twitter:image" content="https://www.valuestocklabs.com/images/hyundai-glovis/thumbnail.png">
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7807868644631223" crossorigin="anonymous"></script>
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "BlogPosting",
    "headline": "현대글로비스 주가 전망 및 기업분석: 영업익 2조 돌파와 2026년 밸류에이션 총정리 (086280)",
    "description": "연간 영업이익 2조 원을 돌파하며 역대 최고 실적을 쓴 현대글로비스. 글로벌 PCTC 선복 부족 수혜, 비계열 매출 53% 확대, 보스턴 다이내믹스 지분 가치 및 주주환원 정책 총정리.",
    "image": ["https://www.valuestocklabs.com/images/hyundai-glovis/thumbnail.png"],
    "datePublished": "2026-10-08T08:30:00+09:00",
    "dateModified": "2026-10-08T08:30:00+09:00",
    "author": {
      "@type": "Organization",
      "name": "ValueStockLabs 리서치팀",
      "url": "https://www.valuestocklabs.com/pages/about.html"
    },
    "publisher": {
      "@type": "Organization",
      "name": "Value Stock Labs",
      "logo": {
        "@type": "ImageObject",
        "url": "https://www.valuestocklabs.com/images/vsl-logo-neon-fire.png"
      }
    },
    "mainEntityOfPage": {
      "@type": "WebPage",
      "@id": "https://www.valuestocklabs.com/posts/20261008-현대글로비스-가치주-기업분석-영업익-2조-돌파와-2026년-밸류에이션-총정리.html"
    }
  }
  </script>"""

if "<meta name=\"description\"" not in html_content:
    html_content = html_content.replace("<title>", seo_head + "\n  <title>")

# Write the post HTML
with open(TARGET_HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"Saved post HTML to: {TARGET_HTML_PATH}")

# 4. Update index.html
INDEX_HTML = BLOG_DIR / "index.html"
with open(INDEX_HTML, "r", encoding="utf-8") as f:
    idx_content = f.read()

post_card = f"""          <!-- Auto-Generated Article: Hyundai Glovis -->
          <article class="post-card" data-category="undervalued">
            <div class="post-thumb-wrap">
              <span class="post-badge undervalued" style="background: linear-gradient(135deg, #4f46e5, #3b82f6); color:#fff; font-weight:700;">💎 저평가 가치주 PICK</span>
              <img src="images/hyundai-glovis/thumbnail.png" class="post-thumb" alt="현대글로비스 주가 전망 및 기업분석: 영업익 2조 돌파와 2026년 밸류에이션 총정리 (086280)" loading="lazy">
            </div>
            <div class="post-body">
              <div class="post-meta">
                <span>📅 2026-10-08</span>
                <span style="color: #38bdf8; font-weight: bold;">⭐ 심층 기업분석</span>
              </div>
              <h3 class="post-title">
                <a href="posts/{FILENAME}">현대글로비스 주가 전망 및 기업분석: 영업익 2조 돌파와 2026년 밸류에이션 총정리 (086280)</a>
              </h3>
              <p class="post-excerpt">
                연간 영업이익 2조 원을 돌파하며 역대 최고 실적을 쓴 현대글로비스(086280)! 글로벌 PCTC 선복 부족 수혜, 비계열 매출 53% 확대, 보스턴 다이내믹스 지분 가치 및 파격적인 3개년 주주환원 정책을 심층 분석합니다.
              </p>
              <div class="post-footer">
                <div class="author-chip">
                  <div class="author-avatar" style="background: #4f46e5;">H</div>
                  <span>가치투자분석팀</span>
                </div>
                <a href="posts/{FILENAME}" class="read-more-link">리포트 읽기 →</a>
              </div>
            </div>
          </article>
"""

if FILENAME not in idx_content:
    target_marker = '<div class="posts-grid" id="postsGrid">'
    idx_content = idx_content.replace(target_marker, target_marker + "\n" + post_card)
    with open(INDEX_HTML, "w", encoding="utf-8") as f:
        f.write(idx_content)
    print("Updated index.html with new post card")

# 5. Update sitemap.xml
SITEMAP_XML = BLOG_DIR / "sitemap.xml"
with open(SITEMAP_XML, "r", encoding="utf-8") as f:
    sitemap_content = f.read()

sitemap_entry = f"""  <url>
    <loc>https://www.valuestocklabs.com/posts/{FILENAME}</loc>
    <lastmod>2026-10-08</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
</urlset>"""

if FILENAME not in sitemap_content:
    sitemap_content = sitemap_content.replace("</urlset>", sitemap_entry)
    with open(SITEMAP_XML, "w", encoding="utf-8") as f:
        f.write(sitemap_content)
    print("Updated sitemap.xml")

# 6. Update rss.xml
RSS_XML = BLOG_DIR / "rss.xml"
with open(RSS_XML, "r", encoding="utf-8") as f:
    rss_content = f.read()

rss_item = f"""    <item>
      <title>현대글로비스 주가 전망 및 기업분석: 영업익 2조 돌파와 2026년 밸류에이션 총정리 (086280)</title>
      <link>https://www.valuestocklabs.com/posts/{FILENAME}</link>
      <guid>https://www.valuestocklabs.com/posts/{FILENAME}</guid>
      <pubDate>Thu, 08 Oct 2026 08:30:00 +0900</pubDate>
      <description>연간 영업이익 2조 원을 돌파하며 역대 최고 실적을 쓴 현대글로비스. 글로벌 PCTC(자동차운반선) 선복 부족 수혜, 비계열 매출 53% 확대, 보스턴 다이내믹스 지분 가치 및 파격적인 주주환원 정책까지 2026년 가치투자 핵심 포인트를 완벽 정리합니다.</description>
    </item>
  </channel>"""

if FILENAME not in rss_content:
    rss_content = rss_content.replace("  </channel>", rss_item)
    with open(RSS_XML, "w", encoding="utf-8") as f:
        f.write(rss_content)
    print("Updated rss.xml")

# 7. Update published_history.json
HISTORY_FILE = WORKSPACE / "stock-blog-agent" / "published_history.json"
if HISTORY_FILE.exists():
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            history = json.load(f)
    except Exception:
        history = []
else:
    history = []

if not any(item.get("filename") == FILENAME for item in history if isinstance(item, dict)):
    history.insert(0, {
        "title": "현대글로비스 주가 전망 및 기업분석: 영업익 2조 돌파와 2026년 밸류에이션 총정리 (086280)",
        "filename": FILENAME,
        "date": "2026-10-08",
        "category": "저평가 가치주",
        "published_at": "2026-10-08 08:30:00"
    })
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
    print("Updated published_history.json")

print("ALL PUBLISHING TASKS COMPLETED SUCCESSFULLY!")
