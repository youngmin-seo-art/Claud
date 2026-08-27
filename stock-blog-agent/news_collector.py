"""
=============================================================================
NEWS COLLECTOR (news_collector.py)
실시간 경제 뉴스 및 주식 시장 트렌드 수집기 (Zero External Dependencies)
=============================================================================
"""

import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import html
import re
import random
import sys
from datetime import datetime

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from config import RSS_FEEDS, HIGH_CPC_KEYWORDS

class NewsCollector:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        }

    def fetch_feed(self, feed_url):
        """RSS 피드 URL에서 최신 뉴스 파싱"""
        news_items = []
        try:
            # URL 내 한글 쿼리 인코딩
            parsed = urllib.parse.urlsplit(feed_url)
            encoded_query = urllib.parse.quote(parsed.query, safe="=&?+")
            encoded_url = urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, parsed.path, encoded_query, parsed.fragment))
            
            req = urllib.request.Request(encoded_url, headers=self.headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                xml_data = response.read()
                root = ET.fromstring(xml_data)
                
                # RSS 2.0 items 파싱
                for item in root.findall(".//item"):
                    title = item.find("title")
                    link = item.find("link")
                    desc = item.find("description")
                    pubDate = item.find("pubDate")
                    
                    t_text = html.unescape(title.text) if title is not None and title.text else ""
                    d_text = html.unescape(desc.text) if desc is not None and desc.text else ""
                    # HTML 태그 제거
                    clean_desc = re.sub(r'<[^>]+>', '', d_text).strip()
                    
                    if t_text:
                        news_items.append({
                            "title": t_text.strip(),
                            "link": link.text if link is not None and link.text else "",
                            "description": clean_desc[:200],
                            "pubDate": pubDate.text if pubDate is not None and pubDate.text else ""
                        })
        except Exception as e:
            print(f"[알림] RSS 피드 수집 건너뜀 ({feed_url[:30]}...): {e}")
        
        return news_items

    def collect_trending_topics(self):
        """여러 금융 RSS 소스에서 최신 주식/경제 핫이슈 수집"""
        all_news = []
        for feed in RSS_FEEDS:
            items = self.fetch_feed(feed["url"])
            for item in items:
                item["source_name"] = feed["name"]
                item["category"] = feed["category"]
                all_news.append(item)

        # 수집된 뉴스가 없을 경우 기본 고단가 주식 테마 풀에서 생성
        if not all_news:
            fallback_titles = [
                {"title": "2026 차세대 AI 반도체 CXL 및 온디바이스 수혜주 분석", "category": "AI 반도체"},
                {"title": "밸류업 지수 편입 저평가 PBR 1배 미만 금융·지주사 톱픽", "category": "저평가 가치주"},
                {"title": "상승초입 거래량 500% 급증 바닥권 박스권 돌파 유망주", "category": "상승초입주"},
                {"title": "월 100만원 배당 파이프라인 완성하는 미국/국내 고배당 ETF 전략", "category": "배당주 투자"},
                {"title": "2026 하반기 대어급 IPO 공모주 일정 및 청약 배정 극대화 전략", "category": "공모주 청약"}
            ]
            selected = random.choice(fallback_titles)
            return {
                "title": selected["title"],
                "category": selected["category"],
                "keywords": random.sample(HIGH_CPC_KEYWORDS, 4),
                "summary": "시장 핵심 모멘텀 및 펀더멘털 지표(PER/PBR/ROE) 정밀 리서치 보고서",
                "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

        # 고단가 키워드가 포함된 가장 가치 있는 뉴스 1건 선별
        for news in all_news:
            for kw in HIGH_CPC_KEYWORDS:
                if any(w in news["title"] for w in kw.split()):
                    return {
                        "title": news["title"],
                        "category": news.get("category", "주식분석"),
                        "keywords": random.sample(HIGH_CPC_KEYWORDS, 4),
                        "summary": news.get("description", "최신 금융 이슈 기반 밸류에이션 리서치"),
                        "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }

        # 기본 1번째 뉴스 반환
        first = all_news[0]
        return {
            "title": first["title"],
            "category": first.get("category", "주식분석"),
            "keywords": random.sample(HIGH_CPC_KEYWORDS, 4),
            "summary": first.get("description", "최신 경제 동향 심층 분석"),
            "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

if __name__ == "__main__":
    collector = NewsCollector()
    topic = collector.collect_trending_topics()
    print("=== 수집된 최신 핫이슈 ===")
    print(f"제목: {topic['title']}")
    print(f"카테고리: {topic['category']}")
    print(f"키워드: {', '.join(topic['keywords'])}")
