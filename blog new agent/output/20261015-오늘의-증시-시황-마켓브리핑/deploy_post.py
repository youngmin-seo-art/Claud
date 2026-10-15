import shutil
import json
import re
import subprocess
from pathlib import Path
from datetime import datetime

ROOT_DIR = Path(r"c:\Users\immnu\Desktop\Claud")
BLOG_DIR = ROOT_DIR / "adsense-stock-blog"
AGENT_OUTPUT = ROOT_DIR / "blog new agent" / "output" / "20261015-오늘의-증시-시황-마켓브리핑"

# 1. 대상 이미지 디렉토리 설정
TARGET_IMG_DIR = BLOG_DIR / "images" / "daily-market-20261015"
TARGET_IMG_DIR.mkdir(parents=True, exist_ok=True)

# 2. 이미지 복사
for img_name in ["thumbnail.png", "body-1.png", "body-2.png", "body-3.png"]:
    src_file = AGENT_OUTPUT / "images" / img_name
    dst_file = TARGET_IMG_DIR / img_name
    shutil.copy2(src_file, dst_file)
    print(f"[이미지 복사 완료] {src_file.name} -> {dst_file}")

# 3. HTML 포스트 생성 (상대 경로 치환 및 프로덕션 헤더/메타태그 설정)
post_filename = "20261015-오늘의-증시-시황-美-9월-cpi-안도-랠리-환율-급락-오늘-tsmc-실적-발표와-코스피-6200선-탈환-전략.html"
post_path = BLOG_DIR / "posts" / post_filename

with open(AGENT_OUTPUT / "final.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# 이미지 경로 치환 (./images/ -> ../images/daily-market-20261015/)
html_content = html_content.replace('src="./images/', 'src="../images/daily-market-20261015/')

# canonical 태그, adsense 스크립트, meta 태그 추가
canonical_url = f"https://www.valuestocklabs.com/posts/{post_filename}"
meta_tags = f'''  <meta name="description" content="미국 9월 CPI 안정과 국채금리 4% 하회, 원/달러 환율 1,330원대 하향 안정세(1,338.50원)로 글로벌 위험자산 투자 심리가 되살아났습니다! 오늘 오후 대만 TSMC 3분기 실적 발표를 앞두고 코스피 6,200선 탈환을 위한 3대 실전 대응 로드맵 총정리.">
  <meta name="keywords" content="오늘의시황, 코스피, 코스닥, 뉴욕증시, 나스닥, 미국CPI, TSMC실적, 환율하락, 반도체, HBM, valuestocklabs">
  <link rel="canonical" href="{canonical_url}">
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7807868644631223" crossorigin="anonymous"></script>
'''

if '<link rel="canonical"' not in html_content:
    html_content = html_content.replace('</head>', f'{meta_tags}</head>')

# 프로덕션 헤더로 교체 (미리보기 모드 배지 제거, 정식 헤더 링크로 변경)
preview_header_pattern = r'<header class="site-header">.*?<a href="#" class="brand-logo">ValueStock<span>Labs</span></a>\s*<span class="badge-preview">Preview Mode</span>.*?</div>\s*</header>'
prod_header = '''  <!-- 스크롤 진행 바 -->
  <div id="progress-container"><div id="progress-bar"></div></div>

  <!-- 헤더 -->
  <header class="site-header">
    <div class="header-inner">
      <a href="../index.html" class="brand-logo">ValueStock<span>Labs</span> <span class="tag">Market Daily</span></a>
      <span class="header-date">2026.10.15 브리핑</span>
    </div>
  </header>'''

html_content = re.sub(preview_header_pattern, prod_header, html_content, flags=re.DOTALL)

# 진행 바 CSS 추가
progress_css = '''
    /* 상단 진행률 바 */
    #progress-container {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 4px;
      background: transparent;
      z-index: 1000;
    }
    #progress-bar {
      height: 100%;
      width: 0%;
      background: linear-gradient(90deg, #10b981, #4f46e5);
      transition: width 0.1s;
    }
    .brand-logo span.tag {
      font-size: 11px;
      font-weight: 700;
      background: #ecfdf5;
      color: #065f46;
      padding: 3px 8px;
      border-radius: 9999px;
      text-transform: uppercase;
    }
    .header-date {
      font-size: 14px;
      font-weight: 600;
      color: var(--text-muted);
    }
'''
if '#progress-container' not in html_content:
    html_content = html_content.replace('</style>', f'{progress_css}\n  </style>')

# 진행 바 스크립트 추가
progress_js = '''
  <!-- 진행률 스크립트 -->
  <script>
    window.addEventListener('scroll', () => {
      const winScroll = document.documentElement.scrollTop || document.body.scrollTop;
      const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
      const scrolled = (winScroll / height) * 100;
      document.getElementById('progress-bar').style.width = scrolled + '%';
    });
  </script>
'''
if 'id="progress-bar"' in html_content and 'scrolled' not in html_content:
    html_content = html_content.replace('</body>', f'{progress_js}\n</body>')

# 푸터 문구 보정
html_content = html_content.replace(
    '<p>© 2026 valuestocklabs.com. All rights reserved.</p>',
    '<p>© 2026 valuestocklabs.com. All rights reserved. | 성공적인 투자를 위한 가치 분석 연구소</p>'
)

with open(post_path, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"[포스트 생성 완료] {post_path}")

# 4. 오늘의 시황 섹션 HTML 생성
briefing_section_html = f'''            <!-- Morning Market Briefing Section (오늘의 시황 세션) -->
    <section class="morning-briefing-wrap" id="morningBriefingSession" aria-label="오늘의 증시 시황">
      <div class="briefing-header">
        <div class="briefing-title-group">
          <h2 class="briefing-title">☕ 오늘의 증시 모닝 브리핑 &amp; 글로벌 핵심 경제 이슈</h2>
        </div>
        <span class="briefing-date" id="briefingDate">2026.10.15 07:15 업데이트</span>
      </div>

      <!-- Live Global Market Snapshot -->
      <div class="briefing-market-grid">
        <div class="market-chip" data-chip-id="kospi">
          <span class="market-chip-name">🇰🇷 코스피</span>
          <span class="market-chip-val ticker-up">6,128.90 ▲ +1.55%</span>
        </div>
        <div class="market-chip" data-chip-id="kosdaq">
          <span class="market-chip-name">🇰🇷 코스닥</span>
          <span class="market-chip-val ticker-up">838.20 ▲ +2.20%</span>
        </div>
        <div class="market-chip" data-chip-id="dji">
          <span class="market-chip-name">🇺🇸 다우존스</span>
          <span class="market-chip-val ticker-up">51,913.35 ▲ +0.47%</span>
        </div>
        <div class="market-chip" data-chip-id="sp500">
          <span class="market-chip-name">🇺🇸 S&amp;P 500</span>
          <span class="market-chip-val ticker-up">7,860.90 ▲ +0.71%</span>
        </div>
        <div class="market-chip" data-chip-id="nasdaq">
          <span class="market-chip-name">🇺🇸 나스닥 100</span>
          <span class="market-chip-val ticker-up">27,470.80 ▲ +0.98%</span>
        </div>
        <div class="market-chip" data-chip-id="sox">
          <span class="market-chip-name">🇺🇸 필라델피아 반도체</span>
          <span class="market-chip-val ticker-up">12,273.15 ▲ +1.85%</span>
        </div>
        <div class="market-chip" data-chip-id="usdkrw">
          <span class="market-chip-name">🇰🇷 원/달러 환율</span>
          <span class="market-chip-val ticker-down">1,338.50 ▼ -0.42%</span>
        </div>
      </div>

      <div class="briefing-content-summary">
        미국 9월 CPI 안정과 국채금리 4% 하회, 원/달러 환율 1,330원대 하향 안정세(1,338.50원)로 글로벌 위험자산 투자 심리가 되살아났습니다! 오늘 오후 대만 TSMC의 3분기 실적 발표를 앞두고 코스피 6,200선 탈환을 위한 3대 실전 대응 로드맵을 총정리합니다.
      </div>

      <ul class="briefing-points">
        <li>📌 <strong>국내증시 수급:</strong> 코스피 6,128.90(+1.55%) 6,100선 안착 성공, 외국인 코스피200 선물 1조 2,400억 원 순매수 전환.</li>
        <li>📌 <strong>뉴욕증시 &amp; 환율:</strong> 美 9월 CPI 2.3% 부합으로 3대 지수 랠리, 10년물 국채금리 3.98% 하회 및 NDF 환율 1,338.50원 안정.</li>
        <li>📌 <strong>오늘의 시장 전략:</strong> 시초가 갭상승 추격 매수 자제 속 6,160선 지지 확인 분할 매수, 오후 TSMC 실적 확인 후 HBM·가치주 5:5 바벨 전략.</li>
      </ul>

      <div style="display: flex; gap: 12px; align-items: center; flex-wrap: wrap;">
        <a href="posts/{post_filename}" class="briefing-btn" id="latestBriefingLink">
          📰 오늘의 시황 분석 리포트 전문 읽기 →
        </a>
        <span style="font-size: 0.8rem; color: var(--text-muted);">매일 아침 최신 경제 데이터로 자동 갱신됩니다.</span>
      </div>
    </section>'''

# 5. index.html, sitemap.xml, rss.xml, published_history.json 동기화
from sys import path
path.insert(0, str(ROOT_DIR / "stock-blog-agent"))
from blog_publisher import BlogPublisher

article_data = {
    "title": "오늘의 증시 시황: 美 9월 CPI 안도 랠리와 환율 안정, TSMC 실적 발표와 코스피 6,200선 탈환 전략",
    "filename": post_filename,
    "date": "2026-10-15",
    "category": "market",
    "image": "images/daily-market-20261015/thumbnail.png",
    "summary": "미국 9월 CPI 안정과 국채금리 4% 하회, 원/달러 환율 1,330원대 하향 안정세(1,338.50원)로 글로벌 위험자산 투자 심리가 되살아났습니다! 오늘 오후 대만 TSMC의 3분기 실적 발표를 앞두고 코스피 6,200선 탈환을 위한 3대 실전 대응 로드맵 총정리.",
    "is_morning": True,
    "briefing_section_html": briefing_section_html
}

publisher = BlogPublisher()
# sitemap 업데이트
publisher.update_sitemap(post_filename, "2026-10-15")
# rss 업데이트
publisher.update_rss(article_data)
# index.html 업데이트
publisher.update_index_html(article_data)
# 발행 이력 기록
publisher.record_published_history(article_data)

# 6. SEO 및 사이트맵 재구축
try:
    import fix_all_internal_links
    import fix_all_seo_and_sitemap
    fix_all_internal_links.fix_all_files()
    fix_all_seo_and_sitemap.rebuild_all()
    print("[성공] SEO 및 사이트맵 재구축 완료")
except Exception as e:
    print(f"[알림] 사후 동기화: {e}")

print("🎉 [배포 준비 완료] 블로그 포스트 및 인덱스 동기화 완료!")
