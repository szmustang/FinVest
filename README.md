# 三因共振量化决策平台 (FinVest)

## 简介
三因共振量化决策平台（FinVest）是一个基于“价值（Value）、大盘（Market）、资金（Capital）”三大维度共振的量化投资决策系统。系统旨在通过对个股的基本面价值、市场大盘运行环境以及主力资金流向进行多维度关联分析，为投资者提供科学的仓位建议与交易信号。

平台的核心理论模型参考项目根目录下的详细文档：《三因共振量化决策体系v2.2.docx》。

## 技术栈

### 后端 (Backend)
- **核心框架**: FastAPI
- **数据处理与计算**: Pandas, NumPy
- **量化数据源**: AkShare (具备防屏蔽代理和自定义 User-Agent 的重试机制)
- **数据持久化**: SQLAlchemy
- **运行环境**: Python, Uvicorn (默认端口 8000)

### 前端 (Frontend)
- **核心框架**: React 19 + TypeScript
- **构建工具**: Vite
- **UI 组件库**: Shoelace (基于 Web Components 构建，提供现代化的 UI 开发体验)
- **网络层**: Axios

## 核心架构设计

按照“三因共振”模型，平台后端独立抽象了三大核心分析引擎：

1. **ValueEngine (价值引擎)**: 负责评估个股的财务与基本面成长指标，占综合评分权重的 30%。
2. **MarketEngine (大盘引擎)**: 负责感知和评估系统的宏观环境，输出大盘分数及市场仓位限制阀值，占综合评分权重的 30%。
3. **CapitalEngine (资金引擎)**: 负责监控微观盘面的主力资金流口与异动信号，占综合评分权重的 40%。

平台通过 `/api/score/{symbol}` 接口对外输出综合研判结果。综合评价得分按照 `(价值*0.3 + 大盘*0.3 + 资金*0.4)` 计算得出（满分 10 分），并依据得分界定出明确的操作建议（如：重仓买入、积极建仓、试探性买入、坚决回避/清仓），同时给出具体建议仓位比例。

## 本地开发与运行指南

### 1. 运行后端服务
建议使用 Python 虚拟环境运行。

```bash
cd backend

# 安装后端依赖
pip install -r requirements.txt

# 启动 FastAPI 服务
python main.py
# 或采用 uvicorn 热更新模式运行：
# uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
服务启动后，可在 `http://localhost:8000/docs` 查看 Swagger 格式的自动生成 API 文档。

### 2. 运行前端服务

```bash
cd frontend

# 安装前端依赖
npm install

# 启动前端开发环境
npm run dev
```
按照终端提示（通常为 `http://localhost:5173/`）在浏览器中访问前端系统。

## 项目结构说明

```text
FinVest/
├── backend/                  # Python 后端工程目录
│   ├── main.py               # FastAPI 服务入口及路由定义
│   ├── data_fetcher.py       # AkShare 数据获取封装层
│   ├── value_engine.py       # 价值评分分析引擎
│   ├── market_engine.py      # 大盘评分分析引擎
│   ├── capital_engine.py     # 资金评分分析引擎
│   └── requirements.txt      # 后端依赖清单
├── frontend/                 # React 前端工程目录
│   ├── src/                  # 前端源码 (React + Vite + Shoelace)
│   ├── package.json          # 前端依赖配置
│   └── vite.config.ts        # Vite 构建配置
├── test_*.py                 # 各类网络代理及AkShare环境可用性的验证/测试脚本
└── 三因共振量化决策体系v2.2.docx # 核心业务理论指导手册
```
