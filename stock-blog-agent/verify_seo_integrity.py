"""
=============================================================================
SEO INTEGRITY VERIFIER (verify_seo_integrity.py)
전체 사이트 HTML 표준 태그, 로봇 태그, 사이트맵 무결성 전수 검증
=============================================================================
"""

import os
import sys
import re
import xml.etree.ElementTree as ET
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent.parent / "adsense-stock-blog"
SITEMAP_XML = BASE_DIR / "sitemap.xml"
RSS_XML = BASE_DIR / "rss.xml"
VERCEL_JSON = BASE_DIR / "vercel.json"

def verify_all():
    print("=" * 60)
    print("[검증 시작] 검색엔진 색인 및 SEO 무결성 전수 검증")
    print("=" * 60)

    errors = []
    checked_count = 0

    # 1. Check all HTML files
    for root, _, files in os.walk(BASE_DIR):
        for f in files:
            if f.endswith(".html") and not f.startswith("google"):
                filepath = Path(root) / f
                rel_path = filepath.relative_to(BASE_DIR).as_posix()
                
                with open(filepath, "r", encoding="utf-8") as file:
                    content = file.read()

                # Admin page check
                if "admin" in rel_path:
                    if 'noindex' not in content:
                        errors.append(f"Admin page {rel_path} must have noindex")
                    continue

                checked_count += 1

                # Check canonical
                if '<link rel="canonical"' not in content:
                    errors.append(f"Missing canonical in {rel_path}")

                # Check robots
                if '<meta name="robots"' not in content:
                    errors.append(f"Missing robots meta in {rel_path}")

                # Check JSON-LD
                if '<script type="application/ld+json">' not in content:
                    errors.append(f"Missing JSON-LD in {rel_path}")

                # Check relative og:image
                if 'property="og:image" content="../' in content:
                    errors.append(f"Relative og:image found in {rel_path}")

    print(f"[*] 총 {checked_count}개 공개 대상 HTML 문서 검사 완료")

    # 2. Check sitemap.xml
    if not SITEMAP_XML.exists():
        errors.append("sitemap.xml does not exist")
    else:
        try:
            tree = ET.parse(SITEMAP_XML)
            root = tree.getroot()
            sitemap_urls = [elem.text.strip() for elem in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
            print(f"[*] sitemap.xml 내 등록된 URL: {len(sitemap_urls)}개")
            if len(sitemap_urls) != checked_count:
                errors.append(f"Sitemap URL count ({len(sitemap_urls)}) != HTML files count ({checked_count})")
        except Exception as e:
            errors.append(f"Sitemap XML parsing error: {e}")

    # 3. Check rss.xml
    if not RSS_XML.exists():
        errors.append("rss.xml does not exist")
    else:
        try:
            tree = ET.parse(RSS_XML)
            print("[*] rss.xml 구문 유효성 검사 통과")
        except Exception as e:
            errors.append(f"RSS XML parsing error: {e}")

    # 4. Check vercel.json cleanUrls
    if VERCEL_JSON.exists():
        with open(VERCEL_JSON, "r", encoding="utf-8") as f:
            v_text = f.read()
        if '"cleanUrls": true' in v_text:
            errors.append("vercel.json still has cleanUrls: true (risk of 308 redirect loop on .html pages)")

    print("=" * 60)
    if not errors:
        print(f"✅ [검증 성공] 모든 {checked_count}개 페이지 및 사이트맵/RSS/배포 설정 오류 0건! 완벽 상태입니다.")
        return True
    else:
        print(f"❌ [검증 실패] {len(errors)}건의 결함 발견:")
        for err in errors:
            print(f"  - {err}")
        return False

if __name__ == "__main__":
    success = verify_all()
    sys.exit(0 if success else 1)
