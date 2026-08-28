"""
=============================================================================
STOCK BLOG AGENT - MASTER CLI (run.py)
원클릭 자동 포스팅 & 실시간 주식 분석글 발행 CLI
=============================================================================
사용법:
  1. 자동 트렌드 분석 & 발행: python run.py --auto
  2. 특정 종목/키워드 지정: python run.py --keyword "삼성전자 HBM4 반도체"
  3. 로컬 테스트 (Git Push 제외): python run.py --auto --test
=============================================================================
"""

import sys
import os
import argparse
import time

from pathlib import Path

# 스크립트 실행 경로를 sys.path에 추가하여 어디서든 실행 가능하게 설정
CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from news_collector import NewsCollector
from article_generator import ArticleGenerator
from blog_publisher import BlogPublisher
import fetch_live_market

def run_agent(keyword=None, is_morning=False, is_test=False):
    print("=" * 60)
    print("🤖 [스톡 블로그 AI 에이전트] 실시간 분석 & 자동 포스팅 가동")
    print("=" * 60)

    # 0. 최신 실시간 증시 데이터 자동 갱신 (Yahoo Finance, Upbit, FX)
    try:
        fetch_live_market.main()
    except Exception as e:
        print(f"⚠️ [실시간 시세 갱신 건너뜀]: {e}")

    collector = NewsCollector()
    generator = ArticleGenerator()

    if is_morning:
        print("☕ [모닝 시황 모드] 밤사이 뉴욕증시 & 국내 아침 경제 이슈 수집 중...")
        # 5개 최신 헤드라인 수집
        items = collector.fetch_feed("https://www.yonhapnewstv.co.kr/browse/feed/")
        headlines = [it["title"] for it in items[:5]] if items else None
        article_data = generator.generate_morning_briefing(headlines)
        print(f"📌 생성된 모닝 브리핑: {article_data['title']}")
    elif keyword:
        print(f"🎯 [키워드 지정 모드] 타겟 키워드: {keyword}")
        topic = {
            "title": f"2026 {keyword} 실전 수혜주 분석 및 적정주가 밸류에이션 리포트",
            "category": "주식분석",
            "keywords": [keyword, "저평가우량주", "상승초입", "목표주가"],
            "summary": f"{keyword}에 대한 펀더멘털 및 기술적 차트 지표 심층 분석"
        }
        article_data = generator.generate_article_content(topic)
        print(f"📌 선정된 아티클 주제: {topic['title']}")
    else:
        print("🔍 [자동 모드] 금융 RSS 피드에서 최신 핫이슈 탐색 중...")
        topic = collector.collect_trending_topics()
        article_data = generator.generate_article_content(topic)
        print(f"📌 선정된 아티클 주제: {topic['title']}")

    # 3. 블로그 자동 반영 & 배포
    print("🚀 [배포 파이프라인] adsense-stock-blog에 포스팅 등록 및 사이트맵/피드 갱신 중...")
    publisher = BlogPublisher()
    live_url = publisher.publish_post(article_data, auto_push=(not is_test))

    print("=" * 60)
    print(f"🎉 [완료] 새로운 포스팅이 성공적으로 등록되었습니다!")
    print(f"🔗 포스팅 라이브 주소: {live_url}")
    print("=" * 60)

def main():
    parser = argparse.ArgumentParser(description="Stock Blog Auto AI Agent")
    parser.add_argument("--auto", action="store_true", help="최신 핫이슈 자동 수집 및 포스팅")
    parser.add_argument("--morning", action="store_true", help="매일 아침 8시 시황 브리핑 생성")
    parser.add_argument("--keyword", type=str, help="특정 종목 또는 키워드 지정 포스팅")
    parser.add_argument("--test", action="store_true", help="로컬 테스트 모드 (Git Push 제외)")
    parser.add_argument("--schedule", type=int, help="지정된 시간(분)마다 자동 반복 실행")

    args = parser.parse_args()

    if args.schedule:
        print(f"⏰ [스케줄러 모드] {args.schedule}분마다 자동으로 최신 글을 수집·발행합니다.")
        while True:
            try:
                run_agent(keyword=args.keyword, is_morning=args.morning, is_test=args.test)
                print(f"💤 {args.schedule}분 동안 대기합니다... (Ctrl+C로 중단)")
                time.sleep(args.schedule * 60)
            except KeyboardInterrupt:
                print("\n[중단] 스케줄러가 종료되었습니다.")
                break
    else:
        run_agent(keyword=args.keyword, is_morning=args.morning, is_test=args.test)

if __name__ == "__main__":
    main()
