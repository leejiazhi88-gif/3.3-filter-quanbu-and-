"""Sina fallback preserving live price and market-cap semantics."""
import math
import time
import pandas as pd
import requests
from tushare.stock import rtq


def fetch_sina():
    count_response = requests.get(rtq.zh_sina_a_stock_count_url, timeout=30)
    count_response.raise_for_status()
    import re
    count = int(re.search(r'\d+', count_response.text).group())
    records = []
    for page in range(1, math.ceil(count / 80) + 1):
        params = dict(rtq.zh_sina_a_stock_payload, page=page, num=80,
                      sort='symbol', asc=1)
        for attempt in range(3):
            try:
                response = requests.get(rtq.zh_sina_a_stock_url,
                                        headers=rtq.zh_sina_a_stock_headers,
                                        params=params, timeout=30)
                response.raise_for_status()
                batch = response.json()
                assert isinstance(batch, list) and batch, (page, batch)
                records.extend(batch)
                break
            except (requests.ConnectionError, requests.Timeout):
                if attempt == 2:
                    raise
                time.sleep(1 + attempt)
        time.sleep(.4)
    raw = pd.DataFrame(records)
    assert len(raw) == count and raw.symbol.nunique() == count
    frame = pd.DataFrame({
        'ts_code': raw.code + '.' + raw.symbol.str[:2].str.upper(),
        'name': raw['name'], 'price': pd.to_numeric(raw.trade),
        'pct_change': pd.to_numeric(raw.changepercent),
        # Sina reports market capitalization in ten thousand CNY.
        'total_mv': pd.to_numeric(raw.mktcap) * 10000,
        'quote_time': raw.ticktime,
    })
    return frame
