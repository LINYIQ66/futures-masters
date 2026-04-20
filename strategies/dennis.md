# Richard Dennis — 海龟交易法则

## 简介
- **年代**: 1949-present
- **绰号**: 面龟之王 (The Turtle Trader)
- **传奇**: $1,600 → $2亿（10年）
- **实验**: 1983年用$1,000和2周培训创造了史上最成功的交易员培训计划

## 核心哲学

### 1. 系统化交易
Dennis 最重要的贡献：**证明了交易可以被系统化和教学**
- 他与 William Eckhardt 打赌：交易是天赋还是技能
- 结论：**系统 + 纪律 > 天赋**

### 2. 海龟交易法则（完整版）

#### A. 入场信号 — 通道突破
```python
# 20日通道突破做多
if close > highest_20d:
    BUY  # 做多

# 10日通道突破做空
if close < lowest_10d:
    SELL  # 做空
```

#### B. 仓位管理 — ATR法
```python
def turtle_position_size(capital, atr, risk_pct=0.01):
    """
    海龟仓位 = (资金 × 风险%) / ATR
    每个"Unit"的风险 = 资金的1%
    """
    unit = capital * risk_pct / atr
    return int(unit)
```

#### C. 加仓规则
```
价格每移动 0.5×ATR 就加一个 Unit
最多加到 4个 Unit
```

#### D. 止损规则
```
入场后 2×ATR 反方向 → 止损
```

#### E. 退出规则
```
10日反方向突破 → 退出
或
止损触发 → 立即退出
```

## 完整可编程策略

```python
import pandas as pd
import numpy as np

def turtle_strategy(df, capital=100000):
    """
    海龟交易法则完整实现
    df: DataFrame with columns [high, low, close]
    """
    df['highest_20d'] = df['high'].rolling(20).max()
    df['lowest_10d'] = df['low'].rolling(10).min()
    df['atr'] = calculate_atr(df, 14)
    
    position = 0
    entry_price = 0
    stop_loss = 0
    units = 0
    
    for i in range(20, len(df)):
        close = df['close'].iloc[i]
        atr = df['atr'].iloc[i]
        
        # 入场
        if position == 0:
            if close > df['highest_20d'].iloc[i-1]:
                position = 1
                entry_price = close
                stop_loss = close - 2 * atr
                units = 1
            elif close < df['lowest_10d'].iloc[i-1]:
                position = -1
                entry_price = close
                stop_loss = close + 2 * atr
                units = 1
        
        # 加仓
        elif position == 1 and units < 4:
            if close >= entry_price + 0.5 * atr * units:
                units += 1
                entry_price = (entry_price * (units-1) + close) / units
        
        # 止损/退出
        elif position == 1:
            if close <= stop_loss or close < df['lowest_10d'].iloc[i-1]:
                position = 0
                units = 0

def calculate_atr(df, period=14):
    high_low = df['high'] - df['low']
    high_close = abs(df['high'] - df['close'].shift())
    low_close = abs(df['low'] - df['close'].shift())
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    return tr.rolling(period).mean()
```

## 经典名言

> "我总说你可以在报纸上公布我的交易法则，但没人会遵守。关键在于连续亏损时你能否还坚持执行。"

> "交易中最重要的事不是你对了多少次，而是你对的时候赚了多少钱。"

> "如果我不是每次都止损，我会破产无数次。"

## 适用市场
- ✅ 商品期货（原始市场）
- ✅ 加密货币（波动率高，趋势明显）
- ✅ 所有高波动率趋势性市场
- ⚠️ 低波动震荡市场需要过滤器
