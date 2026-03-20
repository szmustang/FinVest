import requests
from urllib3.exceptions import InsecureRequestWarning
import warnings
warnings.simplefilter('ignore', InsecureRequestWarning)

original_request = requests.Session.request

def patched_request(self, method, url, **kwargs):
    headers = kwargs.get('headers', {})
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    headers['Referer'] = 'https://quote.eastmoney.com/'
    kwargs['headers'] = headers
    kwargs['verify'] = False
    return original_request(self, method, url, **kwargs)

requests.Session.request = patched_request

import akshare as ak

print("Testing akshare stock info...")
try:
    df = ak.stock_individual_info_em(symbol="600036")
    print(df.head())
except Exception as e:
    print("Failed info:", e)

print("Testing akshare stock daily...")
try:
    df = ak.stock_zh_a_hist(symbol="600036", period="daily", start_date="20250101", end_date="20260319")
    print(len(df), "rows")
except Exception as e:
    print("Failed hist:", e)
