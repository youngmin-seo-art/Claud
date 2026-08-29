"""
=============================================================================
NEWS COLLECTOR (news_collector.py)
실시간 경제 뉴스 및 주식 시장 트렌드 수집기 & 중복 방지 시스템
=============================================================================
"""

import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import html
import re
import random
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from config import RSS_FEEDS, HIGH_CPC_KEYWORDS, POSTS_DIR, HISTORY_FILE

class NewsCollector:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        }
        self.published_titles = self.load_published_history()

    def clean_text(self, text):
        """텍스트 정제 및 특수문자 제거"""
        if not text:
            return ""
        unescaped = html.unescape(text)
        cleaned = re.sub(r'<[^>]+>', '', unescaped)
        cleaned = re.sub(r'[\r\n\t]+', ' ', cleaned)
        return cleaned.strip()

    def normalize_title(self, title):
        """제목 비교를 위한 정규화 (특수문자 및 공백 제거)"""
        return re.sub(r'[\W_]+', '', title.lower())

    def load_published_history(self):
        """기존 발행된 글 목록(히스토리 파일 + posts 디렉토리) 로드"""
        published = set()

        # 1. published_history.json 파일에서 로드
        if HISTORY_FILE.exists():
            try:
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    history = json.load(f)
                    for item in history:
                        if isinstance(item, dict):
                            t = item.get("title", "")
                            if t:
                                published.add(self.normalize_title(t))
                        elif isinstance(item, str):
                            published.add(self.normalize_title(item))
            except Exception as e:
                print(f"[알림] 발행 히스토리 파일 읽기 실패: {e}")

        # 2. posts 디렉토리 내 html 파일 제목/파일명 스캔
        if POSTS_DIR.exists():
            for p in POSTS_DIR.glob("*.html"):
                try:
                    # 파일명에서 날짜 뒷부분 키워드 추출
                    name_part = p.stem
                    published.add(self.normalize_title(name_part))
                    
                    # HTML 내부 title 태그 추출
                    with open(p, "r", encoding="utf-8", errors="ignore") as f:
                        html_text = f.read(2048)
                        match = re.search(r'<title>(.*?)</title>', html_text, re.IGNORECASE)
                        if match:
                            raw_t = match.group(1).split("|")[0].strip()
                            published.add(self.normalize_title(raw_t))
                except Exception:
                    pass

        return published

    def is_already_published(self, title):
        """이미 발행된 기사인지 검사 (정확 일치 및 높은 유사도)"""
        norm = self.normalize_title(title)
        if not norm:
            return True

        if norm in self.published_titles:
            return True

        # 단어 교집합 비율 검사 (핵심 단어가 60% 이상 겹치면 중복으로 판단)
        words = set(w for w in re.findall(r'[가-힣a-zA-Z0-9]{2,}', title))
        if not words:
            return False

        for pub in self.published_titles:
            pub_words = set(w for w in re.findall(r'[가-힣a-zA-Z0-9]{2,}', pub))
            if pub_words:
                overlap = words.intersection(pub_words)
                if len(overlap) >= 3 and len(overlap) / min(len(words), len(pub_words)) > 0.6:
                    return True

        return False

    def fetch_feed(self, feed_url):
        """RSS 피드 URL에서 최신 뉴스 파싱"""
        news_items = []
        try:
            parsed = urllib.parse.urlsplit(feed_url)
            encoded_query = urllib.parse.quote(parsed.query, safe="=&?+")
            encoded_url = urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, parsed.path, encoded_query, parsed.fragment))
            
            req = urllib.request.Request(encoded_url, headers=self.headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                xml_data = response.read()
                root = ET.fromstring(xml_data)
                
                for item in root.findall(".//item"):
                    title_elem = item.find("title")
                    link_elem = item.find("link")
                    desc_elem = item.find("description")
                    pub_date_elem = item.find("pubDate")
                    
                    t_text = self.clean_text(title_elem.text if title_elem is not None and title_elem.text else "")
                    d_text = self.clean_text(desc_elem.text if desc_elem is not None and desc_elem.text else "")
                    link_text = link_elem.text.strip() if link_elem is not None and link_elem.text else ""
                    pub_date_text = pub_date_elem.text.strip() if pub_date_elem is not None and pub_date_elem.text else ""
                    
                    if t_text:
                        news_items.append({
                            "title": t_text,
                            "link": link_text,
                            "description": d_text,
                            "pubDate": pub_date_text
                        })
        except Exception as e:
            print(f"[알림] RSS 피드 수집 건너뜀 ({feed_url[:35]}...): {e}")
        
        return news_items

    def classify_category_and_keywords(self, title, description):
        """제목 및 본문 요약을 바탕으로 정확한 금융 카테고리와 타겟 키워드 자동 분류"""
        full_text = f"{title} {description}"

        if any(w in full_text for w in ["반도체", "HBM", "엔비디아", "하이닉스", "삼성전자", "파운드리", "CXL", "온디바이스", "소부장", "빅테크", "AI투자"]):
            return "AI 반도체", ["AI 반도체 HBM", "SK하이닉스", "엔비디아 밸류체인", "소부장 대장주", "빅테크 AI CAPEX"]
        elif any(w in full_text for w in ["밸류업", "저PBR", "배당", "주주환원", "자사주", "금융지주", "은행주", "보험주", "지주사"]):
            return "저평가 가치주", ["기업 밸류업 프로그램", "저PBR 우량주", "고배당 금융지주", "주주환원율", "자사주 소각"]
        elif any(w in full_text for w in ["대출", "가계부채", "예대마진", "가산금리", "주담대", "신용대출", "월급쟁이"]):
            return "거시경제/금리", ["기준금리 동향", "대출금리 인상", "가계부채 현황", "예대금리차", "금융당국 규제"]
        elif any(w in full_text for w in ["금리", "환율", "외환", "인플레이션", "국채", "한은", "한국은행", "기준금리", "통화정책"]):
            return "거시경제/금리", ["기준금리 동향", "환율 변동성", "글로벌 매크로", "인플레이션 추이", "국채금리"]
        elif any(w in full_text for w in ["반등", "상승초입", "골든크로스", "돌파", "신고가", "수급", "증시반등"]):
            return "상승초입주", ["상승초입주", "골든크로스", "증시 반등 조건", "외국인 순매수", "주도 섹터"]
        elif any(w in full_text for w in ["2차전지", "배터리", "전고체", "양극재", "에코프로", "포스코", "전기차", "로봇", "휴머노이드"]):
            return "모빌리티/신기술", ["2차전지 전고체", "양극재 밸류체인", "로보틱스 액추에이터", "피지컬 AI", "휴머노이드"]
        elif any(w in full_text for w in ["바이오", "제약", "임상", "FDA", "CDMO", "신약", "기술수출", "헬스케어", "비만치료제"]):
            return "바이오/제약", ["바이오 CDMO 신약", "FDA 임상 3상", "기술수출(L/O)", "비만치료제 GLP-1", "헬스케어"]
        elif any(w in full_text for w in ["공모주", "청약", "IPO", "상장", "의무보유", "수요예측", "따따상"]):
            return "공모주 청약", ["공모주 청약 일정", "수요예측 경쟁률", "의무보유 확약비율", "상장 첫날 유통물량", "적정 공모가"]
        elif any(w in full_text for w in ["유가", "원자재", "방산", "중동", "지정학", "해운", "조선", "방위산업"]):
            return "원자재/지정학", ["국제유가 WTI", "지정학적 리스크", "방산 수주 모멘텀", "해운 운임지수", "조선업 슈퍼사이클"]
        else:
            return "주식분석", random.sample(HIGH_CPC_KEYWORDS, 4)

    def get_fallback_topic(self):
        """피드 수집이 어렵거나 전체 중복 시 날짜(일자)별 고유한 테마 캘린더에서 매일 새로운 주제 선택"""
        day_of_year = datetime.now().timetuple().tm_yday
        today_date = datetime.now().strftime("%Y년 %m월 %d일")

        fallback_pool = [
            {
                "title": f"[{today_date}] 한은 기준금리 인하 가시화… 예대금리차 확대와 시중은행 가계대출 금리 인상 파장",
                "category": "거시경제/금리",
                "keywords": ["대출금리", "기준금리", "가계부채", "예대금리차", "금융주"],
                "summary": "한국은행의 통화정책 전환 기대감 속에 은행권의 가산금리 인상 조치로 가계와 기업 간 대출금리 양극화가 심화되고 있는 경제적 배경과 금융시장 파급 효과 분석."
            },
            {
                "title": f"[{today_date}] 차세대 AI 반도체 HBM4 및 CXL 2.0 상용화 로드맵과 글로벌 소부장 톱픽",
                "category": "AI 반도체",
                "keywords": ["AI 반도체", "HBM4", "CXL 메모리", "SK하이닉스", "소부장"],
                "summary": "엔비디아 블랙웰 아키텍처 양산 본격화에 따른 HBM 공급 부족 지속 및 CXL 기반 차세대 서버 메모리 생태계 수혜주 밸류에이션 리포트."
            },
            {
                "title": f"[{today_date}] 밸류업 2차 세제 혜택 확정… PBR 0.8배 미만 고배당 금융·지주사 외국인 순매수 집중",
                "category": "저평가 가치주",
                "keywords": ["기업 밸류업", "저PBR", "배당소득 분리과세", "자사주 소각", "금융지주"],
                "summary": "정부의 주주환원 세제 개편안과 자사주 소각 인센티브 도입에 따른 저평가 가치주 멀티플 리레이팅 및 외국인 자금 유입 분석."
            },
            {
                "title": f"[{today_date}] 바닥권 거래량 500% 폭증… 장기 박스권 돌파 상승초입 주도 섹터 퀀트 스크리닝",
                "category": "상승초입주",
                "keywords": ["상승초입주", "골든크로스", "거래량 급증", "이평선 수렴", "기술적 분석"],
                "summary": "기관 및 외국인 동시 순매수와 60일·120일 이동평균선 골든크로스가 발생한 바닥권 탈출 유망 종목군 기술적 차트 분석."
            },
            {
                "title": f"[{today_date}] 월 100만원 배당 파이프라인 완성: 미국 SCHD & 국내 월배당 커버드콜 ETF 포트폴리오",
                "category": "배당주 투자",
                "keywords": ["월배당 ETF", "SCHD", "커버드콜", "배당성장주", "은퇴 현금흐름"],
                "summary": "인플레이션 헷지와 안정적인 월 현금흐름을 동시에 달성하는 고배당 ETF 자산배분 및 절세 계좌(ISA/IRP) 실전 운용 전략."
            },
            {
                "title": f"[{today_date}] AI 데이터센터 전력 소비 폭증… 초고압 변압기·전선·전력기기 슈퍼사이클 수주 점검",
                "category": "시장분석",
                "keywords": ["전력망", "초고압 변압기", "AI 데이터센터", "전선주", "수주 잔고"],
                "summary": "빅테크 기업들의 AI 데이터센터 전력망 증설 경쟁으로 인한 북미 변압기 쇼티지 및 국내 전력 인프라 대장주 실적 모멘텀 분석."
            },
            {
                "title": f"[{today_date}] 2026 하반기 대어급 IPO 공모주 청약 캘린더 및 기관 수요예측 배정 극대화 전략",
                "category": "공모주 청약",
                "keywords": ["공모주 청약", "IPO 일정", "수요예측", "의무보유 확약", "균등배정"],
                "summary": "하반기 조 단위 대형 신규 상장 기업들의 공모가 산정 적정성 평가와 청약 증거금 대비 기대 수익률 시뮬레이션."
            },
            {
                "title": f"[{today_date}] 2차전지 전고체 배터리 파일럿 라인 가동… 양극재·음극재 기술 혁신과 리레이팅 전망",
                "category": "모빌리티/신기술",
                "keywords": ["2차전지", "전고체 배터리", "황화물계", "양극재", "소재 혁신"],
                "summary": "차세대 꿈의 배터리로 불리는 전고체 배터리 양산 일정 가시화와 소재 공급망 선점 기업들의 중장기 성장성 분석."
            },
            {
                "title": f"[{today_date}] 글로벌 K-바이오 빅파마 기술수출(L/O) 릴레이… FDA 임상 3상 승인 기대주 총정리",
                "category": "바이오/제약",
                "keywords": ["바이오 신약", "기술수출", "FDA 승인", "비만치료제", "ADC 항암제"],
                "summary": "차세대 ADC(항체-약물 접합체) 및 비만치료제 파이프라인을 보유한 국내 대표 바이오텍의 마일스톤 유입 및 임상 데이터 분석."
            },
            {
                "title": f"[{today_date}] 중개형 ISA & IRP 만기 비과세 절세 극대화 전략 및 해외 ETF 환차익 노하우",
                "category": "절세·재테크",
                "keywords": ["중개형 ISA", "IRP", "연금저축", "비과세 한도", "절세 꿀팁"],
                "summary": "금융소득종합과세를 피하고 비과세 및 분리과세 혜택을 100% 활용하는 2026 개정 세법 맞춤형 자산 관리 가이드."
            }
        ]

        # 날짜 기반으로 순환 선택
        selected = fallback_pool[day_of_year % len(fallback_pool)]
        return {
            "title": selected["title"],
            "category": selected["category"],
            "keywords": selected["keywords"],
            "summary": selected["summary"],
            "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "source_name": "Value Stock Labs 리서치센터",
            "link": ""
        }

    def collect_trending_topics(self):
        """여러 금융 RSS 소스에서 '중복되지 않은 가장 신선한 최신 뉴스' 선별 수집"""
        all_news = []
        for feed in RSS_FEEDS:
            items = self.fetch_feed(feed["url"])
            for item in items:
                item["source_name"] = feed["name"]
                item["feed_category"] = feed["category"]
                all_news.append(item)

        print(f"[정보] 총 {len(all_news)}건의 실시간 뉴스 아이템 수집 완료. 중복 및 기발행 여부 검사 중...")

        # 1. 이미 발행된 기사 필터링
        fresh_news = []
        for item in all_news:
            title = item["title"]
            if not self.is_already_published(title):
                fresh_news.append(item)
            else:
                # print(f"  - [중복 제외]: {title[:30]}...")
                pass

        print(f"[정보] 기발행 제외 후 신규 뉴스 후보: {len(fresh_news)}건")

        if not fresh_news:
            print("⚠️ [알림] 새로운 RSS 기사가 모두 기발행되었거나 없어 날짜별 고유 테마 캘린더에서 선별합니다.")
            return self.get_fallback_topic()

        # 2. 고단가/핵심 금융 키워드 우선순위 평가
        def score_news(item):
            score = 0
            t = item["title"]
            d = item.get("description", "")
            full = f"{t} {d}"

            # 핵심 금융 키워드 가중치
            for kw in HIGH_CPC_KEYWORDS:
                if any(w in t for w in kw.split()):
                    score += 15
                elif any(w in d for w in kw.split()):
                    score += 5

            # 중요 경제 이슈 단어
            for imp in ["금리", "환율", "대출", "증시", "실적", "수주", "반도체", "배당", "밸류업", "외국인", "기관", "신고가", "돌파"]:
                if imp in t:
                    score += 8

            # 단순 사건사고나 연예/가십 제외
            for bad in ["포토", "인사", "부고", "동정", "날씨", "사고", "화재", "살인", "폭행", "음주"]:
                if bad in t:
                    score -= 50

            return score

        # 점수 높은 순으로 정렬
        fresh_news.sort(key=score_news, reverse=True)
        best_item = fresh_news[0]

        category, keywords = self.classify_category_and_keywords(best_item["title"], best_item.get("description", ""))

        summary = best_item.get("description", "")
        if not summary or len(summary) < 20:
            summary = f"{best_item['title']} 관련 시장 핵심 모멘텀 및 펀더멘털 지표(PER/PBR/ROE) 정밀 리서치 보고서"

        return {
            "title": best_item["title"],
            "category": category,
            "keywords": keywords,
            "summary": summary,
            "source_name": best_item.get("source_name", "실시간 뉴스"),
            "link": best_item.get("link", ""),
            "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

if __name__ == "__main__":
    collector = NewsCollector()
    topic = collector.collect_trending_topics()
    print("\n=== [수집된 최신 핫이슈 결과] ===")
    print(f"📌 제목: {topic['title']}")
    print(f"📂 카테고리: {topic['category']}")
    print(f"🏷️ 키워드: {', '.join(topic['keywords'])}")
    print(f"📝 요약: {topic['summary']}")
