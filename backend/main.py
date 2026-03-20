from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from value_engine import ValueEngine
from market_engine import MarketEngine
from capital_engine import CapitalEngine

app = FastAPI(title="三因共振量化决策平台 - API", version="2.2.0")

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

value_eng = ValueEngine()
market_eng = MarketEngine()
capital_eng = CapitalEngine()

@app.get("/")
def read_root():
    return {"status": "ok", "message": "三因共振量化决策平台后端服务已启动"}

@app.get("/api/health")
def health_check():
    return {"status": "ok"}

from data_fetcher import get_basic_quote

@app.get("/api/score/{symbol}")
def get_comprehensive_score(symbol: str):
    """根据文档，计算个股综合评分"""
    val_res = value_eng.calculate_score(symbol)
    mar_res = market_eng.evaluate_market_condition()
    cap_res = capital_eng.calculate_signal(symbol)
    
    quote = get_basic_quote(symbol)
    
    total_score = val_res['value_score'] * 0.3 + mar_res['market_score'] * 0.3 + cap_res['capital_score'] * 0.4
    
    position_advice = "0-10%"
    action = "持有或观望"
    if total_score >= 8.5:
        position_advice = "25%-30%"
        action = "重仓买入"
    elif total_score >= 7.0:
        position_advice = "20%-25%"
        action = "积极建仓"
    elif total_score >= 5.5:
        position_advice = "15%-20%"
        action = "试探性买入"
    elif total_score < 4.0:
        position_advice = "0%"
        action = "坚决回避/清仓"
        
    return {
        "symbol": symbol,
        "quote": quote,
        "total_score": round(total_score, 2),
        "action": action,
        "suggested_position": position_advice,
        "market_position_limit": mar_res['position_limit'],
        "details": {
            "value": val_res,
            "market": mar_res,
            "capital": cap_res
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
