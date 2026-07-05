#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""生成 ma_backtest.html — 嵌入所有股票数据到 HTML 模板中"""
import csv, os

BASE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(BASE), "data")
OUT = os.path.join(BASE, "ma_backtest.html")

# 股票列表 (code, name, ts_code)
stocks = [
    ("603986", "兆易创新", "603986.SH"),
    ("001280", "中国铀业", "001280.SZ"),
    ("301275", "汉朔科技", "301275.SZ"),
    ("601318", "中国平安", "601318.SH"),
]

embedded = {}
for code, name, ts_code in stocks:
    fp = os.path.join(DATA_DIR, f"{code}_daily.csv")
    if not os.path.exists(fp):
        print(f"  跳过: {fp} 不存在")
        continue
    with open(fp, encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    # 紧凑格式: date,open,high,low,close,vol
    compact = ";".join(
        f"{r['trade_date']},{r['open']},{r['high']},{r['low']},{r['close']},{r['vol']}"
        for r in rows
    )
    embedded[code] = f'    "{code}":{{"name":"{name}","ts_code":"{ts_code}","data":"{compact}"}}'

data_block = ",\n".join(embedded.values())

# 读取 HTML 模板
template_path = os.path.join(BASE, "ma_backtest_template.html")
with open(template_path, encoding="utf-8") as f:
    html = f.read()

html = html.replace("/* __DATA_GOES_HERE__ */ {}", f"{{\n{data_block}\n}}")

with open(OUT, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Generated: {OUT}")
print(f"Size: {os.path.getsize(OUT)} bytes")
for code, name, _ in stocks:
    fp = os.path.join(DATA_DIR, f"{code}_daily.csv")
    if os.path.exists(fp):
        with open(fp, encoding="utf-8-sig") as f:
            n = sum(1 for _ in f) - 1
        print(f"  {code} {name}: {n} rows")
