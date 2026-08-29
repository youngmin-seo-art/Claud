"""
=============================================================================
BLOG PUBLISHER (blog_publisher.py)
adsense-stock-blog 자동 포스팅 저장, index/sitemap/rss 동기화, 이력 기록 및 Git Auto-Deploy
=============================================================================
"""

import os
import sys
import re
import json
import subprocess
import xml.etree.ElementTree as ET
from datetime import datetime

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from config import BLOG_DIR, POSTS_DIR, INDEX_HTML, SITEMAP_XML, RSS_XML, BLOG_DOMAIN, PROJECT_ROOT, HISTORY_FILE

class BlogPublisher:
    def __init__(self):
        POSTS_DIR.mkdir(parents=True, exist_ok=True)

    def publish_post(self, article_data, auto_push=True):
        """1. HTML 포스트 저장, 2. sitemap.xml 갱신, 3. rss.xml 갱신, 4. index.html 갱신, 5. 발행 이력 기록, 6. Git Push"""
        filename = article_data["filename"]
        target_path = POSTS_DIR / filename
        
        # 1. 파일 저장
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(article_data["html"])
        print(f"[성공] 신규 분석글 저장 완료: {target_path}")

        # 2. sitemap.xml 갱신
        self.update_sitemap(filename, article_data["date"])

        # 3. rss.xml 갱신
        self.update_rss(article_data)

        # 4. index.html 최신 글 목록에 카드 추가 및 시황 세션 링크 갱신
        self.update_index_html(article_data)

        # 5. 발행 이력 누적 저장 (중복 방지용)
        self.record_published_history(article_data)

        # 6. Git Push 자동 배포
        if auto_push:
            self.git_push(article_data["title"])

        return f"{BLOG_DOMAIN}/posts/{filename}"

    def record_published_history(self, article_data):
        """발행된 기사 목록을 published_history.json에 누적 저장"""
        try:
            history = []
            if HISTORY_FILE.exists():
                try:
                    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                        history = json.load(f)
                except Exception:
                    history = []

            # 중복 체크 후 추가
            existing_filenames = {item.get("filename") for item in history if isinstance(item, dict)}
            if article_data["filename"] not in existing_filenames:
                history.append({
                    "title": article_data["title"],
                    "filename": article_data["filename"],
                    "date": article_data.get("date", datetime.now().strftime("%Y-%m-%d")),
                    "category": article_data.get("category", "주식분석"),
                    "published_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                # 최근 200개만 유지
                if len(history) > 200:
                    history = history[-200:]

                with open(HISTORY_FILE, "w", encoding="utf-8") as f:
                    json.dump(history, f, ensure_ascii=False, indent=2)
                print(f"[성공] published_history.json에 발행 이력 기록 완료 ({len(history)}건 누적)")
        except Exception as e:
            print(f"[경고] 발행 이력 기록 실패: {e}")

    def update_sitemap(self, filename, date_str):
        """sitemap.xml에 신규 URL 추가"""
        try:
            with open(SITEMAP_XML, "r", encoding="utf-8") as f:
                content = f.read()

            post_url = f"{BLOG_DOMAIN}/posts/{filename}"
            if post_url not in content:
                new_entry = f"""  <url>
    <loc>{post_url}</loc>
    <lastmod>{date_str}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
</urlset>"""
                content = content.replace("</urlset>", new_entry)
                with open(SITEMAP_XML, "w", encoding="utf-8") as f:
                    f.write(content)
                print("[성공] sitemap.xml에 신규 포스트 등록 완료")
        except Exception as e:
            print(f"[경고] sitemap.xml 갱신 실패: {e}")

    def update_rss(self, article_data):
        """rss.xml에 신규 아이템 추가"""
        try:
            with open(RSS_XML, "r", encoding="utf-8") as f:
                content = f.read()

            post_url = f"{BLOG_DOMAIN}/posts/{article_data['filename']}"
            if post_url not in content:
                pub_date = datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0900")
                desc = article_data.get("summary", f"{article_data['title']} 밸류에이션 및 기술적 분석 리포트")
                new_item = f"""    <item>
      <title>{article_data['title']}</title>
      <link>{post_url}</link>
      <guid>{post_url}</guid>
      <pubDate>{pub_date}</pubDate>
      <description>{desc}</description>
    </item>
  </channel>"""
                content = content.replace("  </channel>", new_item)
                with open(RSS_XML, "w", encoding="utf-8") as f:
                    f.write(content)
                print("[성공] rss.xml에 신규 피드 등록 완료")
        except Exception as e:
            print(f"[경고] rss.xml 갱신 실패: {e}")

    def update_index_html(self, article_data):
        """index.html 아티클 그리드 상단에 신규 포스팅 카드 삽입 및 시황 섹션 최신화 (읽는 시간 메타 제거)"""
        try:
            with open(INDEX_HTML, "r", encoding="utf-8") as f:
                content = f.read()

            is_morning = article_data.get("is_morning", False) or "시황" in article_data["title"] or article_data.get("category") == "market"
            
            if is_morning:
                category = "market"
                badge_html = '<span class="post-badge market" style="background:#059669; color:#fff;">☕ 모닝 시황</span>'
                thumb_img = "images/hero.jpg"
                author = "시황분석팀"
                avatar = "M"
                excerpt = f"{article_data['title']} - 밤사이 뉴욕증시 마감 및 거시경제 지표, 장 시작 전 국내 핵심 주도 섹터와 주요 뉴스 총정리."
                
                # 상단 오늘의 시황 세션 링크 및 날짜 갱신
                content = re.sub(
                    r'<a href="posts/[^"]+" class="briefing-btn" id="latestBriefingLink">',
                    f'<a href="posts/{article_data["filename"]}" class="briefing-btn" id="latestBriefingLink">',
                    content
                )
                today_display = datetime.now().strftime("%Y.%m.%d")
                content = re.sub(
                    r'<span class="briefing-date" id="briefingDate">[^<]+</span>',
                    f'<span class="briefing-date" id="briefingDate">{today_display} 08:00 AM 업데이트</span>',
                    content
                )
            else:
                raw_cat = article_data.get("category", "")
                if "반도체" in article_data["title"] or "HBM" in article_data["title"] or raw_cat == "semiconductor" or "AI" in raw_cat:
                    category = "semiconductor"
                    badge_html = '<span class="post-badge breakout">⚡ AI 반도체</span>'
                    thumb_img = "images/semiconductor.jpg"
                    author = "반도체테크"
                    avatar = "H"
                elif "공모주" in article_data["title"] or raw_cat == "ipo" or "청약" in article_data["title"]:
                    category = "ipo"
                    badge_html = '<span class="post-badge tax">🎯 공모주 청약</span>'
                    thumb_img = "images/ipo.jpg"
                    author = "공모주애널"
                    avatar = "I"
                elif "배당" in article_data["title"] or "절세" in article_data["title"] or raw_cat == "dividend":
                    category = "dividend"
                    badge_html = '<span class="post-badge dividend">💰 배당/절세</span>'
                    thumb_img = "images/dividend.jpg"
                    author = "배당인컴"
                    avatar = "D"
                elif "금리" in article_data["title"] or "대출" in article_data["title"] or "거시" in raw_cat:
                    category = "macro"
                    badge_html = '<span class="post-badge market" style="background:#0284c7; color:#fff;">📊 거시경제/금리</span>'
                    thumb_img = "images/dividend.jpg"
                    author = "매크로리서치"
                    avatar = "M"
                elif "상승" in article_data["title"] or "돌파" in article_data["title"] or raw_cat == "breakout":
                    category = "breakout"
                    badge_html = '<span class="post-badge breakout">🚀 상승초입주</span>'
                    thumb_img = "images/breakout.jpg"
                    author = "차트마스터"
                    avatar = "C"
                else:
                    category = "undervalued"
                    badge_html = '<span class="post-badge undervalued">💎 저평가 가치주</span>'
                    thumb_img = "images/hero.jpg"
                    author = "스톡리서치"
                    avatar = "S"

                excerpt = article_data.get("summary", f"{article_data['title']}에 대한 퀀트 재무 지표 및 기술적 차트 지지선 분석 리포트입니다.")

            # 고유 썸네일 이미지 우선 적용 (글마다 다른 사진 사용)
            if article_data.get("image"):
                thumb_img = article_data["image"]

            card_html = f"""          <!-- Auto-Generated Article -->
          <article class="post-card" data-category="{category}">
            <div class="post-thumb-wrap">
              {badge_html}
              <img src="{thumb_img}" class="post-thumb" alt="{article_data['title']}" loading="lazy">
            </div>
            <div class="post-body">
              <div class="post-meta">
                <span>📅 {article_data['date']}</span>
                <span>🔥 NEW</span>
              </div>
              <h3 class="post-title">
                <a href="posts/{article_data['filename']}">{article_data['title']}</a>
              </h3>
              <p class="post-excerpt">
                {excerpt}
              </p>
              <div class="post-footer">
                <div class="author-chip">
                  <div class="author-avatar">{avatar}</div>
                  <span>{author}</span>
                </div>
                <a href="posts/{article_data['filename']}" class="read-more-link">리포트 읽기 →</a>
              </div>
            </div>
          </article>
"""
            # <div class="posts-grid" id="postsGrid"> 바로 아래에 삽입
            target = '<div class="posts-grid" id="postsGrid">'
            posts_grid_part = content.split(target)[1] if target in content else ""
            
            if target in content and f'posts/{article_data["filename"]}' not in posts_grid_part:
                content = content.replace(target, f"{target}\n{card_html}")
                with open(INDEX_HTML, "w", encoding="utf-8") as f:
                    f.write(content)
                print("[성공] index.html 메인 화면에 신규 아티클 카드 및 링크 반영 완료")
            else:
                with open(INDEX_HTML, "w", encoding="utf-8") as f:
                    f.write(content)
                print("[성공] index.html 메인 화면 시황 링크 최신화 완료")
        except Exception as e:
            print(f"[경고] index.html 갱신 실패: {e}")

    def git_push(self, title):
        """변경사항을 Git에 자동 커밋 및 Push하여 Vercel 실시간 배포"""
        try:
            print("[진행 중] Git 커밋 및 Vercel 실시간 배포 중...")
            subprocess.run(["git", "add", "adsense-stock-blog", "stock-blog-agent/published_history.json"], cwd=PROJECT_ROOT, check=True)
            subprocess.run(["git", "commit", "-m", f"feat(agent): 신규 주식 분석글 자동 발행 - {title[:30]}"], cwd=PROJECT_ROOT, check=True)
            subprocess.run(["git", "push", "origin", "main"], cwd=PROJECT_ROOT, check=True)
            print("🚀 [배포 완료] valuestocklabs.com에 실시간 라이브 반영 완료!")
        except Exception as e:
            print(f"[알림] Git Push 실행 건너뜀 (로컬 저장 유지): {e}")

if __name__ == "__main__":
    publisher = BlogPublisher()
    print("BlogPublisher 모듈 정상 로드 완료")
