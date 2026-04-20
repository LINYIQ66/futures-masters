# Futures Masters — 期货交易大师策略库

系统化研究世界顶级期货/合约交易大师的策略，提炼可编程、可回测的交易规则。

## 大师清单

| # | 大师 | 年代 | 核心风格 | 传奇战绩 |
|---|------|------|---------|---------|
| 1 | Jesse Livermore | 1900s | 趋势跟踪 + 关键点突破 | 从$5到$1亿（今日~$15亿） |
| 2 | Ed Seykota | 1970s | 趋势跟踪 + 情绪过滤 | $5k→$1500万（12年） |
| 3 | Richard Dennis | 1980s | 系统化趋势跟踪 | $1600→$2亿 |
| 4 | Larry Williams | 1980s | 动量指标 + 季节性 | $1万→$110万（1年） |
| 5 | Paul Tudor Jones | 1980s | 反转 + 风险管理 | 1987崩盘做空赚$1亿 |
| 6 | Stanley Druckenmiller | 1990s | 宏观趋势 + 集中押注 | 年均回报30%无亏损年 |
| 7 | Bill Lipschutz | 1980s | 外汇/合约 + 概率思维 | 年赚$3亿（所罗门兄弟） |
| 8 | Bruce Kovner | 1980s | 宏观 + 止损纪律 | $3k→$110亿基金 |

## 项目结构

```
futures-masters/
├── README.md                 # 本文件
├── strategies/
│   ├── livermore.md          # Livermore 关键点突破策略
│   ├── seykota.md            # Seykota 趋势+情绪策略
│   ├── dennis.md             # Dennis 海龟交易法则
│   ├── williams.md           # Williams %R + 动量
│   ├── tudor-jones.md        # Jones 反转+风控
│   ├── druckenmiller.md      # Druckenmiller 集中押注
│   ├── lipschutz.md          # Lipschutz 概率交易
│   └── kovner.md             # Kovner 宏观+止损
├── signals/                  # 可编程信号指标
│   ├── key_point_breakout.py # Livermore 关键点突破
│   ├── trend_filter.py       # Seykota 趋势过滤器
│   ├── turtle_breakout.py    # Dennis 海龟通道突破
│   ├── williams_r.py         # Williams %R 指标
│   └── momentum_reversal.py  # Jones 动量反转
├── backtest/                 # 回测框架
│   ├── engine.py             # 简易回测引擎
│   └── results/              # 回测结果
└── docs/
    └── lessons.md            # 共同教训与核心原则
```

## 快速开始

```bash
pip install pandas numpy ta-lib
cd signals
python key_point_breakout.py --symbol BTC-USDT-SWAP --days 90
```

## 核心共识（所有大师共有的原则）

1. **趋势是你的朋友** — 8/8 大师都强调顺势交易
2. **止损先于入场** — 先想好亏多少再决定买多少
3. **让利润奔跑** — 盈利头寸加仓，亏损头寸绝不加
4. **情绪是最大敌人** — 系统化、机械化执行
5. **仓位管理决定生死** — 单笔风险不超过总资金2%
6. **大赚小亏** — 胜率不重要，盈亏比才关键

## License

MIT — 自由使用、修改、分享
