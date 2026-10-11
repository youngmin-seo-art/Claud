import asyncio
import os
from pathlib import Path
from playwright.async_api import async_playwright

OUTPUT_DIR = Path(r"c:\Users\immnu\Desktop\Claud\blog new agent\output\오늘의-증시-시황-글로벌-국내-마켓브리핑\images")
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
      background: linear-gradient(135deg, #090d16 0%, #111827 50%, #1e1b4b 100%);
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
      right: -100px;
      background: radial-gradient(circle, rgba(99, 102, 241, 0.3) 0%, transparent 70%);
      filter: blur(70px);
    }
    .glow-2 {
      position: absolute;
      width: 550px;
      height: 550px;
      bottom: -120px;
      left: -100px;
      background: radial-gradient(circle, rgba(16, 185, 129, 0.25) 0%, transparent 70%);
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
      padding: 70px 50px;
      backdrop-filter: blur(16px);
      box-shadow: 0 30px 60px rgba(0, 0, 0, 0.5);
      position: relative;
      z-index: 10;
    }
    .header-badge {
      display: inline-flex;
      align-items: center;
      gap: 10px;
      font-size: 20px;
      font-weight: 700;
      color: #818cf8;
      background: rgba(99, 102, 241, 0.15);
      border: 1px solid rgba(99, 102, 241, 0.35);
      padding: 12px 28px;
      border-radius: 9999px;
      letter-spacing: 0.5px;
    }
    .main-content {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 20px;
      width: 100%;
    }
    .title {
      font-size: 56px;
      font-weight: 900;
      line-height: 1.25;
      word-break: keep-all;
      background: linear-gradient(180deg, #ffffff 0%, #cbd5e1 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .subtitle {
      font-size: 26px;
      font-weight: 500;
      color: #94a3b8;
      line-height: 1.45;
      word-break: keep-all;
      max-width: 820px;
    }
    .stats-row {
      display: flex;
      gap: 16px;
      width: 100%;
      justify-content: center;
      margin-top: 10px;
    }
    .stat-pill {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 20px;
      padding: 18px 24px;
      display: flex;
      flex-direction: column;
      gap: 6px;
      min-width: 230px;
      text-align: center;
    }
    .stat-label {
      font-size: 15px;
      color: #94a3b8;
      font-weight: 600;
    }
    .stat-val {
      font-size: 24px;
      font-weight: 800;
      color: #f8fafc;
    }
    .down { color: #f87171 !important; }
    .up { color: #34d399 !important; }
    .footer-brand {
      font-size: 18px;
      font-weight: 700;
      color: #64748b;
      letter-spacing: 1.5px;
      text-transform: uppercase;
    }
    .footer-brand span { color: #818cf8; }
  </style>
</head>
<body>
  <div class="glow-1"></div>
  <div class="glow-2"></div>
  <div class="card">
    <div class="header-badge">
      <span>📊</span> VALUESTOCKLABS 오늘의 시황 브리핑
    </div>
    <div class="main-content">
      <h1 class="title">코스피 6,600선 조정과<br>뉴욕증시 3대 지수 반등</h1>
      <p class="subtitle">삼성전자 사상 최대 실적 후 '셀온' 현상 & 3분기 어닝시즌 투자 전략</p>
      <div class="stats-row">
        <div class="stat-pill">
          <div class="stat-label">KOSPI</div>
          <div class="stat-val down">6,625.93 (-2.62%)</div>
        </div>
        <div class="stat-pill">
          <div class="stat-label">NASDAQ</div>
          <div class="stat-val up">27,366.17 (+0.64%)</div>
        </div>
        <div class="stat-pill">
          <div class="stat-label">USD/KRW</div>
          <div class="stat-val">1,343.50 원</div>
        </div>
      </div>
    </div>
    <div class="footer-brand">
      ValueStock<span>Labs</span> · Daily Market Insight
    </div>
  </div>
</body>
</html>
"""

# 2. 본문 이미지 1 (1200x720): 비교 표 (국내외 주요 지수 및 수급 현황)
body_1_html = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 1200px;
      height: 720px;
      background: #0f172a;
      font-family: 'Pretendard', sans-serif;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      padding: 50px;
      color: #ffffff;
    }
    .header {
      width: 100%;
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      margin-bottom: 24px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
      padding-bottom: 16px;
    }
    .title-box h2 {
      font-size: 32px;
      font-weight: 800;
      color: #f8fafc;
      margin-bottom: 6px;
    }
    .title-box p {
      font-size: 16px;
      color: #94a3b8;
    }
    .tag {
      background: rgba(99, 102, 241, 0.2);
      border: 1px solid rgba(99, 102, 241, 0.4);
      color: #a5b4fc;
      font-size: 14px;
      font-weight: 700;
      padding: 6px 16px;
      border-radius: 9999px;
    }
    .table-card {
      width: 100%;
      background: rgba(30, 41, 59, 0.6);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 20px;
      overflow: hidden;
      box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
    }
    table {
      width: 100%;
      border-collapse: collapse;
      text-align: left;
    }
    th {
      background: rgba(15, 23, 42, 0.8);
      color: #94a3b8;
      font-size: 16px;
      font-weight: 700;
      padding: 18px 24px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    td {
      padding: 18px 24px;
      font-size: 18px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.06);
      color: #e2e8f0;
    }
    tr:last-child td { border-bottom: none; }
    .badge-dn {
      color: #f87171;
      font-weight: 800;
      background: rgba(239, 68, 68, 0.12);
      padding: 4px 12px;
      border-radius: 8px;
      display: inline-block;
    }
    .badge-up {
      color: #34d399;
      font-weight: 800;
      background: rgba(16, 185, 129, 0.12);
      padding: 4px 12px;
      border-radius: 8px;
      display: inline-block;
    }
    .highlight-name {
      font-weight: 700;
      color: #ffffff;
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .cntry-tag {
      font-size: 11px;
      font-weight: 800;
      color: #94a3b8;
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid rgba(255, 255, 255, 0.15);
      padding: 3px 8px;
      border-radius: 6px;
      letter-spacing: 0.5px;
    }
    .desc-cell {
      font-size: 15px;
      color: #94a3b8;
    }
  </style>
</head>
<body>
  <div class="header">
    <div class="title-box">
      <h2>글로벌 및 국내 주요 지수 등락 현황</h2>
      <p>10월 8일 국내 마감 및 10월 10일 뉴욕증시 마감 기준</p>
    </div>
    <div class="tag">KEY METRICS TABLE</div>
  </div>
  <div class="table-card">
    <table>
      <thead>
        <tr>
          <th>지수 / 시장</th>
          <th>마감 수치</th>
          <th>전일 대비 등락률</th>
          <th>수급 및 핵심 요인</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td class="highlight-name"><span class="cntry-tag">KOR</span> 코스피 (KOSPI)</td>
          <td><strong>6,625.93 pt</strong></td>
          <td><span class="badge-dn">-2.62% (-177.97)</span></td>
          <td class="desc-cell">외인·기관 -3.6조 동반 순매도 / 반도체 셀온</td>
        </tr>
        <tr>
          <td class="highlight-name"><span class="cntry-tag">KOR</span> 코스닥 (KOSDAQ)</td>
          <td><strong>892.27 pt</strong></td>
          <td><span class="badge-dn">-0.69% (-6.16)</span></td>
          <td class="desc-cell">바이오·소부장 순환매 유입으로 하방 경직성</td>
        </tr>
        <tr>
          <td class="highlight-name"><span class="cntry-tag">USA</span> 나스닥 (NASDAQ)</td>
          <td><strong>27,366.17 pt</strong></td>
          <td><span class="badge-up">+0.64% (+172.83)</span></td>
          <td class="desc-cell">엔비디아·애플 등 빅테크 메가캡 반등 주도</td>
        </tr>
        <tr>
          <td class="highlight-name"><span class="cntry-tag">USA</span> 다우존스 (DOW)</td>
          <td><strong>51,654.95 pt</strong></td>
          <td><span class="badge-up">+0.83% (+423.31)</span></td>
          <td class="desc-cell">금융주 및 우량 산업재 실적 기대감 선반영</td>
        </tr>
        <tr>
          <td class="highlight-name"><span class="cntry-tag">USA</span> S&P 500</td>
          <td><strong>7,811.54 pt</strong></td>
          <td><span class="badge-up">+0.59% (+46.18)</span></td>
          <td class="desc-cell">시장 금리 안정세와 기업 실적 낙관론 확산</td>
        </tr>
      </tbody>
    </table>
  </div>
</body>
</html>
"""

# 3. 본문 이미지 2 (1200x720): 핵심 포인트 카드 4종 (외환/금리/수급/빅테크)
body_2_html = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 1200px;
      height: 720px;
      background: #090d16;
      font-family: 'Pretendard', sans-serif;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      padding: 50px;
      color: #ffffff;
    }
    .header {
      width: 100%;
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      margin-bottom: 26px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
      padding-bottom: 16px;
    }
    .title-box h2 {
      font-size: 32px;
      font-weight: 800;
      color: #f8fafc;
      margin-bottom: 6px;
    }
    .title-box p {
      font-size: 16px;
      color: #94a3b8;
    }
    .tag {
      background: rgba(16, 185, 129, 0.2);
      border: 1px solid rgba(16, 185, 129, 0.4);
      color: #6ee7b7;
      font-size: 14px;
      font-weight: 700;
      padding: 6px 16px;
      border-radius: 9999px;
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 20px;
      width: 100%;
    }
    .card {
      background: rgba(30, 41, 59, 0.6);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 20px;
      padding: 28px 30px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      backdrop-filter: blur(10px);
      box-shadow: 0 15px 30px rgba(0,0,0,0.3);
    }
    .card-top {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 14px;
    }
    .card-badge {
      font-size: 14px;
      font-weight: 700;
      color: #94a3b8;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .card-metric {
      font-size: 26px;
      font-weight: 900;
      color: #f8fafc;
    }
    .card-title {
      font-size: 20px;
      font-weight: 800;
      color: #e2e8f0;
      margin-bottom: 8px;
    }
    .card-desc {
      font-size: 15px;
      color: #94a3b8;
      line-height: 1.5;
    }
    .pill-red { color: #f87171; }
    .pill-green { color: #34d399; }
    .pill-blue { color: #60a5fa; }
    .pill-yellow { color: #fbbf24; }
  </style>
</head>
<body>
  <div class="header">
    <div class="title-box">
      <h2>글로벌 마켓 핵심 지표 4대 포인트</h2>
      <p>외환 변동성 · 채권 금리 · 국내 수급 쏠림 · 미국 빅테크 동향</p>
    </div>
    <div class="tag">MARKET OVERVIEW</div>
  </div>
  <div class="grid">
    <div class="card">
      <div class="card-top">
        <div class="card-badge">💵 원/달러 환율 (FX)</div>
        <div class="card-metric pill-yellow">1,343.50 원</div>
      </div>
      <div class="card-title">단기 박스권 상단 저항</div>
      <div class="card-desc">1,341~1,345원 구간에서 팽팽한 공방전. 환율 추가 급등 제한 시 외국인 수급 복귀 여건 조성 기대.</div>
    </div>
    <div class="card">
      <div class="card-top">
        <div class="card-badge">📉 미국 10년물 국채 금리</div>
        <div class="card-metric pill-blue">안정세 유지</div>
      </div>
      <div class="card-title">기술주 밸류에이션 부담 완화</div>
      <div class="card-desc">연준의 금리 인하 사이클 재확인 속 채권 금리 진정. 나스닥 성장주 및 반도체 섹터 할인율 안정.</div>
    </div>
    <div class="card">
      <div class="card-top">
        <div class="card-badge">⚠️ 코스피 메이저 수급</div>
        <div class="card-metric pill-red">-3.6조 원</div>
      </div>
      <div class="card-title">외인·기관 동반 순매도 폭탄</div>
      <div class="card-desc">선물 매도 연계 프로그램 차익 청산 집중. 개인 2.9조 저가 매수 유입 속 단기 바닥 테스트 국면.</div>
    </div>
    <div class="card">
      <div class="card-top">
        <div class="card-badge">🚀 메가캡 빅테크</div>
        <div class="card-metric pill-green">엔비디아 주도 반등</div>
      </div>
      <div class="card-title">3분기 어닝시즌 기대감 확산</div>
      <div class="card-desc">AI 인프라 실적 확인 기대와 TSMC 실적 발표 대기. 기술적 지지선 확인 후 저가 매수세 강화.</div>
    </div>
  </div>
</body>
</html>
"""

# 4. 본문 이미지 3 (1200x720): 단계별 다이어그램 (투자 대응 4단계 로드맵)
body_3_html = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 1200px;
      height: 720px;
      background: #0f172a;
      font-family: 'Pretendard', sans-serif;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      padding: 50px;
      color: #ffffff;
    }
    .header {
      width: 100%;
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      margin-bottom: 30px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
      padding-bottom: 16px;
    }
    .title-box h2 {
      font-size: 32px;
      font-weight: 800;
      color: #f8fafc;
      margin-bottom: 6px;
    }
    .title-box p {
      font-size: 16px;
      color: #94a3b8;
    }
    .tag {
      background: rgba(99, 102, 241, 0.2);
      border: 1px solid rgba(99, 102, 241, 0.4);
      color: #a5b4fc;
      font-size: 14px;
      font-weight: 700;
      padding: 6px 16px;
      border-radius: 9999px;
    }
    .flow-container {
      display: flex;
      gap: 16px;
      width: 100%;
    }
    .step-card {
      flex: 1;
      background: rgba(30, 41, 59, 0.6);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 20px;
      padding: 30px 24px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      box-shadow: 0 15px 30px rgba(0, 0, 0, 0.3);
      position: relative;
    }
    .step-badge {
      display: inline-block;
      font-size: 13px;
      font-weight: 800;
      color: #818cf8;
      background: rgba(99, 102, 241, 0.15);
      border: 1px solid rgba(99, 102, 241, 0.3);
      padding: 6px 12px;
      border-radius: 9999px;
      margin-bottom: 18px;
    }
    .step-title {
      font-size: 21px;
      font-weight: 800;
      color: #ffffff;
      margin-bottom: 14px;
      line-height: 1.35;
    }
    .step-desc {
      font-size: 15px;
      color: #94a3b8;
      line-height: 1.6;
    }
    .step-footer {
      margin-top: 24px;
      padding-top: 16px;
      border-top: 1px solid rgba(255, 255, 255, 0.08);
      font-size: 13px;
      font-weight: 700;
      color: #38bdf8;
    }
  </style>
</head>
<body>
  <div class="header">
    <div class="title-box">
      <h2>3분기 어닝시즌 투자자 실전 대응 4단계 로드맵</h2>
      <p>조정장 속 심리 안정과 성공적인 분할 매수 포트폴리오 전략</p>
    </div>
    <div class="tag">STRATEGY ROADMAP</div>
  </div>
  <div class="flow-container">
    <div class="step-card">
      <div>
        <div class="step-badge">STEP 01</div>
        <div class="step-title">코스피 6,600선<br>지지력 확인</div>
        <div class="step-desc">외국인 선물 매도세 둔화 및 선물 베이시스 개선 여부를 가장 먼저 확인합니다.</div>
      </div>
      <div class="step-footer">체크: 외인 현·선물 수급</div>
    </div>
    <div class="step-card">
      <div>
        <div class="step-badge">STEP 02</div>
        <div class="step-title">반도체 대형주<br>분할 매수 타이밍</div>
        <div class="step-desc">실적 피크아웃 우려가 과도한 우량 반도체(삼성·하이닉스)의 낙폭 과대 구간 분할 접근.</div>
      </div>
      <div class="step-footer">전략: 2~3회 분할 진입</div>
    </div>
    <div class="step-card">
      <div>
        <div class="step-badge">STEP 03</div>
        <div class="step-title">수주·실적주<br>순환매 동승</div>
        <div class="step-desc">실적 가시성이 검증된 방산, 조선, 고배당 밸류업 금융주로 방어적 포트폴리오 보강.</div>
      </div>
      <div class="step-footer">타깃: 한화에어로·삼성중공업</div>
    </div>
    <div class="step-card">
      <div>
        <div class="step-badge">STEP 04</div>
        <div class="step-title">글로벌 실적<br>슈퍼위크 대비</div>
        <div class="step-desc">TSMC, 빅테크 및 미국 주요 은행 실적 발표에 따른 글로벌 투자 심리 변화 점검.</div>
      </div>
      <div class="step-footer">일정: TSMC·빅테크 어닝</div>
    </div>
  </div>
</body>
</html>
"""

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        tasks = [
            ("thumbnail.png", thumbnail_html, 1080, 1080),
            ("body-1.png", body_1_html, 1200, 720),
            ("body-2.png", body_2_html, 1200, 720),
            ("body-3.png", body_3_html, 1200, 720),
        ]

        for filename, html, w, h in tasks:
            page = await browser.new_page(viewport={"width": w, "height": h}, device_scale_factor=2)
            await page.set_content(html, wait_until="networkidle")
            out_path = OUTPUT_DIR / filename
            await page.screenshot(path=str(out_path), type="png")
            await page.close()
            print(f"[성공] 생성 완료: {out_path} ({w}x{h})")

        await browser.close()
    print("모든 이미지 제작이 완료되었습니다.")

if __name__ == "__main__":
    asyncio.run(main())
