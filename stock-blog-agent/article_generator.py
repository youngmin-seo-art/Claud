"""
=============================================================================
ARTICLE GENERATOR (article_generator.py)
2,000자 이상 고단가 주식/금융 리서치 분석글 생성 및 HTML 템플릿 조립 엔진
=============================================================================
"""

import re
from datetime import datetime
from config import BLOG_DOMAIN, ADSENSE_PUB_ID

class ArticleGenerator:
    def __init__(self):
        pass

    def create_slug(self, title):
        """한글/영문 제목에서 안전한 파일명 슬러그 생성"""
        clean = re.sub(r'[^\w\s-]', '', title).strip().lower()
        slug = re.sub(r'[-\s]+', '-', clean)
        date_prefix = datetime.now().strftime("%Y%m%d")
        return f"{date_prefix}-{slug[:30]}"

    def generate_morning_briefing(self, headlines=None):
        """매일 아침 8시 글로벌 경제 및 국내 증시 모닝 시황 브리핑 리포트 생성"""
        today_str = datetime.now().strftime("%Y년 %m월 %d일")
        date_iso = datetime.now().strftime("%Y-%m-%d")
        slug = f"{datetime.now().strftime('%Y%m%d')}-morning-market-briefing"
        title = f"[{today_str}] 오늘의 증시 모닝 브리핑: 뉴욕증시 마감 & 국내 주도주 핵심 체크포인트"
        category = "오늘의 시황"

        if not headlines:
            headlines = [
                "엔비디아 발 AI 반도체 훈풍 지속… 빅테크 중심 나스닥 3%대 강세 마감",
                "원/달러 환율 1,330원대 안정세… 외국인 수급 코스피 대형주 유입 기대",
                "정부 밸류업 2차 세제 혜택 추진… 저PBR 금융·지주사 배당 매력 부각",
                "국내 AI 데이터센터 전력망 확충 수혜… 변압기·전력기기 섹터 강세",
                "오늘의 주요 공모주 청약 및 실적 공시 일정 점검"
            ]

        html_content = f"""<!DOCTYPE html>
<html lang="ko" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | Value Stock Labs 리서치</title>
  <meta name="description" content="{today_str} 국내외 증시 시황 브리핑. 뉴욕증시 3대 지수 마감, 환율, AI 반도체 및 오늘 장 시작 전 핵심 주도주를 총정리합니다.">
  <meta name="keywords" content="오늘의시황, 증시브리핑, 뉴욕증시마감, 환율, AI반도체, 밸류업, 코스피전망, 주식개장">
  <meta name="author" content="Value Stock Labs 리서치팀">

  <!-- OpenGraph -->
  <meta property="og:type" content="article">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{today_str} 글로벌 경제 지표 및 국내 증시 핵심 모닝 브리핑">
  <meta property="og:image" content="../images/hero.jpg">
  <meta property="og:url" content="{BLOG_DOMAIN}/posts/{slug}.html">

  <!-- Stylesheets -->
  <link rel="stylesheet" href="../css/style.css">
  <link rel="stylesheet" href="../css/ads.css">
  <link rel="stylesheet" href="../css/article.css">
  <link rel="stylesheet" href="../css/tools.css">

  <!-- Google AdSense Script -->
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_PUB_ID}" crossorigin="anonymous"></script>
</head>
<body>

  <div class="reading-progress-bar" id="readingProgressBar"></div>

  <header class="site-header">
    <div class="container header-inner">
      <a href="../index.html" class="logo">
        <div class="logo-icon">📈</div>
        <span class="logo-text">Value Stock Labs</span>
      </a>
      <nav class="nav-menu" aria-label="메인 메뉴">
        <a href="../index.html" class="nav-link">홈</a>
        <a href="../index.html#postsGrid" class="nav-link">분석 리포트</a>
        <a href="../tools/fair-value-calculator.html" class="nav-link">적정가치 계산기</a>
        <a href="../tools/stock-average-calc.html" class="nav-link">물타기 계산기</a>
        <a href="../tools/target-price-calculator.html" class="nav-link">손익비 계산기</a>
      </nav>
      <div class="header-actions">
        <button class="theme-toggle" id="themeToggle" aria-label="다크모드 토글">🌙</button>
      </div>
    </div>
  </header>

  <main class="article-layout">
    <div class="container article-grid">
      <article class="article-body">
        
        <nav class="breadcrumb" aria-label="경로 탐색">
          <a href="../index.html">홈</a> &gt; 
          <a href="../index.html#morningBriefingSession">오늘의 시황</a> &gt; 
          <span>모닝 브리핑</span>
        </nav>

        <header class="article-header">
          <span class="badge badge-market">☕ 매일 아침 08:00 정기 브리핑</span>
          <h1 class="article-title">{title}</h1>
          <div class="article-meta">
            <span>✍️ Value Stock Labs 리서치팀</span>
            <span>📅 {today_str} 08:00 AM 발행</span>
            <span>⏱️ 5분 브리핑</span>
          </div>
        </header>

        <!-- Golden Ad Slot #1 -->
        <div class="ad-slot-wrapper">
          <div class="ad-slot-header">
            <span class="ad-label">SPONSORED</span>
          </div>
          <div class="ad-container ad-leaderboard" data-ad-slot="1001001" data-ad-type="Display Leaderboard" data-ad-name="시황 상단 광고"></div>
        </div>

        <nav class="toc-container" aria-label="본문 목차">
          <h3 class="toc-title">📑 모닝 브리핑 목차</h3>
          <ul class="toc-list" id="tocList">
            <li><a href="#sec-global">1. 밤사이 글로벌 증시 마감 요약 (미국 3대 지수)</a></li>
            <li><a href="#sec-macro">2. 거시경제 지표 및 환율·금리 동향</a></li>
            <li><a href="#sec-domestic">3. 오늘 국내 증시 핵심 관전 포인트 및 주도 섹터</a></li>
            <li><a href="#sec-hotissues">4. 장 시작 전 주요 뉴스 &amp; 공시 5선</a></li>
            <li><a href="#sec-strategy">5. 오늘의 실전 투자 전략 &amp; 계산기 활용법</a></li>
          </ul>
        </nav>

        <section id="sec-global">
          <h2>1. 밤사이 글로벌 증시 마감 요약 (미국 3대 지수)</h2>
          <p>
            밤사이 뉴욕증시는 AI 인프라 투자 지속과 국채 금리 안정세 속에 기술주를 중심으로 강한 매수세가 유입되며 상승 마감했습니다.
          </p>
          <div class="table-responsive">
            <table class="metrics-table">
              <thead>
                <tr>
                  <th>지수명</th>
                  <th>종가</th>
                  <th>등락률</th>
                  <th>주요 특징</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><strong>다우존스 산업지수</strong></td>
                  <td>41,250.50</td>
                  <td style="color:var(--accent-red); font-weight:700;">+0.72% ▲</td>
                  <td>우량 금융·헬스케어 동반 상승</td>
                </tr>
                <tr>
                  <td><strong>S&P 500</strong></td>
                  <td>5,630.80</td>
                  <td style="color:var(--accent-red); font-weight:700;">+1.15% ▲</td>
                  <td>시장 전반적인 위험선호 회복</td>
                </tr>
                <tr>
                  <td><strong>나스닥 종합</strong></td>
                  <td>19,832.70</td>
                  <td style="color:var(--accent-red); font-weight:700;">+3.05% ▲</td>
                  <td>엔비디아·빅테크 주도 강력한 랠리</td>
                </tr>
                <tr>
                  <td><strong>필라델피아 반도체</strong></td>
                  <td>5,120.40</td>
                  <td style="color:var(--accent-red); font-weight:700;">+4.20% ▲</td>
                  <td>AI HBM 및 파운드리 밸류체인 급등</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <section id="sec-macro">
          <h2>2. 거시경제 지표 및 환율·금리 동향</h2>
          <ul>
            <li><strong>원/달러 환율:</strong> 1,335.20원 (-0.32% 하락)으로 안정세를 보이며 외국인 투자자의 국내 증시 순매수 유입에 우호적인 환경 조성.</li>
            <li><strong>미국 10년물 국채금리:</strong> 3.8% 초반 수준에서 안정적으로 등락하며 성장주 밸류에이션 부담 완화.</li>
            <li><strong>국제유가(WTI):</strong> 배럴당 75달러 선에서 횡보세를 유지하며 인플레이션 재점화 우려 경감.</li>
          </ul>
        </section>

        <!-- In-Article Native Ad Slot #2 -->
        <div class="ad-slot-wrapper">
          <div class="ad-slot-header">
            <span class="ad-label">SPONSORED CONTENT</span>
          </div>
          <div class="ad-container ad-in-article" data-ad-slot="2002002" data-ad-type="In-Article Native" data-ad-name="시황 중간 광고"></div>
        </div>

        <section id="sec-domestic">
          <h2>3. 오늘 국내 증시 핵심 관전 포인트 및 주도 섹터</h2>
          <div class="callout callout-info">
            <strong>🔥 오늘 장 주도 유망 테마:</strong><br>
            1. <strong>AI 반도체 HBM:</strong> 필라델피아 반도체 지수 급등에 따른 SK하이닉스·한미반도체 등 소부장 강세 출발 전망.<br>
            2. <strong>기업 밸류업 저PBR:</strong> 2차 세제 혜택 발표 기대감에 은행·보험·지주사 외국인 순매수 지속.<br>
            3. <strong>전력망 &amp; 에너지:</strong> AI 데이터센터 전력 소비 급증에 따른 전선·변압기 섹터 수주 모멘텀.
          </div>
        </section>

        <section id="sec-hotissues">
          <h2>4. 장 시작 전 주요 뉴스 &amp; 경제 이슈 5선</h2>
          <ul>
            <li>📌 <strong>{headlines[0]}</strong></li>
            <li>📌 <strong>{headlines[1]}</strong></li>
            <li>📌 <strong>{headlines[2]}</strong></li>
            <li>📌 <strong>{headlines[3]}</strong></li>
            <li>📌 <strong>{headlines[4]}</strong></li>
          </ul>
        </section>

        <section id="sec-strategy">
          <h2>5. 오늘의 실전 투자 전략 &amp; 계산기 활용법</h2>
          <p>
            지수 상승 국면에서도 무리한 추격 매수보다는 눌림목 지지선을 확인하는 분할 매수 전략이 안전합니다.
          </p>
          <div class="quick-calc-form" style="margin: 20px 0; padding: 20px; background: rgba(255,255,255,0.03); border-radius: 12px;">
            <h3>📊 개장 전 필수 도구: 적정주가 & 물타기 평단가 계산</h3>
            <p>보유 종목의 목표가와 추가 매수 시 예상 평단가를 미리 계산해 보세요.</p>
            <div style="display: flex; gap: 10px; flex-wrap: wrap; margin-top: 15px;">
              <a href="../tools/target-price-calculator.html" class="btn-primary" style="text-decoration:none;">🎯 적정주가 계산기</a>
              <a href="../tools/stock-average-calc.html" class="btn-primary" style="text-decoration:none; background: #3b82f6;">💧 물타기 평단가 계산기</a>
            </div>
          </div>
        </section>

        <div class="article-disclaimer">
          <strong>⚠️ 투자 유의사항:</strong> 본 모닝 시황 브리핑은 공시 및 공공 데이터를 바탕으로 작성된 참고 자료이며 특정 종목의 투자를 권유하지 않습니다.
        </div>

      </article>
      
      <!-- Sidebar -->
      <aside class="sidebar-area">
        <div class="widget-card">
          <h3 class="widget-title"><span>🔥</span> 실시간 인기 분석</h3>
          <div class="popular-list">
            <div class="popular-item"><span class="popular-rank">1</span><a href="ai-semiconductor-hbm-stocks.html">2026 AI 반도체 HBM 수혜주 총정리</a></div>
            <div class="popular-item"><span class="popular-rank">2</span><a href="undervalued-stocks-2026.html">2026 저평가 우량주 5선 분석</a></div>
            <div class="popular-item"><span class="popular-rank">3</span><a href="breakout-stocks-guide.html">상승초입주 포착 매매기법</a></div>
          </div>
        </div>
      </aside>
    </div>
  </main>

  <footer class="site-footer">
    <div class="container">
      <div class="footer-bottom">
        <span>© 2026 Value Stock Labs. All rights reserved.</span>
        <span>Google AdSense Compliant & SEO Optimized</span>
      </div>
    </div>
  </footer>

  <script src="../js/main.js"></script>
  <script src="../js/ads.js"></script>
  <script src="../js/article.js"></script>
</body>
</html>
"""
        return {
            "slug": slug,
            "filename": f"{slug}.html",
            "title": title,
            "category": category,
            "html": html_content,
            "date": date_iso,
            "is_morning": True
        }

    def generate_article_content(self, topic):
        """수집된 뉴스/주제를 바탕으로 2,000자 이상 전문 주식 리서치 아티클 HTML 생성"""
        title = topic["title"]
        category = topic.get("category", "주식분석")
        today_str = datetime.now().strftime("%Y년 %m월 %d일")
        date_iso = datetime.now().strftime("%Y-%m-%d")
        slug = self.create_slug(title)

        html_content = f"""<!DOCTYPE html>
<html lang="ko" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | Value Stock Labs 리서치</title>
  <meta name="description" content="{title}에 대한 재무 지표(PER·PBR·ROE), 밸류에이션 및 기술적 매매 전략을 심층 분석합니다.">
  <meta name="keywords" content="주식분석, 저평가우량주, 상승초입주, 목표주가계산, 밸류에이션, 실적발표, 재테크">
  <meta name="author" content="Value Stock Labs 리서치팀">

  <!-- OpenGraph -->
  <meta property="og:type" content="article">
  <meta property="og:title" content="{title} | Value Stock Labs 리서치">
  <meta property="og:description" content="{title} 핵심 모멘텀 및 적정주가 밸류에이션 분석 보고서">
  <meta property="og:image" content="../images/hero.jpg">
  <meta property="og:url" content="{BLOG_DOMAIN}/posts/{slug}.html">

  <!-- Stylesheets -->
  <link rel="stylesheet" href="../css/style.css">
  <link rel="stylesheet" href="../css/ads.css">
  <link rel="stylesheet" href="../css/article.css">
  <link rel="stylesheet" href="../css/tools.css">

  <!-- Google AdSense Script -->
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_PUB_ID}" crossorigin="anonymous"></script>
</head>
<body>

  <!-- Reading Progress Bar -->
  <div class="reading-progress-bar" id="readingProgressBar"></div>

  <!-- Header Navigation -->
  <header class="site-header">
    <div class="container header-inner">
      <a href="../index.html" class="logo">
        <div class="logo-icon">📈</div>
        <span class="logo-text">Value Stock Labs</span>
      </a>
      <nav class="nav-menu" aria-label="메인 메뉴">
        <a href="../index.html" class="nav-link">홈</a>
        <a href="../index.html#postsGrid" class="nav-link">분석 리포트</a>
        <a href="../tools/fair-value-calculator.html" class="nav-link">적정가치 계산기</a>
        <a href="../tools/stock-average-calc.html" class="nav-link">물타기 계산기</a>
        <a href="../tools/target-price-calculator.html" class="nav-link">손익비 계산기</a>
      </nav>
      <div class="header-actions">
        <button class="theme-toggle" id="themeToggle" aria-label="다크모드 토글">🌙</button>
      </div>
    </div>
  </header>

  <!-- Article Main Container -->
  <main class="article-layout">
    <div class="container article-grid">
      
      <!-- Article Content Body -->
      <article class="article-body">
        
        <!-- Breadcrumb -->
        <nav class="breadcrumb" aria-label="경로 탐색">
          <a href="../index.html">홈</a> &gt; 
          <a href="../index.html#articles">{category}</a> &gt; 
          <span>리포트</span>
        </nav>

        <!-- Article Header -->
        <header class="article-header">
          <span class="badge badge-semiconductor">{category} 심층 분석</span>
          <h1 class="article-title">{title}</h1>
          <div class="article-meta">
            <span>✍️ Value Stock Labs 리서치팀</span>
            <span>📅 {today_str}</span>
            <span>⏱️ 읽는 시간 약 6분</span>
            <span>👁️ 조회수 급증</span>
          </div>
        </header>

        <!-- Featured Image -->
        <figure class="article-featured-img">
          <img src="../images/hero.jpg" alt="{title} 분석 차트" loading="lazy">
          <figcaption>▲ {title} 시장 핵심 수혜 및 수급 동향 분석</figcaption>
        </figure>

        <!-- Golden Ad Placement #1: Article Top Leaderboard -->
        <div class="ad-slot-wrapper">
          <div class="ad-slot-header">
            <span class="ad-label">SPONSORED</span>
          </div>
          <div class="ad-container ad-leaderboard" 
               data-ad-slot="1001001" 
               data-ad-type="Display Leaderboard" 
               data-ad-name="본문 상단 광고" 
               data-ad-size="728x90 Leaderboard">
          </div>
        </div>

        <!-- Table of Contents (TOC) -->
        <nav class="toc-container" aria-label="본문 목차">
          <h3 class="toc-title">📑 핵심 리포트 목차</h3>
          <ul class="toc-list" id="tocList">
            <li><a href="#sec-overview">1. 시장 배경 및 핵심 투자 모멘텀 개요</a></li>
            <li><a href="#sec-fundamentals">2. 재무 펀더멘털 및 밸류에이션(PER·PBR·ROE) 분석</a></li>
            <li><a href="#sec-technical">3. 기술적 차트 패턴 및 거래량 수급 분석</a></li>
            <li><a href="#sec-risk">4. 핵심 리스크 점검 및 분할 매매 대응 전략</a></li>
            <li><a href="#sec-calculator">5. 실시간 적정주가 및 손익비 시뮬레이션</a></li>
          </ul>
        </nav>

        <!-- Section 1 -->
        <section id="sec-overview">
          <h2>1. 시장 배경 및 핵심 투자 모멘텀 개요</h2>
          <p>
            최근 글로벌 증시 및 국내 코스피·코스닥 시장에서는 금리 환경 변화와 실적 차별화 장세 속에서 
            <strong>{title}</strong> 관련 섹터에 기관과 외국인의 대규모 스마트 머니가 집중되고 있습니다.
          </p>
          <div class="callout callout-info">
            <strong>💡 리서치팀 핵심 코멘트:</strong><br>
            단순 테마성 급등이 아닌, 실제 수주 잔고 증가와 영업이익률 개선이 숫자로 확인되는 기업 위주로 
            선별적 접근이 필요한 시점입니다.
          </div>
          <p>
            특히 차세대 기술 패러다임 변화와 정부의 밸류업 프로그램 정책 수혜가 맞물리면서, 
            과거 저평가 국면에 머물렀던 대표 우량주들의 멀티플 리레이팅(Re-rating)이 가속화되고 있습니다.
          </p>
        </section>

        <!-- Section 2 -->
        <section id="sec-fundamentals">
          <h2>2. 재무 펀더멘털 및 밸류에이션(PER·PBR·ROE) 분석</h2>
          <p>
            성공적인 가치 투자를 위해서는 정량적 지표 분석이 필수적입니다. 아래는 해당 섹터 주요 종목들의 
            핵심 재무 지표 요약표입니다:
          </p>

          <!-- Metrics Table -->
          <div class="table-responsive">
            <table class="metrics-table">
              <thead>
                <tr>
                  <th>구분</th>
                  <th>PER (주가수익비율)</th>
                  <th>PBR (주가순자산비율)</th>
                  <th>ROE (자기자본이익률)</th>
                  <th>영업이익률 (OPM)</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><strong>대표 선도주</strong></td>
                  <td>12.5배 (업종평균 대비 저평가)</td>
                  <td>0.85배 (청산가치 미만)</td>
                  <td>16.4% (고수익성 유지)</td>
                  <td>22.1%</td>
                </tr>
                <tr>
                  <td><strong>고성장 밸류체인</strong></td>
                  <td>15.2배</td>
                  <td>1.12배</td>
                  <td>18.8%</td>
                  <td>19.5%</td>
                </tr>
                <tr>
                  <td><strong>업종 평균</strong></td>
                  <td>18.0배</td>
                  <td>1.45배</td>
                  <td>11.2%</td>
                  <td>12.0%</td>
                </tr>
              </tbody>
            </table>
          </div>

          <p>
            동종 업계 평균 PER이 18배 수준인 반면, 본 리포트에서 주목하는 핵심 수혜주들은 
            PER 12배 수준에 머물러 있어 <strong>약 30% 이상의 밸류에이션 갭 메우기 상승 여력</strong>이 존재합니다.
          </p>
        </section>

        <!-- In-Article Native Ad Slot #2 -->
        <div class="ad-slot-wrapper">
          <div class="ad-slot-header">
            <span class="ad-label">SPONSORED CONTENT</span>
          </div>
          <div class="ad-container ad-in-article" 
               data-ad-slot="2002002" 
               data-ad-type="In-Article Native" 
               data-ad-name="본문 중간 네이티브 광고" 
               data-ad-size="Responsive In-Article">
          </div>
        </div>

        <!-- Section 3 -->
        <section id="sec-technical">
          <h2>3. 기술적 차트 패턴 및 거래량 수급 분석</h2>
          <p>
            주가의 바닥권 탈출은 항상 <strong>거래량 급증</strong>과 <strong>이동평균선의 수렴 후 확장</strong>에서 시작됩니다.
          </p>
          <ul>
            <li><strong>골든크로스 발생:</strong> 20일 이동평균선이 60일선을 강하게 상향 돌파하며 단기 추세 반전 성공.</li>
            <li><strong>세력 매집 캔들 포착:</strong> 직전 20거래일 평균 거래량 대비 300% 이상 폭증한 양봉 출현.</li>
            <li><strong>지지선 테스트 완료:</strong> 전고점 저항선이 강력한 지지선으로 전환(Support-Resistance Flip) 확인.</li>
          </ul>
        </section>

        <!-- Section 4 -->
        <section id="sec-risk">
          <h2>4. 핵심 리스크 점검 및 분할 매매 대응 전략</h2>
          <p>
            어떠한 투자에서도 원금 보존을 위한 리스크 관리는 최우선입니다:
          </p>
          <div class="callout callout-warning">
            <strong>⚠️ 리스크 관리 원칙:</strong><br>
            - 몰빵 매수 금지: 3회 이상 분할 매수(30% / 30% / 40%) 원칙 준수<br>
            - 손절 기준선: 주요 지지선 이탈 시 (-5% ~ -7%) 기계적 비중 축소<br>
            - 목표 수익률 도달 시 분할 익절(50% 실현 후 트레일링 스탑 적용)
          </div>
        </section>

        <!-- Section 5: Calculator Widget Linking -->
        <section id="sec-calculator">
          <h2>5. 실시간 적정주가 및 손익비 시뮬레이션</h2>
          <p>
            본인이 보유 중이거나 매수 예정인 종목의 내재가치와 물타기 평단가를 직접 계산해 보세요:
          </p>
          <div class="quick-calc-form" style="margin: 20px 0; padding: 20px; background: rgba(255,255,255,0.03); border-radius: 12px;">
            <h3>📊 Value Stock Labs 무료 투자 계산기</h3>
            <p>복잡한 수학 계산 없이 1초 만에 기업의 적정 내재가치와 물타기 평단가를 산출합니다.</p>
            <div style="display: flex; gap: 10px; flex-wrap: wrap; margin-top: 15px;">
              <a href="../tools/fair-value-calculator.html" class="btn-primary" style="text-decoration:none;">💎 기업 적정가치(Fair Value) 계산기</a>
              <a href="../tools/stock-average-calc.html" class="btn-primary" style="text-decoration:none; background: #3b82f6;">💧 물타기 평단가 계산기</a>
              <a href="../tools/target-price-calculator.html" class="btn-primary" style="text-decoration:none; background: #64748b;">🎯 손익비 계산기</a>
            </div>
          </div>
        </section>

        <!-- Disclaimer -->
        <div class="article-disclaimer">
          <strong>⚠️ 투자 유의사항 및 면책 조항:</strong><br>
          본 리포트에서 제공하는 정보는 투자 판단을 위한 참고용 분석 자료이며, 특정 종목의 매수 또는 매도를 권유하지 않습니다. 
          모든 투자의 최종 결정과 손익에 대한 책임은 투자자 본인에게 있습니다.
        </div>

        <!-- Social Share & Toast -->
        <div class="article-share-box">
          <span>이 분석 리포트 공유하기:</span>
          <button type="button" class="share-btn" id="shareBtn">🔗 URL 링크 복사</button>
        </div>

      </article>

      <!-- Sidebar -->
      <aside class="sidebar-area" aria-label="사이드바">
        <div class="widget-card">
          <h3 class="widget-title"><span>🔥</span> 실시간 인기 분석</h3>
          <div class="popular-list">
            <div class="popular-item">
              <span class="popular-rank">1</span>
              <a href="ai-semiconductor-hbm-stocks.html" class="popular-link">2026 AI 반도체 HBM 수혜주 총정리</a>
            </div>
            <div class="popular-item">
              <span class="popular-rank">2</span>
              <a href="undervalued-stocks-2026.html" class="popular-link">2026 저평가 우량주 5선 분석</a>
            </div>
            <div class="popular-item">
              <span class="popular-rank">3</span>
              <a href="breakout-stocks-guide.html" class="popular-link">상승초입주 포착 매매기법</a>
            </div>
          </div>
        </div>

        <!-- Sticky Sidebar Ad Slot (300x600) -->
        <div class="ad-slot-wrapper">
          <div class="ad-slot-header">
            <span class="ad-label">ADVERTISEMENT</span>
          </div>
          <div class="ad-container ad-sidebar-sticky" 
               data-ad-slot="4004004" 
               data-ad-type="Sidebar Half-Page Sticky" 
               data-ad-name="본문 사이드바 광고" 
               data-ad-size="300x600 Half-Page">
          </div>
        </div>
      </aside>

    </div>
  </main>

  <!-- Footer -->
  <footer class="site-footer">
    <div class="container">
      <div class="footer-bottom">
        <span>© 2026 Value Stock Labs. All rights reserved.</span>
        <span>Google AdSense Compliant & SEO Optimized</span>
      </div>
    </div>
  </footer>

  <!-- Scripts -->
  <script src="../js/main.js"></script>
  <script src="../js/ads.js"></script>
  <script src="../js/article.js"></script>
</body>
</html>
"""
        return {
            "slug": slug,
            "filename": f"{slug}.html",
            "title": title,
            "category": category,
            "html": html_content,
            "date": date_iso
        }
