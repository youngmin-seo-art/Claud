import shutil
import json
import re
from pathlib import Path
from datetime import datetime

ROOT_DIR = Path(r"c:\Users\immnu\Desktop\Claud")
BLOG_DIR = ROOT_DIR / "adsense-stock-blog"
AGENT_OUTPUT = ROOT_DIR / "blog new agent" / "output" / "20261013-오늘의-증시-시황-마켓브리핑"

# 1. 대상 디렉토리 설정
TARGET_IMG_DIR = BLOG_DIR / "images" / "daily-market-20261013"
TARGET_IMG_DIR.mkdir(parents=True, exist_ok=True)

# 2. 이미지 복사
for img_name in ["thumbnail.png", "body-1.png", "body-2.png", "body-3.png"]:
    src_file = AGENT_OUTPUT / "images" / img_name
    dst_file = TARGET_IMG_DIR / img_name
    shutil.copy2(src_file, dst_file)
    print(f"[이미지 복사 완료] {src_file.name} -> {dst_file}")

# 3. HTML 포스트 생성 (상대 경로 치환)
post_filename = "20261013-오늘의-증시-시황-코스피-6380선-지지력-테스트와-뉴욕증시-혼조-9월-cpi-tsmc-어닝시즌-투자-전략.html"
post_path = BLOG_DIR / "posts" / post_filename

with open(AGENT_OUTPUT / "final.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# 이미지 경로 치환 (./images/ -> ../images/daily-market-20261013/)
html_content = html_content.replace('src="./images/', 'src="../images/daily-market-20261013/')

# canonical 태그 및 adsense 스크립트 추가
canonical_url = f"https://www.valuestocklabs.com/posts/{post_filename}"
if '<link rel="canonical"' not in html_content:
    html_content = html_content.replace(
        '</head>',
        f'  <link rel="canonical" href="{canonical_url}">\n  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7807868644631223" crossorigin="anonymous"></script>\n</head>'
    )

with open(post_path, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"[포스트 생성 완료] {post_path}")

# 4. index.html, sitemap.xml, rss.xml, published_history.json 동기화
from sys import path
path.insert(0, str(ROOT_DIR / "stock-blog-agent"))
from blog_publisher import BlogPublisher

article_data = {
    "title": "오늘의 증시 시황: 코스피 6,380선 지지력 테스트와 뉴욕증시 혼조, 9월 CPI·TSMC 슈퍼위크 투자 전략",
    "filename": post_filename,
    "date": "2026-10-13",
    "category": "market",
    "image": "images/daily-market-20261013/thumbnail.png",
    "summary": "코스피 6,380선 급락과 외국인 2.1조 원 매도 충격, 뉴욕증시 다우 반등과 반도체 셀온(Sell-on) 분석, 14일 9월 CPI 및 15일 TSMC 3분기 실적 대비 투자 로드맵 총정리.",
    "is_morning": True,
}

publisher = BlogPublisher()
# sitemap 업데이트
publisher.update_sitemap(post_filename, "2026-10-13")
# rss 업데이트
publisher.update_rss(article_data)
# index.html 업데이트
publisher.update_index_html(article_data)
# 발행 이력 기록
publisher.record_published_history(article_data)

print("🎉 [배포 준비 완료] 블로그 포스트 및 인덱스 동기화 완료!")
