import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

ROOT_DIR = Path(r"c:\Users\immnu\Desktop\Claud")
BLOG_DIR = ROOT_DIR / "adsense-stock-blog"
OUTPUT_DIR = BLOG_DIR / "images" / "adsense-master-guide"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

html_content = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 1080px;
      height: 1080px;
      background: linear-gradient(135deg, #070a13 0%, #0f172a 50%, #1e1b4b 100%);
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
      width: 580px;
      height: 580px;
      top: -140px;
      right: -120px;
      background: radial-gradient(circle, rgba(245, 158, 11, 0.35) 0%, transparent 70%);
      filter: blur(80px);
    }
    .glow-2 {
      position: absolute;
      width: 580px;
      height: 580px;
      bottom: -140px;
      left: -120px;
      background: radial-gradient(circle, rgba(16, 185, 129, 0.3) 0%, transparent 70%);
      filter: blur(80px);
    }
    .card {
      width: 100%;
      height: 100%;
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid rgba(255, 255, 255, 0.15);
      border-radius: 40px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      align-items: center;
      text-align: center;
      padding: 70px 50px;
      backdrop-filter: blur(20px);
      box-shadow: 0 30px 60px rgba(0, 0, 0, 0.6);
      position: relative;
      z-index: 10;
    }
    .header-badge {
      display: inline-flex;
      align-items: center;
      gap: 12px;
      font-size: 20px;
      font-weight: 700;
      color: #fbbf24;
      background: rgba(245, 158, 11, 0.15);
      border: 1px solid rgba(245, 158, 11, 0.35);
      padding: 12px 30px;
      border-radius: 9999px;
      letter-spacing: 0.5px;
    }
    .header-badge span.dot {
      width: 10px;
      height: 10px;
      background-color: #10b981;
      border-radius: 50%;
      box-shadow: 0 0 10px #10b981;
    }
    .title-box {
      display: flex;
      flex-direction: column;
      gap: 20px;
      align-items: center;
    }
    .sub-title {
      font-size: 26px;
      font-weight: 600;
      color: #94a3b8;
      letter-spacing: -0.5px;
    }
    .main-title {
      font-size: 54px;
      font-weight: 900;
      line-height: 1.25;
      letter-spacing: -1.5px;
      background: linear-gradient(180deg, #ffffff 0%, #cbd5e1 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .highlight {
      background: linear-gradient(90deg, #f59e0b 0%, #10b981 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .grid-stats {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 20px;
      width: 100%;
      margin: 10px 0;
    }
    .stat-item {
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 20px;
      padding: 24px 16px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    .stat-label {
      font-size: 16px;
      color: #94a3b8;
      font-weight: 600;
    }
    .stat-val {
      font-size: 26px;
      font-weight: 800;
      color: #38bdf8;
    }
    .footer-bar {
      width: 100%;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-top: 1px solid rgba(255, 255, 255, 0.1);
      padding-top: 30px;
    }
    .brand-logo {
      font-size: 24px;
      font-weight: 900;
      letter-spacing: -0.5px;
      color: #ffffff;
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .brand-logo span {
      color: #4f46e5;
    }
    .date-tag {
      font-size: 18px;
      color: #64748b;
      font-weight: 600;
    }
  </style>
</head>
<body>
  <div class="glow-1"></div>
  <div class="glow-2"></div>
  <div class="card">
    <div class="header-badge">
      <span class="dot"></span>
      VALUE STOCK LABS OFFICIAL GUIDE
    </div>
    <div class="title-box">
      <div class="sub-title">100% 승인 체크리스트 &amp; 수익 극대화 전략</div>
      <h1 class="main-title">
        구글 애드센스 승인 &amp;<br>
        <span class="highlight">수익 극대화 실전 마스터 가이드</span>
      </h1>
    </div>
    <div class="grid-stats">
      <div class="stat-item">
        <span class="stat-label">무료 배포</span>
        <span class="stat-val">Vercel / Netlify</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">검색 색인</span>
        <span class="stat-val">GSC 사이트맵</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">수익 최적화</span>
        <span class="stat-val">고단가 CPC 공식</span>
      </div>
    </div>
    <div class="footer-bar">
      <div class="brand-logo">ValueStockLabs<span>.com</span></div>
      <div class="date-tag">2026.10.14</div>
    </div>
  </div>
</body>
</html>"""

async def generate_thumbnail():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1080, "height": 1080}, device_scale_factor=2)
        await page.set_content(html_content)
        await page.wait_for_timeout(500)
        out_path = OUTPUT_DIR / "thumbnail.png"
        await page.screenshot(path=str(out_path))
        await browser.close()
        print(f"[성공] 썸네일 이미지 생성 완료: {out_path}")

if __name__ == "__main__":
    asyncio.run(generate_thumbnail())
