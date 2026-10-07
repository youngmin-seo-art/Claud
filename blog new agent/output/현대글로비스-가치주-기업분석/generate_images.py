import asyncio
import os
from pathlib import Path
from playwright.async_api import async_playwright

OUTPUT_DIR = Path(r"c:\Users\immnu\Desktop\Claud\blog new agent\output\현대글로비스-가치주-기업분석\images")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 1. 대표 썸네일 HTML (1080x1080)
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
      background: linear-gradient(135deg, #070b14 0%, #0d1527 50%, #161e38 100%);
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
      width: 550px;
      height: 550px;
      top: -120px;
      right: -120px;
      background: radial-gradient(circle, rgba(56, 189, 248, 0.3) 0%, transparent 70%);
      filter: blur(70px);
    }
    .glow-2 {
      position: absolute;
      width: 550px;
      height: 550px;
      bottom: -120px;
      left: -120px;
      background: radial-gradient(circle, rgba(99, 102, 241, 0.3) 0%, transparent 70%);
      filter: blur(70px);
    }
    .card {
      width: 100%;
      height: 100%;
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 36px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      align-items: center;
      text-align: center;
      padding: 65px 45px;
      backdrop-filter: blur(16px);
      box-shadow: 0 25px 60px rgba(0, 0, 0, 0.6);
      position: relative;
      z-index: 10;
    }
    .badge {
      font-size: 22px;
      font-weight: 700;
      color: #38bdf8;
      background: rgba(56, 189, 248, 0.12);
      border: 1px solid rgba(56, 189, 248, 0.35);
      padding: 12px 28px;
      border-radius: 9999px;
      letter-spacing: 0.5px;
      display: inline-flex;
      align-items: center;
      gap: 10px;
    }
    .badge .dot {
      width: 10px;
      height: 10px;
      border-radius: 50%;
      background: #38bdf8;
      box-shadow: 0 0 10px #38bdf8;
    }
    .title-box {
      margin: auto 0;
    }
    .title-sub {
      font-size: 28px;
      font-weight: 600;
      color: #94a3b8;
      margin-bottom: 16px;
      letter-spacing: -0.5px;
    }
    .title-main {
      font-size: 56px;
      font-weight: 900;
      line-height: 1.28;
      letter-spacing: -1.5px;
      word-break: keep-all;
      background: linear-gradient(180deg, #ffffff 0%, #e2e8f0 70%, #94a3b8 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .highlight {
      background: linear-gradient(90deg, #38bdf8 0%, #818cf8 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .stats-row {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 20px;
      width: 100%;
    }
    .stat-card {
      background: rgba(15, 23, 42, 0.65);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 20px;
      padding: 22px 16px;
      text-align: center;
    }
    .stat-label {
      font-size: 16px;
      color: #94a3b8;
      margin-bottom: 8px;
      font-weight: 500;
    }
    .stat-value {
      font-size: 28px;
      font-weight: 800;
      color: #38bdf8;
      letter-spacing: -0.5px;
    }
    .stat-value.orange { color: #fb923c; }
    .stat-value.green { color: #34d399; }
    .footer-tag {
      margin-top: 15px;
      font-size: 15px;
      color: #64748b;
      letter-spacing: 0.5px;
    }
  </style>
</head>
<body>
  <div class="glow-1"></div>
  <div class="glow-2"></div>
  <div class="card">
    <div class="badge">
      <span class="dot"></span>
      VALUESTOCKLABS · K-물류·해운 대장주 심층분석
    </div>
    <div class="title-box">
      <div class="title-sub">086280 · 사상 첫 영업익 2조 돌파</div>
      <h1 class="title-main">현대글로비스<br><span class="highlight">주가 전망 & 밸류에이션</span></h1>
    </div>
    <div class="stats-row">
      <div class="stat-card">
        <div class="stat-label">해운 비계열 비중</div>
        <div class="stat-value orange">53%+ 돌파</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">2026(F) 예상 매출</div>
        <div class="stat-value">31.5조 원</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">2026(F) 예상 PER</div>
        <div class="stat-value green">8.5~9.5배</div>
      </div>
    </div>
    <div class="footer-tag">PCTC 선복 쇼티지 · 보스턴다이내믹스 지분 12.5% · 배당성향 25%+ · 지배구조 핵심</div>
  </div>
</body>
</html>
"""

# 2. 본문 1: 4대 핵심 성장 엔진 카드 (1080x640)
body_1_html = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 1080px;
      height: 640px;
      background: #0b0f19;
      font-family: 'Pretendard', sans-serif;
      padding: 36px 40px;
      color: #ffffff;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
      padding-bottom: 14px;
    }
    .header h2 {
      font-size: 25px;
      font-weight: 800;
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .tag {
      font-size: 13.5px;
      font-weight: 600;
      background: rgba(56, 189, 248, 0.15);
      color: #38bdf8;
      border: 1px solid rgba(56, 189, 248, 0.35);
      padding: 5px 14px;
      border-radius: 9999px;
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 16px;
      margin-top: 14px;
      flex: 1;
    }
    .pillar-card {
      background: rgba(15, 23, 42, 0.7);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 18px;
      padding: 20px 22px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
      overflow: hidden;
    }
    .pillar-card::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      width: 4px;
      height: 100%;
      background: #38bdf8;
    }
    .pillar-card.card-2::before { background: #34d399; }
    .pillar-card.card-3::before { background: #818cf8; }
    .pillar-card.card-4::before { background: #fb923c; }

    .card-top {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 8px;
    }
    .card-num {
      font-size: 12px;
      font-weight: 800;
      color: #64748b;
      letter-spacing: 1px;
    }
    .card-badge {
      font-size: 12px;
      font-weight: 700;
      padding: 3px 10px;
      border-radius: 6px;
    }
    .badge-blue { background: rgba(56, 189, 248, 0.15); color: #38bdf8; }
    .badge-green { background: rgba(52, 211, 153, 0.15); color: #34d399; }
    .badge-purple { background: rgba(129, 140, 248, 0.15); color: #818cf8; }
    .badge-orange { background: rgba(251, 146, 60, 0.15); color: #fb923c; }

    .card-title {
      font-size: 19px;
      font-weight: 800;
      color: #ffffff;
      margin-bottom: 6px;
      letter-spacing: -0.3px;
    }
    .card-desc {
      font-size: 13.5px;
      color: #94a3b8;
      line-height: 1.5;
    }
    .card-stat {
      margin-top: 10px;
      padding-top: 8px;
      border-top: 1px solid rgba(255, 255, 255, 0.06);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .stat-desc { font-size: 12px; color: #64748b; }
    .stat-bold { font-size: 15px; font-weight: 800; color: #38bdf8; }
    .stat-bold.green { color: #34d399; }
    .stat-bold.purple { color: #818cf8; }
    .stat-bold.orange { color: #fb923c; }
  </style>
</head>
<body>
  <div class="header">
    <h2>🚀 현대글로비스 4대 핵심 성장 엔진 & 리레이팅 포인트</h2>
    <span class="tag">글로벌 종합 SCM 대전환</span>
  </div>

  <div class="grid">
    <!-- 카드 1 -->
    <div class="pillar-card card-1">
      <div>
        <div class="card-top">
          <span class="card-num">PILLAR 01</span>
          <span class="card-badge badge-blue">해운 부문 수익 극대화</span>
        </div>
        <h3 class="card-title">PCTC 선복 쇼티지 & 비계열 53%+</h3>
        <p class="card-desc">글로벌 완성차 운반선 공급 부족 장기화. 중국 전기차 수출 급증 수혜로 고단가 비계열 수주 확대.</p>
      </div>
      <div class="card-stat">
        <span class="stat-desc">선대 확충 목표</span>
        <span class="stat-bold">2030년 128척 (10,800 CEU)</span>
      </div>
    </div>

    <!-- 카드 2 -->
    <div class="pillar-card card-2">
      <div>
        <div class="card-top">
          <span class="card-num">PILLAR 02</span>
          <span class="card-badge badge-green">신성장 동력</span>
        </div>
        <h3 class="card-title">보스턴다이내믹스 로보틱스 시너지</h3>
        <p class="card-desc">지분 12.5% 보유. 하역 로봇 스트레치 및 아틀라스 물류센터 실전 배치, 향후 나스닥 IPO 지분가치 2조 기대.</p>
      </div>
      <div class="card-stat">
        <span class="stat-desc">물류 자동화 솔루션</span>
        <span class="stat-bold green">스마트 풀필먼트 SCM 선도</span>
      </div>
    </div>

    <!-- 카드 3 -->
    <div class="pillar-card card-3">
      <div>
        <div class="card-top">
          <span class="card-num">PILLAR 03</span>
          <span class="card-badge badge-purple">중장기 비전</span>
        </div>
        <h3 class="card-title">CEO 인베스터 데이 2030 가이던스</h3>
        <p class="card-desc">2030년 매출 40조 원+ 및 OPM 7% 목표. 9조 원 CAPEX로 물류 인프라, 신조선, 배터리 재활용 집중 투자.</p>
      </div>
      <div class="card-stat">
        <span class="stat-desc">목표 수익성</span>
        <span class="stat-bold purple">ROE 15%+ 지속 유지</span>
      </div>
    </div>

    <!-- 카드 4 -->
    <div class="pillar-card card-4">
      <div>
        <div class="card-top">
          <span class="card-num">PILLAR 04</span>
          <span class="card-badge badge-orange">주주환원 & 지배구조</span>
        </div>
        <h3 class="card-title">배당성향 25%+ & 정의선 지분 20%</h3>
        <p class="card-desc">매년 DPS 최소 5% 상향 보장. 정의선 회장의 경영권 승계 핵심 재원 역할로 대주주-소액주주 이해관계 일치.</p>
      </div>
      <div class="card-stat">
        <span class="stat-desc">주주친화 정책</span>
        <span class="stat-bold orange">2025 밸류업 우수기업 선정</span>
      </div>
    </div>
  </div>
</body>
</html>
"""

# 3. 본문 2: 2024~2027년 실적 추이 바 차트 및 지표 (1080x640)
body_2_html = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 1080px;
      height: 640px;
      background: #0b0f19;
      font-family: 'Pretendard', sans-serif;
      padding: 38px 40px;
      color: #ffffff;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
      padding-bottom: 14px;
    }
    .header h2 {
      font-size: 25px;
      font-weight: 800;
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .tag {
      font-size: 13.5px;
      font-weight: 600;
      background: rgba(16, 185, 129, 0.15);
      color: #34d399;
      border: 1px solid rgba(16, 185, 129, 0.35);
      padding: 5px 14px;
      border-radius: 9999px;
    }
    .chart-container {
      display: grid;
      grid-template-columns: 1.4fr 1fr;
      gap: 24px;
      margin-top: 14px;
      flex: 1;
    }
    .bars-card {
      background: rgba(15, 23, 42, 0.7);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 20px;
      padding: 18px 22px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .bars-title {
      font-size: 15px;
      font-weight: 700;
      color: #94a3b8;
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 6px;
    }
    .bar-group {
      display: flex;
      flex-direction: column;
      gap: 9px;
    }
    .year-row {
      display: flex;
      flex-direction: column;
      gap: 4px;
      background: rgba(0, 0, 0, 0.2);
      padding: 8px 12px;
      border-radius: 10px;
      border: 1px solid rgba(255, 255, 255, 0.03);
    }
    .year-row.active {
      border-color: rgba(56, 189, 248, 0.35);
      background: rgba(14, 165, 233, 0.06);
    }
    .year-label {
      display: flex;
      justify-content: space-between;
      font-size: 13px;
      font-weight: 700;
      color: #e2e8f0;
    }
    .bar-wrapper {
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .bar-name {
      font-size: 11px;
      color: #94a3b8;
      width: 38px;
    }
    .bar-track {
      flex: 1;
      height: 15px;
      background: rgba(255, 255, 255, 0.05);
      border-radius: 5px;
      overflow: hidden;
      display: flex;
    }
    .bar-fill-sales {
      height: 100%;
      background: linear-gradient(90deg, #0284c7 0%, #38bdf8 100%);
      border-radius: 5px;
    }
    .bar-fill-op {
      height: 100%;
      background: linear-gradient(90deg, #059669 0%, #34d399 100%);
      border-radius: 5px;
    }
    .bar-val-text {
      font-size: 12px;
      font-weight: 700;
      color: #e2e8f0;
      min-width: 75px;
      text-align: right;
    }
    .bar-val-text.green { color: #34d399; }
    .bar-val-text.blue { color: #38bdf8; }
    .metrics-card {
      display: flex;
      flex-direction: column;
      gap: 10px;
      justify-content: center;
    }
    .metric-box {
      background: rgba(15, 23, 42, 0.7);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 14px;
      padding: 13px 18px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .metric-box.highlight {
      border-color: rgba(56, 189, 248, 0.4);
      background: linear-gradient(135deg, rgba(56, 189, 248, 0.1) 0%, rgba(15, 23, 42, 0.8) 100%);
    }
    .metric-name {
      font-size: 13px;
      color: #94a3b8;
    }
    .metric-val {
      font-size: 20px;
      font-weight: 800;
      color: #ffffff;
    }
    .metric-val.green { color: #34d399; }
    .metric-val.blue { color: #38bdf8; }
    .metric-val.orange { color: #fb923c; }
    .legend {
      display: flex;
      gap: 12px;
      font-size: 12px;
      color: #94a3b8;
    }
    .legend-item {
      display: flex;
      align-items: center;
      gap: 5px;
    }
    .legend-dot {
      width: 9px;
      height: 9px;
      border-radius: 3px;
    }
  </style>
</head>
<body>
  <div class="header">
    <h2>📈 2024~2027년 실적 추이 및 폭발적 수익성 지표</h2>
    <span class="tag">영업이익 2조 클럽 안착</span>
  </div>

  <div class="chart-container">
    <!-- 바 차트 -->
    <div class="bars-card">
      <div class="bars-title">
        <span>연간 매출액 및 영업이익 추이</span>
        <div class="legend">
          <div class="legend-item"><span class="legend-dot" style="background:#38bdf8;"></span> 매출</div>
          <div class="legend-item"><span class="legend-dot" style="background:#34d399;"></span> 영업익</div>
        </div>
      </div>

      <div class="bar-group">
        <!-- 2024 -->
        <div class="year-row">
          <div class="year-label">
            <span>2024 (A) 실적</span>
            <span style="color:#94a3b8; font-size:11.5px;">OPM 6.2%</span>
          </div>
          <div class="bar-wrapper">
            <span class="bar-name">매출</span>
            <div class="bar-track"><div class="bar-fill-sales" style="width: 84%;"></div></div>
            <span class="bar-val-text blue">28.5조 원</span>
          </div>
          <div class="bar-wrapper">
            <span class="bar-name">영익</span>
            <div class="bar-track"><div class="bar-fill-op" style="width: 75%;"></div></div>
            <span class="bar-val-text green">1.75조 원</span>
          </div>
        </div>

        <!-- 2025 -->
        <div class="year-row">
          <div class="year-label">
            <span>2025 (A) 실적</span>
            <span style="color:#34d399; font-size:11.5px; font-weight:700;">OPM 7.0% (사상 최대)</span>
          </div>
          <div class="bar-wrapper">
            <span class="bar-name">매출</span>
            <div class="bar-track"><div class="bar-fill-sales" style="width: 87%;"></div></div>
            <span class="bar-val-text blue">29.6조 원</span>
          </div>
          <div class="bar-wrapper">
            <span class="bar-name">영익</span>
            <div class="bar-track"><div class="bar-fill-op" style="width: 89%;"></div></div>
            <span class="bar-val-text green">2.07조 원</span>
          </div>
        </div>

        <!-- 2026 -->
        <div class="year-row active">
          <div class="year-label">
            <span style="color:#38bdf8;">2026 (F) 컨센서스</span>
            <span style="color:#34d399; font-size:11.5px; font-weight:800;">OPM 6.8%</span>
          </div>
          <div class="bar-wrapper">
            <span class="bar-name" style="color:#38bdf8; font-weight:700;">매출</span>
            <div class="bar-track"><div class="bar-fill-sales" style="width: 93%;"></div></div>
            <span class="bar-val-text blue">31.5조 원</span>
          </div>
          <div class="bar-wrapper">
            <span class="bar-name" style="color:#34d399; font-weight:700;">영익</span>
            <div class="bar-track"><div class="bar-fill-op" style="width: 93%;"></div></div>
            <span class="bar-val-text green">2.15조 원</span>
          </div>
        </div>

        <!-- 2027 -->
        <div class="year-row">
          <div class="year-label">
            <span>2027 (F) 중장기 전망</span>
            <span style="color:#94a3b8; font-size:11.5px;">신조선 대거 인도</span>
          </div>
          <div class="bar-wrapper">
            <span class="bar-name">매출</span>
            <div class="bar-track"><div class="bar-fill-sales" style="width: 100%;"></div></div>
            <span class="bar-val-text blue">33.8조 원</span>
          </div>
          <div class="bar-wrapper">
            <span class="bar-name">영익</span>
            <div class="bar-track"><div class="bar-fill-op" style="width: 100%;"></div></div>
            <span class="bar-val-text green">2.32조 원</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 핵심 재무 지표 카드 -->
    <div class="metrics-card">
      <div class="metric-box highlight">
        <div>
          <div class="metric-name">2026(F) 예상 PER</div>
          <div style="font-size:11px; color:#64748b;">글로벌 피어 평균 13~16배</div>
        </div>
        <div class="metric-val green">8.5~9.5배</div>
      </div>

      <div class="metric-box">
        <div>
          <div class="metric-name">자기자본이익률 (ROE)</div>
          <div style="font-size:11px; color:#64748b;">견고한 자본 효율성</div>
        </div>
        <div class="metric-val blue">15.2%</div>
      </div>

      <div class="metric-box">
        <div>
          <div class="metric-name">증권사 평균 목표주가</div>
          <div style="font-size:11px; color:#64748b;">상승여력 +45% 수준</div>
        </div>
        <div class="metric-val orange">320,000원</div>
      </div>
    </div>
  </div>
</body>
</html>
"""

# 4. 본문 3: 주주환원 배당 정책 & 지배구조 수혜 분석 카드 (1080x640)
body_3_html = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 1080px;
      height: 640px;
      background: #0b0f19;
      font-family: 'Pretendard', sans-serif;
      padding: 38px 40px;
      color: #ffffff;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
      padding-bottom: 14px;
    }
    .header h2 {
      font-size: 25px;
      font-weight: 800;
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .tag {
      font-size: 13.5px;
      font-weight: 600;
      background: rgba(251, 146, 60, 0.15);
      color: #fb923c;
      border: 1px solid rgba(251, 146, 60, 0.35);
      padding: 5px 14px;
      border-radius: 9999px;
    }
    .content-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
      margin-top: 14px;
      flex: 1;
    }
    .section-card {
      background: rgba(15, 23, 42, 0.7);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 20px;
      padding: 22px 24px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .card-head {
      display: flex;
      align-items: center;
      gap: 10px;
      margin-bottom: 14px;
    }
    .card-head h3 {
      font-size: 19px;
      font-weight: 800;
      color: #ffffff;
    }
    .item-list {
      display: flex;
      flex-direction: column;
      gap: 12px;
    }
    .item-row {
      background: rgba(0, 0, 0, 0.25);
      border: 1px solid rgba(255, 255, 255, 0.04);
      border-radius: 12px;
      padding: 12px 14px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .item-label {
      font-size: 13.5px;
      color: #94a3b8;
      font-weight: 500;
    }
    .item-value {
      font-size: 15px;
      font-weight: 800;
      color: #38bdf8;
    }
    .item-value.green { color: #34d399; }
    .item-value.orange { color: #fb923c; }
    .bottom-box {
      margin-top: 10px;
      background: rgba(56, 189, 248, 0.08);
      border: 1px solid rgba(56, 189, 248, 0.25);
      border-radius: 12px;
      padding: 12px 14px;
      font-size: 12.5px;
      color: #cbd5e1;
      line-height: 1.45;
    }
    .bottom-box.gold {
      background: rgba(251, 146, 60, 0.08);
      border-color: rgba(251, 146, 60, 0.25);
    }
  </style>
</head>
<body>
  <div class="header">
    <h2>💎 주주환원 밸류업 & 지배구조 개편 핵심 수혜</h2>
    <span class="tag">대주주-소액주주 이해 일치</span>
  </div>

  <div class="content-grid">
    <!-- 주주환원 카드 -->
    <div class="section-card">
      <div>
        <div class="card-head">
          <span style="font-size:22px;">🎁</span>
          <h3>3개년 주주환원 정책 (2025~2027)</h3>
        </div>
        <div class="item-list">
          <div class="item-row">
            <span class="item-label">연결 배당성향 기준</span>
            <span class="item-value green">지배순익 25% 이상</span>
          </div>
          <div class="item-row">
            <span class="item-label">주당 배당금 (DPS)</span>
            <span class="item-value green">매년 최소 5%↑ 상향</span>
          </div>
          <div class="item-row">
            <span class="item-label">100% 무상증자 완료</span>
            <span class="item-value">유통 주식수 2배 확대</span>
          </div>
        </div>
      </div>
      <div class="bottom-box">
        💡 <strong>밸류업 우수기업 선정:</strong> 실적 성장과 연동된 고배당 및 주주친화 경영으로 배당수익률 3.5% 수준 보장.
      </div>
    </div>

    <!-- 지배구조 카드 -->
    <div class="section-card">
      <div>
        <div class="card-head">
          <span style="font-size:22px;">👑</span>
          <h3>현대차그룹 지배구조 핵심 자산</h3>
        </div>
        <div class="item-list">
          <div class="item-row">
            <span class="item-label">정의선 회장 보유 지분</span>
            <span class="item-value orange">19.99% (핵심 최대주주)</span>
          </div>
          <div class="item-row">
            <span class="item-label">현대모비스 지분 확보</span>
            <span class="item-value orange">경영권 승계 핵심 재원</span>
          </div>
          <div class="item-row">
            <span class="item-label">기업가치 부양 유인</span>
            <span class="item-value green">100% 일치 (Win-Win)</span>
          </div>
        </div>
      </div>
      <div class="bottom-box gold">
        💡 <strong>지배구조 프리미엄:</strong> 총수 일가 최대 지분 상장사로서 배당 확대 및 주가 부양이 지배구조상 절대적으로 필요.
      </div>
    </div>
  </div>
</body>
</html>
"""

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        items = [
            ("thumbnail.png", thumbnail_html, 1080, 1080),
            ("body-1.png", body_1_html, 1080, 640),
            ("body-2.png", body_2_html, 1080, 640),
            ("body-3.png", body_3_html, 1080, 640),
        ]
        
        for filename, html, width, height in items:
            page = await browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=2)
            await page.set_content(html, wait_until="networkidle")
            out_path = OUTPUT_DIR / filename
            await page.screenshot(path=str(out_path), type="png")
            await page.close()
            print(f"[생성 완료] {filename} ({width}x{height})")
            
        await browser.close()
        print("모든 이미지 생성 완료!")

if __name__ == "__main__":
    asyncio.run(main())
