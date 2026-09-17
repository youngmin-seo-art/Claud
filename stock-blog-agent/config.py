"""
=============================================================================
STOCK BLOG AGENT - CONFIGURATION (config.py)
=============================================================================
"""

import os
from pathlib import Path

# 기본 디렉토리 경로
AGENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = AGENT_DIR.parent
BLOG_DIR = PROJECT_ROOT / "adsense-stock-blog"
POSTS_DIR = BLOG_DIR / "posts"
INDEX_HTML = BLOG_DIR / "index.html"
SITEMAP_XML = BLOG_DIR / "sitemap.xml"
RSS_XML = BLOG_DIR / "rss.xml"
HISTORY_FILE = AGENT_DIR / "published_history.json"

# 공식 블로그 도메인 및 메타데이터 (Vercel 기본 호스트: www.valuestocklabs.com)
BLOG_DOMAIN = "https://www.valuestocklabs.com"
BLOG_TITLE = "Value Stock Labs | 저평가 가치주 & 상승초입주 리서치"
ADSENSE_PUB_ID = "ca-pub-7807868644631223"
ADSENSE_CLIENT_ID = "pub-7807868644631223"

# 실시간 금융 뉴스 RSS 피드 소스
RSS_FEEDS = [
    {
        "name": "연합뉴스 경제",
        "url": "https://www.yonhapnewstv.co.kr/browse/feed/",
        "category": "경제/증시"
    },
    {
        "name": "매일경제 증권",
        "url": "https://www.mk.co.kr/rss/30100041/",
        "category": "증시전망"
    },
    {
        "name": "매일경제 경제종합",
        "url": "https://www.mk.co.kr/rss/30000001/",
        "category": "거시경제"
    },
    {
        "name": "Google News 주식/증시",
        "url": "https://news.google.com/rss/search?q=코스피+주식+금리+실적&hl=ko&gl=KR&ceid=KR:ko",
        "category": "시장분석"
    },
    {
        "name": "Google News 테크/반도체",
        "url": "https://news.google.com/rss/search?q=반도체+AI+HBM+밸류업&hl=ko&gl=KR&ceid=KR:ko",
        "category": "AI/반도체"
    },
    {
        "name": "Google News 금융/가계대출",
        "url": "https://news.google.com/rss/search?q=대출금리+가계부채+은행+예대마진&hl=ko&gl=KR&ceid=KR:ko",
        "category": "금융/금리"
    }
]

# 고단가(High CPC) 타겟 주식/금융 키워드 풀
HIGH_CPC_KEYWORDS = [
    "저평가 가치주", "AI 반도체 HBM", "상승초입주 골든크로스", "공모주 청약 따따상",
    "월배당 ETF 고배당주", "중개형 ISA 세액공제", "기업 밸류업 프로그램", "2차전지 전고체",
    "자율주행 온디바이스AI", "로봇 액추에이터", "바이오 CDMO 신약", "미국 배당성장주 SCHD"
]

# 카테고리 매핑
CATEGORIES = {
    "undervalued": "저평가 가치주",
    "breakout": "상승초입주",
    "semiconductor": "AI 반도체",
    "ipo": "공모주 청약",
    "dividend": "배당주 투자",
    "tax": "절세·재테크"
}
