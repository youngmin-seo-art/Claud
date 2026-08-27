# 🤖 스톡 블로그 자동 업데이트 AI Agent (`stock-blog-agent`)

컴퓨터 앞에서 일일이 글을 쓰지 않아도, **실시간 금융 뉴스와 주식 핫이슈를 자동 수집하여 2,000자 이상의 고품질 SEO 리서치 아티클을 생성하고 `valuestocklabs.com`에 실시간으로 배포**하는 무인 자동화 에이전트입니다.

---

## 🌟 주요 기능

1. **실시간 경제 뉴스 및 핫이슈 자동 수집 (`news_collector.py`)**:
   - 네이버 금융, 연합뉴스, 한국경제 등에서 실적/수주/반도체/공모주/밸류업 관련 고단가 키워드 이슈 자동 선별.
2. **2,000자 이상 고품질 SEO 분석글 자동 작성 (`article_generator.py`)**:
   - 정량 재무 지표 분석표(PER, PBR, ROE), 기술적 골든크로스 차트 분석, 투자 리스크 체크포인트 자동 생성.
   - **본문 상단 리더보드 + 본문 중간 인피드 광고 슬롯 2개 자동 삽입**.
   - 실시간 인터랙티브 목차(TOC) 및 물타기/적정주가 계산기 위젯 연계.
3. **사이트 맵/피드 동기화 & 실시간 자동 배포 (`blog_publisher.py`)**:
   - `adsense-stock-blog/posts/`에 신규 `.html` 생성.
   - `index.html`, `sitemap.xml`, `rss.xml` 자동 업데이트.
   - Git Commit & Push 자동 실행 ➔ **[https://valuestocklabs.com](https://valuestocklabs.com)**에 실시간 라이브 반영!

---

## 🚀 사용 방법

`stock-blog-agent` 폴더에서 아래 명령어 중 원하는 모드를 실행하시면 됩니다:

### 1. 🔍 최신 핫이슈 자동 감지 포스팅 (가장 추천!)
```bash
python run.py --auto
```
- 금융 뉴스를 실시간으로 읽고 가장 핫한 주제 1건을 자동으로 작성하여 즉시 배포합니다.

### 2. 🎯 특정 종목/키워드 지정 포스팅
```bash
python run.py --keyword "삼성전자 2nm 파운드리"
python run.py --keyword "현대차 로보틱스 자율주행"
python run.py --keyword "월배당 커버드콜 ETF"
```
- 본인이 원하는 종목이나 테마를 입력하면 해당 주제에 맞춘 전문 분석 리포트가 1초 만에 생성되어 발행됩니다.

### 3. 🧪 로컬 테스트 모드 (Git 배포 없이 로컬 미리보기)
```bash
python run.py --auto --test
```

### 4. ⏰ 무인 스케줄러 반복 실행 (예: 6시간마다 1편씩 자동 발행)
```bash
python run.py --auto --schedule 360
```
- 360분(6시간)마다 자동으로 최신 뉴스를 가져와 하루 4편씩 블로그를 자동으로 키워줍니다.
