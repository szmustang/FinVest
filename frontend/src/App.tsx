import { useState } from 'react';
import axios from 'axios';
import '@shoelace-style/shoelace/dist/components/input/input.js';
import '@shoelace-style/shoelace/dist/components/button/button.js';
import '@shoelace-style/shoelace/dist/components/card/card.js';
import '@shoelace-style/shoelace/dist/components/tag/tag.js';
import '@shoelace-style/shoelace/dist/components/spinner/spinner.js';
import '@shoelace-style/shoelace/dist/components/icon/icon.js';
import '@shoelace-style/shoelace/dist/components/divider/divider.js';

interface Quote {
  date: string;
  name: string;
  price: number;
  change_pct: number;
}

interface ScoreResponse {
  symbol: string;
  quote?: Quote;
  total_score: number;
  action: string;
  suggested_position: string;
  market_position_limit: string;
  details: {
    value: { value_score: number; reasons: string[]; is_core_pool: boolean };
    market: { market_score: number; condition: string; position_limit: string; details: string[] };
    capital: { capital_score: number; status: string; signals: string[] };
  };
}

function App() {
  const [symbol, setSymbol] = useState('000001');
  const [data, setData] = useState<ScoreResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSearch = async () => {
    if (!symbol) return;
    setLoading(true);
    setError('');
    try {
      const res = await axios.get(`http://localhost:8000/api/score/${symbol}`);
      setData(res.data);
    } catch (err) {
      setError('数据获取失败，请检查后端服务是否启动。');
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  const getScoreClass = (score: number) => {
    if (score >= 8.5) return 'score-high';
    if (score >= 5.5) return 'score-mid';
    return 'score-low';
  };

  return (
    <div className="dashboard-container sl-theme-dark" style={{ minHeight: '100vh', backgroundColor: 'var(--sl-color-neutral-950)' }}>
      <div className="header">
        <div className="title-area">
          <h1>三因共振量化决策平台</h1>
          <p>价值因子 (30%) · 市场因子 (30%) · 资金因子 (40%)</p>
        </div>
      </div>

      <div className="search-section">
        <sl-input 
          placeholder="输入股票代码 (如 000001)" 
          value={symbol} 
          onInput={(e: any) => setSymbol(e.target.value)}
          onKeyDown={handleKeyDown}
          style={{ width: '300px' }}
        >
          <sl-icon name="search" slot="prefix"></sl-icon>
        </sl-input>
        <sl-button variant="primary" onClick={handleSearch} disabled={loading}>
          {loading ? <sl-spinner></sl-spinner> : '查询综合评分'}
        </sl-button>
      </div>

      {error && <div style={{ color: 'var(--sl-color-danger-500)', marginBottom: '1rem' }}>{error}</div>}

      {data && (
        <>
          {data.quote && (
            <div className="quote-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem', backgroundColor: '#1e293b', padding: '1rem 2rem', borderRadius: '8px', border: '1px solid #334155' }}>
               <div>
                 <span style={{ fontSize: '1.25rem', fontWeight: 'bold', marginRight: '1rem', color: '#f8fafc' }}>{data.quote.name} ({symbol})</span>
                 <span style={{ fontSize: '1.5rem', fontWeight: 'bold', color: data.quote.change_pct >= 0 ? '#ef4444' : '#22c55e', marginRight: '1rem' }}>
                   {data.quote.price} 
                 </span>
                 <span style={{ fontSize: '1rem', color: data.quote.change_pct >= 0 ? '#ef4444' : '#22c55e', fontWeight: 'bold' }}>
                   {data.quote.change_pct >= 0 ? '+' : ''}{data.quote.change_pct}%
                 </span>
               </div>
               <div style={{ color: '#94a3b8', fontSize: '0.9rem' }}>更新时间: {data.quote.date}</div>
            </div>
          )}
          <div className="score-card">
            <h2>{data.symbol} 综合评分</h2>
            <div className={`score-value ${getScoreClass(data.total_score)}`}>
              {data.total_score}
            </div>
            <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center' }}>
              <sl-tag variant={data.total_score >= 8.5 ? "success" : data.total_score >= 5.5 ? "warning" : "danger"} size="large">
                决策: {data.action}
              </sl-tag>
              <sl-tag variant="primary" size="large">
                建议仓位: {data.suggested_position}
              </sl-tag>
              <sl-tag variant="neutral" size="large">
                全市场仓位上限: {data.market_position_limit}
              </sl-tag>
            </div>
          </div>

          <div className="factors-grid">
            <sl-card>
              <div className="card-header">
                <span>🏦 价值因子 (30%)</span>
                <span>{data.details.value.value_score} / 10</span>
              </div>
              <sl-divider></sl-divider>
              <div>
                <sl-tag size="small" variant={data.details.value.is_core_pool ? "success" : "danger"} style={{ marginBottom: '1rem' }}>
                  {data.details.value.is_core_pool ? '符合核心股票池' : '未入核心池'}
                </sl-tag>
                <ul style={{ paddingLeft: '1.2rem', margin: 0 }}>
                  {data.details.value.reasons.map((r, i) => <li key={i}>{r}</li>)}
                </ul>
              </div>
            </sl-card>

            <sl-card>
              <div className="card-header">
                <span>📈 市场因子 (30%)</span>
                <span>{data.details.market.market_score} / 10</span>
              </div>
              <sl-divider></sl-divider>
              <div>
                 <sl-tag size="small" variant="primary" style={{ marginBottom: '1rem' }}>
                  当前环境: {data.details.market.condition}
                </sl-tag>
                <ul style={{ paddingLeft: '1.2rem', margin: 0 }}>
                  {data.details.market.details.map((r, i) => <li key={i}>{r}</li>)}
                </ul>
              </div>
            </sl-card>

            <sl-card>
              <div className="card-header">
                <span>📊 资金因子 (40%)</span>
                <span>{data.details.capital.capital_score} / 10</span>
              </div>
              <sl-divider></sl-divider>
              <div>
                 <sl-tag size="small" variant="warning" style={{ marginBottom: '1rem' }}>
                  资金状态: {data.details.capital.status}
                </sl-tag>
                <ul style={{ paddingLeft: '1.2rem', margin: 0 }}>
                  {data.details.capital.signals.map((r, i) => <li key={i}>{r}</li>)}
                </ul>
              </div>
            </sl-card>
          </div>
        </>
      )}
    </div>
  );
}

export default App;
