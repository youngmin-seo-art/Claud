# Image Maker Agent 가이드 (Image Guide)

이 문서는 **Image Maker Agent**가 블로그 포스트의 대표 썸네일 및 본문 인포그래픽 이미지를 제작할 때 반드시 준수해야 하는 표준 가이드라인입니다.

---

## 1. 대표 이미지 (Thumbnail) 규격

블로그 메인, SNS 공유 및 구글 검색 결과에 노출되는 대표 썸네일 규격입니다.

| 항목 | 규격 및 스타일 |
|---|---|
| **해상도 및 비율** | **1080px × 1080px** (1:1 정방형) |
| **배경 스타일** | 다크 블루-퍼플 선형 그라데이션 (`linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)`) |
| **메인 텍스트** | 포스트 제목 (큰 글씨 `48~56px`, Bold, `#ffffff`, 줄바꿈 최적화) |
| **보조 텍스트** | 카테고리 태그 또는 부제 (작은 글씨 `20~24px`, `#a0aec0` / `#cbd5e1`, 뱃지 스타일 권장) |
| **텍스트 정렬** | 가로 / 세로 **완전 중앙 정렬** (`display: flex; flex-direction: column; justify-content: center; align-items: center;`) |
| **폰트 (Font)** | `Pretendard`, `-apple-system`, `BlinkMacSystemFont`, `'Malgun Gothic'`, sans-serif |
| **포인트 요소** | 부드러운 글로우(Glow) 효과, 세련된 반투명 글래스모피즘 카드 또는 포인트 보더라인 (`rgba(255, 255, 255, 0.1)`) |

---

## 2. 본문 삽입 이미지 종류 (4가지 유형)

본문 `[IMAGE:설명]` 태그의 맥락에 맞추어 아래 4가지 유형 중 가장 적합한 형식을 선택하여 제작합니다.

### 유형 1: 비교 표 (Comparison Table)
- **용도**: 두 개 이상의 개념, 지표, 제품, 투자 방법론을 항목별로 나란히 대조할 때
- **디자인 구성**:
  - 헤더 영역과 데이터 행의 명확한 시각적 대비
  - 긍정/우위 항목에는 포인트 컬러(예: 에메랄드 그린 `#10b981` 또는 블루 `#3b82f6`) 적용
  - 깔끔한 다크 테이블 레이아웃 (`#1e293b` 배경 + `#334155` 보더)

### 유형 2: 단계별 다이어그램 (Step-by-Step Diagram)
- **용도**: 3~5단계의 순서, 밸류에이션 절차, 프로세스 흐름을 순차적으로 보여줄 때
- **디자인 구성**:
  - `Step 1 ➔ Step 2 ➔ Step 3` 형태의 화살표 및 넘버링 뱃지
  - 단계별 핵심 키워드 + 1줄 요약 설명
  - 가로형 또는 지그재그형 카드 플로우 레이아웃

### 유형 3: 핵심 포인트 카드 (Key Points Grid)
- **용도**: 3~5개의 핵심 요점, 투자 원칙, 스크리닝 필터 기준을 한눈에 요약할 때
- **디자인 구성**:
  - 2열 또는 3열 그리드 카드 레이아웃
  - 각 카드 상단에 아이콘(이모지 또는 심플 SVG) + 볼드 타이틀 + 핵심 수치/설명
  - 카드 배경: 반투명 다크 글래스 스타일 (`background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(8px);`)

### 유형 4: 인용 / 강조 박스 (Quote & Callout Box)
- **용도**: 투자 대가(워런 버핏, 피터 린치 등)의 명언, 핵심 공식, 주의해야 할 단 하나의 메시지를 극적으로 강조할 때
- **디자인 구성**:
  - 대형 따옴표(`“ ”`) 또는 수식 하이라이트 박스
  - 중앙 집중형 타이포그래피 + 저자/출처 표기
  - 포인트 그라데이션 보더 (`border-left: 6px solid #6366f1;`)

---

## 3. 공통 제작 규칙 및 기술 스택

1. **HTML + CSS 렌더링 & Playwright 캡처**:
   - 모든 이미지는 독립된 **HTML/CSS 템플릿**으로 렌더링합니다.
   - Python의 `playwright` 라이브러리를 실행하여 브라우저에서 정확한 픽셀 단위로 스크린샷(`.png`)을 캡처합니다.
2. **AI / 테크 / 금융 프리미엄 톤앤매너**:
   - 다크 모드 기반의 세련된 톤 (`#0f172a`, `#1a1a2e`, `#1e293b`)
   - 눈이 편안하면서도 가독성 높은 고대비 텍스트 컬러 (`#ffffff`, `#e2e8f0`, `#94a3b8`)
   - 포인트 컬러: 인디고/바이올렛 (`#6366f1`), 사이언/블루 (`#06b6d4`, `#3b82f6`), 에메랄드 (`#10b981`)
3. **간결한 텍스트 (시각적 보조)**:
   - 텍스트 나열을 피하고, 1~2개 핵심 단어와 수치(숫자, %) 위주로 디자인합니다.
   - 독자가 3초 안에 핵심 메시지를 직관적으로 파악할 수 있어야 합니다.
4. **코드 블록 및 모노스페이스 활용**:
   - 수식, 공식, 퀀트 조건식, 코드 스타일 요소는 `JetBrains Mono`, `Fira Code`, `monospace` 폰트를 적용하고 터미널 창 스타일(상단 3개 컬러 버튼 등)을 디자인 요소로 활용할 수 있습니다.

---

## 4. Python Playwright 자동 캡처 스크립트 템플릿

```python
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

async def render_html_to_png(html_content: str, output_path: str, width: int = 1080, height: int = 1080):
    """
    HTML/CSS 코드를 Playwright로 렌더링하여 고해상도 PNG 파일로 저장합니다.
    """
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=2)
        
        await page.set_content(html_content, wait_until="networkidle")
        await page.screenshot(path=str(output_file), type="png")
        await browser.close()
        print(f"[성공] 이미지 생성 완료: {output_path}")

# 사용 예시:
# asyncio.run(render_html_to_png(html_code, "output/주제/images/thumbnail.png", 1080, 1080))
```

---

## 5. HTML/CSS 기본 템플릿 예시 (대표 썸네일)

```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 1080px;
      height: 1080px;
      background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
      font-family: 'Pretendard', sans-serif;
      display: flex;
      justify-content: center;
      align-items: center;
      color: #ffffff;
      padding: 80px;
    }
    .card {
      width: 100%;
      height: 100%;
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 32px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      text-align: center;
      padding: 60px;
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.4);
    }
    .badge {
      font-size: 22px;
      font-weight: 600;
      color: #818cf8;
      background: rgba(99, 102, 241, 0.15);
      border: 1px solid rgba(99, 102, 241, 0.3);
      padding: 10px 24px;
      border-radius: 9999px;
      margin-bottom: 36px;
      letter-spacing: 1px;
    }
    .title {
      font-size: 54px;
      font-weight: 800;
      line-height: 1.35;
      margin-bottom: 28px;
      word-break: keep-all;
      background: linear-gradient(180deg, #ffffff 0%, #cbd5e1 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .subtitle {
      font-size: 24px;
      font-weight: 400;
      color: #94a3b8;
      line-height: 1.5;
      word-break: keep-all;
    }
  </style>
</head>
<body>
  <div class="card">
    <div class="badge">주식 밸류에이션 가이드</div>
    <h1 class="title">EPS 기반 저평가주 찾는 법</h1>
    <p class="subtitle">Forward PER · PEG 공식과 4단계 실전 스크리닝</p>
  </div>
</body>
</html>
```
