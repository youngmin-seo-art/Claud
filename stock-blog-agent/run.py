"""
=============================================================================
STOCK BLOG AGENT - MASTER CLI (run.py)
원클릭 자동 포스팅 & 실시간 주식 분석글 발행 CLI
=============================================================================
주요 특징:
  - 주말(토/일) 및 대한민국 공휴일/대체공휴일/증시 휴장일 자동 감지 및 자동 실행 스킵
  - 강제 실행이 필요한 경우 --force 옵션 지원
  - KST(한국 표준시) 타임존 완벽 지원 (로컬 PC 및 GitHub Actions 환경 호환)
=============================================================================
사용법:
  1. 자동 트렌드 분석 & 발행 (주말/공휴일 자동 스킵): python run.py --auto
  2. 아침 8시 모닝 시황 브리핑 (주말/공휴일 자동 스킵): python run.py --morning
  3. 주말/공휴일에도 강제 발행: python run.py --auto --force
  4. 특정 종목/키워드 지정: python run.py --keyword "삼성전자 HBM4 반도체"
  5. 로컬 테스트 (Git Push 제외): python run.py --auto --test
  6. 정기 시각 스케줄러: python run.py --daily-at 08:00
  7. 오늘 휴장일/공휴일 여부 확인: python run.py --check-holiday
=============================================================================
"""

import sys
import os
import re
import argparse
import time
from pathlib import Path
from datetime import datetime

# 윈도우 콘솔 UTF-8 출력 호환성 보장
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    try:
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# 스크립트 실행 경로를 sys.path에 추가하여 어디서든 실행 가능하게 설정
CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from news_collector import NewsCollector
from article_generator import ArticleGenerator
from blog_publisher import BlogPublisher
import fetch_live_market
from holiday_checker import (
    is_market_closed,
    get_korean_now,
    get_korean_today,
    get_next_business_day,
)

def run_agent(keyword=None, is_morning=False, is_test=False, force=False):
    """
    스톡 블로그 에이전트 핵심 실행 함수
    - 주말 및 공휴일(증시 휴장일) 자동 감지
    - force=True 또는 수동 keyword 지정 시 휴일에도 진행 가능
    """
    today_kst = get_korean_today()
    now_kst = get_korean_now()
    is_closed, reason = is_market_closed(today_kst)

    # 주말/공휴일 체크
    if is_closed and not force:
        if keyword:
            print("=" * 60)
            print(f"ℹ️ [휴일 안내] 오늘({today_kst}, {reason})은 주말/공휴일이지만,")
            print(f"   지정된 키워드('{keyword}') 수동 분석을 위해 포스팅을 계속 진행합니다.")
            print("=" * 60)
        else:
            print("=" * 60)
            print(f"🏖️ [휴일 알림] 오늘({today_kst}, {reason})은 주말/공휴일(증시 휴장일)입니다.")
            print("🛑 주말 및 공휴일에는 자동 포스팅을 실행하지 않고 안전하게 건너뜁니다.")
            print(f"📅 다음 증시 개장일(영업일): {get_next_business_day(today_kst)}")
            print("💡 주말/공휴일에도 강제로 실행하려면 --force 옵션을 추가하세요.")
            print("   예: python run.py --auto --force")
            print("=" * 60)
            return False
    elif is_closed and force:
        print("=" * 60)
        print(f"⚡ [--force 강제 실행] 오늘({today_kst}, {reason})은 휴일이지만 강제 실행 모드로 포스팅을 진행합니다.")
        print("=" * 60)

    print("=" * 60)
    print("🤖 [스톡 블로그 AI 에이전트] 실시간 분석 & 자동 포스팅 가동")
    print(f"🕒 실행 시각(KST): {now_kst.strftime('%Y-%m-%d %H:%M:%S')}")
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
        headlines = collector.get_morning_headlines()
        article_data = generator.generate_morning_briefing(headlines)
        print(f"📌 생성된 모닝 브리핑: {article_data['title']}")
    elif keyword:
        if collector.is_banned(keyword):
            print(f"🛑 [차단 알림] 지정된 키워드('{keyword}')는 영구 차단 목록에 포함되어 있어 발행할 수 없습니다.")
            return False
        clean_kw = re.sub(r'^(20\d\d\s*)+', '', keyword).strip()
        final_kw = clean_kw if clean_kw else keyword
        topic = {
            "title": f"2026 {final_kw} 실전 수혜주 분석 및 적정주가 밸류에이션 리포트",
            "category": "주식분석",
            "keywords": [final_kw, "저평가우량주", "상승초입", "목표주가"],
            "summary": f"{final_kw}에 대한 펀더멘털 및 기술적 차트 지표 심층 분석"
        }
        if collector.is_banned(topic["title"], topic["summary"]):
            print(f"🛑 [차단 알림] 생성된 주제('{topic['title']}')가 영구 차단 목록에 해당하여 발행을 중단합니다.")
            return False
        article_data = generator.generate_article_content(topic)
        print(f"📌 선정된 아티클 주제: {topic['title']}")
    else:
        print("🔍 [자동 모드] 금융 RSS 피드에서 최신 핫이슈 탐색 중...")
        topic = collector.collect_trending_topics()
        if collector.is_banned(topic.get("title", ""), topic.get("summary", "")):
            print(f"🛑 [차단 알림] 선정된 주제('{topic.get('title')}')가 영구 차단 목록에 해당하여 발행을 중단합니다.")
            return False
        article_data = generator.generate_article_content(topic)
        print(f"📌 선정된 아티클 주제: {topic['title']}")

    # 안전 검증: article_data 제목 및 본문 차단 키워드 2차 검증
    if collector.is_banned(article_data.get("title", ""), article_data.get("excerpt", "")):
        print(f"🛑 [차단 알림] 최종 생성물('{article_data.get('title')}')이 영구 차단 정책에 위배되어 발행을 취소합니다.")
        return False

    # 3. 블로그 자동 반영 & 배포
    print("🚀 [배포 파이프라인] adsense-stock-blog에 포스팅 등록 및 사이트맵/피드 갱신 중...")
    publisher = BlogPublisher()
    live_url = publisher.publish_post(article_data, auto_push=(not is_test))

    print("=" * 60)
    print(f"🎉 [완료] 새로운 포스팅이 성공적으로 등록되었습니다!")
    print(f"🔗 포스팅 라이브 주소: {live_url}")
    print("=" * 60)
    return True

def calculate_seconds_until(target_time_str):
    """지정된 시각(예: '08:00')까지 남은 대기 시간(초) 계산 (KST 기준)"""
    from datetime import timedelta
    now_kst = get_korean_now()
    try:
        t_hour, t_min = map(int, target_time_str.split(":"))
    except ValueError:
        raise ValueError("시간 형식은 'HH:MM'이어야 합니다. (예: 08:00)")

    target_dt = now_kst.replace(hour=t_hour, minute=t_min, second=0, microsecond=0)
    if target_dt <= now_kst:
        target_dt += timedelta(days=1)
    
    diff_sec = (target_dt - now_kst).total_seconds()
    return diff_sec, target_dt

def main():
    parser = argparse.ArgumentParser(description="Stock Blog Auto AI Agent (주말/공휴일 자동 스킵 지원)")
    parser.add_argument("--auto", action="store_true", help="최신 핫이슈 자동 수집 및 포스팅 (주말/공휴일 스킵)")
    parser.add_argument("--morning", action="store_true", help="매일 아침 8시 시황 브리핑 생성 (주말/공휴일 스킵)")
    parser.add_argument("--keyword", type=str, help="특정 종목 또는 키워드 지정 포스팅")
    parser.add_argument("--test", action="store_true", help="로컬 테스트 모드 (Git Push 제외)")
    parser.add_argument("--force", action="store_true", help="주말 및 공휴일에도 강제로 실행")
    parser.add_argument("--schedule", type=int, help="지정된 시간(분)마다 자동 반복 실행 (주말/공휴일 스킵)")
    parser.add_argument("--daily-at", type=str, help="매일 지정된 시각(HH:MM)에 자동 실행 (예: 08:00, 주말/공휴일 스킵)")
    parser.add_argument("--check-holiday", action="store_true", help="오늘이 주말/공휴일(증시 휴장일)인지 확인만 수행")

    args = parser.parse_args()

    # 휴일 확인 모드
    if args.check_holiday:
        today_kst = get_korean_today()
        is_closed, reason = is_market_closed(today_kst)
        print("=" * 60)
        print("📅 [대한민국 증시 휴장 및 공휴일 확인]")
        print(f"   현재 시각(KST): {get_korean_now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   오늘 날짜: {today_kst}")
        print(f"   상태: {'🏖️ 휴장/공휴일 (자동 실행 건너뜀)' if is_closed else '💼 정상 영업일 (자동 실행 대상)'}")
        print(f"   사유: {reason}")
        if is_closed:
            print(f"   다음 영업일: {get_next_business_day(today_kst)}")
        print("=" * 60)
        return

    if args.daily_at:
        print(f"⏰ [일일 정기 스케줄러 가동] 매일 {args.daily_at} 정각에 자동 실행합니다. (주말/공휴일은 자동 건너뜀)")
        while True:
            try:
                wait_sec, next_run_dt = calculate_seconds_until(args.daily_at)
                print(f"💤 다음 실행 예정 시각: {next_run_dt.strftime('%Y-%m-%d %H:%M:%S')} (약 {wait_sec/3600:.1f}시간 대기 중... Ctrl+C로 종료)")
                time.sleep(wait_sec)

                today_kst = get_korean_today()
                is_closed, reason = is_market_closed(today_kst)
                is_morning_mode = args.morning or (args.daily_at.startswith("08") or args.daily_at.startswith("07"))

                if is_closed and not args.force and not args.keyword:
                    print(f"\n🔔 [정각 알림] {args.daily_at} 도달했으나 오늘({today_kst}, {reason})은 주말/공휴일입니다.")
                    print(f"🏖️ 오늘의 자동 포스팅을 건너뛰고 다음 영업일({get_next_business_day(today_kst)})에 실행합니다.")
                else:
                    print(f"\n🔔 [정각 알림] {args.daily_at} 도달! 자동 분석 및 포스팅을 시작합니다.")
                    run_agent(keyword=args.keyword, is_morning=is_morning_mode, is_test=args.test, force=args.force)

                # 실행 후 10초 대기하여 중복 실행 방지
                time.sleep(10)
            except KeyboardInterrupt:
                print("\n[중단] 스케줄러가 정상적으로 종료되었습니다.")
                break
    elif args.schedule:
        print(f"⏰ [주기적 스케줄러 모드] {args.schedule}분마다 자동으로 최신 글을 수집·발행합니다. (주말/공휴일은 자동 건너뜀)")
        while True:
            try:
                run_agent(keyword=args.keyword, is_morning=args.morning, is_test=args.test, force=args.force)
                print(f"💤 {args.schedule}분 동안 대기합니다... (Ctrl+C로 중단)")
                time.sleep(args.schedule * 60)
            except KeyboardInterrupt:
                print("\n[중단] 스케줄러가 종료되었습니다.")
                break
    else:
        run_agent(keyword=args.keyword, is_morning=args.morning, is_test=args.test, force=args.force)

if __name__ == "__main__":
    main()
