import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

OUTPUT_DIR = Path(r"c:\Users\immnu\Desktop\Claud\blog new agent\output\20261020-오늘의-증시-시황-마켓브리핑\images")
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
    background: linear-gradient(135deg, #070a12 0%, #0f172a 50%, #1e1b4b 100%);
    font-family: -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", "Pretendard", sans-serif;
    color: #ffffff;
    display: flex; flex-direction: column; justify-content: space-between;
    padding: 80px 70px;
    position: relative; overflow: hidden;
  }
  .bg-glow {
    position: absolute; width: 650px; height: 650px;
    background: radial-gradient(circle, rgba(99, 102, 241, 0.22) 0%, rgba(0,0,0,0) 70%);
    top: -100px; right: -100px; border-radius: 50%;
  }
  .bg-glow-2 {
    position: absolute; width: 550px; height: 550px;
    background: radial-gradient(circle, rgba(52, 211, 153, 0.18) 0%, rgba(0,0,0,0) 70%);
    bottom: -100px; left: -100px; border-radius: 50%;
  }
  .tag {
    display: inline-flex; align-items: center; gap: 8px;
    background: rgba(99, 102, 241, 0.2);
    border: 1px solid rgba(129, 140, 248, 0.4);
    color: #a5b4fc; font-size: 22px; font-weight: 700;
    padding: 10px 24px; border-radius: 100px;
    width: fit-content;
  }
  .main-title {
    font-size: 54px; font-weight: 900; line-height: 1.25;
    letter-spacing: -1.5px; margin-top: 24px;
    color: #ffffff;
  }
  .main-title .highlight {
    background: linear-gradient(90deg, #38bdf8, #34d399);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  }
  .main-title .gold {
    background: linear-gradient(90deg, #fbbf24, #f59e0b);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  }
  .stats-grid {
    display: grid; grid-template-columns: 1fr 1fr; gap: 20px;
    margin: 32px 0;
  }
  .stat-card {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 20px; padding: 24px 28px;
    backdrop-filter: blur(10px);
  }
  .stat-label { font-size: 20px; color: #94a3b8; font-weight: 600; margin-bottom: 8px; }
  .stat-val { font-size: 38px; font-weight: 900; }
  .stat-val.up { color: #34d399; }
  .stat-val.cyan { color: #38bdf8; }
  .stat-sub { font-size: 16px; color: #64748b; margin-top: 4px; font-weight: 500; }
  .bottom-bar {
    display: flex; justify-content: space-between; align-items: center;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    padding-top: 24px;
  }
  .author { font-size: 20px; color: #94a3b8; font-weight: 600; }
  .author span { color: #60a5fa; font-weight: 800; }
  .date-badge {
    background: rgba(255, 255, 255, 0.08);
    padding: 8px 18px; border-radius: 8px;
    font-size: 18px; color: #cbd5e1; font-weight: 700;
  }
</style>
</head>
<body>
  <div class="bg-glow"></div>
  <div class="bg-glow-2"></div>
  <div>
    <div class="tag">⚡ 2026.10.20 마켓 브리핑</div>
    <div class="main-title">
      코스피 <span class="highlight">5,488선 딛고 5,768선</span> V자 반등<br>
      뉴욕 반도체 <span class="gold">8일만 상승 탈출</span>
    </div>
  </div>

  <div class="stats-grid">
    <div class="stat-card">
      <div class="stat-label">KOSPI 마감</div>
      <div class="stat-val up">5,768.01 <span style="font-size: 22px;">(+1.76%)</span></div>
      <div class="stat-sub">장중 5,488 저점 대비 +280pt 폭풍 반등</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">원·달러 환율</div>
      <div class="stat-val cyan">1,330.3원 <span style="font-size: 22px;">(-1.1원)</span></div>
      <div class="stat-sub">1,330원선 확고한 하향 안착 성공</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">기관 순매수</div>
      <div class="stat-val up">+5,746억 원</div>
      <div class="stat-sub">외인 매도 축소 및 삼성전자 2일 연속 순매수</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">간밤 나스닥 & 반도체</div>
      <div class="stat-val up">나스닥 +1.11%</div>
      <div class="stat-sub">필라델피아 반도체 8일 연속 하락세 탈출(+1.8%)</div>
    </div>
  </div>

  <div class="bottom-bar">
    <div class="author"><span>ValueStockLabs</span> Daily Market Report</div>
    <div class="date-badge">2026.10.20 화요일 장전</div>
  </div>
</body>
</html>"""
    },
    "body-1.png": {
        "width": 1080,
        "height": 620,
        "html": """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    width: 1080px; height: 620px;
    background: #0f172a;
    font-family: -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", "Pretendard", sans-serif;
    color: #ffffff; padding: 45px 50px;
    display: flex; flex-direction: column; justify-content: space-between;
  }
  .header {
    display: flex; justify-content: space-between; align-items: flex-end;
    border-bottom: 2px solid rgba(255, 255, 255, 0.1); padding-bottom: 16px;
  }
  .title { font-size: 30px; font-weight: 800; color: #f8fafc; }
  .title span { color: #38bdf8; }
  .subtitle { font-size: 16px; color: #94a3b8; margin-top: 4px; }
  .badge { background: rgba(56, 189, 248, 0.15); color: #38bdf8; padding: 6px 14px; border-radius: 8px; font-size: 14px; font-weight: 700; }
  
  .table-box {
    margin-top: 18px; border-radius: 14px; overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.1);
  }
  table { width: 100%; border-collapse: collapse; text-align: left; }
  th { background: #1e293b; color: #94a3b8; font-size: 15px; font-weight: 700; padding: 14px 20px; border-bottom: 1px solid rgba(255, 255, 255, 0.1); }
  td { padding: 14px 20px; border-bottom: 1px solid rgba(255, 255, 255, 0.06); font-size: 16px; color: #e2e8f0; }
  tr:last-child td { border-bottom: none; }
  tr:nth-child(even) { background: rgba(255, 255, 255, 0.02); }
  .bold { font-weight: 800; color: #ffffff; }
  .up { color: #34d399; font-weight: 700; }
  .down { color: #38bdf8; font-weight: 700; }
  .note { color: #cbd5e1; font-size: 14px; }
  
  .footer-note {
    font-size: 14px; color: #64748b; display: flex; justify-content: space-between;
    margin-top: 10px;
  }
</style>
</head>
<body>
  <div class="header">
    <div>
      <div class="title">10월 19일 <span>국내 증시 핵심 지표 및 수급</span> 마감 분석</div>
      <div class="subtitle">5,488선 저점 딛고 280pt V자 급반등 · 기관 5,746억 순매수 견인</div>
    </div>
    <div class="badge">KRX 10.19 확정치</div>
  </div>

  <div class="table-box">
    <table>
      <thead>
        <tr>
          <th>지표 / 구분</th>
          <th>10월 19일 마감치</th>
          <th>전일 대비 등락</th>
          <th>핵심 특징 및 수급 분석</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td class="bold">코스피 (KOSPI)</td>
          <td class="bold">5,768.01 pt</td>
          <td class="up">+99.96 pt (+1.76%)</td>
          <td class="note">장중 5,488.41(-3%) 추락 후 +280pt V자 폭풍 반등</td>
        </tr>
        <tr>
          <td class="bold">코스닥 (KOSDAQ)</td>
          <td class="bold">808.89 pt</td>
          <td class="up">+14.11 pt (+1.78%)</td>
          <td class="note">과매도 해소와 함께 800선 단숨에 탈환 안착</td>
        </tr>
        <tr>
          <td class="bold">원·달러 환율</td>
          <td class="bold">1,330.3 원</td>
          <td class="down">-1.1 원 (원화 강세)</td>
          <td class="note">1,340원대 저항 후 1,330원선 확고한 하향 안착</td>
        </tr>
        <tr>
          <td class="bold">기관 수급</td>
          <td class="up">+5,746억 원</td>
          <td class="up">순매수 견인</td>
          <td class="note">금융투자·연기금 저가 매집으로 지수 반등 주도</td>
        </tr>
        <tr>
          <td class="bold">외국인 수급</td>
          <td>-364억 원</td>
          <td class="up">매도세 소멸 국면</td>
          <td class="note">삼성전자 1,720억 2일 연속 순매수 집중</td>
        </tr>
      </tbody>
    </table>
  </div>

  <div class="footer-note">
    <div>* 출처: 한국거래소(KRX) 및 서울외환시장 (2026.10.19)</div>
    <div>ValueStockLabs Research</div>
  </div>
</body>
</html>"""
    },
    "body-2.png": {
        "width": 1080,
        "height": 620,
        "html": """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    width: 1080px; height: 620px;
    background: #090d16;
    font-family: -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", "Pretendard", sans-serif;
    color: #ffffff; padding: 45px 50px;
    display: flex; flex-direction: column; justify-content: space-between;
  }
  .header {
    border-bottom: 2px solid rgba(255, 255, 255, 0.1); padding-bottom: 16px;
    display: flex; justify-content: space-between; align-items: flex-end;
  }
  .title { font-size: 30px; font-weight: 800; }
  .title span { color: #34d399; }
  .badge { background: rgba(52, 211, 153, 0.15); color: #34d399; padding: 6px 14px; border-radius: 8px; font-size: 14px; font-weight: 700; }
  
  .cards-grid {
    display: grid; grid-template-columns: 1fr 1fr; gap: 20px;
    margin: 20px 0;
  }
  .card {
    background: #111827; border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px; padding: 22px 24px;
    display: flex; flex-direction: column; justify-content: space-between;
  }
  .card-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
  .card-label { font-size: 18px; font-weight: 700; color: #94a3b8; }
  .card-tag { font-size: 13px; font-weight: 700; padding: 4px 10px; border-radius: 6px; }
  .tag-green { background: rgba(52, 211, 153, 0.2); color: #34d399; }
  .tag-blue { background: rgba(56, 189, 248, 0.2); color: #38bdf8; }
  .card-val { font-size: 32px; font-weight: 900; color: #ffffff; margin-bottom: 6px; }
  .card-val .rate { font-size: 20px; margin-left: 6px; color: #34d399; }
  .card-desc { font-size: 14px; color: #cbd5e1; line-height: 1.5; }
  
  .bottom-info {
    background: rgba(255, 255, 255, 0.04); border-radius: 10px;
    padding: 12px 20px; font-size: 14px; color: #94a3b8;
    display: flex; justify-content: space-between; align-items: center;
  }
</style>
</head>
<body>
  <div class="header">
    <div>
      <div class="title">간밤 뉴욕증시 <span>반등 포인트 4대 지표</span> 총정리</div>
      <div style="font-size: 16px; color: #94a3b8; margin-top: 4px;">10월 19일 현지시간 마감: 반도체 8일 만의 하락 탈출 및 빅테크 저가 매수세</div>
    </div>
    <div class="badge">Global Macro 10.19</div>
  </div>

  <div class="cards-grid">
    <div class="card">
      <div class="card-top">
        <div class="card-label">나스닥 종합지수</div>
        <div class="card-tag tag-green">+1.11% 반등</div>
      </div>
      <div class="card-val">26,430.89 <span class="rate">(+290.86p)</span></div>
      <div class="card-desc">AI 인프라 부채 과열 우려 흡수하며 빅테크 중심 저가 매수세 유입</div>
    </div>
    <div class="card">
      <div class="card-top">
        <div class="card-label">필라델피아 반도체</div>
        <div class="card-tag tag-green">8일만 하락 탈출</div>
      </div>
      <div class="card-val">+1.8% <span class="rate">반등 성공</span></div>
      <div class="card-desc">2008년 이후 최장 8일 연속 하락세 마감. 엔비디아·마이크론 반등</div>
    </div>
    <div class="card">
      <div class="card-top">
        <div class="card-label">S&P 500 지수</div>
        <div class="card-tag tag-blue">+0.41% 상승</div>
      </div>
      <div class="card-val">7,690.73 <span class="rate">(+31.29p)</span></div>
      <div class="card-desc">대형 우량주 중심 하방 경직성 확보하며 상승 흐름 동조</div>
    </div>
    <div class="card">
      <div class="card-top">
        <div class="card-label">공포지수 (VIX) & 유가</div>
        <div class="card-tag tag-blue">안정화 진입</div>
      </div>
      <div class="card-val">20.4 <span class="rate" style="color: #38bdf8;">하향 안정</span></div>
      <div class="card-desc">WTI 100달러선 추가 급등 제한 및 VIX 지수 20선 초반 진정</div>
    </div>
  </div>

  <div class="bottom-info">
    <div>💡 월가 진단: "AI 사모부채 이슈는 개별 기업 문제일 뿐 빅테크 현금 흐름 훼손 불가"</div>
    <div>ValueStockLabs Macro Desk</div>
  </div>
</body>
</html>"""
    },
    "body-3.png": {
        "width": 1080,
        "height": 620,
        "html": """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    width: 1080px; height: 620px;
    background: #0f172a;
    font-family: -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", "Pretendard", sans-serif;
    color: #ffffff; padding: 45px 50px;
    display: flex; flex-direction: column; justify-content: space-between;
  }
  .header {
    border-bottom: 2px solid rgba(255, 255, 255, 0.1); padding-bottom: 16px;
    display: flex; justify-content: space-between; align-items: flex-end;
  }
  .title { font-size: 30px; font-weight: 800; }
  .title span { color: #f59e0b; }
  .badge { background: rgba(245, 158, 11, 0.15); color: #f59e0b; padding: 6px 14px; border-radius: 8px; font-size: 14px; font-weight: 700; }
  
  .steps-container {
    display: flex; flex-direction: column; gap: 14px;
    margin: 20px 0;
  }
  .step-row {
    background: #1e293b; border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px; padding: 18px 24px;
    display: flex; align-items: center; gap: 24px;
  }
  .step-num {
    font-size: 20px; font-weight: 900; color: #f59e0b;
    background: rgba(245, 158, 11, 0.15); border-radius: 10px;
    padding: 8px 16px; min-width: 90px; text-align: center;
  }
  .step-content { flex: 1; }
  .step-title { font-size: 18px; font-weight: 800; color: #ffffff; margin-bottom: 4px; }
  .step-desc { font-size: 14px; color: #94a3b8; line-height: 1.4; }
  
  .bottom-box {
    background: linear-gradient(90deg, rgba(99, 102, 241, 0.15), rgba(52, 211, 153, 0.15));
    border: 1px solid rgba(99, 102, 241, 0.3); border-radius: 12px;
    padding: 14px 20px; display: flex; justify-content: space-between; align-items: center;
    font-size: 15px; color: #e2e8f0; font-weight: 600;
  }
  .bottom-box span { color: #34d399; font-weight: 800; }
</style>
</head>
<body>
  <div class="header">
    <div>
      <div class="title">10월 20일 화요일 <span>실전 투자 대응 3대 수칙</span></div>
      <div style="font-size: 16px; color: #94a3b8; margin-top: 4px;">PBR 1.09배 더블 바닥(5,488pt - 5,554pt) 완성에 따른 최적 전략</div>
    </div>
    <div class="badge">Action Plan 10.20</div>
  </div>

  <div class="steps-container">
    <div class="step-row">
      <div class="step-num">수칙 01</div>
      <div class="step-content">
        <div class="step-title">뇌동 매도 자제 및 저평가 우량주 분할 매수 기조 유지</div>
        <div class="step-desc">15일 서킷브레이커(5,554)와 19일 저점(5,488)의 W자 쌍바닥 확인. 청산가치 지지력 입증으로 투매 지양</div>
      </div>
    </div>
    <div class="step-row">
      <div class="step-num">수칙 02</div>
      <div class="step-content">
        <div class="step-title">미국 반도체 반등 훈풍 속 삼성전자·SK하이닉스 수급 추적</div>
        <div class="step-desc">필라델피아 반도체 지수의 8일 만의 반등. 삼성전자에 대한 외국인 3일 연속 순매수 지속 여부가 핵심</div>
      </div>
    </div>
    <div class="step-row">
      <div class="step-num">수칙 03</div>
      <div class="step-content">
        <div class="step-title">3분기 실적 가시성이 뚜렷한 저PBR 주도주로 포트폴리오 압축</div>
        <div class="step-desc">미국 ESS 반사이익 2차전지, 견고한 수출의 현대차·기아, 밸류업 수혜 금융주 등 현금흐름 탄탄한 종목 집중</div>
      </div>
    </div>
  </div>

  <div class="bottom-box">
    <div>📊 코스피 12M Fwd PBR: <span>1.09배</span> · PER: <span>4.2배</span> (역사적 저평가 안전마진)</div>
    <div style="color: #a5b4fc;">ValueStockLabs Strategy</div>
  </div>
</body>
</html>"""
    }
}

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        for fname, config in HTML_TEMPLATES.items():
            page = await browser.new_page(
                viewport={"width": config["width"], "height": config["height"]},
                device_scale_factor=2
            )
            await page.set_content(config["html"], wait_until="networkidle")
            out_path = OUTPUT_DIR / fname
            await page.screenshot(path=str(out_path), type="png")
            await page.close()
            print(f"[성공] 이미지 생성 완료: {out_path}")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
