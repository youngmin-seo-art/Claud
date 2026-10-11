import asyncio
import os
from pathlib import Path
from playwright.async_api import async_playwright

OUTPUT_DIR = Path(r"c:\Users\immnu\Desktop\Claud\blog new agent\output\KB금융-가치주-기업분석\images")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 1. 썸네일 HTML (1080x1080)
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
      background: linear-gradient(135deg, #090d16 0%, #0f172a 45%, #1a162b 100%);
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
      right: -150px;
      background: radial-gradient(circle, rgba(245, 158, 11, 0.28) 0%, transparent 70%);
      filter: blur(80px);
    }
    .glow-2 {
      position: absolute;
      width: 600px;
      height: 600px;
      bottom: -150px;
      left: -150px;
      background: radial-gradient(circle, rgba(59, 130, 246, 0.25) 0%, transparent 70%);
      filter: blur(80px);
    }
    .card {
      width: 100%;
      height: 100%;
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 40px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      align-items: center;
      text-align: center;
      padding: 70px 50px;
      backdrop-filter: blur(20px);
      box-shadow: 0 30px 70px rgba(0, 0, 0, 0.65);
      position: relative;
      z-index: 10;
    }
    .badge-wrap {
      display: flex;
      gap: 14px;
    }
    .badge {
      font-size: 22px;
      font-weight: 700;
      color: #fbbf24;
      background: rgba(251, 191, 36, 0.12);
      border: 1px solid rgba(251, 191, 36, 0.35);
      padding: 10px 24px;
      border-radius: 9999px;
      letter-spacing: -0.5px;
    }
    .badge-sub {
      font-size: 22px;
      font-weight: 700;
      color: #38bdf8;
      background: rgba(56, 189, 248, 0.12);
      border: 1px solid rgba(56, 189, 248, 0.35);
      padding: 10px 24px;
      border-radius: 9999px;
    }
    .title-area {
      display: flex;
      flex-direction: column;
      gap: 18px;
    }
    .ticker {
      font-size: 32px;
      font-weight: 800;
      color: #94a3b8;
      letter-spacing: 2px;
    }
    .title {
      font-size: 62px;
      font-weight: 900;
      line-height: 1.22;
      background: linear-gradient(180deg, #ffffff 0%, #e2e8f0 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      letter-spacing: -2px;
    }
    .highlight {
      background: linear-gradient(90deg, #fbbf24 0%, #f59e0b 50%, #38bdf8 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .subtitle {
      font-size: 26px;
      font-weight: 500;
      color: #cbd5e1;
      line-height: 1.5;
      margin-top: 6px;
    }
    .stats-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 20px;
      width: 100%;
    }
    .stat-box {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 20px;
      padding: 22px 16px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    .stat-label {
      font-size: 18px;
      color: #94a3b8;
      font-weight: 600;
    }
    .stat-val {
      font-size: 34px;
      font-weight: 800;
      color: #fbbf24;
    }
    .footer {
      font-size: 20px;
      color: #64748b;
      font-weight: 600;
      letter-spacing: 1px;
    }
  </style>
</head>
<body>
  <div class="glow-1"></div>
  <div class="glow-2"></div>
  <div class="card">
    <div class="badge-wrap">
      <div class="badge">저평가 가치주 · 기업분석</div>
      <div class="badge-sub">KOSPI 105560</div>
    </div>
    <div class="title-area">
      <div class="ticker">KB FINANCIAL GROUP</div>
      <h1 class="title">KB금융 기업분석<br><span class="highlight">순이익 6.5조 & 주주환원 55%</span></h1>
      <p class="subtitle">보통주자본비율 13% 초과 전액 환원 · 비은행 이익 44% 도약</p>
    </div>
    <div class="stats-grid">
      <div class="stat-box">
        <span class="stat-label">2026E 연결순이익</span>
        <span class="stat-val" style="color:#fbbf24;">6.5조 원</span>
      </div>
      <div class="stat-box">
        <span class="stat-label">총 주주환원율</span>
        <span class="stat-val" style="color:#38bdf8;">55.0%+</span>
      </div>
      <div class="stat-box">
        <span class="stat-label">목표주가 컨센서스</span>
        <span class="stat-val" style="color:#4ade80;">215,857원</span>
      </div>
    </div>
    <div class="footer">valuestocklabs.com · Value Stock Research</div>
  </div>
</body>
</html>"""

# 2. 본문 1: 당기순이익 성장 추이 및 비은행 계열사 기여도 (1200x750)
body1_html = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 1200px;
      height: 750px;
      background: #090d16;
      font-family: 'Pretendard', sans-serif;
      color: #ffffff;
      padding: 50px 60px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
      overflow: hidden;
    }
    .header {
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      border-bottom: 1px solid rgba(255, 255, 255, 0.12);
      padding-bottom: 24px;
    }
    .title-group h2 {
      font-size: 36px;
      font-weight: 800;
      color: #ffffff;
      letter-spacing: -1px;
    }
    .title-group p {
      font-size: 20px;
      color: #94a3b8;
      margin-top: 6px;
    }
    .badge {
      font-size: 18px;
      font-weight: 700;
      color: #fbbf24;
      background: rgba(251, 191, 36, 0.12);
      border: 1px solid rgba(251, 191, 36, 0.3);
      padding: 8px 18px;
      border-radius: 8px;
    }
    .content-grid {
      display: grid;
      grid-template-columns: 1.1fr 1fr;
      gap: 32px;
      margin-top: 24px;
      flex: 1;
    }
    .panel {
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 20px;
      padding: 28px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .panel-title {
      font-size: 22px;
      font-weight: 700;
      color: #38bdf8;
      margin-bottom: 16px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .earnings-bars {
      display: flex;
      flex-direction: column;
      gap: 16px;
    }
    .bar-item {
      display: flex;
      flex-direction: column;
      gap: 6px;
    }
    .bar-label-row {
      display: flex;
      justify-content: space-between;
      font-size: 17px;
      font-weight: 600;
      color: #cbd5e1;
    }
    .bar-bg {
      width: 100%;
      height: 24px;
      background: rgba(255, 255, 255, 0.06);
      border-radius: 12px;
      overflow: hidden;
      position: relative;
    }
    .bar-fill {
      height: 100%;
      border-radius: 12px;
    }
    .subsidiary-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 14px;
    }
    .sub-card {
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 14px;
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 4px;
    }
    .sub-name {
      font-size: 16px;
      font-weight: 700;
      color: #fbbf24;
    }
    .sub-metric {
      font-size: 22px;
      font-weight: 800;
      color: #ffffff;
    }
    .sub-desc {
      font-size: 14px;
      color: #94a3b8;
    }
    .footer-note {
      font-size: 16px;
      color: #64748b;
      margin-top: 14px;
      text-align: right;
    }
  </style>
</head>
<body>
  <div class="header">
    <div class="title-group">
      <h2>KB금융 실적 성장 & 비은행 다각화 구조</h2>
      <p>순이익 6.5조 원 시대 진입과 비은행 이익 기여도 44% 도약</p>
    </div>
    <div class="badge">사상 최대 실적 경신</div>
  </div>

  <div class="content-grid">
    <!-- 패널 1: 순이익 성장 추이 -->
    <div class="panel">
      <div>
        <div class="panel-title">📈 연결 당기순이익 성장 추이</div>
        <div class="earnings-bars">
          <div class="bar-item">
            <div class="bar-label-row">
              <span>2024년 (결산)</span>
              <span style="color:#94a3b8;">5조 700억 원</span>
            </div>
            <div class="bar-bg">
              <div class="bar-fill" style="width: 78%; background: linear-gradient(90deg, #64748b, #94a3b8);"></div>
            </div>
          </div>
          <div class="bar-item">
            <div class="bar-label-row">
              <span>2025년 (사상 최대)</span>
              <span style="color:#38bdf8; font-weight:700;">5조 8,400억 원 (+15.1%)</span>
            </div>
            <div class="bar-bg">
              <div class="bar-fill" style="width: 89%; background: linear-gradient(90deg, #0284c7, #38bdf8);"></div>
            </div>
          </div>
          <div class="bar-item">
            <div class="bar-label-row">
              <span>2026년 (연간 전망)</span>
              <span style="color:#fbbf24; font-weight:800;">6조 5,000억 원 (E)</span>
            </div>
            <div class="bar-bg">
              <div class="bar-fill" style="width: 100%; background: linear-gradient(90deg, #d97706, #fbbf24);"></div>
            </div>
          </div>
        </div>
      </div>
      <div style="background: rgba(251,191,36,0.08); border: 1px solid rgba(251,191,36,0.25); border-radius: 12px; padding: 14px 18px; margin-top: 14px;">
        <span style="color:#fbbf24; font-weight:700; font-size:16px;">💡 핵심 포인트: </span>
        <span style="color:#e2e8f0; font-size:15px;">2026 상반기에만 순익 3.88조 원(+13.1%)으로 반기 신기록 경신</span>
      </div>
    </div>

    <!-- 패널 2: 비은행 포트폴리오 기여도 -->
    <div class="panel">
      <div>
        <div class="panel-title">🏛️ 비은행 계열사 포트폴리오 (비중 44%)</div>
        <div class="subsidiary-grid">
          <div class="sub-card">
            <div class="sub-name">KB증권</div>
            <div class="sub-metric">7,963억 원</div>
            <div class="sub-desc">상반기 순익 · ROE 21.04%</div>
          </div>
          <div class="sub-card">
            <div class="sub-name">KB손해보험</div>
            <div class="sub-metric">4,788억 원</div>
            <div class="sub-desc">상반기 순익 · 우수 CSM 잔액</div>
          </div>
          <div class="sub-card">
            <div class="sub-name">KB국민카드</div>
            <div class="sub-metric">안정적 캐시카우</div>
            <div class="sub-desc">플랫폼 결제 수수료 방어</div>
          </div>
          <div class="sub-card">
            <div class="sub-name">KB라이프생명</div>
            <div class="sub-metric">보장성 성장</div>
            <div class="sub-desc">통합 시너지 본격화</div>
          </div>
        </div>
      </div>
      <div style="background: rgba(56,189,248,0.08); border: 1px solid rgba(56,189,248,0.25); border-radius: 12px; padding: 14px 18px; margin-top: 14px;">
        <span style="color:#38bdf8; font-weight:700; font-size:16px;">🛡️ 마진 방어: </span>
        <span style="color:#e2e8f0; font-size:15px;">은행 NIM 하락을 비이자이익·수수료 급증으로 완벽 상쇄</span>
      </div>
    </div>
  </div>

  <div class="footer-note">출처: KB금융 IR 공시 및 증권가 컨센서스 · valuestocklabs.com</div>
</body>
</html>"""

# 3. 본문 2: 3단계 밸류업 주주환원 프레임워크 (1200x750)
body2_html = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 1200px;
      height: 750px;
      background: #090d16;
      font-family: 'Pretendard', sans-serif;
      color: #ffffff;
      padding: 50px 60px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
      overflow: hidden;
    }
    .header {
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      border-bottom: 1px solid rgba(255, 255, 255, 0.12);
      padding-bottom: 24px;
    }
    .title-group h2 {
      font-size: 36px;
      font-weight: 800;
      color: #ffffff;
      letter-spacing: -1px;
    }
    .title-group p {
      font-size: 20px;
      color: #94a3b8;
      margin-top: 6px;
    }
    .badge {
      font-size: 18px;
      font-weight: 700;
      color: #38bdf8;
      background: rgba(56, 189, 248, 0.12);
      border: 1px solid rgba(56, 189, 248, 0.3);
      padding: 8px 18px;
      border-radius: 8px;
    }
    .steps-container {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 24px;
      margin-top: 24px;
    }
    .step-card {
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 20px;
      padding: 30px 24px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
    }
    .step-header {
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 16px;
    }
    .step-num {
      width: 44px;
      height: 44px;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 20px;
      font-weight: 900;
    }
    .step-title {
      font-size: 20px;
      font-weight: 700;
      color: #ffffff;
    }
    .step-desc {
      font-size: 16px;
      color: #cbd5e1;
      line-height: 1.6;
      margin-bottom: 20px;
    }
    .metric-badge {
      background: rgba(255, 255, 255, 0.06);
      border-radius: 12px;
      padding: 14px;
      text-align: center;
    }
    .metric-title {
      font-size: 13px;
      color: #94a3b8;
      font-weight: 600;
    }
    .metric-value {
      font-size: 24px;
      font-weight: 800;
      margin-top: 4px;
    }
    .summary-bar {
      background: linear-gradient(90deg, rgba(251,191,36,0.12) 0%, rgba(56,189,248,0.12) 100%);
      border: 1px solid rgba(251,191,36,0.3);
      border-radius: 18px;
      padding: 20px 30px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 14px;
    }
    .sum-text {
      font-size: 18px;
      font-weight: 700;
      color: #ffffff;
    }
    .sum-highlight {
      font-size: 28px;
      font-weight: 900;
      color: #fbbf24;
    }
    .footer-note {
      font-size: 16px;
      color: #64748b;
      margin-top: 14px;
      text-align: right;
    }
  </style>
</head>
<body>
  <div class="header">
    <div class="title-group">
      <h2>보통주자본비율(CET1) 연계 '3단계 밸류업 프레임워크'</h2>
      <p>국내 최초 밸류업 본공시의 수학적 자본관리 및 복리 환원 공식</p>
    </div>
    <div class="badge">KB표 주주환원 원칙</div>
  </div>

  <div class="steps-container">
    <!-- Step 1 -->
    <div class="step-card">
      <div>
        <div class="step-header">
          <div class="step-num" style="background:rgba(251,191,36,0.2); color:#fbbf24;">01</div>
          <div class="step-title">연말 CET1 13% 초과 환원</div>
        </div>
        <p class="step-desc">
          매 연말 보통주자본비율 13.0%를 초과하는 잉여 자본 전액을 다음 연도 주주환원 재원으로 의무 편성
        </p>
      </div>
      <div class="metric-badge">
        <div class="metric-title">자본 관리 기준선</div>
        <div class="metric-value" style="color:#fbbf24;">CET1 > 13.0%</div>
      </div>
    </div>

    <!-- Step 2 -->
    <div class="step-card">
      <div>
        <div class="step-header">
          <div class="step-num" style="background:rgba(56,189,248,0.2); color:#38bdf8;">02</div>
          <div class="step-title">연중 13.5% 초과시 추가소각</div>
        </div>
        <p class="step-desc">
          반기 결산 기준 13.5% 초과 자본 발생 시 하반기 자사주를 추가 매입하여 전량 영구 소각 집행
        </p>
      </div>
      <div class="metric-badge">
        <div class="metric-title">2026 하반기 추가 소각</div>
        <div class="metric-value" style="color:#38bdf8;">7,000억 원 추가</div>
      </div>
    </div>

    <!-- Step 3 -->
    <div class="step-card">
      <div>
        <div class="step-header">
          <div class="step-num" style="background:rgba(74,222,128,0.2); color:#4ade80;">03</div>
          <div class="step-title">DPS 우상향 복리 마법</div>
        </div>
        <p class="step-desc">
          분기 균등배당 + 연간 1,000만 주 소각으로 총주식수가 감소하여 주당 배당금(DPS) 매년 자동 상승
        </p>
      </div>
      <div class="metric-badge">
        <div class="metric-title">연간 자사주 소각 규모</div>
        <div class="metric-value" style="color:#4ade80;">약 2.1조 원</div>
      </div>
    </div>
  </div>

  <div class="summary-bar">
    <div class="sum-text">🎯 2026년 연간 총 주주환원 패키지</div>
    <div class="sum-highlight">총 3.7조 원 (주주환원율 55.0%+)</div>
  </div>

  <div class="footer-note">출처: KB금융그룹 밸류업 본공시 자료 · valuestocklabs.com</div>
</body>
</html>"""

# 4. 본문 3: 4대 핵심 투자 포인트 및 자본건전성 요약 (1200x750)
body3_html = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 1200px;
      height: 750px;
      background: #090d16;
      font-family: 'Pretendard', sans-serif;
      color: #ffffff;
      padding: 50px 60px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
      overflow: hidden;
    }
    .header {
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      border-bottom: 1px solid rgba(255, 255, 255, 0.12);
      padding-bottom: 24px;
    }
    .title-group h2 {
      font-size: 36px;
      font-weight: 800;
      color: #ffffff;
      letter-spacing: -1px;
    }
    .title-group p {
      font-size: 20px;
      color: #94a3b8;
      margin-top: 6px;
    }
    .badge {
      font-size: 18px;
      font-weight: 700;
      color: #4ade80;
      background: rgba(74, 222, 128, 0.12);
      border: 1px solid rgba(74, 222, 128, 0.3);
      padding: 8px 18px;
      border-radius: 8px;
    }
    .grid-container {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 24px;
      margin-top: 24px;
      flex: 1;
    }
    .card {
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 20px;
      padding: 24px 28px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .card-top {
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 10px;
    }
    .card-icon {
      font-size: 28px;
    }
    .card-title {
      font-size: 22px;
      font-weight: 700;
      color: #ffffff;
    }
    .card-body {
      font-size: 16px;
      color: #cbd5e1;
      line-height: 1.6;
    }
    .card-highlight {
      margin-top: 14px;
      padding: 10px 16px;
      background: rgba(255, 255, 255, 0.05);
      border-radius: 12px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .tag-name {
      font-size: 15px;
      color: #94a3b8;
      font-weight: 600;
    }
    .tag-val {
      font-size: 22px;
      font-weight: 800;
    }
    .footer-note {
      font-size: 16px;
      color: #64748b;
      margin-top: 14px;
      text-align: right;
    }
  </style>
</head>
<body>
  <div class="header">
    <div class="title-group">
      <h2>KB금융 4대 핵심 투자 포인트 및 자본건전성</h2>
      <p>밸류업 대장주의 안정성과 성장 모멘텀 한눈에 보기</p>
    </div>
    <div class="badge">투자 핵심 체크</div>
  </div>

  <div class="grid-container">
    <!-- Card 1 -->
    <div class="card">
      <div>
        <div class="card-top">
          <span class="card-icon">🚀</span>
          <span class="card-title">사상 최대 실적 & ROE 10%</span>
        </div>
        <p class="card-body">
          2026년 순이익 6.5조 원 돌파 예상. 비은행 이익 기여도 44%와 안정적 NIM 관리로 자본 효율성 글로벌 수준 도달.
        </p>
      </div>
      <div class="card-highlight">
        <span class="tag-name">2026E 자기자본이익률</span>
        <span class="tag-val" style="color:#fbbf24;">ROE 10.2%</span>
      </div>
    </div>

    <!-- Card 2 -->
    <div class="card">
      <div>
        <div class="card-top">
          <span class="card-icon">🎁</span>
          <span class="card-title">주주환원율 55% & 자사주 소각</span>
        </div>
        <p class="card-body">
          연간 3.7조 원의 주주환원. 매년 1천만 주 이상의 자사주 영구 소각으로 BPS 및 주당 배당금(DPS)의 구조적 레벨업.
        </p>
      </div>
      <div class="card-highlight">
        <span class="tag-name">총 주주환원율 목표</span>
        <span class="tag-val" style="color:#38bdf8;">55.0% 달성</span>
      </div>
    </div>

    <!-- Card 3 -->
    <div class="card">
      <div>
        <div class="card-top">
          <span class="card-icon">🛡️</span>
          <span class="card-title">클린 밸런스시트 & 리스크 완충</span>
        </div>
        <p class="card-body">
          대손충당금전입비율(CCR) 0.39%로 전년비 15bp 개선. 선제적 충당금 확보와 PF 부실 정리로 대손비용 하향 안정화.
        </p>
      </div>
      <div class="card-highlight">
        <span class="tag-name">대손충당금전입비율 (CCR)</span>
        <span class="tag-val" style="color:#4ade80;">0.39% (안정)</span>
      </div>
    </div>

    <!-- Card 4 -->
    <div class="card">
      <div>
        <div class="card-top">
          <span class="card-icon">📈</span>
          <span class="card-title">PBR 0.75배 탈피와 리레이팅</span>
        </div>
        <p class="card-body">
          과거 PBR 0.3~0.4배 만년 저평가 구간 탈피. 글로벌 선진 은행(0.9~1.1배) 수준으로 기업가치 재평가 지속 진행 중.
        </p>
      </div>
      <div class="card-highlight">
        <span class="tag-name">적정 PBR 목표치</span>
        <span class="tag-val" style="color:#f43f5e;">0.90배 수렴</span>
      </div>
    </div>
  </div>

  <div class="footer-note">출처: KB금융 IR 및 애널리스트 리포트 종합 · valuestocklabs.com</div>
</body>
</html>"""

# 5. 본문 4: 증권사별 목표주가 및 투자의견 컨센서스 (1200x750)
body4_html = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 1200px;
      height: 750px;
      background: #090d16;
      font-family: 'Pretendard', sans-serif;
      color: #ffffff;
      padding: 50px 60px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
      overflow: hidden;
    }
    .header {
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      border-bottom: 1px solid rgba(255, 255, 255, 0.12);
      padding-bottom: 24px;
    }
    .title-group h2 {
      font-size: 36px;
      font-weight: 800;
      color: #ffffff;
      letter-spacing: -1px;
    }
    .title-group p {
      font-size: 20px;
      color: #94a3b8;
      margin-top: 6px;
    }
    .badge {
      font-size: 18px;
      font-weight: 700;
      color: #fbbf24;
      background: rgba(251, 191, 36, 0.12);
      border: 1px solid rgba(251, 191, 36, 0.3);
      padding: 8px 18px;
      border-radius: 8px;
    }
    .broker-list {
      display: flex;
      flex-direction: column;
      gap: 12px;
      margin-top: 20px;
    }
    .broker-row {
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 14px;
      padding: 14px 22px;
      display: grid;
      grid-template-columns: 140px 100px 160px 1fr;
      align-items: center;
      gap: 16px;
    }
    .broker-name {
      font-size: 19px;
      font-weight: 700;
      color: #ffffff;
    }
    .opinion {
      font-size: 15px;
      font-weight: 800;
      color: #4ade80;
      background: rgba(74, 222, 128, 0.12);
      border: 1px solid rgba(74, 222, 128, 0.3);
      padding: 4px 10px;
      border-radius: 6px;
      text-align: center;
      width: fit-content;
    }
    .target-price {
      font-size: 24px;
      font-weight: 900;
      color: #fbbf24;
    }
    .broker-comment {
      font-size: 16px;
      color: #cbd5e1;
    }
    .consensus-box {
      background: linear-gradient(90deg, rgba(251,191,36,0.12) 0%, rgba(56,189,248,0.12) 100%);
      border: 1px solid rgba(251,191,36,0.3);
      border-radius: 16px;
      padding: 18px 28px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 14px;
    }
    .con-label {
      font-size: 18px;
      font-weight: 700;
      color: #ffffff;
    }
    .con-values {
      display: flex;
      gap: 24px;
      align-items: center;
    }
    .con-target {
      font-size: 28px;
      font-weight: 900;
      color: #fbbf24;
    }
    .con-upside {
      font-size: 20px;
      font-weight: 800;
      color: #38bdf8;
      background: rgba(56,189,248,0.12);
      padding: 6px 14px;
      border-radius: 8px;
    }
    .footer-note {
      font-size: 16px;
      color: #64748b;
      margin-top: 10px;
      text-align: right;
    }
  </style>
</head>
<body>
  <div class="header">
    <div class="title-group">
      <h2>주요 증권사별 KB금융 목표주가 및 투자의견</h2>
      <p>금융업종 부동의 원픽(Top Pick) · 일제히 '매수(BUY)' 의견 제시</p>
    </div>
    <div class="badge">컨센서스 종합</div>
  </div>

  <div class="broker-list">
    <div class="broker-row">
      <div class="broker-name">하나증권</div>
      <div class="opinion">BUY</div>
      <div class="target-price">235,000원</div>
      <div class="broker-comment">국내 금융주 최초 밸류업 본공시 정착, 목표 PBR 0.9배 상향 타당</div>
    </div>
    <div class="broker-row">
      <div class="broker-name">키움증권</div>
      <div class="opinion">BUY</div>
      <div class="target-price">230,000원</div>
      <div class="broker-comment">CET1 13.74% 돌파로 총주주환원율 55% 달성 확실, 압도적 톱픽</div>
    </div>
    <div class="broker-row">
      <div class="broker-name">한국투자증권</div>
      <div class="opinion">BUY</div>
      <div class="target-price">225,000원</div>
      <div class="broker-comment">비은행 이익 비중 44%로 이익 체질 개선, 금리 인하기 최적 대안</div>
    </div>
    <div class="broker-row">
      <div class="broker-name">NH투자증권</div>
      <div class="opinion">BUY</div>
      <div class="target-price">220,000원</div>
      <div class="broker-comment">연간 3.7조 원 규모 주주환원, 연간 1천만 주 소각으로 DPS 복리 상승</div>
    </div>
    <div class="broker-row">
      <div class="broker-name">메리츠증권</div>
      <div class="opinion">BUY</div>
      <div class="target-price">210,000원</div>
      <div class="broker-comment">CCR 0.39%로 대손비용 하향 안정화, 2026년 순이익 6.5조 원 기대</div>
    </div>
  </div>

  <div class="consensus-box">
    <div class="con-label">📊 증권가 컨센서스 평균 (현재가 162,800원 대비)</div>
    <div class="con-values">
      <div class="con-target">215,857원</div>
      <div class="con-upside">+32.6% 상승 여력</div>
    </div>
  </div>

  <div class="footer-note">출처: 와이즈리포트 및 주요 증권사 최신 리포트 · valuestocklabs.com</div>
</body>
</html>"""

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        # 1. 썸네일 (1080x1080)
        page = await browser.new_page(viewport={"width": 1080, "height": 1080}, device_scale_factor=2)
        await page.set_content(thumbnail_html, wait_until="networkidle")
        await page.screenshot(path=str(OUTPUT_DIR / "thumbnail.png"))
        print("[완료] thumbnail.png")
        await page.close()

        # 2. 본문 1 (1200x750)
        page = await browser.new_page(viewport={"width": 1200, "height": 750}, device_scale_factor=2)
        await page.set_content(body1_html, wait_until="networkidle")
        await page.screenshot(path=str(OUTPUT_DIR / "body-1.png"))
        print("[완료] body-1.png")
        await page.close()

        # 3. 본문 2 (1200x750)
        page = await browser.new_page(viewport={"width": 1200, "height": 750}, device_scale_factor=2)
        await page.set_content(body2_html, wait_until="networkidle")
        await page.screenshot(path=str(OUTPUT_DIR / "body-2.png"))
        print("[완료] body-2.png")
        await page.close()

        # 4. 본문 3 (1200x750)
        page = await browser.new_page(viewport={"width": 1200, "height": 750}, device_scale_factor=2)
        await page.set_content(body3_html, wait_until="networkidle")
        await page.screenshot(path=str(OUTPUT_DIR / "body-3.png"))
        print("[완료] body-3.png")
        await page.close()

        # 5. 본문 4 (1200x750)
        page = await browser.new_page(viewport={"width": 1200, "height": 750}, device_scale_factor=2)
        await page.set_content(body4_html, wait_until="networkidle")
        await page.screenshot(path=str(OUTPUT_DIR / "body-4.png"))
        print("[완료] body-4.png")
        await page.close()

        await browser.close()
        print("모든 이미지 생성 완료!")

if __name__ == "__main__":
    asyncio.run(main())
