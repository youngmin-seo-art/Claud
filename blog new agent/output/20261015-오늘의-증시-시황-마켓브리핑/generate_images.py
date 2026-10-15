import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

OUTPUT_DIR = Path(r"c:\Users\immnu\Desktop\Claud\blog new agent\output\20261015-오늘의-증시-시황-마켓브리핑\images")
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
      width: 600px;
      height: 600px;
      top: -150px;
      right: -130px;
      background: radial-gradient(circle, rgba(14, 165, 233, 0.4) 0%, transparent 70%);
      filter: blur(80px);
    }
    .glow-2 {
      position: absolute;
      width: 600px;
      height: 600px;
      bottom: -150px;
      left: -130px;
      background: radial-gradient(circle, rgba(16, 185, 129, 0.35) 0%, transparent 70%);
      filter: blur(80px);
    }
    .card {
      width: 100%;
      height: 100%;
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid rgba(255, 255, 255, 0.14);
      border-radius: 40px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      align-items: center;
      text-align: center;
      padding: 70px 50px;
      backdrop-filter: blur(25px);
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
      color: #38bdf8;
      background: rgba(14, 165, 233, 0.15);
      border: 1px solid rgba(14, 165, 233, 0.35);
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
      font-size: 54px;
      font-weight: 900;
      line-height: 1.25;
      letter-spacing: -1.5px;
      color: #ffffff;
    }
    .title .highlight {
      background: linear-gradient(90deg, #38bdf8, #818cf8, #34d399);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .subtitle {
      font-size: 24px;
      color: #94a3b8;
      font-weight: 500;
      line-height: 1.5;
      max-width: 800px;
      word-break: keep-all;
    }
    .metrics-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 18px;
      width: 100%;
    }
    .metric-box {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 20px;
      padding: 22px 16px;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }
    .metric-label {
      font-size: 14px;
      color: #94a3b8;
      font-weight: 600;
    }
    .metric-val {
      font-size: 26px;
      font-weight: 800;
      color: #38bdf8;
      letter-spacing: -0.5px;
    }
    .metric-val.green {
      color: #34d399;
    }
    .metric-val.purple {
      color: #c084fc;
    }
    .metric-desc {
      font-size: 13px;
      color: #cbd5e1;
    }
    .footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
      width: 100%;
      border-top: 1px solid rgba(255, 255, 255, 0.1);
      padding-top: 24px;
      font-size: 15px;
      color: #64748b;
    }
    .footer .source {
      font-weight: 600;
      color: #94a3b8;
    }
  </style>
</head>
<body>
  <div class="glow-1"></div>
  <div class="glow-2"></div>
  <div class="card">
    <div class="header-badge">
      <span class="dot"></span>
      2026.10.15 오늘의 증시 시황 마켓브리핑
    </div>
    
    <div class="main-content">
      <h1 class="title">
        美 CPI 안도 랠리 · 환율 1,330원대 안정<br>
        <span class="highlight">오늘 TSMC 실적 발표 & 6,200선 탈환</span>
      </h1>
      <p class="subtitle">
        9월 CPI 2.3% 부합 · 10년물 금리 3.98% 하회 · 외인 선물 1.2조 순매수 전환<br>
        글로벌 파운드리 1위 TSMC 실적과 코스피 주도주 실전 대응 로드맵
      </p>
    </div>

    <div class="metrics-grid">
      <div class="metric-box">
        <span class="metric-label">美 9월 헤드라인 CPI</span>
        <span class="metric-val green">+2.3%</span>
        <span class="metric-desc">예상 부합 · 인플레 안정</span>
      </div>
      <div class="metric-box">
        <span class="metric-label">원/달러 환율 (NDF)</span>
        <span class="metric-val">1,338.5원</span>
        <span class="metric-desc">전일비 -5.7원 하락(원화 안정세)</span>
      </div>
      <div class="metric-box">
        <span class="metric-label">오늘 핵심 이벤트</span>
        <span class="metric-val purple">TSMC 3Q 실적</span>
        <span class="metric-desc">잠정매출 467억$ · CAPEX 가이던스</span>
      </div>
    </div>

    <div class="footer">
      <span class="source">valuestocklabs.com · 리서치팀</span>
      <span>KOSPI 6,128.90 (+1.55%) | NASDAQ (+0.98%) | 필라델피아반도체 (+1.85%)</span>
    </div>
  </div>
</body>
</html>
"""

# 2. 본문 1: 코스피 6,100선 탈환 및 수급 정상화 비교 인포그래픽 (1080x720)
body1_html = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 1080px;
      height: 720px;
      background: linear-gradient(135deg, #0b0f19 0%, #111827 100%);
      font-family: 'Pretendard', sans-serif;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      color: #ffffff;
      padding: 45px 50px;
      position: relative;
      overflow: hidden;
    }
    .glow {
      position: absolute;
      width: 500px;
      height: 500px;
      top: -100px;
      right: -100px;
      background: radial-gradient(circle, rgba(56, 189, 248, 0.25) 0%, transparent 70%);
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
    .header h2 {
      font-size: 28px;
      font-weight: 800;
      color: #ffffff;
      letter-spacing: -0.5px;
    }
    .header h2 span {
      color: #38bdf8;
    }
    .header .tag {
      font-size: 14px;
      font-weight: 600;
      color: #34d399;
      background: rgba(16, 185, 129, 0.15);
      border: 1px solid rgba(16, 185, 129, 0.3);
      padding: 6px 14px;
      border-radius: 9999px;
    }
    .cards-container {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 22px;
      position: relative;
      z-index: 2;
      margin: 20px 0;
    }
    .market-card {
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 20px;
      padding: 24px;
      display: flex;
      flex-direction: column;
      gap: 14px;
      backdrop-filter: blur(15px);
    }
    .card-title {
      font-size: 16px;
      font-weight: 700;
      color: #94a3b8;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .stat-row {
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      padding: 10px 0;
      border-bottom: 1px dashed rgba(255, 255, 255, 0.08);
    }
    .stat-row:last-child {
      border-bottom: none;
      padding-bottom: 0;
    }
    .stat-name {
      font-size: 15px;
      color: #cbd5e1;
      font-weight: 500;
    }
    .stat-val {
      font-size: 20px;
      font-weight: 800;
      color: #ffffff;
    }
    .stat-val.up { color: #f87171; }
    .stat-val.blue { color: #38bdf8; }
    .stat-val.green { color: #34d399; }
    .footer-note {
      position: relative;
      z-index: 2;
      background: rgba(14, 165, 233, 0.08);
      border: 1px solid rgba(14, 165, 233, 0.2);
      border-radius: 12px;
      padding: 14px 20px;
      font-size: 14px;
      color: #bae6fd;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .footer-note strong {
      color: #ffffff;
    }
  </style>
</head>
<body>
  <div class="glow"></div>
  <div class="header">
    <div>
      <h2>코스피 6,100선 탈환 및 <span>외인·기관 수급 정상화 기류</span></h2>
    </div>
    <div class="tag">10월 14일 마감 & 15일 개장 체크</div>
  </div>

  <div class="cards-container">
    <div class="market-card">
      <div class="card-title">📊 국내 대표 지수 및 환율 변동</div>
      <div class="stat-row">
        <span class="stat-name">코스피(KOSPI)</span>
        <span class="stat-val up">6,128.90 (+1.55%)</span>
      </div>
      <div class="stat-row">
        <span class="stat-name">코스닥(KOSDAQ)</span>
        <span class="stat-val up">838.20 (+2.20%)</span>
      </div>
      <div class="stat-row">
        <span class="stat-name">원/달러 환율 (NDF)</span>
        <span class="stat-val blue">1,338.50원 (-5.7원)</span>
      </div>
      <div class="stat-row">
        <span class="stat-name">외인 선물 순매수</span>
        <span class="stat-val green">+1조 2,400억 원</span>
      </div>
    </div>

    <div class="market-card">
      <div class="card-title">⚡ 시가총액 상위 대장주 등락률</div>
      <div class="stat-row">
        <span class="stat-name">삼성전자 (반도체)</span>
        <span class="stat-val up">237,500원 (+2.37%)</span>
      </div>
      <div class="stat-row">
        <span class="stat-name">SK하이닉스 (HBM)</span>
        <span class="stat-val up">1,488,000원 (+3.12%)</span>
      </div>
      <div class="stat-row">
        <span class="stat-name">한화에어로스페이스 (방산)</span>
        <span class="stat-val up">1,020,000원 (+3.44%)</span>
      </div>
      <div class="stat-row">
        <span class="stat-name">삼성중공업 (조선/FLNG)</span>
        <span class="stat-val up">14,250원 (+2.81%)</span>
      </div>
    </div>
  </div>

  <div class="footer-note">
    <span>💡 <strong>핵심 포인트:</strong> 외인 현물 매도세 급감(-1,840억) 및 선물 대량 환매수로 지수 하방 지지력 확보 완료</span>
    <span>valuestocklabs.com</span>
  </div>
</body>
</html>
"""

# 3. 본문 2: TSMC 3분기 실적 및 CAPEX 수혜 다이어그램 (1080x720)
body2_html = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 1080px;
      height: 720px;
      background: linear-gradient(135deg, #090d16 0%, #151d30 100%);
      font-family: 'Pretendard', sans-serif;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      color: #ffffff;
      padding: 45px 50px;
      position: relative;
      overflow: hidden;
    }
    .glow {
      position: absolute;
      width: 550px;
      height: 550px;
      bottom: -150px;
      right: -100px;
      background: radial-gradient(circle, rgba(129, 140, 248, 0.25) 0%, transparent 70%);
      filter: blur(70px);
    }
    .header {
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
      padding-bottom: 18px;
      position: relative;
      z-index: 2;
    }
    .header h2 {
      font-size: 27px;
      font-weight: 800;
      color: #ffffff;
    }
    .header h2 span { color: #818cf8; }
    .badge {
      font-size: 13px;
      font-weight: 700;
      color: #c084fc;
      background: rgba(192, 132, 252, 0.15);
      border: 1px solid rgba(192, 132, 252, 0.35);
      padding: 6px 14px;
      border-radius: 9999px;
    }
    .diagram-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 18px;
      position: relative;
      z-index: 2;
      margin: 18px 0;
    }
    .diagram-step {
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 18px;
      padding: 24px 20px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      backdrop-filter: blur(15px);
    }
    .step-header {
      display: flex;
      align-items: center;
      gap: 10px;
      margin-bottom: 14px;
    }
    .step-num {
      width: 28px;
      height: 28px;
      background: #4f46e5;
      color: #ffffff;
      font-size: 14px;
      font-weight: 800;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .step-title {
      font-size: 17px;
      font-weight: 700;
      color: #e2e8f0;
    }
    .step-body {
      font-size: 14px;
      color: #94a3b8;
      line-height: 1.6;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    .step-highlight {
      background: rgba(99, 102, 241, 0.15);
      border: 1px solid rgba(99, 102, 241, 0.3);
      padding: 10px 12px;
      border-radius: 10px;
      font-size: 13px;
      color: #c7d2fe;
      font-weight: 600;
      margin-top: 10px;
    }
    .summary-bar {
      position: relative;
      z-index: 2;
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 14px;
      padding: 16px 22px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 14px;
    }
    .summary-bar .item {
      display: flex;
      gap: 8px;
      align-items: center;
      color: #cbd5e1;
    }
    .summary-bar .item strong {
      color: #38bdf8;
    }
  </style>
</head>
<body>
  <div class="glow"></div>
  <div class="header">
    <div>
      <h2>대만 TSMC 3분기 실적 발표 & <span>국내 반도체 밸류체인 수혜</span></h2>
    </div>
    <div class="badge">오늘 15:00 전후 콘퍼런스콜</div>
  </div>

  <div class="diagram-grid">
    <div class="diagram-step">
      <div>
        <div class="step-header">
          <div class="step-num">1</div>
          <div class="step-title">역대 최대 분기 실적</div>
        </div>
        <div class="step-body">
          <p>• 3Q 잠정매출 467억 달러 달성</p>
          <p>• 매출총이익률(GPM) 55% 상회</p>
          <p>• 애플·엔비디아 선단 공정 풀가동</p>
        </div>
      </div>
      <div class="step-highlight">
        🔍 <strong>체크:</strong> AI 가속기 칩 수요의 공급 초과 지속
      </div>
    </div>

    <div class="diagram-step">
      <div>
        <div class="step-header">
          <div class="step-num">2</div>
          <div class="step-title">CAPEX 400억$ 상향</div>
        </div>
        <div class="step-body">
          <p>• 기존 300~320억$ ➔ 400억$ 수준 상향</p>
          <p>• 2nm 팹 양산 설비 조기 투자</p>
          <p>• CoWoS 첨단 패키징 캐파 2배 증설</p>
        </div>
      </div>
      <div class="step-highlight">
        🚀 <strong>체크:</strong> 2026~2027년 반도체 슈퍼사이클 재점화
      </div>
    </div>

    <div class="diagram-step">
      <div>
        <div class="step-header">
          <div class="step-num">3</div>
          <div class="step-title">국내 밸류체인 직격 수혜</div>
        </div>
        <div class="step-body">
          <p>• <strong>SK하이닉스:</strong> TSMC 원팀 HBM4 동맹</p>
          <p>• <strong>삼성전자:</strong> 파운드리 턴어라운드 모멘텀</p>
          <p>• <strong>소부장:</strong> 한미반도체, HPSP, 이수페타시스</p>
        </div>
      </div>
      <div class="step-highlight">
        💎 <strong>체크:</strong> 중국 CXMT 노이즈 및 고점론 종식
      </div>
    </div>
  </div>

  <div class="summary-bar">
    <div class="item">🎯 <span>핵심 결론:</span> <strong>TSMC 호실적은 글로벌 AI 반도체 2차 랠리의 방아쇠</strong></div>
    <div class="item">🌐 <span>valuestocklabs.com</span></div>
  </div>
</body>
</html>
"""

# 4. 본문 3: 핵심 이벤트 및 3대 실전 행동 강령 요약 카드 (1080x720)
body3_html = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 1080px;
      height: 720px;
      background: linear-gradient(135deg, #070d18 0%, #111a2e 100%);
      font-family: 'Pretendard', sans-serif;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      color: #ffffff;
      padding: 45px 50px;
      position: relative;
      overflow: hidden;
    }
    .glow {
      position: absolute;
      width: 600px;
      height: 600px;
      top: -150px;
      left: -150px;
      background: radial-gradient(circle, rgba(16, 185, 129, 0.25) 0%, transparent 70%);
      filter: blur(80px);
    }
    .header {
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
      padding-bottom: 18px;
      position: relative;
      z-index: 2;
    }
    .header h2 {
      font-size: 27px;
      font-weight: 800;
      color: #ffffff;
    }
    .header h2 span { color: #34d399; }
    .badge {
      font-size: 13px;
      font-weight: 700;
      color: #38bdf8;
      background: rgba(56, 189, 248, 0.15);
      border: 1px solid rgba(56, 189, 248, 0.35);
      padding: 6px 14px;
      border-radius: 9999px;
    }
    .actions-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 18px;
      position: relative;
      z-index: 2;
      margin: 18px 0;
    }
    .action-card {
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 20px;
      padding: 24px 20px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      backdrop-filter: blur(15px);
    }
    .action-badge {
      display: inline-block;
      font-size: 12px;
      font-weight: 800;
      padding: 4px 10px;
      border-radius: 6px;
      margin-bottom: 12px;
      width: fit-content;
    }
    .action-badge.blue { background: rgba(56, 189, 248, 0.2); color: #38bdf8; }
    .action-badge.purple { background: rgba(192, 132, 252, 0.2); color: #c084fc; }
    .action-badge.green { background: rgba(52, 211, 153, 0.2); color: #34d399; }
    .action-title {
      font-size: 18px;
      font-weight: 800;
      color: #ffffff;
      line-height: 1.4;
      margin-bottom: 12px;
    }
    .action-desc {
      font-size: 14px;
      color: #94a3b8;
      line-height: 1.6;
    }
    .action-footer {
      border-top: 1px solid rgba(255, 255, 255, 0.08);
      padding-top: 12px;
      margin-top: 14px;
      font-size: 13px;
      color: #cbd5e1;
      font-weight: 600;
    }
    .banner {
      position: relative;
      z-index: 2;
      background: linear-gradient(90deg, rgba(16, 185, 129, 0.15) 0%, rgba(56, 189, 248, 0.15) 100%);
      border: 1px solid rgba(52, 211, 153, 0.3);
      border-radius: 14px;
      padding: 16px 22px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 14px;
    }
    .banner-text {
      color: #d1fae5;
      font-weight: 600;
    }
    .banner-text span {
      color: #ffffff;
      font-weight: 800;
    }
  </style>
</head>
<body>
  <div class="glow"></div>
  <div class="header">
    <div>
      <h2>코스피 6,200선 탈환 대비 <span>3대 실전 투자 행동 강령</span></h2>
    </div>
    <div class="badge">오늘의 실전 가이드</div>
  </div>

  <div class="actions-grid">
    <div class="action-card">
      <div>
        <div class="action-badge blue">원칙 1 · 장 초반</div>
        <div class="action-title">갭상승 추격 매수 자제<br>6,160선 지지 확인</div>
        <div class="action-desc">
          장 초반 CPI 호재로 갭상승 시 차익 매물 소화 과정이 나타날 수 있음. 10시 이후 지지력 확인 후 분할 매수.
        </div>
      </div>
      <div class="action-footer">
        📌 <strong>대응:</strong> 시초가 흥분 금지, 분할 진입
      </div>
    </div>

    <div class="action-card">
      <div>
        <div class="action-badge purple">원칙 2 · 장중 대응</div>
        <div class="action-title">TSMC 가이던스 확인<br>HBM·소부장 선별 압축</div>
        <div class="action-desc">
          오후 3시 TSMC 실적 및 CAPEX 상향 확인 후 HBM4 핵심 장비(한미반도체), 기판(이수페타시스) 등 1등주 집중.
        </div>
      </div>
      <div class="action-footer">
        📌 <strong>대응:</strong> 실질 수혜주 중심 압축
      </div>
    </div>

    <div class="action-card">
      <div>
        <div class="action-badge green">원칙 3 · 포트폴리오</div>
        <div class="action-title">3Q 호실적 가치주 병행<br>5:5 바벨 전략 유지</div>
        <div class="action-desc">
          단일 섹터 쏠림 방지. 3분기 실적 호전이 확정적인 방산, 조선, 전력인프라, 밸류업 금융주를 40~50% 균형 편입.
        </div>
      </div>
      <div class="action-footer">
        📌 <strong>대응:</strong> 성장주 + 방어 가치주 균형
      </div>
    </div>
  </div>

  <div class="banner">
    <div class="banner-text">🛡️ <span>핵심 메시지:</span> 단기 소음 극복하고 실적 가시성이 검증된 1등 주도주를 선점하라</div>
    <div style="font-size: 13px; color: #94a3b8;">valuestocklabs.com</div>
  </div>
</body>
</html>
"""

async def render():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        # 1. 썸네일 (1080x1080)
        page1 = await browser.new_page(viewport={"width": 1080, "height": 1080}, device_scale_factor=2)
        await page1.set_content(thumbnail_html, wait_until="networkidle")
        await page1.screenshot(path=str(OUTPUT_DIR / "thumbnail.png"), type="png")
        print("[완료] thumbnail.png 캡처 완료")
        await page1.close()

        # 2. 본문 1 (1080x720)
        page2 = await browser.new_page(viewport={"width": 1080, "height": 720}, device_scale_factor=2)
        await page2.set_content(body1_html, wait_until="networkidle")
        await page2.screenshot(path=str(OUTPUT_DIR / "body-1.png"), type="png")
        print("[완료] body-1.png 캡처 완료")
        await page2.close()

        # 3. 본문 2 (1080x720)
        page3 = await browser.new_page(viewport={"width": 1080, "height": 720}, device_scale_factor=2)
        await page3.set_content(body2_html, wait_until="networkidle")
        await page3.screenshot(path=str(OUTPUT_DIR / "body-2.png"), type="png")
        print("[완료] body-2.png 캡처 완료")
        await page3.close()

        # 4. 본문 3 (1080x720)
        page4 = await browser.new_page(viewport={"width": 1080, "height": 720}, device_scale_factor=2)
        await page4.set_content(body3_html, wait_until="networkidle")
        await page4.screenshot(path=str(OUTPUT_DIR / "body-3.png"), type="png")
        print("[완료] body-3.png 캡처 완료")
        await page4.close()

        await browser.close()
    print("[성공] 모든 이미지 캡처 완료!")

if __name__ == "__main__":
    asyncio.run(render())
