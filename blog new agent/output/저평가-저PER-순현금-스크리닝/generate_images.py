import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

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
      background: radial-gradient(circle at 50% 20%, #1e1b4b 0%, #0f172a 60%, #020617 100%);
      font-family: 'Pretendard', sans-serif;
      display: flex;
      justify-content: center;
      align-items: center;
      color: #ffffff;
      padding: 70px;
    }
    .card {
      width: 100%;
      height: 100%;
      background: rgba(30, 41, 59, 0.45);
      border: 1px solid rgba(255, 255, 255, 0.12);
      backdrop-filter: blur(16px);
      border-radius: 36px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      text-align: center;
      padding: 60px 50px;
      box-shadow: 0 25px 60px rgba(0, 0, 0, 0.6);
      position: relative;
    }
    .badge {
      font-size: 22px;
      font-weight: 700;
      color: #818cf8;
      background: rgba(99, 102, 241, 0.18);
      border: 1px solid rgba(99, 102, 241, 0.4);
      padding: 10px 26px;
      border-radius: 9999px;
      margin-bottom: 32px;
      letter-spacing: 0.5px;
    }
    .title {
      font-size: 52px;
      font-weight: 800;
      line-height: 1.35;
      margin-bottom: 24px;
      word-break: keep-all;
      background: linear-gradient(180deg, #ffffff 0%, #cbd5e1 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .title span {
      background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .subtitle {
      font-size: 24px;
      font-weight: 500;
      color: #94a3b8;
      line-height: 1.5;
      margin-bottom: 44px;
      word-break: keep-all;
    }
    .metrics-row {
      display: flex;
      gap: 20px;
      width: 100%;
      justify-content: center;
    }
    .metric-pill {
      background: rgba(15, 23, 42, 0.8);
      border: 1px solid rgba(255, 255, 255, 0.08);
      padding: 16px 28px;
      border-radius: 18px;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 6px;
    }
    .metric-name {
      font-size: 14px;
      color: #94a3b8;
      font-weight: 600;
      text-transform: uppercase;
    }
    .metric-val {
      font-size: 24px;
      font-weight: 800;
      color: #38bdf8;
    }
  </style>
</head>
<body>
  <div class="card">
    <div class="badge">Value Investing & Quant Guide</div>
    <h1 class="title">저PER & 순현금비율<br><span>저평가 우량주</span> 발굴법</h1>
    <p class="subtitle">시총 50% 순현금 안전마진과 4단계 퀀트 스크리닝 공식</p>
    <div class="metrics-row">
      <div class="metric-pill">
        <span class="metric-name">PER 필터</span>
        <span class="metric-val">10배 이하</span>
      </div>
      <div class="metric-pill">
        <span class="metric-name">순현금비율</span>
        <span class="metric-val">40% 이상</span>
      </div>
      <div class="metric-pill">
        <span class="metric-name">영업현금흐름</span>
        <span class="metric-val">3년 연속 흑자</span>
      </div>
    </div>
  </div>
</body>
</html>
"""

HTML_BODY_1 = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 1000px;
      height: 600px;
      background: #0f172a;
      font-family: 'Pretendard', sans-serif;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      color: #ffffff;
      padding: 40px;
    }
    .header {
      text-align: center;
      margin-bottom: 28px;
    }
    .header h2 {
      font-size: 28px;
      font-weight: 800;
      color: #f8fafc;
      margin-bottom: 8px;
    }
    .header p {
      font-size: 16px;
      color: #94a3b8;
    }
    .grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 24px;
      width: 100%;
    }
    .card {
      background: #1e293b;
      border-radius: 20px;
      padding: 28px;
      border: 1px solid rgba(255, 255, 255, 0.08);
      position: relative;
    }
    .card.highlight {
      border: 2px solid #6366f1;
      background: linear-gradient(180deg, rgba(99, 102, 241, 0.12) 0%, rgba(30, 41, 59, 0.9) 100%);
    }
    .card-badge {
      display: inline-block;
      font-size: 13px;
      font-weight: 700;
      padding: 5px 12px;
      border-radius: 6px;
      margin-bottom: 16px;
    }
    .badge-bad { background: rgba(239, 68, 68, 0.2); color: #f87171; }
    .badge-good { background: rgba(16, 185, 129, 0.2); color: #34d399; }
    .card-title {
      font-size: 20px;
      font-weight: 700;
      margin-bottom: 18px;
      color: #ffffff;
    }
    .row {
      display: flex;
      justify-content: space-between;
      padding: 10px 0;
      border-bottom: 1px solid rgba(255, 255, 255, 0.06);
      font-size: 15px;
    }
    .row:last-child { border-bottom: none; }
    .label { color: #94a3b8; }
    .value { font-weight: 700; color: #f1f5f9; }
    .val-highlight { color: #38bdf8; font-size: 18px; }
  </style>
</head>
<body>
  <div class="header">
    <h2>겉보기 PER vs 순현금 반영 실질 PER 비교</h2>
    <p>동일한 겉보기 PER 10배 기업이라도 순현금 보유량에 따라 실질 가치는 극명하게 갈립니다</p>
  </div>
  <div class="grid">
    <div class="card">
      <span class="card-badge badge-bad">주의: 차입금 보유 기업 B</span>
      <div class="card-title">시총 1,000억 / 순이익 100억</div>
      <div class="row"><span class="label">보유 순차입금 (빚)</span><span class="value">+500억 원</span></div>
      <div class="row"><span class="label">실질 기업가치 (EV)</span><span class="value">1,500억 원</span></div>
      <div class="row"><span class="label">실질 PER (EV/순이익)</span><span class="value val-highlight" style="color:#f87171;">15.0배 (고평가)</span></div>
      <div class="row"><span class="label">하방 안전마진</span><span class="value" style="color:#ef4444;">취약 (이자부담 증가)</span></div>
    </div>
    <div class="card highlight">
      <span class="card-badge badge-good">추천: 순현금 우량 기업 A</span>
      <div class="card-title">시총 1,000억 / 순이익 100억</div>
      <div class="row"><span class="label">보유 순현금 (곳간)</span><span class="value" style="color:#34d399;">500억 원 (비율 50%)</span></div>
      <div class="row"><span class="label">실질 기업가치 (EV)</span><span class="value">500억 원</span></div>
      <div class="row"><span class="label">실질 PER (EV/순이익)</span><span class="value val-highlight" style="color:#38bdf8;">5.0배 (극단적 저평가)</span></div>
      <div class="row"><span class="label">하방 안전마진</span><span class="value" style="color:#34d399;">강력 (시총 50% 현금 지지)</span></div>
    </div>
  </div>
</body>
</html>
"""

HTML_BODY_2 = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 1000px;
      height: 600px;
      background: #0b1329;
      font-family: 'Pretendard', sans-serif;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      color: #ffffff;
      padding: 40px;
    }
    .header {
      text-align: center;
      margin-bottom: 30px;
    }
    .header h2 {
      font-size: 28px;
      font-weight: 800;
      color: #f8fafc;
      margin-bottom: 8px;
    }
    .header p {
      font-size: 16px;
      color: #94a3b8;
    }
    .steps-container {
      display: flex;
      gap: 16px;
      width: 100%;
    }
    .step-card {
      flex: 1;
      background: #1e293b;
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 18px;
      padding: 24px 18px;
      display: flex;
      flex-direction: column;
      position: relative;
    }
    .step-card:hover {
      border-color: #6366f1;
    }
    .step-num {
      width: 36px;
      height: 36px;
      border-radius: 10px;
      background: #4f46e5;
      color: #ffffff;
      display: flex;
      justify-content: center;
      align-items: center;
      font-weight: 800;
      font-size: 16px;
      margin-bottom: 16px;
    }
    .step-title {
      font-size: 17px;
      font-weight: 700;
      color: #ffffff;
      margin-bottom: 12px;
    }
    .step-desc {
      font-size: 13px;
      color: #94a3b8;
      line-height: 1.6;
    }
    .step-badge {
      margin-top: auto;
      padding-top: 14px;
      font-size: 12px;
      font-weight: 700;
      color: #38bdf8;
    }
  </style>
</head>
<body>
  <div class="header">
    <h2>저PER & 고순현금 4단계 스크리닝 프로세스</h2>
    <p>재무 안전성부터 주가 촉매(Catalyst)까지 정밀하게 검증하는 단계별 필터</p>
  </div>
  <div class="steps-container">
    <div class="step-card">
      <div class="step-num">01</div>
      <div class="step-title">순현금 필터</div>
      <div class="step-desc">• 순현금 > 0<br>• 순현금비율 ≥ 40%<br>• 무차입 또는 실질 무차입</div>
      <div class="step-badge">안전마진 확보</div>
    </div>
    <div class="step-card">
      <div class="step-num">02</div>
      <div class="step-title">밸류에이션</div>
      <div class="step-desc">• PER ≤ 8~10배<br>• PBR ≤ 0.8배<br>• 업종 평균 대비 저평가</div>
      <div class="step-badge">가격 매력도 검증</div>
    </div>
    <div class="step-card">
      <div class="step-num">03</div>
      <div class="step-title">현금창출력</div>
      <div class="step-desc">• 3개년 연속 영업흑자<br>• 영업현금흐름 > 순이익<br>• 부채비율 < 50%</div>
      <div class="step-badge">이익 퀄리티 확인</div>
    </div>
    <div class="step-card">
      <div class="step-num">04</div>
      <div class="step-title">주주환원/촉매</div>
      <div class="step-desc">• 배당수익률 3% 이상<br>• 자사주 매입/소각 이력<br>• 밸류업 공시 참여</div>
      <div class="step-badge">주가 리레이팅 트리거</div>
    </div>
  </div>
</body>
</html>
"""

HTML_BODY_3 = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 1000px;
      height: 600px;
      background: #0f172a;
      font-family: 'Pretendard', sans-serif;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      color: #ffffff;
      padding: 40px;
    }
    .header {
      text-align: center;
      margin-bottom: 30px;
    }
    .header h2 {
      font-size: 28px;
      font-weight: 800;
      color: #f8fafc;
      margin-bottom: 8px;
    }
    .header p {
      font-size: 16px;
      color: #f59e0b;
      font-weight: 600;
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 20px;
      width: 100%;
    }
    .card {
      background: #1e293b;
      border: 1px solid rgba(245, 158, 11, 0.2);
      border-radius: 18px;
      padding: 26px 20px;
      display: flex;
      flex-direction: column;
    }
    .icon-wrap {
      font-size: 32px;
      margin-bottom: 16px;
    }
    .card-title {
      font-size: 18px;
      font-weight: 700;
      color: #ffffff;
      margin-bottom: 12px;
    }
    .card-desc {
      font-size: 14px;
      color: #94a3b8;
      line-height: 1.6;
      margin-bottom: 16px;
    }
    .card-action {
      margin-top: auto;
      background: rgba(245, 158, 11, 0.1);
      border: 1px solid rgba(245, 158, 11, 0.3);
      padding: 8px 12px;
      border-radius: 8px;
      font-size: 12px;
      color: #fbbf24;
      font-weight: 600;
    }
  </style>
</head>
<body>
  <div class="header">
    <h2>가치 함정(Value Trap) 방지 3대 핵심 체크리스트</h2>
    <p>⚠️ 저PER & 순현금 기업이라도 아래 3가지 함정은 반드시 걸러내야 합니다</p>
  </div>
  <div class="grid">
    <div class="card">
      <div class="icon-wrap">🔒</div>
      <div class="card-title">1. 현금 방치형 기업</div>
      <div class="card-desc">현금이 수천억 원 있어도 배당 성향 5% 미만, 대주주 지분 승계용으로 주가를 일부러 방치하는 기업.</div>
      <div class="card-action">체크: 배당성향 및 주주환원율</div>
    </div>
    <div class="card">
      <div class="icon-wrap">📉</div>
      <div class="card-title">2. 현금 소진형 적자 기업</div>
      <div class="card-desc">본업 경쟁력 훼손으로 분기마다 영업적자가 누적되어 곳간의 현금이 빠르게 녹아내리는 기업.</div>
      <div class="card-action">체크: 영업활동현금흐름(OCF)</div>
    </div>
    <div class="card">
      <div class="icon-wrap">🎭</div>
      <div class="card-title">3. 일회성 이익 착시형</div>
      <div class="card-desc">부동산 매각, 자회사 지분 처분 등 1회성 이익으로 당기순이익만 급증해 PER이 낮아 보이는 착시 기업.</div>
      <div class="card-action">체크: 영업이익 vs 순이익 괴리</div>
    </div>
  </div>
</body>
</html>
"""

async def generate():
    output_dir = Path("output/저평가-저PER-순현금-스크리닝/images")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    tasks = [
        (HTML_THUMBNAIL, output_dir / "thumbnail.png", 1080, 1080),
        (HTML_BODY_1, output_dir / "body-1.png", 1000, 600),
        (HTML_BODY_2, output_dir / "body-2.png", 1000, 600),
        (HTML_BODY_3, output_dir / "body-3.png", 1000, 600),
    ]
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        for html, path, w, h in tasks:
            page = await browser.new_page(viewport={"width": w, "height": h}, device_scale_factor=2)
            await page.set_content(html, wait_until="networkidle")
            await page.screenshot(path=str(path), type="png")
            await page.close()
            print(f"[성공] 생성 완료: {path}")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(generate())
