import os
import glob

posts = glob.glob('adsense-stock-blog/posts/*.html')
pages = glob.glob('adsense-stock-blog/pages/*.html')
tools = glob.glob('adsense-stock-blog/tools/*.html')

script_tag = '<script src="../js/admin-analytics.js" defer></script>\n</body>'

for fpath in posts + pages + tools:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'admin-analytics.js' not in content and '</body>' in content:
        new_content = content.replace('</body>', script_tag)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Injected admin-analytics into: {fpath}")

print("All HTML files updated successfully!")
