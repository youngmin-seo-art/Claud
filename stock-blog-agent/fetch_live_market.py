"""
=============================================================================
LIVE MARKET FETCHER (fetch_live_market.py)
Yahoo Finance, Upbit, and ExchangeRate APIs -> market-summary.json
=============================================================================
"""

import sys
import json
import urllib.request
import urllib.parse
from datetime import datetime
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "adsense-stock-blog" / "data"
OUTPUT_JSON = DATA_DIR / "market-summary.json"

INSTRUMENTS = [
    # 1. 주요 지수 및 환율
    {"id": "kospi", "cat": "지수", "name": "KOSPI", "symbol": "^KS11", "precision": 2, "prefix": "", "suffix": "pt"},
    {"id": "kosdaq", "cat": "지수", "name": "KOSDAQ", "symbol": "^KQ11", "precision": 2, "prefix": "", "suffix": "pt"},
    {"id": "dji", "cat": "지수", "name": "다우존스", "symbol": "^DJI", "precision": 2, "prefix": "", "suffix": "pt"},
    {"id": "sp500", "cat": "지수", "name": "S&P 500", "symbol": "^GSPC", "precision": 2, "prefix": "", "suffix": "pt"},
    {"id": "nasdaq", "cat": "지수", "name": "NASDAQ 100", "symbol": "^IXIC", "precision": 2, "prefix": "", "suffix": "pt"},
    {"id": "sox", "cat": "지수", "name": "필라델피아반도체", "symbol": "^SOX", "precision": 2, "prefix": "", "suffix": "pt"},
    {"id": "usdkrw", "cat": "환율", "name": "USD/KRW", "symbol": "KRW=X", "precision": 2, "prefix": "", "suffix": "원"},

    # 2. 국내 KOSPI 시총 상위
    {"id": "samsung", "cat": "코스피", "name": "삼성전자", "symbol": "005930.KS", "precision": 0, "prefix": "", "suffix": "원"},
    {"id": "skhynix", "cat": "코스피", "name": "SK하이닉스", "symbol": "000660.KS", "precision": 0, "prefix": "", "suffix": "원"},
    {"id": "lgenergy", "cat": "코스피", "name": "LG에너지솔루션", "symbol": "373220.KS", "precision": 0, "prefix": "", "suffix": "원"},
    {"id": "samsungbio", "cat": "코스피", "name": "삼성바이오로직스", "symbol": "207940.KS", "precision": 0, "prefix": "", "suffix": "원"},
    {"id": "hyundai", "cat": "코스피", "name": "현대차", "symbol": "005380.KS", "precision": 0, "prefix": "", "suffix": "원"},

    # 3. 국내 KOSDAQ 시총 상위
    {"id": "alteogen", "cat": "코스닥", "name": "알테오젠", "symbol": "196170.KQ", "precision": 0, "prefix": "", "suffix": "원"},
    {"id": "ecoprobm", "cat": "코스닥", "name": "에코프로비엠", "symbol": "247540.KQ", "precision": 0, "prefix": "", "suffix": "원"},
    {"id": "ecopro", "cat": "코스닥", "name": "에코프로", "symbol": "086520.KQ", "precision": 0, "prefix": "", "suffix": "원"},
    {"id": "hlb", "cat": "코스닥", "name": "HLB", "symbol": "028300.KQ", "precision": 0, "prefix": "", "suffix": "원"},
    {"id": "ligachem", "cat": "코스닥", "name": "리가켐바이오", "symbol": "141080.KQ", "precision": 0, "prefix": "", "suffix": "원"},
    {"id": "enchem", "cat": "코스닥", "name": "엔켐", "symbol": "348370.KQ", "precision": 0, "prefix": "", "suffix": "원"},
    {"id": "samchendang", "cat": "코스닥", "name": "삼천당제약", "symbol": "000250.KQ", "precision": 0, "prefix": "", "suffix": "원"},
    {"id": "classys", "cat": "코스닥", "name": "클래시스", "symbol": "214150.KQ", "precision": 0, "prefix": "", "suffix": "원"},
    {"id": "hugel", "cat": "코스닥", "name": "휴젤", "symbol": "145020.KQ", "precision": 0, "prefix": "", "suffix": "원"},
    {"id": "leeno", "cat": "코스닥", "name": "리노공업", "symbol": "058470.KQ", "precision": 0, "prefix": "", "suffix": "원"},

    # 4. 미국 빅테크
    {"id": "nvda", "cat": "미국주식", "name": "엔비디아 (NVDA)", "symbol": "NVDA", "precision": 2, "prefix": "$", "suffix": ""},
    {"id": "aapl", "cat": "미국주식", "name": "애플 (AAPL)", "symbol": "AAPL", "precision": 2, "prefix": "$", "suffix": ""},
    {"id": "msft", "cat": "미국주식", "name": "마이크로소프트 (MSFT)", "symbol": "MSFT", "precision": 2, "prefix": "$", "suffix": ""},
    {"id": "googl", "cat": "미국주식", "name": "알파벳 (GOOGL)", "symbol": "GOOGL", "precision": 2, "prefix": "$", "suffix": ""},
    {"id": "amzn", "cat": "미국주식", "name": "아마존 (AMZN)", "symbol": "AMZN", "precision": 2, "prefix": "$", "suffix": ""},
    {"id": "meta", "cat": "미국주식", "name": "메타 (META)", "symbol": "META", "precision": 2, "prefix": "$", "suffix": ""},
    {"id": "tsla", "cat": "미국주식", "name": "테슬라 (TSLA)", "symbol": "TSLA", "precision": 2, "prefix": "$", "suffix": ""},
    {"id": "avgo", "cat": "미국주식", "name": "브로드컴 (AVGO)", "symbol": "AVGO", "precision": 2, "prefix": "$", "suffix": ""},
    {"id": "brk", "cat": "미국주식", "name": "버크셔해서웨이 (BRK.B)", "symbol": "BRK-B", "precision": 2, "prefix": "$", "suffix": ""},
    {"id": "lly", "cat": "미국주식", "name": "일라이릴리 (LLY)", "symbol": "LLY", "precision": 2, "prefix": "$", "suffix": ""},

    # 5. 가상화폐 (Upbit)
    {"id": "btc", "cat": "코인", "name": "비트코인 (BTC)", "marketCode": "KRW-BTC", "precision": 0, "prefix": "₩", "suffix": "", "isCrypto": True},
    {"id": "eth", "cat": "코인", "name": "이더리움 (ETH)", "marketCode": "KRW-ETH", "precision": 0, "prefix": "₩", "suffix": "", "isCrypto": True},
    {"id": "xrp", "cat": "코인", "name": "리플 (XRP)", "marketCode": "KRW-XRP", "precision": 0, "prefix": "₩", "suffix": "", "isCrypto": True},
    {"id": "sol", "cat": "코인", "name": "솔라나 (SOL)", "marketCode": "KRW-SOL", "precision": 0, "prefix": "₩", "suffix": "", "isCrypto": True},
]

def fetch_yahoo_quote(symbol):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(symbol)}?interval=1d&range=1d"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    with urllib.request.urlopen(req, timeout=6) as response:
        data = json.loads(response.read().decode('utf-8'))
        meta = data['chart']['result'][0]['meta']
        price = meta.get('regularMarketPrice')
        prev_close = meta.get('chartPreviousClose') or meta.get('previousClose')
        return price, prev_close

def fetch_upbit_quotes():
    url = "https://api.upbit.com/v1/ticker?markets=KRW-BTC,KRW-ETH,KRW-XRP,KRW-SOL"
    req = urllib.request.Request(url, headers={'Accept': 'application/json', 'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=6) as response:
        data = json.loads(response.read().decode('utf-8'))
        return {item['market']: item for item in data}

def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🚀 실시간 증시 데이터 수집 시작...")

    results = []

    # 1. Fetch Upbit Crypto
    upbit_map = {}
    try:
        upbit_map = fetch_upbit_quotes()
        print(f"  [성공] Upbit 가상화폐 4종 실시간 시세 수신 완료")
    except Exception as e:
        print(f"  [경고] Upbit 시세 수신 실패: {e}")

    # 2. Fetch Stock & Index & FX
    for inst in INSTRUMENTS:
        item = dict(inst)
        if inst.get("isCrypto") and inst.get("marketCode") in upbit_map:
            u_data = upbit_map[inst["marketCode"]]
            price = u_data["trade_price"]
            prev_close = u_data.get("prev_closing_price") or (price - u_data.get("signed_change_price", 0))
            diff_rate = u_data["signed_change_rate"] * 100
            item["price"] = price
            item["baseClose"] = prev_close
            item["diffRate"] = round(diff_rate, 2)
            item["diff"] = round(price - prev_close, 2)
            results.append(item)
            print(f"  [성공] {item['name']}: {price:,.0f}원 ({diff_rate:+.2f}%)")
        elif "symbol" in inst:
            sym = inst["symbol"]
            try:
                price, prev_close = fetch_yahoo_quote(sym)
                if price is not None:
                    if not prev_close or prev_close == 0:
                        prev_close = price
                    diff = price - prev_close
                    diff_rate = (diff / prev_close) * 100 if prev_close else 0
                    item["price"] = price
                    item["baseClose"] = prev_close
                    item["diffRate"] = round(diff_rate, 2)
                    item["diff"] = round(diff, 2)
                    results.append(item)
                    print(f"  [성공] {item['name']} ({sym}): {price:,.2f} ({diff_rate:+.2f}%)")
                else:
                    print(f"  [경고] {item['name']} 가격 데이터 없음")
            except Exception as e:
                print(f"  [경고] {item['name']} ({sym}) 조회 실패: {e}")

    payload = {
        "updatedAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "timestamp": int(datetime.now().timestamp() * 1000),
        "instruments": results
    }

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(f"🎉 [완료] {len(results)}개 실시간 시세 데이터가 {OUTPUT_JSON}에 저장되었습니다.")

if __name__ == "__main__":
    main()
