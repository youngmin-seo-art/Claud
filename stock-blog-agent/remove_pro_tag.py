import os
import glob
import re

def remove_pro_from_files():
    base_dir = r"c:\Users\immnu\Desktop\Claud\adsense-stock-blog"
    html_files = glob.glob(os.path.join(base_dir, "**", "*.html"), recursive=True)
    
    pattern = re.compile(r'\s*<span class="logo-tag">\s*PRO\s*</span>', re.IGNORECASE)
    
    modified_count = 0
    for fpath in html_files:
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        
        if '<span class="logo-tag">PRO</span>' in content or '<span class="logo-tag">PRO</span>' in content.upper():
            new_content = pattern.sub('', content)
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(new_content)
            modified_count += 1
            print(f"Updated HTML: {fpath}")

    # Also update stock-blog-agent/article_generator.py
    gen_path = r"c:\Users\immnu\Desktop\Claud\stock-blog-agent\article_generator.py"
    if os.path.exists(gen_path):
        with open(gen_path, "r", encoding="utf-8") as f:
            gen_content = f.read()
        if '<span class="logo-tag">PRO</span>' in gen_content:
            gen_new = pattern.sub('', gen_content)
            with open(gen_path, "w", encoding="utf-8") as f:
                f.write(gen_new)
            print(f"Updated Generator: {gen_path}")
            
    print(f"Total files updated: {modified_count}")

if __name__ == "__main__":
    remove_pro_from_files()
