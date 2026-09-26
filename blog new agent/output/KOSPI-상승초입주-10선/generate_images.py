import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

output_dir = Path("c:/Users/immnu/Desktop/Claud/blog new agent/output/KOSPI-상승초입주-10선/images")
output_dir.mkdir(parents=True, exist_ok=True)

thumbnail_html = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 1080px;
      height: 1080px;
      background: radial-gradient(circle at 20% 20%, #1e1b4b 0%, #0f172a 60%, #020617 100%);
      font-family: 'Pretendard', sans-serif;
      display: flex;
      justify-content: center;
      align-items: center;
      color: #ffffff;
      padding: 60px;
    }
    .card {
      width: 100%;
      height: 100%;
      background: rgba(30, 41, 59, 0.45);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 36px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      padding: 64px;
      box-shadow: 0 25px 60px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.15);
      backdrop-filter: blur(20px);
      position: relative;
      overflow: hidden;
    }
    .card::before {
      content: '';
      position: absolute;
      top: -100px;
      right: -100px;
      width: 300px;
      height: 300px;
      background: radial-gradient(circle, rgba(99, 102, 241, 0.35) 0%, rgba(99, 102, 241, 0) 70%);
      border-radius: 50%;
    }
    .top-badge-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .badge {
      font-size: 20px;
      font-weight: 700;
      color: #818cf8;
      background: rgba(99, 102, 241, 0.18);
      border: 1px solid rgba(99, 102, 241, 0.4);
      padding: 10px 24px;
      border-radius: 9999px;
      letter-spacing: 0.5px;
      display: inline-flex;
      align-items: center;
      gap: 8px;
    }
    .brand-tag {
      font-size: 18px;
      font-weight: 600;
      color: #94a3b8;
      letter-spacing: 1px;
    }
    .center-content {
      text-align: center;
      margin: auto 0;
    }
    .sub-highlight {
      font-size: 24px;
      font-weight: 700;
      color: #38bdf8;
      margin-bottom: 20px;
      letter-spacing: 2px;
      text-transform: uppercase;
    }
    .title {
      font-size: 58px;
      font-weight: 800;
      line-height: 1.28;
      margin-bottom: 24px;
      word-break: keep-all;
      background: linear-gradient(180deg, #ffffff 0%, #e2e8f0 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      letter-spacing: -1.5px;
    }
    .desc {
      font-size: 23px;
      font-weight: 400;
      color: #cbd5e1;
      line-height: 1.6;
      word-break: keep-all;
    }
    .bottom-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 16px;
    }
    .grid-item {
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 18px;
      padding: 18px 20px;
      text-align: center;
    }
    .grid-label {
      font-size: 14px;
      color: #94a3b8;
      margin-bottom: 6px;
    }
    .grid-val {
      font-size: 20px;
      font-weight: 700;
      color: #10b981;
    }
  </style>
</head>
<body>
  <div class="card">
    <div class="top-badge-row">
      <div class="badge">🚀 2026 KOSPI 퀀트 스크리닝</div>
      <div class="brand-tag">VALUE STOCK LABS</div>
    </div>
    <div class="center-content">
      <div class="sub-highlight">BREAKOUT STOCKS TOP 10</div>
      <h1 class="title">KOSPI 종목 중<br>상승 초입주 10선</h1>
      <p class="desc">바닥권 정배열 돌파 · 거래량 폭증 · 퀀트 밸류에이션 리포트</p>
    </div>
    <div class="bottom-grid">
      <div class="grid-item">
        <div class="grid-label">기술적 시그널</div>
        <div class="grid-val">20일선 골든크로스</div>
      </div>
      <div class="grid-item">
        <div class="grid-label">수급 조건</div>
        <div class="grid-val">거래량 +250% 폭증</div>
      </div>
      <div class="grid-item">
        <div class="grid-label">주도 섹터</div>
        <div class="grid-val">AI전력·조선·방산</div>
      </div>
    </div>
  </div>
</body>
</html>
"""

body1_html = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 1200px;
      height: 760px;
      background: linear-gradient(135deg, #0b0f19 0%, #111827 50%, #030712 100%);
      font-family: 'Pretendard', sans-serif;
      display: flex;
      justify-content: center;
      align-items: center;
      color: #ffffff;
      padding: 36px;
    }
    .container {
      width: 100%;
      height: 100%;
      background: rgba(17, 24, 39, 0.7);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 24px;
      padding: 32px 40px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
    }
    .header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
      padding-bottom: 16px;
    }
    .header h2 {
      font-size: 26px;
      font-weight: 800;
      color: #f8fafc;
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .header .tag {
      font-size: 14px;
      background: rgba(59, 130, 246, 0.18);
      color: #60a5fa;
      padding: 6px 14px;
      border-radius: 9999px;
      border: 1px solid rgba(59, 130, 246, 0.3);
      font-weight: 600;
    }
    .cards-grid {
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 14px;
      margin: 18px 0;
    }
    .stock-card {
      background: rgba(30, 41, 59, 0.6);
      border: 1px solid rgba(255, 255, 255, 0.07);
      border-radius: 14px;
      padding: 16px 14px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .stock-name {
      font-size: 16px;
      font-weight: 700;
      color: #ffffff;
      margin-bottom: 4px;
    }
    .stock-theme {
      font-size: 12px;
      color: #38bdf8;
      margin-bottom: 12px;
    }
    .metric-row {
      display: flex;
      justify-content: space-between;
      font-size: 12px;
      color: #94a3b8;
      margin-bottom: 4px;
    }
    .metric-val {
      font-weight: 600;
      color: #f1f5f9;
    }
    .target-box {
      margin-top: 10px;
      padding-top: 8px;
      border-top: 1px dashed rgba(255, 255, 255, 0.1);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .target-label { font-size: 11px; color: #a5b4fc; }
    .target-val { font-size: 13px; font-weight: 700; color: #10b981; }
    .footer-note {
      font-size: 12px;
      color: #64748b;
      text-align: right;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h2>📊 KOSPI 상승초입주 TOP 10 퀀트 밸류에이션 요약</h2>
      <div class="tag">2026 컨센서스 기준</div>
    </div>
    <div class="cards-grid">
      <!-- 1 -->
      <div class="stock-card">
        <div>
          <div class="stock-name">HD현대일렉트릭</div>
          <div class="stock-theme">AI 전력망/변압기</div>
        </div>
        <div>
          <div class="metric-row"><span>PER</span><span class="metric-val">21.5배</span></div>
          <div class="metric-row"><span>ROE</span><span class="metric-val">38.2%</span></div>
          <div class="target-box"><span class="target-label">목표가</span><span class="target-val">100만원</span></div>
        </div>
      </div>
      <!-- 2 -->
      <div class="stock-card">
        <div>
          <div class="stock-name">LS일렉트릭</div>
          <div class="stock-theme">배전반/신공장</div>
        </div>
        <div>
          <div class="metric-row"><span>PER</span><span class="metric-val">16.8배</span></div>
          <div class="metric-row"><span>ROE</span><span class="metric-val">22.4%</span></div>
          <div class="target-box"><span class="target-label">목표가</span><span class="target-val">30만원</span></div>
        </div>
      </div>
      <!-- 3 -->
      <div class="stock-card">
        <div>
          <div class="stock-name">삼양식품</div>
          <div class="stock-theme">K-푸드/밀양2공장</div>
        </div>
        <div>
          <div class="metric-row"><span>PER</span><span class="metric-val">18.2배</span></div>
          <div class="metric-row"><span>ROE</span><span class="metric-val">34.5%</span></div>
          <div class="target-box"><span class="target-label">목표가</span><span class="target-val">190만원</span></div>
        </div>
      </div>
      <!-- 4 -->
      <div class="stock-card">
        <div>
          <div class="stock-name">한화에어로스페이스</div>
          <div class="stock-theme">K-방산/천무 수출</div>
        </div>
        <div>
          <div class="metric-row"><span>PER</span><span class="metric-val">15.1배</span></div>
          <div class="metric-row"><span>ROE</span><span class="metric-val">21.0%</span></div>
          <div class="target-box"><span class="target-label">목표가</span><span class="target-val">155만원</span></div>
        </div>
      </div>
      <!-- 5 -->
      <div class="stock-card">
        <div>
          <div class="stock-name">삼성중공업</div>
          <div class="stock-theme">FLNG/조선 흑자</div>
        </div>
        <div>
          <div class="metric-row"><span>PER</span><span class="metric-val">14.5배</span></div>
          <div class="metric-row"><span>ROE</span><span class="metric-val">14.8%</span></div>
          <div class="target-box"><span class="target-label">목표가</span><span class="target-val">3.8만원</span></div>
        </div>
      </div>
      <!-- 6 -->
      <div class="stock-card">
        <div>
          <div class="stock-name">두산에너빌리티</div>
          <div class="stock-theme">SMR/원전 르네상스</div>
        </div>
        <div>
          <div class="metric-row"><span>PER</span><span class="metric-val">19.3배</span></div>
          <div class="metric-row"><span>ROE</span><span class="metric-val">9.8%</span></div>
          <div class="target-box"><span class="target-label">목표가</span><span class="target-val">13.5만원</span></div>
        </div>
      </div>
      <!-- 7 -->
      <div class="stock-card">
        <div>
          <div class="stock-name">KB금융</div>
          <div class="stock-theme">밸류업 대장/주주환원</div>
        </div>
        <div>
          <div class="metric-row"><span>PER</span><span class="metric-val">6.2배</span></div>
          <div class="metric-row"><span>PBR</span><span class="metric-val">0.58배</span></div>
          <div class="target-box"><span class="target-label">목표가</span><span class="target-val">22만원</span></div>
        </div>
      </div>
      <!-- 8 -->
      <div class="stock-card">
        <div>
          <div class="stock-name">기아</div>
          <div class="stock-theme">HEV/저PER 우량</div>
        </div>
        <div>
          <div class="metric-row"><span>PER</span><span class="metric-val">4.8배</span></div>
          <div class="metric-row"><span>ROE</span><span class="metric-val">18.5%</span></div>
          <div class="target-box"><span class="target-label">목표가</span><span class="target-val">16.5만원</span></div>
        </div>
      </div>
      <!-- 9 -->
      <div class="stock-card">
        <div>
          <div class="stock-name">한미반도체</div>
          <div class="stock-theme">HBM4 본더 독점</div>
        </div>
        <div>
          <div class="metric-row"><span>영업이익률</span><span class="metric-val">42.0%</span></div>
          <div class="metric-row"><span>ROE</span><span class="metric-val">31.0%</span></div>
          <div class="target-box"><span class="target-label">목표가</span><span class="target-val">30만원</span></div>
        </div>
      </div>
      <!-- 10 -->
      <div class="stock-card">
        <div>
          <div class="stock-name">현대글로비스</div>
          <div class="stock-theme">해상물류/지배구조</div>
        </div>
        <div>
          <div class="metric-row"><span>PER</span><span class="metric-val">7.5배</span></div>
          <div class="metric-row"><span>배당수익률</span><span class="metric-val">4.8%</span></div>
          <div class="target-box"><span class="target-label">목표가</span><span class="target-val">30만원</span></div>
        </div>
      </div>
    </div>
    <div class="footer-note">출처: 에프앤가이드 컨센서스 및 주요 증권사 리서치 센터 취합 · ValueStockLabs</div>
  </div>
</body>
</html>
"""

body2_html = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 1200px;
      height: 680px;
      background: linear-gradient(135deg, #090d16 0%, #111827 100%);
      font-family: 'Pretendard', sans-serif;
      display: flex;
      justify-content: center;
      align-items: center;
      color: #ffffff;
      padding: 40px;
    }
    .container {
      width: 100%;
      height: 100%;
      background: rgba(17, 24, 39, 0.7);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 24px;
      padding: 36px 44px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
    }
    .title-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
      padding-bottom: 16px;
    }
    .title-row h2 {
      font-size: 26px;
      font-weight: 800;
      color: #ffffff;
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .steps-wrapper {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 20px;
      margin: 24px 0;
    }
    .step-card {
      background: rgba(30, 41, 59, 0.5);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 18px;
      padding: 24px 22px;
      display: flex;
      flex-direction: column;
      position: relative;
    }
    .step-badge {
      width: fit-content;
      font-size: 13px;
      font-weight: 800;
      padding: 6px 14px;
      border-radius: 9999px;
      margin-bottom: 14px;
    }
    .step-1 .step-badge { background: rgba(59, 130, 246, 0.2); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.4); }
    .step-2 .step-badge { background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.4); }
    .step-3 .step-badge { background: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.4); }
    
    .step-title {
      font-size: 19px;
      font-weight: 700;
      color: #ffffff;
      margin-bottom: 10px;
    }
    .step-desc {
      font-size: 14px;
      color: #cbd5e1;
      line-height: 1.6;
      margin-bottom: 16px;
    }
    .rule-box {
      background: rgba(15, 23, 42, 0.7);
      border-radius: 10px;
      padding: 12px 14px;
      font-size: 13px;
      color: #94a3b8;
      border-left: 3px solid #6366f1;
    }
    .bottom-rule {
      background: rgba(239, 68, 68, 0.1);
      border: 1px solid rgba(239, 68, 68, 0.25);
      border-radius: 12px;
      padding: 14px 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      color: #fca5a5;
      font-size: 14px;
      font-weight: 500;
    }
    .bottom-rule strong { color: #ffffff; }
  </style>
</head>
<body>
  <div class="container">
    <div class="title-row">
      <h2>📈 상승초입주 실전 매매 3단계 프로세스</h2>
      <span style="font-size: 14px; color: #94a3b8; font-weight: 600;">리스크 최소화 & 수익 극대화 모델</span>
    </div>
    <div class="steps-wrapper">
      <div class="step-card step-1">
        <div class="step-badge">STEP 1 · 돌파 확인 (비중 30%)</div>
        <div class="step-title">기준봉 거래량 돌파 진입</div>
        <div class="step-desc">장기 저항선이나 박스권 상단을 전일 대비 200% 이상 거래량으로 상향 돌파하는 당일 1차 진입.</div>
        <div class="rule-box">📌 조건: 거래량 폭증 + 종가 안착 확인</div>
      </div>
      <div class="step-card step-2">
        <div class="step-badge">STEP 2 · 눌림목 지지 (비중 70%)</div>
        <div class="step-title">전고점 리테스트 분할 매수</div>
        <div class="step-desc">돌파 후 2~5일간 과거 저항선(현 지지선) 또는 20일 이평선까지 건전한 가격 조정을 줄 때 추가 매수.</div>
        <div class="rule-box">📌 조건: 거래량 감소 + 20일선 지지 캔들</div>
      </div>
      <div class="step-card step-3">
        <div class="step-badge">STEP 3 · 손절 & 익절 원칙</div>
        <div class="step-title">트레일링 스탑 & 기계적 손절</div>
        <div class="step-desc">목표가 1차 도달 시 50% 분할 익절, 나머지는 20일선 추세 추종. 지지 이탈 시 무조건 손절.</div>
        <div class="rule-box">📌 조건: 기준봉 시가 이탈 시 -3~5% 손절</div>
      </div>
    </div>
    <div class="bottom-rule">
      <span>⚠️ <strong>철칙</strong>: 거래량이 실리지 않은 돌파는 '가짜 돌파(Fakeout)'일 확률이 높으므로 절대 뇌동매수하지 않습니다.</span>
      <span>ValueStockLabs 매매 원칙</span>
    </div>
  </div>
</body>
</html>
"""

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        # 1. thumbnail
        page = await browser.new_page(viewport={"width": 1080, "height": 1080}, device_scale_factor=2)
        await page.set_content(thumbnail_html, wait_until="networkidle")
        await page.screenshot(path=str(output_dir / "thumbnail.png"), type="png")
        print("thumbnail.png saved")
        
        # 2. body-1
        page1 = await browser.new_page(viewport={"width": 1200, "height": 760}, device_scale_factor=2)
        await page1.set_content(body1_html, wait_until="networkidle")
        await page1.screenshot(path=str(output_dir / "body-1.png"), type="png")
        print("body-1.png saved")
        
        # 3. body-2
        page2 = await browser.new_page(viewport={"width": 1200, "height": 680}, device_scale_factor=2)
        await page2.set_content(body2_html, wait_until="networkidle")
        await page2.screenshot(path=str(output_dir / "body-2.png"), type="png")
        print("body-2.png saved")
        
        await browser.close()
        print("All images generated successfully!")

asyncio.run(main())
