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
import subprocess
from urllib.parse import quote
import html as html_lib
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

DATES_JSON = Path(__file__).resolve().parent / "post_dates.json"


def extract_meta_content(html, name_or_prop):
    # 여는 따옴표와 같은 종류의 따옴표에서만 끝나도록 역참조(\1) 사용.
    # (이전 정규식은 '굴욕' 같은 작은따옴표에서 설명이 잘리는 버그가 있었음)
    key = re.escape(name_or_prop)
    m = re.search(rf'<meta\s+(?:name|property)=["\']{key}["\']\s+content=(["\'])(.*?)\1', html, re.IGNORECASE | re.DOTALL)
    if not m:
        m = re.search(rf'<meta\s+content=(["\'])(.*?)\1\s+(?:name|property)=["\']{key}["\']', html, re.IGNORECASE | re.DOTALL)
    return html_lib.unescape(m.group(2).strip()) if m else ""


def repair_broken_meta(html):
    """content="... "따옴표" ..." 처럼 속성 안의 큰따옴표가 이스케이프되지 않아
    설명이 중간에서 끊긴 <meta> 줄을 복구합니다 (한 줄짜리 meta 태그만 대상)."""
    def fix(m):
        inner = m.group(3)
        if '"' not in inner:
            return m.group(0)
        return f'{m.group(1)}content="{inner.replace(chr(34), "&quot;")}"{m.group(4)}'
    return re.sub(
        r'^(\s*<meta\s+(name|property)=["\'][^"\']+["\']\s+)content="(.*)"(\s*/?>)\s*$',
        fix, html, flags=re.MULTILINE)


def attr(value):
    """HTML 속성값용 이스케이프 (따옴표·& 포함)"""
    return html_lib.escape(value, quote=True)


def xml_text(value):
    return html_lib.escape(value, quote=False)


def _load_dates():
    try:
        with open(DATES_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _git_first_added(path):
    """git 이력에서 파일이 처음 추가된 날짜(YYYY-MM-DD). 실패 시 빈 문자열."""
    try:
        out = subprocess.run(
            ["git", "log", "--diff-filter=A", "--format=%cs", "--", str(path)],
            cwd=path.parent, capture_output=True, text=True, timeout=30,
        ).stdout.strip().splitlines()
        return out[-1] if out else ""
    except Exception:
        return ""


def _index_card_dates():
    """index.html 카드에 적힌 날짜 (파일명 → YYYY-MM-DD)"""
    dates = {}
    try:
        html = INDEX_HTML.read_text(encoding="utf-8")
    except Exception:
        return dates
    for card in re.findall(r'<article class="post-card".*?</article>', html, re.DOTALL):
        href = re.search(r'href="posts/([^"]+)"', card)
        d = re.search(r'📅\s*(\d{4})[.-](\d{2})[.-](\d{2})', card)
        if href and d and href.group(1) not in dates:
            dates[href.group(1)] = f"{d.group(1)}-{d.group(2)}-{d.group(3)}"
    return dates


_DATES = _load_dates()
_CARD_DATES = None


def resolve_date(rel_key, path, filename):
    """발행일 결정 순서: 파일명 날짜 → post_dates.json → index 카드 날짜 → git 최초 추가일 → 오늘.
    한 번 정해진 날짜는 post_dates.json에 고정되어, 재실행해도 '오늘'로 바뀌지 않음."""
    global _CARD_DATES
    m = re.match(r'(\d{4})(\d{2})(\d{2})', filename)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    if rel_key in _DATES:
        return _DATES[rel_key]
    if _CARD_DATES is None:
        _CARD_DATES = _index_card_dates()
    date = _CARD_DATES.get(filename) if rel_key.startswith("posts/") else ""
    date = date or _git_first_added(path) or datetime.now().strftime("%Y-%m-%d")
    _DATES[rel_key] = date
    return date


def save_dates():
    with open(DATES_JSON, "w", encoding="utf-8") as f:
        json.dump(dict(sorted(_DATES.items())), f, ensure_ascii=False, indent=2)
        f.write("\n")

def extract_title(html):
    m = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
    if m:
        return html_lib.unescape(re.sub(r'\s+', ' ', m.group(1)).strip())
    return "Value Stock Labs 리서치"

def fix_head_seo(html_path, page_type="post", filename=""):
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    html = repair_broken_meta(html)

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
    # 글 대표 이미지가 사이트 로고로 되어 있으면 본문 첫 이미지(썸네일)로 교체
    if page_type == "post" and "vsl-logo" in raw_img:
        body_img = re.search(r'<img[^>]+src=["\'](?:\.\./)?(images/(?!vsl-logo)[^"\']+)["\']', html, re.IGNORECASE)
        if body_img:
            raw_img = body_img.group(1)
    
    # Clean image url to absolute with www
    raw_img = raw_img.replace("https://valuestocklabs.com", DOMAIN).replace("http://valuestocklabs.com", DOMAIN)
    clean_img = raw_img.replace("../", "").lstrip("/")
    if not clean_img.startswith("http"):
        img_url = f"{DOMAIN}/{clean_img}"
    else:
        img_url = clean_img

    # Date extraction (재실행할 때마다 '오늘'로 바뀌지 않도록 고정 날짜 사용)
    rel_key = "index.html" if page_type == "index" else f"{page_type}s/{filename}"
    iso_date = resolve_date(rel_key, Path(html_path), filename)

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
  <link rel="canonical" href="{attr(canonical_url)}">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">

  <!-- OpenGraph / SNS Meta -->
  <meta property="og:type" content="{'website' if page_type == 'index' else 'article'}">
  <meta property="og:site_name" content="Value Stock Labs">
  <meta property="og:title" content="{attr(title)}">
  <meta property="og:description" content="{attr(desc)}">
  <meta property="og:image" content="{attr(img_url)}">
  <meta property="og:url" content="{attr(canonical_url)}">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{attr(title)}">
  <meta name="twitter:description" content="{attr(desc)}">
  <meta name="twitter:image" content="{attr(img_url)}">

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

    # index.html의 lastmod = 가장 최근 포스트 발행일
    if posts_list:
        idx_info["date"] = max(p["date"] for p in posts_list)
    _DATES.pop("index.html", None)
    save_dates()

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
    <loc>{xml_text(quote(url, safe=':/?=&#%'))}</loc>
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
    posts_sorted = sorted(posts_list, key=lambda x: (x["date"], x["filename"]), reverse=True)
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

        clean_title = xml_text(p["title"])
        clean_desc = xml_text(p["desc"])
        link = xml_text(quote(p['url'], safe=':/?=&#%'))

        rss_lines.append(f"""    <item>
      <title>{clean_title}</title>
      <link>{link}</link>
      <guid isPermaLink="true">{link}</guid>
      <pubDate>{rfc_date}</pubDate>
      <description>{clean_desc}</description>
    </item>""")

    rss_lines.append('  </channel>\n</rss>\n')
    with open(RSS_XML, "w", encoding="utf-8") as f:
        f.write("\n".join(rss_lines))
    print(f"[성공] rss.xml 생성 완료: 최신 {min(60, len(posts_sorted))}개 포스트 등록")

if __name__ == "__main__":
    rebuild_all()
