import os
import re
from pathlib import Path
from urllib.parse import urlparse

WORKSPACE = Path(r"c:\Users\immnu\Desktop\Claud\adsense-stock-blog")

all_html_files = list(WORKSPACE.rglob("*.html"))
print(f"Total HTML files found: {len(all_html_files)}")

broken_images = []
broken_links = []
missing_meta = []
missing_adsense = []

for html_path in all_html_files:
    rel_file = html_path.relative_to(WORKSPACE)
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {rel_file}: {e}")
        continue

    # 1. Check Images
    img_matches = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', content, re.IGNORECASE)
    for src in img_matches:
        if src.startswith("http") or src.startswith("data:"):
            continue
        # resolve relative to current html file
        img_target = (html_path.parent / src).resolve()
        if not img_target.exists():
            broken_images.append((str(rel_file), src, str(img_target)))

    # 2. Check Internal Links (a href)
    a_matches = re.findall(r'<a[^>]+href=["\']([^"\']+)["\']', content, re.IGNORECASE)
    for href in a_matches:
        if href.startswith("http") or href.startswith("mailto:") or href.startswith("tel:") or href.startswith("#") or href.startswith("javascript:"):
            continue
        clean_href = href.split("#")[0].split("?")[0]
        if not clean_href:
            continue
        link_target = (html_path.parent / clean_href).resolve()
        if not link_target.exists():
            broken_links.append((str(rel_file), href, str(link_target)))

    # 3. Check SEO & AdSense
    if "<title>" not in content:
        missing_meta.append((str(rel_file), "Missing <title>"))
    if "description" not in content and "pages" not in str(rel_file):
        missing_meta.append((str(rel_file), "Missing meta description"))
    if "adsbygoogle.js" not in content and "googleTG" not in str(rel_file) and "googlea4" not in str(rel_file):
        missing_adsense.append(str(rel_file))

print(f"\n--- AUDIT RESULTS ---")
print(f"Broken Images: {len(broken_images)}")
for item in broken_images[:10]:
    print(f"  [IMG 404] File: {item[0]} -> src: '{item[1]}'")

print(f"\nBroken Links: {len(broken_links)}")
for item in broken_links[:15]:
    print(f"  [LINK 404] File: {item[0]} -> href: '{item[1]}'")

print(f"\nMissing Meta: {len(missing_meta)}")
for item in missing_meta[:10]:
    print(f"  [META] {item[0]}: {item[1]}")

print(f"\nMissing AdSense Script: {len(missing_adsense)}")
for item in missing_adsense[:10]:
    print(f"  [ADSENSE] {item}")
