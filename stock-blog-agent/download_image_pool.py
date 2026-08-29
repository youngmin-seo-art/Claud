import urllib.request
import os
import json
import hashlib
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

IMAGE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "adsense-stock-blog", "images")
os.makedirs(IMAGE_DIR, exist_ok=True)

# Curated high-res Unsplash stock photos for financial blog
IMAGE_CATALOG = {
    # 1. AI Semiconductor & Hardware (4 distinct images)
    "semiconductor-1.jpg": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=1200&q=85", # Macro circuit board & chip
    "semiconductor-2.jpg": "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=1200&q=85", # Cyber futuristic hardware
    "semiconductor-3.jpg": "https://images.unsplash.com/photo-1591488320449-011701bb6704?w=1200&q=85", # GPU processor microchip
    "semiconductor-4.jpg": "https://images.unsplash.com/photo-1555680202-c86f0e12f086?w=1200&q=85", # Glowing microchips & tech

    # 2. Market & Macro Trading Floor (4 distinct images)
    "market-1.jpg": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=1200&q=85", # Stock chart on screen
    "market-2.jpg": "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=1200&q=85", # Multi-monitor trading desk
    "market-3.jpg": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=1200&q=85", # Financial district towers
    "market-4.jpg": "https://images.unsplash.com/photo-1535320903710-d993d3d77d29?w=1200&q=85", # Financial city skyline

    # 3. Morning Briefing & News (3 distinct images)
    "morning-1.jpg": "https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=1200&q=85", # Executive morning with coffee
    "morning-2.jpg": "https://images.unsplash.com/photo-1495344517868-8ebaf0a2044a?w=1200&q=85", # Sunrise morning reading desk
    "morning-3.jpg": "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=1200&q=85", # Morning analysis journal

    # 4. Breakout & Chart Analysis (3 distinct images)
    "breakout-1.jpg": "https://images.unsplash.com/photo-1642543492481-44e81e3914a7?w=1200&q=85", # Green candlestick breakout
    "breakout-2.jpg": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1200&q=85", # Dark theme data dashboard
    "breakout-3.jpg": "https://images.unsplash.com/photo-1618042164219-62c820f10723?w=1200&q=85", # Upward glowing trend graph

    # 5. Dividend & Wealth (3 distinct images)
    "dividend-1.jpg": "https://images.unsplash.com/photo-1565514020179-026b92b84bb6?w=1200&q=85", # Stacked gold coins & growth
    "dividend-2.jpg": "https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?w=1200&q=85", # Investment growth & piggy bank
    "dividend-3.jpg": "https://images.unsplash.com/photo-1559526324-4b87b5e36e44?w=1200&q=85", # Wealth planning & dividends

    # 6. Macro Economics & Central Bank / FX (3 distinct images)
    "macro-1.jpg": "https://images.unsplash.com/photo-1580519542036-c47de6196ba5?w=1200&q=85", # Global currencies & USD bills
    "macro-2.jpg": "https://images.unsplash.com/photo-1501167786227-4cba60f6d58f?w=1200&q=85", # Classical central bank pillars
    "macro-3.jpg": "https://images.unsplash.com/photo-1526304640581-d334cdbbf45e?w=1200&q=85", # Cash flow & exchange rate

    # 7. IPO & Special Themes (5 distinct images)
    "ipo-1.jpg": "https://images.unsplash.com/photo-1450133064473-71024230f91b?w=1200&q=85", # Business contract & corporate IPO
    "ipo-2.jpg": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=1200&q=85", # Financial growth analytics
    "tax-1.jpg": "https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?w=1200&q=85", # Tax calculator & savings sheet
    "battery-1.jpg": "https://images.unsplash.com/photo-1593941707882-a5bba14938c7?w=1200&q=85", # EV electric vehicle battery
    "bio-1.jpg": "https://images.unsplash.com/photo-1532187863486-abf9dbad1b69?w=1200&q=85" # Biotechnology lab & microscope
}

def download_images():
    print(f"📥 Downloading {len(IMAGE_CATALOG)} diverse stock photos into {IMAGE_DIR}...")
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    for filename, url in IMAGE_CATALOG.items():
        filepath = os.path.join(IMAGE_DIR, filename)
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as resp:
                content = resp.read()
                with open(filepath, "wb") as f:
                    f.write(content)
                print(f"  [성공] {filename} ({len(content):,} bytes)")
        except Exception as e:
            print(f"  [실패] {filename}: {e}")

if __name__ == "__main__":
    download_images()
