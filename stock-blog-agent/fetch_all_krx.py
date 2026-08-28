import urllib.request
import json
import time
import os

def get_chosung(text):
    CHOSUNG = ['ㄱ','ㄲ','ㄴ','ㄷ','ㄸ','ㄹ','ㅁ','ㅂ','ㅃ','ㅅ','ㅆ','ㅇ','ㅈ','ㅉ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ']
    res = ''
    for char in text:
        code = ord(char) - 44032
        if 0 <= code <= 11171:
            res += CHOSUNG[code // 588]
        else:
            res += char
    return res.lower()

def fetch_market_stocks(market_name):
    # market_name: 'KOSPI' or 'KOSDAQ'
    all_stocks = []
    page = 1
    page_size = 100
    
    while True:
        url = f"https://m.stock.naver.com/api/stocks/marketValue/{market_name}?page={page}&pageSize={page_size}"
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://m.stock.naver.com/'
        })
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                stocks = data.get('stocks', [])
                if not stocks:
                    break
                
                for s in stocks:
                    code = s.get('itemCode', '')
                    name = s.get('stockName', '')
                    raw_price = s.get('closePrice', '0').replace(',', '')
                    try:
                        price = float(raw_price)
                    except:
                        price = 0
                    
                    if code and name:
                        all_stocks.append({
                            'code': code,
                            'name': name,
                            'chosung': get_chosung(name),
                            'market': market_name,
                            'price': price
                        })
                
                total_count = data.get('totalCount', 0)
                print(f"[{market_name}] Page {page} fetched, accum {len(all_stocks)} / {total_count}")
                if len(all_stocks) >= total_count:
                    break
                page += 1
                time.sleep(0.03)
        except Exception as e:
            print(f"Error fetching {market_name} page {page}: {e}")
            break
            
    return all_stocks

if __name__ == '__main__':
    print("Fetching KOSPI stocks...")
    kospi = fetch_market_stocks('KOSPI')
    
    print("Fetching KOSDAQ stocks...")
    kosdaq = fetch_market_stocks('KOSDAQ')
    
    # Add top US Tech Stocks
    us_stocks = [
        { "code": "NVDA", "name": "엔비디아 (NVDA)", "chosung": "ㅇㅂㄷㅇ", "market": "US", "price": 128.8, "bps": 18.5, "roe": 55.0, "eps": 3.80, "r": 10.0, "g": 35.0, "per": 35.0, "omega": "1.0" },
        { "code": "AAPL", "name": "애플 (AAPL)", "chosung": "ㅇㅍ", "market": "US", "price": 228.4, "bps": 5.10, "roe": 145.0, "eps": 6.70, "r": 8.5, "g": 10.0, "per": 33.0, "omega": "1.0" },
        { "code": "MSFT", "name": "마이크로소프트 (MSFT)", "chosung": "ㅁㅇㅋㄹㅅㅍㅌ", "market": "US", "price": 448.5, "bps": 36.5, "roe": 38.0, "eps": 12.2, "r": 8.5, "g": 15.0, "per": 35.0, "omega": "1.0" },
        { "code": "GOOGL", "name": "알파벳/구글 (GOOGL)", "chosung": "ㄱㄱ", "market": "US", "price": 176.2, "bps": 25.5, "roe": 28.0, "eps": 7.20, "r": 8.5, "g": 14.0, "per": 24.0, "omega": "1.0" },
        { "code": "AMZN", "name": "아마존 (AMZN)", "chosung": "ㅇㅁㅈ", "market": "US", "price": 182.5, "bps": 22.0, "roe": 22.0, "eps": 4.80, "r": 9.0, "g": 20.0, "per": 38.0, "omega": "1.0" },
        { "code": "META", "name": "메타 (META)", "chosung": "ㅁㅌ", "market": "US", "price": 524.3, "bps": 62.0, "roe": 32.0, "eps": 21.5, "r": 8.5, "g": 18.0, "per": 24.0, "omega": "1.0" },
        { "code": "TSLA", "name": "테슬라 (TSLA)", "chosung": "ㅌㅅㄹ", "market": "US", "price": 224.5, "bps": 22.0, "roe": 15.0, "eps": 2.80, "r": 10.0, "g": 25.0, "per": 75.0, "omega": "1.0" },
        { "code": "AVGO", "name": "브로드컴 (AVGO)", "chosung": "ㅂㄹㄷㅋ", "market": "US", "price": 168.2, "bps": 16.0, "roe": 35.0, "eps": 5.40, "r": 9.0, "g": 22.0, "per": 30.0, "omega": "1.0" },
        { "code": "AMD", "name": "AMD", "chosung": "ㅇㅇㅇㄷ", "market": "US", "price": 154.5, "bps": 34.0, "roe": 14.0, "eps": 3.40, "r": 9.5, "g": 28.0, "per": 45.0, "omega": "1.0" },
        { "code": "TSM", "name": "TSMC (TSM)", "chosung": "ㅌㅅㅇㅇ", "market": "US", "price": 172.0, "bps": 24.0, "roe": 28.0, "eps": 6.80, "r": 9.0, "g": 20.0, "per": 25.0, "omega": "1.0" }
    ]
    
    # Merge curated financials for popular stocks
    POPULAR_FINANCIALS = {
      "005930": { "bps": 58000, "roe": 11.5, "eps": 5200, "r": 8.5, "g": 12.0, "per": 15.0, "omega": "0.9" },
      "000660": { "bps": 115000, "roe": 18.0, "eps": 14500, "r": 9.5, "g": 20.0, "per": 13.5, "omega": "0.9" },
      "042700": { "bps": 12500, "roe": 32.0, "eps": 4100, "r": 9.5, "g": 35.0, "per": 30.0, "omega": "1.0" },
      "058470": { "bps": 45000, "roe": 24.5, "eps": 8500, "r": 8.5, "g": 18.0, "per": 24.0, "omega": "1.0" },
      "007660": { "bps": 7200, "roe": 21.0, "eps": 1650, "r": 9.0, "g": 25.0, "per": 26.0, "omega": "0.9" },
      "403870": { "bps": 4800, "roe": 38.0, "eps": 1250, "r": 9.5, "g": 30.0, "per": 27.0, "omega": "1.0" },
      "066570": { "bps": 118000, "roe": 8.0, "eps": 8200, "r": 8.5, "g": 8.0, "per": 12.0, "omega": "0.9" },
      "009150": { "bps": 98000, "roe": 9.5, "eps": 8900, "r": 8.5, "g": 12.0, "per": 16.0, "omega": "0.9" },
      "005380": { "bps": 340000, "roe": 13.0, "eps": 36000, "r": 8.5, "g": 8.0, "per": 8.0, "omega": "0.9" },
      "000270": { "bps": 128000, "roe": 19.5, "eps": 21500, "r": 8.5, "g": 8.0, "per": 6.0, "omega": "0.9" },
      "012330": { "bps": 420000, "roe": 8.5, "eps": 28000, "r": 8.5, "g": 7.0, "per": 8.5, "omega": "0.9" },
      "035420": { "bps": 170000, "roe": 8.5, "eps": 8800, "r": 8.5, "g": 10.0, "per": 22.0, "omega": "0.9" },
      "035720": { "bps": 28500, "roe": 7.2, "eps": 2100, "r": 8.5, "g": 12.0, "per": 25.0, "omega": "0.9" },
      "259960": { "bps": 115000, "roe": 18.5, "eps": 17500, "r": 8.5, "g": 16.0, "per": 20.0, "omega": "0.9" },
      "036570": { "bps": 154000, "roe": 5.5, "eps": 7200, "r": 8.5, "g": 5.0, "per": 25.0, "omega": "0.8" },
      "352820": { "bps": 72000, "roe": 9.0, "eps": 5200, "r": 9.0, "g": 15.0, "per": 35.0, "omega": "0.9" },
      "373220": { "bps": 98000, "roe": 6.8, "eps": 6500, "r": 9.0, "g": 18.0, "per": 45.0, "omega": "0.9" },
      "247540": { "bps": 38000, "roe": 8.0, "eps": 2800, "r": 9.5, "g": 25.0, "per": 50.0, "omega": "0.9" },
      "086520": { "bps": 22000, "roe": 6.5, "eps": 1200, "r": 9.5, "g": 20.0, "per": 55.0, "omega": "0.9" },
      "005490": { "bps": 560000, "roe": 5.5, "eps": 24000, "r": 8.5, "g": 7.0, "per": 15.0, "omega": "0.8" },
      "006400": { "bps": 290000, "roe": 7.5, "eps": 19000, "r": 8.5, "g": 12.0, "per": 18.0, "omega": "0.9" },
      "196170": { "bps": 14500, "roe": 35.0, "eps": 4800, "r": 10.0, "g": 40.0, "per": 60.0, "omega": "1.0" },
      "207940": { "bps": 215000, "roe": 10.5, "eps": 15000, "r": 8.5, "g": 18.0, "per": 65.0, "omega": "1.0" },
      "068270": { "bps": 72000, "roe": 12.5, "eps": 6200, "r": 8.5, "g": 15.0, "per": 32.0, "omega": "0.9" },
      "000100": { "bps": 31000, "roe": 8.0, "eps": 1850, "r": 8.5, "g": 25.0, "per": 45.0, "omega": "1.0" },
      "000250": { "bps": 16000, "roe": 15.0, "eps": 2400, "r": 9.5, "g": 30.0, "per": 50.0, "omega": "1.0" },
      "141080": { "bps": 9800, "roe": 18.0, "eps": 1950, "r": 10.0, "g": 35.0, "per": 45.0, "omega": "1.0" },
      "028300": { "bps": 8200, "roe": 12.0, "eps": 1100, "r": 10.0, "g": 30.0, "per": 50.0, "omega": "0.9" },
      "214150": { "bps": 8500, "roe": 32.0, "eps": 1850, "r": 8.5, "g": 24.0, "per": 30.0, "omega": "1.0" },
      "105560": { "bps": 135000, "roe": 9.8, "eps": 12500, "r": 8.5, "g": 6.0, "per": 7.0, "omega": "0.9" },
      "055550": { "bps": 98000, "roe": 9.2, "eps": 8800, "r": 8.5, "g": 6.0, "per": 6.5, "omega": "0.9" },
      "086790": { "bps": 118000, "roe": 9.5, "eps": 11800, "r": 8.5, "g": 5.5, "per": 5.5, "omega": "0.9" },
      "138040": { "bps": 48000, "roe": 26.0, "eps": 12500, "r": 8.5, "g": 12.0, "per": 7.5, "omega": "1.0" },
      "267260": { "bps": 46000, "roe": 34.0, "eps": 14500, "r": 8.5, "g": 30.0, "per": 22.0, "omega": "1.0" },
      "298040": { "bps": 142000, "roe": 18.0, "eps": 24500, "r": 8.5, "g": 25.0, "per": 16.0, "omega": "0.9" },
      "034020": { "bps": 16500, "roe": 6.8, "eps": 750, "r": 8.5, "g": 15.0, "per": 28.0, "omega": "0.9" },
      "003490": { "bps": 28500, "roe": 12.0, "eps": 3200, "r": 8.5, "g": 6.0, "per": 7.2, "omega": "0.8" }
    }
    
    total = kospi + kosdaq + us_stocks
    for s in total:
        code = s.get('code')
        if code in POPULAR_FINANCIALS:
            s.update(POPULAR_FINANCIALS[code])
            
    print(f"Total stocks: {len(total)} (KOSPI: {len(kospi)}, KOSDAQ: {len(kosdaq)}, US: {len(us_stocks)})")
    
    os.makedirs('adsense-stock-blog/data', exist_ok=True)
    os.makedirs('adsense-stock-blog/js', exist_ok=True)
    
    # Save as JSON
    with open('adsense-stock-blog/data/all_stocks.json', 'w', encoding='utf-8') as f:
        json.dump(total, f, ensure_ascii=False, separators=(',', ':'))
        
    # Save as Javascript file for instant client-side inclusion
    js_content = f"// All KOSPI & KOSDAQ Stocks Database ({len(total)} items)\nwindow.ALL_STOCKS_DB = " + json.dumps(total, ensure_ascii=False, separators=(',', ':')) + ";\n"
    with open('adsense-stock-blog/js/all-stocks.js', 'w', encoding='utf-8') as f:
        f.write(js_content)
        
    print("Successfully saved adsense-stock-blog/js/all-stocks.js and all_stocks.json!")
