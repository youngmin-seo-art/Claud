import asyncio
import os
from pathlib import Path
from playwright.async_api import async_playwright

OUTPUT_DIR = Path(r"c:\Users\immnu\Desktop\Claud\blog new agent\output\한미반도체-AI반도체-기업분석\images")
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
      background: linear-gradient(135deg, #070b14 0%, #0f172a 45%, #1e1b4b 100%);
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
      background: radial-gradient(circle, rgba(99, 102, 241, 0.4) 0%, transparent 70%);
      filter: blur(80px);
    }
    .glow-2 {
      position: absolute;
      width: 550px;
      height: 550px;
      bottom: -120px;
      left: -120px;
      background: radial-gradient(circle, rgba(14, 165, 233, 0.35) 0%, transparent 70%);
      filter: blur(80px);
    }
    .card {
      width: 100%;
      height: 100%;
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 40px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      align-items: center;
      text-align: center;
      padding: 70px 50px;
      backdrop-filter: blur(25px);
      box-shadow: 0 30px 70px rgba(0, 0, 0, 0.7);
      position: relative;
      z-index: 10;
    }
    .badge-wrap {
      display: flex;
      gap: 14px;
    }
    .badge {
      font-size: 22px;
      font-weight: 700;
      color: #38bdf8;
      background: rgba(56, 189, 248, 0.15);
      border: 1px solid rgba(56, 189, 248, 0.4);
      padding: 10px 24px;
      border-radius: 9999px;
      letter-spacing: -0.5px;
    }
    .badge-sub {
      font-size: 22px;
      font-weight: 700;
      color: #a855f7;
      background: rgba(168, 85, 247, 0.15);
      border: 1px solid rgba(168, 85, 247, 0.4);
      padding: 10px 24px;
      border-radius: 9999px;
    }
    .title-area {
      display: flex;
      flex-direction: column;
      gap: 18px;
    }
    .ticker {
      font-size: 32px;
      font-weight: 800;
      color: #94a3b8;
      letter-spacing: 2px;
    }
    .title {
      font-size: 64px;
      font-weight: 900;
      line-height: 1.25;
      letter-spacing: -1.5px;
      background: linear-gradient(180deg, #ffffff 30%, #cbd5e1 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .highlight {
      background: linear-gradient(90deg, #38bdf8, #818cf8);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .desc {
      font-size: 24px;
      color: #94a3b8;
      font-weight: 500;
      line-height: 1.5;
      max-width: 780px;
    }
    .stats-row {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 20px;
      width: 100%;
    }
    .stat-box {
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 20px;
      padding: 22px 16px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    .stat-label {
      font-size: 17px;
      color: #94a3b8;
      font-weight: 600;
    }
    .stat-val {
      font-size: 30px;
      font-weight: 800;
      color: #38bdf8;
    }
    .footer-brand {
      font-size: 19px;
      font-weight: 700;
      color: #64748b;
      letter-spacing: 1px;
    }
  </style>
</head>
<body>
  <div class="glow-1"></div>
  <div class="glow-2"></div>
  <div class="card">
    <div class="badge-wrap">
      <span class="badge">AI반도체 심층 기업분석</span>
      <span class="badge-sub">글로벌 슈퍼 을(乙)</span>
    </div>
    
    <div class="title-area">
      <div class="ticker">KOSDAQ 042700</div>
      <h1 class="title">한미반도체<br><span class="highlight">HBM4 TC본더 1위</span><br>독점력 & 괴물 마진</h1>
      <p class="desc">글로벌 점유율 71.2% 부동의 세계 1위 · 2분기 영업이익률 51.9% · 곽동신 회장 702억 사재 매입의 함의</p>
    </div>

    <div class="stats-row">
      <div class="stat-box">
        <span class="stat-label">글로벌 점유율</span>
        <span class="stat-val" style="color: #38bdf8;">71.2% (1위)</span>
      </div>
      <div class="stat-box">
        <span class="stat-label">2Q26 영업이익률</span>
        <span class="stat-val" style="color: #10b981;">51.9%</span>
      </div>
      <div class="stat-box">
        <span class="stat-label">목표 생산능력</span>
        <span class="stat-val" style="color: #a855f7;">연 2조 원</span>
      </div>
    </div>

    <div class="footer-brand">VALUETOCKLABS.COM</div>
  </div>
</body>
</html>
"""

# 2. 본문 1: 비교 표 (Comparison Table, 1080x700)
body1_html = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 1080px;
      height: 700px;
      background: #0b0f19;
      font-family: 'Pretendard', sans-serif;
      display: flex;
      justify-content: center;
      align-items: center;
      color: #ffffff;
      padding: 40px;
    }
    .container {
      width: 100%;
      height: 100%;
      background: #111827;
      border: 1px solid #1f2937;
      border-radius: 28px;
      padding: 44px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      box-shadow: 0 20px 50px rgba(0,0,0,0.5);
    }
    .header {
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      border-bottom: 2px solid #1f2937;
      padding-bottom: 20px;
    }
    .title-box h2 {
      font-size: 32px;
      font-weight: 800;
      color: #f8fafc;
      letter-spacing: -0.5px;
    }
    .title-box p {
      font-size: 17px;
      color: #94a3b8;
      margin-top: 6px;
    }
    .tag {
      background: rgba(56, 189, 248, 0.12);
      border: 1px solid rgba(56, 189, 248, 0.35);
      color: #38bdf8;
      font-size: 15px;
      font-weight: 700;
      padding: 6px 16px;
      border-radius: 9999px;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 15px;
    }
    th, td {
      padding: 16px 18px;
      text-align: center;
      font-size: 17px;
    }
    th {
      background: #1e293b;
      color: #cbd5e1;
      font-weight: 700;
      font-size: 18px;
      border-top: 1px solid #334155;
      border-bottom: 2px solid #334155;
    }
    th:first-child { text-align: left; border-top-left-radius: 12px; }
    th:last-child { border-top-right-radius: 12px; }
    td {
      border-bottom: 1px solid #1e293b;
      color: #e2e8f0;
      vertical-align: middle;
    }
    td:first-child {
      text-align: left;
      font-weight: 700;
      color: #94a3b8;
    }
    .highlight-col {
      background: rgba(56, 189, 248, 0.08);
      color: #38bdf8;
      font-weight: 800;
    }
    .badge-win {
      display: inline-block;
      background: #0284c7;
      color: #ffffff;
      padding: 4px 10px;
      border-radius: 6px;
      font-size: 14px;
      font-weight: 800;
      margin-left: 6px;
    }
    .footer {
      display: flex;
      justify-content: space-between;
      color: #64748b;
      font-size: 14px;
      font-weight: 500;
      padding-top: 10px;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <div class="title-box">
        <h2>글로벌 HBM TC 본더 주요 제조사 역량 비교</h2>
        <p>글로벌 시장점유율, 양산 레퍼런스, 마진율 및 핵심 차별화 경쟁력 대조</p>
      </div>
      <span class="tag">심층 경쟁구도 분석</span>
    </div>

    <table>
      <thead>
        <tr>
          <th style="width: 22%;">비교 항목</th>
          <th style="width: 30%; background: #0369a1; color: #ffffff;">한미반도체 (042700)</th>
          <th style="width: 24%;">한화세미텍 (신규 진입)</th>
          <th style="width: 24%;">ASMPT / 신카와 등</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>글로벌 시장점유율</td>
          <td class="highlight-col">71.2% <span class="badge-win">압도적 1위</span></td>
          <td>초기 진입 (점유율 점진 확대)</td>
          <td>15% ~ 20% 내외 분산</td>
        </tr>
        <tr>
          <td>주력 라인업</td>
          <td class="highlight-col">TC본더 4.5 그리핀 / 드래곤</td>
          <td>자체 개발 TC 본더</td>
          <td>선택적 TC본더 모델</td>
        </tr>
        <tr>
          <td>주요 고객사 기반</td>
          <td class="highlight-col">SK하이닉스 + 마이크론 + 북미</td>
          <td>SK하이닉스 (듀얼 벤더 진입)</td>
          <td>마이크론 및 일부 파운드리</td>
        </tr>
        <tr>
          <td>HBM 특허 포트폴리오</td>
          <td class="highlight-col">160건 이상 원천 특허 독점</td>
          <td>개발 진행 및 특허 공방 대응</td>
          <td>일반 패키징 중심 특허</td>
        </tr>
        <tr>
          <td>영업이익률 (OPM)</td>
          <td class="highlight-col">50% ~ 51.9% (ASML급 초고마진)</td>
          <td>10% ~ 15% 수준 추정</td>
          <td>12% ~ 18% 수준</td>
        </tr>
      </tbody>
    </table>

    <div class="footer">
      <span>출처: 테크인사이츠(TechInsights), 금융감독원 전자공시시스템(DART), 발루스탁랩스 정리</span>
      <span>valuestocklabs.com</span>
    </div>
  </div>
</body>
</html>
"""

# 3. 본문 2: 단계별 다이어그램 (Step-by-Step Diagram, 1080x680)
body2_html = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 1080px;
      height: 680px;
      background: #090d16;
      font-family: 'Pretendard', sans-serif;
      display: flex;
      justify-content: center;
      align-items: center;
      color: #ffffff;
      padding: 40px;
    }
    .container {
      width: 100%;
      height: 100%;
      background: #0f172a;
      border: 1px solid #1e293b;
      border-radius: 28px;
      padding: 44px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      box-shadow: 0 20px 50px rgba(0,0,0,0.6);
    }
    .header {
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      border-bottom: 2px solid #1e293b;
      padding-bottom: 20px;
    }
    .title-box h2 {
      font-size: 32px;
      font-weight: 800;
      color: #f8fafc;
    }
    .title-box p {
      font-size: 17px;
      color: #94a3b8;
      margin-top: 6px;
    }
    .steps-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
      margin-top: 25px;
      position: relative;
    }
    .step-card {
      background: rgba(30, 41, 59, 0.7);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 20px;
      padding: 24px 20px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
    }
    .step-card.active {
      border: 1px solid #38bdf8;
      background: rgba(14, 165, 233, 0.1);
      box-shadow: 0 10px 25px rgba(56, 189, 248, 0.15);
    }
    .step-badge {
      display: inline-block;
      align-self: flex-start;
      font-size: 14px;
      font-weight: 800;
      padding: 4px 12px;
      border-radius: 9999px;
      margin-bottom: 14px;
    }
    .badge-gray { background: #334155; color: #94a3b8; }
    .badge-blue { background: #0284c7; color: #ffffff; }
    .badge-indigo { background: #4f46e5; color: #ffffff; }
    .badge-purple { background: #9333ea; color: #ffffff; }
    
    .step-title {
      font-size: 20px;
      font-weight: 800;
      color: #ffffff;
      margin-bottom: 8px;
    }
    .step-device {
      font-size: 16px;
      font-weight: 700;
      color: #38bdf8;
      margin-bottom: 12px;
    }
    .step-desc {
      font-size: 14px;
      color: #cbd5e1;
      line-height: 1.5;
    }
    .footer {
      display: flex;
      justify-content: space-between;
      color: #64748b;
      font-size: 14px;
      padding-top: 10px;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <div class="title-box">
        <h2>HBM 세대별 진화와 한미반도체 본더 로드맵</h2>
        <p>HBM3부터 차세대 하이브리드 본딩까지 이어지는 선제적 기술 대응</p>
      </div>
      <span style="color: #38bdf8; font-weight: 700; font-size: 16px;">기술 로드맵</span>
    </div>

    <div class="steps-grid">
      <!-- Step 1 -->
      <div class="step-card">
        <div>
          <span class="step-badge badge-gray">1단계 (2023)</span>
          <div class="step-title">HBM3 / 8단</div>
          <div class="step-device">듀얼 TC본더 1.0 드래곤</div>
        </div>
        <p class="step-desc">SK하이닉스 양산 라인 최초 대량 공급 성공, HBM 붐 초입 독점적 공급망 형성</p>
      </div>

      <!-- Step 2 -->
      <div class="step-card">
        <div>
          <span class="step-badge badge-blue">2단계 (2024~2025)</span>
          <div class="step-title">HBM3E / 12단</div>
          <div class="step-device">듀얼 TC본더 1.0 그리핀</div>
        </div>
        <p class="step-desc">엔비디아 H200/B200 탑재용. 초정밀 급열·급랭 제어로 칩 휨 방지 및 마이크론 수주 성공</p>
      </div>

      <!-- Step 3 -->
      <div class="step-card active">
        <div>
          <span class="step-badge badge-indigo">3단계 (2026 현재)</span>
          <div class="step-title">HBM4 / 16단</div>
          <div class="step-device">TC본더 4.5 그리핀</div>
        </div>
        <p class="step-desc">로직 베이스 다이(TSMC 파운드리) 결합 및 16단 초고적층 완벽 지원, 독점적 지위 수성</p>
      </div>

      <!-- Step 4 -->
      <div class="step-card">
        <div>
          <span class="step-badge badge-purple">4단계 (2028~)</span>
          <div class="step-title">HBM4E / HBM5</div>
          <div class="step-device">2세대 하이브리드 본더</div>
        </div>
        <p class="step-desc">범프 없는 직접 Cu-Cu 원자 접합. 연내 프로토타입 공개 및 전용 7공장 선제 구축 중</p>
      </div>
    </div>

    <div class="footer">
      <span>포인트: 16단 HBM4까지는 TC 본더가 메인이며, 하이브리드 본더 역시 선제 개발 완료</span>
      <span>valuestocklabs.com</span>
    </div>
  </div>
</body>
</html>
"""

# 4. 본문 3: 핵심 포인트 카드 (Key Points Grid, 1080x720)
body3_html = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 1080px;
      height: 720px;
      background: #080c15;
      font-family: 'Pretendard', sans-serif;
      display: flex;
      justify-content: center;
      align-items: center;
      color: #ffffff;
      padding: 40px;
    }
    .container {
      width: 100%;
      height: 100%;
      background: #0f172a;
      border: 1px solid #1e293b;
      border-radius: 28px;
      padding: 44px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      box-shadow: 0 20px 50px rgba(0,0,0,0.6);
    }
    .header {
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      border-bottom: 2px solid #1e293b;
      padding-bottom: 18px;
    }
    .title-box h2 {
      font-size: 32px;
      font-weight: 800;
      color: #f8fafc;
    }
    .title-box p {
      font-size: 17px;
      color: #94a3b8;
      margin-top: 6px;
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 20px;
      margin-top: 20px;
    }
    .card {
      background: rgba(30, 41, 59, 0.6);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 20px;
      padding: 26px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      backdrop-filter: blur(10px);
    }
    .card-top {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .icon-box {
      width: 44px;
      height: 44px;
      border-radius: 12px;
      display: flex;
      justify-content: center;
      align-items: center;
      font-size: 22px;
      font-weight: 800;
    }
    .icon-1 { background: rgba(56, 189, 248, 0.15); color: #38bdf8; }
    .icon-2 { background: rgba(16, 185, 129, 0.15); color: #10b981; }
    .icon-3 { background: rgba(245, 158, 11, 0.15); color: #f59e0b; }
    .icon-4 { background: rgba(168, 85, 247, 0.15); color: #a855f7; }

    .card-title {
      font-size: 21px;
      font-weight: 800;
      color: #ffffff;
    }
    .card-metric {
      font-size: 26px;
      font-weight: 800;
      color: #38bdf8;
      letter-spacing: -0.5px;
    }
    .card-desc {
      font-size: 15px;
      color: #cbd5e1;
      line-height: 1.5;
    }
    .footer {
      display: flex;
      justify-content: space-between;
      color: #64748b;
      font-size: 14px;
      padding-top: 10px;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <div class="title-box">
        <h2>한미반도체 핵심 투자 포인트 4가지</h2>
        <p>글로벌 독점력, 괴물 같은 마진 체력, 대규모 캐파 증설 및 주주환원</p>
      </div>
      <span style="color: #38bdf8; font-weight: 700; font-size: 16px;">밸류에이션 요약</span>
    </div>

    <div class="grid">
      <!-- Point 1 -->
      <div class="card">
        <div class="card-top">
          <div class="icon-box icon-1">01</div>
          <div class="card-title">HBM TC본더 세계 1위</div>
        </div>
        <div class="card-metric">글로벌 점유율 71.2%</div>
        <p class="card-desc">160여 건 특허 그물망과 SK하이닉스·마이크론 양산 검증을 바탕으로 대체 불가능한 슈퍼 을(乙) 지위 유지</p>
      </div>

      <!-- Point 2 -->
      <div class="card">
        <div class="card-top">
          <div class="icon-box icon-2">02</div>
          <div class="card-title">ASML급 괴물 마진 체력</div>
        </div>
        <div class="card-metric" style="color: #10b981;">2Q26 OPM 51.9%</div>
        <p class="card-desc">핵심 부품 내재화율 90% 이상과 강력한 가격 결정력(Pricing Power)으로 하드웨어 장비사 중 전 세계 최상위 수익성 기록</p>
      </div>

      <!-- Point 3 -->
      <div class="card">
        <div class="card-top">
          <div class="icon-box icon-3">03</div>
          <div class="card-title">연 2조 원 캐파 & 테라팹</div>
        </div>
        <div class="card-metric" style="color: #f59e0b;">8공장 착공 & 북미 확장</div>
        <p class="card-desc">일론 머스크의 1TW 테라팹 프로젝트 대응 및 한미USA 설립, 8공장 신설로 납기 3~6개월 단축 경쟁력 확보</p>
      </div>

      <!-- Point 4 -->
      <div class="card">
        <div class="card-top">
          <div class="icon-box icon-4">04</div>
          <div class="card-title">대주주 사재 매입 & 소각</div>
        </div>
        <div class="card-metric" style="color: #a855f7;">702억 매수 + 1300억 소각</div>
        <p class="card-desc">곽동신 회장의 2023~2026년 사재 702억 장내 매입 및 대규모 자사주 소각으로 주당 가치를 극대화하는 선진 주주환원</p>
      </div>
    </div>

    <div class="footer">
      <span>체크포인트: 2026년 하반기 증권가 평균 목표주가 285,000원 (최고 50만 원)</span>
      <span>valuestocklabs.com</span>
    </div>
  </div>
</body>
</html>
"""

# 5. 본문 4: 인용/강조 박스 (Quote & Callout Box, 1080x600)
body4_html = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 1080px;
      height: 600px;
      background: #090e18;
      font-family: 'Pretendard', sans-serif;
      display: flex;
      justify-content: center;
      align-items: center;
      color: #ffffff;
      padding: 40px;
    }
    .container {
      width: 100%;
      height: 100%;
      background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
      border: 1px solid #312e81;
      border-radius: 28px;
      padding: 50px 60px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
      overflow: hidden;
      box-shadow: 0 25px 60px rgba(0,0,0,0.7);
    }
    .quote-mark {
      position: absolute;
      top: 20px;
      left: 40px;
      font-size: 140px;
      line-height: 1;
      color: rgba(99, 102, 241, 0.12);
      font-family: serif;
      pointer-events: none;
    }
    .top-badge {
      display: inline-flex;
      align-items: center;
      gap: 10px;
      background: rgba(99, 102, 241, 0.2);
      border: 1px solid rgba(99, 102, 241, 0.5);
      color: #a5b4fc;
      padding: 8px 18px;
      border-radius: 9999px;
      font-size: 16px;
      font-weight: 700;
      align-self: flex-start;
      z-index: 2;
    }
    .main-content {
      z-index: 2;
      display: flex;
      flex-direction: column;
      gap: 20px;
    }
    .statement {
      font-size: 34px;
      font-weight: 800;
      line-height: 1.4;
      color: #ffffff;
      letter-spacing: -1px;
    }
    .statement .hl {
      color: #38bdf8;
      background: linear-gradient(90deg, #38bdf8, #818cf8);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .detail-row {
      display: flex;
      gap: 30px;
      padding-top: 10px;
      border-top: 1px solid rgba(255, 255, 255, 0.1);
    }
    .detail-item {
      display: flex;
      flex-direction: column;
      gap: 4px;
    }
    .detail-label {
      font-size: 14px;
      color: #94a3b8;
      font-weight: 600;
    }
    .detail-val {
      font-size: 22px;
      font-weight: 800;
      color: #ffffff;
    }
    .footer {
      display: flex;
      justify-content: space-between;
      color: #64748b;
      font-size: 14px;
      z-index: 2;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="quote-mark">“</div>
    
    <div class="top-badge">
      <span>책임경영 & 압도적 펀더멘털</span>
    </div>

    <div class="main-content">
      <div class="statement">
        "하드웨어 장비사에서 <span class="hl">영업이익률 51.9%</span>는 독점력의 증거이며,<br>
        대주주의 <span class="hl">사재 702억 매입</span>은 미래 성장에 대한 확신이다."
      </div>
      
      <div class="detail-row">
        <div class="detail-item">
          <span class="detail-label">2023~2026 곽동신 회장 사재 매입</span>
          <span class="detail-val" style="color: #38bdf8;">702억 원 이상 (74만 주)</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">창사 이래 최대 자사주 소각</span>
          <span class="detail-val" style="color: #10b981;">1,300억 원 상당 (주당가치 제고)</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">2026년 2분기 연결 영업이익률</span>
          <span class="detail-val" style="color: #a855f7;">51.9% (ASML급 수익성)</span>
        </div>
      </div>
    </div>

    <div class="footer">
      <span>한미반도체 (042700) 밸류에이션 및 주주환원 핵심 요약</span>
      <span>valuestocklabs.com</span>
    </div>
  </div>
</body>
</html>
"""

async def generate_all_images():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        # 1. 썸네일 (1080x1080)
        page = await browser.new_page(viewport={"width": 1080, "height": 1080}, device_scale_factor=2)
        await page.set_content(thumbnail_html, wait_until="networkidle")
        await page.screenshot(path=str(OUTPUT_DIR / "thumbnail.png"))
        print("[완료] thumbnail.png 생성 완료")
        await page.close()

        # 2. 본문 1: 비교 표 (1080x700)
        page = await browser.new_page(viewport={"width": 1080, "height": 700}, device_scale_factor=2)
        await page.set_content(body1_html, wait_until="networkidle")
        await page.screenshot(path=str(OUTPUT_DIR / "body-1.png"))
        print("[완료] body-1.png 생성 완료")
        await page.close()

        # 3. 본문 2: 단계별 다이어그램 (1080x680)
        page = await browser.new_page(viewport={"width": 1080, "height": 680}, device_scale_factor=2)
        await page.set_content(body2_html, wait_until="networkidle")
        await page.screenshot(path=str(OUTPUT_DIR / "body-2.png"))
        print("[완료] body-2.png 생성 완료")
        await page.close()

        # 4. 본문 3: 핵심 포인트 카드 (1080x720)
        page = await browser.new_page(viewport={"width": 1080, "height": 720}, device_scale_factor=2)
        await page.set_content(body3_html, wait_until="networkidle")
        await page.screenshot(path=str(OUTPUT_DIR / "body-3.png"))
        print("[완료] body-3.png 생성 완료")
        await page.close()

        # 5. 본문 4: 인용/강조 박스 (1080x600)
        page = await browser.new_page(viewport={"width": 1080, "height": 600}, device_scale_factor=2)
        await page.set_content(body4_html, wait_until="networkidle")
        await page.screenshot(path=str(OUTPUT_DIR / "body-4.png"))
        print("[완료] body-4.png 생성 완료")
        await page.close()

        await browser.close()
        print("모든 5개 이미지 생성 완료!")

if __name__ == "__main__":
    asyncio.run(generate_all_images())
