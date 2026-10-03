import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

async def generate_images():
    output_dir = Path("output/LS일렉트릭-가치주-기업분석/images")
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
      background: radial-gradient(circle, rgba(99, 102, 241, 0.35) 0%, transparent 70%);
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
      color: #38bdf8;
      background: rgba(56, 189, 248, 0.15);
      border: 1px solid rgba(56, 189, 248, 0.35);
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
      font-size: 58px;
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
      background: linear-gradient(90deg, #38bdf8 0%, #818cf8 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .subtitle {
      font-size: 26px;
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
      color: #38bdf8;
    }
  </style>
</head>
<body>
  <div class="card">
    <div class="header">
      <div class="badge">가치투자 & 종목분석</div>
      <div class="ticker">KOSPI 010120</div>
    </div>
    <div class="main-content">
      <h1 class="title">LS일렉트릭 기업분석<br><span>4대 해자 · AI 데이터센터</span><br>PEG 0.6배 저평가 가치</h1>
      <p class="subtitle">국내 배전 70% 독점 캐시카우 + 초고압 변압기 3배 증설과 글로벌 빅테크 턴키 수주</p>
    </div>
    <div class="footer-grid">
      <div class="stat-pill">
        <div class="stat-label">국내 배전 점유율</div>
        <div class="stat-val">70% 독점</div>
      </div>
      <div class="stat-pill">
        <div class="stat-label">초고압 변압기 CAPA</div>
        <div class="stat-val">6,000억 (3배↑)</div>
      </div>
      <div class="stat-pill">
        <div class="stat-label">피터 린치 밸류에이션</div>
        <div class="stat-val">PEG 0.54~0.6x</div>
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
      color: #38bdf8;
      background: rgba(56, 189, 248, 0.15);
      border: 1px solid rgba(56, 189, 248, 0.3);
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
      background: #4f46e5;
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
      color: #38bdf8;
      font-weight: 700;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <div class="title-group">
        <h2>LS일렉트릭 4대 핵심 경제적 해자(Economic Moats)</h2>
        <p>국내 유일의 송·변·배전 풀스택 경쟁력과 독보적 진입장벽</p>
      </div>
      <div class="tag">MOAT ANALYSIS</div>
    </div>
    <div class="grid">
      <div class="card">
        <div class="card-header">
          <div class="num-badge">1</div>
          <div class="card-title">국내 배전 시장 70% 과점 독점</div>
        </div>
        <p class="card-desc">저·고압 차단기 및 배전반 규격 락인(Lock-in)과 50년 레퍼런스로 <span class="highlight">연 4,000억+ 안정적 EBITDA</span> 창출하는 철옹성 캐시카우.</p>
      </div>
      <div class="card">
        <div class="card-header">
          <div class="num-badge" style="background:#0284c7;">2</div>
          <div class="card-title">부산공장 초고압 변압기 3배 증설</div>
        </div>
        <p class="card-desc">1,008억 원 투자로 제2생산동 완공, 초고압 생산능력 <span class="highlight">2,000억 → 6,000억 원으로 3배 확대</span>하여 북미 345kV급 납기 병목 해소.</p>
      </div>
      <div class="card">
        <div class="card-header">
          <div class="num-badge" style="background:#059669;">3</div>
          <div class="card-title">AI 데이터센터 'Beyond X MDB' 턴키</div>
        </div>
        <p class="card-desc">설치 면적 30% 절감 초슬림 모듈형 배전반으로 <span class="highlight">배전반 수주잔고 2조 원 돌파</span>, 변압기+배전반 일괄 공급 체계 완성.</p>
      </div>
      <div class="card">
        <div class="card-header">
          <div class="num-badge" style="background:#d97706;">4</div>
          <div class="card-title">국내 유일 HVDC 독점 & GE 합작</div>
        </div>
        <p class="card-desc">차세대 직류 송전망인 HVDC 국산화 성공 및 국가 에너지 고속도로 독점, <span class="highlight">GE버노바 합작법인</span>으로 글로벌 직류 시장 선점.</p>
      </div>
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
      background: rgba(56, 189, 248, 0.12);
    }
    tr.highlight-row td {
      color: #ffffff;
      font-weight: 600;
    }
    .badge-ls {
      background: #0284c7;
      color: #fff;
      padding: 4px 10px;
      border-radius: 6px;
      font-weight: 800;
    }
    .text-green { color: #34d399; font-weight: 700; }
    .text-blue { color: #38bdf8; font-weight: 800; }
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
        <h2>국내외 전력기기 선도 5사 밸류에이션 및 수익성 비교</h2>
        <p>글로벌 Peer 대비 과도하게 할인된 LS일렉트릭의 리레이팅 기회</p>
      </div>
      <div style="color:#38bdf8; font-weight:700; font-size:14px;">PEER GROUP COMPARISON</div>
    </div>
    <div class="table-box">
      <table>
        <thead>
          <tr>
            <th>기업명</th>
            <th>주력 사업 영역</th>
            <th>2026(E) OPM</th>
            <th>수주잔고</th>
            <th>2026(E) PER</th>
            <th>사업 순수성 및 리스크</th>
          </tr>
        </thead>
        <tbody>
          <tr class="highlight-row">
            <td><span class="badge-ls">LS일렉트릭</span></td>
            <td>송·변·배전 풀스택 + IDC 배전반</td>
            <td class="text-green">11.5% ~ 13.0%</td>
            <td>약 7.0조 원 (배전 2조)</td>
            <td class="text-blue">15 ~ 18배 (저평가)</td>
            <td>전력·자동화 100% 순수주</td>
          </tr>
          <tr>
            <td>HD현대일렉트릭</td>
            <td>초고압 송전 변압기 특화</td>
            <td class="text-green">24.5% ~ 25.5%</td>
            <td>약 11~12조 원</td>
            <td>25 ~ 30배</td>
            <td>전력기기 100% 순수주</td>
          </tr>
          <tr>
            <td>효성중공업</td>
            <td>초고압 변압기 + 건설</td>
            <td>9.5% ~ 11.0%</td>
            <td>약 17.5조 원 (건설포함)</td>
            <td>18 ~ 22배</td>
            <td>건설 PF 우발채무 리스크 혼재</td>
          </tr>
          <tr>
            <td>Eaton (미국)</td>
            <td>북미 배전/전력 인프라 1위</td>
            <td>17.5% ~ 18.5%</td>
            <td>-</td>
            <td>35 ~ 38배</td>
            <td>북미 지배력 높으나 고평가 부담</td>
          </tr>
          <tr>
            <td>Schneider (프랑스)</td>
            <td>글로벌 에너지관리/배전 1위</td>
            <td>18.0% ~ 19.5%</td>
            <td>-</td>
            <td>30 ~ 33배</td>
            <td>유럽 경기 둔화 영향 일부 노출</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="footer-note">
      <span>* 출처: FnGuide, Bloomberg, 각 사 2026년 실적 컨센서스 집계</span>
      <span>※ LS일렉트릭은 글로벌 Peer 평균(30배+) 대비 약 40% 이상 저평가</span>
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
      color: #6366f1;
      font-weight: bold;
    }
    .bottom-box {
      background: rgba(99, 102, 241, 0.12);
      border: 1px solid rgba(99, 102, 241, 0.3);
      border-radius: 14px;
      padding: 14px 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 14px;
      color: #cbd5e1;
    }
    .bottom-box strong { color: #38bdf8; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <div class="title-group">
        <h2>AI 데이터센터 전력 계통 & LS일렉트릭 턴키 공급 체계</h2>
        <p>초고압 수전부터 서버 랙 정밀 배전까지 원스톱 풀스택 솔루션</p>
      </div>
      <div style="color:#818cf8; font-weight:700; font-size:14px;">TURN-KEY SOLUTION</div>
    </div>
    
    <div class="flow-wrapper">
      <div class="flow-step" style="border-top: 4px solid #3b82f6;">
        <div class="step-badge" style="background:rgba(59,130,246,0.2); color:#60a5fa;">STEP 01</div>
        <div class="step-title">초고압 송전 / 연계</div>
        <div class="step-desc">HVDC 변환소<br>500kV 초고압 GIS<br>국가 기간망 직결</div>
      </div>
      <div class="arrow">➔</div>
      <div class="flow-step" style="border-top: 4px solid #06b6d4;">
        <div class="step-badge" style="background:rgba(6,182,212,0.2); color:#22d3ee;">STEP 02</div>
        <div class="step-title">특고압 수전 / 강압</div>
        <div class="step-desc">345kV 초고압 변압기<br>부산 2공장 생산물량<br>대용량 전력 수전</div>
      </div>
      <div class="arrow">➔</div>
      <div class="flow-step" style="border-top: 4px solid #10b981;">
        <div class="step-badge" style="background:rgba(16,185,129,0.2); color:#34d399;">STEP 03</div>
        <div class="step-title">초슬림 내부 배전</div>
        <div class="step-desc">Beyond X MDB<br>면적 30% 절감 배전반<br>무정전 ACB/VCB 차단</div>
      </div>
      <div class="arrow">➔</div>
      <div class="flow-step" style="border-top: 4px solid #f59e0b;">
        <div class="step-badge" style="background:rgba(245,158,11,0.2); color:#fbbf24;">STEP 04</div>
        <div class="step-title">AI 서버 랙 공급</div>
        <div class="step-desc">GPU 고밀도 부하 제어<br>전력 효율성 극대화<br>스마트 원격 관제</div>
      </div>
    </div>

    <div class="bottom-box">
      <span>💡 <strong>LS일렉트릭의 독보적 강점</strong>: 송전-변전-배전 전 라인업을 일괄 납품하여 빅테크의 공기 단축 및 호환성 리스크 0% 달성</span>
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
    .m-op { font-size: 22px; font-weight: 900; color: #38bdf8; }
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
    .val-desc strong { color: #38bdf8; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <div class="title-group">
        <h2>LS일렉트릭 실적 퀀텀점프 및 저평가(PEG) 밸류에이션</h2>
        <p>부산공장 증설 가동으로 OPM 12% 돌파 및 EPS 연 30% 고속 성장</p>
      </div>
      <div style="color:#34d399; font-weight:700; font-size:14px;">VALUATION CHECK</div>
    </div>

    <div class="grid-top">
      <div class="metric-card">
        <div class="m-year">2024년 (확정)</div>
        <div class="m-rev">매출 4.58조</div>
        <div class="m-op" style="color:#cbd5e1;">3,920억</div>
        <div class="m-opm">OPM 8.6%</div>
      </div>
      <div class="metric-card">
        <div class="m-year">2025년 (확정)</div>
        <div class="m-rev">매출 4.96조</div>
        <div class="m-op" style="color:#cbd5e1;">4,269억</div>
        <div class="m-opm">OPM 8.6%</div>
      </div>
      <div class="metric-card" style="border: 1.5px solid #38bdf8; background: rgba(56,189,248,0.1);">
        <div class="m-year" style="color:#38bdf8;">2026년 (E)</div>
        <div class="m-rev">매출 5.65조</div>
        <div class="m-op">6,500억</div>
        <div class="m-opm">OPM 11.5% (급상승)</div>
      </div>
      <div class="metric-card" style="border: 1.5px solid #818cf8; background: rgba(129,140,248,0.1);">
        <div class="m-year" style="color:#818cf8;">2027년 (E)</div>
        <div class="m-rev">매출 6.40조</div>
        <div class="m-op" style="color:#818cf8;">8,200억</div>
        <div class="m-opm">OPM 12.8% (최고치)</div>
      </div>
    </div>

    <div class="grid-bottom">
      <div class="val-card">
        <div class="val-title">📊 피터 린치 PEG 0.54~0.60x 딥 밸류</div>
        <p class="val-desc">연평균 순이익 성장률 <strong>30.5%</strong> 대비 2026년 Forward PER은 <strong>16.5배</strong>에 불과합니다. 피터 린치 기준 <strong>PEG 1.0 미만은 매력적 저평가, 0.6x는 강력 매수 구간</strong>입니다.</p>
      </div>
      <div class="val-card">
        <div class="val-title">🚀 목표 PER 22배 멀티플 리레이팅</div>
        <p class="val-desc">HD현대일렉트릭(PER 28배) 및 Eaton(PER 35배) 대비 40% 이상 할인된 상태입니다. 부산공장 가동과 AI 배전반 확대로 <strong>목표주가 270,000~310,000원</strong>의 상승여력을 보유합니다.</p>
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
            print(f"[OK] Generated: {output_file}")
            await page.close()
        await browser.close()

if __name__ == "__main__":
    asyncio.run(generate_images())
