import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

OUTPUT_DIR = Path(r"c:\Users\immnu\Desktop\Claud\blog new agent\output\20261016-오늘의-증시-시황-마켓브리핑\images")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

HTML_TEMPLATES = {
    "thumbnail.png": {
        "width": 1080,
        "height": 1080,
        "html": """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    width: 1080px; height: 1080px;
    background: linear-gradient(135deg, #090d16 0%, #111827 50%, #1e1b4b 100%);
    font-family: -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", "Pretendard", sans-serif;
    color: #ffffff;
    display: flex; flex-direction: column; justify-content: space-between;
    padding: 80px 70px;
    position: relative; overflow: hidden;
  }
  .bg-glow {
    position: absolute; width: 600px; height: 600px;
    background: radial-gradient(circle, rgba(99, 102, 241, 0.15) 0%, rgba(0,0,0,0) 70%);
    top: -100px; right: -100px; border-radius: 50%;
  }
  .tag {
    display: inline-flex; align-items: center; gap: 8px;
    background: rgba(99, 102, 241, 0.2);
    border: 1px solid rgba(129, 140, 248, 0.4);
    color: #a5b4fc; font-size: 22px; font-weight: 700;
    padding: 10px 22px; border-radius: 100px;
    width: fit-content;
  }
  .main-title {
    font-size: 58px; font-weight: 900; line-height: 1.25;
    letter-spacing: -1.5px; margin-top: 24px;
    color: #ffffff;
  }
  .main-title .highlight {
    background: linear-gradient(90deg, #60a5fa, #818cf8);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  }
  .main-title .alert {
    color: #f87171;
  }
  .stats-grid {
    display: grid; grid-template-columns: 1fr 1fr; gap: 20px;
    margin: 36px 0;
  }
  .stat-card {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 20px; padding: 26px 28px;
    backdrop-filter: blur(10px);
  }
  .stat-label { font-size: 20px; color: #94a3b8; font-weight: 600; margin-bottom: 8px; }
  .stat-val { font-size: 38px; font-weight: 900; }
  .stat-val.up { color: #34d399; }
  .stat-val.down { color: #f87171; }
  .stat-val.blue { color: #60a5fa; }
  .stat-sub { font-size: 16px; color: #64748b; margin-top: 6px; }
  .footer-bar {
    display: flex; justify-content: space-between; align-items: center;
    border-top: 1px solid rgba(255, 255, 255, 0.12);
    padding-top: 24px;
  }
  .footer-logo { font-size: 24px; font-weight: 800; color: #818cf8; letter-spacing: -0.5px; }
  .footer-date { font-size: 20px; color: #94a3b8; font-weight: 500; }
</style>
</head>
<body>
  <div class="bg-glow"></div>
  <div>
    <div class="tag">🚨 10월 16일 긴급 시황 분석</div>
    <div class="main-title">
      15일 <span class="alert">서킷브레이커 쇼크</span> 후<br>
      코스피 <span class="highlight">5,700선 기술적 반등</span><br>
      바닥 진단과 실전 대응
    </div>
  </div>

  <div class="stats-grid">
    <div class="stat-card">
      <div class="stat-label">15일 코스피 (검은목요일)</div>
      <div class="stat-val down">5,554.22 <span style="font-size:24px;">(-7.57%)</span></div>
      <div class="stat-sub">양대 시장 서킷브레이커(CB) 발동</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">16일 오늘 코스피 (반등)</div>
      <div class="stat-val up">5,720.50 <span style="font-size:24px;">(+3.0%)</span></div>
      <div class="stat-sub">저가 매수세 유입 5,700선 탈환</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">원/달러 환율 (안정 유지)</div>
      <div class="stat-val blue">1,343.8원</div>
      <div class="stat-sub">1,340원대 방어로 외환위기 차단</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">코스피 밸류에이션 (PBR)</div>
      <div class="stat-val blue">1.08배</div>
      <div class="stat-sub">증권가 1차 안전판: 1.0배(5,000선)</div>
    </div>
  </div>

  <div class="footer-bar">
    <div class="footer-logo">ValueStockLabs</div>
    <div class="footer-date">2026.10.16 장중 긴급 분석 리포트</div>
  </div>
</body>
</html>"""
    },
    "body-1.png": {
        "width": 1080,
        "height": 720,
        "html": """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    width: 1080px; height: 720px;
    background: #0f172a;
    font-family: -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", "Pretendard", sans-serif;
    color: #ffffff; padding: 50px 60px;
    display: flex; flex-direction: column; justify-content: space-between;
  }
  .title-area { border-left: 5px solid #818cf8; padding-left: 18px; margin-bottom: 24px; }
  .badge { font-size: 15px; color: #818cf8; font-weight: 700; text-transform: uppercase; }
  .title { font-size: 32px; font-weight: 800; color: #ffffff; margin-top: 4px; }
  .timeline-table {
    width: 100%; border-collapse: separate; border-spacing: 0;
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 14px; overflow: hidden;
  }
  .timeline-table th {
    background: rgba(255, 255, 255, 0.08);
    padding: 16px 20px; font-size: 17px; font-weight: 700; color: #cbd5e1;
    text-align: left; border-bottom: 1px solid rgba(255, 255, 255, 0.12);
  }
  .timeline-table td {
    padding: 18px 20px; font-size: 18px; color: #ffffff;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    vertical-align: middle;
  }
  .timeline-table tr:last-child td { border-bottom: none; }
  .down { color: #f87171; font-weight: 800; }
  .up { color: #34d399; font-weight: 800; }
  .highlight-row { background: rgba(99, 102, 241, 0.12); }
  .note-box {
    background: rgba(255, 255, 255, 0.04);
    border: 1px dashed rgba(255, 255, 255, 0.2);
    border-radius: 10px; padding: 14px 20px;
    font-size: 16px; color: #94a3b8; display: flex; align-items: center; gap: 10px;
  }
</style>
</head>
<body>
  <div class="title-area">
    <div class="badge">Market Timeline & Indicators</div>
    <div class="title">10월 14~16일 국내 증시 지표 및 변동 흐름</div>
  </div>

  <table class="timeline-table">
    <thead>
      <tr>
        <th>거래일</th>
        <th>코스피 지수</th>
        <th>등락률</th>
        <th>원/달러 환율</th>
        <th>핵심 시장 이벤트 및 특징</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>10월 14일 (화)</strong></td>
        <td>6,008.81</td>
        <td class="down">-0.44%</td>
        <td>1,338.3원</td>
        <td>6,000선 턱걸이 마감, 외인 매도세 전환</td>
      </tr>
      <tr>
        <td><strong>10월 15일 (수)</strong></td>
        <td class="down">5,554.22</td>
        <td class="down">-7.57% 폭락</td>
        <td>1,344.6원</td>
        <td><strong>서킷브레이커(CB) 발동</strong>, AI 부채 및 미 물가 쇼크</td>
      </tr>
      <tr class="highlight-row">
        <td><strong>10월 16일 (목)</strong></td>
        <td class="up">5,720.50선</td>
        <td class="up">+3.0% 반등</td>
        <td>1,343.8원</td>
        <td><strong>5,700선 기술적 탈환</strong>, 코스닥 +4.1%(792선) 급반등</td>
      </tr>
    </tbody>
  </table>

  <div class="note-box">
    <span>💡</span>
    <span><strong>팩트 검증 완료:</strong> 주가 급변동 속에서도 원/달러 환율은 <strong>1,340원대</strong>에서 안정적으로 방어되어 외환위기 우려를 불식하고 있습니다.</span>
  </div>
</body>
</html>"""
    },
    "body-2.png": {
        "width": 1080,
        "height": 720,
        "html": """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    width: 1080px; height: 720px;
    background: #0b0f19;
    font-family: -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", "Pretendard", sans-serif;
    color: #ffffff; padding: 50px 60px;
    display: flex; flex-direction: column; justify-content: space-between;
  }
  .title-area { border-left: 5px solid #38bdf8; padding-left: 18px; margin-bottom: 20px; }
  .badge { font-size: 15px; color: #38bdf8; font-weight: 700; }
  .title { font-size: 30px; font-weight: 800; color: #ffffff; margin-top: 4px; }
  .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
  .col-card {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 14px; padding: 24px;
  }
  .col-title { font-size: 20px; font-weight: 800; margin-bottom: 16px; display: flex; align-items: center; gap: 8px; }
  .col-title.red { color: #f87171; }
  .col-title.green { color: #34d399; }
  .item { margin-bottom: 14px; }
  .item-head { font-size: 16px; font-weight: 700; color: #f1f5f9; margin-bottom: 4px; }
  .item-desc { font-size: 14px; color: #94a3b8; line-height: 1.5; }
</style>
</head>
<body>
  <div class="title-area">
    <div class="badge">Root Causes & Valuation Analysis</div>
    <div class="title">15일 대폭락 3대 원인 & 5,700선 밸류에이션 팩트</div>
  </div>

  <div class="grid">
    <div class="col-card">
      <div class="col-title red">⚠️ 15일 서킷브레이커 3대 원인</div>
      <div class="item">
        <div class="item-head">1. 미국 9월 CPI 쇼크</div>
        <div class="item-desc">예상치 상회한 물가지표로 연준 긴축 장기화 우려 점화</div>
      </div>
      <div class="item">
        <div class="item-head">2. AI 빅테크 부채 및 수익성 의구심</div>
        <div class="item-desc">인프라 투자 대비 현금흐름 회수 지연에 따른 반도체 차익실현</div>
      </div>
      <div class="item">
        <div class="item-head">3. 외국인 대규모 디리스킹</div>
        <div class="item-desc">삼성전자(-9.48%), SK하이닉스(-11.06%) 중심 매도 집중</div>
      </div>
    </div>

    <div class="col-card">
      <div class="col-title green">💡 객관적 밸류에이션 팩트 점검</div>
      <div class="item">
        <div class="item-head">1. 코스피 5,700선 = PBR 1.08배</div>
        <div class="item-desc">12개월 선행 PBR 1.08배로 단기 과매도 국면 진입</div>
      </div>
      <div class="item">
        <div class="item-head">2. 역사적 1차 마지노선 = PBR 1.0배 (5,000선)</div>
        <div class="item-desc">청산가치 수렴 구간인 5,000포인트가 강력한 하방 경직성 제공</div>
      </div>
      <div class="item">
        <div class="item-head">3. 환율 1,340원대 안정 유지</div>
        <div class="item-desc">1,343.8원 등락으로 외환 안정성 유지, 저가 매수세 유입 근거</div>
      </div>
    </div>
  </div>

  <div style="font-size: 14px; color: #64748b; text-align: right;">ValueStockLabs Research Desk</div>
</body>
</html>"""
    },
    "body-3.png": {
        "width": 1080,
        "height": 720,
        "html": """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    width: 1080px; height: 720px;
    background: #090d16;
    font-family: -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", "Pretendard", sans-serif;
    color: #ffffff; padding: 50px 60px;
    display: flex; flex-direction: column; justify-content: space-between;
  }
  .title-area { border-left: 5px solid #f59e0b; padding-left: 18px; margin-bottom: 24px; }
  .badge { font-size: 15px; color: #f59e0b; font-weight: 700; text-transform: uppercase; }
  .title { font-size: 30px; font-weight: 800; color: #ffffff; margin-top: 4px; }
  .rules-wrap { display: flex; flex-direction: column; gap: 16px; }
  .rule-card {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 14px; padding: 20px 24px;
    display: flex; align-items: flex-start; gap: 20px;
  }
  .rule-num {
    background: linear-gradient(135deg, #f59e0b, #d97706);
    color: #ffffff; font-size: 20px; font-weight: 900;
    width: 44px; height: 44px; border-radius: 12px;
    display: flex; align-items: center; justify-content: center; flex-shrink: 0;
  }
  .rule-title { font-size: 20px; font-weight: 800; color: #ffffff; margin-bottom: 6px; }
  .rule-desc { font-size: 15px; color: #94a3b8; line-height: 1.5; }
</style>
</head>
<body>
  <div class="title-area">
    <div class="badge">Actionable Risk Strategy</div>
    <div class="title">서킷브레이커 익일 반등 장세: 실전 비상 3대 수칙</div>
  </div>

  <div class="rules-wrap">
    <div class="rule-card">
      <div class="rule-num">1</div>
      <div>
        <div class="rule-title">기술적 반등 시 '뇌동 추격 매수' 엄금</div>
        <div class="rule-desc">폭락 직후 첫 반등은 자율 반등 성격이 강함. 5,700선 지지력과 W자 쌍바닥 테스트를 오후 종가까지 반드시 확인 후 대응.</div>
      </div>
    </div>
    <div class="rule-card">
      <div class="rule-num">2</div>
      <div>
        <div class="rule-title">외국인 선물 및 현물 '실제 수급 전환' 확인</div>
        <div class="rule-desc">지수 반등에도 외인은 2,000억대 순매도 우위 지속 중. 코스피 200 선물 순매수 전환 및 현물 매도세 축소를 확인해야 안전.</div>
      </div>
    </div>
    <div class="rule-card">
      <div class="rule-num">3</div>
      <div>
        <div class="rule-title">PBR 1.0배(5,000선) 버퍼 확보 &amp; 분할 매수</div>
        <div class="rule-desc">현금 비중 최소 30%를 유지하며, 청산가치 수준인 5,000선까지의 추가 하방 버퍼를 열어두고 실적주 중심 3~4회 분할 접근.</div>
      </div>
    </div>
  </div>

  <div style="font-size: 14px; color: #64748b; text-align: right;">ValueStockLabs Emergency Checklist</div>
</body>
</html>"""
    }
}

async def generate_images():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        for filename, data in HTML_TEMPLATES.items():
            page = await browser.new_page(
                viewport={"width": data["width"], "height": data["height"]},
                device_scale_factor=2
            )
            await page.set_content(data["html"])
            await page.wait_for_timeout(300)
            target_path = OUTPUT_DIR / filename
            await page.screenshot(path=str(target_path))
            print(f"[완료] 이미지 생성: {filename} ({data['width']}x{data['height']})")
            await page.close()
        await browser.close()

if __name__ == "__main__":
    asyncio.run(generate_images())
