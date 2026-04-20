# Paul Tudor Jones — 反转+风控策略

## 简介
- **年代**: 1954-present
- **传奇**: 1987年"黑色星期一"做空美股，赚$1亿
- **基金**: Tudor Capital，管理$110亿+
- **年均回报**: ~19.5%（扣除费用后，40年无亏损年）

## 核心哲学

### 1. 风险第一，利润第二
Jones 最著名的原则：**永远不要平均亏损**

```
错误：价格跌了 → 买入更多 → 降低成本 → 等待反弹
正确：价格跌了 → 止损 → 等待新机会
```

### 2. 反转信号识别
Jones 特别擅长在市场极端情绪中捕捉反转：
- 市场狂热（量价背离）→ 准备做空
- 市场恐慌（VIX飙升）→ 准备做多

### 3. 200日均线法则
Jones 的核心指标：**200日移动平均线**

```python
def jones_200dma_signal(close, ma_period=200):
    """
    Jones 200日均线策略
    - 价格在MA200之上：只做多
    - 价格在MA200之下：只做空
    - 价格穿过MA200：趋势反转信号
    """
    ma = close.rolling(ma_period).mean()
    
    if close.iloc[-1] > ma.iloc[-1] and close.iloc[-2] <= ma.iloc[-2]:
        return "BUY_BREAKOUT"   # 突破MA200向上
    elif close.iloc[-1] < ma.iloc[-1] and close.iloc[-2] >= ma.iloc[-2]:
        return "SELL_BREAKOUT"  # 跌破MA200向下
    elif close.iloc[-1] > ma.iloc[-1]:
        return "BULLISH"        # 多头趋势
    else:
        return "BEARISH"        # 空头趋势
```

### 4. 量价背离反转
```python
def volume_price_divergence(close, volume, period=20):
    """
    量价背离识别
    - 价格创新高但成交量下降 → 多头衰竭 → 可能反转
    - 价格创新低但成交量下降 → 空头衰竭 → 可能反转
    """
    price_high = close.rolling(period).max()
    price_low = close.rolling(period).min()
    vol_avg = volume.rolling(period).mean()
    
    if close.iloc[-1] >= price_high.iloc[-1] and volume.iloc[-1] < vol_avg.iloc[-1]:
        return "BEARISH_DIVERGENCE"  # 多头背离，准备做空
    elif close.iloc[-1] <= price_low.iloc[-1] and volume.iloc[-1] < vol_avg.iloc[-1]:
        return "BULLISH_DIVERGENCE"  # 空头背离，准备做多
    return None
```

### 5. 仓位管理 — 2%规则
```python
def jones_position_size(capital, entry, stop_loss, max_risk=0.02):
    """
    单笔最大亏损 = 总资金 × 2%
    """
    risk_amount = capital * max_risk
    risk_per_unit = abs(entry - stop_loss)
    if risk_per_unit == 0:
        return 0
    return int(risk_amount / risk_per_unit)
```

### 6. 5:1 盈亏比
Jones 的目标：每笔交易盈亏比至少 5:1
```python
def calculate_risk_reward(entry, stop_loss, take_profit):
    risk = abs(entry - stop_loss)
    reward = abs(take_profit - entry)
    return reward / risk

# 只做盈亏比 ≥ 5:1 的交易
if risk_reward >= 5:
    execute_trade()
```

## 经典名言

> "不要总想着自己对不对，而要想如果自己错了亏多少。"

> "我每天都假设我之前的每一笔交易都是错的。"

> "最重要的是防守，不是进攻。如果你防守做得好，进攻自然会有机会。"

> "市场在变，人性不变。"

## 适用市场
- ✅ 股指期货（反转信号强）
- ✅ 加密货币（情绪极端频繁）
- ✅ 外汇（200日均线有效）
- ⚠️ 需要耐心等待高质量信号
