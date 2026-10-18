import shutil
import json
import re
import sys
from pathlib import Path
from datetime import datetime

ROOT_DIR = Path(r"c:\Users\immnu\Desktop\Claud")
BLOG_DIR = ROOT_DIR / "adsense-stock-blog"
AGENT_OUTPUT = ROOT_DIR / "blog new agent" / "output" / "한미반도체-AI반도체-기업분석"

# 1. 대상 이미지 디렉토리 설정 및 복사
TARGET_IMG_DIR = BLOG_DIR / "images" / "hanmi-semiconductor"
TARGET_IMG_DIR.mkdir(parents=True, exist_ok=True)

for img_name in ["thumbnail.png", "body-1.png", "body-2.png", "body-3.png", "body-4.png"]:
    src_file = AGENT_OUTPUT / "images" / img_name
    dst_file = TARGET_IMG_DIR / img_name
    shutil.copy2(src_file, dst_file)
    print(f"[이미지 복사 완료] {src_file.name} -> {dst_file}")

# 2. HTML 원본 로드 및 프로덕션 블로그 포스트 형식으로 변환
post_filename = "20261018-한미반도체-주가-전망-및-2026-실적-분석-hbm4-tc본더-1위의-독점력과-괴물-마진.html"
post_path = BLOG_DIR / "posts" / post_filename

with open(AGENT_OUTPUT / "final.html", "r", encoding="utf-8") as f:
    source_html = f.read()

# 이미지 상대 경로 변환
html = source_html.replace("./images/", "../images/hanmi-semiconductor/")

# 브랜드 로고 및 뱃지 변환
html = html.replace(
    '<a href="https://valuestocklabs.com" class="brand-logo" target="_blank">\n        valuestock<span>labs</span>\n      </a>',
    '<a href="../index.html" class="brand-logo">ValueStock<span>Labs</span></a>'
)
html = html.replace('● 미리보기 검수 모드', '리서치 리포트')

# 종목가치 분석 섹터 뱃지
html = html.replace(
    '<span class="post-category">AI반도체</span>',
    '<span class="post-category">종목가치 분석 &amp; 기업분석 (KOSPI 042700)</span>'
)

# 메타 태그 및 SEO 주입
post_url = f"https://www.valuestocklabs.com/posts/{post_filename}"
meta_seo_block = f"""  <meta name="description" content="글로벌 HBM TC 본더 점유율 71.2%의 절대강자 한미반도체(042700). 2026년 2분기 영업이익률 51.9%를 달성하며 입증한 괴물 같은 마진 체력과 차세대 HBM4 수주 모멘텀, 그리고 듀얼벤더 우려를 정밀 해부합니다.">
  <meta name="keywords" content="한미반도체, 한미반도체 주가, 042700, HBM, HBM4, TC본더, TC 본더 4.5 그리핀, 곽동신, SK하이닉스, 마이크론, 엔비디아, 테라팹, 종목가치분석, 기업분석, 반도체소부장, valuestocklabs">
  <meta name="author" content="ValueStockLabs 리서치팀">
  <link rel="icon" type="image/x-icon" href="../favicon.ico">
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7807868644631223" crossorigin="anonymous"></script>

  <!-- Canonical & Search Engine Indexing -->
  <link rel="canonical" href="{post_url}">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">

  <!-- OpenGraph / SNS Meta -->
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="Value Stock Labs">
  <meta property="og:title" content="한미반도체 주가 전망 및 2026 실적 분석: HBM4 TC본더 1위의 독점력과 괴물 마진 | valuestocklabs">
  <meta property="og:description" content="글로벌 HBM TC 본더 점유율 71.2%의 절대강자 한미반도체(042700). 2026년 2분기 영업이익률 51.9%를 달성하며 입증한 괴물 같은 마진 체력과 차세대 HBM4 수주 모멘텀, 그리고 듀얼벤더 우려를 정밀 해부합니다.">
  <meta property="og:image" content="https://www.valuestocklabs.com/images/hanmi-semiconductor/thumbnail.png">
  <meta property="og:url" content="{post_url}">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="한미반도체 주가 전망 및 2026 실적 분석: HBM4 TC본더 1위의 독점력과 괴물 마진 | valuestocklabs">
  <meta name="twitter:description" content="글로벌 HBM TC 본더 점유율 71.2%의 절대강자 한미반도체(042700). 2026년 2분기 영업이익률 51.9%를 달성하며 입증한 괴물 같은 마진 체력과 차세대 HBM4 수주 모멘텀, 그리고 듀얼벤더 우려를 정밀 해부합니다.">
  <meta name="twitter:image" content="https://www.valuestocklabs.com/images/hanmi-semiconductor/thumbnail.png">

  <!-- Schema.org JSON-LD Structured Data -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BlogPosting",
    "headline": "한미반도체 주가 전망 및 2026 실적 분석: HBM4 TC본더 1위의 독점력과 괴물 마진",
    "description": "글로벌 HBM TC 본더 점유율 71.2%의 절대강자 한미반도체(042700). 2026년 2분기 영업이익률 51.9%를 달성하며 입증한 괴물 같은 마진 체력과 차세대 HBM4 수주 모멘텀, 그리고 듀얼벤더 우려를 정밀 해부합니다.",
    "image": [
      "https://www.valuestocklabs.com/images/hanmi-semiconductor/thumbnail.png"
    ],
    "datePublished": "2026-10-18T08:30:00+09:00",
    "dateModified": "2026-10-18T08:30:00+09:00",
    "author": {{
      "@type": "Organization",
      "name": "Value Stock Labs 리서치팀",
      "url": "https://www.valuestocklabs.com/pages/about.html"
    }},
    "publisher": {{
      "@type": "Organization",
      "name": "Value Stock Labs",
      "logo": {{
        "@type": "ImageObject",
        "url": "https://www.valuestocklabs.com/images/vsl-logo-neon-fire.png"
      }}
    }},
    "mainEntityOfPage": {{
      "@type": "WebPage",
      "@id": "{post_url}"
    }}
  }}
  </script>
"""

# title 태그 아래에 SEO 블록 주입
html = html.replace(
    '<title>한미반도체 주가 전망 및 2026 실적 분석: HBM4 TC본더 1위의 독점력과 괴물 마진 | valuestocklabs</title>',
    f'<title>한미반도체 주가 전망 및 2026 실적 분석: HBM4 TC본더 1위의 독점력과 괴물 마진 | valuestocklabs</title>\n{meta_seo_block}'
)

with open(post_path, "w", encoding="utf-8") as f:
    f.write(html)
print(f"[포스트 생성 완료] {post_path}")

# 3. index.html 업데이트 (종목가치 분석 섹터 카드 삽입)
INDEX_HTML = BLOG_DIR / "index.html"
with open(INDEX_HTML, "r", encoding="utf-8") as f:
    index_content = f.read()

card_html = f"""          <!-- Auto-Generated Article: Hanmi Semiconductor (042700) -->
          <article class="post-card" data-category="valuation">
            <div class="post-thumb-wrap">
              <span class="post-badge valuation" style="background: linear-gradient(135deg, #4f46e5, #3b82f6); color:#fff; font-weight:700;">📊 종목가치 분석 PICK</span>
              <img src="images/hanmi-semiconductor/thumbnail.png" class="post-thumb" alt="한미반도체 주가 전망 및 2026 실적 분석: HBM4 TC본더 1위의 독점력과 괴물 마진 (042700)" loading="lazy">
            </div>
            <div class="post-body">
              <div class="post-meta">
                <span>📅 2026-10-18</span>
                <span style="color: #38bdf8; font-weight: bold;">⭐ 심층 기업분석</span>
              </div>
              <h3 class="post-title">
                <a href="posts/{post_filename}">한미반도체 주가 전망 및 2026 실적 분석: HBM4 TC본더 1위의 독점력과 괴물 마진 (042700)</a>
              </h3>
              <p class="post-excerpt">
                글로벌 HBM TC 본더 시장점유율 71.2%의 절대강자 한미반도체(042700). 2026년 2분기 영업이익률 51.9%를 달성하며 입증한 괴물 같은 마진 체력과 차세대 HBM4 수주 모멘텀, 그리고 듀얼벤더 우려를 정밀 해부합니다.
              </p>
              <div class="post-footer">
                <div class="author-chip">
                  <div class="author-avatar" style="background: #4f46e5;">H</div>
                  <span>가치투자분석팀</span>
                </div>
                <a href="posts/{post_filename}" class="read-more-link">리포트 읽기 →</a>
              </div>
            </div>
          </article>
"""

# postsGrid 바로 아래 첫 번째 카드로 삽입
target_grid_marker = '<div class="posts-grid" id="postsGrid">'
if target_grid_marker in index_content and post_filename not in index_content:
    index_content = index_content.replace(target_grid_marker, target_grid_marker + "\n" + card_html, 1)
    with open(INDEX_HTML, "w", encoding="utf-8") as f:
        f.write(index_content)
    print("[성공] index.html 종목가치 분석 섹터 카드 등록 완료")

# 4. published_history.json 기록
HISTORY_FILE = ROOT_DIR / "stock-blog-agent" / "published_history.json"
try:
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        history = json.load(f)
except Exception:
    history = []

history_entry = {
    "title": "한미반도체 주가 전망 및 2026 실적 분석: HBM4 TC본더 1위의 독점력과 괴물 마진 (042700)",
    "filename": post_filename,
    "date": "2026-10-18",
    "category": "valuation",
    "published_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

if not any(item.get("filename") == post_filename for item in history if isinstance(item, dict)):
    history.append(history_entry)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
    print("[성공] published_history.json 등록 완료")

# 5. 내부 링크 및 사이트맵, RSS 자동 동기화
sys.path.insert(0, str(ROOT_DIR / "stock-blog-agent"))
try:
    import fix_all_internal_links
    import fix_all_seo_and_sitemap
    fix_all_internal_links.fix_all_files()
    fix_all_seo_and_sitemap.rebuild_all()
    print("[성공] 내부 링크, sitemap.xml, rss.xml 자동 동기화 완료")
except Exception as e:
    print(f"[알림] 동기화 스크립트 실행 오류: {e}")

print("🎉 한미반도체(042700) 블로그 배포 완료!")
