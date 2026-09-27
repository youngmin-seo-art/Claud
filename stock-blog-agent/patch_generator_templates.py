"""
=============================================================================
PATCH ARTICLE GENERATOR & BLOG PUBLISHER TEMPLATES
=============================================================================
Ensures all future generated articles strictly adhere to Google AdSense
program policies, compliant ad slots, compliant labels, and robust E-E-A-T.
"""

import os
import sys
import re
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent

def patch_article_generator():
    ag_path = BASE_DIR / "article_generator.py"
    with open(ag_path, "r", encoding="utf-8") as f:
        code = f.read()

    # 1. Replace SPONSORED with ADVERTISEMENT
    code = code.replace('<span class="ad-label">SPONSORED</span>', '<span class="ad-label">ADVERTISEMENT</span>')
    code = code.replace('<span class="ad-label">스폰서</span>', '<span class="ad-label">ADVERTISEMENT</span>')

    # 2. Replace footer title & text
    code = code.replace('<h4 class="footer-col-title">애드센스 필수 정책</h4>', '<h4 class="footer-col-title">사이트 정책 및 법적 고지</h4>')
    code = code.replace('<h4 class="footer-col-title">애드센스 정책</h4>', '<h4 class="footer-col-title">사이트 정책 및 법적 고지</h4>')
    code = code.replace('<span>Google AdSense Compliant &amp; SEO Optimized</span>', '<span>공인 데이터 기반 독립 금융 리서치 포털</span>')
    code = code.replace('<span>Google AdSense Compliant & SEO Optimized</span>', '<span>공인 데이터 기반 독립 금융 리서치 포털</span>')

    # 3. Clean dummy slot numbers
    code = re.sub(r'data-ad-slot="[0-9]{4,7}"', 'data-ad-slot=""', code)

    # 4. Remove mobile sticky anchor ad overlay
    code = re.sub(r'<!-- Mobile Sticky Anchor Ad -->[\s\S]*?</div>\s*</div>\s*</div>', '', code)
    code = re.sub(r'<div class="mobile-anchor-ad"[\s\S]*?</div>\s*</div>', '', code)

    with open(ag_path, "w", encoding="utf-8") as f:
        f.write(code)
    print("✅ article_generator.py patched successfully!")

def patch_blog_publisher():
    bp_path = BASE_DIR / "blog_publisher.py"
    with open(bp_path, "r", encoding="utf-8") as f:
        code = f.read()

    # Make publish_post run fix_all_internal_links & fix_all_seo_and_sitemap automatically
    if "import fix_all_internal_links" not in code:
        patch_logic = """
        # 4.5. 애드센스 정책 준수를 위한 내부 링크 및 전체 SEO/사이트맵 자동 동기화
        try:
            import fix_all_internal_links
            import fix_all_seo_and_sitemap
            fix_all_internal_links.fix_all_files()
            fix_all_seo_and_sitemap.rebuild_all()
        except Exception as e:
            print(f"[알림] 사후 링크/사이트맵 동기화: {e}")
"""
        # Insert before git_push
        if "if auto_push:" in code:
            code = code.replace("if auto_push:", f"{patch_logic}\n        if auto_push:")

    with open(bp_path, "w", encoding="utf-8") as f:
        f.write(code)
    print("✅ blog_publisher.py patched successfully!")

if __name__ == "__main__":
    patch_article_generator()
    patch_blog_publisher()
