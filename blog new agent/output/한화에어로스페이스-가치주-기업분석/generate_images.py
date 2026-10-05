import asyncio
import os
from pathlib import Path
from playwright.async_api import async_playwright

OUTPUT_DIR = Path(r"c:\Users\immnu\Desktop\Claud\blog new agent\output\한화에어로스페이스-가치주-기업분석\images")
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
      background: radial-gradient(circle, rgba(59, 130, 246, 0.3) 0%, transparent 70%);
      filter: blur(70px);
    }
    .glow-2 {
      position: absolute;
      width: 550px;
      height: 550px;
      bottom: -120px;
      left: -120px;
      background: radial-gradient(circle, rgba(234, 88, 12, 0.25) 0%, transparent 70%);
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
      font-size: 30px;
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
      background: linear-gradient(90deg, #38bdf8 0%, #f97316 100%);
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
      letter-spacing: 1px;
    }
  </style>
</head>
<body>
  <div class="glow-1"></div>
  <div class="glow-2"></div>
  <div class="card">
    <div class="badge">
      <span class="dot"></span>
      VALUESTOCKLABS · K-방산 대장주 심층분석
    </div>
    <div class="title-box">
      <div class="title-sub">012450 · 코스피 시총 55조</div>
      <h1 class="title-main">한화에어로스페이스<br><span class="highlight">주가 전망 & 종목분석</span></h1>
    </div>
    <div class="stats-row">
      <div class="stat-card">
        <div class="stat-label">방산 수주잔고</div>
        <div class="stat-value orange">38.3조+</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">2026(F) 예상 매출</div>
        <div class="stat-value">31.8조 원</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">2026(F) 영업이익</div>
        <div class="stat-value green">4.6조 원</div>
      </div>
    </div>
    <div class="footer-tag">K9 자주포 · 천무 · 레드백 · 항공우주 엔진 · 한화오션 시너지</div>
  </div>
</body>
</html>
"""

# 3. 본문 3: 실적 추이 바 차트 및 지표 (개선 버전: 1080x640)
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
      padding: 40px;
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
      padding-bottom: 16px;
    }
    .header h2 {
      font-size: 26px;
      font-weight: 800;
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .tag {
      font-size: 14px;
      font-weight: 600;
      background: rgba(16, 185, 129, 0.15);
      color: #34d399;
      border: 1px solid rgba(16, 185, 129, 0.35);
      padding: 6px 14px;
      border-radius: 9999px;
    }
    .chart-container {
      display: grid;
      grid-template-columns: 1.4fr 1fr;
      gap: 24px;
      margin: 18px 0;
      flex: 1;
    }
    .bars-card {
      background: rgba(15, 23, 42, 0.7);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 20px;
      padding: 22px 24px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .bars-title {
      font-size: 16px;
      font-weight: 700;
      color: #94a3b8;
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 8px;
    }
    .bar-group {
      display: flex;
      flex-direction: column;
      gap: 12px;
    }
    .year-row {
      display: flex;
      flex-direction: column;
      gap: 5px;
      background: rgba(0, 0, 0, 0.2);
      padding: 10px 14px;
      border-radius: 12px;
      border: 1px solid rgba(255, 255, 255, 0.03);
    }
    .year-row.active {
      border-color: rgba(56, 189, 248, 0.3);
      background: rgba(14, 165, 233, 0.05);
    }
    .year-label {
      display: flex;
      justify-content: space-between;
      font-size: 13.5px;
      font-weight: 700;
      color: #e2e8f0;
    }
    .bar-wrapper {
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .bar-name {
      font-size: 11px;
      color: #94a3b8;
      width: 44px;
    }
    .bar-track {
      flex: 1;
      height: 18px;
      background: rgba(255, 255, 255, 0.05);
      border-radius: 6px;
      overflow: hidden;
      display: flex;
    }
    .bar-fill-sales {
      height: 100%;
      background: linear-gradient(90deg, #0284c7 0%, #38bdf8 100%);
      border-radius: 6px;
    }
    .bar-fill-op {
      height: 100%;
      background: linear-gradient(90deg, #059669 0%, #34d399 100%);
      border-radius: 6px;
    }
    .bar-val-text {
      font-size: 12.5px;
      font-weight: 700;
      color: #e2e8f0;
      min-width: 85px;
      text-align: right;
    }
    .bar-val-text.green { color: #34d399; }
    .bar-val-text.blue { color: #38bdf8; }
    .metrics-card {
      display: flex;
      flex-direction: column;
      gap: 12px;
      justify-content: center;
    }
    .metric-box {
      background: rgba(15, 23, 42, 0.7);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 16px;
      padding: 16px 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .metric-box.highlight {
      border-color: rgba(56, 189, 248, 0.4);
      background: linear-gradient(135deg, rgba(56, 189, 248, 0.1) 0%, rgba(15, 23, 42, 0.8) 100%);
    }
    .metric-name {
      font-size: 14px;
      color: #94a3b8;
    }
    .metric-val {
      font-size: 22px;
      font-weight: 800;
      color: #ffffff;
    }
    .metric-val.green { color: #34d399; }
    .metric-val.blue { color: #38bdf8; }
    .metric-val.orange { color: #fb923c; }
    .legend {
      display: flex;
      gap: 14px;
      font-size: 12px;
      color: #94a3b8;
    }
    .legend-item {
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .legend-dot {
      width: 10px;
      height: 10px;
      border-radius: 3px;
    }
  </style>
</head>
<body>
  <div class="header">
    <h2>📈 2024~2026년 실적 추이 및 폭발적 성장 전망</h2>
    <span class="tag">매출 30조 · 영업이익 4.5조 시대 개막</span>
  </div>

  <div class="chart-container">
    <!-- 바 차트 -->
    <div class="bars-card">
      <div class="bars-title">
        <span>연간 매출 & 영업이익 추이</span>
        <div class="legend">
          <div class="legend-item"><span class="legend-dot" style="background:#38bdf8;"></span> 매출액</div>
          <div class="legend-item"><span class="legend-dot" style="background:#34d399;"></span> 영업이익</div>
        </div>
      </div>

      <div class="bar-group">
        <!-- 2024 -->
        <div class="year-row">
          <div class="year-label">
            <span>2024 (A) 실적</span>
            <span style="color:#94a3b8; font-size:12px;">OPM 15.4%</span>
          </div>
          <div class="bar-wrapper">
            <span class="bar-name">매출</span>
            <div class="bar-track"><div class="bar-fill-sales" style="width: 35.2%;"></div></div>
            <span class="bar-val-text blue">11.2조 원</span>
          </div>
          <div class="bar-wrapper">
            <span class="bar-name">영익</span>
            <div class="bar-track"><div class="bar-fill-op" style="width: 37.0%;"></div></div>
            <span class="bar-val-text green">1.7조 원</span>
          </div>
        </div>

        <!-- 2025 -->
        <div class="year-row">
          <div class="year-label">
            <span>2025 (E/P) 실적</span>
            <span style="color:#94a3b8; font-size:12px;">OPM 12.7% (한화오션 연결 편입)</span>
          </div>
          <div class="bar-wrapper">
            <span class="bar-name">매출</span>
            <div class="bar-track"><div class="bar-fill-sales" style="width: 83.9%;"></div></div>
            <span class="bar-val-text blue">26.7조 원</span>
          </div>
          <div class="bar-wrapper">
            <span class="bar-name">영익</span>
            <div class="bar-track"><div class="bar-fill-op" style="width: 73.9%;"></div></div>
            <span class="bar-val-text green">3.4조 원</span>
          </div>
        </div>

        <!-- 2026 -->
        <div class="year-row active">
          <div class="year-label">
            <span style="color:#38bdf8;">2026 (F) 컨센서스 전망</span>
            <span style="color:#34d399; font-size:12px; font-weight:800;">OPM 14.5% (수출 물량 집중)</span>
          </div>
          <div class="bar-wrapper">
            <span class="bar-name" style="color:#38bdf8; font-weight:700;">매출</span>
            <div class="bar-track"><div class="bar-fill-sales" style="width: 100%;"></div></div>
            <span class="bar-val-text blue">31.8조 원 <small>(+19%)</small></span>
          </div>
          <div class="bar-wrapper">
            <span class="bar-name" style="color:#34d399; font-weight:700;">영익</span>
            <div class="bar-track"><div class="bar-fill-op" style="width: 100%;"></div></div>
            <span class="bar-val-text green">4.6조 원 <small>(+35%)</small></span>
          </div>
        </div>
      </div>
    </div>

    <!-- 핵심 재무 지표 카드 -->
    <div class="metrics-card">
      <div class="metric-box highlight">
        <div>
          <div class="metric-name">방산 수주잔고</div>
          <div style="font-size:12px; color:#64748b;">4~5년 치 확정 일감</div>
        </div>
        <div class="metric-val orange">38.3조 원+</div>
      </div>

      <div class="metric-box">
        <div>
          <div class="metric-name">2026(F) 영업이익률(OPM)</div>
          <div style="font-size:12px; color:#64748b;">지상방산 15~18%</div>
        </div>
        <div class="metric-val green">14.5%</div>
      </div>

      <div class="metric-box">
        <div>
          <div class="metric-name">2026(F) 지배순이익</div>
          <div style="font-size:12px; color:#64748b;">견고한 현금흐름</div>
        </div>
        <div class="metric-val blue">3.2조 원</div>
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
            ("body-3.png", body_3_html, 1080, 640),
        ]
        
        for filename, html, width, height in items:
            page = await browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=2)
            await page.set_content(html, wait_until="networkidle")
            out_path = OUTPUT_DIR / filename
            await page.screenshot(path=str(out_path), type="png")
            await page.close()
            print(f"[재생성 완료] {filename} ({width}x{height})")
            
        await browser.close()
        print("수정 이미지 재생성 완료!")

if __name__ == "__main__":
    asyncio.run(main())
