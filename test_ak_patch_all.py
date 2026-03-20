import requests
from urllib3.exceptions import InsecureRequestWarning
import warnings
warnings.simplefilter('ignore', InsecureRequestWarning)

original_get = requests.get
original_post = requests.post
original_request = requests.Session.request

def add_headers(kwargs):
    headers = kwargs.get('headers', {})
    if 'User-Agent' not in headers or 'python-requests' in headers.get('User-Agent', ''):
        headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    headers['Referer'] = 'https://quote.eastmoney.com/'
    kwargs['headers'] = headers
    kwargs['verify'] = False
    
    # Try disabling proxies at requests level
    kwargs['proxies'] = {
        "http": None,
        "https": None,
    }
    return kwargs

def patched_get(url, **kwargs):
    return original_get(url, **add_headers(kwargs))

def patched_post(url, **kwargs):
    return original_post(url, **add_headers(kwargs))
    
def patched_session_request(self, method, url, **kwargs):
    return original_request(self, method, url, **add_headers(kwargs))

requests.get = patched_get
requests.post = patched_post
requests.Session.request = patched_session_request

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
    print(len(df), "rows. Head:")
    print(df.head(2))
except Exception as e:
    print("Failed hist:", e)
