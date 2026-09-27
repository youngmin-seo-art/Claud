"""
=============================================================================
FIX ALL INTERNAL LINKS & ENSURE 100% RESOLUTION
=============================================================================
Scans every HTML file in the blog and automatically fixes any link pointing to
deleted/renamed posts, ensuring 0 broken links across the entire site.
"""

import os
import sys
import glob
import re
from pathlib import Path
from html.parser import HTMLParser

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_DIR = Path(r"c:\Users\immnu\Desktop\Claud\adsense-stock-blog")
POSTS_DIR = BASE_DIR / "posts"

def build_valid_posts_map():
    """Builds a lookup map for resolving deleted/renamed post links."""
    existing_posts = [p.name for p in POSTS_DIR.glob("*.html")]
    print(f"Total valid post targets: {len(existing_posts)}")
    
    # Keyword & normalized map
    lookup = {}
    for p in existing_posts:
        lookup[p] = p
        
        # normalized hangul+alphanumeric signature
        norm = re.sub(r'[^가-힣a-zA-Z0-9]', '', p)
        lookup[norm[:15]] = p
        
    return existing_posts, lookup

def resolve_target(old_href, source_file_path, existing_posts, lookup):
    """Resolves an old href into a valid existing relative URL."""
    # Split anchor and query
    parts = old_href.split("#")
    base_part = parts[0].split("?")[0]
    hash_part = f"#{parts[1]}" if len(parts) > 1 else ""
    
    old_filename = Path(base_part).name
    
    # 1. Direct match
    if old_filename in existing_posts:
        return None # already valid
        
    # 2. Morning market briefings -> latest briefing
    if "morning-market-briefing" in old_filename:
        # Check if 20260927 exists, else 20260926
        target_name = "20260927-morning-market-briefing.html" if (POSTS_DIR / "20260927-morning-market-briefing.html").exists() else "20260926-morning-market-briefing.html"
        return fix_rel_path(source_file_path, target_name) + hash_part

    # 3. Strip media tags from old filename
    cleaned_stem = re.sub(r'[-\s]+(leadeconomy|leadersfact(?:co)?|smartbizn|4thkr|4th|imnewsimbc|the-biz|thebiz|smartbiz|content|리드경제|리더스팩트|포쓰저널|아시아타임즈|파이낸셜포스트|스마트비)', '', Path(old_filename).stem, flags=re.I)
    cleaned_stem = re.sub(r'[①②③④⑤⑥⑦⑧⑨⑩]', '', cleaned_stem).strip(' -')
    candidate_name = f"{cleaned_stem}.html"
    if candidate_name in existing_posts:
        return fix_rel_path(source_file_path, candidate_name) + hash_part
        
    # 4. Try normalized signature match
    norm_old = re.sub(r'[^가-힣a-zA-Z0-9]', '', old_filename)
    if norm_old[:15] in lookup:
        matched = lookup[norm_old[:15]]
        return fix_rel_path(source_file_path, matched) + hash_part
        
    # 5. Fallback matching by keyword
    if "hbm" in old_filename or "반도체" in old_filename or "삼성전자" in old_filename or "sk하이닉스" in old_filename:
        return fix_rel_path(source_file_path, "ai-semiconductor-hbm-stocks.html") + hash_part
    elif "저평가" in old_filename or "가치주" in old_filename or "per" in old_filename:
        return fix_rel_path(source_file_path, "undervalued-stocks-2026.html") + hash_part
    elif "상승" in old_filename or "돌파" in old_filename:
        return fix_rel_path(source_file_path, "breakout-stocks-guide.html") + hash_part
    elif "배당" in old_filename or "절세" in old_filename or "isa" in old_filename:
        return fix_rel_path(source_file_path, "dividend-aristocrats-krx.html") + hash_part
    elif "공모주" in old_filename or "ipo" in old_filename:
        return fix_rel_path(source_file_path, "ipo-public-offering-guide.html") + hash_part
        
    # Default fallback to index.html
    return fix_rel_path(source_file_path, "index.html", to_root=True)

def fix_rel_path(source_path, target_filename, to_root=False):
    """Calculates proper relative path from source file to target file."""
    source_dir = source_path.parent
    if source_dir.name == "posts":
        if to_root:
            return f"../{target_filename}"
        else:
            return target_filename
    elif source_dir.name in ["pages", "tools", "admin"]:
        if to_root:
            return f"../{target_filename}"
        else:
            return f"../posts/{target_filename}"
    else:
        # root dir (index.html)
        if to_root:
            return target_filename
        else:
            return f"posts/{target_filename}"

def fix_all_files():
    print("=" * 60)
    print("FIXING ALL INTERNAL BROKEN LINKS")
    print("=" * 60)
    
    existing_posts, lookup = build_valid_posts_map()
    all_html = glob.glob(str(BASE_DIR / "**/*.html"), recursive=True)
    
    total_links_fixed = 0
    
    for file_path in all_html:
        path = Path(file_path)
        if path.name.startswith("google"):
            continue
            
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            
        # Find all hrefs
        def replace_href(match):
            nonlocal total_links_fixed
            prefix = match.group(1) # e.g. href="
            url = match.group(2)
            suffix = match.group(3) # e.g. "
            
            # Skip externals
            if (url.startswith("http://") or 
                url.startswith("https://") or 
                url.startswith("mailto:") or 
                url.startswith("tel:") or 
                url.startswith("#") or 
                url.startswith("javascript:")):
                return match.group(0)
                
            clean_u = url.split("#")[0].split("?")[0]
            if not clean_u:
                return match.group(0)
                
            target_check = (path.parent / clean_u).resolve()
            if target_check.exists():
                return match.group(0) # valid
                
            # If broken, resolve replacement
            fixed = resolve_target(url, path, existing_posts, lookup)
            if fixed and fixed != url:
                total_links_fixed += 1
                return f"{prefix}{fixed}{suffix}"
            return match.group(0)

        # Regex for href attributes
        new_content = re.sub(r'(href=["\'])([^"\']+)(["\'])', replace_href, content)
        
        # Also clean admin/index.html to have noindex
        if path.name == "index.html" and path.parent.name == "admin":
            if "noindex" not in new_content:
                new_content = new_content.replace("<head>", '<head>\n  <meta name="robots" content="noindex, nofollow">')
                
        if new_content != content:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_content)
                
    print(f"Successfully fixed {total_links_fixed} broken links across all HTML files!")

if __name__ == "__main__":
    fix_all_files()
