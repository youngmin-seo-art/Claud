import os
import re
import xml.etree.ElementTree as ET

base_dir = r"c:\Users\immnu\Desktop\Claud\adsense-stock-blog"

# 1. XML validation
try:
    ET.parse(os.path.join(base_dir, 'sitemap.xml'))
    ET.parse(os.path.join(base_dir, 'rss.xml'))
    print("SUCCESS: sitemap.xml and rss.xml parsed successfully.")
except Exception as e:
    print(f"ERROR: XML parsing failed: {e}")

# 2. Check sitemap links exist
with open(os.path.join(base_dir, 'sitemap.xml'), 'r', encoding='utf-8') as f:
    sitemap_text = f.read()

urls = re.findall(r'<loc>https://valuestocklabs\.com/(.*?)</loc>', sitemap_text)
missing_sitemap = []
for u in urls:
    if u == '':
        target = os.path.join(base_dir, 'index.html')
    else:
        target = os.path.join(base_dir, u.replace('/', os.sep))
    if not os.path.exists(target):
        missing_sitemap.append((u, target))

if missing_sitemap:
    print(f"ERROR: Missing in sitemap: {missing_sitemap}")
else:
    print(f"SUCCESS: All {len(urls)} sitemap URLs exist on disk.")

# 3. Check index.html links exist
with open(os.path.join(base_dir, 'index.html'), 'r', encoding='utf-8') as f:
    index_text = f.read()

index_post_links = set(re.findall(r'href="(posts/[^"]+)"', index_text))
missing_index = []
for link in index_post_links:
    target = os.path.join(base_dir, link.replace('/', os.sep))
    if not os.path.exists(target):
        missing_index.append((link, target))

if missing_index:
    print(f"ERROR: Missing in index.html: {missing_index}")
else:
    print(f"SUCCESS: All {len(index_post_links)} index.html post links exist on disk.")
