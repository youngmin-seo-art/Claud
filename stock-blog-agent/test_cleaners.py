from news_collector import NewsCollector
from article_generator import ArticleGenerator
import re

collector = NewsCollector()
generator = ArticleGenerator()

# 1. Test clean_title stripping duplicate media source and bracket dates
test_titles = [
    ('리서치센터장 "빅테크 AI투자 확인·반도체 실적·금리우려 완화, 증시반등 조건" - 머니투데이 - 머니투데이', '리서치센터장 "빅테크 AI투자 확인·반도체 실적·금리우려 완화, 증시반등 조건"'),
    ('미국 정말 금리 올릴까‥"반도체 실적·환율 변수 등 돌다리 두드려야" - MBC 뉴스', '미국 정말 금리 올릴까‥"반도체 실적·환율 변수 등 돌다리 두드려야"'),
    ('[4월 27일](국장 마감) 코스피 6,600선 돌파! 외국인·기관 2.5조 쌍끌이 매수와 \'반도체 파티\' - 네이버 프리미엄콘텐츠', '코스피 6,600선 돌파! 외국인·기관 2.5조 쌍끌이 매수와 \'반도체 파티\''),
    ('[속보] 코스피 2700 돌파 - 한국경제', '코스피 2700 돌파'),
]

for raw, expected in test_titles:
    cleaned = collector.clean_title(raw)
    assert cleaned == expected, f"Expected '{expected}', got '{cleaned}'"
    print(f"✅ Title Cleaned: '{raw}' -> '{cleaned}'")

# 2. Test duplicate year prevention
raw_kw = "2026 현대차 인도법인 상장 및 수혜주"
clean_kw = re.sub(r'^(202[4-9]|2030)\s*', '', raw_kw).strip()
title = f"2026 {clean_kw} 실전 수혜주 분석 및 적정주가 밸류에이션 리포트"
assert "2026 2026" not in title, f"Duplicate year found: {title}"
print(f"✅ Year Deduplication OK: '{title}'")

# 3. Test slug generation
slug = generator.create_slug(title)
assert not slug.startswith("2026-2026-"), f"Bad slug prefix: {slug}"
print(f"✅ Slug Clean: '{slug}'")

# 4. Test negative filtering for geopolitical noise
geo_item = {
    'title': '이란 안보수장 "미국 신뢰하지 않아…역사에 남을 재앙 가할 것"',
    'summary': '이란 안보수장이 미국을 향해 강경 발언을 쏟아냈다.'
}
score = collector.score_news(geo_item)
assert score <= 0, f"Geopolitical news should receive zero or negative score, got {score}"
print(f"✅ Geopolitical Negative Score Filter: score = {score}")

print("\n🎉 ALL UNIT TESTS PASSED!")

