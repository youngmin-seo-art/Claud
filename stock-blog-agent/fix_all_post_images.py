import os
import re
import glob
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS_DIR = os.path.join(BASE_DIR, "adsense-stock-blog", "posts")
INDEX_FILE = os.path.join(BASE_DIR, "adsense-stock-blog", "index.html")

# Mapping specific posts to curated, 100% unique photos
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
    "20260828-가계-기업-대출금리-양극화-예대금리차-확대-분석.html": "images/macro-2.jpg",
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

def update_posts():
    print("🔄 Updating all individual post HTML files with distinct images...")
    for post_file, img_path in POST_IMAGE_MAPPING.items():
        full_path = os.path.join(POSTS_DIR, post_file)
        if not os.path.exists(full_path):
            print(f"  [스킵] {post_file} not found")
            continue
            
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # 1. OpenGraph Image 태그 교체
        content = re.sub(
            r'<meta property="og:image" content="[^"]+">',
            f'<meta property="og:image" content="../{img_path}">',
            content
        )
        
        # 2. 본문 상단 메인 이미지 교체 (article-body 내 첫 번째 img)
        content = re.sub(
            r'<img src="(\.\./)?images/[^"]+"([^>]*class="[^"]*post-thumb[^"]*"[^>]*)?>',
            f'<img src="../{img_path}"\\2>',
            content,
            count=1
        )
        
        # 3. figure 내 썸네일 이미지 교체
        content = re.sub(
            r'<figure class="article-thumb">\s*<img src="[^"]+"',
            f'<figure class="article-thumb">\n          <img src="../{img_path}"',
            content
        )
        
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  [성공] {post_file} -> ../{img_path}")

def update_index():
    print("🔄 Updating index.html cards with distinct images...")
    if not os.path.exists(INDEX_FILE):
        return
        
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        content = f.read()
        
    for post_file, img_path in POST_IMAGE_MAPPING.items():
        # post-card 내부의 href와 img를 찾아 교체
        # 패턴: <a href="posts/{post_file}"> 가 포함된 카드 내의 <img src="images/..."
        # 각 카드 블록을 정규식으로 치환
        card_pattern = rf'(<article class="post-card"[^>]*>[\s\S]*?<img src=")[^"]+("[\s\S]*?<a href="posts/{re.escape(post_file)}")'
        if re.search(card_pattern, content):
            content = re.sub(card_pattern, rf'\g<1>{img_path}\g<2>', content)
            print(f"  [카드 갱신] {post_file} -> {img_path}")
            
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write(content)
    print("  [성공] index.html 모든 포스트 카드 고유 사진 매핑 완료!")

if __name__ == "__main__":
    update_posts()
    update_index()
