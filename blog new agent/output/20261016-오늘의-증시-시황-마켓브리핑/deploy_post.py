import shutil
import json
import re
import subprocess
from pathlib import Path
from datetime import datetime

ROOT_DIR = Path(r"c:\Users\immnu\Desktop\Claud")
BLOG_DIR = ROOT_DIR / "adsense-stock-blog"
AGENT_OUTPUT = ROOT_DIR / "blog new agent" / "output" / "20261016-오늘의-증시-시황-마켓브리핑"

# 1. 대상 이미지 디렉토리 설정
TARGET_IMG_DIR = BLOG_DIR / "images" / "daily-market-20261016"
TARGET_IMG_DIR.mkdir(parents=True, exist_ok=True)

# 2. 이미지 복사
for img_name in ["thumbnail.png", "body-1.png", "body-2.png", "body-3.png"]:
    src_file = AGENT_OUTPUT / "images" / img_name
    dst_file = TARGET_IMG_DIR / img_name
    shutil.copy2(src_file, dst_file)
    print(f"[이미지 복사 완료] {src_file.name} -> {dst_file}")

# 3. HTML 포스트 생성
post_filename = "20261016-오늘의-증시-시황-15일-서킷브레이커-쇼크-후-코스피-5700선-기술적-반등-환율-1340원대와-pbr-1-0배-지지선-점검.html"
post_path = BLOG_DIR / "posts" / post_filename

# 이전 오정보 파일들 정리
old_posts_to_delete = [
    "20261016-오늘의-증시-시황-tsmc-어닝-서프라이즈-미-신고가-랠리-코스피-6200선-돌파와-금요일-실전-전략.html",
    "20261016-오늘의-증시-시황-코스피-5700선-추락과-14-15일-연쇄-폭락-쇼크-바닥-진단과-금요일-비상-대응-전략.html"
]
for old_name in old_posts_to_delete:
    old_file = BLOG_DIR / "posts" / old_name
    if old_file.exists():
        try:
            old_file.unlink()
            print(f"[기존 오정보 파일 삭제 완료] {old_name}")
        except Exception as e:
            print(f"[경고] 기존 파일 삭제 실패: {e}")

with open(AGENT_OUTPUT / "final.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# 이미지 경로 치환 (./images/ -> ../images/daily-market-20261016/)
html_content = html_content.replace('src="./images/', 'src="../images/daily-market-20261016/')

# canonical 태그, adsense 스크립트, meta 태그 추가
canonical_url = f"https://www.valuestocklabs.com/posts/{post_filename}"
meta_tags = f'''  <meta name="description" content="10월 15일 코스피 -7.57% 서킷브레이커 폭락 쇼크 후 16일 5,700선(+3.0%) 기술적 반등 전개. 원/달러 환율 1,340원대 안정 속 코스피 12M Fwd PBR 1.08배 도달과 PBR 1.0배(5,000선) 지지선 분석, 실전 비상 대응 3대 수칙 총정리.">
  <meta name="keywords" content="오늘의시황, 코스피5700선, 서킷브레이커, 검은목요일, 기술적반등, 환율1340원대, 코스피PBR, 삼성전자, SK하이닉스, 밸류에이션, 실전대응전략, valuestocklabs">
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
      <span class="header-date">2026.10.16 긴급 브리핑</span>
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
      background: linear-gradient(90deg, #4f46e5, #06b6d4);
      transition: width 0.1s;
    }
    .brand-logo span.tag {
      font-size: 11px;
      font-weight: 700;
      background: #e0e7ff;
      color: #3730a3;
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
          <h2 class="briefing-title">🚨 긴급 시황 브리핑: 15일 서킷브레이커 쇼크 후 코스피 5,700선 기술적 반등</h2>
        </div>
        <span class="briefing-date" id="briefingDate">2026.10.16 11:30 팩트체크 업데이트</span>
      </div>

      <!-- Live Global Market Snapshot -->
      <div class="briefing-market-grid">
        <div class="market-chip" data-chip-id="kospi">
          <span class="market-chip-name">🇰🇷 코스피</span>
          <span class="market-chip-val ticker-up">5,720.50 ▲ +3.00%</span>
        </div>
        <div class="market-chip" data-chip-id="kosdaq">
          <span class="market-chip-name">🇰🇷 코스닥</span>
          <span class="market-chip-val ticker-up">792.00 ▲ +4.10%</span>
        </div>
        <div class="market-chip" data-chip-id="dji">
          <span class="market-chip-name">🇺🇸 다우존스</span>
          <span class="market-chip-val ticker-up">52,245.50 ▲ +0.37%</span>
        </div>
        <div class="market-chip" data-chip-id="sp500">
          <span class="market-chip-name">🇺🇸 S&amp;P 500</span>
          <span class="market-chip-val ticker-up">7,908.20 ▲ +0.60%</span>
        </div>
        <div class="market-chip" data-chip-id="nasdaq">
          <span class="market-chip-name">🇺🇸 나스닥 100</span>
          <span class="market-chip-val ticker-up">27,650.40 ▲ +0.65%</span>
        </div>
        <div class="market-chip" data-chip-id="sox">
          <span class="market-chip-name">🇺🇸 필라델피아 반도체</span>
          <span class="market-chip-val ticker-up">12,625.30 ▲ +2.87%</span>
        </div>
        <div class="market-chip" data-chip-id="usdkrw">
          <span class="market-chip-name">🇰🇷 원/달러 환율</span>
          <span class="market-chip-val ticker-down" style="color: #10b981; font-weight: 800;">1,343.80 ▼ -0.80원</span>
        </div>
      </div>

      <div class="briefing-content-summary">
        10월 15일 -7.57% 서킷브레이커 대폭락(5,554.22) 후, 16일 뉴욕증시 반등과 낙폭 과대에 따른 기술적 저가 매수세가 유입되며 코스피가 5,720선(+3.0%)을 탈환했습니다. 원/달러 환율 1,340원대 안정 유지 속 12M Fwd PBR 1.08배 도달과 PBR 1.0배(5,000선) 안전 마진, 실전 비상 3대 대응 전략을 긴급 점검합니다.
      </div>

      <ul class="briefing-points">
        <li>📌 <strong>증시 타임라인:</strong> 15일 코스피 5,554.22(-7.57%) 서킷브레이커 쇼크 후 16일 5,720선(+3.0%) 회복 및 코스닥 792선(+4.1%) 급반등.</li>
        <li>📌 <strong>환율 &amp; 밸류에이션:</strong> 원/달러 환율 1,340원대(1,343.8원) 안정으로 외환위기 차단, 코스피 PBR 1.08배 도달 및 1차 마지노선 PBR 1.0배(5,000선) 지지선.</li>
        <li>📌 <strong>실전 대응 수칙:</strong> 기술적 반등 시 뇌동 추격 매수 엄금, 외국인 선물·현물 수급 전환 확인, 현금 30% 확보 및 실적주 분할 매수.</li>
      </ul>

      <div style="display: flex; gap: 12px; align-items: center; flex-wrap: wrap;">
        <a href="posts/{post_filename}" class="briefing-btn" id="latestBriefingLink">
          🚨 오늘의 증시 긴급 분석 리포트 전문 읽기 →
        </a>
        <span style="font-size: 0.8rem; color: var(--text-muted);">매일 최신 경제 데이터 및 긴급 시황으로 자동 갱신됩니다.</span>
      </div>
    </section>'''

# 5. index.html, sitemap.xml, rss.xml, published_history.json 동기화
from sys import path
path.insert(0, str(ROOT_DIR / "stock-blog-agent"))
from blog_publisher import BlogPublisher

article_data = {
    "title": "오늘의 증시 시황: 15일 서킷브레이커 쇼크 후 코스피 5,700선 기술적 반등... 환율 1,340원대와 PBR 1.0배 지지선 점검",
    "filename": post_filename,
    "date": "2026-10-16",
    "category": "market",
    "image": "images/daily-market-20261016/thumbnail.png",
    "summary": "10월 15일 코스피 -7.57% 서킷브레이커 폭락 쇼크 후 16일 5,700선(+3.0%) 기술적 반등 전개. 원/달러 환율 1,340원대 안정 속 코스피 12M Fwd PBR 1.08배 도달과 PBR 1.0배(5,000선) 지지선 분석, 실전 비상 대응 3대 수칙 총정리.",
    "is_morning": True,
    "briefing_section_html": briefing_section_html
}

publisher = BlogPublisher()
# sitemap 업데이트
publisher.update_sitemap(post_filename, "2026-10-16")
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

print("[배포 완료] 블로그 포스트 및 인덱스 동기화 완료!")
