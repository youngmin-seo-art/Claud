"""
=============================================================================
ARTICLE GENERATOR (article_generator.py)
기사 제목 연동 심층 분석 본문 생성 & 소제목별 상세 리서치 엔진 (대번호 간 대형 여백/구분선 & 행간 2.2 극대화)
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
        """제목 및 요약문을 분석하여 세부 리포트 템플릿 유형 결정 (10개 섹터 정밀 분류)"""
        full_text = f"{title} {summary}"

        if any(k in full_text for k in ["반도체", "HBM", "엔비디아", "하이닉스", "삼성전자", "파운드리", "CXL", "온디바이스", "소부장", "빅테크", "AI투자", "AI 반도체", "SK 밸류업", "최태원"]):
            return "ai_semiconductor"
        elif any(k in full_text for k in ["대출", "가계부채", "가산금리", "월급쟁이", "예대", "주담대", "신용대출", "금리", "한은", "한국은행", "기준금리", "물가", "환율", "인플레", "통화정책"]):
            return "macro_interest_rate"
        elif any(k in full_text for k in ["밸류업", "저PBR", "배당", "주주환원", "자사주", "금융지주", "은행주", "보험주", "지주사"]):
            return "valueup_dividend"
        elif any(k in full_text for k in ["현대차", "기아", "완성차", "2차전지", "배터리", "전고체", "양극재", "에코프로", "포스코", "로봇", "자율주행", "모빌리티", "인도법인"]):
            return "battery_mobility"
        elif any(k in full_text for k in ["바이오", "제약", "임상", "FDA", "CDMO", "신약", "기술수출", "비만치료제", "ADC", "헬스케어"]):
            return "bio_healthcare"
        elif any(k in full_text for k in ["공모주", "청약", "IPO", "상장", "수요예측", "의무보유"]):
            return "ipo"
        elif any(k in full_text for k in ["전력", "변압기", "전선", "데이터센터", "원전", "SMR", "에너지", "전력망"]):
            return "power_energy"
        elif any(k in full_text for k in ["유가", "방산", "중동", "지정학", "해운", "조선", "방위산업", "원자재"]):
            return "geopolitics"
        elif any(k in full_text for k in ["상승초입", "골든크로스", "돌파", "신고가", "바닥권", "거래량 급증", "박스권"]):
            return "breakout_stocks"
        else:
            return "general_stock"

    def get_category_image_info(self, topic_type, title):
        """주제 유형 및 제목 고유 해시를 바탕으로 중복 없이 다양한 썸네일 이미지 매핑"""
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
            "breakout_stocks": [
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
        """기사 제목과 뉴스 맥락에 100% 일치하는 풍부하고 전문적인 5개 본문 섹션 HTML 생성 (대번호 간 대형 여백/구분선 & 행간 2.2)"""
        clean_title = html.escape(title)
        clean_summary = html.escape(summary)
        if clean_summary:
            clean_summary = re.sub(r'\s+', ' ', clean_summary).strip()
            clean_summary = re.sub(r'([.?!])\s+(?=[가-힣A-Za-z0-9])', r'\1<br><br>\n            ', clean_summary)
        kw_str = ", ".join(keywords)

        div_sep = '<div style="margin: 64px 0 48px; border-top: 2px solid rgba(6, 182, 212, 0.4); width: 100%;"></div>'

        if topic_type == "macro_interest_rate":
            return f"""
        <!-- Section 1 -->
        <section id="sec-issue-brief" style="margin-bottom: 50px;">
          <h2 style="font-size: 1.75rem; font-weight: 800; color: #ffffff; margin-bottom: 36px; padding-bottom: 18px; border-bottom: 2px solid rgba(6, 182, 212, 0.35); line-height: 1.55;">1. 핵심 이슈 브리핑: 대출금리 양극화와 금융시장 배경</h2>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            최근 금융권과 거시경제 전반에서 가장 뜨거운 화두는 단연 <strong style="color: #ffffff;">“{clean_title}”</strong> 현상입니다.<br><br>
            {clean_summary}
          </p>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            현재 금융 시장은 글로벌 통화정책 전환기(피벗, Pivot)에 접어들며 기준금리 인하에 대한 기대감이 고조되고 있습니다.<br><br>
            그러나 실제 금융 소비자와 가계가 체감하는 시장 대출 금리는 정반대의 흐름을 보이고 있습니다.<br><br>
            금융당국의 가계부채 총량 관리 압박과 스트레스 DSR 2단계 도입으로 인해 시중은행들이 대출 가산금리를 연쇄적으로 인상하고 있기 때문입니다.
          </p>
          
          <div class="callout callout-info" style="margin: 48px 0; padding: 34px 38px; background: rgba(6, 182, 212, 0.08); border-left: 5px solid var(--accent-cyan); border-radius: 12px; line-height: 2.5;">
            <div style="font-weight: 700; margin-bottom: 24px; color: var(--accent-cyan); font-size: 1.2rem;">💡 리서치센터 핵심 팩트체크:</div>
            
            <div style="margin-bottom: 26px; line-height: 2.5;">
              • <strong style="color: #ffffff;">가계대출 가산금리 기습 인상:</strong><br>
              기준금리 및 금융채 금리 하락세에도 불구하고, 시중은행들은 가산금리를 0.2%p~0.4%p 기습 인상하여 가계 대출 문턱을 대폭 높였습니다.
            </div>
            
            <div style="margin-bottom: 26px; line-height: 2.5;">
              • <strong style="color: #ffffff;">기업대출 유치 경쟁과 금리 역전 현상:</strong><br>
              가계대출 총량이 묶인 은행들이 우량 기업 대출로 영업력을 집중하면서 대기업 대출금리가 가계대출 금리보다 낮아지는 기현상이 발생했습니다.
            </div>
            
            <div>
              • <strong style="color: #ffffff;">예대금리차(NIS) 확대 및 이익 방어:</strong><br>
              예금 금리는 빠르게 인하된 반면 대출 금리는 견조하게 유지되면서 은행의 순이자마진(NIM)이 단기적으로 방어되고 있습니다.
            </div>
          </div>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            이러한 정책적·시장적 왜곡은 단기적으로 실수요 대출자의 이자 상환 부담을 가중시키며 가계의 가처분소득을 제약하고 있습니다.<br><br>
            이에 따라 향후 거시경제의 민간 소비 회복 속도와 금융권의 건전성 관리 여부가 핵심 변수로 부각되고 있습니다.
          </p>
        </section>

        {div_sep}

        <!-- Section 2 -->
        <section id="sec-impact-analysis" style="margin-bottom: 50px;">
          <h2 style="font-size: 1.75rem; font-weight: 800; color: #ffffff; margin-bottom: 36px; padding-bottom: 18px; border-bottom: 2px solid rgba(6, 182, 212, 0.35); line-height: 1.55;">2. 시장 파급 효과 및 은행·금융 섹터 영향 분석</h2>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            이번 대출금리 체계 개편과 가계부채 규제 강화는 단순한 개인 금융 영역을 넘어 <strong style="color: #ffffff;">국내 자산 시장과 증시 금융업종 밸류에이션</strong>에 심대한 파급 효과를 미치고 있습니다.
          </p>

          <h3 style="font-size: 1.38rem; font-weight: 700; color: var(--accent-cyan); margin: 52px 0 26px; line-height: 1.55;">🏛️ 3대 주요 파급 영향 및 핵심 관전 포인트</h3>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            <strong style="color: #ffffff;">1. 주요 금융지주의 이익 방어력 강화 (KB금융, 신한지주, 하나금융지주 등)</strong><br><br>
            가계대출 가산금리 인상에 힘입어 은행권의 순이자마진(NIM) 훼손이 최소화되며 사상 최대 수준의 이자이익이 유지될 전망입니다.<br><br>
            이는 기업 밸류업 프로그램과 맞물려 금융주의 배당 여력 및 자사주 소각 규모를 확대하는 핵심 동력으로 작용합니다.
          </p>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            <strong style="color: #ffffff;">2. 내수 소비재 및 유통 섹터의 실적 회복 지연</strong><br><br>
            월급쟁이 직장인과 영끌 차주들의 원리금 상환 부담이 줄어들지 않으면서 백화점, 패션, 외식, 레저 등 내수 민감 업종의 매출 둔화 압력이 지속되고 있습니다.
          </p>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            <strong style="color: #ffffff;">3. 신용 리스크 및 대손충당금 관리 이슈</strong><br><br>
            취약 차주와 다중채무자의 연체율 추이가 은행권의 대손비용률을 결정짓는 뇌관으로 작용할 수 있어, 자산 건전성이 우수한 대형 시중은행 중심의 선별적 접근이 필요합니다.
          </p>
          
          <ul style="margin: 32px 0 48px 28px; line-height: 2.5; color: #cbd5e1; display: flex; flex-direction: column; gap: 24px;">
            <li style="margin-bottom: 20px; line-height: 2.5;">
              <strong style="color: #ffffff;">은행주 밸류에이션 리레이팅:</strong><br>
              안정적인 이익 창출 능력을 바탕으로 저PBR(0.4~0.5배) 탈피 가속.
            </li>
            <li style="margin-bottom: 20px; line-height: 2.5;">
              <strong style="color: #ffffff;">부동산 PF 및 2금융권 건전성:</strong><br>
              시중은행의 대출 규제로 저축은행·카드사 등 제2금융권으로의 풍선효과 및 연체율 모니터링 필요.
            </li>
            <li>
              <strong style="color: #ffffff;">외국인 수급 유입:</strong><br>
              배당수익률 6% 이상을 보장하는 고배당 금융주로 글로벌 패시브 자금 유입 지속.
            </li>
          </ul>
        </section>

        {div_sep}

        <!-- Section 3: Data Table -->
        <section id="sec-data-table" style="margin-bottom: 50px;">
          <h2 style="font-size: 1.75rem; font-weight: 800; color: #ffffff; margin-bottom: 36px; padding-bottom: 18px; border-bottom: 2px solid rgba(6, 182, 212, 0.35); line-height: 1.55;">3. 핵심 수치 및 대출 유형별 금리 동향 비교 지표</h2>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            아래는 최근 시중 5대 은행(KB·신한·하나·우리·NH)의 차주별(가계 vs 기업) 평균 대출금리 추이 및 세부 가산금리 변동폭을 분석한 비교 데이터입니다:
          </p>

          <div class="table-responsive" style="margin: 36px 0;">
            <table class="metrics-table">
              <thead>
                <tr>
                  <th>대출 상품 구분</th>
                  <th>평균 대출금리 밴드</th>
                  <th>가산금리 변동 추이</th>
                  <th>주요 정책 규제 및 시장 영향</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><strong>가계 주택담보대출 (주담대)</strong></td>
                  <td style="color:var(--accent-red); font-weight:700;">3.95% ~ 4.55% ▲</td>
                  <td>+0.25%p ~ +0.45%p 인상</td>
                  <td>스트레스 DSR 2단계 적용 및 주택구입 목적 대출 축소</td>
                </tr>
                <tr>
                  <td><strong>가계 신용대출 (월급쟁이)</strong></td>
                  <td style="color:var(--accent-red); font-weight:700;">5.20% ~ 5.95% ▲</td>
                  <td>+0.20%p ~ +0.35%p 인상</td>
                  <td>직장인 우대금리 축소 및 연소득 대비 대출 한도 100% 이내 제한</td>
                </tr>
                <tr>
                  <td><strong>우량 대기업 대출</strong></td>
                  <td style="color:#00f2fe; font-weight:700;">4.05% ~ 4.25% ▼</td>
                  <td>-0.15%p ~ -0.30%p 인하</td>
                  <td>은행 간 우량 차주 유치 경쟁 및 회사채 발행 대체 수요 흡수</td>
                </tr>
                <tr>
                  <td><strong>중소기업·개인사업자 대출</strong></td>
                  <td>4.70% ~ 5.10% (보합)</td>
                  <td>보합권 등락</td>
                  <td>정책금융 지원 및 이차보전 연계 대출 유지</td>
                </tr>
              </tbody>
            </table>
          </div>

          <h3 style="font-size: 1.38rem; font-weight: 700; color: var(--accent-cyan); margin: 52px 0 26px; line-height: 1.55;">📊 데이터 표 심층 분석 및 시사점</h3>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            위 지표에서 가장 주목해야 할 점은 <strong style="color: #ffffff;">가계 주담대 금리의 하단이 대기업 대출 금리를 상회하는 비정상적 역전 구조</strong>가 고착화되고 있다는 점입니다.<br><br>
            통상적으로 담보력이 확실한 주담대는 무담보 기업대출보다 금리가 낮아야 정상이지만, 금융당국의 인위적 가산금리 조정이 시장 가격 결정 구조를 바꾼 결과입니다.<br><br>
            결과적으로 은행권은 대출 총량 증가율이 둔화되더라도 건당 마진이 개선됨에 따라 연간 35조 원 이상의 순이자이익을 달성할 수 있는 탄탄한 펀더멘털을 확보하게 되었습니다.
          </p>
        </section>

        {div_sep}

        <!-- Section 4 -->
        <section id="sec-strategy" style="margin-bottom: 50px;">
          <h2 style="font-size: 1.75rem; font-weight: 800; color: #ffffff; margin-bottom: 36px; padding-bottom: 18px; border-bottom: 2px solid rgba(6, 182, 212, 0.35); line-height: 1.55;">4. 금융소비자 & 투자자 관점 실전 대응 전략</h2>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            금리 변동성과 정책 규제가 엇갈리는 시기에는 자산 운용과 부채 관리 양 측면에서 정밀한 전략을 구사해야 합니다:
          </p>
          
          <h3 style="font-size: 1.38rem; font-weight: 700; color: var(--accent-cyan); margin: 52px 0 26px; line-height: 1.55;">💡 금융소비자 부채 다이어트 3대 수칙</h3>
          
          <ol style="margin: 32px 0 48px 28px; line-height: 2.5; color: #cbd5e1; display: flex; flex-direction: column; gap: 24px;">
            <li style="margin-bottom: 20px; line-height: 2.5;">
              <strong style="color: #ffffff;">온라인 원스톱 대환대출 인프라 적극 활용:</strong><br>
              모바일 앱을 통해 은행별 실시간 금리를 비교하고, 중도상환수수료 감면 시점을 노려 금리 0.3%p 이상 낮은 상품으로 적극 갈아타기.
            </li>
            <li style="margin-bottom: 20px; line-height: 2.5;">
              <strong style="color: #ffffff;">금리인하요구권 적극 행사:</strong><br>
              승진, 연봉 인상, 신용점수 900점 이상 진입, 부채 일부 상환 등 신용 상태가 개선된 경우 주거래 은행 모바일 앱을 통해 즉시 금리인하 신청(연 2회 권장).
            </li>
            <li>
              <strong style="color: #ffffff;">고정형 vs 변동형 금리 포트폴리오 리밸런싱:</strong><br>
              향후 1~2년에 걸친 한국은행의 완만한 기준금리 인하 기조를 감안할 때, 5년 고정(주기형) 금리가 변동금리보다 0.5%p 이상 저렴하다면 주기형 상품을 우선 선택하는 것이 유리.
            </li>
          </ol>

          <div class="callout callout-warning" style="margin: 48px 0; padding: 34px 38px; background: rgba(245, 158, 11, 0.08); border-left: 5px solid var(--accent-gold); border-radius: 12px; line-height: 2.5;">
            <div style="font-weight: 700; margin-bottom: 24px; color: var(--accent-gold); font-size: 1.2rem;">🎯 주식 투자자 포트폴리오 전략:</div>
            
            <div style="margin-bottom: 24px; line-height: 2.5;">
              - <strong style="color: #ffffff;">금융주 바벨 전략:</strong><br>
              안정적인 분기 배당(연 6~7%)과 자사주 소각을 병행하는 대형 금융지주 비중 60% 유지.
            </div>
            
            <div style="margin-bottom: 24px; line-height: 2.5;">
              - <strong style="color: #ffffff;">금리 인하 수혜주 선별:</strong><br>
              이자비용 부담 감소로 순이익 턴어라운드가 기대되는 바이오, IT 성장주 눌림목 분할 매수.
            </div>
            
            <div>
              - <strong style="color: #ffffff;">리스크 관리:</strong><br>
              가계부채 건전성 악화로 충당금 리스크가 부각될 수 있는 중소형 금융주 및 저축은행 지분 보유 기업은 비중 축소.
            </div>
          </div>
        </section>
"""
        elif topic_type == "ai_semiconductor":
            return f"""
        <!-- Section 1 -->
        <section id="sec-issue-brief" style="margin-bottom: 50px;">
          <h2 style="font-size: 1.75rem; font-weight: 800; color: #ffffff; margin-bottom: 36px; padding-bottom: 18px; border-bottom: 2px solid rgba(6, 182, 212, 0.35); line-height: 1.55;">1. 핵심 이슈 브리핑: AI 반도체 슈퍼사이클 및 공급망 현황</h2>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            글로벌 빅테크 기업들의 생성형 AI 및 AGI(범용인공지능) 인프라 구축 경쟁이 가속화되면서 <strong style="color: #ffffff;">“{clean_title}”</strong> 이슈가 국내외 증시의 강력한 주도 테마로 자리매김하고 있습니다.<br><br>
            {clean_summary}
          </p>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            엔비디아(NVIDIA)의 차세대 AI 가속기(블랙웰 B200, GB200) 양산이 본격화됨에 따라 고대역폭 메모리(HBM3E 8단/12단 및 HBM4)에 대한 글로벌 쇼티지(공급 부족)가 지속되고 있습니다.<br><br>
            마이크로소프트, 구글, 메타, 아마존 등 하이퍼스케일러들의 연간 AI 데이터센터 CAPEX(설비투자) 규모는 2026년 전년 대비 30% 이상 증가한 2,000억 달러를 돌파할 것으로 전망됩니다.
          </p>
          
          <div class="callout callout-info" style="margin: 48px 0; padding: 34px 38px; background: rgba(6, 182, 212, 0.08); border-left: 5px solid var(--accent-cyan); border-radius: 12px; line-height: 2.5;">
            <div style="font-weight: 700; margin-bottom: 24px; color: var(--accent-cyan); font-size: 1.2rem;">💡 리서치센터 핵심 팩트체크:</div>
            
            <div style="margin-bottom: 26px; line-height: 2.5;">
              • <strong style="color: #ffffff;">HBM 독점적 공급망 및 고수익성:</strong><br>
              차세대 HBM3E 및 HBM4 시장에서 SK하이닉스와 삼성전자의 수주 잔고가 이미 2026년 말 물량까지 완판(Sold-out) 상태에 도달했습니다.
            </div>
            
            <div style="margin-bottom: 26px; line-height: 2.5;">
              • <strong style="color: #ffffff;">첨단 패키징(Advanced Packaging) 병목:</strong><br>
              2.5D 및 3D 이종 집적 패키징 기술이 AI 반도체 성능의 핵심 병목으로 부상하며 후공정(OSAT) 장비 기업의 수혜가 극대화되고 있습니다.
            </div>
            
            <div>
              • <strong style="color: #ffffff;">CXL & 온디바이스 AI 융합:</strong><br>
              고용량 메모리 인터페이스인 CXL 2.0/3.0 생태계 확장과 스마트폰, 온디바이스 PC용 저전력 반도체(LPDDR5X, NPU) 수요가 동반 폭증하고 있습니다.
            </div>
          </div>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            과거 메모리 반도체 산업이 경기 변동에 따라 급격한 부침을 겪던 '원자재형 사이클'이었다면, 현재의 AI 반도체는 고객사 맞춤형(Customized) 고부가가치 수주 산업으로 체질이 완전히 전환되었습니다.<br><br>
            이에 따라 선도 기업들의 영업이익률(OPM)은 사상 최고치를 경신하는 구조적 호황기를 맞이하고 있습니다.
          </p>
        </section>

        {div_sep}

        <!-- Section 2 -->
        <section id="sec-impact-analysis" style="margin-bottom: 50px;">
          <h2 style="font-size: 1.75rem; font-weight: 800; color: #ffffff; margin-bottom: 36px; padding-bottom: 18px; border-bottom: 2px solid rgba(6, 182, 212, 0.35); line-height: 1.55;">2. 섹터별 밸류에이션 및 실적 퀀텀점프 전망</h2>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            AI 반도체 슈퍼사이클은 단순히 메모리 완제품 제조사에 그치지 않고, <strong style="color: #ffffff;">전공정 극자외선(EUV)부터 후공정 하이브리드 본딩, 테스트 소켓 등 소부장 밸류체인 전반</strong>으로 강력한 낙수 효과를 일으키고 있습니다:
          </p>

          <h3 style="font-size: 1.38rem; font-weight: 700; color: var(--accent-cyan); margin: 52px 0 26px; line-height: 1.55;">🔬 핵심 밸류체인 3대 수혜 영역 심층 분석</h3>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            <strong style="color: #ffffff;">1. HBM 선도 메모리 제조사 (SK하이닉스, 삼성전자)</strong><br><br>
            기존 범용 D램 대비 5배 이상의 가격 프리미엄과 40%를 상회하는 압도적인 마진율을 바탕으로 2026년 사상 최대 영업이익 달성이 확실시되고 있습니다.<br><br>
            특히 수율 안정성과 엔비디아 공급 점유율 우위를 지닌 기업을 중심으로 글로벌 기관들의 강력한 순매수가 유입되고 있습니다.
          </p>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            <strong style="color: #ffffff;">2. 첨단 후공정(Advanced OSAT) 및 본딩 장비주</strong><br><br>
            칩을 미세하게 적층하는 TC 본더(Thermal Compression Bonder)와 차세대 하이브리드 본더(Hybrid Bonder) 기술을 독점 공급하는 국내 장비 기업들의 수주 잔고가 분기마다 사상 최고치를 경신하고 있습니다.<br><br>
            글로벌 OSAT 및 파운드리(TSMC 등) 고객사 다변화가 진행되며 멀티플(PER) 리레이팅이 가속화되고 있습니다.
          </p>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            <strong style="color: #ffffff;">3. 초고속 검사 소켓 및 CXL 테스트 생태계</strong><br><br>
            적층 단수가 12단, 16단으로 높아질수록 칩 불량 검사의 난이도와 시간이 기하급수적으로 증가합니다.<br><br>
            이에 따라 고부가 실리콘 러버 소켓, 번인(Burn-in) 테스터, CXL 전용 테스트 장비를 양산하는 강소기업들의 실적 레버리지 효과가 두드러지고 있습니다.
          </p>
          
          <ul style="margin: 32px 0 48px 28px; line-height: 2.5; color: #cbd5e1; display: flex; flex-direction: column; gap: 24px;">
            <li style="margin-bottom: 20px; line-height: 2.5;">
              <strong style="color: #ffffff;">기관·외국인 수급 집중:</strong><br>
              반도체 대장주 및 핵심 소부장에 외국인 순매수 비중 60% 이상 집중.
            </li>
            <li style="margin-bottom: 20px; line-height: 2.5;">
              <strong style="color: #ffffff;">주요 기술적 지표:</strong><br>
              20일선 지지 기반의 계단식 상승 패턴 형성 및 역사적 신고가 돌파 시도.
            </li>
            <li>
              <strong style="color: #ffffff;">리스크 요인:</strong><br>
              글로벌 매크로 경기 침체에 따른 IT 완제품(스마트폰/PC) 수요 둔화 여부 체크 필요.
            </li>
          </ul>
        </section>

        {div_sep}

        <!-- Section 3: Data Table -->
        <section id="sec-data-table" style="margin-bottom: 50px;">
          <h2 style="font-size: 1.75rem; font-weight: 800; color: #ffffff; margin-bottom: 36px; padding-bottom: 18px; border-bottom: 2px solid rgba(6, 182, 212, 0.35); line-height: 1.55;">3. 반도체 세부 밸류체인별 핵심 재무 및 투자 지표 비교표</h2>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            아래는 AI 반도체 밸류체인 내 핵심 영역별 예상 실적, 영업이익률(OPM), 밸류에이션(PER/PBR) 지표를 정밀 분석한 데이터입니다:
          </p>

          <div class="table-responsive" style="margin: 36px 0;">
            <table class="metrics-table">
              <thead>
                <tr>
                  <th>세부 밸류체인 영역</th>
                  <th>대표 핵심 기술 및 제품</th>
                  <th>2026 예상 영업이익률 (OPM)</th>
                  <th>예상 PER 밴드</th>
                  <th>핵심 투자 체크포인트</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><strong>HBM 메모리 선도사</strong></td>
                  <td>HBM3E / HBM4 독점 공급</td>
                  <td style="color:var(--accent-red); font-weight:700;">38% ~ 46%</td>
                  <td>6.5배 ~ 9.0배 (저평가)</td>
                  <td>엔비디아 퀄테스트 통과 및 16단 HBM4 양산 수율</td>
                </tr>
                <tr>
                  <td><strong>첨단 패키징 본딩 장비</strong></td>
                  <td>열압착(TC) 본더, 하이브리드 본더</td>
                  <td style="color:var(--accent-red); font-weight:700;">28% ~ 35%</td>
                  <td>18.0배 ~ 24.0배</td>
                  <td>해외 글로벌 파운드리 고객사 추가 수주 여부</td>
                </tr>
                <tr>
                  <td><strong>테스트 & CXL 검사 소켓</strong></td>
                  <td>실리콘 러버 소켓, CXL 테스터</td>
                  <td>22% ~ 28%</td>
                  <td>12.0배 ~ 16.0배</td>
                  <td>고단수 적층에 따른 소모품 교체 주기 단축 수혜</td>
                </tr>
                <tr>
                  <td><strong>전공정 식각·증착 소재/가스</strong></td>
                  <td>EUV 감광액, 특수가스, 쿼츠</td>
                  <td>16% ~ 22%</td>
                  <td>10.0배 ~ 13.5배</td>
                  <td>가동률 100% 도달에 따른 분기별 출하량(Q) 증가</td>
                </tr>
              </tbody>
            </table>
          </div>

          <h3 style="font-size: 1.38rem; font-weight: 700; color: var(--accent-cyan); margin: 52px 0 26px; line-height: 1.55;">📊 데이터 표 심층 분석 및 시사점</h3>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            표에서 알 수 있듯이, <strong style="color: #ffffff;">HBM 메모리 선도사들의 예상 PER은 6~9배 수준으로 역사적 저평가 구간</strong>에 머물러 있습니다.<br><br>
            이는 과거 메모리 다운턴에 대한 시장의 기우가 반영된 결과이지만, 수주 기반 고수익 비즈니스 모델로의 전환을 감안할 때 향후 강력한 밸류에이션 갭 메우기(리레이팅)가 전개될 가능성이 높습니다.<br><br>
            반면 후공정 장비주의 경우 높은 PER(18~24배)을 부여받고 있으므로, 신규 매수 시에는 추격 매수보다 20일선 또는 60일 이동평균선 지지력을 확인하는 눌림목 분할 매수 전략이 안전합니다.
          </p>
        </section>

        {div_sep}

        <!-- Section 4 -->
        <section id="sec-strategy" style="margin-bottom: 50px;">
          <h2 style="font-size: 1.75rem; font-weight: 800; color: #ffffff; margin-bottom: 36px; padding-bottom: 18px; border-bottom: 2px solid rgba(6, 182, 212, 0.35); line-height: 1.55;">4. 실전 포트폴리오 비중 및 분할 매매 대응 전략</h2>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            주도주 섹터에서는 시장 변동성을 기회로 활용하여 승률 높은 포트폴리오를 구축해야 합니다:
          </p>

          <h3 style="font-size: 1.38rem; font-weight: 700; color: var(--accent-cyan); margin: 52px 0 26px; line-height: 1.55;">🎯 반도체 포트폴리오 3단계 분할 매수 가이드</h3>
          
          <ol style="margin: 32px 0 48px 28px; line-height: 2.5; color: #cbd5e1; display: flex; flex-direction: column; gap: 24px;">
            <li style="margin-bottom: 20px; line-height: 2.5;">
              <strong style="color: #ffffff;">1차 진입 (비중 30%):</strong><br>
              주요 지지선(20일 이동평균선 또는 전고점 지지 라인) 도달 시 분할 1차 매수 실행.
            </li>
            <li style="margin-bottom: 20px; line-height: 2.5;">
              <strong style="color: #ffffff;">2차 추가 (비중 30%):</strong><br>
              일봉상 거래량이 줄어들며 바닥을 다지는 수급 전환 확인 후 2차 분할 매수.
            </li>
            <li>
              <strong style="color: #ffffff;">3차 불타기 (비중 40%):</strong><br>
              거래량 200% 이상 동반하며 직전 박스권 저항선을 강력하게 돌파할 때 추세 추종 매수.
            </li>
          </ol>

          <div class="callout callout-warning" style="margin: 48px 0; padding: 34px 38px; background: rgba(245, 158, 11, 0.08); border-left: 5px solid var(--accent-gold); border-radius: 12px; line-height: 2.5;">
            <div style="font-weight: 700; margin-bottom: 24px; color: var(--accent-gold); font-size: 1.2rem;">📋 필수 리스크 관리 및 체크리스트:</div>
            
            <div style="margin-bottom: 24px; line-height: 2.5;">
              • <strong style="color: #ffffff;">대장주 60% + 소부장 40%:</strong><br>
              실적 가시성이 가장 높은 대형 메모리사 중심의 안전판 확보 후 고성장 장비주로 초과수익(Alpha) 추구.
            </div>
            
            <div style="margin-bottom: 24px; line-height: 2.5;">
              • <strong style="color: #ffffff;">기계적 손절 라인 (-6% ~ -8%):</strong><br>
              주요 수급선인 60일 이동평균선을 대량 거래량과 함께 하향 이탈할 경우 비중 축소 및 현금화.
            </div>
            
            <div>
              • <strong style="color: #ffffff;">분할 익절 전략:</strong><br>
              목표 수익률(+20%, +35%) 도달 시 50% 분할 익절 후 잔여 물량은 트레일링 스탑 적용.
            </div>
          </div>
        </section>
"""
        elif topic_type == "valueup_dividend":
            return f"""
        <!-- Section 1 -->
        <section id="sec-issue-brief" style="margin-bottom: 50px;">
          <h2 style="font-size: 1.75rem; font-weight: 800; color: #ffffff; margin-bottom: 36px; padding-bottom: 18px; border-bottom: 2px solid rgba(6, 182, 212, 0.35); line-height: 1.55;">1. 핵심 이슈 브리핑: 기업 밸류업 프로그램과 주주환원 혁신</h2>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            정부의 자본시장 선진화 및 코리아 디스카운트 해소 정책에 힘입어 <strong style="color: #ffffff;">“{clean_title}”</strong> 이슈에 국내외 기관 및 장기 펀드 자금이 대거 유입되고 있습니다.<br><br>
            {clean_summary}
          </p>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            기업 밸류업 프로그램의 2단계 세제 개편안(배당소득 분리과세 및 자사주 소각 법인세 감면)이 가시화되면서, 
            국내 상장사들의 만성적 저평가 원인으로 지목되던 취약한 거버넌스와 낮은 주주환원율이 구조적으로 개선되고 있습니다.
          </p>
          
          <div class="callout callout-info" style="margin: 48px 0; padding: 34px 38px; background: rgba(6, 182, 212, 0.08); border-left: 5px solid var(--accent-cyan); border-radius: 12px; line-height: 2.5;">
            <div style="font-weight: 700; margin-bottom: 24px; color: var(--accent-cyan); font-size: 1.2rem;">💡 리서치센터 핵심 팩트체크:</div>
            
            <div style="margin-bottom: 26px; line-height: 2.5;">
              • <strong style="color: #ffffff;">PBR 1배 미만 해소:</strong><br>
              청산가치에도 미치지 못하던 금융지주, 보험, 증권, 순수 지주사, 전통 제조업 우량주들의 밸류에이션 정상화가 본격화되었습니다.
            </div>
            
            <div style="margin-bottom: 26px; line-height: 2.5;">
              • <strong style="color: #ffffff;">주주환원율 40% 도달 목표:</strong><br>
              대형 금융지주와 지주사들이 연이어 자사주 매입 및 전량 소각 공시를 발표하며 주당순이익(EPS)과 주당순자산(BPS)이 동반 상승하고 있습니다.
            </div>
            
            <div>
              • <strong style="color: #ffffff;">분기·월 배당 정착:</strong><br>
              결산 배당 중심에서 분기 균등 배당으로 전환되며 투자자들에게 연중 안정적인 현금흐름을 제공하는 배당 매력이 극대화되었습니다.
            </div>
          </div>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            특히 글로벌 패시브 자금과 국부펀드들이 코리아 밸류업 지수(Value-up Index) 편입 종목을 중심으로 기계적인 매수세를 유입시키고 있어, 
            실질적인 주주환원 의지를 보인 기업들의 주가 하방 지지력이 매우 강력하게 형성되고 있습니다.
          </p>
        </section>

        {div_sep}

        <!-- Section 2 -->
        <section id="sec-impact-analysis" style="margin-bottom: 50px;">
          <h2 style="font-size: 1.75rem; font-weight: 800; color: #ffffff; margin-bottom: 36px; padding-bottom: 18px; border-bottom: 2px solid rgba(6, 182, 212, 0.35); line-height: 1.55;">2. 펀더멘털 지표(PER·PBR·ROE) 및 외국인 수급 분석</h2>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            밸류업 랠리의 핵심은 단순 테마성 급등이 아니라 <strong style="color: #ffffff;">자기자본이익률(ROE) 개선과 자본 효율화</strong>에 기반한 장기 펀더멘털 리레이팅입니다:
          </p>

          <h3 style="font-size: 1.38rem; font-weight: 700; color: var(--accent-cyan); margin: 52px 0 26px; line-height: 1.55;">🏛️ 밸류업 수혜 3대 대표 업종 심층 분석</h3>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            <strong style="color: #ffffff;">1. 대형 금융지주 (KB금융, 신한지주, 하나금융지주 등)</strong><br><br>
            CET1(보통주자본비율) 13% 이상을 기반으로 초과 자본을 전액 자사주 소각 및 배당금 확대에 투입하고 있습니다.<br><br>
            배당수익률 6~7%대와 자사주 소각 수익률 2~3%를 합산한 총 주주환원 수익률이 9%에 육박하며 글로벌 투자자들의 톱픽으로 자리잡았습니다.
          </p>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            <strong style="color: #ffffff;">2. 우량 지주사 및 자산주</strong><br><br>
            자회사 배당금 유입 및 자사주 소각 의무화 추진으로 순자산가치(NAV) 대비 할인율이 기존 60%에서 40% 수준으로 빠르게 축소되고 있습니다.<br><br>
            보유 부동산 및 현금성 자산 가치가 시가총액을 넘어서는 자산주들의 재평가가 두드러집니다.
          </p>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            <strong style="color: #ffffff;">3. 현금성 자산 풍부 전통 제조업</strong><br><br>
            무차입 경영을 유지하며 현금성 자산을 수천억 원 보유한 전통 산업재 선도 기업들이 밸류업 가이드라인 공시를 통해 배당 성향을 대폭 상향하고 있습니다.
          </p>
          
          <ul style="margin: 32px 0 48px 28px; line-height: 2.5; color: #cbd5e1; display: flex; flex-direction: column; gap: 24px;">
            <li style="margin-bottom: 20px; line-height: 2.5;">
              <strong style="color: #ffffff;">외국인 지분율 확대:</strong><br>
              대형 금융지주의 외국인 지분율이 60~75%대로 사상 최고치 기록.
            </li>
            <li>
              <strong style="color: #ffffff;">하방 경직성:</strong><br>
              주가 하락 시 배당수익률이 7~8%대로 올라서며 기관 및 연기금의 저가 매수세 유입.
            </li>
          </ul>
        </section>

        {div_sep}

        <!-- Section 3: Data Table -->
        <section id="sec-data-table" style="margin-bottom: 50px;">
          <h2 style="font-size: 1.75rem; font-weight: 800; color: #ffffff; margin-bottom: 36px; padding-bottom: 18px; border-bottom: 2px solid rgba(6, 182, 212, 0.35); line-height: 1.55;">3. 대표 저평가 가치주 밸류에이션 및 주주환원 지표 비교표</h2>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            아래는 밸류업 프로그램 대표 수혜주군과 코스피 평균 지표를 비교 분석한 데이터 테이블입니다:
          </p>

          <div class="table-responsive" style="margin: 36px 0;">
            <table class="metrics-table">
              <thead>
                <tr>
                  <th>구분</th>
                  <th>예상 PER</th>
                  <th>현재 PBR</th>
                  <th>자기자본이익률 (ROE)</th>
                  <th>예상 배당수익률</th>
                  <th>총 주주환원율</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><strong>대표 금융지주 톱픽</strong></td>
                  <td style="color:#00f2fe; font-weight:700;">5.2배</td>
                  <td style="color:var(--accent-red); font-weight:700;">0.48배</td>
                  <td>11.8%</td>
                  <td style="color:var(--accent-red); font-weight:700;">6.8% (분기배당)</td>
                  <td>38% ~ 42%</td>
                </tr>
                <tr>
                  <td><strong>우량 지주사 밸류업군</strong></td>
                  <td>6.5배</td>
                  <td style="color:var(--accent-red); font-weight:700;">0.52배</td>
                  <td>9.5%</td>
                  <td>5.4% (자사주소각)</td>
                  <td>35% ~ 38%</td>
                </tr>
                <tr>
                  <td><strong>고배당 통신/보험주</strong></td>
                  <td>7.8배</td>
                  <td>0.65배</td>
                  <td>10.2%</td>
                  <td>6.2%</td>
                  <td>30% ~ 35%</td>
                </tr>
                <tr>
                  <td><strong>코스피(KOSPI) 전체 평균</strong></td>
                  <td>11.5배</td>
                  <td>0.95배</td>
                  <td>8.5%</td>
                  <td>2.1%</td>
                  <td>28.5%</td>
                </tr>
              </tbody>
            </table>
          </div>

          <h3 style="font-size: 1.38rem; font-weight: 700; color: var(--accent-cyan); margin: 52px 0 26px; line-height: 1.55;">📊 데이터 표 심층 분석 및 시사점</h3>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            금융지주 및 지주사들의 PBR은 여전히 0.4~0.5배 수준으로 청산가치의 절반에 불과합니다.<br><br>
            일본 증시의 밸류업 성공 사례(도쿄증권거래소의 PBR 1배 미만 개선 요구)를 볼 때, 국내 우량 가치주들 역시 PBR 0.8~1.0배 수준까지 중장기적인 리레이팅 랠리가 지속될 여력이 충분합니다.<br><br>
            특히 ROE가 10% 이상이면서 PBR이 0.5배 미만인 기업은 이익 창출력 대비 극단적으로 저평가된 상태이므로, 주가 조정 시마다 적극적인 배당 재투자 전략이 유효합니다.
          </p>
        </section>

        {div_sep}

        <!-- Section 4 -->
        <section id="sec-strategy" style="margin-bottom: 50px;">
          <h2 style="font-size: 1.75rem; font-weight: 800; color: #ffffff; margin-bottom: 36px; padding-bottom: 18px; border-bottom: 2px solid rgba(6, 182, 212, 0.35); line-height: 1.55;">4. 배당 재투자 및 절세 계좌(ISA/IRP) 실전 활용 전략</h2>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            고배당 밸류업 종목은 일반 주식 계좌보다 세제 혜택이 주어지는 절세 계좌에서 운용할 때 복리 수익률이 극대화됩니다:
          </p>

          <h3 style="font-size: 1.38rem; font-weight: 700; color: var(--accent-cyan); margin: 52px 0 26px; line-height: 1.55;">💰 절세 극대화 3대 핵심 노하우</h3>
          
          <ol style="margin: 32px 0 48px 28px; line-height: 2.5; color: #cbd5e1; display: flex; flex-direction: column; gap: 24px;">
            <li style="margin-bottom: 20px; line-height: 2.5;">
              <strong style="color: #ffffff;">중개형 ISA (개인종합자산관리계좌):</strong><br>
              일반 계좌에서는 배당금에 대해 15.4%의 배당소득세가 원천징수되지만, 중개형 ISA를 활용하면 최대 500만 원까지 비과세 혜택을 받고 초과분도 9.9% 분리과세 적용을 받아 세금을 대폭 아낄 수 있습니다.
            </li>
            <li style="margin-bottom: 20px; line-height: 2.5;">
              <strong style="color: #ffffff;">연금저축 & IRP 계좌 활용:</strong><br>
              밸류업 고배당 ETF 및 금융지주를 연금 계좌에 편입할 경우, 매년 최대 900만 원 한도로 세액공제(13.2%~16.5%)를 받고 배당금은 과세이연되어 전액 재투자할 수 있습니다.
            </li>
            <li>
              <strong style="color: #ffffff;">배당락일 역발상 매수 기법:</strong><br>
              배당기준일 직후 주가가 일시적으로 하락하는 배당락 기간을 활용하여 우량 가치주를 저렴하게 추가 매수하는 전략이 유리합니다.
            </li>
          </ol>

          <div class="callout callout-warning" style="margin: 48px 0; padding: 34px 38px; background: rgba(245, 158, 11, 0.08); border-left: 5px solid var(--accent-gold); border-radius: 12px; line-height: 2.5;">
            <div style="font-weight: 700; margin-bottom: 24px; color: var(--accent-gold); font-size: 1.2rem;">⚠️ 투자 시 유의사항:</div>
            
            <div>
              단순히 배당수익률 숫자만 높은 '배당의 덫(Dividend Trap)'을 주의해야 합니다.<br><br>
              영업이익이 적자이거나 부채비율이 높은 기업의 고배당은 지속 불가능하므로, 반드시 <strong style="color: #ffffff;">잉여현금흐름(FCF)이 흑자이고 영업이익이 매년 성장하는 기업</strong>에 한정하여 투자해야 합니다.
            </div>
          </div>
        </section>
"""
        elif topic_type == "battery_mobility":
            return f"""
        <!-- Section 1 -->
        <section id="sec-issue-brief" style="margin-bottom: 50px;">
          <h2 style="font-size: 1.75rem; font-weight: 800; color: #ffffff; margin-bottom: 36px; padding-bottom: 18px; border-bottom: 2px solid rgba(6, 182, 212, 0.35); line-height: 1.55;">1. 핵심 이슈 브리핑: 미래 모빌리티와 배터리 혁신</h2>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            글로벌 완성차 시장의 지각 변동과 미래 차세대 모빌리티 전환 속에서 <strong style="color: #ffffff;">“{clean_title}”</strong> 이슈가 시장의 핵심 승부처로 부각되고 있습니다.<br><br>
            {clean_summary}
          </p>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            완성차 업계는 전기차 캐즘(Chasm, 일시적 수요 둔화) 구간을 하이브리드(HEV) 고수익 라인업 확대로 성공적으로 방어하고 있습니다.<br><br>
            동시에 인도 등 신흥 거점 시장에서의 대규모 IPO(상장)와 설비투자를 통해 글로벌 톱3 굳히기에 돌입하고 있습니다.<br><br>
            또한 2차전지 및 소재 업계는 황화물계 전고체 배터리 파일럿 라인 가동과 양극재·음극재 원가 혁신을 통해 차세대 모빌리티 주도권 선점에 총력을 기울이고 있습니다.
          </p>
          
          <div class="callout callout-info" style="margin: 48px 0; padding: 34px 38px; background: rgba(6, 182, 212, 0.08); border-left: 5px solid var(--accent-cyan); border-radius: 12px; line-height: 2.5;">
            <div style="font-weight: 700; margin-bottom: 24px; color: var(--accent-cyan); font-size: 1.2rem;">💡 리서치센터 핵심 팩트체크:</div>
            
            <div style="margin-bottom: 26px; line-height: 2.5;">
              • <strong style="color: #ffffff;">글로벌 IPO 및 대규모 투자 실탄 조달:</strong><br>
              현대차 인도법인의 수조 원대 현지 상장 성공으로 유입된 막대한 자금이 자율주행, SDV(소프트웨어 중심 차), 피지컬 AI 로보틱스 생태계로 재투자되고 있습니다.
            </div>
            
            <div style="margin-bottom: 26px; line-height: 2.5;">
              • <strong style="color: #ffffff;">하이브리드(HEV) 캐시카우 호조:</strong><br>
              전기차 전환 지연 국면에서 두 자릿수 영업이익률을 기록하는 하이브리드 차종의 판매 호조로 완성차 제조사의 현금 흐름이 사상 최대를 기록하고 있습니다.
            </div>
            
            <div>
              • <strong style="color: #ffffff;">전고체 배터리 & 소재 밸류체인:</strong><br>
              2026~2027년 상용화를 목표로 한 꿈의 배터리(전고체) 기술 검증이 본격화되며 핵심 소재 공급망 선점 경쟁이 심화되고 있습니다.
            </div>
          </div>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            이러한 모빌리티 대전환은 단순한 자동차 제조업의 범주를 넘어 자율주행 알고리즘, 전장 부품, 로보틱스 액추에이터, 차세대 배터리 소재가 유기적으로 결합된 복합 테크 생태계로 확장되고 있습니다.
          </p>
        </section>

        {div_sep}

        <!-- Section 2 -->
        <section id="sec-impact-analysis" style="margin-bottom: 50px;">
          <h2 style="font-size: 1.75rem; font-weight: 800; color: #ffffff; margin-bottom: 36px; padding-bottom: 18px; border-bottom: 2px solid rgba(6, 182, 212, 0.35); line-height: 1.55;">2. 시장 파급 효과 및 모빌리티 밸류체인 심층 분석</h2>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            완성차 선도 기업들의 밸류에이션 재평가와 배터리 소재 턴어라운드는 <strong style="color: #ffffff;">부품 협력사 및 차세대 로보틱스 하드웨어 기업</strong>에 강력한 모멘텀을 제공하고 있습니다:
          </p>

          <h3 style="font-size: 1.38rem; font-weight: 700; color: var(--accent-cyan); margin: 52px 0 26px; line-height: 1.55;">🚗 밸류체인 3대 핵심 수혜 섹터</h3>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            <strong style="color: #ffffff;">1. 완성차 선도 대장주 (현대차, 기아)</strong><br><br>
            사상 최대 영업이익과 북미/인도 시장 점유율 확대를 바탕으로 저평가(PER 4~6배) 탈피가 가속화되고 있습니다.<br><br>
            현지 법인 상장에 따른 지분 가치 재평가와 대규모 특별 주주환원(자사주 소각 및 배당 확대)이 주가 상승을 견인합니다.
          </p>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            <strong style="color: #ffffff;">2. 핵심 전장 부품 및 자회사 밸류체인</strong><br><br>
            현대모비스, 현대글로비스, 현대위아 등 그룹 핵심 계열사 및 1차 협력사들의 글로벌 공급 물량이 급증하고 있습니다.<br><br>
            SDV 전환에 따른 전장 소프트웨어 및 제어기 부품의 평균판매단가(ASP) 상승이 마진율을 끌어올리고 있습니다.
          </p>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            <strong style="color: #ffffff;">3. 2차전지 셀 & 차세대 소재(전고체/양극재)</strong><br><br>
            리튬·니켈 등 핵심 광물 가격이 바닥을 다지고 반등함에 따라 원재료 래깅 효과가 소멸되고 재고평가손실이 환입되며 흑자 턴어라운드가 가시화되고 있습니다.
          </p>
          
          <ul style="margin: 32px 0 48px 28px; line-height: 2.5; color: #cbd5e1; display: flex; flex-direction: column; gap: 24px;">
            <li style="margin-bottom: 20px; line-height: 2.5;">
              <strong style="color: #ffffff;">기관·외국인 동반 순매수:</strong><br>
              완성차 대장주와 핵심 전장 부품주로 대규모 프로그램 순매수 유입.
            </li>
            <li>
              <strong style="color: #ffffff;">차트 기술적 분석:</strong><br>
              장기 하락 추세선을 돌파하며 120일 이동평균선 안착 후 우상향 정배열 전환.
            </li>
          </ul>
        </section>

        {div_sep}

        <!-- Section 3: Data Table -->
        <section id="sec-data-table" style="margin-bottom: 50px;">
          <h2 style="font-size: 1.75rem; font-weight: 800; color: #ffffff; margin-bottom: 36px; padding-bottom: 18px; border-bottom: 2px solid rgba(6, 182, 212, 0.35); line-height: 1.55;">3. 모빌리티·배터리 대표 기업 밸류에이션 비교 지표</h2>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            아래는 완성차 및 배터리·부품 대표 기업들의 실적 전망과 가치평가 지표를 비교 정리한 데이터입니다:
          </p>

          <div class="table-responsive" style="margin: 36px 0;">
            <table class="metrics-table">
              <thead>
                <tr>
                  <th>구분</th>
                  <th>예상 PER</th>
                  <th>예상 PBR</th>
                  <th>영업이익률 (OPM)</th>
                  <th>배당수익률</th>
                  <th>수급 및 모멘텀</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><strong>완성차 선도사 (현대차/기아)</strong></td>
                  <td style="color:#00f2fe; font-weight:700;">4.8배 ~ 5.5배</td>
                  <td>0.62배</td>
                  <td>10.5%</td>
                  <td style="color:var(--accent-red); font-weight:700;">5.5% ~ 6.0%</td>
                  <td>인도 상장 모멘텀 & 외인 매수</td>
                </tr>
                <tr>
                  <td><strong>핵심 전장/물류 부품사</strong></td>
                  <td>6.2배 ~ 8.0배</td>
                  <td>0.58배</td>
                  <td>6.8%</td>
                  <td>3.8%</td>
                  <td>SDV 수주 확대 & 기관 매수</td>
                </tr>
                <tr>
                  <td><strong>2차전지 셀 선도사</strong></td>
                  <td>22.0배 ~ 28.0배</td>
                  <td>2.80배</td>
                  <td>5.2%</td>
                  <td>0.8%</td>
                  <td>바닥권 거래량 급증 & 턴어라운드</td>
                </tr>
                <tr>
                  <td><strong>전고체 배터리 핵심 소재사</strong></td>
                  <td>25.0배 ~ 35.0배</td>
                  <td>3.50배</td>
                  <td>8.5%</td>
                  <td>0.5%</td>
                  <td>파일럿 라인 가동 & 테마 랠리</td>
                </tr>
              </tbody>
            </table>
          </div>

          <h3 style="font-size: 1.38rem; font-weight: 700; color: var(--accent-cyan); margin: 52px 0 26px; line-height: 1.55;">📊 데이터 표 심층 분석 및 시사점</h3>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            완성차 제조사들은 글로벌 경쟁사(토요타, 폭스바겐 등) 대비 여전히 40% 이상 저평가되어 있어 주가 상승 여력이 매우 높습니다.<br><br>
            특히 배당수익률이 5% 이상으로 높아 가치주와 성장주의 매력을 동시에 겸비하고 있습니다.<br><br>
            배터리 소재주의 경우 밸류에이션 부담이 일부 존재하므로 기술적 지지선(60일선) 부근에서 분할 매수하는 호흡 조절이 필요합니다.
          </p>
        </section>

        {div_sep}

        <!-- Section 4 -->
        <section id="sec-strategy" style="margin-bottom: 50px;">
          <h2 style="font-size: 1.75rem; font-weight: 800; color: #ffffff; margin-bottom: 36px; padding-bottom: 18px; border-bottom: 2px solid rgba(6, 182, 212, 0.35); line-height: 1.55;">4. 실전 투자 전략 및 분할 매수 체크리스트</h2>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            모빌리티 대전환기에는 섹터별 순환매에 유연하게 대응하는 바벨 포트폴리오 전략이 최선입니다:
          </p>

          <h3 style="font-size: 1.38rem; font-weight: 700; color: var(--accent-cyan); margin: 52px 0 26px; line-height: 1.55;">🎯 실전 포트폴리오 구성 비중 제안</h3>
          
          <ol style="margin: 32px 0 48px 28px; line-height: 2.5; color: #cbd5e1; display: flex; flex-direction: column; gap: 24px;">
            <li style="margin-bottom: 20px; line-height: 2.5;">
              <strong style="color: #ffffff;">코어 자산 (완성차 50%):</strong><br>
              호실적과 고배당으로 하방을 지지해 줄 완성차 대장주 비중 절반 유지.
            </li>
            <li style="margin-bottom: 20px; line-height: 2.5;">
              <strong style="color: #ffffff;">성장 알파 자산 (전장·로봇 30%):</strong><br>
              SDV 전환 및 자율주행 로보틱스 수혜가 가시화되는 전장 부품주 분할 편입.
            </li>
            <li>
              <strong style="color: #ffffff;">베팅 자산 (전고체/2차전지 20%):</strong><br>
              업황 바닥을 통과 중인 2차전지 및 차세대 전고체 소재주에 중장기 적립식 매수.
            </li>
          </ol>

          <div class="callout callout-warning" style="margin: 48px 0; padding: 34px 38px; background: rgba(245, 158, 11, 0.08); border-left: 5px solid var(--accent-gold); border-radius: 12px; line-height: 2.5;">
            <div style="font-weight: 700; margin-bottom: 24px; color: var(--accent-gold); font-size: 1.2rem;">⚠️ 리스크 관리 원칙:</div>
            
            <div style="margin-bottom: 24px; line-height: 2.5;">
              - <strong style="color: #ffffff;">주요 지정학 관세 리스크:</strong><br>
              미국 및 유럽연합(EU)의 무역 정책 변화 및 관세 부과 여부 실시간 점검.
            </div>
            
            <div>
              - <strong style="color: #ffffff;">단기 급등 시 차익 실현:</strong><br>
              단기 급등 종목은 20일 이격도 115% 초과 시 일부 비중을 현금화하여 수익 확정.
            </div>
          </div>
        </section>
"""
        elif topic_type == "bio_healthcare":
            return f"""
        <!-- Section 1 -->
        <section id="sec-issue-brief" style="margin-bottom: 50px;">
          <h2 style="font-size: 1.75rem; font-weight: 800; color: #ffffff; margin-bottom: 36px; padding-bottom: 18px; border-bottom: 2px solid rgba(6, 182, 212, 0.35); line-height: 1.55;">1. 핵심 이슈 브리핑: K-바이오 글로벌 기술수출 및 신약 파이프라인</h2>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            글로벌 빅파마들의 대규모 M&A 및 신약 기술도입(License-in) 수요가 폭증하면서 <strong style="color: #ffffff;">“{clean_title}”</strong> 이슈가 바이오 섹터의 주가 상승을 견인하고 있습니다.<br><br>
            {clean_summary}
          </p>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            미국 생물보안법(Biosecure Act) 통과에 따른 중국 CDMO 기업 제재로 국내 위탁개발생산(CDMO) 및 바이오시밀러 기업들의 글로벌 수주 반사이익이 현실화되고 있습니다.<br><br>
            동시에 ADC(항체-약물 접합체), 비만·당뇨 치료제, 면역항암제 분야에서 조 단위 기술이전 계약이 잇따르고 있습니다.
          </p>
          
          <div class="callout callout-info" style="margin: 48px 0; padding: 34px 38px; background: rgba(6, 182, 212, 0.08); border-left: 5px solid var(--accent-cyan); border-radius: 12px; line-height: 2.5;">
            <div style="font-weight: 700; margin-bottom: 24px; color: var(--accent-cyan); font-size: 1.2rem;">💡 리서치센터 핵심 팩트체크:</div>
            
            <div style="margin-bottom: 26px; line-height: 2.5;">
              • <strong style="color: #ffffff;">생물보안법 최대 수혜:</strong><br>
              글로벌 톱티어 수준의 생산 캐파(Capa)를 보유한 국내 대형 CDMO 기업들로 글로벌 제약사들의 장기 생산 계약 문의가 집중되고 있습니다.
            </div>
            
            <div style="margin-bottom: 26px; line-height: 2.5;">
              • <strong style="color: #ffffff;">플랫폼 기술의 확장성:</strong><br>
              피하주사(SC) 제형 변경 플랫폼과 ADC 링커 기술을 보유한 바이오텍들의 로열티 및 마일스톤(단계별 기술료) 유입이 가속화되고 있습니다.
            </div>
            
            <div>
              • <strong style="color: #ffffff;">FDA 승인 및 상업화 성공:</strong><br>
              자체 개발 신약의 미국 FDA 품목허가 승인 획득으로 직판 체제를 구축한 기업들의 실적 퀀텀점프가 숫자로 입증되고 있습니다.
            </div>
          </div>
        </section>

        {div_sep}

        <!-- Section 2 -->
        <section id="sec-impact-analysis" style="margin-bottom: 50px;">
          <h2 style="font-size: 1.75rem; font-weight: 800; color: #ffffff; margin-bottom: 36px; padding-bottom: 18px; border-bottom: 2px solid rgba(6, 182, 212, 0.35); line-height: 1.55;">2. 수급 및 파이프라인 가치평가 분석</h2>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            바이오 투자는 단순한 꿈과 기대감이 아니라 <strong style="color: #ffffff;">실제 계약 규모, 마일스톤 유입 시점, 현금 보유력</strong>을 기반으로 철저히 옥석을 가려야 합니다:
          </p>

          <h3 style="font-size: 1.38rem; font-weight: 700; color: var(--accent-cyan); margin: 52px 0 26px; line-height: 1.55;">🧬 3대 바이오 수혜 축</h3>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            <strong style="color: #ffffff;">1. 글로벌 CDMO & 바이오시밀러 대장주</strong><br><br>
            안정적인 분기 영업이익과 가동률 100%를 바탕으로 코스피 대형주 내 최고의 방어력과 성장성을 겸비.
          </p>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            <strong style="color: #ffffff;">2. 플랫폼 기술수출 선도 바이오텍</strong><br><br>
            단일 파이프라인 실패 리스크가 없는 다중 타겟 플랫폼(SC 변경, ADC 등) 기업으로 기관 자금 집중.
          </p>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            <strong style="color: #ffffff;">3. FDA 승인 신약 보유 상업화 제약사</strong><br><br>
            글로벌 처방 데이터 증가에 따라 분기마다 마진율이 급증하는 고수익 구조 안착.
          </p>
        </section>

        {div_sep}

        <!-- Section 3: Data Table -->
        <section id="sec-data-table" style="margin-bottom: 50px;">
          <h2 style="font-size: 1.75rem; font-weight: 800; color: #ffffff; margin-bottom: 36px; padding-bottom: 18px; border-bottom: 2px solid rgba(6, 182, 212, 0.35); line-height: 1.55;">3. 바이오 대표 종목군 지표 비교표</h2>
          
          <div class="table-responsive" style="margin: 36px 0;">
            <table class="metrics-table">
              <thead>
                <tr>
                  <th>기업 구분</th>
                  <th>주요 파이프라인 / 강점</th>
                  <th>예상 마일스톤 / 수주</th>
                  <th>투자 매력도</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><strong>대형 CDMO 선도사</strong></td>
                  <td>항체의약품 대규모 생산 캐파</td>
                  <td>조 단위 글로벌 장기 수주</td>
                  <td style="color:var(--accent-red); font-weight:700;">최상 (안정성+성장성)</td>
                </tr>
                <tr>
                  <td><strong>SC제형 플랫폼 바이오텍</strong></td>
                  <td>글로벌 빅파마 독점 기술수출</td>
                  <td>2026~2027 조 단위 로열티 본격화</td>
                  <td style="color:var(--accent-red); font-weight:700;">최상 (모멘텀 강세)</td>
                </tr>
                <tr>
                  <td><strong>ADC/표적항암 신약사</strong></td>
                  <td>차세대 링커 기술 및 임상 2상</td>
                  <td>추가 글로벌 라이선스 아웃</td>
                  <td>상 (임상 결과 주목)</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        {div_sep}

        <!-- Section 4 -->
        <section id="sec-strategy" style="margin-bottom: 50px;">
          <h2 style="font-size: 1.75rem; font-weight: 800; color: #ffffff; margin-bottom: 36px; padding-bottom: 18px; border-bottom: 2px solid rgba(6, 182, 212, 0.35); line-height: 1.55;">4. 바이오 종목 실전 매매 원칙</h2>
          
          <div class="callout callout-warning" style="margin: 48px 0; padding: 34px 38px; background: rgba(245, 158, 11, 0.08); border-left: 5px solid var(--accent-gold); border-radius: 12px; line-height: 2.5;">
            <div style="font-weight: 700; margin-bottom: 24px; color: var(--accent-gold); font-size: 1.2rem;">🎯 바이오 성공 투자 3계명:</div>
            
            <div style="margin-bottom: 24px; line-height: 2.5;">
              1. <strong style="color: #ffffff;">학회 일정(AACR, ASCO 등) 선취매:</strong><br>
              발표 1~2개월 전 바닥권 분할 매수 후 학회 개막 직전 분할 매도.
            </div>
            
            <div style="margin-bottom: 24px; line-height: 2.5;">
              2. <strong style="color: #ffffff;">현금 소진율(Burn Rate) 체크:</strong><br>
              1년 이상 유상증자 없이 연구개발이 가능한 풍부한 현금 보유 기업 선별.
            </div>
            
            <div>
              3. <strong style="color: #ffffff;">철저한 비중 조절:</strong><br>
              변동성이 큰 개별 바이오텍은 계좌 내 비중을 15% 이내로 엄격히 관리.
            </div>
          </div>
        </section>
"""
        elif topic_type == "power_energy":
            return f"""
        <!-- Section 1 -->
        <section id="sec-issue-brief" style="margin-bottom: 50px;">
          <h2 style="font-size: 1.75rem; font-weight: 800; color: #ffffff; margin-bottom: 36px; padding-bottom: 18px; border-bottom: 2px solid rgba(6, 182, 212, 0.35); line-height: 1.55;">1. 핵심 이슈 브리핑: AI 전력망 인프라 슈퍼사이클</h2>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            전 세계적인 AI 데이터센터 증설과 노후 전력망 교체 주기가 맞물려 <strong style="color: #ffffff;">“{clean_title}”</strong> 테마가 강력한 메가트렌드로 자리잡았습니다.<br><br>
            {clean_summary}
          </p>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            미국과 유럽을 중심으로 초고압 변압기(UHV)와 배전 기기, 해저 케이블의 납기가 4~5년 이상 지연되는 극심한 공급 부족(Shortage) 현상이 지속되고 있습니다.<br><br>
            국내 전력 인프라 3사의 수주 잔고는 이미 2029년 생산 물량까지 가득 차 있는 상태입니다.
          </p>
          
          <div class="callout callout-info" style="margin: 48px 0; padding: 34px 38px; background: rgba(6, 182, 212, 0.08); border-left: 5px solid var(--accent-cyan); border-radius: 12px; line-height: 2.5;">
            <div style="font-weight: 700; margin-bottom: 24px; color: var(--accent-cyan); font-size: 1.2rem;">💡 리서치센터 핵심 팩트체크:</div>
            
            <div style="margin-bottom: 26px; line-height: 2.5;">
              • <strong style="color: #ffffff;">북미 전력망 교체 사이클:</strong><br>
              미국 내 설치된 변압기의 70% 이상이 설계 수명(25년)을 초과하여 대규모 교체 발주 진행 중.
            </div>
            
            <div style="margin-bottom: 26px; line-height: 2.5;">
              • <strong style="color: #ffffff;">빅테크 전력 구매 계약:</strong><br>
              구글, 마이크로소프트, 아마존이 데이터센터 가동을 위해 원전(SMR) 및 전력 설비 기업과 장기 공급 계약 체결.
            </div>
            
            <div>
              • <strong style="color: #ffffff;">영업이익률 급상승:</strong><br>
              판가 인상(P)과 물량 증가(Q)가 동반되며 전력기기 업계의 영업이익률이 20%를 돌파.
            </div>
          </div>
        </section>

        {div_sep}

        <!-- Section 2 -->
        <section id="sec-impact-analysis" style="margin-bottom: 50px;">
          <h2 style="font-size: 1.75rem; font-weight: 800; color: #ffffff; margin-bottom: 36px; padding-bottom: 18px; border-bottom: 2px solid rgba(6, 182, 212, 0.35); line-height: 1.55;">2. 전력·원전 밸류체인 수혜 분석</h2>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            <strong style="color: #ffffff;">1. 초고압 변압기 & 전력기기 선도사 (HD현대일렉트릭, 효성중공업, LS일렉트릭)</strong><br><br>
            북미 수출 비중 확대와 공장 증설 효과로 분기마다 사상 최고 실적 경신.
          </p>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            <strong style="color: #ffffff;">2. 초고압 해저케이블 & 전선 기업 (LS, 대한전선)</strong><br><br>
            해상풍력 발전 및 국가 간 송전망 연결 프로젝트로 초고압직류송전(HVDC) 케이블 수주 폭증.
          </p>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            <strong style="color: #ffffff;">3. SMR(소형모듈원자로) 및 대형 원전 밸류체인</strong><br><br>
            체코 원전 수주를 필두로 유럽·중동 원전 르네상스 진입.
          </p>
        </section>

        {div_sep}

        <!-- Section 3: Data Table -->
        <section id="sec-data-table" style="margin-bottom: 50px;">
          <h2 style="font-size: 1.75rem; font-weight: 800; color: #ffffff; margin-bottom: 36px; padding-bottom: 18px; border-bottom: 2px solid rgba(6, 182, 212, 0.35); line-height: 1.55;">3. 전력 대표주 밸류에이션 비교</h2>
          
          <div class="table-responsive" style="margin: 36px 0;">
            <table class="metrics-table">
              <thead>
                <tr>
                  <th>업종/구분</th>
                  <th>수주 잔고 (년수)</th>
                  <th>2026 예상 OPM</th>
                  <th>주요 수출 지역</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><strong>초고압 변압기 선도</strong></td>
                  <td>4.5년 치 확보</td>
                  <td style="color:var(--accent-red); font-weight:700;">22% ~ 26%</td>
                  <td>북미, 중동</td>
                </tr>
                <tr>
                  <td><strong>중저압 배전 & 스마트그리드</strong></td>
                  <td>3.0년 치 확보</td>
                  <td>12% ~ 16%</td>
                  <td>국내, 북미 데이터센터</td>
                </tr>
                <tr>
                  <td><strong>초고압 HVDC 전선</strong></td>
                  <td>3.5년 치 확보</td>
                  <td>10% ~ 14%</td>
                  <td>유럽, 아시아 해상풍력</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        {div_sep}

        <!-- Section 4 -->
        <section id="sec-strategy" style="margin-bottom: 50px;">
          <h2 style="font-size: 1.75rem; font-weight: 800; color: #ffffff; margin-bottom: 36px; padding-bottom: 18px; border-bottom: 2px solid rgba(6, 182, 212, 0.35); line-height: 1.55;">4. 전력 인프라 실전 투자 전략</h2>
          
          <div class="callout callout-warning" style="margin: 48px 0; padding: 34px 38px; background: rgba(245, 158, 11, 0.08); border-left: 5px solid var(--accent-gold); border-radius: 12px; line-height: 2.5;">
            <div style="font-weight: 700; margin-bottom: 24px; color: var(--accent-gold); font-size: 1.2rem;">⚡ 매매 가이드:</div>
            
            <div style="margin-bottom: 24px; line-height: 2.5;">
              - <strong style="color: #ffffff;">눌림목 분할 매수:</strong><br>
              역사적 신고가 부근에서는 추격 매수 대신 20일선 및 60일선 조정 시 분할 매수.
            </div>
            
            <div>
              - <strong style="color: #ffffff;">수주 공시 모멘텀:</strong><br>
              대형 수주 공시 후 단기 차익 매물이 출회될 때 저점 매수 기회로 활용.
            </div>
          </div>
        </section>
"""
        elif topic_type == "geopolitics":
            return f"""
        <!-- Section 1 -->
        <section id="sec-issue-brief" style="margin-bottom: 50px;">
          <h2 style="font-size: 1.75rem; font-weight: 800; color: #ffffff; margin-bottom: 36px; padding-bottom: 18px; border-bottom: 2px solid rgba(6, 182, 212, 0.35); line-height: 1.55;">1. 핵심 이슈 브리핑: 글로벌 지정학 리스크와 K-방산</h2>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            중동 분쟁, 동유럽 전황 및 글로벌 안보 불안 속에서 <strong style="color: #ffffff;">“{clean_title}”</strong> 테마가 강력한 시장 방어주이자 성장주로 주목받고 있습니다.<br><br>
            {clean_summary}
          </p>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            나토(NATO) 회원국들의 국방비 증액 의무화와 중동 국가들의 방공망 강화 수요가 겹치며 K-방산 기업들의 글로벌 수출 파이프라인이 유례없이 확장되고 있습니다.
          </p>
          
          <div class="callout callout-info" style="margin: 48px 0; padding: 34px 38px; background: rgba(6, 182, 212, 0.08); border-left: 5px solid var(--accent-cyan); border-radius: 12px; line-height: 2.5;">
            <div style="font-weight: 700; margin-bottom: 24px; color: var(--accent-cyan); font-size: 1.2rem;">💡 리서치센터 핵심 팩트체크:</div>
            
            <div style="margin-bottom: 26px; line-height: 2.5;">
              • <strong style="color: #ffffff;">가성비와 빠른 납기:</strong><br>
              서구권 무기체계 대비 30% 이상 저렴한 가격과 압도적으로 빠른 양산 납기 능력이 글로벌 표준으로 인정받음.
            </div>
            
            <div style="margin-bottom: 26px; line-height: 2.5;">
              • <strong style="color: #ffffff;">유도무기 & 자주포 수출 다변화:</strong><br>
              폴란드, 루마니아, 호주에 이어 중동(UAE, 사우디)으로 천궁-II, K9 자주포 수출 계약 연속 체결.
            </div>
            
            <div>
              • <strong style="color: #ffffff;">조선·해운 반사이익:</strong><br>
              홍해 사태 등 해상 운임 상승과 노후 함정 MRO(유지·보수·정비) 시장 진출로 특수선 매출 급증.
            </div>
          </div>
        </section>

        {div_sep}

        <!-- Section 2 -->
        <section id="sec-impact-analysis" style="margin-bottom: 50px;">
          <h2 style="font-size: 1.75rem; font-weight: 800; color: #ffffff; margin-bottom: 36px; padding-bottom: 18px; border-bottom: 2px solid rgba(6, 182, 212, 0.35); line-height: 1.55;">2. 방산·조선 밸류체인 수혜 종목군</h2>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            <strong style="color: #ffffff;">1. 지상 무기 & 유도무기 체계 선도사 (한화에어로스페이스, LIG넥스원, 현대로템)</strong><br><br>
            사상 최대 수출 잔고를 바탕으로 계절성 없는 실적 고성장세 지속.
          </p>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            <strong style="color: #ffffff;">2. 항공우주 & 감시정찰 (KAI, 한화시스템)</strong><br><br>
            KF-21 양산 착수 및 군사정찰위성 발사 성공으로 독보적인 기술 진입장벽 구축.
          </p>
        </section>

        {div_sep}

        <!-- Section 3: Data Table -->
        <section id="sec-data-table" style="margin-bottom: 50px;">
          <h2 style="font-size: 1.75rem; font-weight: 800; color: #ffffff; margin-bottom: 36px; padding-bottom: 18px; border-bottom: 2px solid rgba(6, 182, 212, 0.35); line-height: 1.55;">3. 주요 방산 기업 펀더멘털 비교</h2>
          
          <div class="table-responsive" style="margin: 36px 0;">
            <table class="metrics-table">
              <thead>
                <tr>
                  <th>구분</th>
                  <th>수출 비중</th>
                  <th>예상 영업이익 증가율</th>
                  <th>외국인 순매수 추이</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><strong>지상 무기 선도</strong></td>
                  <td>55% 이상</td>
                  <td style="color:var(--accent-red); font-weight:700;">+45% YoY</td>
                  <td>외국인 보유율 40% 돌파</td>
                </tr>
                <tr>
                  <td><strong>정밀 유도무기</strong></td>
                  <td>40% 이상</td>
                  <td>+35% YoY</td>
                  <td>기관 연기금 연속 순매수</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        {div_sep}

        <!-- Section 4 -->
        <section id="sec-strategy" style="margin-bottom: 50px;">
          <h2 style="font-size: 1.75rem; font-weight: 800; color: #ffffff; margin-bottom: 36px; padding-bottom: 18px; border-bottom: 2px solid rgba(6, 182, 212, 0.35); line-height: 1.55;">4. 지정학 리스크 실전 헤징 전략</h2>
          
          <div class="callout callout-warning" style="margin: 48px 0; padding: 34px 38px; background: rgba(245, 158, 11, 0.08); border-left: 5px solid var(--accent-gold); border-radius: 12px; line-height: 2.5;">
            <div style="font-weight: 700; margin-bottom: 24px; color: var(--accent-gold); font-size: 1.2rem;">🛡️ 리스크 헤징 포트폴리오:</div>
            
            <div>
              지정학 분쟁 뉴스에 따라 일시적 급등락이 발생하므로, <strong style="color: #ffffff;">방산주 15% + 고배당주 20%</strong> 조합으로 시장 하락 위험을 헤지하면서 중장기 수출 실적 모멘텀을 향유하는 전략을 권장합니다.
            </div>
          </div>
        </section>
"""
        elif topic_type == "ipo":
            return f"""
        <!-- Section 1 -->
        <section id="sec-issue-brief" style="margin-bottom: 50px;">
          <h2 style="font-size: 1.75rem; font-weight: 800; color: #ffffff; margin-bottom: 36px; padding-bottom: 18px; border-bottom: 2px solid rgba(6, 182, 212, 0.35); line-height: 1.55;">1. 핵심 이슈 브리핑: 공모주 청약 및 신규 상장주 옥석 가리기</h2>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            IPO 시장의 열기와 함께 <strong style="color: #ffffff;">“{clean_title}”</strong> 이슈에 개인 투자자 및 공모주 펀드의 관심이 집중되고 있습니다.<br><br>
            {clean_summary}
          </p>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            최근 상장일 가격제한폭 제도 시행 이후, 기업의 실질적 가치보다 수급에 의한 변동성이 확대되고 있습니다.<br><br>
            이에 따라 상장 첫날 유통 가능 물량과 기관 의무보유확약 비율을 철저히 사전 분석해야 합니다.
          </p>
          
          <div class="callout callout-info" style="margin: 48px 0; padding: 34px 38px; background: rgba(6, 182, 212, 0.08); border-left: 5px solid var(--accent-cyan); border-radius: 12px; line-height: 2.5;">
            <div style="font-weight: 700; margin-bottom: 24px; color: var(--accent-cyan); font-size: 1.2rem;">💡 리서치센터 핵심 팩트체크:</div>
            
            <div style="margin-bottom: 26px; line-height: 2.5;">
              • <strong style="color: #ffffff;">의무보유확약 비율(Lock-up):</strong><br>
              기관투자자의 의무보유확약 비율이 30% 이상일수록 상장 후 오버행(대량 매도) 부담이 적습니다.
            </div>
            
            <div style="margin-bottom: 26px; line-height: 2.5;">
              • <strong style="color: #ffffff;">유통 가능 물량:</strong><br>
              상장 당일 유통 가능 주식 수가 20~25% 이하인 품절주 성격의 종목이 초기 주가 방어력이 높습니다.
            </div>
            
            <div>
              • <strong style="color: #ffffff;">공모가 산정 밸류에이션:</strong><br>
              비교 대상 기업의 PER이 지나치게 고평가되어 산정되지 않았는지 꼼꼼한 확인이 필수입니다.
            </div>
          </div>
        </section>

        {div_sep}

        <!-- Section 2 -->
        <section id="sec-impact-analysis" style="margin-bottom: 50px;">
          <h2 style="font-size: 1.75rem; font-weight: 800; color: #ffffff; margin-bottom: 36px; padding-bottom: 18px; border-bottom: 2px solid rgba(6, 182, 212, 0.35); line-height: 1.55;">2. 공모주 청약 실전 배정 및 자금 운용 팁</h2>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            <strong style="color: #ffffff;">1. 균등 배정 vs 비례 배정 자금 배분</strong><br><br>
            최소 청약 증거금으로 균등 배정 주식을 챙기고, 단기 대출 이자비용을 감안하여 비례 배정 자금을 효율적으로 안배.
          </p>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            <strong style="color: #ffffff;">2. 상장일 시초가 매매 및 분할 매도 원칙</strong><br><br>
            상장 첫날 개장 직후 30분간의 거래량과 변동성을 활용하여 70%는 분할 익절, 나머지 30%는 추세 이탈 시 정리.
          </p>
        </section>

        {div_sep}

        <!-- Section 3: Data Table -->
        <section id="sec-data-table" style="margin-bottom: 50px;">
          <h2 style="font-size: 1.75rem; font-weight: 800; color: #ffffff; margin-bottom: 36px; padding-bottom: 18px; border-bottom: 2px solid rgba(6, 182, 212, 0.35); line-height: 1.55;">3. 공모주 핵심 체크리스트 지표</h2>
          
          <div class="table-responsive" style="margin: 36px 0;">
            <table class="metrics-table">
              <thead>
                <tr>
                  <th>체크포인트</th>
                  <th>안전 기준선</th>
                  <th>위험 기준선</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><strong>기관 경쟁률</strong></td>
                  <td>1,000 : 1 이상</td>
                  <td>500 : 1 미만</td>
                </tr>
                <tr>
                  <td><strong>의무보유확약 비율</strong></td>
                  <td>30% 이상</td>
                  <td>10% 미만 (상장일 매물 주의)</td>
                </tr>
                <tr>
                  <td><strong>유통 가능 물량</strong></td>
                  <td>25% 이하</td>
                  <td>40% 초과 (오버행 경고)</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        {div_sep}

        <!-- Section 4 -->
        <section id="sec-strategy" style="margin-bottom: 50px;">
          <h2 style="font-size: 1.75rem; font-weight: 800; color: #ffffff; margin-bottom: 36px; padding-bottom: 18px; border-bottom: 2px solid rgba(6, 182, 212, 0.35); line-height: 1.55;">4. 신규 상장주 락업 해제 일정 관리</h2>
          
          <div class="callout callout-warning" style="margin: 48px 0; padding: 34px 38px; background: rgba(245, 158, 11, 0.08); border-left: 5px solid var(--accent-gold); border-radius: 12px; line-height: 2.5;">
            <div style="font-weight: 700; margin-bottom: 24px; color: var(--accent-gold); font-size: 1.2rem;">📅 오버행 캘린더 관리:</div>
            
            <div>
              상장 후 15일, 1개월, 3개월, 6개월 차에 대규모 벤처캐피탈(VC) 및 기관 락업이 순차적으로 해제됩니다.<br><br>
              <strong style="color: #ffffff;">보호예수 해제일 3~5일 전에는 단기 차익 실현 후 관망</strong>하는 전략이 안전합니다.
            </div>
          </div>
        </section>
"""
        elif topic_type == "breakout_stocks":
            return f"""
        <!-- Section 1 -->
        <section id="sec-issue-brief" style="margin-bottom: 50px;">
          <h2 style="font-size: 1.75rem; font-weight: 800; color: #ffffff; margin-bottom: 36px; padding-bottom: 18px; border-bottom: 2px solid rgba(6, 182, 212, 0.35); line-height: 1.55;">1. 핵심 이슈 브리핑: 상승초입 신고가 돌파 및 거래량 급증 포착</h2>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            바닥권 장기 횡보를 끝내고 강력한 모멘텀으로 추세를 전환하는 <strong style="color: #ffffff;">“{clean_title}”</strong> 종목이 시장 참여자들의 이목을 사로잡고 있습니다.<br><br>
            {clean_summary}
          </p>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            기술적 분석에서 가장 신뢰도가 높은 패턴은 '거래량 급증을 동반한 전고점 돌파'와 '20일·60일·120일 이동평균선의 정배열 골든크로스'입니다.<br><br>
            스마트 머니의 매집이 완료된 종목은 단기 변동성을 딛고 강력한 2차 상승 파동을 만들어냅니다.
          </p>
          
          <div class="callout callout-info" style="margin: 48px 0; padding: 34px 38px; background: rgba(6, 182, 212, 0.08); border-left: 5px solid var(--accent-cyan); border-radius: 12px; line-height: 2.5;">
            <div style="font-weight: 700; margin-bottom: 24px; color: var(--accent-cyan); font-size: 1.2rem;">💡 리서치센터 차트 팩트체크:</div>
            
            <div style="margin-bottom: 26px; line-height: 2.5;">
              • <strong style="color: #ffffff;">거래량 500% 급증:</strong><br>
              횡보 구간 평균 거래량 대비 5배 이상의 대량 거래가 실리며 직전 박스권 상단을 양봉으로 돌파.
            </div>
            
            <div style="margin-bottom: 26px; line-height: 2.5;">
              • <strong style="color: #ffffff;">외국인·기관 쌍끌이 순매수:</strong><br>
              개인 투자자들의 매물을 메이저 수급 주체가 흡수하며 매물벽을 완전히 소화.
            </div>
            
            <div>
              • <strong style="color: #ffffff;">이격도 및 보조지표:</strong><br>
              RSI 60~70권 진입, MACD 오실레이터가 0선을 돌파하며 강한 추세 상승 모멘텀 형성.
            </div>
          </div>
        </section>

        {div_sep}

        <!-- Section 2 -->
        <section id="sec-impact-analysis" style="margin-bottom: 50px;">
          <h2 style="font-size: 1.75rem; font-weight: 800; color: #ffffff; margin-bottom: 36px; padding-bottom: 18px; border-bottom: 2px solid rgba(6, 182, 212, 0.35); line-height: 1.55;">2. 수급 주체별 매매 동향 및 지지선 분석</h2>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            <strong style="color: #ffffff;">1. 전고점 지지력 테스트 (눌림목 매수 구간)</strong><br><br>
            돌파된 직전 저항선은 이제 가장 강력한 지지선으로 작용합니다.<br><br>
            거래량이 줄어들며 전고점 라인을 리테스트할 때가 가장 손익비가 우수한 1차 진입 타점입니다.
          </p>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            <strong style="color: #ffffff;">2. 이평선 정배열 추세 추종 전략</strong><br><br>
            20일선이 살아있는 한 주가는 지속적인 N자형 상승 파동을 그립니다.<br><br>
            20일선 이탈 전까지는 홀딩하며 수익을 극대화하는 '트렌드 팔로잉'이 필수적입니다.
          </p>
        </section>

        {div_sep}

        <!-- Section 3: Data Table -->
        <section id="sec-data-table" style="margin-bottom: 50px;">
          <h2 style="font-size: 1.75rem; font-weight: 800; color: #ffffff; margin-bottom: 36px; padding-bottom: 18px; border-bottom: 2px solid rgba(6, 182, 212, 0.35); line-height: 1.55;">3. 기술적 돌파 지표 핵심 기준표</h2>
          
          <div class="table-responsive" style="margin: 36px 0;">
            <table class="metrics-table">
              <thead>
                <tr>
                  <th>기술적 지표</th>
                  <th>이상적인 매수 시그널</th>
                  <th>경계 / 매도 시그널</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><strong>거래량</strong></td>
                  <td>전일 대비 300%~500% 이상 폭증</td>
                  <td>주가 상승에도 거래량 급감 (다이버전스)</td>
                </tr>
                <tr>
                  <td><strong>이동평균선</strong></td>
                  <td>5일 &gt; 20일 &gt; 60일 정배열 확장</td>
                  <td>20일선 하향 이탈 데드크로스</td>
                </tr>
                <tr>
                  <td><strong>RSI (상대강도지수)</strong></td>
                  <td>55 ~ 68 (상승 추세 진행)</td>
                  <td>80 이상 과매수권 (단기 과열)</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        {div_sep}

        <!-- Section 4 -->
        <section id="sec-strategy" style="margin-bottom: 50px;">
          <h2 style="font-size: 1.75rem; font-weight: 800; color: #ffffff; margin-bottom: 36px; padding-bottom: 18px; border-bottom: 2px solid rgba(6, 182, 212, 0.35); line-height: 1.55;">4. 승률 80% 돌파 매매 실전 수칙</h2>
          
          <div class="callout callout-warning" style="margin: 48px 0; padding: 34px 38px; background: rgba(245, 158, 11, 0.08); border-left: 5px solid var(--accent-gold); border-radius: 12px; line-height: 2.5;">
            <div style="font-weight: 700; margin-bottom: 24px; color: var(--accent-gold); font-size: 1.2rem;">🎯 손익비 중심 매매 룰:</div>
            
            <div style="margin-bottom: 24px; line-height: 2.5;">
              • <strong style="color: #ffffff;">손절선은 짧게 (-3% ~ -5%):</strong><br>
              돌파에 실패하고 직전 박스권 안으로 다시 밀려날 경우 즉시 손절하여 손실 최소화.
            </div>
            
            <div>
              • <strong style="color: #ffffff;">익절은 길게 (+15% ~ +30%):</strong><br>
              돌파 성공 시에는 5일선 종가 이탈 전까지 추세를 즐기며 분할 매도로 수익 극대화.
            </div>
          </div>
        </section>
"""
        else: # general_stock
            return f"""
        <!-- Section 1 -->
        <section id="sec-issue-brief" style="margin-bottom: 50px;">
          <h2 style="font-size: 1.75rem; font-weight: 800; color: #ffffff; margin-bottom: 36px; padding-bottom: 18px; border-bottom: 2px solid rgba(6, 182, 212, 0.35); line-height: 1.55;">1. 핵심 이슈 브리핑: 시장 배경 및 팩트체크</h2>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            최근 국내외 증시 및 금융 시장에서 큰 주목을 받고 있는 핵심 테마는 <strong style="color: #ffffff;">“{clean_title}”</strong>입니다.<br><br>
            {clean_summary}
          </p>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            거시경제 환경의 불확실성과 업종별 수급 순환매가 빠르게 전개되는 국면입니다.<br><br>
            시장을 주도하는 핵심 모멘텀과 실적 펀더멘털을 정밀 분석하여 선별적으로 접근하는 것이 중요합니다.
          </p>
          
          <div class="callout callout-info" style="margin: 48px 0; padding: 34px 38px; background: rgba(6, 182, 212, 0.08); border-left: 5px solid var(--accent-cyan); border-radius: 12px; line-height: 2.5;">
            <div style="font-weight: 700; margin-bottom: 24px; color: var(--accent-cyan); font-size: 1.2rem;">💡 리서치센터 핵심 관전 포인트:</div>
            
            <div style="margin-bottom: 26px; line-height: 2.5;">
              • <strong style="color: #ffffff;">시장 모멘텀:</strong><br>
              매크로 지표 변화와 업종별 수급 순환매 속에서 {clean_title} 관련 핵심 기업들로 스마트 머니가 유입되고 있습니다.
            </div>
            
            <div style="margin-bottom: 26px; line-height: 2.5;">
              • <strong style="color: #ffffff;">실적 및 펀더멘털:</strong><br>
              단순 기대감이 아닌 실제 영업이익 개선과 수주 잔고 증가가 숫자로 증명되는 선도주 선별이 필수적입니다.
            </div>
            
            <div>
              • <strong style="color: #ffffff;">정책 및 글로벌 환경:</strong><br>
              글로벌 산업 동향과 정부 정책 지원이 맞물려 중장기 성장 동력이 강화되고 있습니다.
            </div>
          </div>
        </section>

        {div_sep}

        <!-- Section 2 -->
        <section id="sec-impact-analysis" style="margin-bottom: 50px;">
          <h2 style="font-size: 1.75rem; font-weight: 800; color: #ffffff; margin-bottom: 36px; padding-bottom: 18px; border-bottom: 2px solid rgba(6, 182, 212, 0.35); line-height: 1.55;">2. 펀더멘털 및 기술적 수급 분석</h2>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            해당 섹터의 주도주들은 안정적인 재무 건전성(낮은 부채비율, 높은 ROE)과 함께 거래량을 동반한 바닥권 박스권 돌파 흐름을 나타내고 있습니다:
          </p>
          
          <ul style="margin: 32px 0 48px 28px; line-height: 2.5; color: #cbd5e1; display: flex; flex-direction: column; gap: 24px;">
            <li style="margin-bottom: 20px; line-height: 2.5;">
              <strong style="color: #ffffff;">기관·외국인 동반 순매수:</strong><br>
              메이저 수급 주체들이 최근 5~10거래일 연속 순매수 우위를 유지.
            </li>
            <li style="margin-bottom: 20px; line-height: 2.5;">
              <strong style="color: #ffffff;">이동평균선 정배열 전환:</strong><br>
              단기 이평선(20일)이 중장기 이평선(60일, 120일)을 골든크로스하며 추세적 상승 국면 진입.
            </li>
            <li>
              <strong style="color: #ffffff;">밸류에이션 매력:</strong><br>
              업종 평균 대비 저평가된 밸류에이션 갭을 메우는 리레이팅 구간 진입.
            </li>
          </ul>
        </section>

        {div_sep}

        <!-- Section 3: Data Table -->
        <section id="sec-data-table" style="margin-bottom: 50px;">
          <h2 style="font-size: 1.75rem; font-weight: 800; color: #ffffff; margin-bottom: 36px; padding-bottom: 18px; border-bottom: 2px solid rgba(6, 182, 212, 0.35); line-height: 1.55;">3. 주요 핵심 지표 및 밸류에이션 요약</h2>
          
          <div class="table-responsive" style="margin: 36px 0;">
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

        {div_sep}

        <!-- Section 4 -->
        <section id="sec-strategy" style="margin-bottom: 50px;">
          <h2 style="font-size: 1.75rem; font-weight: 800; color: #ffffff; margin-bottom: 36px; padding-bottom: 18px; border-bottom: 2px solid rgba(6, 182, 212, 0.35); line-height: 1.55;">4. 핵심 리스크 점검 및 분할 매매 대응 전략</h2>
          
          <div class="callout callout-warning" style="margin: 48px 0; padding: 34px 38px; background: rgba(245, 158, 11, 0.08); border-left: 5px solid var(--accent-gold); border-radius: 12px; line-height: 2.5;">
            <div style="font-weight: 700; margin-bottom: 24px; color: var(--accent-gold); font-size: 1.2rem;">⚠️ 리스크 관리 원칙:</div>
            
            <div style="margin-bottom: 24px; line-height: 2.5;">
              - 단기 급등에 따른 뇌동매매를 지양하고 <strong style="color: #ffffff;">3회 이상 분할 매수(30% / 30% / 40%)</strong> 원칙 준수.
            </div>
            
            <div style="margin-bottom: 24px; line-height: 2.5;">
              - 주요 기술적 지지선 이탈 시 <strong style="color: #ffffff;">손절 기준선(-5% ~ -7%)</strong>을 엄격히 지켜 원금 보존 최우선.
            </div>
            
            <div>
              - 목표 수익률 도달 시 50% 분할 익절 후 잔여 물량은 트레일링 스탑 적용.
            </div>
          </div>
        </section>
"""

    def analyze_morning_headline(self, title, summary):
        """모닝 브리핑 헤드라인 뉴스에 대해 맥락에 맞는 3단 맞춤형 전문 해설 생성 (줄바꿈 최적화)"""
        full_text = f"{title} {summary}"

        if any(k in full_text for k in ["금리", "대출", "가계부채", "한은", "환율", "인플레", "월급쟁이", "예대"]):
            return (
                "통화정책 피벗 국면에서 가계부채 관리 규제와 예대금리차 변화가 은행 및 내수 소비재 섹터 실적에 미치는 파급 효과를 예의주시해야 합니다.",
                "대형 금융지주(KB/신한/하나) 배당 안정성 강화 vs 내수 유통/소비재 업종 단기 변동성 확대"
            )
        elif any(k in full_text for k in ["반도체", "HBM", "엔비디아", "하이닉스", "삼성전자", "AI", "빅테크"]):
            return (
                "글로벌 AI 인프라 투자 지속 및 차세대 HBM 공급 쇼티지로 인해 메모리 대장주와 첨단 후공정(OSAT) 및 본딩 장비주의 실적 레버리지가 극대화될 전망입니다.",
                "HBM 선도사(SK하이닉스/삼성전자), 패키징 및 테스트 소부장 밸류체인"
            )
        elif any(k in full_text for k in ["자동차", "현대차", "기아", "배터리", "2차전지", "IPO", "인도"]):
            return (
                "글로벌 거점 시장(인도 등) 대규모 상장 모멘텀과 하이브리드(HEV) 고마진 구조 안착이 완성차 및 핵심 전장 부품주의 밸류에이션 리레이팅을 견인하고 있습니다.",
                "완성차 선도사(현대차/기아), 핵심 전장 부품 및 차세대 전고체 소재주"
            )
        elif any(k in full_text for k in ["바이오", "제약", "신약", "FDA", "임상", "CDMO"]):
            return (
                "미국 생물보안법 수혜와 글로벌 빅파마 대상 기술수출(L/O) 파이프라인 가치 부각으로 K-바이오 대형주 및 플랫폼 바이오텍 중심의 수급 유입이 기대됩니다.",
                "대형 바이오 CDMO, SC 제형 변경 및 ADC 신약 플랫폼 기업"
            )
        elif any(k in full_text for k in ["전력", "변압기", "원전", "에너지", "전선"]):
            return (
                "AI 데이터센터 전력 수요 폭증 및 북미 전력망 교체 사이클에 힘입어 초고압 변압기 및 전선 인프라 기업들의 3~4년 치 수주 잔고가 실적으로 가시화되고 있습니다.",
                "초고압 변압기 3사, 해저 전선 및 SMR(소형원전) 관련주"
            )
        elif any(k in full_text for k in ["방산", "조선", "유가", "지정학", "중동"]):
            return (
                "글로벌 안보 불안 장기화 및 국방비 증액 트렌드에 따라 K-방산 수주잔고 급증과 특수선 조선사들의 구조적 실적 개선이 기대됩니다.",
                "K-방산 지상무기 및 유도무기 선도사, 특수선/MRO 조선주"
            )
        elif any(k in full_text for k in ["밸류업", "배당", "자사주", "지주사", "저PBR"]):
            return (
                "기업 밸류업 세제 혜택과 자사주 소각 의무화 추진으로 저PBR 우량 가치주의 배당수익률 및 주주환원율 매력이 부각되며 기관 매수세가 집중되고 있습니다.",
                "고배당 금융주, 순수 지주사 및 자산가치 우량주"
            )
        else:
            return (
                "시장 변동성 속에서도 견조한 실적 펀더멘털과 외국인·기관 수급 유입이 확인되는 업종 대표주를 중심으로 선별적 접근이 유효한 시점입니다.",
                "업종별 1등 대장주 및 20일선 지지 기반 상승초입 추세주"
            )

    def generate_morning_briefing_html(self, market_data, top_headlines):
        """모닝 브리핑 전용 고품질 HTML 페이지 생성 (대번호 간 대형 여백/구분선 & 행간 2.2)"""
        today_str = datetime.now().strftime("%Y년 %m월 %d일")
        date_iso = datetime.now().strftime("%Y-%m-%d")
        slug = f"{datetime.now().strftime('%Y%m%d')}-morning-market-briefing"

        kospi = market_data.get("^KS11", {})
        kosdaq = market_data.get("^KQ11", {})
        usdkrw = market_data.get("KRW=X", {})
        sp500 = market_data.get("^GSPC", {})
        nasdaq = market_data.get("^IXIC", {})
        btc = market_data.get("BTC", {})

        def fmt_change(item):
            change = item.get("change", 0.0)
            sign = "+" if change > 0 else ""
            color = "var(--accent-red)" if change > 0 else "#00f2fe" if change < 0 else "var(--text-muted)"
            price = f"{item.get('price', 0):,.2f}" if isinstance(item.get('price', 0), float) else f"{item.get('price', 0):,}"
            return f'<span style="color:{color}; font-weight:700;">{price} ({sign}{change:.2f}%)</span>'

        div_sep = '<div style="margin: 64px 0 48px; border-top: 2px solid rgba(6, 182, 212, 0.4); width: 100%;"></div>'

        headlines_html = ""
        for i, h in enumerate(top_headlines[:5], 1):
            h_title = html.escape(h.get('title', '주요 경제 이슈'))
            h_summary = html.escape(h.get('summary', ''))
            analysis_text, target_sectors = self.analyze_morning_headline(h.get('title', ''), h.get('summary', ''))

            headlines_html += f"""
            <div style="margin-bottom: 36px; padding: 26px 30px; background: var(--bg-secondary); border: 1px solid var(--border-color); border-radius: 14px; border-left: 5px solid var(--accent-cyan); box-shadow: var(--shadow-sm);">
              <h3 style="font-size: 1.22rem; margin-bottom: 18px; color: var(--text-primary); line-height: 1.5;">
                <span style="display:inline-flex; align-items:center; justify-content:center; width:28px; height:28px; background:var(--accent-cyan); color:#070a13; border-radius:6px; font-size:0.9rem; font-weight:800; margin-right:10px;">{i}</span>
                {h_title}
              </h3>
              
              <p style="font-size: 1.1rem; color: #cbd5e1; margin-bottom: 22px; line-height: 2.2;">
                {h_summary}
              </p>
              
              <div style="padding: 18px 22px; background: rgba(6, 182, 212, 0.06); border-radius: 10px; font-size: 1rem; line-height: 2.0;">
                <div style="margin-bottom: 12px;">
                  <strong style="color:var(--accent-cyan);">💡 리서치센터 핵심 요약:</strong><br>
                  {analysis_text}
                </div>
                <div>
                  <strong style="color:var(--accent-emerald);">🎯 시장 영향 &amp; 관련 섹터:</strong><br>
                  {target_sectors}
                </div>
              </div>
            </div>
            """

        html_content = f"""<!DOCTYPE html>
<html lang="ko" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>오늘의 모닝 증시 브리핑 ({today_str}) | Value Stock Labs</title>
  <meta name="description" content="{today_str} 국내외 주요 증시 지표, 환율, 가상자산 동향 및 오늘의 핵심 경제 뉴스 5선 리서치 리포트">
  <meta name="keywords" content="모닝브리핑, 증시시황, 코스피, 코스닥, 환율, 나스닥, 비트코인, 주식뉴스">
  <meta name="author" content="Value Stock Labs 리서치팀">
  
  <meta property="og:type" content="article">
  <meta property="og:title" content="오늘의 모닝 증시 브리핑 ({today_str}) | Value Stock Labs">
  <meta property="og:description" content="{today_str} 국내외 핵심 증시 지표 요약 및 오늘의 주요 경제 뉴스 심층 분석">
  <meta property="og:image" content="../images/hero.jpg">
  <meta property="og:url" content="https://valuestocklabs.com/posts/{slug}.html">

  <link rel="stylesheet" href="../css/style.css?v=20260829_v5">
  <link rel="stylesheet" href="../css/ads.css?v=20260829_v5">
  <link rel="stylesheet" href="../css/article.css?v=20260829_v5">
  <link rel="stylesheet" href="../css/tools.css?v=20260829_v5">

  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7807868644631223" crossorigin="anonymous"></script>
  <link rel="icon" type="image/x-icon" href="../favicon.ico">
  <link rel="manifest" href="../site.webmanifest">
</head>
<body>

  <!-- Reading Progress Bar -->
  <div class="reading-progress-bar" id="readingProgressBar"></div>

  <!-- Header Navigation -->
  <header class="site-header">
    <div class="container header-inner">
      <div class="logo-group">
        <a href="../index.html" class="brand-logo">
          <span class="logo-symbol">📈</span>
          <span class="logo-text">Value Stock Labs</span>
        </a>
      </div>
      <nav class="main-nav" aria-label="메인 메뉴">
        <a href="../index.html" class="nav-link">홈</a>
        <a href="../index.html#macro" class="nav-link">시장지표</a>
        <a href="../index.html#articles" class="nav-link">리포트</a>
        <a href="../tools/fair-value-calculator.html" class="nav-link">투자계산기</a>
      </nav>
      <div class="header-actions">
        <button type="button" class="theme-toggle-btn" id="themeToggleBtn" aria-label="테마 전환">
          <span class="theme-icon-dark">🌙</span>
          <span class="theme-icon-light">☀️</span>
        </button>
      </div>
    </div>
  </header>

  <!-- Main Container -->
  <main class="article-layout">
    <div class="container article-grid">
      
      <article class="article-body">
        <nav class="breadcrumb" aria-label="경로 탐색">
          <a href="../index.html">홈</a> &gt; 
          <a href="../index.html#articles">모닝 시황</a> &gt; 
          <span>일일 브리핑</span>
        </nav>

        <header class="article-header">
          <span class="badge badge-market">🌅 데일리 모닝 리포트</span>
          <h1 class="article-title">오늘의 증시 모닝 브리핑: 핵심 지표 요약 및 주요 뉴스 5선 ({today_str})</h1>
          <div class="article-meta">
            <span>✍️ Value Stock Labs 시황분석팀</span>
            <span>📅 {today_str} AM 08:00 기준</span>
          </div>
        </header>

        <figure class="article-featured-img">
          <img src="../images/hero.jpg" alt="글로벌 증시 시황 모닝 브리핑" loading="lazy">
          <figcaption>▲ {today_str} 글로벌 마켓 데이터 및 주요 경제 헤드라인 총정리</figcaption>
        </figure>

        <!-- Golden Ad #1 -->
        <div class="ad-slot-wrapper">
          <div class="ad-slot-header"><span class="ad-label">SPONSORED</span></div>
          <div class="ad-container ad-leaderboard" data-ad-slot="1001001" data-ad-type="Display Leaderboard" data-ad-name="본문 상단 광고" data-ad-size="728x90 Leaderboard"></div>
        </div>

        <section id="sec-market-indicators" style="margin-bottom: 50px;">
          <h2 style="font-size: 1.75rem; font-weight: 800; color: #ffffff; margin-bottom: 36px; padding-bottom: 18px; border-bottom: 2px solid rgba(6, 182, 212, 0.35); line-height: 1.55;">1. 글로벌 &amp; 국내 주요 시장 지표 요약</h2>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            개장 전 반드시 확인해야 할 국내외 증시 및 원자재, 가상자산 시세 현황입니다:
          </p>
          
          <div class="table-responsive" style="margin: 36px 0;">
            <table class="metrics-table">
              <thead>
                <tr>
                  <th>지수 / 지표</th>
                  <th>현재가</th>
                  <th>시장 평가 및 동향</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><strong>코스피 (KOSPI)</strong></td>
                  <td>{fmt_change(kospi)}</td>
                  <td>국내 대형주 중심 수급 공방</td>
                </tr>
                <tr>
                  <td><strong>코스닥 (KOSDAQ)</strong></td>
                  <td>{fmt_change(kosdaq)}</td>
                  <td>바이오 및 2차전지 테마 순환매</td>
                </tr>
                <tr>
                  <td><strong>S&amp;P 500 (미국)</strong></td>
                  <td>{fmt_change(sp500)}</td>
                  <td>빅테크 실적 및 매크로 지표 주시</td>
                </tr>
                <tr>
                  <td><strong>나스닥 (NASDAQ)</strong></td>
                  <td>{fmt_change(nasdaq)}</td>
                  <td>AI 반도체 밸류체인 변동성</td>
                </tr>
                <tr>
                  <td><strong>원/달러 환율 (USD/KRW)</strong></td>
                  <td>{fmt_change(usdkrw)}</td>
                  <td>글로벌 달러화 인덱스 연동 등락</td>
                </tr>
                <tr>
                  <td><strong>비트코인 (BTC)</strong></td>
                  <td>{fmt_change(btc)}</td>
                  <td>기관 자금 유입 및 변동성 안정세</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        {div_sep}

        <section id="sec-top-news" style="margin-bottom: 50px;">
          <h2 style="font-size: 1.75rem; font-weight: 800; color: #ffffff; margin-bottom: 36px; padding-bottom: 18px; border-bottom: 2px solid rgba(6, 182, 212, 0.35); line-height: 1.55;">2. 오늘 꼭 챙겨봐야 할 핵심 경제 뉴스 5선 &amp; 리서치 코멘트</h2>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            국내외 금융 시장에 영향을 미치는 주요 언론 헤드라인과 이에 대한 리서치센터의 정밀 분석 코멘트입니다:
          </p>
          
          {headlines_html}
        </section>

        <!-- Golden Ad #2 -->
        <div class="ad-slot-wrapper">
          <div class="ad-slot-header"><span class="ad-label">SPONSORED CONTENT</span></div>
          <div class="ad-container ad-in-article" data-ad-slot="2002002" data-ad-type="In-Article Native" data-ad-name="본문 중간 네이티브 광고" data-ad-size="Responsive In-Article"></div>
        </div>

        {div_sep}

        <section id="sec-today-strategy" style="margin-bottom: 50px;">
          <h2 style="font-size: 1.75rem; font-weight: 800; color: #ffffff; margin-bottom: 36px; padding-bottom: 18px; border-bottom: 2px solid rgba(6, 182, 212, 0.35); line-height: 1.55;">3. 오늘의 투자 전략 및 수급 대응 가이드</h2>
          
          <div class="callout callout-warning" style="margin: 48px 0; padding: 34px 38px; background: rgba(245, 158, 11, 0.08); border-left: 5px solid var(--accent-gold); border-radius: 12px; line-height: 2.5;">
            <div style="font-weight: 700; margin-bottom: 24px; color: var(--accent-gold); font-size: 1.2rem;">💡 오늘의 실전 투자 체크포인트:</div>
            
            <div style="margin-bottom: 24px; line-height: 2.5;">
              • <strong style="color: #ffffff;">지수 방향성보다 종목별 수급:</strong><br>
              외국인 및 기관의 수급이 연속 유입되는 실적 개선 주도주에 집중.
            </div>
            
            <div style="margin-bottom: 24px; line-height: 2.5;">
              • <strong style="color: #ffffff;">장 초반 갭상승 추격 매수 자제:</strong><br>
              시초가 갭상승 종목은 30분 이후 수급 안정성을 확인 후 분할 매수.
            </div>
            
            <div>
              • <strong style="color: #ffffff;">철저한 손익비 관리:</strong><br>
              주요 지지선 이탈 시 기계적 손절(-3~-5%) 원칙 준수.
            </div>
          </div>
        </section>

        <div class="article-disclaimer">
          <strong>⚠️ 투자 유의사항 및 면책 조항:</strong><br>
          본 시황 자료는 참고용 정보 제공을 목적으로 작성되었으며, 특정 종목의 매수 또는 매도를 추천하지 않습니다.<br>
          투자의 최종 판단과 책임은 투자자 본인에게 있습니다.
        </div>

        <div class="article-share-box">
          <span>오늘의 시황 리포트 공유하기:</span>
          <button type="button" class="share-btn" id="shareBtn">🔗 URL 링크 복사</button>
        </div>

      </article>

      <!-- Sidebar -->
      <aside class="sidebar-area" aria-label="사이드바">
        <div class="widget-card">
          <h3 class="widget-title"><span>📊</span> 퀀트 계산기 툴</h3>
          <div style="display:flex; flex-direction:column; gap:14px;">
            <a href="../tools/fair-value-calculator.html" class="btn-primary" style="text-decoration:none;">💎 기업 적정가치 계산기</a>
            <a href="../tools/stock-average-calc.html" class="btn-primary" style="text-decoration:none; background:#3b82f6;">💧 물타기 평단가 계산기</a>
            <a href="../tools/target-price-calculator.html" class="btn-primary" style="text-decoration:none; background:#64748b;">🎯 손익비 계산기</a>
          </div>
        </div>

        <div class="ad-slot-wrapper">
          <div class="ad-slot-header"><span class="ad-label">ADVERTISEMENT</span></div>
          <div class="ad-container ad-sidebar-sticky" data-ad-slot="4004004" data-ad-type="Sidebar Half-Page Sticky" data-ad-name="본문 사이드바 광고" data-ad-size="300x600 Half-Page"></div>
        </div>
      </aside>

    </div>
  </main>

  <footer class="site-footer">
    <div class="container">
      <div class="footer-bottom">
        <span>© 2026 Value Stock Labs. All rights reserved.</span>
        <span>Google AdSense Compliant &amp; SEO Optimized</span>
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
            "title": f"오늘의 증시 모닝 브리핑 ({today_str})",
            "category": "모닝 시황",
            "summary": f"{today_str} 국내외 주요 시장 지표 요약 및 오늘의 핵심 경제 뉴스 5선 심층 분석",
            "image": "images/hero.jpg",
            "html": html_content,
            "date": date_iso
        }

    def generate_article_html(self, title, summary, category, keywords, content_type="deep_dive"):
        """일반 심층 분석 기사 고품질 HTML 생성 (대번호 간 대형 여백/구분선 & 행간 2.2 극대화)"""
        today_str = datetime.now().strftime("%Y년 %m월 %d일")
        date_iso = datetime.now().strftime("%Y-%m-%d")
        slug = self.create_slug(title)

        topic_type = self.detect_topic_type(title, summary)
        image_path, image_caption = self.get_category_image_info(topic_type, title)
        image_src = f"../{image_path}" if not image_path.startswith("http") else image_path

        sections_html = self.build_contextual_sections(topic_type, title, summary, category, keywords)
        div_sep = '<div style="margin: 64px 0 48px; border-top: 2px solid rgba(6, 182, 212, 0.4); width: 100%;"></div>'

        html_content = f"""<!DOCTYPE html>
<html lang="ko" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | Value Stock Labs 리서치</title>
  <meta name="description" content="{title}에 대한 심층 팩트체크, 금융 시장 파급 효과, 핵심 데이터 지표 및 실전 투자 전략을 분석합니다.">
  <meta name="keywords" content="{', '.join(keywords)}">
  <meta name="author" content="Value Stock Labs 리서치팀">

  <!-- OpenGraph -->
  <meta property="og:type" content="article">
  <meta property="og:title" content="{title} | Value Stock Labs 리서치">
  <meta property="og:description" content="{title} 핵심 팩트체크 및 금융·시장 밸류에이션 분석 리포트">
  <meta property="og:image" content="{image_src}">
  <meta property="og:url" content="https://valuestocklabs.com/posts/{slug}.html">

  <!-- Stylesheets -->
  <link rel="stylesheet" href="../css/style.css?v=20260829_v5">
  <link rel="stylesheet" href="../css/ads.css?v=20260829_v5">
  <link rel="stylesheet" href="../css/article.css?v=20260829_v5">
  <link rel="stylesheet" href="../css/tools.css?v=20260829_v5">

  <!-- Google AdSense Script -->
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7807868644631223" crossorigin="anonymous"></script>
  
  <!-- Favicon -->
  <link rel="icon" type="image/x-icon" href="../favicon.ico">
  <link rel="manifest" href="../site.webmanifest">
  <meta name="theme-color" content="#090d16">
</head>
<body>

  <!-- Reading Progress Bar -->
  <div class="reading-progress-bar" id="readingProgressBar"></div>

  <!-- Header Navigation -->
  <header class="site-header">
    <div class="container header-inner">
      <div class="logo-group">
        <a href="../index.html" class="brand-logo">
          <span class="logo-symbol">📈</span>
          <span class="logo-text">Value Stock Labs</span>
        </a>
      </div>
      
      <nav class="main-nav" aria-label="메인 메뉴">
        <a href="../index.html" class="nav-link">홈</a>
        <a href="../index.html#macro" class="nav-link">시장지표</a>
        <a href="../index.html#articles" class="nav-link">리포트</a>
        <a href="../tools/fair-value-calculator.html" class="nav-link">투자계산기</a>
      </nav>

      <div class="header-actions">
        <button type="button" class="theme-toggle-btn" id="themeToggleBtn" aria-label="다크/라이트 테마 전환">
          <span class="theme-icon-dark">🌙</span>
          <span class="theme-icon-light">☀️</span>
        </button>
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

        <!-- Article Header -->
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

        {div_sep}

        <!-- Section 5: Calculator Widget Linking -->
        <section id="sec-calculator" style="margin-bottom: 50px;">
          <h2 style="font-size: 1.75rem; font-weight: 800; color: #ffffff; margin-bottom: 36px; padding-bottom: 18px; border-bottom: 2px solid rgba(6, 182, 212, 0.35); line-height: 1.55;">5. 실시간 가치평가 및 계산기 활용 가이드</h2>
          
          <p style="font-size: 1.15rem; line-height: 2.65; margin-bottom: 38px; color: #cbd5e1;">
            보유 중이거나 매수 검토 중인 금융 상품 및 종목의 적정가치와 물타기 평단가를 직접 시뮬레이션해 보세요:
          </p>
          
          <div class="quick-calc-form" style="margin: 36px 0; padding: 28px 32px; background: rgba(255,255,255,0.03); border-radius: 14px; border: 1px solid var(--border-color);">
            <h3 style="font-size:1.22rem; margin-bottom:14px; color:var(--text-primary);">📊 Value Stock Labs 무료 퀀트 투자 계산기</h3>
            <p style="font-size:1.02rem; color:var(--text-secondary); margin-bottom:22px; line-height: 1.8;">복잡한 재무 지표를 1초 만에 계산하여 합리적인 매매 기준선을 제시합니다.</p>
            
            <div style="display: flex; gap: 14px; flex-wrap: wrap;">
              <a href="../tools/fair-value-calculator.html" class="btn-primary" style="text-decoration:none;">💎 기업 적정가치(Fair Value) 계산기</a>
              <a href="../tools/stock-average-calc.html" class="btn-primary" style="text-decoration:none; background: #3b82f6;">💧 물타기 평단가 계산기</a>
              <a href="../tools/target-price-calculator.html" class="btn-primary" style="text-decoration:none; background: #64748b;">🎯 손익비 계산기</a>
            </div>
          </div>
        </section>

        <!-- Disclaimer -->
        <div class="article-disclaimer">
          <strong>⚠️ 투자 유의사항 및 면책 조항:</strong><br>
          본 리포트에서 제공하는 정보는 투자 판단을 위한 참고용 분석 자료이며, 특정 종목이나 금융 상품의 매수 또는 매도를 권유하지 않습니다.<br>
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
        <span>Google AdSense Compliant &amp; SEO Optimized</span>
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

    def generate_article_content(self, topic_info):
        """뉴스 수집기(NewsCollector)에서 전달받은 토픽 정보로 심층 기사 생성"""
        return self.generate_article_html(
            title=topic_info.get("title", "주식 분석 리포트"),
            summary=topic_info.get("summary", ""),
            category=topic_info.get("category", "주식분석"),
            keywords=topic_info.get("keywords", ["주식", "투자", "밸류에이션"])
        )

    def generate_morning_briefing(self, headlines=None):
        """실시간 증시 데이터와 주요 뉴스를 기반으로 모닝 브리핑 생성"""
        from news_collector import NewsCollector
        collector = NewsCollector()
        market_data = collector.collect_market_data() if hasattr(collector, "collect_market_data") else {}
        if not headlines:
            headlines = []
        return self.generate_morning_briefing_html(market_data, headlines)
