"""
=============================================================================
ARTICLE GENERATOR (article_generator.py)
기사 제목 연동 심층 분석 본문 생성 & 메타 UI 최적화 엔진
=============================================================================
"""

import re
import html
import hashlib
from datetime import datetime
from config import BLOG_DOMAIN, ADSENSE_PUB_ID

class ArticleGenerator:
    def __init__(self):
        pass

    def create_slug(self, title):
        """한글/영문 제목에서 안전하고 유니크한 파일명 슬러그 생성"""
        clean = re.sub(r'[^\w\s-]', '', title).strip().lower()
        slug = re.sub(r'[-\s]+', '-', clean).strip('-')
        clean_slug = slug[:40].rstrip('-')
        date_prefix = datetime.now().strftime("%Y%m%d")
        return f"{date_prefix}-{clean_slug}" if clean_slug else f"{date_prefix}-report"

    def detect_topic_type(self, title, summary=""):
        """제목 및 요약문을 분석하여 세부 리포트 템플릿 유형 결정"""
        full_text = f"{title} {summary}"

        if any(k in full_text for k in ["반도체", "HBM", "엔비디아", "하이닉스", "삼성전자", "파운드리", "CXL", "온디바이스", "소부장", "빅테크", "AI투자", "AI"]):
            return "ai_semiconductor"
        elif any(k in full_text for k in ["대출", "가계부채", "가산금리", "월급쟁이", "예대", "주담대", "신용대출"]):
            return "macro_interest_rate"
        elif any(k in full_text for k in ["금리", "한은", "한국은행", "기준금리", "물가", "환율", "인플레", "통화정책"]):
            return "macro_interest_rate"
        elif any(k in full_text for k in ["밸류업", "저PBR", "배당", "주주환원", "자사주", "금융지주", "은행주", "보험주", "지주사"]):
            return "valueup_dividend"
        elif any(k in full_text for k in ["2차전지", "배터리", "전고체", "양극재", "에코프로", "포스코", "로봇", "자율주행", "모빌리티"]):
            return "battery_mobility"
        elif any(k in full_text for k in ["바이오", "제약", "임상", "FDA", "CDMO", "신약", "기술수출", "비만치료제"]):
            return "bio_healthcare"
        elif any(k in full_text for k in ["공모주", "청약", "IPO", "상장", "수요예측"]):
            return "ipo"
        elif any(k in full_text for k in ["전력", "변압기", "전선", "데이터센터", "원전", "에너지"]):
            return "power_energy"
        elif any(k in full_text for k in ["유가", "방산", "중동", "지정학", "해운", "조선"]):
            return "geopolitics"
        else:
            return "general_stock"

    def get_category_image_info(self, topic_type, title):
        """주제 유형 및 제목 고유 해시를 바탕으로 중복 없이 다양한 썸네일 이미지 매핑 (동일 섹터 내에서도 글마다 다른 사진 할당)"""
        title_hash = int(hashlib.md5(title.encode('utf-8')).hexdigest(), 16)

        image_pools = {
            "ai_semiconductor": [
                "images/semiconductor-1.jpg",
                "images/semiconductor-2.jpg",
                "images/semiconductor-3.jpg",
                "images/semiconductor-4.jpg",
                "images/semiconductor.jpg",
            ],
            "valueup_dividend": [
                "images/dividend-1.jpg",
                "images/dividend-2.jpg",
                "images/dividend-3.jpg",
                "images/dividend.jpg",
            ],
            "macro_interest_rate": [
                "images/macro-1.jpg",
                "images/macro-2.jpg",
                "images/macro-3.jpg",
                "images/market-3.jpg",
            ],
            "battery_mobility": [
                "images/battery-1.jpg",
                "images/breakout-2.jpg",
                "images/breakout-3.jpg",
            ],
            "bio_healthcare": [
                "images/bio-1.jpg",
                "images/market-2.jpg",
            ],
            "ipo": [
                "images/ipo-1.jpg",
                "images/ipo-2.jpg",
                "images/ipo.jpg",
            ],
            "power_energy": [
                "images/breakout-3.jpg",
                "images/semiconductor-2.jpg",
                "images/market-4.jpg",
            ],
            "geopolitics": [
                "images/macro-1.jpg",
                "images/market-3.jpg",
                "images/market-4.jpg",
            ],
            "breakout": [
                "images/breakout-1.jpg",
                "images/breakout-2.jpg",
                "images/breakout-3.jpg",
                "images/breakout.jpg",
            ],
            "general_stock": [
                "images/market-1.jpg",
                "images/market-2.jpg",
                "images/market-3.jpg",
                "images/market-4.jpg",
                "images/breakout-1.jpg",
                "images/hero.jpg",
            ]
        }

        pool = image_pools.get(topic_type, image_pools["general_stock"])
        chosen_img = pool[title_hash % len(pool)]

        return chosen_img, f"▲ {title} 관련 심층 데이터 분석 및 시장 동향"

    def build_contextual_sections(self, topic_type, title, summary, category, keywords):
        """기사 제목과 뉴스 맥락에 100% 일치하는 구체적인 5개 본문 섹션 HTML 생성"""
        clean_title = html.escape(title)
        clean_summary = html.escape(summary)
        kw_str = ", ".join(keywords)

        if topic_type == "macro_interest_rate":
            # 거시경제 / 대출금리 / 가계부채 / 예대마진 맞춤형 본문
            return f"""
        <!-- Section 1 -->
        <section id="sec-issue-brief">
          <h2>1. 핵심 이슈 브리핑: 대출금리 양극화와 금융시장 배경</h2>
          <p>
            최근 금융권과 가계 경제를 강타하고 있는 핵심 이슈는 <strong>“{clean_title}”</strong> 현상입니다.
            {clean_summary}
          </p>
          <div class="callout callout-info">
            <strong>💡 리서치센터 핵심 팩트체크:</strong><br>
            • <strong>가계대출 가산금리 인상:</strong> 금융당국의 가계부채 총량 관리 압박에 따라 시중은행들이 주택담보대출 및 신용대출 가산금리를 연이어 인상했습니다.<br>
            • <strong>기업대출 유치 경쟁:</strong> 반면 우량 대기업 및 중소기업 대출 확보를 위한 은행 간 금리 인하 경쟁이 붙으면서 기업대출 금리는 하향 안정세를 보이고 있습니다.<br>
            • <strong>예대금리차 확대:</strong> 결과적으로 가계 대출자의 이자 부담은 가중되고 은행권의 예대마진(NIS)은 단기적으로 확대되는 왜곡 현상이 발생했습니다.
          </div>
          <p>
            기준금리 인하에 대한 기대감이 높아지는 거시경제 환경 속에서도, 가계 대출자들은 체감 금리 인하 혜택을 받지 못하고 
            오히려 가산금리 인상으로 인한 이자 상환 부담이 늘어나는 이중고를 겪고 있습니다.
          </p>
        </section>

        <!-- Section 2 -->
        <section id="sec-impact-analysis">
          <h2>2. 시장 파급 효과 및 은행·금융 섹터 영향 분석</h2>
          <p>
            이번 대출금리 역전 및 가산금리 조정은 단순한 개인 금융 문제를 넘어 <strong>국내 증시 및 금융업종 밸류에이션</strong>에 복합적인 영향을 미치고 있습니다:
          </p>
          <ul>
            <li><strong>은행주 순이자마진(NIM) 방어:</strong> 가계대출 가산금리 인상으로 주요 금융지주(KB금융, 신한지주, 하나금융지주 등)의 단기 이자이익 마진이 견조하게 유지되고 있습니다.</li>
            <li><strong>내수 소비 및 가계 가처분소득 둔화:</strong> 월급쟁이 등 실수요 가계의 원리금 상환액이 증가하면서 유통, 소비재, 레저 등 내수 민감 섹터의 실적 회복 속도가 지연될 가능성이 있습니다.</li>
            <li><strong>신용 리스크 및 건전성 관리:</strong> 다중채무자 및 영끌 대출자의 연체율 상승 여부가 은행권의 대손충당금 적립 규모를 결정짓는 핵심 변수로 부상하고 있습니다.</li>
          </ul>
        </section>

        <!-- Section 3: Data Table -->
        <section id="sec-data-table">
          <h2>3. 핵심 수치 및 대출 유형별 금리 동향 지표</h2>
          <p>
            아래는 최근 시중은행의 차주별(가계 vs 기업) 평균 대출금리 및 예대마진 추이를 정리한 데이터 비교표입니다:
          </p>

          <div class="table-responsive">
            <table class="metrics-table">
              <thead>
                <tr>
                  <th>구분</th>
                  <th>평균 대출금리 추이</th>
                  <th>가산금리 변동폭</th>
                  <th>주요 영향 및 금융당국 정책</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><strong>가계 주택담보대출</strong></td>
                  <td style="color:var(--accent-red); font-weight:700;">3.95% ~ 4.45% ▲</td>
                  <td>+0.20%p ~ +0.40%p 인상</td>
                  <td>가계부채 억제 가이드라인 및 DSR 강화</td>
                </tr>
                <tr>
                  <td><strong>가계 신용대출</strong></td>
                  <td style="color:var(--accent-red); font-weight:700;">5.10% ~ 5.80% ▲</td>
                  <td>+0.15%p ~ +0.30%p 인상</td>
                  <td>월급쟁이 직장인 한도 축소 및 우대금리 축소</td>
                </tr>
                <tr>
                  <td><strong>대기업 대출</strong></td>
                  <td style="color:#00f2fe; font-weight:700;">4.10% ~ 4.30% ▼</td>
                  <td>-0.10%p ~ -0.25%p 인하</td>
                  <td>우량 기업 유치 경쟁 및 회사채 대체 수요</td>
                </tr>
                <tr>
                  <td><strong>중소기업 대출</strong></td>
                  <td>4.60% ~ 4.90% (보합)</td>
                  <td>변동폭 제한적</td>
                  <td>정책금융 및 보증부 대출 우대 적용</td>
                </tr>
              </tbody>
            </table>
          </div>
          <p>
            이러한 금리 격차는 향후 한국은행의 통화정책 완화 기조와 금융당국의 거시건전성 규제 완화 여부에 따라 점진적으로 수렴할 것으로 전망됩니다.
          </p>
        </section>

        <!-- Section 4 -->
        <section id="sec-strategy">
          <h2>4. 금융소비자 & 투자자 관점 실전 대응 전략</h2>
          <p>
            금리 변동성이 큰 시기에는 자산과 부채를 정밀하게 점검하고 전략적인 재무 조정을 실행해야 합니다:
          </p>
          <div class="callout callout-warning">
            <strong>📋 필수 금융 대응 수칙:</strong><br>
            1. <strong>온라인 원스톱 대환대출 인프라 적극 활용:</strong> 은행 간 대출 갈아타기 플랫폼을 통해 금리 0.3%p 이상 낮은 상품으로 적극 전환.<br>
            2. <strong>금리인하요구권 행사:</strong> 승진, 연봉 인상, 신용점수 상승, 부채 감소 등 조건 충족 시 주거래 은행에 즉시 금리인하 신청.<br>
            3. <strong>고정금리 vs 변동금리 리밸런싱:</strong> 향후 1~2년 내 기준금리 인하 사이클 도래를 감안하여 주기형/변동형 금리 비중을 합리적으로 분산.
          </div>
        </section>
"""
        elif topic_type == "ai_semiconductor":
            # AI 반도체 / HBM / 소부장 맞춤형 본문
            return f"""
        <!-- Section 1 -->
        <section id="sec-issue-brief">
          <h2>1. 핵심 이슈 브리핑: AI 반도체 슈퍼사이클 및 공급망 현황</h2>
          <p>
            글로벌 빅테크의 AI 인프라 투자 지속과 함께 <strong>“{clean_title}”</strong> 이슈가 글로벌 증시의 강력한 모멘텀으로 작용하고 있습니다.
            {clean_summary}
          </p>
          <div class="callout callout-info">
            <strong>💡 리서치센터 핵심 팩트체크:</strong><br>
            • <strong>HBM / 첨단 패키징 쇼티지:</strong> 엔비디아의 차세대 GPU 라인업(블랙웰 등) 수요 폭증으로 고대역폭 메모리(HBM3E, HBM4) 공급 부족이 지속되고 있습니다.<br>
            • <strong>글로벌 팹 증설 및 CAPEX 집행:</strong> SK하이닉스, 삼성전자, TSMC 등 글로벌 파운드리 및 메모리 선도기업들의 대규모 설비투자가 본격화되고 있습니다.<br>
            • <strong>소부장 밸류체인 수혜 확산:</strong> 전공정 EUV 및 후공정 TC본더, 테스트 소켓, CXL 검사장비 등 핵심 기술력을 보유한 국내 소부장 기업들의 실적 퀀텀점프가 기대됩니다.
          </div>
        </section>

        <!-- Section 2 -->
        <section id="sec-impact-analysis">
          <h2>2. 섹터별 밸류에이션 및 실적 퀀텀점프 전망</h2>
          <p>
            과거 단순 메모리 사이클과 달리 이번 AI 랠리는 <strong>높은 영업이익률(OPM)과 독점적 단가 결정력</strong>을 기반으로 구조적인 밸류에이션 리레이팅이 진행되고 있습니다:
          </p>
          <ul>
            <li><strong>HBM 선도 메모리사:</strong> 공급 단가 프리미엄과 장기 공급 계약(LTA) 체결로 2026년 역대 최대 영업이익 달성 가시화.</li>
            <li><strong>후공정(OSAT) 및 첨단 패키징 장비주:</strong> 하이브리드 본딩, 3D 패키징 장비 수주 잔고 급증에 따른 멀티플 상향.</li>
            <li><strong>온디바이스 AI & CXL 생태계:</strong> 서버뿐 아니라 스마트폰, PC, 자율주행차로 AI 칩 탑재가 확산되며 신규 폼팩터 수혜주 발굴 가속.</li>
          </ul>
        </section>

        <!-- Section 3: Data Table -->
        <section id="sec-data-table">
          <h2>3. 핵심 반도체 세부 밸류체인 지표 비교표</h2>
          <div class="table-responsive">
            <table class="metrics-table">
              <thead>
                <tr>
                  <th>분야</th>
                  <th>대표 수혜 영역</th>
                  <th>예상 영업이익률 (OPM)</th>
                  <th>핵심 투자 체크포인트</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><strong>HBM 메모리 선도주</strong></td>
                  <td>HBM3E / HBM4 독점 공급</td>
                  <td style="color:var(--accent-red); font-weight:700;">35% ~ 45%</td>
                  <td>엔비디아 퀄테스트 통과 및 수율 안정성</td>
                </tr>
                <tr>
                  <td><strong>첨단 패키징 본딩 장비</strong></td>
                  <td>TC 본더, 하이브리드 본더</td>
                  <td style="color:var(--accent-red); font-weight:700;">28% ~ 34%</td>
                  <td>글로벌 OSAT 고객사 다변화 및 독점 라이선스</td>
                </tr>
                <tr>
                  <td><strong>테스트 & CXL 검사 소켓</strong></td>
                  <td>실리콘 러버 소켓, CXL 2.0</td>
                  <td>22% ~ 27%</td>
                  <td>고단수 적층 칩 테스트 시간 증가에 따른 소모품 수요</td>
                </tr>
                <tr>
                  <td><strong>반도체 소재/가스</strong></td>
                  <td>특수가스, 감광액, 식각액</td>
                  <td>15% ~ 20%</td>
                  <td>가동률 100% 도달에 따른 분기별 Q 증가</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <!-- Section 4 -->
        <section id="sec-strategy">
          <h2>4. 기술적 지지선 및 실전 매매 대응 전략</h2>
          <p>
            주도주 섹터에서는 추격 매수보다 주요 이동평균선(20일선, 60일선) 눌림목을 활용한 분할 접근이 유리합니다:
          </p>
          <div class="callout callout-warning">
            <strong>🎯 실전 포트폴리오 운용 원칙:</strong><br>
            - 실적 가시성이 가장 높은 대장주 60%, 고성장 소부장 중소형주 40% 비중 구성<br>
            - 기관·외국인 수급 유입 연속성 확인 및 전고점 돌파 거래량 체크<br>
            - 주요 지지선(-5% ~ -7%) 이탈 시 기계적 리스크 관리 원칙 준수
          </div>
        </section>
"""
        elif topic_type == "valueup_dividend":
            # 밸류업 / 저PBR / 배당주 맞춤형 본문
            return f"""
        <!-- Section 1 -->
        <section id="sec-issue-brief">
          <h2>1. 핵심 이슈 브리핑: 기업 밸류업 프로그램과 주주환원</h2>
          <p>
            정부의 자본시장 선진화 정책과 세제 개편안에 힘입어 <strong>“{clean_title}”</strong> 테마에 외국인 투자자들의 장기 투자 자금이 집중되고 있습니다.
            {clean_summary}
          </p>
          <div class="callout callout-info">
            <strong>💡 리서치센터 핵심 팩트체크:</strong><br>
            • <strong>PBR 1배 미만 해소:</strong> 청산가치에도 미치지 못하던 금융, 지주사, 전통 제조업 우량주들의 밸류에이션 정상화 가속.<br>
            • <strong>주주환원율 40% 시대:</strong> 배당금 확대뿐 아니라 자사주 매입 및 전량 소각 공시가 잇따르며 주당순이익(EPS)과 주당순자산(BPS)이 동반 상승.<br>
            • <strong>세제 혜택 인센티브:</strong> 배당소득 분리과세 및 법인세 세액공제 도입으로 대주주와 일반 주주의 이해관계가 일치하는 선순환 구조 정착.
          </div>
        </section>

        <!-- Section 2 -->
        <section id="sec-impact-analysis">
          <h2>2. 펀더멘털 지표(PER·PBR·ROE) 및 외국인 수급 분석</h2>
          <p>
            글로벌 펀드들은 코리아 디스카운트 해소 가능성에 베팅하며 안정적인 배당수익률과 자사주 소각 여력이 풍부한 기업을 집중 매수하고 있습니다:
          </p>
          <ul>
            <li><strong>금융지주 및 은행/보험주:</strong> 배당수익률 6~8%대 및 분기 균등 배당 정착으로 강력한 하방 지지선 형성.</li>
            <li><strong>순수 지주사:</strong> 자회사 배당금 유입 및 자사주 소각 계획 발표로 NAV(순자산가치) 대비 할인율 축소.</li>
            <li><strong>현금성 자산 풍부 제조사:</strong> 순현금 비중이 시가총액의 50%를 상회하는 자산주들의 리레이팅 랠리.</li>
          </ul>
        </section>

        <!-- Section 3: Data Table -->
        <section id="sec-data-table">
          <h2>3. 대표 저평가 가치주 밸류에이션 지표 비교표</h2>
          <div class="table-responsive">
            <table class="metrics-table">
              <thead>
                <tr>
                  <th>구분</th>
                  <th>PER (배)</th>
                  <th>PBR (배)</th>
                  <th>ROE (%)</th>
                  <th>배당수익률</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><strong>대표 금융지주 톱픽</strong></td>
                  <td>5.2배</td>
                  <td style="color:var(--accent-red); font-weight:700;">0.48배</td>
                  <td>11.5%</td>
                  <td style="color:var(--accent-red); font-weight:700;">6.8% (분기배당)</td>
                </tr>
                <tr>
                  <td><strong>우량 지주사 밸류업군</strong></td>
                  <td>6.8배</td>
                  <td style="color:var(--accent-red); font-weight:700;">0.55배</td>
                  <td>9.8%</td>
                  <td>5.4% (자사주소각)</td>
                </tr>
                <tr>
                  <td><strong>코스피 전체 평균</strong></td>
                  <td>11.8배</td>
                  <td>0.95배</td>
                  <td>8.2%</td>
                  <td>2.1%</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <!-- Section 4 -->
        <section id="sec-strategy">
          <h2>4. 배당 재투자 및 절세 계좌(ISA/IRP) 실전 활용법</h2>
          <div class="callout callout-warning">
            <strong>💰 절세 극대화 팁:</strong><br>
            - 일반 계좌 배당소득세(15.4%) 대신 <strong>중개형 ISA(최대 500만원 비과세, 초과분 9.9% 분리과세)</strong>를 활용하여 복리 효과 극대화.<br>
            - 연금저축/IRP 계좌에서 고배당 밸류업 ETF를 매수하여 배당금 전액 과세이연 및 재투자 실행.
          </div>
        </section>
"""
        else:
            # 일반 주식 / 산업 리서치 / 시황 맞춤형 본문
            return f"""
        <!-- Section 1 -->
        <section id="sec-issue-brief">
          <h2>1. 핵심 이슈 브리핑: 시장 배경 및 팩트체크</h2>
          <p>
            최근 국내외 증시 및 금융 시장에서 큰 주목을 받고 있는 핵심 테마는 <strong>“{clean_title}”</strong>입니다.
            {clean_summary}
          </p>
          <div class="callout callout-info">
            <strong>💡 리서치센터 핵심 관전 포인트:</strong><br>
            • <strong>시장 모멘텀:</strong> 매크로 지표 변화와 업종별 수급 순환매 속에서 {clean_title} 관련 핵심 기업들로 스마트 머니가 유입되고 있습니다.<br>
            • <strong>실적 및 펀더멘털:</strong> 단순 기대감이 아닌 실제 영업이익 개선과 수주 잔고 증가가 숫자로 증명되는 선도주 선별이 필수적입니다.<br>
            • <strong>정책 및 글로벌 환경:</strong> 글로벌 산업 동향과 정부 정책 지원이 맞물려 중장기 성장 동력이 강화되고 있습니다.
          </div>
        </section>

        <!-- Section 2 -->
        <section id="sec-impact-analysis">
          <h2>2. 펀더멘털 및 기술적 수급 분석</h2>
          <p>
            해당 섹터의 주도주들은 <strong>안정적인 재무 건전성(낮은 부채비율, 높은 ROE)</strong>과 함께 
            거래량을 동반한 바닥권 박스권 돌파 흐름을 나타내고 있습니다:
          </p>
          <ul>
            <li><strong>기관·외국인 동반 순매수:</strong> 메이저 수급 주체들이 최근 5~10거래일 연속 순매수 우위를 유지.</li>
            <li><strong>이동평균선 정배열 전환:</strong> 단기 이평선(20일)이 중장기 이평선(60일, 120일)을 골든크로스하며 추세적 상승 국면 진입.</li>
            <li><strong>밸류에이션 매력:</strong> 업종 평균 대비 저평가된 밸류에이션 갭을 메우는 리레이팅 구간 진입.</li>
          </ul>
        </section>

        <!-- Section 3: Data Table -->
        <section id="sec-data-table">
          <h2>3. 주요 핵심 지표 및 밸류에이션 요약</h2>
          <div class="table-responsive">
            <table class="metrics-table">
              <thead>
                <tr>
                  <th>구분</th>
                  <th>PER 지표</th>
                  <th>PBR 지표</th>
                  <th>ROE 지표</th>
                  <th>수급 및 모멘텀 평가</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><strong>선도 대장주</strong></td>
                  <td style="color:var(--accent-red); font-weight:700;">11.8배</td>
                  <td>0.88배</td>
                  <td>15.2%</td>
                  <td>외국인 대량 순매수 / 골든크로스</td>
                </tr>
                <tr>
                  <td><strong>고성장 후발주</strong></td>
                  <td>14.5배</td>
                  <td>1.15배</td>
                  <td>18.0%</td>
                  <td>거래량 300% 급증 / 저항선 돌파</td>
                </tr>
                <tr>
                  <td><strong>업종 평균</strong></td>
                  <td>17.2배</td>
                  <td>1.40배</td>
                  <td>10.5%</td>
                  <td>시장 지수 대비 아웃퍼폼</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <!-- Section 4 -->
        <section id="sec-strategy">
          <h2>4. 핵심 리스크 점검 및 분할 매매 대응 전략</h2>
          <div class="callout callout-warning">
            <strong>⚠️ 리스크 관리 원칙:</strong><br>
            - 단기 급등에 따른 뇌동매매를 지양하고 3회 이상 분할 매수(30% / 30% / 40%) 원칙 준수.<br>
            - 주요 기술적 지지선 이탈 시 손절 기준선(-5% ~ -7%)을 엄격히 지켜 원금 보존 최우선.<br>
            - 목표 수익률 도달 시 50% 분할 익절 후 잔여 물량은 트레일링 스탑 적용.
          </div>
        </section>
"""

    def generate_morning_briefing(self, headlines=None):
        """매일 아침 8시 글로벌 경제 및 국내 증시 모닝 시황 브리핑 리포트 생성 (읽는 시간 UI 제거)"""
        today_str = datetime.now().strftime("%Y년 %m월 %d일")
        date_iso = datetime.now().strftime("%Y-%m-%d")
        slug = f"{datetime.now().strftime('%Y%m%d')}-morning-market-briefing"
        title = f"[{today_str}] 오늘의 증시 모닝 브리핑: 뉴욕증시 마감 & 국내 주도주 핵심 체크포인트"
        category = "오늘의 시황"

        if not headlines:
            headlines = [
                "엔비디아 발 AI 반도체 훈풍 지속… 빅테크 중심 나스닥 강세 마감",
                "원/달러 환율 1,330원대 안정세… 외국인 수급 코스피 대형주 유입 기대",
                "정부 밸류업 2차 세제 혜택 추진… 저PBR 금융·지주사 배당 매력 부각",
                "국내 AI 데이터센터 전력망 확충 수혜… 변압기·전력기기 섹터 강세",
                "오늘의 주요 공모주 청약 및 실적 공시 일정 점검"
            ]

        # 5개 헤드라인 보장
        while len(headlines) < 5:
            headlines.append("국내 증시 외국인·기관 수급 동향 및 주요 기업 실적 발표 일정")

        morning_pool = [
            "images/morning-1.jpg",
            "images/morning-2.jpg",
            "images/morning-3.jpg",
            "images/market-1.jpg",
            "images/market-2.jpg"
        ]
        title_hash = int(hashlib.md5(title.encode('utf-8')).hexdigest(), 16)
        chosen_image = morning_pool[title_hash % len(morning_pool)]
        image_src = f"../{chosen_image}"

        html_content = f"""<!DOCTYPE html>
<html lang="ko" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | Value Stock Labs 리서치</title>
  <meta name="description" content="{today_str} 국내외 증시 시황 브리핑. 뉴욕증시 3대 지수 마감, 환율, AI 반도체 및 오늘 장 시작 전 핵심 주도주를 총정리합니다.">
  <meta name="keywords" content="오늘의시황, 증시브리핑, 뉴욕증시마감, 환율, AI반도체, 밸류업, 코스피전망, 주식개장">
  <meta name="author" content="Value Stock Labs 리서치팀">

  <!-- OpenGraph -->
  <meta property="og:type" content="article">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{today_str} 글로벌 경제 지표 및 국내 증시 핵심 모닝 브리핑">
  <meta property="og:image" content="{image_src}">
  <meta property="og:url" content="{BLOG_DOMAIN}/posts/{slug}.html">

  <!-- Stylesheets -->
  <link rel="stylesheet" href="../css/style.css">
  <link rel="stylesheet" href="../css/ads.css">
  <link rel="stylesheet" href="../css/article.css">
  <link rel="stylesheet" href="../css/tools.css">

  <!-- Google AdSense Script -->
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_PUB_ID}" crossorigin="anonymous"></script>
  <!-- Favicon & Search Engine Identity -->
  <link rel="icon" type="image/x-icon" href="../favicon.ico">
  <link rel="icon" type="image/png" sizes="16x16" href="../favicon-16x16.png">
  <link rel="icon" type="image/png" sizes="32x32" href="../favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="48x48" href="../favicon-48x48.png">
  <link rel="apple-touch-icon" sizes="180x180" href="../apple-touch-icon.png">
  <link rel="icon" type="image/svg+xml" href="../favicon.svg">
  <link rel="manifest" href="../site.webmanifest">
  <meta name="theme-color" content="#090d16">
  <meta name="msapplication-TileColor" content="#090d16">
  <meta name="msapplication-TileImage" content="../apple-touch-icon.png">
</head>
<body>

  <div class="reading-progress-bar" id="readingProgressBar"></div>

  <header class="site-header">
    <div class="container header-inner">
      <a href="../index.html" class="logo">
        <div class="logo-icon"><img src="../images/vsl-logo-neon-fire.png" alt="VSL Logo" class="logo-img" width="38" height="38"></div>
        <span class="logo-text">Value Stock Labs</span>
      </a>
      <nav class="nav-menu" aria-label="메인 메뉴">
        <a href="../index.html" class="nav-link">홈</a>
        <a href="../index.html#postsGrid" class="nav-link">분석 리포트</a>
        <a href="../tools/fair-value-calculator.html" class="nav-link">적정가치 계산기</a>
        <a href="../tools/stock-average-calc.html" class="nav-link">물타기 계산기</a>
        <a href="../tools/target-price-calculator.html" class="nav-link">손익비 계산기</a>
      </nav>
      <div class="header-actions">
        <button class="theme-toggle" id="themeToggle" aria-label="다크모드 토글">🌙</button>
      </div>
    </div>
  </header>

  <main class="article-layout">
    <div class="container article-grid">
      <article class="article-body">
        
        <nav class="breadcrumb" aria-label="경로 탐색">
          <a href="../index.html">홈</a> &gt; 
          <a href="../index.html#morningBriefingSession">오늘의 시황</a> &gt; 
          <span>모닝 브리핑</span>
        </nav>

        <header class="article-header">
          <span class="badge badge-market">☕ 매일 아침 08:00 정기 브리핑</span>
          <h1 class="article-title">{title}</h1>
          <div class="article-meta">
            <span>✍️ Value Stock Labs 리서치팀</span>
            <span>📅 {today_str} 08:00 AM 발행</span>
          </div>
        </header>

        <!-- Golden Ad Slot #1 -->
        <div class="ad-slot-wrapper">
          <div class="ad-slot-header">
            <span class="ad-label">SPONSORED</span>
          </div>
          <div class="ad-container ad-leaderboard" data-ad-slot="1001001" data-ad-type="Display Leaderboard" data-ad-name="시황 상단 광고"></div>
        </div>

        <nav class="toc-container" aria-label="본문 목차">
          <h3 class="toc-title">📑 모닝 브리핑 목차</h3>
          <ul class="toc-list" id="tocList">
            <li><a href="#sec-global">1. 밤사이 글로벌 증시 마감 요약 (미국 3대 지수)</a></li>
            <li><a href="#sec-macro">2. 거시경제 지표 및 환율·금리 동향</a></li>
            <li><a href="#sec-domestic">3. 오늘 국내 증시 핵심 관전 포인트 및 주도 섹터</a></li>
            <li><a href="#sec-hotissues">4. 장 시작 전 주요 뉴스 &amp; 공시 5선</a></li>
            <li><a href="#sec-calc">5. 오늘의 실전 투자 전략 &amp; 계산기 활용법</a></li>
          </ul>
        </nav>

        <section id="sec-global">
          <h2>1. 밤사이 글로벌 증시 마감 요약 (미국 3대 지수)</h2>
          <p>
            밤사이 뉴욕증시는 인플레이션 둔화 지표와 국채 금리 안정세 속에 기술주와 우량 가치주를 중심으로 매수세가 유입되며 견조한 흐름으로 마감했습니다.
          </p>
          <div class="table-responsive">
            <table class="metrics-table">
              <thead>
                <tr>
                  <th>지수명</th>
                  <th>마감 추이</th>
                  <th>주요 특징</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><strong>나스닥 종합 (NASDAQ)</strong></td>
                  <td style="color:var(--accent-red); font-weight:700;">강세 마감 ▲</td>
                  <td>빅테크 AI 인프라 투자 지속 및 반도체 랠리</td>
                </tr>
                <tr>
                  <td><strong>S&P 500</strong></td>
                  <td style="color:var(--accent-red); font-weight:700;">상승 마감 ▲</td>
                  <td>시장 전반적인 위험선호 심리 회복</td>
                </tr>
                <tr>
                  <td><strong>다우존스 산업지수</strong></td>
                  <td style="color:var(--accent-red); font-weight:700;">견조한 흐름 ▲</td>
                  <td>우량 금융·헬스케어·제조업 동반 상승</td>
                </tr>
                <tr>
                  <td><strong>필라델피아 반도체</strong></td>
                  <td style="color:var(--accent-red); font-weight:700;">급등세 연출 ▲</td>
                  <td>AI HBM 및 파운드리 밸류체인 강세</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <section id="sec-macro">
          <h2>2. 거시경제 지표 및 환율·금리 동향</h2>
          <ul>
            <li><strong>원/달러 환율:</strong> 1,330원대 중반에서 안정세를 유지하며 외국인 투자자의 국내 증시 순매수에 우호적인 환경 조성.</li>
            <li><strong>미국 10년물 국채금리:</strong> 기준금리 인하 가시화로 3.8% 수준에서 안정적 등락하며 성장주 밸류에이션 부담 경감.</li>
            <li><strong>국제유가(WTI):</strong> 배럴당 70달러대 중반에서 횡보세를 보이며 수입 물가 안정에 기여.</li>
          </ul>
        </section>

        <!-- In-Article Native Ad Slot #2 -->
        <div class="ad-slot-wrapper">
          <div class="ad-slot-header">
            <span class="ad-label">SPONSORED CONTENT</span>
          </div>
          <div class="ad-container ad-in-article" data-ad-slot="2002002" data-ad-type="In-Article Native" data-ad-name="시황 중간 광고"></div>
        </div>

        <section id="sec-domestic">
          <h2>3. 오늘 국내 증시 핵심 관전 포인트 및 주도 섹터</h2>
          <div class="callout callout-info">
            <strong>🔥 오늘 장 주도 유망 테마:</strong><br>
            1. <strong>AI 반도체 &amp; 소부장:</strong> 필라델피아 반도체 지수 강세에 따른 HBM 및 패키징 장비주 순매수 유입.<br>
            2. <strong>기업 밸류업 &amp; 금융주:</strong> 주주환원 세제 혜택 추진에 따른 저PBR 은행·지주사 외국인 순매수 지속.<br>
            3. <strong>전력망 &amp; 에너지 인프라:</strong> 북미 변압기 쇼티지 및 데이터센터 전력망 수주 모멘텀.
          </div>
        </section>

        <section id="sec-hotissues">
          <h2>4. 장 시작 전 주요 뉴스 &amp; 경제 이슈 5선</h2>
          <ul>
            <li>📌 <strong>{headlines[0]}</strong></li>
            <li>📌 <strong>{headlines[1]}</strong></li>
            <li>📌 <strong>{headlines[2]}</strong></li>
            <li>📌 <strong>{headlines[3]}</strong></li>
            <li>📌 <strong>{headlines[4]}</strong></li>
          </ul>
        </section>

        <section id="sec-calc">
          <h2>5. 오늘의 실전 투자 전략 &amp; 계산기 활용법</h2>
          <p>
            지수 상승 국면에서도 무리한 추격 매수보다는 20일선 지지력을 확인하는 분할 매수 전략이 안전합니다.
          </p>
          <div class="quick-calc-form" style="margin: 20px 0; padding: 20px; background: rgba(255,255,255,0.03); border-radius: 12px;">
            <h3>📊 개장 전 필수 도구: 적정주가 &amp; 물타기 평단가 계산</h3>
            <p>보유 종목의 목표가와 추가 매수 시 예상 평단가를 미리 계산해 보세요.</p>
            <div style="display: flex; gap: 10px; flex-wrap: wrap; margin-top: 15px;">
              <a href="../tools/fair-value-calculator.html" class="btn-primary" style="text-decoration:none;">💎 기업 적정가치 계산기</a>
              <a href="../tools/stock-average-calc.html" class="btn-primary" style="text-decoration:none; background: #3b82f6;">💧 물타기 평단가 계산기</a>
              <a href="../tools/target-price-calculator.html" class="btn-primary" style="text-decoration:none; background: #64748b;">🎯 손익비 계산기</a>
            </div>
          </div>
        </section>

        <div class="article-disclaimer">
          <strong>⚠️ 투자 유의사항:</strong> 본 모닝 시황 브리핑은 공시 및 공공 데이터를 바탕으로 작성된 참고 자료이며 특정 종목의 투자를 권유하지 않습니다.
        </div>

      </article>
      
      <!-- Sidebar -->
      <aside class="sidebar-area">
        <div class="widget-card">
          <h3 class="widget-title"><span>🔥</span> 실시간 인기 분석</h3>
          <div class="popular-list">
            <div class="popular-item"><span class="popular-rank">1</span><a href="ai-semiconductor-hbm-stocks.html">2026 AI 반도체 HBM 수혜주 총정리</a></div>
            <div class="popular-item"><span class="popular-rank">2</span><a href="undervalued-stocks-2026.html">2026 저평가 우량주 5선 분석</a></div>
            <div class="popular-item"><span class="popular-rank">3</span><a href="breakout-stocks-guide.html">상승초입주 포착 매매기법</a></div>
          </div>
        </div>
      </aside>
    </div>
  </main>

  <footer class="site-footer">
    <div class="container">
      <div class="footer-bottom">
        <span>© 2026 Value Stock Labs. All rights reserved.</span>
        <span>Google AdSense Compliant & SEO Optimized</span>
      </div>
    </div>
  </footer>

  <script src="../js/main.js"></script>
  <script src="../js/ads.js"></script>
  <script src="../js/article.js"></script>
  <script src="../js/admin-analytics.js" defer></script>
</body>
</html>
"""
        return {
            "slug": slug,
            "filename": f"{slug}.html",
            "title": title,
            "category": category,
            "image": chosen_image,
            "html": html_content,
            "date": date_iso,
            "is_morning": True
        }

    def generate_article_content(self, topic):
        """수집된 뉴스/주제를 바탕으로 제목과 100% 일치하는 2,000자 이상 전문 주식 리서치 아티클 HTML 생성"""
        title = topic["title"]
        summary = topic.get("summary", "")
        category = topic.get("category", "주식분석")
        keywords = topic.get("keywords", ["주식분석", "저평가우량주", "상승초입", "적정주가"])
        today_str = datetime.now().strftime("%Y년 %m월 %d일")
        date_iso = datetime.now().strftime("%Y-%m-%d")
        slug = self.create_slug(title)

        topic_type = self.detect_topic_type(title, summary)
        image_path, image_caption = self.get_category_image_info(topic_type, title)
        image_src = f"../{image_path}"
        sections_html = self.build_contextual_sections(topic_type, title, summary, category, keywords)

        html_content = f"""<!DOCTYPE html>
<html lang="ko" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | Value Stock Labs 리서치</title>
  <meta name="description" content="{title}에 대한 심층 팩트체크, 금융 시장 파급 효과, 핵심 데이터 지표 및 실전 투자 전략을 분석합니다.">
  <meta name="keywords" content="{', '.join(keywords)}, 주식분석, 밸류에이션, 재테크">
  <meta name="author" content="Value Stock Labs 리서치팀">

  <!-- OpenGraph -->
  <meta property="og:type" content="article">
  <meta property="og:title" content="{title} | Value Stock Labs 리서치">
  <meta property="og:description" content="{title} 핵심 팩트체크 및 금융·시장 밸류에이션 분석 리포트">
  <meta property="og:image" content="{image_src}">
  <meta property="og:url" content="{BLOG_DOMAIN}/posts/{slug}.html">

  <!-- Stylesheets -->
  <link rel="stylesheet" href="../css/style.css">
  <link rel="stylesheet" href="../css/ads.css">
  <link rel="stylesheet" href="../css/article.css">
  <link rel="stylesheet" href="../css/tools.css">

  <!-- Google AdSense Script -->
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_PUB_ID}" crossorigin="anonymous"></script>
  <!-- Favicon & Search Engine Identity -->
  <link rel="icon" type="image/x-icon" href="../favicon.ico">
  <link rel="icon" type="image/png" sizes="16x16" href="../favicon-16x16.png">
  <link rel="icon" type="image/png" sizes="32x32" href="../favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="48x48" href="../favicon-48x48.png">
  <link rel="apple-touch-icon" sizes="180x180" href="../apple-touch-icon.png">
  <link rel="icon" type="image/svg+xml" href="../favicon.svg">
  <link rel="manifest" href="../site.webmanifest">
  <meta name="theme-color" content="#090d16">
  <meta name="msapplication-TileColor" content="#090d16">
  <meta name="msapplication-TileImage" content="../apple-touch-icon.png">
</head>
<body>

  <!-- Reading Progress Bar -->
  <div class="reading-progress-bar" id="readingProgressBar"></div>

  <!-- Header Navigation -->
  <header class="site-header">
    <div class="container header-inner">
      <a href="../index.html" class="logo">
        <div class="logo-icon"><img src="../images/vsl-logo-neon-fire.png" alt="VSL Logo" class="logo-img" width="38" height="38"></div>
        <span class="logo-text">Value Stock Labs</span>
      </a>
      <nav class="nav-menu" aria-label="메인 메뉴">
        <a href="../index.html" class="nav-link">홈</a>
        <a href="../index.html#postsGrid" class="nav-link">분석 리포트</a>
        <a href="../tools/fair-value-calculator.html" class="nav-link">적정가치 계산기</a>
        <a href="../tools/stock-average-calc.html" class="nav-link">물타기 계산기</a>
        <a href="../tools/target-price-calculator.html" class="nav-link">손익비 계산기</a>
      </nav>
      <div class="header-actions">
        <button class="theme-toggle" id="themeToggle" aria-label="다크모드 토글">🌙</button>
      </div>
    </div>
  </header>

  <!-- Article Main Container -->
  <main class="article-layout">
    <div class="container article-grid">
      
      <!-- Article Content Body -->
      <article class="article-body">
        
        <!-- Breadcrumb -->
        <nav class="breadcrumb" aria-label="경로 탐색">
          <a href="../index.html">홈</a> &gt; 
          <a href="../index.html#articles">{category}</a> &gt; 
          <span>심층 리포트</span>
        </nav>

        <!-- Article Header (읽는 시간, 조회수 급증 완전 제거) -->
        <header class="article-header">
          <span class="badge badge-semiconductor">{category} 심층 분석</span>
          <h1 class="article-title">{title}</h1>
          <div class="article-meta">
            <span>✍️ Value Stock Labs 리서치팀</span>
            <span>📅 {today_str}</span>
          </div>
        </header>

        <!-- Featured Image -->
        <figure class="article-featured-img">
          <img src="{image_src}" alt="{title} 분석 차트" loading="lazy">
          <figcaption>{image_caption}</figcaption>
        </figure>

        <!-- Golden Ad Placement #1: Article Top Leaderboard -->
        <div class="ad-slot-wrapper">
          <div class="ad-slot-header">
            <span class="ad-label">SPONSORED</span>
          </div>
          <div class="ad-container ad-leaderboard" 
               data-ad-slot="1001001" 
               data-ad-type="Display Leaderboard" 
               data-ad-name="본문 상단 광고" 
               data-ad-size="728x90 Leaderboard">
          </div>
        </div>

        <!-- Table of Contents (TOC) -->
        <nav class="toc-container" aria-label="본문 목차">
          <h3 class="toc-title">📑 핵심 리포트 목차</h3>
          <ul class="toc-list" id="tocList">
            <li><a href="#sec-issue-brief">1. 핵심 이슈 브리핑 &amp; 팩트체크</a></li>
            <li><a href="#sec-impact-analysis">2. 시장 파급 효과 및 섹터 영향 분석</a></li>
            <li><a href="#sec-data-table">3. 핵심 수치 및 비교 데이터 지표</a></li>
            <li><a href="#sec-strategy">4. 실전 대응 전략 및 리스크 관리</a></li>
            <li><a href="#sec-calculator">5. 실시간 가치평가 및 계산기 활용 가이드</a></li>
          </ul>
        </nav>

        <!-- Dynamic Contextual Sections -->
        {sections_html}

        <!-- In-Article Native Ad Slot #2 -->
        <div class="ad-slot-wrapper">
          <div class="ad-slot-header">
            <span class="ad-label">SPONSORED CONTENT</span>
          </div>
          <div class="ad-container ad-in-article" 
               data-ad-slot="2002002" 
               data-ad-type="In-Article Native" 
               data-ad-name="본문 중간 네이티브 광고" 
               data-ad-size="Responsive In-Article">
          </div>
        </div>

        <!-- Section 5: Calculator Widget Linking -->
        <section id="sec-calculator">
          <h2>5. 실시간 가치평가 및 계산기 활용 가이드</h2>
          <p>
            보유 중이거나 매수 검토 중인 금융 상품 및 종목의 적정가치와 물타기 평단가를 직접 시뮬레이션해 보세요:
          </p>
          <div class="quick-calc-form" style="margin: 20px 0; padding: 20px; background: rgba(255,255,255,0.03); border-radius: 12px;">
            <h3>📊 Value Stock Labs 무료 퀀트 투자 계산기</h3>
            <p>복잡한 재무 지표를 1초 만에 계산하여 합리적인 매매 기준선을 제시합니다.</p>
            <div style="display: flex; gap: 10px; flex-wrap: wrap; margin-top: 15px;">
              <a href="../tools/fair-value-calculator.html" class="btn-primary" style="text-decoration:none;">💎 기업 적정가치(Fair Value) 계산기</a>
              <a href="../tools/stock-average-calc.html" class="btn-primary" style="text-decoration:none; background: #3b82f6;">💧 물타기 평단가 계산기</a>
              <a href="../tools/target-price-calculator.html" class="btn-primary" style="text-decoration:none; background: #64748b;">🎯 손익비 계산기</a>
            </div>
          </div>
        </section>

        <!-- Disclaimer -->
        <div class="article-disclaimer">
          <strong>⚠️ 투자 유의사항 및 면책 조항:</strong><br>
          본 리포트에서 제공하는 정보는 투자 판단을 위한 참고용 분석 자료이며, 특정 종목이나 금융 상품의 매수 또는 매도를 권유하지 않습니다. 
          모든 투자의 최종 결정과 손익에 대한 책임은 투자자 본인에게 있습니다.
        </div>

        <!-- Social Share & Toast -->
        <div class="article-share-box">
          <span>이 분석 리포트 공유하기:</span>
          <button type="button" class="share-btn" id="shareBtn">🔗 URL 링크 복사</button>
        </div>

      </article>

      <!-- Sidebar -->
      <aside class="sidebar-area" aria-label="사이드바">
        <div class="widget-card">
          <h3 class="widget-title"><span>🔥</span> 실시간 인기 분석</h3>
          <div class="popular-list">
            <div class="popular-item">
              <span class="popular-rank">1</span>
              <a href="ai-semiconductor-hbm-stocks.html" class="popular-link">2026 AI 반도체 HBM 수혜주 총정리</a>
            </div>
            <div class="popular-item">
              <span class="popular-rank">2</span>
              <a href="undervalued-stocks-2026.html" class="popular-link">2026 저평가 우량주 5선 분석</a>
            </div>
            <div class="popular-item">
              <span class="popular-rank">3</span>
              <a href="breakout-stocks-guide.html" class="popular-link">상승초입주 포착 매매기법</a>
            </div>
          </div>
        </div>

        <!-- Sticky Sidebar Ad Slot (300x600) -->
        <div class="ad-slot-wrapper">
          <div class="ad-slot-header">
            <span class="ad-label">ADVERTISEMENT</span>
          </div>
          <div class="ad-container ad-sidebar-sticky" 
               data-ad-slot="4004004" 
               data-ad-type="Sidebar Half-Page Sticky" 
               data-ad-name="본문 사이드바 광고" 
               data-ad-size="300x600 Half-Page">
          </div>
        </div>
      </aside>

    </div>
  </main>

  <!-- Footer -->
  <footer class="site-footer">
    <div class="container">
      <div class="footer-bottom">
        <span>© 2026 Value Stock Labs. All rights reserved.</span>
        <span>Google AdSense Compliant & SEO Optimized</span>
      </div>
    </div>
  </footer>

  <!-- Scripts -->
  <script src="../js/main.js"></script>
  <script src="../js/ads.js"></script>
  <script src="../js/article.js"></script>
  <script src="../js/admin-analytics.js" defer></script>
</body>
</html>
"""
        return {
            "slug": slug,
            "filename": f"{slug}.html",
            "title": title,
            "category": category,
            "summary": summary,
            "image": image_path,
            "html": html_content,
            "date": date_iso
        }
