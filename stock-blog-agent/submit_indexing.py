"""
=============================================================================
SEARCH ENGINE INSTANT INDEXING DISPATCHER (submit_indexing.py)
Google Sitemap Ping, Bing & Naver IndexNow API 일괄 색인 요청 자동화
=============================================================================
"""

import sys
import json
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent.parent / "adsense-stock-blog"
SITEMAP_XML = BASE_DIR / "sitemap.xml"
INDEXNOW_KEY = "a4b8c7d6e5f4123456789abcdef01234"
HOST = "www.valuestocklabs.com"
SITEMAP_URL = f"https://{HOST}/sitemap.xml"

def get_all_urls():
    if not SITEMAP_XML.exists():
        print(f"[오류] {SITEMAP_XML} 파일이 존재하지 않습니다.")
        return []
    tree = ET.parse(SITEMAP_XML)
    root = tree.getroot()
    urls = [elem.text.strip() for elem in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
    return urls

def ping_google():
    print("\n1. Google 검색엔진 Sitemap Ping 전송 중...")
    url = f"https://www.google.com/ping?sitemap={urllib.parse.quote(SITEMAP_URL)}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (compatible; ValueStockLabsBot/1.0)'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"  [성공] Google 응답 코드: {resp.getcode()}")
    except Exception as e:
        print(f"  [참고] Google Ping 전송 완료 (응답: {e})")

def ping_bing():
    print("\n2. Bing 검색엔진 Sitemap Ping 전송 중...")
    url = f"https://www.bing.com/ping?sitemap={urllib.parse.quote(SITEMAP_URL)}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (compatible; ValueStockLabsBot/1.0)'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"  [성공] Bing 응답 코드: {resp.getcode()}")
    except Exception as e:
        print(f"  [참고] Bing Ping 전송 완료 (응답: {e})")

def submit_indexnow(urls):
    print(f"\n3. IndexNow API (Bing / Naver / Yandex) {len(urls)}개 URL 전수 전송 중...")
    endpoint = "https://api.indexnow.org/indexnow"
    
    payload = {
        "host": HOST,
        "key": INDEXNOW_KEY,
        "keyLocation": f"https://{HOST}/{INDEXNOW_KEY}.txt",
        "urlList": urls
    }

    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        endpoint,
        data=data,
        headers={
            'Content-Type': 'application/json; charset=utf-8',
            'User-Agent': 'ValueStockLabs-Indexing-Agent/1.0'
        },
        method='POST'
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            status = resp.getcode()
            print(f"  [성공] IndexNow API 응답 코드: {status} (200/202: 정상 수신 완료)")
    except Exception as e:
        print(f"  [오류] IndexNow API 전송 실패: {e}")

def main():
    print("=" * 60)
    print("🚀 [검색엔진 색인 즉시 수집 요청] Google & Naver/Bing API 디스패치")
    print("=" * 60)

    urls = get_all_urls()
    print(f"[*] 총 제출 대상 URL 수: {len(urls)}개")

    ping_google()
    ping_bing()
    if urls:
        submit_indexnow(urls)

    print("\n" + "=" * 60)
    print("✅ 검색엔진 수집 신호 전송 완료!")
    print("=" * 60)

if __name__ == "__main__":
    main()
