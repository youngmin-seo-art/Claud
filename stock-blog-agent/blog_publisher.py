"""
=============================================================================
BLOG PUBLISHER (blog_publisher.py)
adsense-stock-blog 자동 포스팅 저장, index/sitemap/rss 동기화 및 Git Auto-Deploy
=============================================================================
"""

import os
import sys
import subprocess
import xml.etree.ElementTree as ET
from datetime import datetime

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from config import BLOG_DIR, POSTS_DIR, INDEX_HTML, SITEMAP_XML, RSS_XML, BLOG_DOMAIN, PROJECT_ROOT

class BlogPublisher:
    def __init__(self):
        POSTS_DIR.mkdir(parents=True, exist_ok=True)

    def publish_post(self, article_data, auto_push=True):
        """1. HTML 포스트 저장, 2. index.html 갱신, 3. sitemap.xml 갱신, 4. rss.xml 갱신, 5. Git Push"""
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

        # 4. index.html 최신 글 목록에 카드 추가
        self.update_index_html(article_data)

        # 5. Git Push 자동 배포
        if auto_push:
            self.git_push(article_data["title"])

        return f"{BLOG_DOMAIN}/posts/{filename}"

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
                new_item = f"""    <item>
      <title>{article_data['title']}</title>
      <link>{post_url}</link>
      <guid>{post_url}</guid>
      <pubDate>{pub_date}</pubDate>
      <description>{article_data['title']} 밸류에이션 및 기술적 매매 분석 리포트</description>
    </item>
  </channel>"""
                content = content.replace("  </channel>", new_item)
                with open(RSS_XML, "w", encoding="utf-8") as f:
                    f.write(content)
                print("[성공] rss.xml에 신규 피드 등록 완료")
        except Exception as e:
            print(f"[경고] rss.xml 갱신 실패: {e}")

    def update_index_html(self, article_data):
        """index.html 아티클 그리드 상단에 신규 포스팅 카드 삽입"""
        try:
            with open(INDEX_HTML, "r", encoding="utf-8") as f:
                content = f.read()

            card_html = f"""        <!-- Auto-Generated Latest Article -->
        <article class="article-card" data-category="semiconductor">
          <div class="card-thumb">
            <img src="images/hero.jpg" alt="{article_data['title']}" loading="lazy">
            <span class="badge badge-semiconductor">NEW 실시간 분석</span>
          </div>
          <div class="card-body">
            <div class="card-meta">
              <span>📅 {article_data['date']}</span>
              <span>⏱️ 6분 정독</span>
            </div>
            <h3 class="card-title">
              <a href="posts/{article_data['filename']}">{article_data['title']}</a>
            </h3>
            <p class="card-excerpt">
              {article_data['title']}에 대한 퀀트 재무 지표 및 기술적 차트 지지선 분석 리포트입니다.
            </p>
            <div class="card-footer">
              <span class="card-author">Value Stock Labs 리서치팀</span>
              <a href="posts/{article_data['filename']}" class="card-link">리포트 읽기 →</a>
            </div>
          </div>
        </article>

"""
            # <div class="articles-grid" id="articlesGrid"> 바로 아래에 삽입
            target = '<div class="articles-grid" id="articlesGrid">'
            if target in content and article_data['filename'] not in content:
                content = content.replace(target, f"{target}\n{card_html}")
                with open(INDEX_HTML, "w", encoding="utf-8") as f:
                    f.write(content)
                print("[성공] index.html 메인 화면에 신규 아티클 카드 반영 완료")
        except Exception as e:
            print(f"[경고] index.html 갱신 실패: {e}")

    def git_push(self, title):
        """변경사항을 Git에 자동 커밋 및 Push하여 Vercel 실시간 배포"""
        try:
            print("[진행 중] Git 커밋 및 Vercel 실시간 배포 중...")
            subprocess.run(["git", "add", "adsense-stock-blog"], cwd=PROJECT_ROOT, check=True)
            subprocess.run(["git", "commit", "-m", f"feat(agent): 신규 주식 분석글 자동 발행 - {title[:30]}"], cwd=PROJECT_ROOT, check=True)
            subprocess.run(["git", "push", "origin", "main"], cwd=PROJECT_ROOT, check=True)
            print("🚀 [배포 완료] valuestocklabs.com에 실시간 라이브 반영 완료!")
        except Exception as e:
            print(f"[알림] Git Push 실행 건너뜀 (로컬 저장 유지): {e}")

if __name__ == "__main__":
    publisher = BlogPublisher()
    print("BlogPublisher 모듈 정상 로드 완료")
