import os
import akshare as ak

os.environ.pop("http_proxy", None)
os.environ.pop("https_proxy", None)
os.environ.pop("HTTP_PROXY", None)
os.environ.pop("HTTPS_PROXY", None)

print("Proxy bypassed.")

try:
    df_info = ak.stock_individual_info_em(symbol="600036")
    print("Success 600036:")
    print(df_info.head())
except Exception as e:
    print("Failed info:", e)
