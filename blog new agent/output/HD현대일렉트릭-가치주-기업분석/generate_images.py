import asyncio
import os
from pathlib import Path
from playwright.async_api import async_playwright

OUTPUT_DIR = Path(r"c:\Users\immnu\Desktop\Claud\blog new agent\output\HD현대일렉트릭-가치주-기업분석\images")
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
      background: linear-gradient(135deg, #0b0f19 0%, #111827 50%, #1e1b4b 100%);
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
      width: 500px;
      height: 500px;
      top: -100px;
      right: -100px;
      background: radial-gradient(circle, rgba(99, 102, 241, 0.25) 0%, transparent 70%);
      filter: blur(60px);
    }
    .glow-2 {
      position: absolute;
      width: 500px;
      height: 500px;
      bottom: -100px;
      left: -100px;
      background: radial-gradient(circle, rgba(16, 185, 129, 0.2) 0%, transparent 70%);
      filter: blur(60px);
    }
    .card {
      width: 100%;
      height: 100%;
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 36px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      align-items: center;
      text-align: center;
      padding: 70px 50px;
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
      letter-spacing: 1px;
      display: inline-flex;
      align-items: center;
      gap: 8px;
    }
    .title-box {
      margin: auto 0;
    }
    .title-sub {
      font-size: 32px;
      font-weight: 600;
      color: #94a3b8;
      margin-bottom: 16px;
      letter-spacing: -0.5px;
    }
    .title-main {
      font-size: 58px;
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
    .footer-stats {
      width: 100%;
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 20px;
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 20px;
      padding: 22px 20px;
    }
    .stat-item {
      display: flex;
      flex-direction: column;
      gap: 6px;
    }
    .stat-label {
      font-size: 16px;
      color: #94a3b8;
      font-weight: 500;
    }
    .stat-val {
      font-size: 26px;
      font-weight: 800;
      color: #38bdf8;
    }
    .stat-val.green { color: #34d399; }
    .stat-val.purple { color: #a78bfa; }
  </style>
</head>
<body>
  <div class="glow-1"></div>
  <div class="glow-2"></div>
  <div class="card">
    <div class="badge">⚡ 저평가 우량주 · 기업 심층분석</div>
    <div class="title-box">
      <div class="title-sub">AI 전력망 슈퍼사이클 대장주</div>
      <h1 class="title-main">HD현대일렉트릭<br><span class="highlight">4대 해자 & 저평가 가치</span> 분석</h1>
    </div>
    <div class="footer-stats">
      <div class="stat-item">
        <span class="stat-label">2026(E) 영업이익률</span>
        <span class="stat-val green">25.5% (1위)</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">수주잔고 규모</span>
        <span class="stat-val">약 11~12조 원</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">PEG 지수</span>
        <span class="stat-val purple">0.75배 (저평가)</span>
      </div>
    </div>
  </div>
</body>
</html>"""

# 2. Body-1: 4대 핵심 경제적 해자 (1080x700)
body_1_html = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 1080px;
      height: 700px;
      background: #0f172a;
      font-family: 'Pretendard', sans-serif;
      padding: 44px;
      color: #ffffff;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .header {
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      border-bottom: 2px solid #1e293b;
      padding-bottom: 16px;
    }
    .header-title {
      font-size: 28px;
      font-weight: 800;
      color: #f8fafc;
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .header-sub {
      font-size: 15px;
      color: #94a3b8;
      font-weight: 500;
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 20px;
      margin-top: 20px;
    }
    .card {
      background: rgba(30, 41, 59, 0.7);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 18px;
      padding: 24px 26px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      position: relative;
    }
    .card-num {
      position: absolute;
      top: 20px;
      right: 24px;
      font-size: 20px;
      font-weight: 900;
      color: rgba(255, 255, 255, 0.15);
    }
    .card-badge {
      display: inline-block;
      align-self: flex-start;
      font-size: 13px;
      font-weight: 700;
      padding: 5px 12px;
      border-radius: 6px;
    }
    .b-blue { background: rgba(56, 189, 248, 0.15); color: #38bdf8; }
    .b-green { background: rgba(52, 211, 153, 0.15); color: #34d399; }
    .b-purple { background: rgba(167, 139, 250, 0.15); color: #a78bfa; }
    .b-orange { background: rgba(251, 146, 60, 0.15); color: #fb923c; }
    .card-title {
      font-size: 20px;
      font-weight: 800;
      color: #ffffff;
      margin-top: 2px;
    }
    .card-desc {
      font-size: 14.5px;
      color: #cbd5e1;
      line-height: 1.6;
      word-break: keep-all;
    }
    .card-tag {
      font-size: 13px;
      font-weight: 600;
      color: #94a3b8;
      border-top: 1px dashed rgba(255, 255, 255, 0.1);
      padding-top: 10px;
      margin-top: 4px;
    }
  </style>
</head>
<body>
  <div class="header">
    <div>
      <div class="header-title">🛡️ HD현대일렉트릭의 4대 핵심 경제적 해자</div>
      <div class="header-sub">글로벌 전력망 슈퍼사이클을 주도하는 압도적 진입장벽</div>
    </div>
    <div style="font-size: 14px; color: #38bdf8; font-weight: 700;">ValueStockLabs Insights</div>
  </div>

  <div class="grid">
    <div class="card" style="border-left: 4px solid #38bdf8;">
      <span class="card-num">01</span>
      <span class="card-badge b-blue">기술 및 인증 장벽</span>
      <h3 class="card-title">765kV 초고압 변압기 & UL 인증</h3>
      <p class="card-desc">광역 정전을 방지하는 고도의 절연 기술과 수십 년 무사고 Track Record 요구. 미국 유틸리티 공급 가능 기업 극소수 독점.</p>
      <div class="card-tag">✅ 글로벌 톱티어 품질 승인 획득</div>
    </div>

    <div class="card" style="border-left: 4px solid #34d399;">
      <span class="card-num">02</span>
      <span class="card-badge b-green">북미 현지화 인프라</span>
      <h3 class="card-title">미국 앨라배마(HPT) 제2공장 증설</h3>
      <p class="card-desc">2억 달러(약 2,900억 원) 투자로 2027년까지 북미 CAPA 50% 확장. '바이 아메리칸' 정책 및 관세 리스크 완벽 방어.</p>
      <div class="card-tag">✅ 연간 2,000억 원 추가 매출 창출</div>
    </div>

    <div class="card" style="border-left: 4px solid #a78bfa;">
      <span class="card-num">03</span>
      <span class="card-badge b-purple">공급자 우위 시장</span>
      <h3 class="card-title">3~4년 리드타임 & 강력한 가격결정권</h3>
      <p class="card-desc">수주잔고 11~12조 원 확보로 2028년 슬롯 마감. 원자재가 상승분 100% 에스컬레이션 전가 및 고마진 선별 수주 체제.</p>
      <div class="card-tag">✅ 영업이익률 25% 돌파의 원동력</div>
    </div>

    <div class="card" style="border-left: 4px solid #fb923c;">
      <span class="card-num">04</span>
      <span class="card-badge b-orange">빅테크 턴키 락인</span>
      <h3 class="card-title">글로벌 하이퍼스케일러 직거래 계약</h3>
      <p class="card-desc">빅테크와 1.1조 원 규모 직거래 패키지 계약 체결. 데이터센터 특고압 수전부터 배전기기까지 일괄 공급해 락인 효과 극대화.</p>
      <div class="card-tag">✅ 데이터센터 수주 비중 1.8% ➔ 16% 급증</div>
    </div>
  </div>
</body>
</html>"""

# 3. Body-2: 국내 전력기기 3사 비교 차트 (1080x700)
body_2_html = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 1080px;
      height: 700px;
      background: #0f172a;
      font-family: 'Pretendard', sans-serif;
      padding: 44px;
      color: #ffffff;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .header {
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      border-bottom: 2px solid #1e293b;
      padding-bottom: 16px;
    }
    .header-title {
      font-size: 28px;
      font-weight: 800;
      color: #f8fafc;
    }
    .header-sub {
      font-size: 15px;
      color: #94a3b8;
      font-weight: 500;
    }
    .compare-container {
      display: grid;
      grid-template-columns: 1.2fr 1fr 1fr;
      gap: 18px;
      margin-top: 20px;
    }
    .peer-card {
      background: rgba(30, 41, 59, 0.6);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 18px;
      padding: 24px 20px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }
    .peer-card.highlight {
      background: linear-gradient(180deg, rgba(37, 99, 235, 0.2) 0%, rgba(15, 23, 42, 0.8) 100%);
      border: 2px solid #38bdf8;
      box-shadow: 0 10px 30px rgba(56, 189, 248, 0.15);
    }
    .peer-badge {
      font-size: 12px;
      font-weight: 700;
      padding: 4px 10px;
      border-radius: 9999px;
      align-self: flex-start;
    }
    .peer-name {
      font-size: 22px;
      font-weight: 800;
      color: #ffffff;
    }
    .metric-row {
      display: flex;
      flex-direction: column;
      gap: 4px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.06);
      padding-bottom: 10px;
    }
    .metric-label {
      font-size: 13px;
      color: #94a3b8;
    }
    .metric-val {
      font-size: 20px;
      font-weight: 800;
      color: #e2e8f0;
    }
    .metric-val.green { color: #34d399; }
    .metric-val.blue { color: #38bdf8; }
    .bar-wrap {
      width: 100%;
      height: 8px;
      background: #334155;
      border-radius: 4px;
      overflow: hidden;
      margin-top: 4px;
    }
    .bar-fill {
      height: 100%;
      border-radius: 4px;
    }
  </style>
</head>
<body>
  <div class="header">
    <div>
      <div class="header-title">📊 국내 전력기기 3사 핵심 역량 및 수익성 비교</div>
      <div class="header-sub">2026년 상반기 기준 영업이익률 · 수주잔고 · 북미 비중 대조</div>
    </div>
    <div style="font-size: 14px; color: #34d399; font-weight: 700;">2026 최신 공시 기준</div>
  </div>

  <div class="compare-container">
    <!-- HD현대일렉트릭 -->
    <div class="peer-card highlight">
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <span class="peer-badge" style="background: #38bdf8; color: #0f172a;">수익성 1위 대장주</span>
        <span style="font-size: 13px; color: #38bdf8; font-weight: 700;">KOSPI 267260</span>
      </div>
      <div class="peer-name">HD현대일렉트릭</div>
      
      <div class="metric-row">
        <span class="metric-label">2026 Q2 영업이익률 (OPM)</span>
        <span class="metric-val green">25.1% (업계 최고)</span>
        <div class="bar-wrap"><div class="bar-fill" style="width: 100%; background: #34d399;"></div></div>
      </div>

      <div class="metric-row">
        <span class="metric-label">수주잔고 규모</span>
        <span class="metric-val blue">약 11~12조 원 (84.9억$)</span>
      </div>

      <div class="metric-row">
        <span class="metric-label">북미 매출 비중</span>
        <span class="metric-val">약 65~70%</span>
      </div>

      <div class="metric-row" style="border-bottom: none;">
        <span class="metric-label">사업 포트폴리오</span>
        <span style="font-size: 14px; color: #cbd5e1; font-weight: 600;">100% 순수 전력·배전기기</span>
      </div>
    </div>

    <!-- 효성중공업 -->
    <div class="peer-card">
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <span class="peer-badge" style="background: rgba(255,255,255,0.1); color: #94a3b8;">수주잔고 1위</span>
        <span style="font-size: 13px; color: #64748b;">KOSPI 298040</span>
      </div>
      <div class="peer-name">효성중공업</div>
      
      <div class="metric-row">
        <span class="metric-label">2026 Q2 영업이익률 (OPM)</span>
        <span class="metric-val">약 18~20% (중공업)</span>
        <div class="bar-wrap"><div class="bar-fill" style="width: 78%; background: #60a5fa;"></div></div>
      </div>

      <div class="metric-row">
        <span class="metric-label">수주잔고 규모</span>
        <span class="metric-val">약 17.5조 원</span>
      </div>

      <div class="metric-row">
        <span class="metric-label">북미 매출 비중</span>
        <span class="metric-val">약 35~40%</span>
      </div>

      <div class="metric-row" style="border-bottom: none;">
        <span class="metric-label">사업 포트폴리오</span>
        <span style="font-size: 14px; color: #94a3b8;">중공업 + 건설사업 혼합</span>
      </div>
    </div>

    <!-- LS ELECTRIC -->
    <div class="peer-card">
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <span class="peer-badge" style="background: rgba(255,255,255,0.1); color: #94a3b8;">배전 솔루션 1위</span>
        <span style="font-size: 13px; color: #64748b;">KOSPI 010120</span>
      </div>
      <div class="peer-name">LS ELECTRIC</div>
      
      <div class="metric-row">
        <span class="metric-label">2026 Q2 영업이익률 (OPM)</span>
        <span class="metric-val">11.3%</span>
        <div class="bar-wrap"><div class="bar-fill" style="width: 45%; background: #94a3b8;"></div></div>
      </div>

      <div class="metric-row">
        <span class="metric-label">수주잔고 규모</span>
        <span class="metric-val">약 7.0조 원</span>
      </div>

      <div class="metric-row">
        <span class="metric-label">북미 매출 비중</span>
        <span class="metric-val">약 25~30%</span>
      </div>

      <div class="metric-row" style="border-bottom: none;">
        <span class="metric-label">사업 포트폴리오</span>
        <span style="font-size: 14px; color: #94a3b8;">배전 솔루션 + 스마트팩토리</span>
      </div>
    </div>
  </div>
</body>
</html>"""

# 4. Body-3: 전력 슈퍼사이클 3대 모멘텀 흐름도 (1080x700)
body_3_html = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 1080px;
      height: 700px;
      background: #0f172a;
      font-family: 'Pretendard', sans-serif;
      padding: 44px;
      color: #ffffff;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .header {
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      border-bottom: 2px solid #1e293b;
      padding-bottom: 16px;
    }
    .header-title {
      font-size: 28px;
      font-weight: 800;
      color: #f8fafc;
    }
    .header-sub {
      font-size: 15px;
      color: #94a3b8;
      font-weight: 500;
    }
    .flow-container {
      display: flex;
      flex-direction: column;
      gap: 16px;
      margin-top: 16px;
    }
    .flow-row {
      display: grid;
      grid-template-columns: 1fr 1fr 1fr;
      gap: 16px;
    }
    .flow-card {
      background: rgba(30, 41, 59, 0.7);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 16px;
      padding: 20px 22px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    .flow-card.c1 { border-top: 4px solid #38bdf8; }
    .flow-card.c2 { border-top: 4px solid #a78bfa; }
    .flow-card.c3 { border-top: 4px solid #34d399; }
    .card-head {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 18px;
      font-weight: 800;
      color: #ffffff;
    }
    .card-text {
      font-size: 14px;
      color: #cbd5e1;
      line-height: 1.55;
    }
    .highlight-pill {
      display: inline-block;
      font-size: 12px;
      font-weight: 700;
      color: #38bdf8;
      background: rgba(56, 189, 248, 0.12);
      padding: 3px 8px;
      border-radius: 4px;
      margin-top: 4px;
    }
    .result-banner {
      background: linear-gradient(90deg, rgba(79, 70, 229, 0.25) 0%, rgba(16, 185, 129, 0.2) 100%);
      border: 1px solid rgba(99, 102, 241, 0.4);
      border-radius: 16px;
      padding: 20px 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .banner-text {
      display: flex;
      flex-direction: column;
      gap: 4px;
    }
    .banner-title {
      font-size: 18px;
      font-weight: 800;
      color: #ffffff;
    }
    .banner-desc {
      font-size: 14px;
      color: #cbd5e1;
    }
    .banner-stat {
      text-align: right;
    }
    .b-stat-val {
      font-size: 26px;
      font-weight: 900;
      color: #34d399;
    }
  </style>
</head>
<body>
  <div class="header">
    <div>
      <div class="header-title">⚡ 글로벌 전력 인프라 3대 슈퍼사이클 모멘텀</div>
      <div class="header-sub">2030년까지 이어지는 구조적 초과수요와 공급 병목 구조</div>
    </div>
    <div style="font-size: 14px; color: #a78bfa; font-weight: 700;">Supercycle 2024-2030</div>
  </div>

  <div class="flow-container">
    <div class="flow-row">
      <div class="flow-card c1">
        <div class="card-head">⚡ 1. 미국 노후망 교체</div>
        <p class="card-text">미국 변압기 70% 이상이 25년 이상 노후화(수명 한계). IIJA 예산 수천억 달러 집행 중.</p>
        <span class="highlight-pill">인프라법 & 송전망 현대화</span>
      </div>

      <div class="flow-card c2">
        <div class="card-head">🤖 2. AI 데이터센터 폭증</div>
        <p class="card-text">하이퍼스케일러 데이터센터 전력 소비 2배 급증. GW급 데이터센터 직결 초고압 변압기 필수.</p>
        <span class="highlight-pill" style="color: #a78bfa; background: rgba(167, 139, 250, 0.12);">빅테크 직거래 패키지 수주</span>
      </div>

      <div class="flow-card c3">
        <div class="card-head">🌱 3. 신재생 계통 연계</div>
        <p class="card-text">태양광·풍력 장거리 송전 연계 및 전기차 충전망 등 산업 전반의 전기화(Electrification).</p>
        <span class="highlight-pill" style="color: #34d399; background: rgba(52, 211, 153, 0.12);">초고압 HVDC 송전망 확대</span>
      </div>
    </div>

    <div class="result-banner">
      <div class="banner-text">
        <div class="banner-title">🚀 결과: 공급자 우위(Seller's Market) & 판가 상승세 지속</div>
        <div class="banner-desc">신규 진입장벽이 높고 증설에 최소 2~3년 소요되어 공급 쇼티지 장기화 확정</div>
      </div>
      <div class="banner-stat">
        <div style="font-size: 13px; color: #94a3b8;">초고압 변압기 리드타임</div>
        <div class="b-stat-val">3~4년 (최대 48개월)</div>
      </div>
    </div>
  </div>
</body>
</html>"""

# 5. Body-4: 2023-2026 실적 퀀텀점프 및 밸류에이션 (1080x700)
body_4_html = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 1080px;
      height: 700px;
      background: #0f172a;
      font-family: 'Pretendard', sans-serif;
      padding: 44px;
      color: #ffffff;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .header {
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      border-bottom: 2px solid #1e293b;
      padding-bottom: 16px;
    }
    .header-title {
      font-size: 28px;
      font-weight: 800;
      color: #f8fafc;
    }
    .header-sub {
      font-size: 15px;
      color: #94a3b8;
      font-weight: 500;
    }
    .metrics-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
      margin-top: 16px;
    }
    .stat-card {
      background: rgba(30, 41, 59, 0.7);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 16px;
      padding: 22px 18px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    .stat-card.main {
      border: 1px solid #38bdf8;
      background: linear-gradient(180deg, rgba(56, 189, 248, 0.15) 0%, rgba(30, 41, 59, 0.8) 100%);
    }
    .s-label { font-size: 14px; color: #94a3b8; font-weight: 500; }
    .s-val { font-size: 28px; font-weight: 900; color: #ffffff; }
    .s-val.green { color: #34d399; }
    .s-val.blue { color: #38bdf8; }
    .s-val.purple { color: #a78bfa; }
    .s-growth { font-size: 13px; font-weight: 700; color: #38bdf8; }
    
    .val-banner {
      background: rgba(15, 23, 42, 0.9);
      border: 1px solid #6366f1;
      border-radius: 16px;
      padding: 22px 26px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 16px;
    }
    .val-box {
      display: flex;
      flex-direction: column;
      gap: 4px;
    }
    .val-title { font-size: 19px; font-weight: 800; color: #ffffff; }
    .val-desc { font-size: 14px; color: #cbd5e1; line-height: 1.5; }
    .peg-badge {
      background: rgba(99, 102, 241, 0.2);
      border: 2px solid #818cf8;
      padding: 12px 22px;
      border-radius: 14px;
      text-align: center;
    }
    .peg-val { font-size: 28px; font-weight: 900; color: #a78bfa; }
    .peg-sub { font-size: 12px; color: #c7d2fe; font-weight: 600; }
  </style>
</head>
<body>
  <div class="header">
    <div>
      <div class="header-title">📈 HD현대일렉트릭 2023-2026 실적 퀀텀점프</div>
      <div class="header-sub">연결 재무제표 기준 3개년 턴어라운드 및 밸류에이션 지표</div>
    </div>
    <div style="font-size: 14px; color: #38bdf8; font-weight: 700;">Financials & Valuation</div>
  </div>

  <div class="metrics-grid">
    <div class="stat-card">
      <span class="s-label">2026(E) 매출액</span>
      <span class="s-val blue">4조 7,500억</span>
      <span class="s-growth">▲ +76% (vs 2023)</span>
    </div>

    <div class="stat-card main">
      <span class="s-label">2026(E) 영업이익</span>
      <span class="s-val green">1조 2,100억</span>
      <span class="s-growth" style="color: #34d399;">▲ +284% (4배 폭증)</span>
    </div>

    <div class="stat-card">
      <span class="s-label">2026(E) 영업이익률</span>
      <span class="s-val green">25.5%</span>
      <span class="s-growth" style="color: #34d399;">제조업 최고 마진</span>
    </div>

    <div class="stat-card">
      <span class="s-label">ROE / 부채비율</span>
      <span class="s-val purple">35.2%</span>
      <span class="s-growth" style="color: #a78bfa;">부채비율 105% 건전</span>
    </div>
  </div>

  <div class="val-banner">
    <div class="val-box">
      <div class="val-title">💡 가치주 관점의 투자 결론: 실질 PEG 0.75배 저평가</div>
      <div class="val-desc">EPS 연평균 성장률(CAGR 45%+) 대비 주가 배수는 여전히 매력적인 성장가치주 구간.<br>미국 Eaton(PER 38배) 대비 OPM과 성장률 모두 앞서며 KOSPI 디스카운트 해소 진행 중.</div>
    </div>
    <div class="peg-badge">
      <div class="peg-val">0.75배</div>
      <div class="peg-sub">피터 린치 저평가 기준 충족</div>
    </div>
  </div>
</body>
</html>"""

async def main():
    items = [
        ("thumbnail.png", thumbnail_html, 1080, 1080),
        ("body-1.png", body_1_html, 1080, 700),
        ("body-2.png", body_2_html, 1080, 700),
        ("body-3.png", body_3_html, 1080, 700),
        ("body-4.png", body_4_html, 1080, 700),
    ]
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        for filename, html, w, h in items:
            page = await browser.new_page(viewport={"width": w, "height": h}, device_scale_factor=2)
            await page.set_content(html, wait_until="networkidle")
            out_file = OUTPUT_DIR / filename
            await page.screenshot(path=str(out_file), type="png")
            await page.close()
            print(f"Generated: {out_file}")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
