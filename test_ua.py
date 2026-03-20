import os
import requests
import warnings
from urllib3.exceptions import InsecureRequestWarning

# Suppress the warnings from verify=False
warnings.simplefilter('ignore', InsecureRequestWarning)

# Temporarily ignore proxy env vars just in case
os.environ['NO_PROXY'] = '*'

original_request = requests.Session.request

def patched_request(self, method, url, **kwargs):
    headers = kwargs.get('headers', {})
    headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8'
    headers['Accept-Language'] = 'zh-CN,zh;q=0.9,en;q=0.8'
    kwargs['headers'] = headers
    kwargs['verify'] = False # bypass local proxy SSL cert issues
    return original_request(self, method, url, **kwargs)

requests.Session.request = patched_request

import akshare as ak

if __name__ == "__main__":
    try:
        df = ak.stock_individual_info_em(symbol="600036")
        print("Success 600036:")
        print(df.head())
    except Exception as e:
        print("Still failed:", e)
