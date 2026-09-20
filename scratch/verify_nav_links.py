import glob
import os
import re

BASE_DIR = r"c:\Users\immnu\Desktop\Claud\adsense-stock-blog"

expected_items = [
    "홈", "오늘의 시황", "저평가주식", "상승초입주", "AI반도체", "공모주",
    "적정가치 계산기", "평단가 계산기", "손익비 계산기", "소개"
]

all_html = glob.glob(os.path.join(BASE_DIR, "**", "*.html"), recursive=True)
issues = []

for fpath in all_html:
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Extract nav
    nav_match = re.search(r'<nav class="main-nav[^>]*>(.*?)</nav>', content, re.DOTALL)
    if not nav_match:
        issues.append((fpath, "NO_NAV"))
        continue
    
    nav_text = nav_match.group(1)
    missing = []
    for item in expected_items:
        if item not in nav_text:
            missing.append(item)
    
    if missing:
        issues.append((fpath, f"MISSING: {missing}"))

print(f"Total HTML files checked: {len(all_html)}")
if not issues:
    print("ALL HTML files have complete navigation menus!")
else:
    print(f"Found {len(issues)} issues:")
    for path, err in issues:
        print(f"  {path}: {err}")
