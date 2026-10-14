# -*- coding: utf-8 -*-
import sys
import io
import re
import json
from pathlib import Path
from datetime import datetime

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT_DIR = Path(r"c:\Users\immnu\Desktop\Claud")
BLOG_DIR = ROOT_DIR / "adsense-stock-blog"
POSTS_DIR = BLOG_DIR / "posts"

POST_FILENAME = "20261014-google-adsense-master-guide.html"
POST_PATH = POSTS_DIR / POST_FILENAME

html_template = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>🏆 구글 애드센스 승인 &amp; 수익 극대화 실전 마스터 가이드 | Value Stock Labs</title>
  <meta name="description" content="스톡인사이트(StockInsight) 블로그를 인터넷에 무료로 배포하고, 구글 검색엔진 등록 및 애드센스 승인을 받아 최대 광고 수익을 올리기 위한 단계별 실전 가이드입니다.">
  <meta name="keywords" content="구글애드센스, 애드센스승인, 블로그배포, Vercel, Netlify, 구글서치콘솔, 사이트맵, ads.txt, ads.js, 고수익RPM, 고단가CPC, valuestocklabs">
  <link rel="canonical" href="https://www.valuestocklabs.com/posts/20261014-google-adsense-master-guide.html">
  <meta property="og:type" content="article">
  <meta property="og:title" content="🏆 구글 애드센스 승인 &amp; 수익 극대화 실전 마스터 가이드 | Value Stock Labs">
  <meta property="og:description" content="스톡인사이트(StockInsight) 블로그를 인터넷에 무료로 배포하고, 구글 검색엔진 등록 및 애드센스 승인을 받아 최대 광고 수익을 올리기 위한 단계별 실전 가이드입니다.">
  <meta property="og:image" content="https://www.valuestocklabs.com/images/adsense-master-guide/thumbnail.png">
  <meta property="og:url" content="https://www.valuestocklabs.com/posts/20261014-google-adsense-master-guide.html">
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7807868644631223" crossorigin="anonymous"></script>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
  <style>
    :root {
      --primary: #4f46e5;
      --primary-hover: #4338ca;
      --primary-light: #eef2ff;
      --accent-cyan: #0284c7;
      --accent-green: #059669;
      --accent-amber: #d97706;
      --text-main: #0f172a;
      --text-body: #334155;
      --text-muted: #64748b;
      --bg-page: #f8fafc;
      --bg-card: #ffffff;
      --border-color: #e2e8f0;
      --radius-sm: 8px;
      --radius-md: 14px;
      --radius-lg: 20px;
      --shadow-sm: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
      --shadow-md: 0 6px 16px -2px rgba(0, 0, 0, 0.06);
      --shadow-lg: 0 16px 32px -4px rgba(0, 0, 0, 0.08);
    }

    * { margin: 0; padding: 0; box-sizing: border-box; }
    html { scroll-behavior: smooth; }
    body {
      font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
      background-color: var(--bg-page);
      color: var(--text-body);
      line-height: 1.85;
      font-size: 17px;
      word-break: keep-all;
      -webkit-font-smoothing: antialiased;
    }

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
      background: linear-gradient(90deg, #f59e0b, #4f46e5);
      transition: width 0.1s;
    }

    .site-header {
      background: rgba(255, 255, 255, 0.95);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--border-color);
      position: sticky;
      top: 0;
      z-index: 900;
    }
    .header-inner {
      max-width: 900px;
      margin: 0 auto;
      padding: 16px 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .brand-logo {
      font-size: 20px;
      font-weight: 900;
      color: var(--text-main);
      text-decoration: none;
      display: flex;
      align-items: center;
      gap: 8px;
      letter-spacing: -0.5px;
    }
    .brand-logo span.tag {
      font-size: 11px;
      font-weight: 700;
      background: #fef3c7;
      color: #92400e;
      padding: 3px 8px;
      border-radius: 9999px;
      text-transform: uppercase;
    }
    .header-date {
      font-size: 14px;
      font-weight: 600;
      color: var(--text-muted);
    }

    .article-container {
      max-width: 840px;
      margin: 40px auto 100px;
      padding: 0 24px;
    }

    .post-header {
      margin-bottom: 36px;
    }
    .category-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: #059669;
      color: #ffffff;
      font-size: 14px;
      font-weight: 700;
      padding: 6px 14px;
      border-radius: 9999px;
      margin-bottom: 18px;
    }
    .post-title {
      font-size: 34px;
      font-weight: 900;
      color: var(--text-main);
      line-height: 1.35;
      letter-spacing: -0.8px;
      margin-bottom: 20px;
    }
    .post-meta {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 16px;
      font-size: 14px;
      color: var(--text-muted);
      padding-bottom: 24px;
      border-bottom: 1px solid var(--border-color);
    }
    .meta-item {
      display: flex;
      align-items: center;
      gap: 5px;
    }
    .meta-badge-eeat {
      background: #ecfdf5;
      color: #065f46;
      border: 1px solid #a7f3d0;
      padding: 2px 8px;
      border-radius: 6px;
      font-weight: 700;
    }

    .lead-box {
      background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
      border: 1px solid var(--border-color);
      border-left: 5px solid #f59e0b;
      padding: 22px 24px;
      border-radius: var(--radius-md);
      margin: 28px 0;
      font-size: 17px;
      line-height: 1.8;
      color: #1e293b;
      font-weight: 500;
      box-shadow: var(--shadow-sm);
    }

    .figure-container {
      margin: 36px 0;
      text-align: center;
    }
    .figure-container img {
      width: 100%;
      height: auto;
      border-radius: var(--radius-md);
      box-shadow: var(--shadow-md);
      border: 1px solid var(--border-color);
      display: block;
    }
    .figure-caption {
      font-size: 14px;
      color: var(--text-muted);
      margin-top: 10px;
      font-weight: 500;
    }

    .toc-card {
      background: #f1f5f9;
      border: 1px solid #e2e8f0;
      border-radius: var(--radius-md);
      padding: 24px 28px;
      margin: 36px 0 44px;
    }
    .toc-title {
      font-size: 17px;
      font-weight: 800;
      color: var(--text-main);
      margin-bottom: 14px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .toc-list {
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }
    .toc-list a {
      color: var(--text-body);
      text-decoration: none;
      font-size: 15px;
      font-weight: 600;
      transition: color 0.15s;
    }
    .toc-list a:hover {
      color: var(--primary);
      text-decoration: underline;
    }

    .content-body h2 {
      font-size: 26px;
      font-weight: 800;
      color: var(--text-main);
      margin: 54px 0 20px;
      padding-bottom: 12px;
      border-bottom: 2px solid #e2e8f0;
      letter-spacing: -0.5px;
      position: relative;
    }
    .content-body h2::after {
      content: '';
      position: absolute;
      bottom: -2px;
      left: 0;
      width: 60px;
      height: 2px;
      background: #f59e0b;
    }
    .content-body h3 {
      font-size: 20px;
      font-weight: 700;
      color: var(--text-main);
      margin: 32px 0 14px;
    }
    .content-body p {
      margin-bottom: 20px;
      color: var(--text-body);
    }
    .content-body ul, .content-body ol {
      margin: 16px 0 24px 24px;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }
    .content-body li {
      color: var(--text-body);
    }
    .content-body a {
      color: var(--primary);
      text-decoration: underline;
      font-weight: 600;
    }

    .checklist-card {
      background: #ffffff;
      border: 1px solid #cbd5e1;
      border-radius: var(--radius-md);
      padding: 24px 28px;
      margin: 24px 0;
      box-shadow: var(--shadow-sm);
    }
    .checklist-item {
      display: flex;
      align-items: flex-start;
      gap: 12px;
      margin-bottom: 14px;
      font-size: 16px;
      color: #1e293b;
    }
    .checklist-item:last-child {
      margin-bottom: 0;
    }
    .check-icon {
      color: #059669;
      font-size: 20px;
      font-weight: 900;
      line-height: 1.2;
    }

    pre {
      background: #0f172a;
      color: #e2e8f0;
      padding: 20px 24px;
      border-radius: var(--radius-sm);
      overflow-x: auto;
      font-family: 'Consolas', 'Courier New', monospace;
      font-size: 14px;
      line-height: 1.6;
      margin: 16px 0 24px;
      border: 1px solid #334155;
    }
    code {
      font-family: 'Consolas', 'Courier New', monospace;
      background: #f1f5f9;
      color: #0f172a;
      padding: 2px 6px;
      border-radius: 4px;
      font-size: 14px;
    }
    pre code {
      background: transparent;
      color: inherit;
      padding: 0;
    }

    .site-footer {
      background: #0f172a;
      color: #94a3b8;
      text-align: center;
      padding: 60px 24px;
      margin-top: 100px;
      font-size: 14px;
      border-top: 1px solid #1e293b;
    }
    .footer-brand {
      font-size: 18px;
      font-weight: 900;
      color: #ffffff;
      letter-spacing: 1px;
      margin-bottom: 12px;
    }
  </style>
</head>
<body>
  <div id="progress-container"><div id="progress-bar"></div></div>

  <header class="site-header">
    <div class="header-inner">
      <a href="../index.html" class="brand-logo">
        Value Stock Labs <span class="tag">MASTER GUIDE</span>
      </a>
      <div class="header-date">2026.10.14</div>
    </div>
  </header>

  <main class="article-container">
    <div class="post-header">
      <span class="category-badge">☕ 모닝 시황</span>
      <h1 class="post-title">🏆 구글 애드센스 승인 &amp; 수익 극대화 실전 마스터 가이드</h1>
      <div class="post-meta">
        <div class="meta-item">✍️ <strong>시황분석팀</strong></div>
        <div class="meta-item">📅 2026-10-14</div>
        <div class="meta-item"><span class="meta-badge-eeat">✓ 공식 가이드</span></div>
      </div>
    </div>

    <div class="lead-box">
      스톡인사이트(StockInsight) 블로그를 인터넷에 무료로 배포하고, 구글 검색엔진 등록 및 애드센스 승인을 받아 <strong>최대 광고 수익</strong>을 올리기 위한 단계별 실전 가이드입니다.
    </div>

    <figure class="figure-container">
      <img src="../images/adsense-master-guide/thumbnail.png" alt="구글 애드센스 승인 및 수익 극대화 실전 마스터 가이드 대표 썸네일">
      <figcaption class="figure-caption">▲ [가이드] Value Stock Labs 공식 구글 애드센스 배포 및 수익 극대화 실전 마스터 가이드</figcaption>
    </figure>

    <div class="toc-card">
      <div class="toc-title">📌 목차</div>
      <ul class="toc-list">
        <li><a href="#step-1">1. STEP 1. 무료 웹 호스팅 1분 배포 (Vercel / Netlify / GitHub)</a></li>
        <li><a href="#step-2">2. STEP 2. 구글 서치콘솔(Google Search Console) 검색 색인 등록</a></li>
        <li><a href="#step-3">3. STEP 3. 구글 애드센스 심사 신청 100% 승인 체크리스트</a></li>
        <li><a href="#step-4">4. STEP 4. 승인 후 실제 구글 광고 활성화 방법 (ads.js &amp; ads.txt)</a></li>
        <li><a href="#step-5">5. STEP 5. 고수익(RPM) 달성을 위한 일일 포스팅 공식</a></li>
      </ul>
    </div>

    <div class="content-body">
      <hr style="margin: 36px 0; border: 0; border-top: 1px solid var(--border-color);">

      <h2 id="step-1">🚀 STEP 1. 무료 웹 호스팅 1분 배포 방법</h2>

      <p>본 블로그는 순수 HTML/CSS/JS 기반으로 빌드 과정 없이 전 세계 CDN 서버에 <strong>무료로 초고속 배포</strong>할 수 있습니다.</p>

      <h3>방법 A: Vercel 배포 (가장 추천 ⭐⭐⭐⭐⭐)</h3>
      <ol>
        <li><a href="https://vercel.com/" target="_blank" rel="noopener">Vercel 공식 홈페이지</a>에 접속하여 무료 회원가입 (GitHub 계정 연동 권장).</li>
        <li><code>Add New...</code> → <code>Project</code> 클릭.</li>
        <li>내 GitHub 저장소를 선택하거나, <code>adsense-stock-blog</code> 폴더를 연결하여 <code>Deploy</code> 버튼 클릭.</li>
        <li>10초 만에 <code>https://내프로젝트.vercel.app</code> 형태의 무료 보안(HTTPS) 도메인이 발급됩니다.</li>
      </ol>

      <h3>방법 B: Netlify 배포</h3>
      <ol>
        <li><a href="https://www.netlify.com/" target="_blank" rel="noopener">Netlify 공식 홈페이지</a> 접속 및 로그인.</li>
        <li><code>Add new site</code> → <code>Deploy manually</code> 선택 후 <code>adsense-stock-blog</code> 폴더를 화면에 드래그 앤 드롭하면 즉시 배포 완료!</li>
      </ol>

      <hr style="margin: 40px 0; border: 0; border-top: 1px solid var(--border-color);">

      <h2 id="step-2">🔍 STEP 2. 구글 서치콘솔(Google Search Console) 등록</h2>

      <p>구글 검색 결과에 내 글들이 자동으로 노출되도록 구글 로봇을 등록합니다.</p>

      <ol>
        <li><a href="https://search.google.com/search-console/" target="_blank" rel="noopener">Google Search Console</a> 접속.</li>
        <li><strong>URL 접두사</strong> 항목에 배포된 내 블로그 주소(예: <code>https://내도메인.vercel.app/</code>) 입력.</li>
        <li>소유권 확인 방식 중 <strong>HTML 태그</strong> 방식을 선택하여 메타 태그 복사 후 <code>index.html</code>의 <code>&lt;head&gt;</code> 안에 붙여넣기.</li>
        <li>서치콘솔 좌측 메뉴의 <strong>Sitemaps(사이트맵)</strong> 클릭:
          <ul style="margin-top: 8px;">
            <li>새 사이트맵 추가 창에 <code>sitemap.xml</code> 입력 후 <strong>[제출]</strong> 클릭.</li>
            <li>상태가 &quot;성공&quot;으로 표시되면 구글봇이 6개의 실전 글과 계산기들을 즉시 수집합니다.</li>
          </ul>
        </li>
      </ol>

      <hr style="margin: 40px 0; border: 0; border-top: 1px solid var(--border-color);">

      <h2 id="step-3">✅ STEP 3. 구글 애드센스 100% 승인 체크리스트</h2>

      <p>스톡인사이트 블로그는 애드센스 승인 심사 기준을 <strong>이미 완벽하게 충족</strong>하고 있습니다.</p>

      <div class="checklist-card">
        <div class="checklist-item">
          <span class="check-icon">☑</span>
          <div><strong>고품질 전문 콘텐츠 구비</strong>: 저평가주, 상승초입주, AI반도체, 공모주 등 1,500자 이상의 고품질 포스팅 6편 완비.</div>
        </div>
        <div class="checklist-item">
          <span class="check-icon">☑</span>
          <div>
            <strong>필수 법적 페이지 탑재</strong>:
            <ul style="margin: 6px 0 0 20px;">
              <li><a href="../pages/privacy-policy.html"><code>pages/privacy-policy.html</code></a> (구글 DART 쿠키 및 개인정보처리방침)</li>
              <li><a href="../pages/disclaimer.html"><code>pages/disclaimer.html</code></a> (금융 투자 면책조항)</li>
              <li><a href="../pages/about.html"><code>pages/about.html</code></a> (블로그 소개 및 에디터 원칙)</li>
              <li><a href="../pages/contact.html"><code>pages/contact.html</code></a> (문의 폼)</li>
            </ul>
          </div>
        </div>
        <div class="checklist-item">
          <span class="check-icon">☑</span>
          <div><strong>모바일 반응형 &amp; 초고속 속도</strong>: Core Web Vitals 최적화 완료.</div>
        </div>
        <div class="checklist-item">
          <span class="check-icon">☑</span>
          <div><strong>명확한 카테고리 네비게이션</strong>: 상단 메뉴 및 하단 푸터 링크 완비.</div>
        </div>
      </div>

      <h3>📝 심사 신청 순서</h3>
      <ol>
        <li><a href="https://adsense.google.com/" target="_blank" rel="noopener">Google AdSense</a> 접속 후 사이트 추가.</li>
        <li>내 블로그 URL 입력.</li>
        <li>애드센스에서 제공하는 애드센스 코드(<code>ca-pub-XXXXXXXXXXXX</code>)를 복사하여 <code>index.html</code> 및 각 포스팅 상단에 입력 (또는 <code>js/ads.js</code>에 입력).</li>
        <li><strong>[검토 요청]</strong> 버튼 클릭! (보통 2일~1주일 내 승인 메일 도착)</li>
      </ol>

      <hr style="margin: 40px 0; border: 0; border-top: 1px solid var(--border-color);">

      <h2 id="step-4">💰 STEP 4. 승인 후 실제 구글 광고 활성화 방법</h2>

      <p>애드센스 승인 완료 메일을 받으신 후 아래 <strong>2가지</strong>만 진행하시면 모든 페이지의 광고가 즉시 실시간 송출됩니다:</p>

      <h3>1) <code>js/ads.js</code> 파일 수정</h3>
      <p><code>c:\\Users\\immnu\\Desktop\\Claud\\adsense-stock-blog\\js\\ads.js</code> 파일을 열고 상단 설정을 변경합니다:</p>

<pre><code class="language-javascript">const ADSENSE_CONFIG = {
  // 발급받은 본인의 애드센스 게시자 ID 입력
  publisherId: 'ca-pub-1234567890123456', 
  
  // false로 변경하여 실제 구글 광고 송출 모드로 전환
  testMode: false, 
  
  autoAds: true
};
</code></pre>

      <h3>2) <code>ads.txt</code> 파일 수정</h3>
      <p><code>c:\\Users\\immnu\\Desktop\\Claud\\adsense-stock-blog\\ads.txt</code> 파일을 열고 본인의 ID로 수정:</p>

<pre><code>google.com, pub-1234567890123456, DIRECT, f08c47fec0942fa0
</code></pre>

      <hr style="margin: 40px 0; border: 0; border-top: 1px solid var(--border-color);">

      <h2 id="step-5">📈 STEP 5. 고수익(RPM) 달성을 위한 일일 포스팅 공식</h2>

      <ol>
        <li>
          <strong>키워드 단가(CPC)가 높은 금융 키워드 집중</strong>:
          <ul style="margin-top: 6px;">
            <li>주식: 저평가 가치주, 실적 턴어라운드, 목표주가, PER/PBR 비교</li>
            <li>재테크: 배당수익률, 연금저축펀드, ISA 비과세, 공모주 청약 일정</li>
          </ul>
        </li>
        <li>
          <strong>체류 시간 증대 유도</strong>:
          <p style="margin-top: 6px;">본문 내에 <a href="../tools/stock-average-calc.html"><code>tools/stock-average-calc.html</code></a>(물타기 계산기)이나 <a href="../tools/target-price-calculator.html"><code>tools/target-price-calculator.html</code></a>(적정주가 계산기) 링크를 걸어 독자가 직접 계산해보게 유도하면 체류 시간이 3분 이상으로 늘어나 광고 RPM이 2배 이상 상승합니다.</p>
        </li>
        <li>
          <strong>골든 슬롯 유지</strong>:
          <p style="margin-top: 6px;">본문 상단 1개, 본문 중간 2개, 우측 스티키 1개 배치를 유지하여 클릭률(CTR) 3%~5% 이상을 달성하세요.</p>
        </li>
      </ol>
    </div>
  </main>

  <footer class="site-footer">
    <div class="footer-brand">VALUE STOCK LABS</div>
    <p>가치투자와 매크로 경제 분석을 선도하는 프리미엄 주식 정보 플랫폼</p>
    <p style="margin-top: 12px; font-size: 13px; color: #64748b;">© 2026 valuestocklabs.com. All rights reserved.</p>
  </footer>

  <script>
    window.addEventListener('scroll', () => {
      const winScroll = document.documentElement.scrollTop || document.body.scrollTop;
      const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
      const scrolled = (winScroll / height) * 100;
      document.getElementById('progress-bar').style.width = scrolled + '%';
    });
  </script>
</body>
</html>
"""

def main():
    # 1. 파일 저장 (UTF-8 인코딩)
    POST_PATH.write_text(html_template, encoding="utf-8")
    print(f"[성공] 신규 포스트 파일 생성: {POST_PATH.name}")

    # 2. BlogPublisher로 동기화
    sys.path.insert(0, str(ROOT_DIR / "stock-blog-agent"))
    from blog_publisher import BlogPublisher
    import rebuild_index_grid
    import fix_all_internal_links
    import fix_all_seo_and_sitemap

    article_data = {
        "title": "🏆 구글 애드센스 승인 & 수익 극대화 실전 마스터 가이드",
        "filename": POST_FILENAME,
        "date": "2026-10-14",
        "category": "market",
        "image": "images/adsense-master-guide/thumbnail.png",
        "summary": "스톡인사이트(StockInsight) 블로그를 인터넷에 무료로 배포하고, 구글 검색엔진 등록 및 애드센스 승인을 받아 최대 광고 수익을 올리기 위한 단계별 실전 가이드입니다.",
        "is_morning": True,
    }

    publisher = BlogPublisher()
    publisher.update_sitemap(POST_FILENAME, "2026-10-14")
    publisher.update_rss(article_data)
    publisher.record_published_history(article_data)

    # 3. index.html 그리드 재빌드
    rebuild_index_grid.rebuild_index_grid()

    # 4. 전체 내부 링크 및 SEO 사이트맵 갱신
    fix_all_internal_links.fix_all_files()
    fix_all_seo_and_sitemap.rebuild_all()

    print("🎉 [배포 완료] 애드센스 마스터 가이드 블로그 오늘의 시황 카테고리 게시 완료!")

if __name__ == "__main__":
    main()
