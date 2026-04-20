# Ed Seykota — 趋势+情绪过滤策略

## 简介
- **年代**: 1946-present
- **成就**: $5,000 → $15,000,000（12年，不含后续资金）
- **风格**: 计算机辅助趋势跟踪（1970s先驱）
- **著作**: 《交易者的智慧》(The Trading Tribe)

## 核心哲学

### 1. 资金管理金字塔
Seykota 认为交易成功由三个因素组成，按重要性排序：

```
资金管理 (60%) > 心态 (30%) > 入场策略 (10%)
```

### 2. 顺势 + 筛选
- **规则一**: 跟随趋势
- **规则二**: 切断亏损
- **规则三**: 让利润奔跑
- **规则四**: 大胆下注高概率机会

### 3. 情绪过滤
Seykota 的独特之处：用"情绪指标"过滤趋势信号
- 只在市场情绪极端时反向思考
- 恐慌时买入，贪婪时减仓

## 可编程信号

### 指数移动平均线趋势过滤
```python
def seykota_trend_filter(close, ema_short=13, ema_long=55):
    """
    Seykota 风格趋势过滤器
    - EMA13 > EMA55: 上升趋势
    - EMA13 < EMA55: 下降趋势
    """
    ema_s = close.ewm(span=ema_short).mean()
    ema_l = close.ewm(span=ema_long).mean()
    
    if ema_s.iloc[-1] > ema_l.iloc[-1] and ema_s.iloc[-2] <= ema_l.iloc[-2]:
        return "BUY"  # 金叉
    elif ema_s.iloc[-1] < ema_l.iloc[-1] and ema_s.iloc[-2] >= ema_l.iloc[-2]:
        return "SELL"  # 死叉
    return "HOLD"
```

### 情绪指标（简易版）
```python
def fear_greed_filter(price, period=20):
    """
    用价格位置判断市场情绪
    - 价格处于高位区间（>80%）：贪婪 → 不追多
    - 价格处于低位区间（<20%）：恐慌 → 不追空
    """
    high = price.rolling(period).max()
    low = price.rolling(period).min()
    position = (price - low) / (high - low)
    return position.iloc[-1]
```

### 风险管理
```python
def position_size(capital, risk_pct=0.02, entry, stop_loss):
    """
    单笔风险不超过总资金2%
    """
    risk_per_unit = abs(entry - stop_loss)
    max_risk = capital * risk_pct
    return int(max_risk / risk_per_unit)
```

## 经典名言

> "每个人从市场中得到的，正是他们想要的。"

> "规则存在的目的是让你自由。"

> "趋势就是你的朋友，直到它弯腰把你甩掉。"

## 适用市场
- ✅ 所有趋势性市场
- ✅ 加密货币（周期性强）
- ⚠️ 低波动震荡市场需降低仓位
