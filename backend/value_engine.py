import pandas as pd
from data_fetcher import get_real_stock_info

class ValueEngine:
    def __init__(self):
        self.sectors = ['消费', '科创', '周期', '金融', '公用事业']

    def calculate_score(self, symbol: str) -> dict:
        """
        根据获取的实时动态基本面更新价值评分
        """
        info = get_real_stock_info(symbol)
        if not info:
             return {"value_score": 4.0, "reasons": ["无法获取该标的的实时基本面API数据"], "is_core_pool": False}
        
        try:
            pe_str = str(info.get('市盈率-动态', '0'))
            pb_str = str(info.get('市净率', '0'))
            pe = float(pe_str) if pe_str and pe_str != 'None' and pe_str != '-' else 0
            pb = float(pb_str) if pb_str and pb_str != 'None' and pb_str != '-' else 0
            
            score = 6.0
            reasons = []
            
            if 0 < pe < 30:
                score += 2.0
                reasons.append(f"动态市盈率低估: {pe}")
            elif pe >= 30:
                score -= 1.0
                reasons.append(f"动态市盈率偏高: {pe}")
                
            if 0 < pb < 3:
                score += 2.0
                reasons.append(f"市净率适中: {pb}")
            elif pb >= 3:
                reasons.append(f"市净率溢价偏高: {pb}")
                
            score = min(max(score, 0), 10.0)
            
            return {
                "symbol": symbol,
                "value_score": round(score, 2),
                "reasons": reasons if reasons else ["基本面指标处于中等水平"],
                "is_core_pool": score >= 7
            }
        except:
            return {"symbol": symbol, "value_score": 5.0, "reasons": ["基本面数据解析计算异常"], "is_core_pool": False}
