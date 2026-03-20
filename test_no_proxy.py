import os
os.environ['NO_PROXY'] = '*'

import akshare as ak

if __name__ == "__main__":
    try:
        df_info = ak.stock_individual_info_em(symbol="600036")
        print("Success 600036! Data fetched:")
        print(df_info.head())
    except Exception as e:
        print("Still failed:", e)
