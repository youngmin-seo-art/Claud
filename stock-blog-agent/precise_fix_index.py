import os
import re
import sys
import hashlib

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_FILE = os.path.join(BASE_DIR, "adsense-stock-blog", "index.html")
POSTS_DIR = os.path.join(BASE_DIR, "adsense-stock-blog", "posts")

POST_IMAGE_MAPPING = {
    # 1. AI 반도체 & HBM 포스트별 각각 다른 고유 실사 사진
    "20260829-2026-삼성전자-hbm4-차세대-패키징-수혜주-실전-수혜주-분석-및-적.html": "images/semiconductor-1.jpg",
    "20260829-2026-빅테크-ai-반도체-hbm-수혜주-및-증시-반등-.html": "images/semiconductor-2.jpg",
    "20260828-sk하이닉스-미-인디애나서-hbm-첫-생산2029년-양.html": "images/semiconductor-3.jpg",
    "ai-semiconductor-hbm-stocks.html": "images/semiconductor-4.jpg",
    
    # 2. 증시 마감 & 코스피 6600 돌파 & 리서치센터장 리포트 각각 다른 사진
    "20260829-4월-27일국장-마감-코스피-6600선-돌파-외국인기관-2.html": "images/market-1.jpg",
    "20260829-리서치센터장-빅테크-ai투자-확인반도체-실적금리우려-완화-.html": "images/market-2.jpg",
    "20260829-미국-정말-금리-올릴까반도체-실적환율-변수-등-돌다리-두드.html": "images/macro-1.jpg",
    "20260828-월급쟁이가-그저-봉이지대출금리-기업은-내리고-가계는-올.html": "images/macro-2.jpg",
    "20260829-월급쟁이가-그저-봉이지대출금리-기업은-내리고-가계는-올.html": "images/macro-3.jpg",
    "20260828-2026-현대차-로보틱스-자율주행-실전-수혜주-분석-및.html": "images/battery-1.jpg",
    
    # 3. 모닝 시황 브리핑 날짜별 다른 사진
    "20260829-morning-market-briefing.html": "images/morning-1.jpg",
    "20260828-morning-market-briefing.html": "images/morning-2.jpg",
    
    # 4. 정적 분석 기사들 각각 다른 사진
    "undervalued-stocks-2026.html": "images/market-4.jpg",
    "breakout-stocks-guide.html": "images/breakout-1.jpg",
    "dividend-aristocrats-krx.html": "images/dividend-1.jpg",
    "ipo-public-offering-guide.html": "images/ipo-1.jpg",
    "isa-irp-tax-saving.html": "images/tax-1.jpg",
}

def update_index_cards():
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Split by </article> to process each card independently
    parts = content.split("</article>")
    new_parts = []

    for idx, part in enumerate(parts):
        if "<article class=\"post-card\"" in part:
            # Find the post filename in the title link
            m = re.search(r'<h3 class="post-title">\s*<a href="posts/([^"]+)"', part)
            if not m:
                m = re.search(r'href="posts/([^"]+)"', part)
            if m:
                filename = m.group(1)
                img = POST_IMAGE_MAPPING.get(filename)
                if not img:
                    # Fallback hash selection
                    h = int(hashlib.md5(filename.encode('utf-8')).hexdigest(), 16)
                    pool = ["images/market-1.jpg", "images/market-2.jpg", "images/semiconductor-1.jpg", "images/breakout-1.jpg"]
                    img = pool[h % len(pool)]
                
                # Replace img src in this card
                part = re.sub(r'<img src="[^"]+" class="post-thumb"', f'<img src="{img}" class="post-thumb"', part)
                print(f"[{idx}] {filename} => {img}")
        new_parts.append(part)

    new_content = "</article>".join(new_parts)
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("✅ index.html 카드별 고유 이미지 치환 완료!")

if __name__ == "__main__":
    update_index_cards()
