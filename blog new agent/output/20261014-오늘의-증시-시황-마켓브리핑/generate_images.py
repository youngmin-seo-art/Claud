import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

OUTPUT_DIR = Path(r"c:\Users\immnu\Desktop\Claud\blog new agent\output\20261014-오늘의-증시-시황-마켓브리핑\images")
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
      width: 600px;
      height: 600px;
      top: -150px;
      right: -130px;
      background: radial-gradient(circle, rgba(99, 102, 241, 0.4) 0%, transparent 70%);
      filter: blur(80px);
    }
    .glow-2 {
      position: absolute;
      width: 600px;
      height: 600px;
      bottom: -150px;
      left: -130px;
      background: radial-gradient(circle, rgba(16, 185, 129, 0.3) 0%, transparent 70%);
      filter: blur(80px);
    }
    .card {
      width: 100%;
      height: 100%;
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid rgba(255, 255, 255, 0.14);
      border-radius: 40px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      align-items: center;
      text-align: center;
      padding: 70px 50px;
      backdrop-filter: blur(25px);
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
      color: #34d399;
      background: rgba(16, 185, 129, 0.15);
      border: 1px solid rgba(16, 185, 129, 0.35);
      padding: 12px 30px;
      border-radius: 9999px;
      letter-spacing: 0.5px;
    }
    .header-badge span.dot {
      width: 10px;
      height: 10px;
      background-color: #10b981;
      border-radius: 50%;
      box-shadow: 0 0 12px #10b981;
    }
    .main-content {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 22px;
    }
    .title {
      font-size: 54px;
      font-weight: 900;
      line-height: 1.25;
      letter-spacing: -1.5px;
      color: #ffffff;
    }
    .title .highlight {
      background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .subtitle {
      font-size: 24px;
      color: #94a3b8;
      font-weight: 500;
      max-width: 820px;
      line-height: 1.5;
    }
    .chips-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 16px;
      width: 100%;
      max-width: 780px;
    }
    .chip {
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 20px;
      padding: 18px 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .chip-label {
      font-size: 17px;
      color: #cbd5e1;
      font-weight: 600;
    }
    .chip-value {
      font-size: 20px;
      font-weight: 800;
      color: #38bdf8;
    }
    .chip-value.up { color: #f87171; }
    .footer-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      width: 100%;
      border-top: 1px solid rgba(255, 255, 255, 0.1);
      padding-top: 24px;
    }
    .author-info {
      display: flex;
      align-items: center;
      gap: 12px;
      font-size: 18px;
      font-weight: 700;
      color: #f1f5f9;
    }
    .author-avatar {
      width: 36px;
      height: 36px;
      background: linear-gradient(135deg, #059669, #10b981);
      border-radius: 50%;
      display: flex;
      justify-content: center;
      align-items: center;
      font-size: 16px;
      font-weight: 900;
    }
    .date-badge {
      font-size: 16px;
      color: #94a3b8;
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
      <span>☕ 모닝 마켓 브리핑 | 오늘의 시황</span>
    </div>
    
    <div class="main-content">
      <h1 class="title">
        코스피 6,000선 사수 후 반등<br>
        <span class="highlight">美 9월 CPI & TSMC 실적 슈퍼위크</span>
      </h1>
      <p class="subtitle">
        전일 4.5조 원 외인 투매 충격 극복 · 반도체 투톱 기술적 반등<br>
        인플레이션 분수령 및 실적 시즌 3대 실전 행동 강령
      </p>
      
      <div class="chips-grid">
        <div class="chip">
          <span class="chip-label">코스피 개장 반등</span>
          <span class="chip-value up">6,132선 회복 (+1.6%)</span>
        </div>
        <div class="chip">
          <span class="chip-label">삼성전자 반발 매수</span>
          <span class="chip-value up">238,000원 (+2.6%)</span>
        </div>
        <div class="chip">
          <span class="chip-label">원/달러 환율</span>
          <span class="chip-value">1,474.50원 안정화 시도</span>
        </div>
        <div class="chip">
          <span class="chip-label">핵심 매크로 분기점</span>
          <span class="chip-value">오늘 밤 美 9월 CPI</span>
        </div>
      </div>
    </div>
    
    <div class="footer-bar">
      <div class="author-info">
        <div class="author-avatar">V</div>
        <span>valuestocklabs.com 리서치팀</span>
      </div>
      <div class="date-badge">📅 2026-10-14 데일리 리포트</div>
    </div>
  </div>
</body>
</html>
"""

# 2. 본문 인포그래픽 1: 증시 급락 vs 반등 비교 (body-1.png)
body1_html = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 1200px;
      height: 700px;
      background: #0b0f19;
      font-family: 'Pretendard', sans-serif;
      color: #ffffff;
      padding: 40px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid rgba(255, 255, 255, 0.12);
      padding-bottom: 20px;
    }
    .title-wrap h2 {
      font-size: 28px;
      font-weight: 800;
      color: #f8fafc;
      letter-spacing: -0.5px;
    }
    .title-wrap p {
      font-size: 16px;
      color: #94a3b8;
      margin-top: 4px;
    }
    .badge {
      background: rgba(56, 189, 248, 0.15);
      border: 1px solid #38bdf8;
      color: #38bdf8;
      font-size: 14px;
      font-weight: 700;
      padding: 8px 18px;
      border-radius: 9999px;
    }
    .grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 24px;
      margin: 24px 0;
    }
    .card {
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 20px;
      padding: 28px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .card.alert {
      border-left: 6px solid #ef4444;
      background: linear-gradient(145deg, rgba(239, 68, 68, 0.05), rgba(255, 255, 255, 0.02));
    }
    .card.rebound {
      border-left: 6px solid #10b981;
      background: linear-gradient(145deg, rgba(16, 185, 129, 0.05), rgba(255, 255, 255, 0.02));
    }
    .card-title {
      font-size: 20px;
      font-weight: 700;
      margin-bottom: 16px;
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .card.alert .card-title { color: #f87171; }
    .card.rebound .card-title { color: #34d399; }
    .stat-list {
      display: flex;
      flex-direction: column;
      gap: 12px;
    }
    .stat-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 10px 14px;
      background: rgba(255, 255, 255, 0.03);
      border-radius: 12px;
    }
    .stat-label { font-size: 15px; color: #cbd5e1; }
    .stat-val { font-size: 16px; font-weight: 800; }
    .down-val { color: #60a5fa; }
    .up-val { color: #f87171; }
    .footer-note {
      background: rgba(255, 255, 255, 0.03);
      border-radius: 12px;
      padding: 14px 20px;
      font-size: 14px;
      color: #94a3b8;
      display: flex;
      justify-content: space-between;
    }
  </style>
</head>
<body>
  <div class="header">
    <div class="title-wrap">
      <h2>📊 국내 증시 긴급 진단: 10/13 폭락 vs 10/14 기술적 반등</h2>
      <p>외국인 4.5조 원 투매 사이드카 충격 이후 저가 반발 매수세 유입 국면</p>
    </div>
    <div class="badge">실시간 마켓 진단</div>
  </div>

  <div class="grid">
    <div class="card alert">
      <div class="card-title">⚠️ 10월 13일 (검은 화요일 충격)</div>
      <div class="stat-list">
        <div class="stat-row">
          <span class="stat-label">코스피 지수 마감</span>
          <span class="stat-val down-val">6,035.35 (-5.46% 폭락)</span>
        </div>
        <div class="stat-row">
          <span class="stat-label">외국인 투자자 수급</span>
          <span class="stat-val down-val">4조 5,200억 원 순매도</span>
        </div>
        <div class="stat-row">
          <span class="stat-label">주요 조치</span>
          <span class="stat-val">2달 만에 '매도 사이드카' 발동</span>
        </div>
        <div class="stat-row">
          <span class="stat-label">삼성전자 / SK하이닉스</span>
          <span class="stat-val down-val">-7.39% / -10.09% 급락</span>
        </div>
      </div>
    </div>

    <div class="card rebound">
      <div class="card-title">🚀 10월 14일 (개장 후 기술적 반등)</div>
      <div class="stat-list">
        <div class="stat-row">
          <span class="stat-label">코스피 지수 흐름</span>
          <span class="stat-val up-val">6,132선 회복 (+1.61%)</span>
        </div>
        <div class="stat-row">
          <span class="stat-label">수급 특징</span>
          <span class="stat-val up-val">외인 선물 환매수 + 기관 순매수</span>
        </div>
        <div class="stat-row">
          <span class="stat-label">시장 심리</span>
          <span class="stat-val">낙폭 과대 인식 및 저가 매수세</span>
        </div>
        <div class="stat-row">
          <span class="stat-label">삼성전자 / SK하이닉스</span>
          <span class="stat-val up-val">+2.59% / +2.91% 반등</span>
        </div>
      </div>
    </div>
  </div>

  <div class="footer-note">
    <span>💡 분석 포인트: 전일 과도한 패닉 셀링 후 저가 매수세가 지수 하방을 방어하고 있으나, 9월 CPI 발표 전까지 분할 대응 필수</span>
    <span>출처: KRX & valuestocklabs</span>
  </div>
</body>
</html>
"""

# 3. 본문 인포그래픽 2: 반도체 CXMT 노이즈 vs HBM 초격차 (body-2.png)
body2_html = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 1200px;
      height: 700px;
      background: #090d16;
      font-family: 'Pretendard', sans-serif;
      color: #ffffff;
      padding: 40px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .header {
      border-bottom: 1px solid rgba(255, 255, 255, 0.12);
      padding-bottom: 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .title-wrap h2 {
      font-size: 28px;
      font-weight: 800;
      color: #ffffff;
    }
    .title-wrap p {
      font-size: 16px;
      color: #94a3b8;
      margin-top: 4px;
    }
    .badge {
      background: rgba(168, 85, 247, 0.15);
      border: 1px solid #c084fc;
      color: #c084fc;
      font-size: 14px;
      font-weight: 700;
      padding: 8px 18px;
      border-radius: 9999px;
    }
    .grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 24px;
      margin: 24px 0;
    }
    .card {
      background: rgba(255, 255, 255, 0.035);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 20px;
      padding: 26px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }
    .card-head {
      display: flex;
      align-items: center;
      gap: 12px;
      font-size: 20px;
      font-weight: 800;
      padding-bottom: 14px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }
    .cxmt { color: #fb923c; }
    .kr-semi { color: #38bdf8; }
    .item-box {
      background: rgba(255, 255, 255, 0.025);
      border-radius: 12px;
      padding: 14px 16px;
    }
    .item-label { font-size: 14px; color: #94a3b8; font-weight: 600; margin-bottom: 4px; }
    .item-desc { font-size: 15px; color: #f1f5f9; line-height: 1.5; font-weight: 500; }
    .conclusion-bar {
      background: linear-gradient(90deg, rgba(56, 189, 248, 0.1), rgba(168, 85, 247, 0.1));
      border: 1px solid rgba(56, 189, 248, 0.3);
      border-radius: 14px;
      padding: 16px 24px;
      font-size: 15px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .conclusion-bar strong { color: #38bdf8; }
  </style>
</head>
<body>
  <div class="header">
    <div class="title-wrap">
      <h2>⚡ 반도체 팩트체크: 중국 CXMT 추격 노이즈 vs 한국 HBM 초격차</h2>
      <p>단기 차익 실현 빌미가 된 시장 우려와 실제 펀더멘털의 격차 분석</p>
    </div>
    <div class="badge">심층 팩트체크</div>
  </div>

  <div class="grid">
    <div class="card">
      <div class="card-head cxmt">
        <span>🇨🇳 시장 공포 요인 (중국 CXMT 이슈)</span>
      </div>
      <div class="item-box">
        <div class="item-label">주력 생산 영역</div>
        <div class="item-desc">DDR4 및 구형 모바일 LPDDR4 등 중저가 레거시 메모리 중심</div>
      </div>
      <div class="item-box">
        <div class="item-label">수율 및 기술 한계</div>
        <div class="item-desc">정부 보조금 의존, EUV 노광장비 부재로 1a/1b D램 미세화 진입 장벽</div>
      </div>
      <div class="item-box">
        <div class="item-label">시장 영향 평가</div>
        <div class="item-desc">단기 글로벌 패시브 자금의 차익 실현 '명분'으로 과도하게 활용됨</div>
      </div>
    </div>

    <div class="card">
      <div class="card-head kr-semi">
        <span>🇰🇷 국내 반도체 투톱 펀더멘털 (삼성전자·SK하이닉스)</span>
      </div>
      <div class="item-box">
        <div class="item-label">독점적 HBM 점유율</div>
        <div class="item-desc">HBM3E 및 차세대 16단 HBM4 시장 글로벌 점유율 90% 이상 장악</div>
      </div>
      <div class="item-box">
        <div class="item-label">실물 수출 폭증세</div>
        <div class="item-desc">10월 1~10일 반도체 수출 122억 달러 기록 (전년비 +170.9% 사상 최대)</div>
      </div>
      <div class="item-box">
        <div class="item-label">중장기 전망</div>
        <div class="item-desc">엔비디아·빅테크 AI 가속기 공급 확정으로 2026~2027년 실적 가시성 절대적</div>
      </div>
    </div>
  </div>

  <div class="conclusion-bar">
    <span>📌 <strong>핵심 결론:</strong> 이번 반도체 급락은 펀더멘털 훼손이 아닌, 단기 고점 인식에 따른 오버슈팅성 조정입니다.</span>
    <span>데이터 출처: 관세청 및 글로벌 시장조사기관</span>
  </div>
</body>
</html>
"""

# 4. 본문 인포그래픽 3: 슈퍼위크 캘린더 & 3대 투자 행동 강령 (body-3.png)
body3_html = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 1200px;
      height: 700px;
      background: #080d1a;
      font-family: 'Pretendard', sans-serif;
      color: #ffffff;
      padding: 40px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .header {
      border-bottom: 1px solid rgba(255, 255, 255, 0.12);
      padding-bottom: 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .title-wrap h2 {
      font-size: 28px;
      font-weight: 800;
      color: #ffffff;
    }
    .title-wrap p {
      font-size: 16px;
      color: #94a3b8;
      margin-top: 4px;
    }
    .badge {
      background: rgba(16, 185, 129, 0.15);
      border: 1px solid #10b981;
      color: #10b981;
      font-size: 14px;
      font-weight: 700;
      padding: 8px 18px;
      border-radius: 9999px;
    }
    .grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 24px;
      margin: 24px 0;
    }
    .box {
      background: rgba(255, 255, 255, 0.035);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 20px;
      padding: 24px;
      display: flex;
      flex-direction: column;
      gap: 14px;
    }
    .box-title {
      font-size: 20px;
      font-weight: 800;
      color: #38bdf8;
      display: flex;
      align-items: center;
      gap: 10px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      padding-bottom: 10px;
    }
    .timeline-item {
      display: flex;
      gap: 14px;
      background: rgba(255, 255, 255, 0.02);
      padding: 12px 14px;
      border-radius: 12px;
      align-items: center;
    }
    .date-tag {
      background: rgba(56, 189, 248, 0.2);
      color: #38bdf8;
      padding: 6px 12px;
      border-radius: 8px;
      font-size: 14px;
      font-weight: 700;
      white-space: nowrap;
    }
    .event-info { font-size: 15px; color: #f1f5f9; font-weight: 600; line-height: 1.4; }
    .action-item {
      display: flex;
      gap: 14px;
      background: rgba(255, 255, 255, 0.02);
      padding: 12px 14px;
      border-radius: 12px;
      align-items: center;
    }
    .num-tag {
      background: rgba(16, 185, 129, 0.2);
      color: #34d399;
      width: 32px;
      height: 32px;
      display: flex;
      justify-content: center;
      align-items: center;
      border-radius: 50%;
      font-size: 15px;
      font-weight: 800;
      flex-shrink: 0;
    }
    .action-text { font-size: 15px; color: #e2e8f0; line-height: 1.4; }
    .bottom-bar {
      background: rgba(255, 255, 255, 0.04);
      border-radius: 12px;
      padding: 14px 20px;
      font-size: 14px;
      color: #cbd5e1;
      text-align: center;
    }
  </style>
</head>
<body>
  <div class="header">
    <div class="title-wrap">
      <h2>🎯 10월 글로벌 슈퍼위크 캘린더 & 3대 실전 행동 강령</h2>
      <p>매크로 변곡점 확인과 시장 복원력에 맞춘 스마트 리스크 관리 가이드</p>
    </div>
    <div class="badge">투자 행동 로드맵</div>
  </div>

  <div class="grid">
    <div class="box">
      <div class="box-title">📅 이번 주 핵심 이벤트 캘린더</div>
      <div class="timeline-item">
        <span class="date-tag">10/14 (수) 21:30</span>
        <span class="event-info">미국 9월 소비자물가지수(CPI) 발표<br>(11월 금리 인하 경로 결정)</span>
      </div>
      <div class="timeline-item">
        <span class="date-tag">10/15 (목) 장중</span>
        <span class="event-info">대만 TSMC 3분기 실적 콘퍼런스콜<br>(AI 파운드리 수요 및 연간 CAPEX)</span>
      </div>
      <div class="timeline-item">
        <span class="date-tag">10/16~17</span>
        <span class="event-info">ASML 수주 잔고 & 월가 메이저 금융주<br>(반도체 장비 수요 및 미국 소비 점검)</span>
      </div>
    </div>

    <div class="box">
      <div class="box-title">🛡️ 3대 실전 투자 행동 강령</div>
      <div class="action-item">
        <div class="num-tag">1</div>
        <div class="action-text"><strong>추격 매수 자제 & 6,100선 안착 확인:</strong><br>단기 급등 시 흥분하지 말고 분할 매수 타점 탐색</div>
      </div>
      <div class="action-item">
        <div class="num-tag">2</div>
        <div class="action-text"><strong>CPI 발표 전까지 현금 비중 20% 확보:</strong><br>물가 서프라이즈 발생 시 저가 줍줍 버퍼 마련</div>
      </div>
      <div class="action-item">
        <div class="num-tag">3</div>
        <div class="action-text"><strong>성장주·가치주 바벨 전략 구축:</strong><br>AI 반도체 50% + 방산/조선/배당 가치주 50% 분산</div>
      </div>
    </div>
  </div>

  <div class="bottom-bar">
    <span>💡 <strong>성공 투자 원칙:</strong> 극단적 공포 국면에서는 투매를 멈추고, 실적 펀더멘털이 검증된 1등 주도주를 선별할 때입니다.</span>
  </div>
</body>
</html>
"""

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        
        # 1. 썸네일 캡처 (1080x1080)
        page1 = await browser.new_page(viewport={"width": 1080, "height": 1080}, device_scale_factor=2)
        await page1.set_content(thumbnail_html)
        await page1.wait_for_load_state("networkidle")
        await page1.screenshot(path=str(OUTPUT_DIR / "thumbnail.png"))
        print("[완료] thumbnail.png 캡처")
        await page1.close()

        # 2. 본문 1 캡처 (1200x700)
        page2 = await browser.new_page(viewport={"width": 1200, "height": 700}, device_scale_factor=2)
        await page2.set_content(body1_html)
        await page2.wait_for_load_state("networkidle")
        await page2.screenshot(path=str(OUTPUT_DIR / "body-1.png"))
        print("[완료] body-1.png 캡처")
        await page2.close()

        # 3. 본문 2 캡처 (1200x700)
        page3 = await browser.new_page(viewport={"width": 1200, "height": 700}, device_scale_factor=2)
        await page3.set_content(body2_html)
        await page3.wait_for_load_state("networkidle")
        await page3.screenshot(path=str(OUTPUT_DIR / "body-2.png"))
        print("[완료] body-2.png 캡처")
        await page3.close()

        # 4. 본문 3 캡처 (1200x700)
        page4 = await browser.new_page(viewport={"width": 1200, "height": 700}, device_scale_factor=2)
        await page4.set_content(body3_html)
        await page4.wait_for_load_state("networkidle")
        await page4.screenshot(path=str(OUTPUT_DIR / "body-3.png"))
        print("[완료] body-3.png 캡처")
        await page4.close()

        await browser.close()
        print("🎉 모든 이미지 캡처 완료!")

if __name__ == "__main__":
    asyncio.run(main())
