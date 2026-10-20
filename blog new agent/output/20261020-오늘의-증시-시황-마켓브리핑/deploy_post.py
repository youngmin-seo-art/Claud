import shutil
import json
import re
import subprocess
from pathlib import Path
from datetime import datetime

ROOT_DIR = Path(r"c:\Users\immnu\Desktop\Claud")
BLOG_DIR = ROOT_DIR / "adsense-stock-blog"
AGENT_OUTPUT = ROOT_DIR / "blog new agent" / "output" / "20261020-오늘의-증시-시황-마켓브리핑"

# 1. 대상 이미지 디렉토리 설정
TARGET_IMG_DIR = BLOG_DIR / "images" / "daily-market-20261020"
TARGET_IMG_DIR.mkdir(parents=True, exist_ok=True)

# 2. 이미지 복사
for img_name in ["thumbnail.png", "body-1.png", "body-2.png", "body-3.png"]:
    src_file = AGENT_OUTPUT / "images" / img_name
    dst_file = TARGET_IMG_DIR / img_name
    shutil.copy2(src_file, dst_file)
    print(f"[이미지 복사 완료] {src_file.name} -> {dst_file}")

# 3. HTML 포스트 생성 (내용 무변경, 경로 및 프로덕션 헤더/메타만 연결)
post_filename = "20261020-오늘의-증시-시황-코스피-5488선-딛고-5768선-v자-반등-뉴욕-반도체-8일만-상승-속-10월-20일-실전-대응-전략.html"
post_path = BLOG_DIR / "posts" / post_filename

with open(AGENT_OUTPUT / "final.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# 이미지 경로 치환 (./images/ -> ../images/daily-market-20261020/)
html_content = html_content.replace('src="./images/', 'src="../images/daily-market-20261020/')

# canonical 태그, adsense 스크립트, meta 태그 추가
canonical_url = f"https://www.valuestocklabs.com/posts/{post_filename}"
meta_tags = f'''  <meta name="description" content="10월 19일 코스피 장초반 5,488선 급락 딛고 +280pt 폭풍 반등 5,768.01(+1.76%) 안착! 기관 5,746억 순매수와 외인 삼성전자 2일 연속 순매수, 환율 1,330.3원 하향 안정. 간밤 뉴욕 나스닥 +1.11% 및 필라델피아 반도체 8일 만의 하락 탈출 속 코스피 12M Fwd PBR 1.09배 더블 바닥 실전 대응 3대 수칙 총정리.">
  <meta name="keywords" content="오늘의시황, 코스피5768선, 기관순매수, 삼성전자외인순매수, 나스닥반등, 필라델피아반도체, 코스피PBR, 환율1330원, 2차전지폭등, 실전대응수칙, valuestocklabs">
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
      <span class="header-date">2026.10.20 장전 브리핑</span>
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
          <h2 class="briefing-title">🚨 마켓 오프닝 브리핑: 코스피 5,488선 딛고 5,768선 V자 반등 &amp; 필라델피아 반도체 8일만 상승 탈출</h2>
        </div>
        <span class="briefing-date" id="briefingDate">2026.10.20 09:00 브리핑 업데이트</span>
      </div>

      <!-- Live Global Market Snapshot -->
      <div class="briefing-market-grid">
        <div class="market-chip" data-chip-id="kospi">
          <span class="market-chip-name">🇰🇷 코스피</span>
          <span class="market-chip-val ticker-up">5,768.01 ▲ +1.76%</span>
        </div>
        <div class="market-chip" data-chip-id="kosdaq">
          <span class="market-chip-name">🇰🇷 코스닥</span>
          <span class="market-chip-val ticker-up">808.89 ▲ +1.78%</span>
        </div>
        <div class="market-chip" data-chip-id="dji">
          <span class="market-chip-name">🇺🇸 다우존스</span>
          <span class="market-chip-val ticker-down" style="color:#94a3b8;">51,966.03 ▼ -0.07%</span>
        </div>
        <div class="market-chip" data-chip-id="sp500">
          <span class="market-chip-name">🇺🇸 S&amp;P 500</span>
          <span class="market-chip-val ticker-up">7,690.73 ▲ +0.41%</span>
        </div>
        <div class="market-chip" data-chip-id="nasdaq">
          <span class="market-chip-name">🇺🇸 나스닥 100</span>
          <span class="market-chip-val ticker-up">26,430.89 ▲ +1.11%</span>
        </div>
        <div class="market-chip" data-chip-id="sox">
          <span class="market-chip-name">🇺🇸 필라델피아 반도체</span>
          <span class="market-chip-val ticker-up">반등 성공 ▲ +1.8%</span>
        </div>
        <div class="market-chip" data-chip-id="usdkrw">
          <span class="market-chip-name">🇰🇷 원/달러 환율</span>
          <span class="market-chip-val ticker-down" style="color: #10b981; font-weight: 800;">1,330.30 ▼ -1.10원</span>
        </div>
      </div>

      <div class="briefing-content-summary">
        10월 19일 코스피가 장초반 5,488선까지 급락한 뒤 저점 대비 280포인트 폭풍 반등하며 5,768선(+1.76%)에 안착했습니다. 기관이 5,746억 원을 순매수하고 외국인의 삼성전자 2일 연속 순매수 유입, 환율 1,330.3원 하향 안정세가 확인되었습니다. 간밤 뉴욕증시에서도 나스닥이 +1.11% 반등하고 필라델피아 반도체 지수가 8거래일 만에 상승 탈출에 성공했습니다.
      </div>

      <ul class="briefing-points">
        <li>📌 <strong>국내 증시 V자 폭풍 반등:</strong> 코스피 5,768.01(+1.76%) 회복(저점 5,488 대비 +280pt) 및 코스닥 808.89(+1.78%) 800선 탈환.</li>
        <li>📌 <strong>수급 &amp; 환율 안정:</strong> 기관 5,746억 순매수 견인, 외국인 삼성전자 약 1,720억 2일 연속 순매수 및 원·달러 환율 1,330.3원 안착.</li>
        <li>📌 <strong>간밤 대외 호재:</strong> 필라델피아 반도체 8일 만의 하락 탈출(+1.8%) 및 나스닥 +1.11% 반등 vs 코스피 12M Fwd PBR 1.09배 더블 바닥 안전판 구축.</li>
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
    "title": "[오늘의 증시 시황] 코스피 5,488선 딛고 5,768선 V자 반등: 뉴욕 반도체 8일만 상승 속 10월 20일 실전 대응 전략",
    "filename": post_filename,
    "date": "2026-10-20",
    "category": "market",
    "image": "images/daily-market-20261020/thumbnail.png",
    "summary": "10월 19일 코스피 장초반 5,488선 급락 딛고 +280pt 폭풍 반등 5,768.01(+1.76%) 안착! 기관 5,746억 순매수와 외인 삼성전자 2일 연속 순매수, 환율 1,330.3원 하향 안정. 간밤 뉴욕 나스닥 +1.11% 및 필라델피아 반도체 8일 만의 하락 탈출 속 코스피 12M Fwd PBR 1.09배 더블 바닥 실전 대응 3대 수칙 총정리.",
    "is_morning": True,
    "briefing_section_html": briefing_section_html
}

publisher = BlogPublisher()
# sitemap 업데이트
publisher.update_sitemap(post_filename, "2026-10-20")
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

# 7. Git Push 자동 배포
try:
    publisher.git_push(article_data["title"])
    print("[성공] Git 커밋 및 valuestocklabs.com 원격 배포 완료")
except Exception as e:
    print(f"[경고] Git push 실패: {e}")

print("[배포 완료] 블로그 포스트 및 인덱스 동기화 완료!")
