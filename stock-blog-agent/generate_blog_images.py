import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

OUTPUT_DIR = Path(r"c:\Users\immnu\Desktop\Claud\output\주식-EOS-저평가-종목-발굴법\images")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 1. Thumbnail (1080 x 1080)
HTML_THUMBNAIL = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 1080px;
      height: 1080px;
      background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f172a 100%);
      font-family: 'Pretendard', sans-serif;
      display: flex;
      justify-content: center;
      align-items: center;
      color: #ffffff;
      padding: 70px;
      overflow: hidden;
      position: relative;
    }
    .bg-circle-1 {
      position: absolute;
      width: 450px;
      height: 450px;
      top: -50px;
      right: -50px;
      background: radial-gradient(circle, rgba(99, 102, 241, 0.25) 0%, rgba(99, 102, 241, 0) 70%);
      border-radius: 50%;
    }
    .bg-circle-2 {
      position: absolute;
      width: 500px;
      height: 500px;
      bottom: -80px;
      left: -80px;
      background: radial-gradient(circle, rgba(6, 182, 212, 0.2) 0%, rgba(6, 182, 212, 0) 70%);
      border-radius: 50%;
    }
    .card {
      width: 100%;
      height: 100%;
      background: rgba(255, 255, 255, 0.035);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 36px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      text-align: center;
      padding: 60px;
      box-shadow: 0 30px 60px rgba(0, 0, 0, 0.5);
      backdrop-filter: blur(20px);
      z-index: 1;
    }
    .badge {
      font-size: 20px;
      font-weight: 700;
      color: #818cf8;
      background: rgba(99, 102, 241, 0.18);
      border: 1px solid rgba(99, 102, 241, 0.35);
      padding: 10px 28px;
      border-radius: 9999px;
      margin-bottom: 40px;
      letter-spacing: 1.5px;
      text-transform: uppercase;
    }
    .title {
      font-size: 56px;
      font-weight: 800;
      line-height: 1.35;
      margin-bottom: 28px;
      word-break: keep-all;
      background: linear-gradient(180deg, #ffffff 0%, #cbd5e1 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .divider {
      width: 80px;
      height: 4px;
      background: linear-gradient(90deg, #6366f1, #06b6d4);
      border-radius: 2px;
      margin-bottom: 30px;
    }
    .subtitle {
      font-size: 26px;
      font-weight: 500;
      color: #94a3b8;
      line-height: 1.5;
      word-break: keep-all;
      max-width: 750px;
    }
  </style>
</head>
<body>
  <div class="bg-circle-1"></div>
  <div class="bg-circle-2"></div>
  <div class="card">
    <div class="badge">Value Stock Valuation Guide</div>
    <h1 class="title">EPS 기반 저평가주<br>찾는 법</h1>
    <div class="divider"></div>
    <p class="subtitle">Forward PER · PEG 공식과 4단계 실전 퀀트 스크리닝</p>
  </div>
</body>
</html>
"""

# 2. Body-1: 4단계 가치투자 스크리닝 인포그래픽 (1080 x 640)
HTML_BODY_1 = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 1080px;
      height: 640px;
      background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
      font-family: 'Pretendard', sans-serif;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      padding: 40px;
      color: #ffffff;
    }
    .header {
      text-align: center;
      margin-bottom: 35px;
    }
    .tag {
      font-size: 15px;
      font-weight: 700;
      color: #38bdf8;
      background: rgba(56, 189, 248, 0.15);
      border: 1px solid rgba(56, 189, 248, 0.3);
      padding: 6px 18px;
      border-radius: 9999px;
      display: inline-block;
      margin-bottom: 10px;
    }
    .title {
      font-size: 32px;
      font-weight: 800;
      color: #f8fafc;
    }
    .steps-container {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
      width: 100%;
    }
    .step-card {
      background: rgba(30, 41, 59, 0.7);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 20px;
      padding: 24px 18px;
      display: flex;
      flex-direction: column;
      position: relative;
    }
    .step-num {
      font-size: 13px;
      font-weight: 800;
      color: #818cf8;
      background: rgba(99, 102, 241, 0.2);
      padding: 4px 10px;
      border-radius: 6px;
      width: fit-content;
      margin-bottom: 12px;
    }
    .step-title {
      font-size: 19px;
      font-weight: 700;
      color: #ffffff;
      margin-bottom: 10px;
      line-height: 1.3;
    }
    .step-desc {
      font-size: 14px;
      color: #94a3b8;
      line-height: 1.5;
    }
    .highlight {
      color: #38bdf8;
      font-weight: 600;
    }
  </style>
</head>
<body>
  <div class="header">
    <div class="tag">4-STEP FRAMEWORK</div>
    <h2 class="title">EPS 기반 4단계 저평가 종목 발굴 로드맵</h2>
  </div>
  <div class="steps-container">
    <div class="step-card">
      <div class="step-num">STEP 01</div>
      <div class="step-title">Forward EPS</div>
      <div class="step-desc">과거 실적 착시 제거<br><span class="highlight">선행 12개월 추정치</span> 상향 여부 확인</div>
    </div>
    <div class="step-card">
      <div class="step-num">STEP 02</div>
      <div class="step-title">업종 PER 밴드</div>
      <div class="step-desc">동종 업계 대비<br><span class="highlight">20~30% 할인</span> 및 5개년 하단 검증</div>
    </div>
    <div class="step-card">
      <div class="step-num">STEP 03</div>
      <div class="step-title">피터 린치 PEG</div>
      <div class="step-desc">성장성 대비 가치<br><span class="highlight">PEG ≤ 1.0</span> (0.5 이하 강력 매수)</div>
    </div>
    <div class="step-card">
      <div class="step-num">STEP 04</div>
      <div class="step-title">그레이엄 공식</div>
      <div class="step-desc">내재가치 계산 및<br><span class="highlight">안전마진 30%</span> 확보 후 분할 매수</div>
    </div>
  </div>
</body>
</html>
"""

# 3. Body-2: EOS 키워드 3가지 의미 비교 다이어그램 (1080 x 640)
HTML_BODY_2 = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 1080px;
      height: 640px;
      background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
      font-family: 'Pretendard', sans-serif;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      padding: 40px;
      color: #ffffff;
    }
    .header {
      text-align: center;
      margin-bottom: 30px;
    }
    .tag {
      font-size: 15px;
      font-weight: 700;
      color: #a855f7;
      background: rgba(168, 85, 247, 0.15);
      border: 1px solid rgba(168, 85, 247, 0.3);
      padding: 6px 18px;
      border-radius: 9999px;
      display: inline-block;
      margin-bottom: 10px;
    }
    .title {
      font-size: 30px;
      font-weight: 800;
      color: #f8fafc;
    }
    .grid {
      display: grid;
      grid-template-columns: 1.2fr 1fr 1fr;
      gap: 20px;
      width: 100%;
    }
    .card {
      background: rgba(30, 41, 59, 0.8);
      border-radius: 20px;
      padding: 26px 22px;
      border: 1px solid rgba(255, 255, 255, 0.08);
      display: flex;
      flex-direction: column;
    }
    .card.primary {
      border: 1.5px solid #6366f1;
      background: rgba(99, 102, 241, 0.1);
    }
    .card-badge {
      font-size: 12px;
      font-weight: 700;
      padding: 4px 10px;
      border-radius: 6px;
      width: fit-content;
      margin-bottom: 12px;
    }
    .badge-blue { background: #6366f1; color: #ffffff; }
    .badge-gray { background: #475569; color: #cbd5e1; }
    .card-title {
      font-size: 21px;
      font-weight: 700;
      color: #ffffff;
      margin-bottom: 10px;
    }
    .card-content {
      font-size: 14px;
      color: #94a3b8;
      line-height: 1.6;
    }
    .point {
      color: #38bdf8;
      font-weight: 600;
    }
  </style>
</head>
<body>
  <div class="header">
    <div class="tag">KEYWORD ANALYSIS</div>
    <h2 class="title">주식 시장에서 'EOS' 키워드의 3가지 의미</h2>
  </div>
  <div class="grid">
    <div class="card primary">
      <div class="card-badge badge-blue">핵심 밸류에이션</div>
      <div class="card-title">EPS (주당순이익) 오타</div>
      <div class="card-content">
        • QWERTY 자판상 P-O 인접 오타<br>
        • <span class="point">본질: 기업 순이익 기반 가치평가</span><br>
        • PER, PEG, ROE와 결합하여 알짜 저평가주 발굴의 근간
      </div>
    </div>
    <div class="card">
      <div class="card-badge badge-gray">미국 나스닥 상장사</div>
      <div class="card-title">Eos Energy (EOSE)</div>
      <div class="card-content">
        • 아연 배터리 ESS 제조 기업<br>
        • 구글·대형 전력사 공급 모멘텀<br>
        • <span class="point">주의: 지속 적자로 재무 리스크 점검 필수</span>
      </div>
    </div>
    <div class="card">
      <div class="card-badge badge-gray">호주 ASX 상장사</div>
      <div class="card-title">EOS Holdings (EOS)</div>
      <div class="card-content">
        • 호주 방산·우주 광학 시스템<br>
        • AI 드론 방어 체계 수출 확대<br>
        • <span class="point">방산 수주 및 매출 성장세 주목</span>
      </div>
    </div>
  </div>
</body>
</html>
"""

# 4. Body-3: Trailing vs Forward EPS 비교 플로우 (1080 x 640)
HTML_BODY_3 = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 1080px;
      height: 640px;
      background: linear-gradient(135deg, #090d16 0%, #1a1e2e 100%);
      font-family: 'Pretendard', sans-serif;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      padding: 40px;
      color: #ffffff;
    }
    .header {
      text-align: center;
      margin-bottom: 25px;
    }
    .title {
      font-size: 30px;
      font-weight: 800;
      color: #ffffff;
    }
    .compare-container {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 24px;
      width: 100%;
      margin-bottom: 20px;
    }
    .box {
      background: rgba(30, 41, 59, 0.7);
      border-radius: 20px;
      padding: 24px;
      border: 1px solid rgba(255, 255, 255, 0.08);
    }
    .box.forward {
      border: 1.5px solid #10b981;
      background: rgba(16, 185, 129, 0.08);
    }
    .box-title {
      font-size: 20px;
      font-weight: 700;
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .box-title.trailing { color: #94a3b8; }
    .box-title.forward { color: #34d399; }
    .item-list {
      list-style: none;
      font-size: 14.5px;
      color: #cbd5e1;
      line-height: 1.7;
    }
    .banner {
      width: 100%;
      background: linear-gradient(90deg, rgba(99, 102, 241, 0.2), rgba(6, 182, 212, 0.2));
      border: 1px solid rgba(99, 102, 241, 0.4);
      border-radius: 14px;
      padding: 14px 24px;
      text-align: center;
      font-size: 16px;
      font-weight: 600;
      color: #e0e7ff;
    }
  </style>
</head>
<body>
  <div class="header">
    <h2 class="title">Trailing EPS vs Forward EPS 비교</h2>
  </div>
  <div class="compare-container">
    <div class="box">
      <div class="box-title trailing">⚠️ Trailing EPS (과거 12개월)</div>
      <ul class="item-list">
        <li>• 이미 주가에 반영 완료된 후행성 지표</li>
        <li>• 부동산/지분 매각 등 일회성 특별이익 착시 위험</li>
        <li>• 업황 꺾일 때 주가 급락 전 저PER 착시 발생</li>
      </ul>
    </div>
    <div class="box forward">
      <div class="box-title forward">✨ Forward EPS (향후 12개월) [추천]</div>
      <ul class="item-list">
        <li>• 증권사 애널리스트 실적 컨센서스 반영</li>
        <li>• 기업의 실질적인 미래 이익 창출력 평가</li>
        <li>• 실적 상향 조정 중인 미반영 종목 발굴에 최적</li>
      </ul>
    </div>
  </div>
  <div class="banner">
    💡 핵심 전략: "Forward EPS가 지속 상향 조정되나 주가가 아직 반응하지 않은 종목을 선점하라"
  </div>
</body>
</html>
"""

# 5. Body-4: 피터 린치 PEG Ratio 해석 기준 (1080 x 640)
HTML_BODY_4 = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 1080px;
      height: 640px;
      background: linear-gradient(135deg, #111827 0%, #1e1b4b 100%);
      font-family: 'Pretendard', sans-serif;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      padding: 40px;
      color: #ffffff;
    }
    .header {
      text-align: center;
      margin-bottom: 25px;
    }
    .title {
      font-size: 30px;
      font-weight: 800;
      color: #f8fafc;
      margin-bottom: 8px;
    }
    .formula-box {
      background: rgba(99, 102, 241, 0.15);
      border: 1px dashed #818cf8;
      border-radius: 12px;
      padding: 10px 24px;
      font-size: 17px;
      font-weight: 700;
      color: #c7d2fe;
      font-family: monospace;
      margin-bottom: 25px;
    }
    .peg-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 16px;
      width: 100%;
    }
    .peg-card {
      border-radius: 18px;
      padding: 24px 20px;
      display: flex;
      flex-direction: column;
      text-align: center;
    }
    .peg-card.green {
      background: rgba(16, 185, 129, 0.12);
      border: 1.5px solid #10b981;
    }
    .peg-card.blue {
      background: rgba(56, 189, 248, 0.12);
      border: 1.5px solid #38bdf8;
    }
    .peg-card.red {
      background: rgba(239, 68, 68, 0.12);
      border: 1.5px solid #ef4444;
    }
    .peg-val {
      font-size: 26px;
      font-weight: 800;
      margin-bottom: 8px;
    }
    .green .peg-val { color: #34d399; }
    .blue .peg-val { color: #38bdf8; }
    .red .peg-val { color: #f87171; }
    .peg-status {
      font-size: 18px;
      font-weight: 700;
      color: #ffffff;
      margin-bottom: 8px;
    }
    .peg-desc {
      font-size: 13.5px;
      color: #94a3b8;
      line-height: 1.5;
    }
  </style>
</head>
<body>
  <div class="header">
    <h2 class="title">피터 린치의 PEG Ratio 밸류에이션 기준</h2>
  </div>
  <div class="formula-box">
    PEG = Forward PER ÷ 연평균 예상 EPS 성장률(%)
  </div>
  <div class="peg-grid">
    <div class="peg-card green">
      <div class="peg-val">PEG ≤ 0.5</div>
      <div class="peg-status">극심한 저평가</div>
      <div class="peg-desc">성장성 대비 주가 매우 저렴<br><strong>강력 매수 검토 구간</strong></div>
    </div>
    <div class="peg-card blue">
      <div class="peg-val">0.5 < PEG ≤ 1.0</div>
      <div class="peg-status">합리적 저평가</div>
      <div class="peg-desc">성장성과 가격의 균형<br><strong>매력적인 가치성장주</strong></div>
    </div>
    <div class="peg-card red">
      <div class="peg-val">PEG > 1.5</div>
      <div class="peg-status">고평가 국면</div>
      <div class="peg-desc">성장성 대비 과도한 프리미엄<br><strong>보수적 접근 필요</strong></div>
    </div>
  </div>
</body>
</html>
"""

# 6. Body-5: 실전 퀀트 스크리닝 7가지 필터 조건식 (1080 x 640)
HTML_BODY_5 = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 1080px;
      height: 640px;
      background: linear-gradient(135deg, #0a0f1d 0%, #161e31 100%);
      font-family: 'Pretendard', sans-serif;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      padding: 35px 40px;
      color: #ffffff;
    }
    .header {
      text-align: center;
      margin-bottom: 20px;
    }
    .title {
      font-size: 28px;
      font-weight: 800;
      color: #f8fafc;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      background: rgba(30, 41, 59, 0.7);
      border-radius: 16px;
      overflow: hidden;
      border: 1px solid rgba(255, 255, 255, 0.1);
    }
    th {
      background: rgba(99, 102, 241, 0.25);
      color: #c7d2fe;
      font-size: 15px;
      font-weight: 700;
      padding: 12px 16px;
      text-align: left;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    td {
      padding: 10px 16px;
      font-size: 14px;
      color: #e2e8f0;
      border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }
    tr:last-child td { border-bottom: none; }
    .badge {
      font-weight: 700;
      color: #38bdf8;
      font-family: monospace;
      background: rgba(56, 189, 248, 0.12);
      padding: 3px 8px;
      border-radius: 4px;
    }
  </style>
</head>
<body>
  <div class="header">
    <h2 class="title">실전 퀀트 스크리닝 7가지 핵심 필터 조건식</h2>
  </div>
  <table>
    <thead>
      <tr>
        <th style="width: 22%;">지표 구분</th>
        <th style="width: 38%;">권장 스크리닝 기준</th>
        <th style="width: 40%;">분석 목적 및 기대 효과</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Forward EPS</strong></td>
        <td><span class="badge">3개년 CAGR ≥ 15%</span></td>
        <td>지속적인 이익 성장 모멘텀 확보</td>
      </tr>
      <tr>
        <td><strong>Forward PER</strong></td>
        <td><span class="badge">동종 업종 평균의 ≤ 70%</span></td>
        <td>업종 대비 상대적 가격 매력도</td>
      </tr>
      <tr>
        <td><strong>PEG Ratio</strong></td>
        <td><span class="badge">0 < PEG ≤ 1.0 (최적 0.7)</span></td>
        <td>성장성 대비 저평가 여부 검증</td>
      </tr>
      <tr>
        <td><strong>ROE</strong></td>
        <td><span class="badge">3년 평균 ≥ 12%</span></td>
        <td>자본 대비 수익 창출 효율성</td>
      </tr>
      <tr>
        <td><strong>부채비율</strong></td>
        <td><span class="badge">≤ 100%</span></td>
        <td>고금리 환경 재무 건전성</td>
      </tr>
      <tr>
        <td><strong>영업현금흐름</strong></td>
        <td><span class="badge">영업현금흐름 > 순이익</span></td>
        <td>장부상 이익 아닌 실제 현금 검증</td>
      </tr>
      <tr>
        <td><strong>유동비율</strong></td>
        <td><span class="badge">≥ 150%</span></td>
        <td>1년 이내 단기 채무 상환 능력</td>
      </tr>
    </tbody>
  </table>
</body>
</html>
"""

# 7. Body-6: 가치 함정(Value Trap) 회피 3대 체크포인트 (1080 x 640)
HTML_BODY_6 = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 1080px;
      height: 640px;
      background: linear-gradient(135deg, #180d1e 0%, #0f172a 100%);
      font-family: 'Pretendard', sans-serif;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      padding: 40px;
      color: #ffffff;
    }
    .header {
      text-align: center;
      margin-bottom: 30px;
    }
    .tag {
      font-size: 15px;
      font-weight: 700;
      color: #f43f5e;
      background: rgba(244, 63, 94, 0.15);
      border: 1px solid rgba(244, 63, 94, 0.3);
      padding: 6px 18px;
      border-radius: 9999px;
      display: inline-block;
      margin-bottom: 10px;
    }
    .title {
      font-size: 30px;
      font-weight: 800;
      color: #ffffff;
    }
    .cards-container {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 20px;
      width: 100%;
    }
    .card {
      background: rgba(30, 41, 59, 0.75);
      border: 1px solid rgba(244, 63, 94, 0.25);
      border-radius: 20px;
      padding: 26px 20px;
      display: flex;
      flex-direction: column;
    }
    .icon-badge {
      font-size: 24px;
      margin-bottom: 12px;
    }
    .card-title {
      font-size: 19px;
      font-weight: 700;
      color: #fecdd3;
      margin-bottom: 10px;
      line-height: 1.3;
    }
    .card-desc {
      font-size: 14px;
      color: #94a3b8;
      line-height: 1.6;
    }
  </style>
</head>
<body>
  <div class="header">
    <div class="tag">RISK MANAGEMENT</div>
    <h2 class="title">가치 함정(Value Trap) 회피 3대 체크포인트</h2>
  </div>
  <div class="cards-container">
    <div class="card">
      <div class="icon-badge">🏢</div>
      <div class="card-title">일회성 특별이익 제외</div>
      <div class="card-desc">
        부동산 매각, 지분 처분 등 일시적 순이익 급증으로 PER이 낮아진 착시 종목을 철저히 분리 검증
      </div>
    </div>
    <div class="card">
      <div class="icon-badge">📈</div>
      <div class="card-title">경기 순환주 정점 주의</div>
      <div class="card-desc">
        해운·화학·철강 등 경기민감주는 실적 피크 시 PER이 최저를 기록하므로 업황 사이클 위치 점검
      </div>
    </div>
    <div class="card">
      <div class="icon-badge">💵</div>
      <div class="card-title">잉여현금흐름(FCF) 확인</div>
      <div class="card-desc">
        장부상 흑자라도 FCF가 만년 마이너스이거나 주주환원이 전무한 기업은 만년 저평가 위험
      </div>
    </div>
  </div>
</body>
</html>
"""

ALL_TEMPLATES = [
    ("thumbnail.png", HTML_THUMBNAIL, 1080, 1080),
    ("body-1.png", HTML_BODY_1, 1080, 640),
    ("body-2.png", HTML_BODY_2, 1080, 640),
    ("body-3.png", HTML_BODY_3, 1080, 640),
    ("body-4.png", HTML_BODY_4, 1080, 640),
    ("body-5.png", HTML_BODY_5, 1080, 640),
    ("body-6.png", HTML_BODY_6, 1080, 640),
]

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        for filename, html_content, width, height in ALL_TEMPLATES:
            page = await browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=2)
            await page.set_content(html_content, wait_until="networkidle")
            out_file = OUTPUT_DIR / filename
            await page.screenshot(path=str(out_file), type="png")
            await page.close()
            print(f"[OK] Generated: {out_file}")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
