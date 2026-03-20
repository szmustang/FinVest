import akshare as ak
from datetime import datetime, timedelta
import traceback

print("Testing stock_individual_info_em...")
try:
    df = ak.stock_individual_info_em(symbol="000001")
    print("Success:\n", df.head())
except Exception as e:
    print("Failed info:", e)

print("\nTesting stock_zh_a_hist...")
try:
    end_date = datetime.now().strftime("%Y%m%d")
    start_date = (datetime.now() - timedelta(days=100)).strftime("%Y%m%d")
    df = ak.stock_zh_a_hist(symbol="000001", period="daily", start_date=start_date, end_date=end_date, adjust="qfq")
    print("Success:", len(df), "rows.\n", df.head())
except Exception as e:
    print("Failed hist:", e)

print("\nTesting HS300 index...")
try:
    df = ak.index_zh_a_hist(symbol="000300", period="daily")
    print("Success HS300:", len(df))
except Exception as e:
    print("Failed HS300:", e)
