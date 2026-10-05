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

from config import (
    RSS_FEEDS,
    HIGH_CPC_KEYWORDS,
    POSTS_DIR,
    HISTORY_FILE,
    BANNED_TOPIC_KEYWORDS,
    BANNED_TITLES,
    BANNED_TOPICS_FILE
)

class NewsCollector:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        }
        self.banned_titles = self.load_banned_topics()
        self.published_titles = self.load_published_history()

    def clean_text(self, text):
        """텍스트 정제 및 특수문자 제거"""
        if not text:
            return ""
        unescaped = html.unescape(text)
        cleaned = re.sub(r'<[^>]+>', '', unescaped)
        cleaned = re.sub(r'[\r\n\t]+', ' ', cleaned)
        cleaned = cleaned.replace("중둥", "중동")
        return cleaned.strip()

    def clean_title(self, raw_title):
        """뉴스 헤드라인 정제: 언론사명 접미사, 도메인, 날짜 태그, 창간/기획/코너 브래킷, 중복 연도, 불필요한 기호 100% 완전 제거"""
        if not raw_title:
            return ""
        title = self.clean_text(raw_title)
        
        # 1. 언론사 접미사 및 도메인 제거 (반복 정제)
        # 구글 뉴스 및 포털 RSS는 주로 " - 언론사명" 또는 " | 언론사명" 형태를 가짐
        known_media = (
            r'머니투데이|MBC\s*뉴스|MBC|네이버\s*프리미엄콘텐츠|네이버뉴스|네이버|다음뉴스|다음|매일경제|한국경제|연합뉴스|연합뉴스TV|연합인포맥스|'
            r'조선일보|중앙일보|동아일보|서울경제|이데일리|아시아경제|아시아타임즈|아시아타임스|헤럴드경제|코리아헤럴드|코리아타임스|'
            r'뉴시스|뉴스1|SBS|KBS|YTN|JTBC|MBN|TV조선|채널A|파이낸셜뉴스|파이낸셜포스트|디지털타임스|전자신문|스마트비즈|블로터|'
            r'더벨|인포스탁데일리|한경닷컴|매경닷컴|머니S|이투데이|더페어|더팩트|조세일보|글로벌이코노믹|뉴스웨이|싱크풀|딜사이트|프라임경제|'
            r'비즈워치|한국금융신문|아이뉴스24|매경이코노미|한경비즈니스|이코노미스트|뉴스토마토|이코노믹리뷰|인더뉴스|브릿지경제|'
            r'비즈니스포스트|팍스넷뉴스|팍스경제TV|뉴스워커|뉴스트리|스트레이트뉴스|전국매일신문|중소기업신문|테크엠|인공지능신문|'
            r'로봇신문|에너지경제|전기신문|가스신문|의학신문|약업신문|청년의사|헬스조선|메디코파마뉴스|팜뉴스|히트뉴스|데일리메디|'
            r'데일리팜|바이오스펙테이터|K스피릿|인사이트|위키트리|오마이뉴스|프레시안|노컷뉴스|미디어오늘|지디넷코리아|ZDNet|'
            r'디지털데일리|매일일보|내외뉴스통신|공감신문|NSP통신|NBN미디어|KCN뉴스|아주뉴스|아주데일리|아주경제|글로벌뉴스|'
            r'중앙이코노미스트|이코노미조선|리더스팩트|리드경제|데일리안|4th|MTN|leadeconomy|smartbizn|leadersfact|thefairnews'
        )
        
        media_endings = (
            r'뉴스|일보|신문|타임스|타임즈|경제|저널|통신|데일리|포스트|투데이|미디어|인사이드|닷컴|비즈|'
            r'프레스|매거진|리더스|리포트|TV|방송|헤럴드|넷|플러스|코리아|인포|파이낸스|앤|이코노미|'
            r'팍스|벨|팩트|스탁|라이프|리뷰|테크|나우|뷰|보이스|위크|픽|머니|스피릿|인포맥스|스펙테이터'
        )

        for _ in range(5):
            # 도메인 제거 (e.g., " - news.mtn.co.kr", " - leadeconomy.com", " - 4th.kr")
            title = re.sub(r'[-\s|·~–—:]+[a-zA-Z0-9.-]+\.(?:co\.kr|com|kr|net|org|news|biz|io|cc|me|tv|asia|ai|xyz)\b.*$', '', title, flags=re.IGNORECASE).strip()
            # 알려진 언론사명 제거
            title = re.sub(rf'[-\s|·~–—:]+(?:{known_media})\b.*$', '', title, flags=re.IGNORECASE).strip()
            # 일반 언론사 접미사 패턴 제거
            title = re.sub(rf'[-\s|·~–—:]+[가-힣A-Za-z0-9\s]{{1,15}}(?:{media_endings})\s*$', '', title, flags=re.IGNORECASE).strip()

        # 2. 날짜, 언론사 코너/기획/창간/특집 및 잡음 태그 제거 (e.g. "[창간 10주년 밸류업 2.0]", "[더페어 전망대]", "[4월 27일]", "[속보]", "[단독]" 등)
        title = re.sub(r'^\[\s*[^\]]*(?:창간|주년|기획|특집|스페셜|시리즈|서막|진단|해설|논평|취재|심층|포커스|분석|전망대|전망|현장|현장에서|레이더|탐방|인사이트|브리핑|체크|이슈|단독|속보|특징주|마감|개장|장마감|국장|뉴욕|글로벌|월가|종합|포토|인사|부고|알림|표|공시|더페어|더벨|리서치센터장|기자수첩|CEO|칼럼|기고|밸류업|마켓|증시)\s*\]\s*', '', title, flags=re.IGNORECASE)
        title = re.sub(r'\[\s*[^\]]*(?:창간|서막|진단|해설|논평|취재|심층|포커스|전망대|더페어|더벨|리서치센터장|기자수첩|칼럼|기고|특집|기획)\s*\]', '', title, flags=re.IGNORECASE)
        title = re.sub(r'^\(\s*(?:국장\s*마감|코스피\s*마감|뉴욕\s*마감|장마감|속보|단독|종합|마감|개장)\s*\)\s*', '', title, flags=re.IGNORECASE)
        title = re.sub(r'\[\s*(?:속보|단독|특징주|종합|1보|2보|3보|상보|인터뷰|포토|인사|부고|알림|공시)\s*\]', '', title, flags=re.IGNORECASE)
        title = re.sub(r'^\[\s*\d+월\s*\d+일\s*\]\s*', '', title)
        title = re.sub(r'[①②③④⑤⑥⑦⑧⑨⑩]', '', title)

        # 3. 중복 연도 정제 (e.g., "2026 2026 ...")
        title = re.sub(r'\b(20\d\d)\s+\1\b', r'\1', title)
        title = re.sub(r'^(20\d\d\s+){2,}', r'\1', title)

        # 4. 언론사 원문 오타 자동 교정 및 특수기호 정리
        typo_map = {
            "중둥": "중동",
            "“": "\"",
            "”": "\"",
            "‘": "'",
            "’": "'",
            "…": "...",
        }
        for typo, correct in typo_map.items():
            title = title.replace(typo, correct)

        # 앞뒤 불필요한 기호 제거
        title = re.sub(r'^[-–—\s:·|]+|[-–—\s:·|]+$', '', title).strip()
        title = re.sub(r'\s+', ' ', title).strip()

        return title

    def normalize_title(self, title):
        """제목 비교를 위한 정규화 (특수문자 및 공백 제거)"""
        return re.sub(r'[\W_]+', '', title.lower())

    def load_banned_topics(self):
        """영구 차단된 주제 및 키워드 목록 로드 (재발행 절대 금지)"""
        banned = set()
        for t in BANNED_TITLES:
            banned.add(self.normalize_title(t))
        
        if BANNED_TOPICS_FILE.exists():
            try:
                with open(BANNED_TOPICS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for item in data:
                        if isinstance(item, dict):
                            t = item.get("title", "")
                            if t:
                                banned.add(self.normalize_title(t))
                            for kw in item.get("banned_keywords", []):
                                BANNED_TOPIC_KEYWORDS.append(kw)
                        elif isinstance(item, str):
                            banned.add(self.normalize_title(item))
            except Exception as e:
                print(f"[알림] 차단 목록 파일 읽기 실패: {e}")
        return banned

    def is_banned(self, title, description=""):
        """영구 차단 키워드 또는 차단 제목 패턴에 해당하는지 검사 (절대 재발행 불가)"""
        if not title:
            return True
        full_text = f"{title} {description}".lower()
        
        # 1. 차단 키워드 검사 (e.g. 5850, 5850선 등)
        for kw in BANNED_TOPIC_KEYWORDS:
            if kw.lower() in full_text:
                return True
        
        # 2. 정규화된 차단 제목 목록 검사
        norm = self.normalize_title(title)
        if norm in self.banned_titles:
            return True
        for b in self.banned_titles:
            if b and (b in norm or norm in b):
                return True
        return False

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
        """이미 발행된 기사인지 또는 영구 차단된 기사인지 검사"""
        if self.is_banned(title):
            return True

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
                    
                    raw_t = title_elem.text if title_elem is not None and title_elem.text else ""
                    t_text = self.clean_title(raw_t)
                    d_text = self.clean_text(desc_elem.text if desc_elem is not None and desc_elem.text else "")
                    link_text = link_elem.text.strip() if link_elem is not None and link_elem.text else ""
                    pub_date_text = pub_date_elem.text.strip() if pub_date_elem is not None and pub_date_elem.text else ""
                    
                    if t_text and len(t_text) >= 5:
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

    def rewrite_summary(self, title, category, keywords, raw_description=""):
        """원문 기사의 단순 복사를 배제하고 100% 저작권 안전하고 전문적인 퀀트/가치투자 리서치 요약문 생성"""
        clean_t = self.clean_title(title)
        
        # 카테고리 및 핵심 키워드 기반의 전문 분석 요약문 재작성
        if category == "AI 반도체" or any(k in clean_t for k in ["반도체", "HBM", "하이닉스", "삼성전자", "엔비디아", "CXL", "소부장"]):
            return f"{clean_t} 이슈를 중심으로 글로벌 빅테크 AI 인프라 투자 확대에 따른 차세대 메모리(HBM/CXL) 및 첨단 반도체 소부장 밸류체인의 분기 실적 가시성, 밸류에이션(PER/PBR) 및 수급 집중도를 심층 분석합니다."
        elif category == "저평가 가치주" or any(k in clean_t for k in ["밸류업", "저PBR", "배당", "자사주", "금융지주"]):
            return f"{clean_t} 관련 기업 밸류업 프로그램 및 주주환원 정책 확대에 따른 저PBR 우량주, 금융지주 및 지주사 섹터의 멀티플 리레이팅 효과와 외국인·기관 패시브 자금 유입 모멘텀을 정밀 점검합니다."
        elif category == "거시경제/금리" or any(k in clean_t for k in ["금리", "환율", "대출", "가계부채", "한은", "한국은행", "물가"]):
            return f"{clean_t} 관련 통화정책 기조와 글로벌 매크로 지표 변화를 점검하고, 기준금리 경로 및 외환시장 변동성이 국내 금융시장 순이자마진(NIM)과 업종별 실적 펀더멘털에 미치는 파급 효과를 분석합니다."
        elif category == "상승초입주" or any(k in clean_t for k in ["상승초입", "골든크로스", "돌파", "신고가", "바닥권", "거래량"]):
            return f"{clean_t} 관련 기술적 수급 분석으로, 바닥권 거래량 급증 및 주요 이동평균선 수렴 후 골든크로스가 발생한 주도 섹터의 차트 지지선, 손익비 및 분할 매매 실행 가이드를 제시합니다."
        elif category == "공모주 청약" or any(k in clean_t for k in ["공모주", "청약", "IPO", "상장", "수요예측"]):
            return f"{clean_t} 관련 신규 상장 공모주의 펀더멘털 분석으로, 기관 수요예측 경쟁률, 의무보유 확약비율, 상장 첫날 유통 가능 물량 및 적정 공모가 밴드를 정밀 평가합니다."
        elif category == "배당주 투자" or any(k in clean_t for k in ["배당", "월배당", "ETF", "ISA", "IRP", "절세"]):
            return f"{clean_t} 관련 안정적 현금흐름 구축 전략으로, 고배당 ETF 및 배당성장주의 시가배당률, 주당배당금(DPS) 추이 및 비과세 절세 계좌를 활용한 실전 자산배분 포트폴리오를 안내합니다."
        elif category == "모빌리티/신기술" or any(k in clean_t for k in ["2차전지", "배터리", "전고체", "현대차", "기아", "로봇"]):
            return f"{clean_t} 관련 미래 모빌리티 및 첨단 하드웨어 산업 분석으로, 완성차 고수익 하이브리드 판매 믹스와 2차전지·로보틱스 밸류체인의 기술 혁신 및 중장기 실적 턴어라운드를 다룹니다."
        elif category == "바이오/제약" or any(k in clean_t for k in ["바이오", "제약", "임상", "FDA", "신약", "CDMO"]):
            return f"{clean_t} 관련 바이오헬스케어 핵심 파이프라인 분석으로, FDA 임상 단계별 성공 확률, 글로벌 기술수출(L/O) 계약 규모 및 대형 CDMO 생산능력 확장에 따른 밸류에이션을 평가합니다."
        elif category == "원자재/지정학" or any(k in clean_t for k in ["유가", "방산", "원자재", "조선", "원전", "변압기"]):
            return f"{clean_t} 관련 글로벌 공급망 및 지정학적 수주 모멘텀 분석으로, 3~4년 치 수주 잔고를 확보한 방산·조선·전력 인프라 대장주의 구조적 이익 성장 사이클을 심층 점검합니다."
        else:
            return f"{clean_t} 이슈에 대한 펀더멘털 및 퀀트 밸류에이션 리서치 보고서로, 시장의 핵심 모멘텀, 기업 재무 건전성 및 실전 투자 전략을 종합 정리합니다."

    def score_news(self, item):
        """뉴스 항목에 대한 투자 가치 및 광고 적합도 점수 산출"""
        t = item.get("title", "")
        d = item.get("description", "") or item.get("summary", "")

        # 차단 키워드 또는 차단 제목인 경우 최하점 부여 (선별 배제)
        if self.is_banned(t, d):
            return -999999

        score = 0

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

        # 단순 사건사고, 연예/가십 및 증시 무관 지정학/정치 뉴스 강력 감점
        for bad in ["포토", "인사", "부고", "동정", "날씨", "사고", "화재", "살인", "폭행", "음주", 
                    "이란", "안보수장", "미사일", "폭격", "전쟁", "군사", "총격", "사망", "피살", 
                    "테러", "외교부", "국방부", "대통령실", "정치", "국회", "여야", "청문회", "간첩"]:
            if bad in t or bad in d:
                score -= 100

        return score

    def collect_trending_topics(self):
        """여러 금융 RSS 소스에서 '중복되지 않고 차단되지 않은 가장 신선한 최신 뉴스' 선별 수집 및 100% 저작권 안전 리서치 가공"""
        all_news = []
        for feed in RSS_FEEDS:
            items = self.fetch_feed(feed["url"])
            for item in items:
                item["source_name"] = "Value Stock Labs 리서치센터"
                item["feed_category"] = feed["category"]
                all_news.append(item)

        print(f"[정보] 총 {len(all_news)}건의 실시간 뉴스 아이템 수집 완료. 중복 및 기발행 여부 검사 중...")

        # 1. 이미 발행된 기사 및 차단 기사 필터링
        fresh_news = []
        for item in all_news:
            raw_t = item.get("title", "")
            desc = item.get("description", "")
            if self.is_banned(raw_t, desc):
                continue
            title = self.clean_title(raw_t)
            if self.is_banned(title, desc):
                continue
            if not self.is_already_published(title):
                item["title"] = title
                fresh_news.append(item)

        print(f"[정보] 기발행 및 차단 항목 제외 후 신규 뉴스 후보: {len(fresh_news)}건")

        if not fresh_news:
            print("⚠️ [알림] 새로운 RSS 기사가 모두 기발행되었거나 없어 날짜별 고유 테마 캘린더에서 선별합니다.")
            return self.get_fallback_topic()

        # 점수 높은 순으로 정렬
        fresh_news.sort(key=self.score_news, reverse=True)
        best_item = fresh_news[0]

        clean_final_title = self.clean_title(best_item["title"])
        if self.is_banned(clean_final_title, best_item.get("description", "")):
            print(f"⚠️ [차단 알림] 선별된 기사('{clean_final_title}')가 영구 차단 목록에 해당하여 대체 주제로 전환합니다.")
            return self.get_fallback_topic()

        category, keywords = self.classify_category_and_keywords(clean_final_title, best_item.get("description", ""))
        rewritten_summary = self.rewrite_summary(clean_final_title, category, keywords, best_item.get("description", ""))

        return {
            "title": clean_final_title,
            "category": category,
            "keywords": keywords,
            "summary": rewritten_summary,
            "source_name": "Value Stock Labs 리서치센터",
            "link": "",
            "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    def collect_market_data(self):
        """adsense-stock-blog/data/market-summary.json 파일에서 실시간 증시 데이터를 파싱하여 심볼/ID 맵핑 반환"""
        data_file = Path(__file__).resolve().parent.parent / "adsense-stock-blog" / "data" / "market-summary.json"
        
        # 파일이 없으면 실시간 수집기 실행
        if not data_file.exists():
            try:
                import fetch_live_market
                fetch_live_market.main()
            except Exception as e:
                print(f"[알림] 실시간 시세 수집 실행 건너뜀: {e}")

        market_map = {}
        if data_file.exists():
            try:
                with open(data_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for item in data.get("instruments", []):
                        diff_rate = item.get("diffRate", 0.0)
                        entry = {
                            "name": item.get("name", ""),
                            "price": item.get("price", 0),
                            "change": diff_rate,
                            "diffRate": diff_rate,
                            "diff": item.get("diff", 0.0),
                            "baseClose": item.get("baseClose", 0)
                        }
                        if "symbol" in item:
                            market_map[item["symbol"]] = entry
                        if "id" in item:
                            market_map[item["id"]] = entry
                            market_map[item["id"].upper()] = entry
            except Exception as e:
                print(f"[알림] market-summary.json 읽기 실패: {e}")

        return market_map

    def get_fallback_morning_headlines(self):
        """인터넷 연결이 불안정하거나 RSS 수집이 부족할 때 사용할 고품질 모닝 시황 헤드라인 5선"""
        today_date = datetime.now().strftime("%Y년 %m월 %d일")
        return [
            {
                "title": f"[{today_date}] 뉴욕증시 빅테크 실적 기대감 속 AI 반도체 밸류체인 훈풍 지속",
                "summary": "엔비디아 블랙웰 아키텍처 양산 본격화 및 빅테크 AI 인프라 CAPEX 확대 기대감에 나스닥과 필라델피아 반도체 지수가 견조한 흐름을 이어갔습니다."
            },
            {
                "title": f"[{today_date}] 한국은행 통화정책 전환 국면… 예대금리차 및 가계부채 관리 파장",
                "summary": "기준금리 인하 가시화에도 시중은행의 주담대 가산금리 인상 조치로 금융권의 순이자마진(NIM) 방어와 내수 소비재 섹터 수급 동향이 주목받고 있습니다."
            },
            {
                "title": f"[{today_date}] 밸류업 2차 세제 개편안 기대… 저PBR 고배당 금융·지주사 외국인 순매수",
                "summary": "배당소득 분리과세 및 자사주 소각 인센티브 등 정부의 기업 밸류업 세제 지원책 구체화에 따라 저평가 우량주로의 기관·외국인 자금 유입이 지속되고 있습니다."
            },
            {
                "title": f"[{today_date}] 원/달러 환율 1,360원대 박스권 등락… 수출 대형주 실적 레버리지 부각",
                "summary": "글로벌 달러화 인덱스 안정 속에 자동차·조선·반도체 등 핵심 수출 기업들의 3분기 실적 개선세와 영업이익 상향 조정이 이어지고 있습니다."
            },
            {
                "title": f"[{today_date}] 비트코인 1억 원대 안착… 글로벌 가상자산 ETF 기관 자금 순유입",
                "summary": "미국 현물 ETF로의 지속적인 기관 자금 유입과 거시 매크로 유동성 공급 기대감에 주요 가상자산이 안정적인 지지선을 구축하고 있습니다."
            }
        ]

    def get_morning_headlines(self):
        """모닝 브리핑용 5대 핵심 시장 축(글로벌증시, 반도체테크, 주도섹터실적, 매크로/밸류업, 대체투자/원자재) 기반 완벽 선별"""
        today_date = datetime.now().strftime("%Y년 %m월 %d일")
        
        # 5대 핵심 필러별 목표 키워드 및 기본 고품질 테마 정의
        pillars = [
            {
                "id": "global_market",
                "name": "글로벌 증시 & 빅테크",
                "keywords": ["뉴욕증시", "나스닥", "S&P500", "S&P 500", "다우존스", "월가", "월스트리트", "엔비디아", "미 증시", "美 증시", "필라델피아반도체"],
                "fallback": {
                    "title": f"[{today_date}] 뉴욕증시 빅테크 실적 기대감 속 AI 반도체 밸류체인 훈풍 지속",
                    "summary": "엔비디아 블랙웰 아키텍처 양산 본격화 및 빅테크 AI 인프라 CAPEX 확대 기대감에 나스닥과 필라델피아 반도체 지수가 견조한 상승 탄력을 이어갔습니다."
                }
            },

            {
                "id": "semiconductor",
                "name": "AI 반도체 & 첨단 테크",
                "keywords": ["반도체", "HBM", "SK하이닉스", "삼성전자", "CXL", "파운드리", "소부장", "패키징", "TC본더", "온디바이스", "용인", "이천"],
                "fallback": {
                    "title": f"[{today_date}] 차세대 AI 반도체 HBM4 로드맵 안착… 삼성전자·SK하이닉스 소부장 낙수효과",
                    "summary": "글로벌 빅테크의 맞춤형(커스텀) AI 칩 수요 급증으로 차세대 HBM 공급 부족이 지속되며 첨단 후공정 및 본딩 장비주의 분기 실적 가시성이 높아지고 있습니다."
                }
            },
            {
                "id": "key_sectors",
                "name": "국내 주도 섹터 & 기업 실적",
                "keywords": ["현대차", "기아", "2차전지", "배터리", "조선업", "조선사", "조선 3사", "신조선가", "HD한국조선해양", "삼성중공업", "한화오션", "K-방산", "방산 수주", "한화에어로스페이스", "현대로템", "LIG넥스원", "원전", "바이오", "실적", "영업이익", "수주", "어닝서프라이즈", "체코 원전", "양극재", "CDMO"],
                "fallback": {
                    "title": f"[{today_date}] 완성차 하이브리드 고수익 안착 & K-방산·조선 조 단위 수주 랠리 가속",
                    "summary": "현대차·기아의 고마진 하이브리드 판매 호조와 함께 방산 및 친환경 선박 대장주들의 3~4년 치 수주 잔고가 분기 사상 최대 실적으로 본격 전환 중입니다."
                }
            },
            {
                "id": "macro_valueup",
                "name": "거시경제 & 밸류업·수급",
                "keywords": ["코스피", "코스닥", "외국인 순매수", "기관 순매수", "외국인 매수", "외인 순매수", "밸류업", "저PBR", "배당", "자사주", "한국은행", "기준금리", "원달러", "원/달러", "환율", "외환"],
                "fallback": {
                    "title": f"[{today_date}] 밸류업 2차 세제 혜택 확정 기대… 저PBR 고배당 금융·지주사 외국인 순매수 유입",
                    "summary": "배당소득 분리과세 및 자사주 소각 인센티브 등 정부의 자본시장 밸류업 정책 구체화로 저평가 우량주와 금융지주사로의 기관·외국인 매수세가 집중되고 있습니다."
                }
            },
            {
                "id": "crypto_commodity",
                "name": "가상자산 & 원자재·대체투자",
                "keywords": ["비트코인", "가상자산", "이더리움", "국제유가", "WTI", "금값", "원자재", "구리", "암호화폐", "가상화폐", "정제마진", "OPEC"],
                "fallback": {
                    "title": f"[{today_date}] 비트코인 1억 원대 견조한 지지선 구축… 글로벌 현물 ETF 기관 자금 순유입",
                    "summary": "미국 가상자산 현물 ETF로의 지속적인 기관 자금 유입과 디지털 자산 제도권 안착 기대감에 주요 가상자산이 변동성을 축소하며 우상향 흐름을 모색하고 있습니다."
                }
            }
        ]

        target_feeds = [
            {"url": "https://www.mk.co.kr/rss/30100041/", "name": "매경 증시"},
            {"url": "https://www.mk.co.kr/rss/30200030/", "name": "매경 금융·거시"},
            {"url": "https://www.mk.co.kr/rss/50200011/", "name": "매경 기업·산업"},
            {"url": "https://news.google.com/rss/search?q=코스피+OR+코스닥+OR+뉴욕증시+OR+반도체+주가&hl=ko&gl=KR&ceid=KR:ko", "name": "글로벌 증시"}
        ]

        # 증시 무관 비금융/사법/사건사고/가십/단순사회뉴스 철저 배제
        non_financial_bad_words = [
            "대법원", "대법관", "판사", "검찰", "재판", "법원", "기소", "구속", "징역", "형사", "경찰", 
            "격려금", "특검", "청문회", "국회", "여야", "정치권", "사망", "피살", "살인", "폭행", "음주", 
            "사고", "화재", "폭발", "날씨", "장마", "태풍", "홍수", "축구", "야구", "올림픽", "연예", 
            "포토", "동정", "부고", "인사", "간첩", "간담회", "아동수당", "설계사", "보험왕", "변호사", 
            "변리사", "회계사", "중국 동포", "취업", "직업", "월급", "자립펀드", "양육비", "고시표",
            "국방상", "북한", "북조선", "조선인민군", "조선중앙통신", "노동당", "김정은", "프리덤에지",
            "한미일", "탄도미사일", "미사일", "무력시위", "합참", "군사훈련", "대응조치", "안보실", "외교부"
        ]

        raw_news = []
        for f in target_feeds:
            items = self.fetch_feed(f["url"])
            for it in items:
                t = it.get("title", "").strip()
                d = it.get("description", "").strip()
                if len(t) < 8:
                    continue
                # 단순 데이터 표/고시표/공지사항 필터링
                if t.startswith("[표]") or t.startswith("[공시]") or t.startswith("[알림]") or t.startswith("[인사]") or t.startswith("[부고]") or "외국환율고시표" in t:
                    continue
                if any(bad in t for bad in non_financial_bad_words):
                    continue
                if any(bad in d for bad in ["살인", "폭행", "사망", "구속", "징역", "대법관", "부고", "설계사", "보험왕"]):
                    continue
                raw_news.append({"title": t, "description": d})


        headlines = []
        used_titles = set()

        for pillar in pillars:
            matched_item = None
            for item in raw_news:
                t = item["title"]
                d = item["description"]
                full_t = f"{t} {d}"
                if t in used_titles:
                    continue
                if any(kw in full_t for kw in pillar["keywords"]):
                    matched_item = item
                    used_titles.add(t)
                    break

            if matched_item:
                clean_t = self.clean_title(matched_item["title"])
                summary_text = self.rewrite_summary(clean_t, pillar["name"], pillar["keywords"], matched_item.get("description", ""))
                headlines.append({
                    "title": clean_t,
                    "summary": summary_text,
                    "pillar_id": pillar["id"]
                })
            else:
                # 폴백 사용
                fb = dict(pillar["fallback"])
                fb["title"] = self.clean_title(fb["title"])
                fb["pillar_id"] = pillar["id"]
                headlines.append(fb)

        return headlines[:5]



if __name__ == "__main__":
    collector = NewsCollector()
    topic = collector.collect_trending_topics()
    print("\n=== [수집된 최신 핫이슈 결과] ===")
    print(f"📌 제목: {topic['title']}")
    print(f"📂 카테고리: {topic['category']}")
    print(f"🏷️ 키워드: {', '.join(topic['keywords'])}")
    print(f"📝 요약: {topic['summary']}")

    print("\n=== [수집된 모닝 브리핑 헤드라인 5선] ===")
    morning_items = collector.get_morning_headlines()
    for idx, mh in enumerate(morning_items, 1):
        print(f" {idx}. {mh['title']}")

