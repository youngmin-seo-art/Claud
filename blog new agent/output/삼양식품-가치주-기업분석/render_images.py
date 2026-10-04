import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

async def generate_images():
    output_dir = Path("output/삼양식품-가치주-기업분석/images")
    output_dir.mkdir(parents=True, exist_ok=True)

    images = [
        {
            "filename": "thumbnail.png",
            "width": 1080,
            "height": 1080,
            "html": """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 1080px;
      height: 1080px;
      background: linear-gradient(135deg, #090d16 0%, #0f172a 50%, #1e1b4b 100%);
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
      background: rgba(30, 41, 59, 0.4);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 36px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      padding: 70px 60px;
      box-shadow: 0 25px 60px rgba(0, 0, 0, 0.6);
      backdrop-filter: blur(16px);
      position: relative;
      overflow: hidden;
    }
    .card::before {
      content: '';
      position: absolute;
      top: -150px;
      right: -150px;
      width: 350px;
      height: 350px;
      background: radial-gradient(circle, rgba(239, 68, 68, 0.35) 0%, transparent 70%);
      border-radius: 50%;
    }
    .header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .badge {
      font-size: 22px;
      font-weight: 700;
      color: #f87171;
      background: rgba(239, 68, 68, 0.15);
      border: 1px solid rgba(239, 68, 68, 0.35);
      padding: 12px 26px;
      border-radius: 9999px;
      letter-spacing: 1px;
    }
    .ticker {
      font-size: 24px;
      font-weight: 700;
      color: #94a3b8;
      font-family: monospace;
      background: rgba(255, 255, 255, 0.05);
      padding: 8px 18px;
      border-radius: 12px;
      border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .main-content {
      text-align: left;
      margin: auto 0;
    }
    .title {
      font-size: 56px;
      font-weight: 900;
      line-height: 1.28;
      margin-bottom: 24px;
      word-break: keep-all;
      background: linear-gradient(180deg, #ffffff 0%, #cbd5e1 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      letter-spacing: -1.5px;
    }
    .title span {
      background: linear-gradient(90deg, #f87171 0%, #fb923c 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .subtitle {
      font-size: 25px;
      font-weight: 500;
      color: #94a3b8;
      line-height: 1.5;
      word-break: keep-all;
    }
    .footer-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 16px;
    }
    .stat-pill {
      background: rgba(15, 23, 42, 0.7);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 20px;
      padding: 18px 20px;
      text-align: center;
    }
    .stat-label {
      font-size: 15px;
      color: #64748b;
      margin-bottom: 6px;
      font-weight: 600;
    }
    .stat-val {
      font-size: 22px;
      font-weight: 800;
      color: #f87171;
    }
  </style>
</head>
<body>
  <div class="card">
    <div class="header">
      <div class="badge">가치투자 & 종목분석</div>
      <div class="ticker">KOSPI 003230</div>
    </div>
    <div class="main-content">
      <h1 class="title">삼양식품 기업분석<br><span>글로벌 수출 83% · OPM 23%</span><br>PEG 0.6배 저평가 가치</h1>
      <p class="subtitle">밀양 2공장 스마트팩토리 CAPA 55% 증설 + 미국 월마트·코스트코 메인스트림 장악</p>
    </div>
    <div class="footer-grid">
      <div class="stat-pill">
        <div class="stat-label">해외 수출 비중</div>
        <div class="stat-val">83.5% 돌파</div>
      </div>
      <div class="stat-pill">
        <div class="stat-label">밀양 2공장 생산능력</div>
        <div class="stat-val">연 28억 개 (+55%)</div>
      </div>
      <div class="stat-pill">
        <div class="stat-label">피터 린치 밸류에이션</div>
        <div class="stat-val">PEG 0.59~0.60x</div>
      </div>
    </div>
  </div>
</body>
</html>"""
        },
        {
            "filename": "body-1.png",
            "width": 1100,
            "height": 680,
            "html": """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 1100px;
      height: 680px;
      background: linear-gradient(135deg, #090d16 0%, #0f172a 100%);
      font-family: 'Pretendard', sans-serif;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      color: #ffffff;
      padding: 36px;
    }
    .container {
      width: 100%;
      height: 100%;
      background: rgba(30, 41, 59, 0.4);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 28px;
      padding: 34px 40px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      backdrop-filter: blur(12px);
    }
    .header {
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
      padding-bottom: 14px;
    }
    .title-group h2 {
      font-size: 26px;
      font-weight: 800;
      color: #ffffff;
    }
    .title-group p {
      font-size: 14px;
      color: #94a3b8;
      margin-top: 4px;
    }
    .flow-wrapper {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin: 20px 0;
      position: relative;
    }
    .flow-step {
      width: 220px;
      background: rgba(15, 23, 42, 0.7);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 20px;
      padding: 22px 18px;
      text-align: center;
      display: flex;
      flex-direction: column;
      align-items: center;
      position: relative;
    }
    .step-badge {
      font-size: 12px;
      font-weight: 800;
      padding: 4px 10px;
      border-radius: 6px;
      margin-bottom: 12px;
    }
    .step-title {
      font-size: 17px;
      font-weight: 700;
      color: #ffffff;
      margin-bottom: 8px;
    }
    .step-desc {
      font-size: 13px;
      color: #94a3b8;
      line-height: 1.5;
    }
    .arrow {
      font-size: 24px;
      color: #ef4444;
      font-weight: bold;
    }
    .bottom-box {
      background: rgba(239, 68, 68, 0.12);
      border: 1px solid rgba(239, 68, 68, 0.3);
      border-radius: 14px;
      padding: 14px 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 14px;
      color: #cbd5e1;
    }
    .bottom-box strong { color: #f87171; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <div class="title-group">
        <h2>삼양식품 글로벌 수출 밸류체인 & 공급 프로세스</h2>
        <p>밀양 스마트팩토리 생산부터 글로벌 메인스트림 유통망 직공급 체계</p>
      </div>
      <div style="color:#f87171; font-weight:700; font-size:14px;">GLOBAL VALUE CHAIN</div>
    </div>
    
    <div class="flow-wrapper">
      <div class="flow-step" style="border-top: 4px solid #ef4444;">
        <div class="step-badge" style="background:rgba(239,68,68,0.2); color:#f87171;">STEP 01</div>
        <div class="step-title">스마트 생산 증설</div>
        <div class="step-desc">밀양 2공장 스마트팩토리<br>연 28억 개 생산능력<br>단위당 제조원가 절감</div>
      </div>
      <div class="arrow">➔</div>
      <div class="flow-step" style="border-top: 4px solid #f97316;">
        <div class="step-badge" style="background:rgba(249,115,22,0.2); color:#fb923c;">STEP 02</div>
        <div class="step-title">해외 거점 직판화</div>
        <div class="step-desc">미국·유럽·중국 법인<br>네덜란드 유럽 R&D 거점<br>직거래 유통 마진 확대</div>
      </div>
      <div class="arrow">➔</div>
      <div class="flow-step" style="border-top: 4px solid #10b981;">
        <div class="step-badge" style="background:rgba(16,185,129,0.2); color:#34d399;">STEP 03</div>
        <div class="step-title">주류 매대 전면 장악</div>
        <div class="step-desc">월마트 90%·코스트코 50%<br>타깃·크로거 전점 확대<br>메인스트림 매대 고정</div>
      </div>
      <div class="arrow">➔</div>
      <div class="flow-step" style="border-top: 4px solid #38bdf8;">
        <div class="step-badge" style="background:rgba(56,189,248,0.2); color:#38bdf8;">STEP 04</div>
        <div class="step-title">소스 B2B 생태계</div>
        <div class="step-desc">글로벌 외식 프랜차이즈<br>디핑소스 B2B 납품<br>OPM 23%+ 극대화</div>
      </div>
    </div>

    <div class="bottom-box">
      <span>💡 <strong>삼양식품의 핵심 경쟁력</strong>: 공급 병목을 100% 해소하고 직판 유통망과 소스 다변화로 영업이익률 23%를 안정적으로 달성</span>
    </div>
  </div>
</body>
</html>"""
        },
        {
            "filename": "body-2.png",
            "width": 1100,
            "height": 680,
            "html": """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 1100px;
      height: 680px;
      background: linear-gradient(135deg, #090d16 0%, #0f172a 100%);
      font-family: 'Pretendard', sans-serif;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      color: #ffffff;
      padding: 40px;
    }
    .container {
      width: 100%;
      height: 100%;
      background: rgba(30, 41, 59, 0.4);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 28px;
      padding: 36px 44px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      backdrop-filter: blur(12px);
    }
    .header {
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
      padding-bottom: 16px;
    }
    .title-group h2 {
      font-size: 28px;
      font-weight: 800;
      color: #ffffff;
      letter-spacing: -0.5px;
    }
    .title-group p {
      font-size: 15px;
      color: #94a3b8;
      margin-top: 4px;
    }
    .tag {
      font-size: 14px;
      font-weight: 700;
      color: #f87171;
      background: rgba(239, 68, 68, 0.15);
      border: 1px solid rgba(239, 68, 68, 0.3);
      padding: 6px 14px;
      border-radius: 8px;
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 20px;
      margin-top: 20px;
    }
    .card {
      background: rgba(15, 23, 42, 0.65);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 18px;
      padding: 22px 24px;
      position: relative;
    }
    .card-header {
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 10px;
    }
    .num-badge {
      width: 32px;
      height: 32px;
      border-radius: 10px;
      background: #ef4444;
      color: #fff;
      font-weight: 800;
      font-size: 16px;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .card-title {
      font-size: 19px;
      font-weight: 700;
      color: #f1f5f9;
    }
    .card-desc {
      font-size: 14px;
      color: #94a3b8;
      line-height: 1.55;
    }
    .highlight {
      color: #f87171;
      font-weight: 700;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <div class="title-group">
        <h2>삼양식품 4대 핵심 경제적 해자(Economic Moats)</h2>
        <p>대체 불가능한 글로벌 브랜드 파워와 독보적 수출 인프라 경쟁력</p>
      </div>
      <div class="tag">MOAT ANALYSIS</div>
    </div>
    <div class="grid">
      <div class="card">
        <div class="card-header">
          <div class="num-badge">1</div>
          <div class="card-title">글로벌 Z세대 팬덤 & 불닭 IP 파워</div>
        </div>
        <p class="card-desc">SNS 바이럴과 컬트적 매운맛 챌린지로 <span class="highlight">광고비 없이 자발적 재구매</span>가 일어나는 대체 불가능한 글로벌 독점 브랜드 파워.</p>
      </div>
      <div class="card">
        <div class="card-header">
          <div class="num-badge" style="background:#f97316;">2</div>
          <div class="card-title">밀양 스마트팩토리 원가 우위</div>
        </div>
        <p class="card-desc">1,643억 원 투입으로 밀양 2공장 준공, 연간 <span class="highlight">28억 개 생산능력 확보</span>와 단위당 제조원가 절감으로 23%대 고마진 수성.</p>
      </div>
      <div class="card">
        <div class="card-header">
          <div class="num-badge" style="background:#10b981;">3</div>
          <div class="card-title">미국·유럽 주류 유통망 선점 락인</div>
        </div>
        <p class="card-desc">월마트 90%, 코스트코 50%, 타깃 등 미국 탑티어 유통업체 <span class="highlight">메인스트림 매대 직입점</span>으로 후발주자 진입장벽 구축.</p>
      </div>
      <div class="card">
        <div class="card-header">
          <div class="num-badge" style="background:#0284c7;">4</div>
          <div class="card-title">불닭 소스 및 글로벌 B2B 확장성</div>
        </div>
        <p class="card-desc">해외 소스 매출 비중 70%+ 돌파 및 판다익스프레스 등 <span class="highlight">글로벌 프랜차이즈 B2B 제휴</span>로 제품 수명주기(PLC) 장기화 달성.</p>
      </div>
    </div>
  </div>
</body>
</html>"""
        },
        {
            "filename": "body-3.png",
            "width": 1100,
            "height": 680,
            "html": """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 1100px;
      height: 680px;
      background: linear-gradient(135deg, #090d16 0%, #0f172a 100%);
      font-family: 'Pretendard', sans-serif;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      color: #ffffff;
      padding: 36px;
    }
    .container {
      width: 100%;
      height: 100%;
      background: rgba(30, 41, 59, 0.4);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 28px;
      padding: 32px 36px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      backdrop-filter: blur(12px);
    }
    .header {
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
      padding-bottom: 14px;
    }
    .title-group h2 {
      font-size: 26px;
      font-weight: 800;
      color: #ffffff;
    }
    .title-group p {
      font-size: 14px;
      color: #94a3b8;
      margin-top: 4px;
    }
    .table-box {
      width: 100%;
      margin: 16px 0;
      border-radius: 16px;
      overflow: hidden;
      border: 1px solid rgba(255, 255, 255, 0.1);
      background: rgba(15, 23, 42, 0.8);
    }
    table {
      width: 100%;
      border-collapse: collapse;
      text-align: center;
      font-size: 14px;
    }
    th {
      background: rgba(30, 41, 59, 0.9);
      color: #94a3b8;
      font-weight: 700;
      padding: 14px 10px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    td {
      padding: 14px 10px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.05);
      color: #e2e8f0;
    }
    tr.highlight-row {
      background: rgba(239, 68, 68, 0.15);
    }
    tr.highlight-row td {
      color: #ffffff;
      font-weight: 600;
    }
    .badge-samyang {
      background: #ef4444;
      color: #fff;
      padding: 4px 10px;
      border-radius: 6px;
      font-weight: 800;
    }
    .text-red { color: #f87171; font-weight: 800; }
    .text-green { color: #34d399; font-weight: 700; }
    .footer-note {
      font-size: 13px;
      color: #64748b;
      display: flex;
      justify-content: space-between;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <div class="title-group">
        <h2>국내외 음식료 및 라면 선도기업 수익성 & 밸류에이션 비교</h2>
        <p>글로벌 Peer 대비 압도적인 수익성(OPM 23%)과 저평가 리레이팅 기회</p>
      </div>
      <div style="color:#f87171; font-weight:700; font-size:14px;">PEER GROUP COMPARISON</div>
    </div>
    <div class="table-box">
      <table>
        <thead>
          <tr>
            <th>기업명</th>
            <th>주력 사업 영역</th>
            <th>2026(E) OPM</th>
            <th>해외 매출 비중</th>
            <th>2026(E) PER</th>
            <th>ROE(자본효율성)</th>
          </tr>
        </thead>
        <tbody>
          <tr class="highlight-row">
            <td><span class="badge-samyang">삼양식품</span></td>
            <td>불닭볶음면 수출 + 소스 B2B</td>
            <td class="text-red">23.4% (업계 1위)</td>
            <td class="text-red">83.5% (압도적)</td>
            <td class="text-red">18.2배 (저평가)</td>
            <td class="text-green">35.8% (최상위)</td>
          </tr>
          <tr>
            <td>농심</td>
            <td>신라면 중심 국내외 라면·스낵</td>
            <td>6.8%</td>
            <td>약 40.0%</td>
            <td>14.5배</td>
            <td>8.5%</td>
          </tr>
          <tr>
            <td>오뚜기</td>
            <td>진라면, 카레, HMR 내수 중심</td>
            <td>6.2%</td>
            <td>약 11.5%</td>
            <td>16.8배</td>
            <td>6.2%</td>
          </tr>
          <tr>
            <td>Nissin Foods (일본)</td>
            <td>글로벌 컵누들 1위</td>
            <td>10.5%</td>
            <td>약 45.0%</td>
            <td>24.5배</td>
            <td>12.0%</td>
          </tr>
          <tr>
            <td>Mondelez (미국)</td>
            <td>글로벌 제과·스낵 공룡</td>
            <td>16.8%</td>
            <td>약 75.0%</td>
            <td>22.0배</td>
            <td>15.5%</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="footer-note">
      <span>* 출처: FnGuide, Bloomberg, 각 사 실적 컨센서스 및 증권사 리포트 종합</span>
      <span>※ 삼양식품의 OPM은 전통 음식료 평균(6~7%)의 3.5배, ROE는 글로벌 최고 수준</span>
    </div>
  </div>
</body>
</html>"""
        },
        {
            "filename": "body-4.png",
            "width": 1100,
            "height": 720,
            "html": """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 1100px;
      height: 720px;
      background: linear-gradient(135deg, #090d16 0%, #0f172a 100%);
      font-family: 'Pretendard', sans-serif;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      color: #ffffff;
      padding: 36px;
    }
    .container {
      width: 100%;
      height: 100%;
      background: rgba(30, 41, 59, 0.4);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 28px;
      padding: 32px 38px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      backdrop-filter: blur(12px);
    }
    .header {
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
      padding-bottom: 12px;
    }
    .title-group h2 {
      font-size: 26px;
      font-weight: 800;
      color: #ffffff;
    }
    .title-group p {
      font-size: 14px;
      color: #94a3b8;
      margin-top: 4px;
    }
    .grid-top {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 14px;
      margin: 14px 0;
    }
    .metric-card {
      background: rgba(15, 23, 42, 0.7);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 16px;
      padding: 16px;
      text-align: center;
    }
    .m-year { font-size: 13px; color: #64748b; font-weight: 700; margin-bottom: 4px; }
    .m-rev { font-size: 16px; color: #cbd5e1; font-weight: 600; margin-bottom: 4px; }
    .m-op { font-size: 22px; font-weight: 900; color: #f87171; }
    .m-opm { font-size: 12px; color: #34d399; font-weight: 700; margin-top: 4px; }
    
    .grid-bottom {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 16px;
    }
    .val-card {
      background: rgba(30, 41, 59, 0.6);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 18px;
      padding: 18px 22px;
    }
    .val-title {
      font-size: 16px;
      font-weight: 800;
      color: #f8fafc;
      margin-bottom: 8px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .val-desc {
      font-size: 13.5px;
      color: #94a3b8;
      line-height: 1.55;
    }
    .val-desc strong { color: #f87171; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <div class="title-group">
        <h2>삼양식품 실적 퀀텀점프 및 저평가(PEG) 밸류에이션</h2>
        <p>밀양 2공장 가동으로 OPM 23% 달성 및 연평균 EPS 30%+ 고속 성장</p>
      </div>
      <div style="color:#34d399; font-weight:700; font-size:14px;">VALUATION CHECK</div>
    </div>

    <div class="grid-top">
      <div class="metric-card">
        <div class="m-year">2023년 (확정)</div>
        <div class="m-rev">매출 1.19조</div>
        <div class="m-op" style="color:#cbd5e1;">1,480억</div>
        <div class="m-opm">OPM 12.4%</div>
      </div>
      <div class="metric-card">
        <div class="m-year">2024년 (확정)</div>
        <div class="m-rev">매출 1.73조</div>
        <div class="m-op" style="color:#cbd5e1;">3,445억</div>
        <div class="m-opm">OPM 20.0%</div>
      </div>
      <div class="metric-card" style="border: 1.5px solid #f87171; background: rgba(239,68,68,0.1);">
        <div class="m-year" style="color:#f87171;">2025년 (확정/잠정)</div>
        <div class="m-rev">매출 2.35조</div>
        <div class="m-op">5,240억</div>
        <div class="m-opm">OPM 22.3%</div>
      </div>
      <div class="metric-card" style="border: 1.5px solid #fb923c; background: rgba(251,146,60,0.1);">
        <div class="m-year" style="color:#fb923c;">2026년 (E)</div>
        <div class="m-rev">매출 2.86~3.0조</div>
        <div class="m-op" style="color:#fb923c;">6,700~7,100억</div>
        <div class="m-opm">OPM 23.4% (최고치)</div>
      </div>
    </div>

    <div class="grid-bottom">
      <div class="val-card">
        <div class="val-title">📊 피터 린치 PEG 0.59~0.60x 딥 밸류</div>
        <p class="val-desc">연평균 순이익 성장률 <strong>30.5%</strong> 대비 2026년 Forward PER은 <strong>18.2배</strong>에 불과합니다. 피터 린치 기준 <strong>PEG 1.0 미만은 매력적 저평가, 0.6x는 강력 매수 구간</strong>입니다.</p>
      </div>
      <div class="val-card">
        <div class="val-title">🚀 목표 PER 25배 멀티플 리레이팅</div>
        <p class="val-desc">글로벌 1위 닛신(PER 24.5배) 및 몬델리즈 대비 수익성은 2배 이상 높습니다. 밀양 2공장 본격 가동으로 <strong>증권가 목표주가 1,800,000~1,950,000원</strong>의 상승여력을 보유합니다.</p>
      </div>
    </div>
  </div>
</body>
</html>"""
        }
    ]

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        for item in images:
            output_file = output_dir / item["filename"]
            page = await browser.new_page(
                viewport={"width": item["width"], "height": item["height"]},
                device_scale_factor=2
            )
            await page.set_content(item["html"], wait_until="networkidle")
            await page.screenshot(path=str(output_file), type="png")
            await page.close()
            print(f"[성공] {item['filename']} 생성 완료 ({item['width']}x{item['height']})")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(generate_images())
