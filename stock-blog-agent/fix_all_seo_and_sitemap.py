"""
=============================================================================
SEO & INDEXING MASTER FIX (fix_all_seo_and_sitemap.py)
전체 HTML 파일(메인, 포스트, 도구, 페이지) SEO 전수 교정 및 Sitemap/RSS 100% 동기화
=============================================================================
"""

import os
import sys
import re
import json
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent.parent / "adsense-stock-blog"
POSTS_DIR = BASE_DIR / "posts"
TOOLS_DIR = BASE_DIR / "tools"
PAGES_DIR = BASE_DIR / "pages"
INDEX_HTML = BASE_DIR / "index.html"
SITEMAP_XML = BASE_DIR / "sitemap.xml"
RSS_XML = BASE_DIR / "rss.xml"
DOMAIN = "https://www.valuestocklabs.com"

def extract_meta_content(html, name_or_prop):
    m = re.search(rf'<meta\s+(?:name|property)=["\']{re.escape(name_or_prop)}["\']\s+content=["\'](.*?)["\']', html, re.IGNORECASE)
    if not m:
        m = re.search(rf'<meta\s+content=["\'](.*?)["\']\s+(?:name|property)=["\']{re.escape(name_or_prop)}["\']', html, re.IGNORECASE)
    return m.group(1).strip() if m else ""

def extract_title(html):
    m = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
    if m:
        return re.sub(r'\s+', ' ', m.group(1)).strip()
    return "Value Stock Labs 리서치"

def fix_head_seo(html_path, page_type="post", filename=""):
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    # Determine canonical URL
    if page_type == "index":
        canonical_url = f"{DOMAIN}/"
    elif page_type == "post":
        canonical_url = f"{DOMAIN}/posts/{filename}"
    elif page_type == "tool":
        canonical_url = f"{DOMAIN}/tools/{filename}"
    elif page_type == "page":
        canonical_url = f"{DOMAIN}/pages/{filename}"
    else:
        canonical_url = f"{DOMAIN}/{filename}"

    title = extract_title(html)
    desc = extract_meta_content(html, "description") or extract_meta_content(html, "og:description") or f"{title} - Value Stock Labs 가치투자 및 금융 데이터 리서치 리포트"
    raw_img = extract_meta_content(html, "og:image") or "images/vsl-logo-neon-fire.png"
    
    # Clean image url to absolute with www
    raw_img = raw_img.replace("https://valuestocklabs.com", DOMAIN).replace("http://valuestocklabs.com", DOMAIN)
    clean_img = raw_img.replace("../", "").lstrip("/")
    if not clean_img.startswith("http"):
        img_url = f"{DOMAIN}/{clean_img}"
    else:
        img_url = clean_img

    # Date extraction
    date_match = re.search(r'(\d{4})(\d{2})(\d{2})', filename)
    if date_match:
        iso_date = f"{date_match.group(1)}-{date_match.group(2)}-{date_match.group(3)}"
    else:
        iso_date = datetime.now().strftime("%Y-%m-%d")

    # 1. Thoroughly remove existing SEO comments, canonical, robots, og, twitter, and JSON-LD
    html = re.sub(r'<!--\s*(?:Canonical\s*&|OpenGraph|Twitter\s*Card|Schema\.org).*?-->\s*', '', html, flags=re.IGNORECASE)
    html = re.sub(r'\s*<link\s+rel=["\']canonical["\'].*?>', '', html, flags=re.IGNORECASE)
    html = re.sub(r'\s*<meta\s+name=["\']robots["\'].*?>', '', html, flags=re.IGNORECASE)
    html = re.sub(r'\s*<meta\s+property=["\']og:[^"\']+["\'].*?>', '', html, flags=re.IGNORECASE)
    html = re.sub(r'\s*<meta\s+name=["\']twitter:[^"\']+["\'].*?>', '', html, flags=re.IGNORECASE)
    html = re.sub(r'\s*<script\s+type=["\']application/ld\+json["\']>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)

    # 2. Build Schema.org JSON-LD
    clean_title_only = title.split("|")[0].strip()
    if page_type == "post":
        is_news = "모닝" in title or "시황" in title or "뉴스" in title
        schema_type = "NewsArticle" if is_news else "BlogPosting"
        json_ld = {
            "@context": "https://schema.org",
            "@type": schema_type,
            "headline": clean_title_only,
            "description": desc,
            "image": [img_url],
            "datePublished": f"{iso_date}T08:30:00+09:00",
            "dateModified": f"{iso_date}T08:30:00+09:00",
            "author": {
                "@type": "Organization",
                "name": "Value Stock Labs 리서치팀",
                "url": f"{DOMAIN}/pages/about.html"
            },
            "publisher": {
                "@type": "Organization",
                "name": "Value Stock Labs",
                "logo": {
                    "@type": "ImageObject",
                    "url": f"{DOMAIN}/images/vsl-logo-neon-fire.png"
                }
            },
            "mainEntityOfPage": {
                "@type": "WebPage",
                "@id": canonical_url
            }
        }
    elif page_type == "tool":
        json_ld = {
            "@context": "https://schema.org",
            "@type": "WebApplication",
            "name": clean_title_only,
            "description": desc,
            "url": canonical_url,
            "applicationCategory": "FinanceApplication",
            "operatingSystem": "All",
            "publisher": {
                "@type": "Organization",
                "name": "Value Stock Labs",
                "url": DOMAIN
            }
        }
    elif page_type == "index":
        json_ld = {
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": "Value Stock Labs",
            "url": f"{DOMAIN}/",
            "image": f"{DOMAIN}/images/vsl-logo-neon-fire.png",
            "description": desc,
            "publisher": {
                "@type": "Organization",
                "name": "Value Stock Labs 리서치팀"
            }
        }
    else:
        json_ld = {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": clean_title_only,
            "description": desc,
            "url": canonical_url,
            "publisher": {
                "@type": "Organization",
                "name": "Value Stock Labs"
            }
        }

    seo_injection = f"""
  <!-- Canonical & Search Engine Indexing -->
  <link rel="canonical" href="{canonical_url}">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">

  <!-- OpenGraph / SNS Meta -->
  <meta property="og:type" content="{'website' if page_type == 'index' else 'article'}">
  <meta property="og:site_name" content="Value Stock Labs">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="{img_url}">
  <meta property="og:url" content="{canonical_url}">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{img_url}">

  <!-- Schema.org JSON-LD Structured Data -->
  <script type="application/ld+json">
{json.dumps(json_ld, ensure_ascii=False, indent=2)}
  </script>
"""

    # Clean double blank lines in head
    html = re.sub(r'\n\s*\n\s*\n', '\n\n', html)

    # Inject right before </head> or after <head>
    if "</head>" in html:
        html = html.replace("</head>", f"{seo_injection}\n</head>")
    elif "<head>" in html:
        html = html.replace("<head>", f"<head>{seo_injection}")
    else:
        html = f"<head>{seo_injection}</head>" + html

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    return {
        "url": canonical_url,
        "title": title,
        "desc": desc,
        "date": iso_date,
        "type": page_type,
        "filename": filename
    }

def rebuild_all():
    print("=" * 60)
    print("[SEO & Sitemap Fix] Rebuilding all HTML files and sitemap.xml")
    print("=" * 60)

    all_pages = []

    # 1. Main index.html
    print("1. index.html 교정 중...")
    idx_info = fix_head_seo(INDEX_HTML, page_type="index", filename="index.html")
    all_pages.append(idx_info)

    # 2. Tools
    print("\n2. tools/ 교정 중...")
    for t in sorted(os.listdir(TOOLS_DIR)):
        if t.endswith(".html"):
            t_path = TOOLS_DIR / t
            info = fix_head_seo(t_path, page_type="tool", filename=t)
            all_pages.append(info)
            print(f"  [완료] tools/{t}")

    # 3. Pages
    print("\n3. pages/ 교정 중...")
    for p in sorted(os.listdir(PAGES_DIR)):
        if p.endswith(".html"):
            p_path = PAGES_DIR / p
            info = fix_head_seo(p_path, page_type="page", filename=p)
            all_pages.append(info)
            print(f"  [완료] pages/{p}")

    # 4. Posts
    print("\n4. posts/ 포스트 교정 중...")
    posts_list = []
    for post_file in sorted(os.listdir(POSTS_DIR)):
        if post_file.endswith(".html"):
            post_path = POSTS_DIR / post_file
            info = fix_head_seo(post_path, page_type="post", filename=post_file)
            all_pages.append(info)
            posts_list.append(info)
            print(f"  [완료] posts/{post_file[:40]}...")

    # 5. Rebuild sitemap.xml
    print(f"\n5. sitemap.xml 재구축 중... (총 {len(all_pages)}개 페이지 전수 포함)")
    sitemap_lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    
    # Priority rules
    for item in all_pages:
        url = item["url"]
        ptype = item["type"]
        date = item["date"]
        
        if ptype == "index":
            priority = "1.0"
            freq = "daily"
        elif ptype == "post":
            priority = "0.9"
            freq = "weekly"
        elif ptype == "tool":
            priority = "0.8"
            freq = "monthly"
        else:
            priority = "0.6"
            freq = "monthly"

        sitemap_lines.append(f"""  <url>
    <loc>{url}</loc>
    <lastmod>{date}</lastmod>
    <changefreq>{freq}</changefreq>
    <priority>{priority}</priority>
  </url>""")

    sitemap_lines.append('</urlset>\n')
    with open(SITEMAP_XML, "w", encoding="utf-8") as f:
        f.write("\n".join(sitemap_lines))
    print(f"[성공] sitemap.xml 생성 완료: {len(all_pages)}개 URL 등록")

    # 6. Rebuild rss.xml
    print(f"\n6. rss.xml 재구축 중...")
    posts_sorted = sorted(posts_list, key=lambda x: x["date"], reverse=True)
    rss_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">',
        '  <channel>',
        '    <title>Value Stock Labs | 저평가 가치주 &amp; 상승초입주 리서치</title>',
        f'    <link>{DOMAIN}/</link>',
        '    <description>데이터 기반 국내외 저평가 우량주, 상승초입주 차트 분석, AI 반도체 HBM 수혜주, 공모주 청약 및 실시간 주식 계산기를 제공하는 금융 리서치 블로그</description>',
        '    <language>ko-KR</language>',
        f'    <lastBuildDate>{datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0900")}</lastBuildDate>',
        f'    <atom:link href="{DOMAIN}/rss.xml" rel="self" type="application/rss+xml"/>',
        ''
    ]

    for p in posts_sorted[:60]:
        try:
            dt = datetime.strptime(p["date"], "%Y-%m-%d")
            rfc_date = dt.strftime("%a, %d %b %Y 08:30:00 +0900")
        except Exception:
            rfc_date = datetime.now().strftime("%a, %d %b %Y 08:30:00 +0900")

        clean_title = p["title"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        clean_desc = p["desc"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

        rss_lines.append(f"""    <item>
      <title>{clean_title}</title>
      <link>{p['url']}</link>
      <guid>{p['url']}</guid>
      <pubDate>{rfc_date}</pubDate>
      <description>{clean_desc}</description>
    </item>""")

    rss_lines.append('  </channel>\n</rss>\n')
    with open(RSS_XML, "w", encoding="utf-8") as f:
        f.write("\n".join(rss_lines))
    print(f"[성공] rss.xml 생성 완료: 최신 {min(60, len(posts_sorted))}개 포스트 등록")

if __name__ == "__main__":
    rebuild_all()
