import os
import glob
import re

BASE_DIR = r"c:\Users\immnu\Desktop\Claud\adsense-stock-blog"
LATEST_BRIEFING_POST = "20260918-morning-market-briefing.html"

def update_index():
    path = os.path.join(BASE_DIR, "index.html")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Replace nav link in index.html
    new_content = re.sub(
        r'<a href="[^"]*morningBriefingSession[^"]*" class="nav-link">오늘의 시황</a>',
        f'<a href="posts/{LATEST_BRIEFING_POST}" class="nav-link">오늘의 시황</a>',
        content
    )
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Updated index.html")

def update_posts():
    post_files = glob.glob(os.path.join(BASE_DIR, "posts", "*.html"))
    for pf in post_files:
        with open(pf, "r", encoding="utf-8") as f:
            content = f.read()
        
        new_content = re.sub(
            r'<a href="[^"]*morningBriefingSession[^"]*" class="nav-link">오늘의 시황</a>',
            f'<a href="{LATEST_BRIEFING_POST}" class="nav-link">오늘의 시황</a>',
            content
        )
        if new_content != content:
            with open(pf, "w", encoding="utf-8") as f:
                f.write(new_content)
    print(f"Updated {len(post_files)} post files")

def update_tools_and_pages():
    for subdir in ["tools", "pages"]:
        files = glob.glob(os.path.join(BASE_DIR, subdir, "*.html"))
        for fpath in files:
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()
            
            new_content = re.sub(
                r'<a href="[^"]*morningBriefingSession[^"]*" class="nav-link">오늘의 시황</a>',
                f'<a href="../posts/{LATEST_BRIEFING_POST}" class="nav-link">오늘의 시황</a>',
                content
            )
            if new_content != content:
                with open(fpath, "w", encoding="utf-8") as f:
                    f.write(new_content)
            print(f"Updated {fpath}")

if __name__ == "__main__":
    update_index()
    update_posts()
    update_tools_and_pages()
