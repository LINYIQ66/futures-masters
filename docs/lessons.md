# 核心教训 — 八位期货大师的共同原则

## 🏆 终极共识

经过系统研究八位最成功的期货交易大师，提炼出以下共同原则：

### 原则 1：趋势是你的朋友
**所有大师都顺势交易**
- Jesse Livermore: "赚大钱靠整体趋势"
- Ed Seykota: "趋势就是你的朋友"
- Richard Dennis: 通道突破系统
- Larry Williams: 动量跟随
- Paul Tudor Jones: 200日均线趋势

**编程实现**: EMA交叉 + 价格位置 + ADX趋势强度

### 原则 2：止损先于入场
**每笔交易先想好亏多少**
- Seykota: 单笔风险≤2%
- Dennis: 2×ATR止损
- Jones: 永远不要平均亏损

**编程实现**: 计算止损位 → 算出仓位大小 → 再入场

### 原则 3：让利润奔跑
**盈利头寸要敢于加仓**
- Livermore: 关键点确认后分批加仓
- Dennis: 每移动0.5×ATR加一个Unit（最多4个）
- Jones: 盈亏比≥5:1

**编程实现**: 追踪止损 + 分批加仓逻辑

### 原则 4：情绪是最大敌人
**系统化、机械化执行**
- Seykota: 情绪过滤器
- Jones: 每天假设之前的交易是错的
- Dennis: 系统规则代替直觉

**编程实现**: 回测验证 → 自动执行 → 不干预

### 原则 5：仓位管理决定生死
**风险控制 > 预测方向**
- 所有大师: 单笔风险 1-2%
- Druckenmiller: 高确信时集中押注
- Kovner: 先确定止损再确定仓位

**编程实现**: 仓位 = 资金 × 风险% ÷ 止损距离

### 原则 6：大赚小亏
**胜率不重要，盈亏比才关键**
- Jones: 盈亏比 5:1
- Dennis: 40%胜率也能赚大钱
- Livermore: 10次小亏 + 1次大赚 = 整体盈利

**编程实现**: 只做盈亏比≥3:1的交易

---

## 💡 实战建议（针对加密合约）

### 1. 不要过度交易
- 大师们交易频率都很低
- 一个月可能只做2-3笔高质量交易
- 频繁交易 = 频繁犯错

### 2. 选择高波动性市场
- BTC/ETH/SOL 趋势性强
- 避免低波动率的小币种
- 主趋势方向才开仓

### 3. 杠杆要保守
- 大师们很少用高杠杆
- 建议杠杆 2-5x
- 最多不超过 10x

### 4. 等待高概率信号
- 不是每天都需要交易
- 市场不确定时 = 空仓等待
- 现金也是仓位

### 5. 记录每一笔交易
- 入场原因
- 止损位
- 目标位
- 实际结果
- 教训

---

## 📊 推荐组合策略（适合加密合约）

```python
# 1. 趋势识别（Seykota）
ema_13 = close.ewm(span=13).mean()
ema_55 = close.ewm(span=55).mean()
trend = "UP" if ema_13 > ema_55 else "DOWN"

# 2. 动量确认（Williams）
momentum = (close - close.shift(10)) / close.shift(10) * 100

# 3. 入场信号（Livermore/Dennis）
if trend == "UP" and momentum > 0:
    signal = "BUY"

# 4. 止损设置（Dennis）
atr = calculate_atr(df, 14)
stop_loss = entry - 2 * atr

# 5. 仓位管理（Seykota/Jones）
position_size = capital * 0.02 / (2 * atr)

# 6. 盈亏比检查（Jones）
risk_reward = (take_profit - entry) / (entry - stop_loss)
if risk_reward >= 3:
    execute_trade()
```

---

## ⚠️ 警告

1. **没有万能策略** — 每个策略都有亏损期
2. **回测不等于实盘** — 过去的表现不代表未来
3. **情绪管理最重要** — 再好的系统也扛不住手贱
4. **持续学习** — 市场在变，策略也要进化
5. **风险自担** — 这只是学习资料，不构成投资建议
