import pandas as pd
from data_fetcher import get_real_daily_data

class CapitalEngine:
    def __init__(self):
        pass

    def calculate_signal(self, symbol: str) -> dict:
        """
        拉取真实日线历史计算资金因子的指标
        """
        df = get_real_daily_data(symbol)
        if df.empty or len(df) < 20:
            return {"capital_score": 3.0, "status": "数据不足或长期停牌", "signals": ["无法获取近期完整的日线及成交量数据"]}
        
        try:
            df['MA5'] = df['收盘'].rolling(5).mean()
            df['MA20'] = df['收盘'].rolling(20).mean()
            df['V_MA5'] = df['成交量'].rolling(5).mean()
            
            latest = df.iloc[-1]
            prev = df.iloc[-2]
            
            score = 5.0
            signals = []
            
            if pd.notna(latest['MA5']) and pd.notna(latest['MA20']):
                if latest['MA5'] > latest['MA20']:
                    score += 1.5
                    signals.append(f"MA5站上MA20均线，短期趋势偏多 (当前收盘: {round(latest['收盘'], 2)})")
                else:
                    score -= 1.0
                    signals.append(f"MA5暂处MA20均线下方，趋势有待修复 (当前收盘: {round(latest['收盘'], 2)})")
                    
            if pd.notna(latest['成交量']) and pd.notna(latest['V_MA5']):
                if latest['成交量'] > latest['V_MA5'] * 1.5 and latest['收盘'] > prev['收盘']:
                    score += 2.0
                    signals.append("今日放量上涨迹象明显，主力介入可能性高")
                elif latest['成交量'] < latest['V_MA5'] * 0.8 and latest['收盘'] <= prev['收盘']:
                    score += 1.0
                    signals.append("当前缩量回调，可能为主力洗盘阶段或买盘暂时休息")
            
            score = min(max(score, 0), 10.0)
            
            status = "资金博弈温和区，持续观察"
            if score >= 8:
                status = "资金量能充沛，具备上攻主力动能"
            elif score <= 4:
                status = "资金面偏弱，量价结构欠佳"

            return {
                "symbol": symbol,
                "capital_score": round(score, 2),
                "status": status,
                "signals": signals if signals else ["未观测到特别突出的异动买卖信号"]
            }
        except Exception as e:
            return {"symbol": symbol, "capital_score": 5.0, "status": "因子分析异常", "signals": [f"错误信息: {e}"]}
