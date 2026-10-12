import asyncio
import os
import sys
from pathlib import Path
from playwright.async_api import async_playwright

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

OUTPUT_DIR = Path(r"c:\Users\immnu\Desktop\Claud\blog new agent\output\기아-가치주-기업분석\images")
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
      font-size: 54px;
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
      VALUESTOCKLABS · 글로벌 완성차 탑티어 가치주 분석
    </div>
    <div class="title-box">
      <div class="title-sub">000270 · 2년 연속 매출 100조 원 안착</div>
      <h1 class="title-main">기아 주가 전망 & 밸류에이션<br><span class="highlight">PER 5배 · 6% 고배당 · PBV</span></h1>
    </div>
    <div class="stats-row">
      <div class="stat-card">
        <div class="stat-label">2026(F) 예상 매출</div>
        <div class="stat-value orange">125조~128조 원</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">밸류에이션 매력</div>
        <div class="stat-value">PER 5.2배 / PBR 0.7배</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">시가배당 & 자사주</div>
        <div class="stat-value green">6.0% (TSR 35%)</div>
      </div>
    </div>
    <div class="footer-tag">화성 EVO 플랜트(연 25만대) · PV5/PV7 전용 PBV · 대중화 EV3/EV4 · 조지아 HMGMA 가동</div>
  </div>
 </body>
</html>
"""

# 2. 본문 1: 기아 vs 글로벌 완성차 밸류에이션 및 실적 비교 (1080x640)
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
      font-size: 24px;
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
    .table-container {
      margin-top: 18px;
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      text-align: center;
      background: rgba(15, 23, 42, 0.7);
      border-radius: 16px;
      overflow: hidden;
      border: 1px solid rgba(255, 255, 255, 0.08);
    }
    th {
      background: rgba(30, 41, 59, 0.9);
      padding: 16px 14px;
      font-size: 15px;
      font-weight: 700;
      color: #cbd5e1;
      border-bottom: 1px solid rgba(255, 255, 255, 0.12);
    }
    td {
      padding: 16px 14px;
      font-size: 16px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.06);
      color: #94a3b8;
    }
    tr.highlight-row {
      background: rgba(56, 189, 248, 0.08);
    }
    tr.highlight-row td {
      color: #ffffff;
      font-weight: 700;
    }
    .badge-kia {
      background: #38bdf8;
      color: #04101e;
      padding: 4px 10px;
      border-radius: 6px;
      font-weight: 800;
      font-size: 13px;
    }
    .val-green { color: #34d399 !important; font-weight: 800; }
    .val-blue { color: #38bdf8 !important; font-weight: 800; }
    .footer-note {
      background: rgba(15, 23, 42, 0.9);
      border: 1px solid rgba(56, 189, 248, 0.3);
      border-radius: 12px;
      padding: 14px 20px;
      display: flex;
      align-items: center;
      gap: 12px;
      font-size: 14.5px;
      color: #e2e8f0;
      margin-top: 12px;
    }
    .footer-note span.icon {
      font-size: 18px;
    }
  </style>
</head>
<body>
  <div class="header">
    <h2>📊 기아 vs 글로벌 주요 완성차 밸류에이션 비교</h2>
    <span class="tag">2026년 기준 컨센서스</span>
  </div>
  <div class="table-container">
    <table>
      <thead>
        <tr>
          <th>기업명</th>
          <th>예상 PER</th>
          <th>예상 PBR</th>
          <th>영업이익률(OPM)</th>
          <th>배당수익률</th>
          <th>종합 평가</th>
        </tr>
      </thead>
      <tbody>
        <tr class="highlight-row">
          <td><span class="badge-kia">기아 (000270)</span></td>
          <td class="val-blue">5.2배</td>
          <td class="val-blue">0.70배</td>
          <td>8.0%</td>
          <td class="val-green">6.0%</td>
          <td class="val-green">극도의 저평가 + 고배당</td>
        </tr>
        <tr>
          <td>현대차 (005380)</td>
          <td>5.8배</td>
          <td>0.65배</td>
          <td>8.5%</td>
          <td>5.2%</td>
          <td>밸류업 수혜 대형주</td>
        </tr>
        <tr>
          <td>토요타 (Toyota)</td>
          <td>9.8배</td>
          <td>1.08배</td>
          <td>9.2%</td>
          <td>2.8%</td>
          <td>글로벌 프리미엄 밸류</td>
        </tr>
        <tr>
          <td>혼다 (Honda)</td>
          <td>7.5배</td>
          <td>0.58배</td>
          <td>6.5%</td>
          <td>3.8%</td>
          <td>중위권 밸류에이션</td>
        </tr>
        <tr>
          <td>폭스바겐 (VW Group)</td>
          <td>4.9배</td>
          <td>0.35배</td>
          <td>5.2%</td>
          <td>7.1%</td>
          <td>구조조정 및 수익성 둔화</td>
        </tr>
      </tbody>
    </table>
  </div>
  <div class="footer-note">
    <span class="icon">💡</span>
    <span><strong>핵심 결론:</strong> 기아는 토요타 수준의 고수익 체질(OPM 8~11%)을 입증했음에도 PER은 토요타 대비 47% 할인된 5.2배에 불과하며, 6% 고배당으로 강력한 안전마진을 보유하고 있습니다.</span>
  </div>
</body>
</html>
"""

# 3. 본문 2: 기아 미래 모빌리티 3대 성장 기둥 (1080x640)
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
      font-size: 24px;
      font-weight: 800;
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .tag {
      font-size: 13.5px;
      font-weight: 600;
      background: rgba(129, 140, 248, 0.15);
      color: #818cf8;
      border: 1px solid rgba(129, 140, 248, 0.35);
      padding: 5px 14px;
      border-radius: 9999px;
    }
    .cards-row {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 20px;
      margin-top: 18px;
      flex: 1;
    }
    .pillar-card {
      background: rgba(15, 23, 42, 0.7);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 20px;
      padding: 24px 20px;
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
      width: 100%;
      height: 4px;
      background: #38bdf8;
    }
    .pillar-card.card-2::before { background: #818cf8; }
    .pillar-card.card-3::before { background: #34d399; }

    .card-num {
      font-size: 13px;
      font-weight: 700;
      color: #38bdf8;
      letter-spacing: 1px;
      margin-bottom: 8px;
    }
    .card-2 .card-num { color: #818cf8; }
    .card-3 .card-num { color: #34d399; }

    .card-title {
      font-size: 20px;
      font-weight: 800;
      color: #ffffff;
      margin-bottom: 12px;
      line-height: 1.35;
    }
    .card-desc {
      font-size: 14.5px;
      color: #94a3b8;
      line-height: 1.6;
      flex: 1;
    }
    .metric-box {
      margin-top: 14px;
      background: rgba(2, 6, 23, 0.6);
      border: 1px solid rgba(255, 255, 255, 0.05);
      border-radius: 12px;
      padding: 12px 14px;
    }
    .metric-title {
      font-size: 12px;
      color: #64748b;
      margin-bottom: 4px;
    }
    .metric-val {
      font-size: 18px;
      font-weight: 800;
      color: #e2e8f0;
    }
  </style>
</head>
<body>
  <div class="header">
    <h2>🚀 기아 미래 모빌리티 3대 성장 기둥 (3-Pillar)</h2>
    <span class="tag">구조적 실적 견인 로드맵</span>
  </div>
  <div class="cards-row">
    <div class="pillar-card card-1">
      <div>
        <div class="card-num">PILLAR 01</div>
        <div class="card-title">고마진 RV & 하이브리드<br>유연 혼류 생산</div>
        <div class="card-desc">
          전체 판매의 70%를 차지하는 쏘렌토·스포티지·카니발 RV 라인업. 전기차 수요 둔화 시 공장을 HEV로 즉각 전환하여 글로벌 평균판매단가(ASP) 방어.
        </div>
      </div>
      <div class="metric-box">
        <div class="metric-title">핵심 실적 지표</div>
        <div class="metric-val" style="color:#38bdf8;">글로벌 RV 비중 70%+</div>
      </div>
    </div>
    <div class="pillar-card card-2">
      <div>
        <div class="card-num">PILLAR 02</div>
        <div class="card-title">대중화 전기차 볼륨화 &<br>미국 HMGMA 가동</div>
        <div class="card-desc">
          3,000~4,000만 원대 EV3·EV4로 대중화 EV 시장 선점. 미국 조지아 메타플랜트 현지 생산을 통해 대미 관세 장벽과 IRA 보조금 요건을 완벽 방어.
        </div>
      </div>
      <div class="metric-box">
        <div class="metric-title">글로벌 생산 거점</div>
        <div class="metric-val" style="color:#818cf8;">조지아 HMGMA 풀가동</div>
      </div>
    </div>
    <div class="pillar-card card-3">
      <div>
        <div class="card-num">PILLAR 03</div>
        <div class="card-title">세계 최초 PBV 전용 공장<br>화성 EVO 플랜트</div>
        <div class="card-desc">
          E-GMP.S 플랫폼 기반 PV5·PV7 런칭. 무인 운반 로봇(AGV) 셀 생산으로 연간 25만 대 규모 다품종 맞춤형 B2B 물류·모빌리티 생태계 독점 선점.
        </div>
      </div>
      <div class="metric-box">
        <div class="metric-title">PBV 양산 능력</div>
        <div class="metric-val" style="color:#34d399;">연간 250,000대 체제</div>
      </div>
    </div>
  </div>
</body>
</html>
"""

# 4. 본문 3: 기아 투자 핵심 체크포인트 4대 카드 & 리스크 점검 (1080x640)
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
      font-size: 24px;
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
    .grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 16px;
      margin-top: 16px;
      flex: 1;
    }
    .card {
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
    .card::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      width: 4px;
      height: 100%;
      background: #38bdf8;
    }
    .card.card-2::before { background: #34d399; }
    .card.card-3::before { background: #818cf8; }
    .card.card-4::before { background: #fb923c; }

    .card-top {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 8px;
    }
    .card-label {
      font-size: 13px;
      font-weight: 700;
      color: #94a3b8;
    }
    .card-stat {
      font-size: 14px;
      font-weight: 800;
      color: #38bdf8;
      background: rgba(56, 189, 248, 0.12);
      padding: 4px 10px;
      border-radius: 6px;
    }
    .card-2 .card-stat { color: #34d399; background: rgba(52, 211, 153, 0.12); }
    .card-3 .card-stat { color: #818cf8; background: rgba(129, 140, 248, 0.12); }
    .card-4 .card-stat { color: #fb923c; background: rgba(251, 146, 60, 0.12); }

    .card-title {
      font-size: 19px;
      font-weight: 800;
      color: #ffffff;
      margin-bottom: 6px;
    }
    .card-desc {
      font-size: 14px;
      color: #94a3b8;
      line-height: 1.55;
    }
  </style>
</head>
<body>
  <div class="header">
    <h2>🎯 기아 가치투자 4대 체크포인트 & 리스크 점검</h2>
    <span class="tag">투자 전략 총정리</span>
  </div>
  <div class="grid">
    <div class="card card-1">
      <div class="card-top">
        <span class="card-label">POINT 01 · 밸류에이션</span>
        <span class="card-stat">PER 5.2배 / PBR 0.7배</span>
      </div>
      <div class="card-title">극도의 저평가 안전마진</div>
      <div class="card-desc">
        글로벌 탑티어 수준의 영업이익률(8~11%)을 기록하면서도 시가총액은 순이익의 5배에 불과. 청산가치(1.0배) 이하의 강력한 가격 방어력.
      </div>
    </div>
    <div class="card card-2">
      <div class="card-top">
        <span class="card-label">POINT 02 · 주주환원</span>
        <span class="card-stat">배당률 6.0% + 소각</span>
      </div>
      <div class="card-title">확실한 고배당 & 밸류업</div>
      <div class="card-desc">
        주당 6,800원 배당으로 시중 금리의 2배 수준 수익률 제공. 매년 5,000억 자사주 매입 및 50% 영구 소각으로 주당 가치 지속 증대.
      </div>
    </div>
    <div class="card card-3">
      <div class="card-top">
        <span class="card-label">POINT 03 · 성장 모멘텀</span>
        <span class="card-stat">화성 EVO 연 25만대</span>
      </div>
      <div class="card-title">PBV 신시장 개척 (PV5/PV7)</div>
      <div class="card-desc">
        단순 완성차를 넘어 물류·플랫폼 B2B 맞춤형 PBV 생태계 선점. 우버, 카카오모빌리티 등과의 계약을 통해 안정적 대량 수주 기반 확보.
      </div>
    </div>
    <div class="card card-4">
      <div class="card-top">
        <span class="card-label">POINT 04 · 리스크 헤지</span>
        <span class="card-stat">HMGMA 현지 생산</span>
      </div>
      <div class="card-title">관세 & 캐즘 리스크 대응</div>
      <div class="card-desc">
        미국 조지아 HMGMA 공장 가동으로 관세 및 IRA 규제 회피. 전기차 캐즘은 고수익 하이브리드 혼류 생산으로 완벽한 포트폴리오 헤지.
      </div>
    </div>
  </div>
</body>
</html>
"""

async def generate_all():
    print("Playwright 브라우저 기동 중...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        # 1. 썸네일
        page_thumb = await browser.new_page(viewport={"width": 1080, "height": 1080}, device_scale_factor=2)
        await page_thumb.set_content(thumbnail_html, wait_until="networkidle")
        await page_thumb.screenshot(path=str(OUTPUT_DIR / "thumbnail.png"), type="png")
        await page_thumb.close()
        print("✅ thumbnail.png 캡처 완료")

        # 2. 본문 1
        page_b1 = await browser.new_page(viewport={"width": 1080, "height": 640}, device_scale_factor=2)
        await page_b1.set_content(body_1_html, wait_until="networkidle")
        await page_b1.screenshot(path=str(OUTPUT_DIR / "body-1.png"), type="png")
        await page_b1.close()
        print("✅ body-1.png 캡처 완료")

        # 3. 본문 2
        page_b2 = await browser.new_page(viewport={"width": 1080, "height": 640}, device_scale_factor=2)
        await page_b2.set_content(body_2_html, wait_until="networkidle")
        await page_b2.screenshot(path=str(OUTPUT_DIR / "body-2.png"), type="png")
        await page_b2.close()
        print("✅ body-2.png 캡처 완료")

        # 4. 본문 3
        page_b3 = await browser.new_page(viewport={"width": 1080, "height": 640}, device_scale_factor=2)
        await page_b3.set_content(body_3_html, wait_until="networkidle")
        await page_b3.screenshot(path=str(OUTPUT_DIR / "body-3.png"), type="png")
        await page_b3.close()
        print("✅ body-3.png 캡처 완료")

        await browser.close()
    print("🎉 모든 이미지 생성 완료!")

if __name__ == "__main__":
    asyncio.run(generate_all())
