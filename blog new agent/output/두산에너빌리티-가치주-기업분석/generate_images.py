import asyncio
import os
from pathlib import Path
from playwright.async_api import async_playwright

OUTPUT_DIR = Path(r"c:\Users\immnu\Desktop\Claud\blog new agent\output\두산에너빌리티-가치주-기업분석\images")
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
      background: linear-gradient(135deg, #070b14 0%, #0f172a 45%, #1e1b4b 100%);
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
      background: radial-gradient(circle, rgba(99, 102, 241, 0.35) 0%, transparent 70%);
      filter: blur(70px);
    }
    .glow-2 {
      position: absolute;
      width: 550px;
      height: 550px;
      bottom: -120px;
      left: -120px;
      background: radial-gradient(circle, rgba(14, 165, 233, 0.3) 0%, transparent 70%);
      filter: blur(70px);
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
      gap: 12px;
    }
    .badge {
      font-size: 22px;
      font-weight: 700;
      color: #38bdf8;
      background: rgba(56, 189, 248, 0.12);
      border: 1px solid rgba(56, 189, 248, 0.35);
      padding: 10px 24px;
      border-radius: 9999px;
      letter-spacing: -0.5px;
    }
    .badge-sub {
      font-size: 22px;
      font-weight: 700;
      color: #a855f7;
      background: rgba(168, 85, 247, 0.12);
      border: 1px solid rgba(168, 85, 247, 0.35);
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
      font-size: 64px;
      font-weight: 900;
      line-height: 1.22;
      background: linear-gradient(180deg, #ffffff 0%, #cbd5e1 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      letter-spacing: -2px;
    }
    .highlight {
      background: linear-gradient(90deg, #38bdf8 0%, #818cf8 100%);
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
      color: #38bdf8;
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
      <div class="badge">저평가주식 · 기업분석</div>
      <div class="badge-sub">KOSPI 034020</div>
    </div>
    <div class="title-area">
      <div class="ticker">DOOSAN ENERBILITY</div>
      <h1 class="title">두산에너빌리티<br><span class="highlight">체코 5.6조 원전 & SMR 독점</span></h1>
      <p class="subtitle">수주잔고 26조원 돌파 · AI 전력난 최대 수혜 가치주 분석</p>
    </div>
    <div class="stats-grid">
      <div class="stat-box">
        <span class="stat-label">체코 원전 주기기</span>
        <span class="stat-val" style="color:#38bdf8;">5.6조 원</span>
      </div>
      <div class="stat-box">
        <span class="stat-label">수주잔고(2026)</span>
        <span class="stat-val" style="color:#4ade80;">26조 원+</span>
      </div>
      <div class="stat-box">
        <span class="stat-label">목표주가 컨센서스</span>
        <span class="stat-val" style="color:#f43f5e;">160,000원</span>
      </div>
    </div>
    <div class="footer">valuestocklabs.com · Value Stock Research</div>
  </div>
</body>
</html>"""

# 2. 본문 1: 실적 퀀텀점프 및 수주잔고 인포그래픽 (1200x750)
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
      font-size: 38px;
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
    .kpi-row {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 24px;
      margin-top: 24px;
    }
    .kpi-card {
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 20px;
      padding: 24px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    .kpi-label {
      font-size: 17px;
      color: #94a3b8;
      font-weight: 600;
    }
    .kpi-value {
      font-size: 42px;
      font-weight: 900;
      letter-spacing: -1px;
    }
    .kpi-desc {
      font-size: 15px;
      color: #cbd5e1;
      font-weight: 500;
    }
    .table-card {
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 20px;
      overflow: hidden;
      margin-top: 20px;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      text-align: center;
    }
    th {
      background: rgba(30, 41, 59, 0.6);
      color: #94a3b8;
      font-size: 17px;
      font-weight: 700;
      padding: 16px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    td {
      padding: 16px;
      font-size: 18px;
      font-weight: 600;
      border-bottom: 1px solid rgba(255, 255, 255, 0.05);
      color: #e2e8f0;
    }
    .col-highlight {
      background: rgba(56, 189, 248, 0.08);
      color: #38bdf8;
      font-weight: 800;
    }
    .col-future {
      background: rgba(74, 222, 128, 0.08);
      color: #4ade80;
      font-weight: 800;
    }
    .footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 15px;
      color: #64748b;
      margin-top: 14px;
    }
  </style>
</head>
<body>
  <div class="header">
    <div class="title-group">
      <h2>📊 두산에너빌리티 실적 퀀텀점프 및 수주잔고 추이</h2>
      <p>연결 재무제표 기준 (2023년 ~ 2027년 컨센서스) · 고마진 원전·가스터빈 매출 본격화</p>
    </div>
    <div class="badge">에프앤가이드 컨센서스 종합</div>
  </div>

  <div class="kpi-row">
    <div class="kpi-card" style="border-top: 4px solid #38bdf8;">
      <span class="kpi-label">2026년 예상 매출액</span>
      <span class="kpi-value" style="color: #38bdf8;">18.8조 원</span>
      <span class="kpi-desc">대형 원전 주기기 본격 매출 인식 (+10.5%)</span>
    </div>
    <div class="kpi-card" style="border-top: 4px solid #4ade80;">
      <span class="kpi-label">2026년 예상 영업이익</span>
      <span class="kpi-value" style="color: #4ade80;">1조 2,800억</span>
      <span class="kpi-desc">전년 대비 +67.8% 급증 (영업이익률 6.8%)</span>
    </div>
    <div class="kpi-card" style="border-top: 4px solid #f59e0b;">
      <span class="kpi-label">확보 수주잔고 (2026)</span>
      <span class="kpi-value" style="color: #f59e0b;">26.0조 원</span>
      <span class="kpi-desc">3.5년~4년 치 안정적 고마진 일감 비축</span>
    </div>
  </div>

  <div class="table-card">
    <table>
      <thead>
        <tr>
          <th>구분</th>
          <th>2023 실적</th>
          <th>2024 실적</th>
          <th>2025 실적</th>
          <th style="color: #38bdf8;">2026 전망 (턴어라운드)</th>
          <th style="color: #4ade80;">2027 컨센서스</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td style="font-weight: 700;">매출액</td>
          <td>17조 5,899억</td>
          <td>16조 2,331억</td>
          <td>17조 579억</td>
          <td class="col-highlight">18조 8,500억</td>
          <td class="col-future">20조 5,000억</td>
        </tr>
        <tr>
          <td style="font-weight: 700;">영업이익</td>
          <td>1조 4,673억</td>
          <td>1조 176억</td>
          <td>7,627억</td>
          <td class="col-highlight">1조 2,800억</td>
          <td class="col-future">1조 6,500억</td>
        </tr>
        <tr>
          <td style="font-weight: 700;">수주잔고</td>
          <td>15.8조 원</td>
          <td>18.2조 원</td>
          <td>22.5조 원</td>
          <td class="col-highlight">26.0조 원 돌파</td>
          <td class="col-future">30.0조 원 돌파</td>
        </tr>
      </tbody>
    </table>
  </div>

  <div class="footer">
    <span>출처: 두산에너빌리티 사업보고서, FnGuide, 증권사 리서치 컨센서스</span>
    <span>valuestocklabs.com · 전문 기업분석 인포그래픽</span>
  </div>
</body>
</html>"""

# 3. 본문 2: SMR 3대장 파운드리 공급망 비교 표 (1200x750)
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
      background: #0b0f19;
      font-family: 'Pretendard', sans-serif;
      color: #ffffff;
      padding: 50px 60px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
    }
    .header {
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      border-bottom: 1px solid rgba(255, 255, 255, 0.12);
      padding-bottom: 20px;
    }
    .title-group h2 {
      font-size: 36px;
      font-weight: 800;
      color: #ffffff;
      letter-spacing: -1px;
    }
    .title-group p {
      font-size: 19px;
      color: #94a3b8;
      margin-top: 6px;
    }
    .badge {
      font-size: 17px;
      font-weight: 700;
      color: #a855f7;
      background: rgba(168, 85, 247, 0.15);
      border: 1px solid rgba(168, 85, 247, 0.35);
      padding: 8px 18px;
      border-radius: 8px;
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 22px;
      margin-top: 24px;
    }
    .card {
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 20px;
      padding: 26px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .card-top {
      display: flex;
      flex-direction: column;
      gap: 12px;
    }
    .card-title {
      font-size: 26px;
      font-weight: 800;
      color: #ffffff;
    }
    .tech-tag {
      font-size: 15px;
      font-weight: 700;
      color: #38bdf8;
      background: rgba(56, 189, 248, 0.12);
      padding: 4px 10px;
      border-radius: 6px;
      align-self: flex-start;
    }
    .card-body {
      display: flex;
      flex-direction: column;
      gap: 12px;
      margin-top: 16px;
      font-size: 16px;
      color: #cbd5e1;
      line-height: 1.5;
    }
    .card-item {
      background: rgba(255, 255, 255, 0.03);
      padding: 10px 14px;
      border-radius: 10px;
      border-left: 3px solid #6366f1;
    }
    .card-item strong {
      color: #ffffff;
      display: block;
      margin-bottom: 2px;
      font-size: 15px;
    }
    .bottom-banner {
      background: linear-gradient(90deg, rgba(99, 102, 241, 0.2) 0%, rgba(14, 165, 233, 0.2) 100%);
      border: 1px solid rgba(99, 102, 241, 0.35);
      border-radius: 16px;
      padding: 18px 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 20px;
    }
    .banner-text {
      font-size: 18px;
      font-weight: 700;
      color: #e0e7ff;
    }
    .banner-highlight {
      color: #38bdf8;
      font-weight: 800;
    }
    .footer {
      display: flex;
      justify-content: space-between;
      font-size: 15px;
      color: #64748b;
      margin-top: 14px;
    }
  </style>
</head>
<body>
  <div class="header">
    <div class="title-group">
      <h2>🌐 글로벌 SMR 3대장과 두산에너빌리티 독점 파운드리</h2>
      <p>빅테크 AI 데이터센터 전력난 해소 · 전 세계 톱티어 SMR 설계 기업의 핵심 제작 독점</p>
    </div>
    <div class="badge">원전업계의 TSMC</div>
  </div>

  <div class="grid">
    <!-- X-energy -->
    <div class="card" style="border-top: 4px solid #f59e0b;">
      <div class="card-top">
        <span class="tech-tag" style="color: #f59e0b; background: rgba(245, 158, 11, 0.15);">고온가스로 (HTGR)</span>
        <h3 class="card-title">엑스에너지 (X-energy)</h3>
      </div>
      <div class="card-body">
        <div class="card-item" style="border-left-color: #f59e0b;">
          <strong>빅테크 파트너십</strong>
          아마존(AWS) 5억$ 투자 유치, 5GW 규모 AI 데이터센터 전력망 공급
        </div>
        <div class="card-item" style="border-left-color: #f59e0b;">
          <strong>두산에너빌리티 역할</strong>
          지분 투자 참여 및 핵심 원자로 주단조품·주기기 제작 독점권 확보
        </div>
      </div>
    </div>

    <!-- NuScale Power -->
    <div class="card" style="border-top: 4px solid #38bdf8;">
      <div class="card-top">
        <span class="tech-tag" style="color: #38bdf8; background: rgba(56, 189, 248, 0.15);">경수로형 (PWR SMR)</span>
        <h3 class="card-title">뉴스케일파워 (NuScale)</h3>
      </div>
      <div class="card-body">
        <div class="card-item" style="border-left-color: #38bdf8;">
          <strong>인허가 표준 인증</strong>
          미국 원자력규제위(NRC) 최초 설계 인증 통과한 대표 SMR
        </div>
        <div class="card-item" style="border-left-color: #38bdf8;">
          <strong>두산에너빌리티 역할</strong>
          2019년 전략적 투자, 원자로 모듈(NPM) 시제품 검증 완료 및 본제품 제작
        </div>
      </div>
    </div>

    <!-- TerraPower -->
    <div class="card" style="border-top: 4px solid #10b981;">
      <div class="card-top">
        <span class="tech-tag" style="color: #10b981; background: rgba(16, 185, 129, 0.15);">소듐냉각고속로 (SFR)</span>
        <h3 class="card-title">테라파워 (TerraPower)</h3>
      </div>
      <div class="card-body">
        <div class="card-item" style="border-left-color: #10b981;">
          <strong>설립자 및 프로젝트</strong>
          빌 게이츠 설립, 미국 와이오밍주 나트륨(Natrium) 실증 플랜트
        </div>
        <div class="card-item" style="border-left-color: #10b981;">
          <strong>두산에너빌리티 역할</strong>
          차세대 고온 원자로 주기기 및 핵심 주단조품 공급 계약 체결 완료
        </div>
      </div>
    </div>
  </div>

  <div class="bottom-banner">
    <div class="banner-text">
      🏭 창원 본사 SMR 전용 클러스터: <span class="banner-highlight">연간 20기 이상 대량 양산 설비 완비</span>
    </div>
    <div class="badge" style="background: rgba(255,255,255,0.1); color: #ffffff; border-color: rgba(255,255,255,0.2);">압도적 진입장벽 구축</div>
  </div>

  <div class="footer">
    <span>출처: US NRC, Amazon AWS 뉴스룸, 테라파워 공식 발표, 대신증권</span>
    <span>valuestocklabs.com · SMR 밸류체인 분석</span>
  </div>
</body>
</html>"""

# 4. 본문 3: 미래 3대 성장 엔진 포인트 카드 (1200x750)
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
      background: #080c15;
      font-family: 'Pretendard', sans-serif;
      color: #ffffff;
      padding: 50px 60px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
    }
    .header {
      border-bottom: 1px solid rgba(255, 255, 255, 0.12);
      padding-bottom: 20px;
    }
    .header h2 {
      font-size: 38px;
      font-weight: 800;
      color: #ffffff;
      letter-spacing: -1px;
    }
    .header p {
      font-size: 20px;
      color: #94a3b8;
      margin-top: 6px;
    }
    .pillars-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 24px;
      margin-top: 24px;
    }
    .pillar-card {
      background: rgba(255, 255, 255, 0.035);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 22px;
      padding: 28px 24px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }
    .pillar-num {
      font-size: 18px;
      font-weight: 800;
      padding: 6px 14px;
      border-radius: 9999px;
      align-self: flex-start;
    }
    .pillar-title {
      font-size: 26px;
      font-weight: 800;
      color: #ffffff;
      line-height: 1.3;
    }
    .pillar-list {
      display: flex;
      flex-direction: column;
      gap: 12px;
      font-size: 16px;
      color: #cbd5e1;
      line-height: 1.5;
    }
    .list-item {
      display: flex;
      align-items: flex-start;
      gap: 8px;
    }
    .bullet {
      color: #38bdf8;
      font-weight: 800;
    }
    .footer {
      display: flex;
      justify-content: space-between;
      font-size: 15px;
      color: #64748b;
      margin-top: 14px;
    }
  </style>
</head>
<body>
  <div class="header">
    <h2>🚀 두산에너빌리티 미래 3대 초격차 성장 엔진</h2>
    <p>대형 원전 르네상스 · AI 전력 SMR 파운드리 · 초대형 가스터빈 국산화 독점 생태계</p>
  </div>

  <div class="pillars-grid">
    <!-- Pillar 1 -->
    <div class="pillar-card" style="border-top: 4px solid #38bdf8;">
      <span class="pillar-num" style="background: rgba(56, 189, 248, 0.15); color: #38bdf8;">ENGINE 01</span>
      <h3 class="pillar-title">체코 5.6조 수주 & 대형 원전 르네상스</h3>
      <div class="pillar-list">
        <div class="list-item">
          <span class="bullet">▪</span>
          <span><strong>체코 두코바니 5·6호기</strong>: 팀코리아 5.6조 원 주기기 독점 공급</span>
        </div>
        <div class="list-item">
          <span class="bullet">▪</span>
          <span><strong>두산스코다파워 시너지</strong>: 현지 3,200억 터빈 공급으로 현지화 장악</span>
        </div>
        <div class="list-item">
          <span class="bullet">▪</span>
          <span><strong>동유럽·중동 확장</strong>: 폴란드, 루마니아, UAE 후속 파이프라인 대기</span>
        </div>
      </div>
    </div>

    <!-- Pillar 2 -->
    <div class="pillar-card" style="border-top: 4px solid #a855f7;">
      <span class="pillar-num" style="background: rgba(168, 85, 247, 0.15); color: #a855f7;">ENGINE 02</span>
      <h3 class="pillar-title">글로벌 빅테크 AI SMR 독점 파운드리</h3>
      <div class="pillar-list">
        <div class="list-item">
          <span class="bullet" style="color: #a855f7;">▪</span>
          <span><strong>빅테크 3각 동맹</strong>: 뉴스케일, 엑스에너지(아마존), 테라파워(게이츠)</span>
        </div>
        <div class="list-item">
          <span class="bullet" style="color: #a855f7;">▪</span>
          <span><strong>창원 SMR 클러스터</strong>: 연간 20기 동시 양산 체제 완비</span>
        </div>
        <div class="list-item">
          <span class="bullet" style="color: #a855f7;">▪</span>
          <span><strong>원전업계의 TSMC</strong>: 설계는 미국, 제조는 창원 독점 체계</span>
        </div>
      </div>
    </div>

    <!-- Pillar 3 -->
    <div class="pillar-card" style="border-top: 4px solid #10b981;">
      <span class="pillar-num" style="background: rgba(168, 85, 247, 0.15); color: #10b981;">ENGINE 03</span>
      <h3 class="pillar-title">세계 5번째 H급 가스터빈 & 수소터빈</h3>
      <div class="pillar-list">
        <div class="list-item">
          <span class="bullet" style="color: #10b981;">▪</span>
          <span><strong>380MW 초대형 국산화</strong>: GE·지멘스 과점 타파, 전 세계 5번째 독자 기술</span>
        </div>
        <div class="list-item">
          <span class="bullet" style="color: #10b981;">▪</span>
          <span><strong>국내 복합발전 연쇄 수주</strong>: 보령 신복합, 안동 2호기, 분당 수주</span>
        </div>
        <div class="list-item">
          <span class="bullet" style="color: #10b981;">▪</span>
          <span><strong>2027 수소 전소 상용화</strong>: 고마진 장기 MRO 유지보수 매출 확보</span>
        </div>
      </div>
    </div>
  </div>

  <div class="footer">
    <span>출처: 두산에너빌리티 기술 백서, 한국원자력산업협회</span>
    <span>valuestocklabs.com · 핵심 전략 인포그래픽</span>
  </div>
</body>
</html>"""

# 5. 본문 4: 목표주가 및 3단계 투자 전략 로드맵 (1200x750)
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
      background: #080c15;
      font-family: 'Pretendard', sans-serif;
      color: #ffffff;
      padding: 50px 60px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
    }
    .header {
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      border-bottom: 1px solid rgba(255, 255, 255, 0.12);
      padding-bottom: 20px;
    }
    .header h2 {
      font-size: 36px;
      font-weight: 800;
      color: #ffffff;
      letter-spacing: -1px;
    }
    .header p {
      font-size: 19px;
      color: #94a3b8;
      margin-top: 6px;
    }
    .badge {
      font-size: 17px;
      font-weight: 700;
      color: #f43f5e;
      background: rgba(244, 63, 94, 0.15);
      border: 1px solid rgba(244, 63, 94, 0.35);
      padding: 8px 18px;
      border-radius: 8px;
    }
    .main-content {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 30px;
      margin-top: 24px;
    }
    .box {
      background: rgba(255, 255, 255, 0.035);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 20px;
      padding: 26px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .box-title {
      font-size: 22px;
      font-weight: 700;
      color: #ffffff;
      margin-bottom: 16px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      padding-bottom: 10px;
    }
    .broker-list {
      display: flex;
      flex-direction: column;
      gap: 12px;
    }
    .broker-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 10px 14px;
      background: rgba(255, 255, 255, 0.03);
      border-radius: 10px;
    }
    .broker-name {
      font-size: 17px;
      font-weight: 600;
      color: #e2e8f0;
    }
    .broker-target {
      font-size: 20px;
      font-weight: 800;
      color: #f43f5e;
    }
    .strategy-steps {
      display: flex;
      flex-direction: column;
      gap: 14px;
    }
    .step-card {
      background: rgba(255, 255, 255, 0.03);
      border-left: 4px solid #38bdf8;
      border-radius: 10px;
      padding: 14px 18px;
    }
    .step-header {
      font-size: 17px;
      font-weight: 700;
      color: #38bdf8;
      margin-bottom: 4px;
    }
    .step-desc {
      font-size: 15px;
      color: #cbd5e1;
      line-height: 1.4;
    }
    .footer {
      display: flex;
      justify-content: space-between;
      font-size: 15px;
      color: #64748b;
      margin-top: 14px;
    }
  </style>
</head>
<body>
  <div class="header">
    <div>
      <h2>🎯 증권사 목표주가 및 3단계 가치투자 전략</h2>
      <p>대형 증권사 전원 '매수(BUY)' 의견 일치 · 평균 목표가 144,000원</p>
    </div>
    <div class="badge">Top Pick 추천</div>
  </div>

  <div class="main-content">
    <!-- Left: Broker Targets -->
    <div class="box">
      <div class="box-title">📊 주요 증권사별 목표주가</div>
      <div class="broker-list">
        <div class="broker-row">
          <span class="broker-name">대신증권 (최고치)</span>
          <span class="broker-target">160,000원</span>
        </div>
        <div class="broker-row">
          <span class="broker-name">NH투자증권</span>
          <span class="broker-target">150,000원</span>
        </div>
        <div class="broker-row">
          <span class="broker-name">한국투자증권</span>
          <span class="broker-target">145,000원</span>
        </div>
        <div class="broker-row">
          <span class="broker-name">메리츠증권</span>
          <span class="broker-target">135,000원</span>
        </div>
        <div class="broker-row">
          <span class="broker-name">신한투자증권</span>
          <span class="broker-target">130,000원</span>
        </div>
      </div>
    </div>

    <!-- Right: 3-Step Strategy -->
    <div class="box">
      <div class="box-title">🛣️ 3단계 밸류에이션 투자 로드맵</div>
      <div class="strategy-steps">
        <div class="step-card" style="border-left-color: #38bdf8;">
          <div class="step-header">STEP 1: 밸류에이션 바닥 구간 분할 매수</div>
          <div class="step-desc">현재 7만 원대 주가는 2026E 실적 턴어라운드 진입 초입으로 분할 매수 기회</div>
        </div>
        <div class="step-card" style="border-left-color: #a855f7;">
          <div class="step-header" style="color: #a855f7;">STEP 2: 체코 본계약 및 SMR 초도 출하</div>
          <div class="step-desc">2026년 하반기 체코 원전 매출 인식 본격화 및 아마존 SMR 파운드리 모멘텀</div>
        </div>
        <div class="step-card" style="border-left-color: #4ade80;">
          <div class="step-header" style="color: #4ade80;">STEP 3: 영업익 1.5조 돌파 및 글로벌 리레이팅</div>
          <div class="step-desc">2027~2028년 국산 수소터빈 상용화와 글로벌 SMR 양산 체제 완성</div>
        </div>
      </div>
    </div>
  </div>

  <div class="footer">
    <span>출처: 대신·NH·한투·메리츠·신한 증권사 리포트 종합</span>
    <span>valuestocklabs.com · 투자 전략 다이어그램</span>
  </div>
</body>
</html>"""

render_tasks = [
    ("thumbnail.png", thumbnail_html, 1080, 1080),
    ("body-1.png", body1_html, 1200, 750),
    ("body-2.png", body2_html, 1200, 750),
    ("body-3.png", body3_html, 1200, 750),
    ("body-4.png", body4_html, 1200, 750),
]

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        for filename, html, width, height in render_tasks:
            page = await browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=2)
            await page.set_content(html, wait_until="networkidle")
            out_file = OUTPUT_DIR / filename
            await page.screenshot(path=str(out_file), type="png")
            await page.close()
            print(f"[성공] 생성 완료: {out_file}")
        await browser.close()
    print("모든 이미지 생성 성공!")

if __name__ == "__main__":
    asyncio.run(main())
