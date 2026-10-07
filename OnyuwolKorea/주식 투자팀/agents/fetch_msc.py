import urllib.request
import json
import re

code = "009780"

# 1. Basic Info
url_basic = f"https://m.stock.naver.com/api/stock/{code}/integration"
req_basic = urllib.request.Request(url_basic, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req_basic) as res:
    basic_data = json.loads(res.read().decode('utf-8'))

info_dict = {item.get('key'): item.get('value') for item in basic_data.get('totalInfos', [])}

# 2. Annual & Quarter Financials
url_ann = f"https://m.stock.naver.com/api/stock/{code}/finance/annual"
req_ann = urllib.request.Request(url_ann, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req_ann) as res:
    ann_data = json.loads(res.read().decode('utf-8'))

url_qtr = f"https://m.stock.naver.com/api/stock/{code}/finance/quarter"
req_qtr = urllib.request.Request(url_qtr, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req_qtr) as res:
    qtr_data = json.loads(res.read().decode('utf-8'))

# Let's inspect balance sheet from fnguide or wisereport
url_bs = f"https://navercomp.wisereport.co.kr/v2/company/c1010001.aspx?cmp_cd={code}"
req_bs = urllib.request.Request(url_bs, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
with urllib.request.urlopen(req_bs) as res:
    bs_html = res.read().decode('utf-8', errors='ignore')

# Extract key statistics
print("=== BASIC INFO ===")
for k, v in info_dict.items():
    print(f"{k}: {v}")

print("\n=== ANNUAL DATA ===")
for r in ann_data.get('financeInfo', {}).get('rowList', []):
    cols = {k: v.get('value') for k, v in r.get('columns', {}).items()}
    print(f"{r.get('title')}: {cols}")

print("\n=== QUARTER DATA ===")
for r in qtr_data.get('financeInfo', {}).get('rowList', []):
    cols = {k: v.get('value') for k, v in r.get('columns', {}).items()}
    print(f"{r.get('title')}: {cols}")
