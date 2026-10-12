import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

OUTPUT_DIR = Path(r"c:\Users\immnu\Desktop\Claud\blog new agent\output\20261013-오늘의-증시-시황-마켓브리핑\images")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 1. 대표 썸네일 (1080x1080)
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
      background: linear-gradient(135deg, #070a13 0%, #0f172a 50%, #1e1b4b 100%);
      font-family: 'Pretendard', sans-serif;
      display: flex;
      justify-content: center;
      align-items: center;
      color: #ffffff;
      padding: 60px;
      position: relative;
      overflow: hidden;
    }
    .glow-1 {
      position: absolute;
      width: 580px;
      height: 580px;
      top: -140px;
      right: -120px;
      background: radial-gradient(circle, rgba(99, 102, 241, 0.35) 0%, transparent 70%);
      filter: blur(80px);
    }
    .glow-2 {
      position: absolute;
      width: 580px;
      height: 580px;
      bottom: -140px;
      left: -120px;
      background: radial-gradient(circle, rgba(16, 185, 129, 0.25) 0%, transparent 70%);
      filter: blur(80px);
    }
    .card {
      width: 100%;
      height: 100%;
      background: rgba(255, 255, 255, 0.035);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 40px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      align-items: center;
      text-align: center;
      padding: 70px 50px;
      backdrop-filter: blur(20px);
      box-shadow: 0 30px 60px rgba(0, 0, 0, 0.6);
      position: relative;
      z-index: 10;
    }
    .header-badge {
      display: inline-flex;
      align-items: center;
      gap: 12px;
      font-size: 20px;
      font-weight: 700;
      color: #818cf8;
      background: rgba(99, 102, 241, 0.15);
      border: 1px solid rgba(99, 102, 241, 0.35);
      padding: 12px 30px;
      border-radius: 9999px;
      letter-spacing: 0.5px;
    }
    .header-badge span.dot {
      width: 10px;
      height: 10px;
      background-color: #38bdf8;
      border-radius: 50%;
      box-shadow: 0 0 12px #38bdf8;
    }
    .main-content {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 22px;
    }
    .title {
      font-size: 56px;
      font-weight: 900;
      line-height: 1.25;
      letter-spacing: -1.5px;
      color: #ffffff;
    }
    .title .highlight {
      background: linear-gradient(90deg, #60a5fa, #818cf8, #c084fc);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .subtitle {
      font-size: 24px;
      color: #94a3b8;
      font-weight: 500;
      line-height: 1.5;
      max-width: 820px;
    }
    .stats-container {
      display: flex;
      gap: 20px;
      width: 100%;
      justify-content: center;
    }
    .stat-pill {
      flex: 1;
      max-width: 290px;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 22px;
      padding: 20px 24px;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 8px;
    }
    .stat-label {
      font-size: 15px;
      color: #94a3b8;
      font-weight: 600;
    }
    .stat-val {
      font-size: 27px;
      font-weight: 800;
      color: #ffffff;
      font-family: 'Pretendard', sans-serif;
    }
    .stat-val.up { color: #34d399; }
    .stat-val.down { color: #f87171; }
    .stat-diff {
      font-size: 14px;
      font-weight: 600;
    }
    .stat-diff.up { color: #34d399; }
    .stat-diff.down { color: #f87171; }
    .footer-brand {
      font-size: 18px;
      font-weight: 700;
      color: #64748b;
      letter-spacing: 2px;
    }
  </style>
</head>
<body>
  <div class="glow-1"></div>
  <div class="glow-2"></div>
  <div class="card">
    <div class="header-badge">
      <span class="dot"></span>
      2026.10.13 오늘의 증시 시황
    </div>
    <div class="main-content">
      <h1 class="title">코스피 <span class="highlight">6,380선 지지력 테스트</span><br>9월 CPI·TSMC 슈퍼위크</h1>
      <p class="subtitle">외국인 2.1조 매도와 반도체 셀온(Sell-on) 분석 & 실적 어닝시즌 투자 전략</p>
    </div>
    <div class="stats-container">
      <div class="stat-pill">
        <span class="stat-label">코스피 (KOSPI)</span>
        <span class="stat-val down">6,384.24 pt</span>
        <span class="stat-diff down">-241.69 (-3.65%)</span>
      </div>
      <div class="stat-pill">
        <span class="stat-label">다우존스 30</span>
        <span class="stat-val up">51,850.55 pt</span>
        <span class="stat-diff up">+195.60 (+0.38%)</span>
      </div>
      <div class="stat-pill">
        <span class="stat-label">원/달러 환율</span>
        <span class="stat-val down">1,334.14원</span>
        <span class="stat-diff down">-5.86 (-0.44%)</span>
      </div>
    </div>
    <div class="footer-brand">VALUE STOCK LABS • DAILY MARKET BRIEFING</div>
  </div>
</body>
</html>
"""

# 2. 본문 인포그래픽 1: 국내외 주요 지수 및 환율 비교 표 (1200x800)
body1_html = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 1200px;
      height: 800px;
      background: #090d16;
      font-family: 'Pretendard', sans-serif;
      color: #ffffff;
      padding: 50px 60px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      overflow: hidden;
      position: relative;
    }
    .glow {
      position: absolute;
      top: -150px;
      right: 100px;
      width: 600px;
      height: 400px;
      background: radial-gradient(circle, rgba(99, 102, 241, 0.25) 0%, transparent 70%);
      filter: blur(60px);
    }
    .header {
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
      padding-bottom: 20px;
      position: relative;
      z-index: 2;
    }
    .header-left h2 {
      font-size: 32px;
      font-weight: 800;
      color: #ffffff;
      margin-bottom: 8px;
    }
    .header-left p {
      font-size: 16px;
      color: #94a3b8;
    }
    .tag {
      font-size: 14px;
      font-weight: 700;
      background: rgba(99, 102, 241, 0.15);
      color: #818cf8;
      border: 1px solid rgba(99, 102, 241, 0.3);
      padding: 6px 16px;
      border-radius: 9999px;
    }
    .table-container {
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 24px;
      padding: 24px;
      backdrop-filter: blur(12px);
      position: relative;
      z-index: 2;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      text-align: left;
    }
    th {
      font-size: 15px;
      font-weight: 600;
      color: #94a3b8;
      padding: 14px 20px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    td {
      font-size: 16px;
      font-weight: 600;
      color: #e2e8f0;
      padding: 16px 20px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.04);
    }
    tr:last-child td {
      border-bottom: none;
    }
    .up { color: #34d399 !important; font-weight: 700; }
    .down { color: #f87171 !important; font-weight: 700; }
    .badge {
      display: inline-block;
      padding: 4px 10px;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 600;
    }
    .badge.down { background: rgba(248, 113, 113, 0.15); color: #f87171; }
    .badge.up { background: rgba(52, 211, 153, 0.15); color: #34d399; }
    .badge.blue { background: rgba(56, 189, 248, 0.15); color: #38bdf8; }
    .footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 14px;
      color: #64748b;
      position: relative;
      z-index: 2;
    }
  </style>
</head>
<body>
  <div class="glow"></div>
  <div class="header">
    <div class="header-left">
      <h2>글로벌 주요 증시 및 환율 등락 비교</h2>
      <p>2026년 10월 13일 국내외 금융시장 실시간 마감 지표 집계</p>
    </div>
    <div class="tag">MARKET OVERVIEW</div>
  </div>

  <div class="table-container">
    <table>
      <thead>
        <tr>
          <th>구분 / 시장</th>
          <th>종목 및 지수명</th>
          <th>현재가 / 지수</th>
          <th>등락률</th>
          <th>시장 진단 및 주요 특징</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><span class="badge down">국내증시</span></td>
          <td><strong>코스피 (KOSPI)</strong></td>
          <td>6,384.24 pt</td>
          <td class="down">-3.65%</td>
          <td>외국인 2.1조 원 집중 매도세에 6,400선 하회</td>
        </tr>
        <tr>
          <td><span class="badge down">국내증시</span></td>
          <td><strong>코스닥 (KOSDAQ)</strong></td>
          <td>849.19 pt</td>
          <td class="down">-4.83%</td>
          <td>바이오·2차전지 중소형 성장주 급락 여파</td>
        </tr>
        <tr>
          <td><span class="badge up">뉴욕증시</span></td>
          <td><strong>다우존스 30</strong></td>
          <td>51,850.55 pt</td>
          <td class="up">+0.38%</td>
          <td>전통 가치주 및 월가 금융주 중심 반등 주도</td>
        </tr>
        <tr>
          <td><span class="badge down">뉴욕증시</span></td>
          <td><strong>S&P 500</strong></td>
          <td>7,807.24 pt</td>
          <td class="down">-0.06%</td>
          <td>빅테크 상승 vs 반도체 조정 속 강보합권</td>
        </tr>
        <tr>
          <td><span class="badge down">뉴욕증시</span></td>
          <td><strong>나스닥 종합</strong></td>
          <td>27,245.90 pt</td>
          <td class="down">-0.44%</td>
          <td>14일 9월 CPI 앞두고 기술주 관망세 형성</td>
        </tr>
        <tr>
          <td><span class="badge down">반도체</span></td>
          <td><strong>필라델피아 반도체</strong></td>
          <td>12,236.79 pt</td>
          <td class="down">-2.67%</td>
          <td>엔비디아(-1.29%), 마이크론 등 차익 매물 출회</td>
        </tr>
        <tr>
          <td><span class="badge blue">외환</span></td>
          <td><strong>USD/KRW 환율</strong></td>
          <td>1,334.14원</td>
          <td class="down">-0.44%</td>
          <td>반도체 수출 네고 물량 유입으로 하향 안정 유지</td>
        </tr>
      </tbody>
    </table>
  </div>

  <div class="footer">
    <span>출처: 한국거래소(KRX), Yahoo Finance 실시간 데이터 집계</span>
    <span>VALVESTOCKLABS RESEARCH</span>
  </div>
</body>
</html>
"""

# 3. 본문 인포그래픽 2: 반도체 급락 3대 원인과 실물 펀더멘털 비교 (1200x800)
body2_html = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 1200px;
      height: 800px;
      background: #090d16;
      font-family: 'Pretendard', sans-serif;
      color: #ffffff;
      padding: 50px 60px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      overflow: hidden;
      position: relative;
    }
    .glow {
      position: absolute;
      top: -120px;
      left: 150px;
      width: 600px;
      height: 400px;
      background: radial-gradient(circle, rgba(239, 68, 68, 0.2) 0%, transparent 70%);
      filter: blur(70px);
    }
    .header {
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
      padding-bottom: 20px;
      position: relative;
      z-index: 2;
    }
    .header-left h2 {
      font-size: 32px;
      font-weight: 800;
      color: #ffffff;
      margin-bottom: 8px;
    }
    .header-left p {
      font-size: 16px;
      color: #94a3b8;
    }
    .tag {
      font-size: 14px;
      font-weight: 700;
      background: rgba(239, 68, 68, 0.15);
      color: #f87171;
      border: 1px solid rgba(239, 68, 68, 0.3);
      padding: 6px 16px;
      border-radius: 9999px;
    }
    .grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 24px;
      position: relative;
      z-index: 2;
    }
    .panel {
      background: rgba(255, 255, 255, 0.035);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 24px;
      padding: 28px 30px;
      backdrop-filter: blur(12px);
    }
    .panel-title {
      font-size: 20px;
      font-weight: 800;
      display: flex;
      align-items: center;
      gap: 10px;
      margin-bottom: 20px;
      padding-bottom: 14px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }
    .panel-title.red { color: #f87171; }
    .panel-title.green { color: #34d399; }
    .issue-item {
      display: flex;
      flex-direction: column;
      gap: 6px;
      margin-bottom: 16px;
    }
    .issue-item:last-child { margin-bottom: 0; }
    .issue-header {
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 16px;
      font-weight: 700;
      color: #e2e8f0;
    }
    .badge-num {
      width: 24px;
      height: 24px;
      border-radius: 50%;
      background: rgba(248, 113, 113, 0.2);
      color: #f87171;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 13px;
      font-weight: 800;
    }
    .issue-desc {
      font-size: 14px;
      color: #94a3b8;
      line-height: 1.5;
      padding-left: 34px;
    }
    .stat-highlight {
      background: rgba(52, 211, 153, 0.08);
      border: 1px solid rgba(52, 211, 153, 0.2);
      border-radius: 18px;
      padding: 20px;
      margin-bottom: 16px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .stat-highlight .label { font-size: 15px; color: #94a3b8; font-weight: 600; }
    .stat-highlight .value { font-size: 24px; font-weight: 900; color: #34d399; }
    .footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 14px;
      color: #64748b;
      position: relative;
      z-index: 2;
    }
  </style>
</head>
<body>
  <div class="glow"></div>
  <div class="header">
    <div class="header-left">
      <h2>반도체 섹터 급락 배경 vs 실물 펀더멘털 비교</h2>
      <p>단기 수급 불안 요인 3가지와 사상 최대 수출 실적 팩트 체크</p>
    </div>
    <div class="tag">DEEP DIVE</div>
  </div>

  <div class="grid">
    <div class="panel">
      <div class="panel-title red">
        <span>⚠️</span> 단기 주가 하락을 유발한 3대 악재
      </div>
      <div class="issue-item">
        <div class="issue-header">
          <span class="badge-num">1</span>
          <span>호실적 발표 후 셀온(Sell-on) 차익 실현</span>
        </div>
        <p class="issue-desc">삼성전자 호실적 발표 직후 단기 재료 소진 인식으로 기관 및 헤지펀드 매물 출회.</p>
      </div>
      <div class="issue-item">
        <div class="issue-header">
          <span class="badge-num">2</span>
          <span>중국 창신메모리(CXMT) 추격 우려</span>
        </div>
        <p class="issue-desc">중국 레거시 D램 공급 확대 보도 및 글로벌 IB의 보수적 리포트로 투심 위축.</p>
      </div>
      <div class="issue-item">
        <div class="issue-header">
          <span class="badge-num">3</span>
          <span>글로벌 패시브 펀드 포트폴리오 리밸런싱</span>
        </div>
        <p class="issue-desc">10월 중순 어닝시즌을 앞두고 한국 대형 IT 비중을 기계적으로 축소 조정.</p>
      </div>
    </div>

    <div class="panel">
      <div class="panel-title green">
        <span>✅</span> 흔들림 없는 실물 펀더멘털 Fact
      </div>
      <div class="stat-highlight">
        <span class="label">10월 1~10일 반도체 수출액</span>
        <span class="value">122억 달러 (+170.9%)</span>
      </div>
      <div class="stat-highlight">
        <span class="label">AI 데이터센터 향 HBM 수주</span>
        <span class="value">2026~2027 가시성 확보</span>
      </div>
      <p style="font-size: 14px; color: #94a3b8; line-height: 1.6; padding: 4px;">
        💡 <strong>리서치 결론:</strong> 이번 코스피 대형 반도체 급락은 이익 훼손에 의한 하락이 아닌 <strong>단기 과열 수급 해소 국면</strong>이며, 사상 최대 수출 실적이 하방을 강력히 지지하고 있습니다.
      </p>
    </div>
  </div>

  <div class="footer">
    <span>출처: 관세청 10월 수출입 통계, 주요 증권사 리서치센터 취합</span>
    <span>VALVESTOCKLABS RESEARCH</span>
  </div>
</body>
</html>
"""

# 4. 본문 인포그래픽 3: 이번 주 슈퍼위크 캘린더 및 3대 투자 수칙 (1200x800)
body3_html = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 1200px;
      height: 800px;
      background: #090d16;
      font-family: 'Pretendard', sans-serif;
      color: #ffffff;
      padding: 50px 60px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      overflow: hidden;
      position: relative;
    }
    .glow {
      position: absolute;
      bottom: -150px;
      right: 150px;
      width: 600px;
      height: 400px;
      background: radial-gradient(circle, rgba(16, 185, 129, 0.2) 0%, transparent 70%);
      filter: blur(70px);
    }
    .header {
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
      padding-bottom: 20px;
      position: relative;
      z-index: 2;
    }
    .header-left h2 {
      font-size: 32px;
      font-weight: 800;
      color: #ffffff;
      margin-bottom: 8px;
    }
    .header-left p {
      font-size: 16px;
      color: #94a3b8;
    }
    .tag {
      font-size: 14px;
      font-weight: 700;
      background: rgba(16, 185, 129, 0.15);
      color: #34d399;
      border: 1px solid rgba(16, 185, 129, 0.3);
      padding: 6px 16px;
      border-radius: 9999px;
    }
    .cards-row {
      display: flex;
      gap: 20px;
      position: relative;
      z-index: 2;
    }
    .card-item {
      flex: 1;
      background: rgba(255, 255, 255, 0.035);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 22px;
      padding: 28px 24px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      backdrop-filter: blur(12px);
    }
    .card-badge {
      font-size: 13px;
      font-weight: 700;
      color: #38bdf8;
      background: rgba(56, 189, 248, 0.12);
      padding: 4px 12px;
      border-radius: 8px;
      display: inline-block;
      margin-bottom: 16px;
      align-self: flex-start;
    }
    .card-title {
      font-size: 20px;
      font-weight: 800;
      color: #ffffff;
      margin-bottom: 12px;
      line-height: 1.35;
    }
    .card-desc {
      font-size: 14px;
      color: #94a3b8;
      line-height: 1.6;
      margin-bottom: 16px;
      flex-grow: 1;
    }
    .card-footer {
      font-size: 13px;
      font-weight: 700;
      color: #34d399;
      border-top: 1px solid rgba(255, 255, 255, 0.06);
      padding-top: 14px;
    }
    .strategy-banner {
      background: rgba(99, 102, 241, 0.12);
      border: 1px solid rgba(99, 102, 241, 0.25);
      border-radius: 20px;
      padding: 20px 28px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      position: relative;
      z-index: 2;
    }
    .strategy-banner .text {
      font-size: 16px;
      color: #e2e8f0;
      font-weight: 600;
    }
    .strategy-banner .text strong {
      color: #818cf8;
    }
    .footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 14px;
      color: #64748b;
      position: relative;
      z-index: 2;
    }
  </style>
</head>
<body>
  <div class="glow"></div>
  <div class="header">
    <div class="header-left">
      <h2>10월 슈퍼위크 주요 캘린더 & 실전 투자 3원칙</h2>
      <p>미국 9월 CPI, ASML 및 TSMC 3분기 실적 발표에 맞춘 대응 로드맵</p>
    </div>
    <div class="tag">ACTION PLAN</div>
  </div>

  <div class="cards-row">
    <div class="card-item">
      <div>
        <span class="card-badge">원칙 1 • 수급 안정</span>
        <h3 class="card-title">코스피 6,350선<br>지지력 확인 후 분할 매수</h3>
        <p class="card-desc">외국인 선물 매도세가 둔화되고 지수 바닥권이 확인될 때까지 뇌동매매를 지양하고 분할 매수 타점 탐색.</p>
      </div>
      <div class="card-footer">외국인 수급 반전 체크</div>
    </div>

    <div class="card-item">
      <div>
        <span class="card-badge" style="color: #a78bfa; background: rgba(167, 139, 250, 0.12);">원칙 2 • 포트폴리오 압축</span>
        <h3 class="card-title">실적 가시성 높은<br>방산·조선·밸류업 압축</h3>
        <p class="card-desc">수주 잔고가 풍부한 방산, 고선가 LNG선 인도 본격화 조선, 자사주 소각 등 주주환원 금융주로 포트폴리오 방어.</p>
      </div>
      <div class="card-footer" style="color: #a78bfa;">어닝 서프라이즈 집중</div>
    </div>

    <div class="card-item">
      <div>
        <span class="card-badge" style="color: #34d399; background: rgba(52, 211, 153, 0.12);">원칙 3 • 슈퍼위크 확인</span>
        <h3 class="card-title">TSMC 실적 가이던스<br>확인 후 반도체 선별 재진입</h3>
        <p class="card-desc">15일 TSMC 실적 콘퍼런스콜에서 AI 수요와 연간 CAPEX 전망 확인 후 낙폭과대 HBM 소부장 선별 접근.</p>
      </div>
      <div class="card-footer">10/15 TSMC 분수령</div>
    </div>
  </div>

  <div class="strategy-banner">
    <div class="text">
      🎯 <strong>핵심 나침반:</strong> 14일 밤 미국 9월 CPI로 매크로 확인 ➔ 15일 TSMC 실적으로 AI 실물 수요 재확인 후 진입
    </div>
    <div style="font-size: 14px; font-weight: 700; color: #818cf8;">VALUE STOCK LABS</div>
  </div>

  <div class="footer">
    <span>일정: 10/14 미국 9월 CPI(21:30) & ASML 실적 | 10/15 TSMC 실적 발표</span>
    <span>VALVESTOCKLABS RESEARCH</span>
  </div>
</body>
</html>
"""

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        tasks = [
            ("thumbnail.png", thumbnail_html, 1080, 1080),
            ("body-1.png", body1_html, 1200, 800),
            ("body-2.png", body2_html, 1200, 800),
            ("body-3.png", body3_html, 1200, 800),
        ]

        for filename, html_code, w, h in tasks:
            page = await browser.new_page(viewport={"width": w, "height": h}, device_scale_factor=2)
            await page.set_content(html_code, wait_until="networkidle")
            out_path = OUTPUT_DIR / filename
            await page.screenshot(path=str(out_path), type="png")
            await page.close()
            print(f"[성공] {filename} 캡처 완료 ({w}x{h}, scale=2)")

        await browser.close()
    print("모든 이미지 제작 및 저장 완료!")

if __name__ == "__main__":
    asyncio.run(main())
