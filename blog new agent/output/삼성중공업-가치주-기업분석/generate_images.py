import asyncio
import os
from pathlib import Path
from playwright.async_api import async_playwright

OUTPUT_DIR = Path(r"c:\Users\immnu\Desktop\Claud\blog new agent\output\삼성중공업-가치주-기업분석\images")
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
      background: linear-gradient(135deg, #0b1120 0%, #0f172a 40%, #1e1b4b 100%);
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
      background: radial-gradient(circle, rgba(56, 189, 248, 0.28) 0%, transparent 70%);
      filter: blur(70px);
    }
    .glow-2 {
      position: absolute;
      width: 550px;
      height: 550px;
      bottom: -120px;
      left: -120px;
      background: radial-gradient(circle, rgba(99, 102, 241, 0.25) 0%, transparent 70%);
      filter: blur(70px);
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
      box-shadow: 0 30px 70px rgba(0, 0, 0, 0.6);
      position: relative;
      z-index: 10;
    }
    .badge {
      font-size: 22px;
      font-weight: 700;
      color: #38bdf8;
      background: rgba(56, 189, 248, 0.12);
      border: 1px solid rgba(56, 189, 248, 0.35);
      padding: 12px 30px;
      border-radius: 9999px;
      letter-spacing: 1px;
      display: inline-flex;
      align-items: center;
      gap: 10px;
    }
    .title-box {
      margin: auto 0;
    }
    .title-sub {
      font-size: 32px;
      font-weight: 600;
      color: #94a3b8;
      margin-bottom: 18px;
      letter-spacing: -0.5px;
    }
    .title-main {
      font-size: 58px;
      font-weight: 900;
      line-height: 1.28;
      letter-spacing: -1.5px;
      word-break: keep-all;
      background: linear-gradient(180deg, #ffffff 0%, #f1f5f9 60%, #cbd5e1 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .highlight {
      background: linear-gradient(90deg, #38bdf8 0%, #818cf8 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .desc {
      font-size: 24px;
      font-weight: 400;
      color: #94a3b8;
      margin-top: 24px;
      line-height: 1.5;
    }
    .stats-row {
      display: flex;
      gap: 20px;
      width: 100%;
      justify-content: center;
    }
    .stat-pill {
      background: rgba(15, 23, 42, 0.7);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 20px;
      padding: 16px 28px;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 6px;
    }
    .stat-label {
      font-size: 15px;
      color: #64748b;
      font-weight: 600;
    }
    .stat-val {
      font-size: 22px;
      color: #38bdf8;
      font-weight: 800;
    }
  </style>
</head>
<body>
  <div class="glow-1"></div>
  <div class="glow-2"></div>
  <div class="card">
    <div class="badge">🚢 조선 슈퍼사이클 & 가치투자 분석</div>
    <div class="title-box">
      <div class="title-sub">삼성중공업 (010140)</div>
      <h1 class="title-main">FLNG 글로벌 독점과<br><span class="highlight">2026년 영업이익 1조</span> 돌파</h1>
      <p class="desc">고선가 LNG선 수주잔고 35조원 · 9년 만의 흑자전환 후 퀀텀점프</p>
    </div>
    <div class="stats-row">
      <div class="stat-pill">
        <span class="stat-label">2026(E) 영업이익</span>
        <span class="stat-val">1조 2,500억 (10.2%)</span>
      </div>
      <div class="stat-pill">
        <span class="stat-label">수주잔고</span>
        <span class="stat-val">약 35.5조원</span>
      </div>
      <div class="stat-pill">
        <span class="stat-label">목표주가 컨센서스</span>
        <span class="stat-val">38,500원 (+97%)</span>
      </div>
    </div>
  </div>
</body>
</html>"""

# 2. 본문 1: 실적 성장 추이 (1000x560)
body1_html = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 1000px;
      height: 560px;
      background: #0f172a;
      font-family: 'Pretendard', sans-serif;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      color: #ffffff;
      padding: 44px 50px;
      position: relative;
    }
    .header {
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      border-bottom: 1px solid #334155;
      padding-bottom: 18px;
    }
    .title {
      font-size: 28px;
      font-weight: 800;
      color: #f8fafc;
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .title span {
      font-size: 14px;
      font-weight: 700;
      background: rgba(56, 189, 248, 0.15);
      color: #38bdf8;
      border: 1px solid rgba(56, 189, 248, 0.4);
      padding: 4px 12px;
      border-radius: 6px;
    }
    .subtitle {
      font-size: 15px;
      color: #94a3b8;
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 18px;
      margin: 24px 0;
    }
    .card {
      background: #1e293b;
      border: 1px solid #334155;
      border-radius: 18px;
      padding: 22px 18px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
    }
    .card.highlight-card {
      background: linear-gradient(180deg, rgba(30, 41, 59, 0.9) 0%, rgba(37, 99, 235, 0.2) 100%);
      border: 1px solid #3b82f6;
      box-shadow: 0 10px 25px rgba(59, 130, 246, 0.2);
    }
    .year-tag {
      font-size: 15px;
      font-weight: 700;
      color: #94a3b8;
      margin-bottom: 12px;
    }
    .card.highlight-card .year-tag {
      color: #60a5fa;
    }
    .metric {
      margin-bottom: 12px;
    }
    .metric-label {
      font-size: 13px;
      color: #64748b;
      margin-bottom: 4px;
    }
    .metric-val {
      font-size: 22px;
      font-weight: 800;
      color: #f1f5f9;
    }
    .opm-badge {
      display: inline-block;
      font-size: 13px;
      font-weight: 700;
      padding: 4px 10px;
      border-radius: 8px;
      background: rgba(16, 185, 129, 0.15);
      color: #10b981;
      border: 1px solid rgba(16, 185, 129, 0.3);
    }
    .footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: rgba(30, 41, 59, 0.6);
      border-radius: 12px;
      padding: 14px 22px;
      font-size: 14px;
      color: #94a3b8;
    }
    .footer strong {
      color: #38bdf8;
    }
  </style>
</head>
<body>
  <div class="header">
    <div>
      <div class="title">삼성중공업 실적 퀀텀점프 추이 <span>연결 기준</span></div>
    </div>
    <div class="subtitle">영업이익률 2.9% ➔ 10.2% 두 자릿수 진입</div>
  </div>

  <div class="grid">
    <div class="card">
      <div class="year-tag">2023년 (흑자전환)</div>
      <div class="metric">
        <div class="metric-label">매출액</div>
        <div class="metric-val">8조 94억</div>
      </div>
      <div class="metric">
        <div class="metric-label">영업이익</div>
        <div class="metric-val">2,333억</div>
      </div>
      <div><span class="opm-badge">OPM 2.9%</span></div>
    </div>

    <div class="card">
      <div class="year-tag">2024년 (이익 급증)</div>
      <div class="metric">
        <div class="metric-label">매출액</div>
        <div class="metric-val">9조 9,024억</div>
      </div>
      <div class="metric">
        <div class="metric-label">영업이익</div>
        <div class="metric-val">5,027억</div>
      </div>
      <div><span class="opm-badge">OPM 5.1% (+115%)</span></div>
    </div>

    <div class="card">
      <div class="year-tag">2025년 (전망)</div>
      <div class="metric">
        <div class="metric-label">매출액</div>
        <div class="metric-val">10조 6,500억</div>
      </div>
      <div class="metric">
        <div class="metric-label">영업이익</div>
        <div class="metric-val">8,200억</div>
      </div>
      <div><span class="opm-badge">OPM 7.7% (+63%)</span></div>
    </div>

    <div class="card highlight-card">
      <div class="year-tag">2026년 (1조 클럽)</div>
      <div class="metric">
        <div class="metric-label">매출액</div>
        <div class="metric-val" style="color: #60a5fa;">12조 2,000억</div>
      </div>
      <div class="metric">
        <div class="metric-label">영업이익</div>
        <div class="metric-val" style="color: #38bdf8;">1조 2,500억</div>
      </div>
      <div><span class="opm-badge" style="background: rgba(56, 189, 248, 0.2); color: #38bdf8; border-color: #38bdf8;">OPM 10.2% (+52%)</span></div>
    </div>
  </div>

  <div class="footer">
    <div>💡 <strong>핵심 시사점:</strong> 저가 수주 물량 완전 해소 및 고선가 LNG선 · FLNG 매출 본격화로 이익 폭발</div>
    <div>출처: 에프앤가이드 & 증권사 컨센서스</div>
  </div>
</body>
</html>"""

# 3. 본문 2: FLNG 프로젝트 요약 카드 (1000x560)
body2_html = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 1000px;
      height: 560px;
      background: #0b1120;
      font-family: 'Pretendard', sans-serif;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      color: #ffffff;
      padding: 44px 50px;
    }
    .header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid #1e293b;
      padding-bottom: 16px;
    }
    .title {
      font-size: 28px;
      font-weight: 800;
      color: #f8fafc;
    }
    .highlight-pill {
      background: linear-gradient(90deg, #38bdf8 0%, #818cf8 100%);
      color: #0f172a;
      font-weight: 800;
      font-size: 14px;
      padding: 6px 16px;
      border-radius: 9999px;
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 20px;
      margin: 22px 0;
    }
    .card {
      background: #131d35;
      border: 1px solid #1e293b;
      border-radius: 20px;
      padding: 24px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .card-badge {
      font-size: 13px;
      font-weight: 700;
      color: #38bdf8;
      background: rgba(56, 189, 248, 0.12);
      padding: 4px 10px;
      border-radius: 6px;
      display: inline-block;
      margin-bottom: 12px;
      align-self: flex-start;
    }
    .project-name {
      font-size: 22px;
      font-weight: 800;
      color: #ffffff;
      margin-bottom: 8px;
    }
    .project-scale {
      font-size: 15px;
      color: #94a3b8;
      margin-bottom: 16px;
    }
    .feature-list {
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 8px;
      font-size: 14px;
      color: #cbd5e1;
    }
    .feature-list li {
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .feature-list li::before {
      content: "✔";
      color: #10b981;
      font-weight: 800;
    }
    .footer-bar {
      background: rgba(30, 41, 59, 0.7);
      border: 1px solid #334155;
      border-radius: 12px;
      padding: 14px 22px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 15px;
    }
    .footer-bar span {
      color: #38bdf8;
      font-weight: 700;
    }
  </style>
</head>
<body>
  <div class="header">
    <div class="title">글로벌 FLNG 시장 압도적 독점과 핵심 프로젝트</div>
    <div class="highlight-pill">세계 시장 점유율 1위 (50%+ 독점)</div>
  </div>

  <div class="grid">
    <div class="card">
      <div>
        <span class="card-badge">모잠비크 프로젝트</span>
        <div class="project-name">Coral Norte FLNG</div>
        <div class="project-scale">수주 규모: 약 25억 달러 (약 3.4조원)</div>
      </div>
      <ul class="feature-list">
        <li>2026년 1월 성공적 진수 완료</li>
        <li>1호선(Coral Sul) 검증된 기술력 계승</li>
        <li>연간 350만 톤 LNG 생산 능력</li>
      </ul>
    </div>

    <div class="card">
      <div>
        <span class="card-badge">북미 캐나다 프로젝트</span>
        <div class="project-name">Cedar FLNG</div>
        <div class="project-scale">수주 규모: 약 15억 달러 (컨소시엄)</div>
      </div>
      <ul class="feature-list">
        <li>미국 Black & Veatch 공동 수주</li>
        <li>2026~2027년 매출 집중 반영</li>
        <li>친환경 전력 기반 저탄소 공정</li>
      </ul>
    </div>

    <div class="card">
      <div>
        <span class="card-badge">미국 멕시코만</span>
        <div class="project-name">Delfin FLNG</div>
        <div class="project-scale">수주 규모: 연속 발주 파이프라인</div>
      </div>
      <ul class="feature-list">
        <li>미국 심해 LNG 수출 핵심 설비</li>
        <li>연간 1~2기 양산 체제 완성</li>
        <li>상선 대비 1.5배 높은 고마진율</li>
      </ul>
    </div>
  </div>

  <div class="footer-bar">
    <div>🌊 <strong>FLNG 강점:</strong> 척당 2~4조 원 규모 · 해양플랜트 OPM 10~15% 고수익 구조 확보</div>
    <div>연간 1~2기 <span>연속 건조 슬롯</span> 완비</div>
  </div>
</body>
</html>"""

# 4. 본문 3: 슈퍼사이클 신조선가지수 및 LNG선가 (1000x520)
body3_html = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 1000px;
      height: 520px;
      background: #0f172a;
      font-family: 'Pretendard', sans-serif;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      color: #ffffff;
      padding: 40px 48px;
    }
    .header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid #334155;
      padding-bottom: 16px;
    }
    .title {
      font-size: 26px;
      font-weight: 800;
      color: #f8fafc;
    }
    .badge {
      font-size: 13px;
      font-weight: 700;
      background: rgba(16, 185, 129, 0.15);
      color: #10b981;
      border: 1px solid rgba(16, 185, 129, 0.4);
      padding: 6px 14px;
      border-radius: 9999px;
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 20px;
      margin: 20px 0;
    }
    .metric-box {
      background: #1e293b;
      border: 1px solid #334155;
      border-radius: 18px;
      padding: 24px 20px;
      text-align: center;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .metric-title {
      font-size: 15px;
      color: #94a3b8;
      font-weight: 600;
      margin-bottom: 10px;
    }
    .metric-value {
      font-size: 38px;
      font-weight: 900;
      color: #38bdf8;
      letter-spacing: -1px;
      margin-bottom: 8px;
    }
    .metric-desc {
      font-size: 13px;
      color: #cbd5e1;
      line-height: 1.5;
    }
    .footer {
      background: rgba(30, 41, 59, 0.6);
      border-radius: 12px;
      padding: 14px 20px;
      display: flex;
      justify-content: space-between;
      font-size: 14px;
      color: #94a3b8;
    }
    .footer strong { color: #38bdf8; }
  </style>
</head>
<body>
  <div class="header">
    <div class="title">조선 슈퍼사이클 핵심 지표 분석</div>
    <div class="badge">16년 만의 최고 선가 기록 경신 중</div>
  </div>

  <div class="grid">
    <div class="metric-box">
      <div>
        <div class="metric-title">클락슨 신조선가지수</div>
        <div class="metric-value">186.6<span style="font-size: 20px;">pt</span></div>
      </div>
      <div class="metric-desc">2008년 최고점(191.6pt) 턱밑 추격<br>역대 최고 호황기 재진입</div>
    </div>

    <div class="metric-box">
      <div>
        <div class="metric-title">174k CBM LNG선 선가</div>
        <div class="metric-value">$2.6<span style="font-size: 20px;">억+</span></div>
      </div>
      <div class="metric-desc">척당 3,500억원 돌파<br>사상 최고가 수준 계약 지속</div>
    </div>

    <div class="metric-box">
      <div>
        <div class="metric-title">삼성중공업 수주잔고</div>
        <div class="metric-value">35.5<span style="font-size: 20px;">조원</span></div>
      </div>
      <div class="metric-desc">3.5년 이상의 안정적 일감 확보<br>고선가 물량 비중 70%+</div>
    </div>
  </div>

  <div class="footer">
    <div>⚓ <strong>거제 제3도크 효과:</strong> 연간 15척 이상 연속 건조로 대당 제조원가 대폭 절감</div>
    <div>출처: 클락슨 리서치 & 삼성중공업 공시</div>
  </div>
</body>
</html>"""

# 5. 본문 4: 증권가 컨센서스 및 목표주가 (1000x520)
body4_html = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 1000px;
      height: 520px;
      background: #0b1120;
      font-family: 'Pretendard', sans-serif;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      color: #ffffff;
      padding: 40px 48px;
    }
    .header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid #1e293b;
      padding-bottom: 16px;
    }
    .title {
      font-size: 26px;
      font-weight: 800;
      color: #f8fafc;
    }
    .target-avg {
      font-size: 16px;
      font-weight: 700;
      color: #38bdf8;
      background: rgba(56, 189, 248, 0.12);
      border: 1px solid rgba(56, 189, 248, 0.35);
      padding: 6px 16px;
      border-radius: 9999px;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin: 18px 0;
      font-size: 14px;
    }
    th {
      background: #1e293b;
      color: #94a3b8;
      font-weight: 700;
      padding: 12px 16px;
      text-align: left;
      border-bottom: 1px solid #334155;
    }
    td {
      padding: 14px 16px;
      border-bottom: 1px solid #1e293b;
      color: #cbd5e1;
    }
    tr:hover td {
      background: rgba(30, 41, 59, 0.5);
    }
    .badge-buy {
      background: rgba(16, 185, 129, 0.15);
      color: #10b981;
      font-weight: 700;
      padding: 4px 10px;
      border-radius: 6px;
      display: inline-block;
    }
    .price-top {
      font-size: 16px;
      font-weight: 800;
      color: #38bdf8;
    }
    .footer {
      background: rgba(30, 41, 59, 0.6);
      border-radius: 12px;
      padding: 14px 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 14px;
      color: #94a3b8;
    }
    .footer strong { color: #38bdf8; }
  </style>
</head>
<body>
  <div class="header">
    <div class="title">주요 증권사별 삼성중공업 투자의견 및 목표주가</div>
    <div class="target-avg">평균 목표주가 38,500원 (+97% 상승 여력)</div>
  </div>

  <table>
    <thead>
      <tr>
        <th>증권사</th>
        <th>투자의견</th>
        <th>목표주가</th>
        <th>핵심 투자 포인트</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="font-weight: 700; color: #ffffff;">한국투자증권</td>
        <td><span class="badge-buy">BUY</span></td>
        <td><span class="price-top">44,000원</span></td>
        <td>FLNG 독점력 및 2026년 영업이익 1.3조원 달성 프리미엄</td>
      </tr>
      <tr>
        <td style="font-weight: 700; color: #ffffff;">다올투자증권</td>
        <td><span class="badge-buy">BUY</span></td>
        <td><span class="price-top">41,000원</span></td>
        <td>고선가 LNG선 건조 본격화 · 해양플랜트 OPM 12% 달성</td>
      </tr>
      <tr>
        <td style="font-weight: 700; color: #ffffff;">IBK투자증권</td>
        <td><span class="badge-buy">BUY</span></td>
        <td><span class="price-top">37,000원</span></td>
        <td>헤비테일 잔금 유입에 따른 재무 건전성 및 순현금 전환</td>
      </tr>
      <tr>
        <td style="font-weight: 700; color: #ffffff;">LS증권</td>
        <td><span class="badge-buy">BUY</span></td>
        <td><span class="price-top">32,000원</span></td>
        <td>슈퍼사이클 최선호주로 중장기 실적 우상향 가시성 확보</td>
      </tr>
    </tbody>
  </table>

  <div class="footer">
    <div>📈 <strong>현재가(약 19,500원) 대비:</strong> 밸류에이션 리레이팅 구간 진입 및 매수 적기 분석</div>
    <div>2026년 10월 기준 취합</div>
  </div>
</body>
</html>"""

async def generate_all_images():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        # 1. 썸네일
        page = await browser.new_page(viewport={"width": 1080, "height": 1080}, device_scale_factor=2)
        await page.set_content(thumbnail_html, wait_until="networkidle")
        await page.screenshot(path=str(OUTPUT_DIR / "thumbnail.png"), type="png")
        print("Generated thumbnail.png")
        
        # 2. body-1
        page1 = await browser.new_page(viewport={"width": 1000, "height": 560}, device_scale_factor=2)
        await page1.set_content(body1_html, wait_until="networkidle")
        await page1.screenshot(path=str(OUTPUT_DIR / "body-1.png"), type="png")
        print("Generated body-1.png")
        
        # 3. body-2
        page2 = await browser.new_page(viewport={"width": 1000, "height": 560}, device_scale_factor=2)
        await page2.set_content(body2_html, wait_until="networkidle")
        await page2.screenshot(path=str(OUTPUT_DIR / "body-2.png"), type="png")
        print("Generated body-2.png")
        
        # 4. body-3
        page3 = await browser.new_page(viewport={"width": 1000, "height": 520}, device_scale_factor=2)
        await page3.set_content(body3_html, wait_until="networkidle")
        await page3.screenshot(path=str(OUTPUT_DIR / "body-3.png"), type="png")
        print("Generated body-3.png")

        # 5. body-4
        page4 = await browser.new_page(viewport={"width": 1000, "height": 520}, device_scale_factor=2)
        await page4.set_content(body4_html, wait_until="networkidle")
        await page4.screenshot(path=str(OUTPUT_DIR / "body-4.png"), type="png")
        print("Generated body-4.png")

        await browser.close()
        print("All images generated successfully!")

if __name__ == "__main__":
    asyncio.run(generate_all_images())
