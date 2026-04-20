#!/usr/bin/env python3
"""
Dennis 海龟通道突破信号 — 加密货币永续合约版
基于 Richard Dennis 的海龟交易法则
"""
import pandas as pd
import numpy as np
import requests
import sys

def fetch_ohlcv(symbol='BTC-USDT-SWAP', interval='1D', limit=100):
    """从OKX获取数据"""
    url = f"https://www.okx.com/api/v5/market/candles?instId={symbol}&bar={interval}&limit={limit}"
    r = requests.get(url, timeout=10)
    data = r.json()
    if data['code'] != '0':
        return None
    
    df = pd.DataFrame(data['data'], columns=[
        'ts', 'open', 'high', 'low', 'close', 'vol', 'volCcy', 'volCcyQuote', 'confirm'
    ])
    df['ts'] = pd.to_datetime(df['ts'].astype(int), unit='ms')
    for col in ['open', 'high', 'low', 'close', 'vol']:
        df[col] = df[col].astype(float)
    df = df.sort_values('ts').reset_index(drop=True)
    return df

def calculate_atr(df, period=14):
    """计算ATR"""
    high_low = df['high'] - df['low']
    high_close = abs(df['high'] - df['close'].shift())
    low_close = abs(df['low'] - df['close'].shift())
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    return tr.rolling(period).mean()

def turtle_breakout(df, entry_period=20, exit_period=10):
    """
    海龟通道突破策略
    
    入场: 价格突破N日最高/最低
    出场: 价格突破M日反方向
    止损: 2×ATR
    加仓: 每移动0.5×ATR加仓（最多4个Unit）
    """
    df['highest_entry'] = df['high'].rolling(entry_period).max()
    df['lowest_entry'] = df['low'].rolling(entry_period).min()
    df['highest_exit'] = df['high'].rolling(exit_period).max()
    df['lowest_exit'] = df['low'].rolling(exit_period).min()
    df['atr'] = calculate_atr(df, 14)
    
    signals = []
    position = 0  # 0=无仓位, 1=多头, -1=空头
    entry_price = 0
    units = 0
    
    for i in range(max(entry_period, exit_period), len(df)):
        close = df['close'].iloc[i]
        atr = df['atr'].iloc[i]
        
        if pd.isna(atr) or atr == 0:
            continue
        
        if position == 0:
            # 入场信号
            if close > df['highest_entry'].iloc[i-1]:
                position = 1
                entry_price = close
                units = 1
                signals.append({
                    'date': df['ts'].iloc[i],
                    'type': 'BUY',
                    'price': close,
                    'units': units,
                    'stop_loss': close - 2 * atr,
                    'atr': atr,
                    'reason': f'突破{entry_period}日高点'
                })
            elif close < df['lowest_entry'].iloc[i-1]:
                position = -1
                entry_price = close
                units = 1
                signals.append({
                    'date': df['ts'].iloc[i],
                    'type': 'SELL',
                    'price': close,
                    'units': units,
                    'stop_loss': close + 2 * atr,
                    'atr': atr,
                    'reason': f'跌破{entry_period}日低点'
                })
        
        elif position == 1:  # 多头
            # 检查止损
            stop = entry_price - 2 * atr
            if close <= stop:
                signals.append({
                    'date': df['ts'].iloc[i],
                    'type': 'STOP_LOSS',
                    'price': close,
                    'pnl': (close - entry_price) * units,
                    'reason': '止损出场'
                })
                position = 0
                units = 0
            # 检查退出
            elif close < df['lowest_exit'].iloc[i-1]:
                signals.append({
                    'date': df['ts'].iloc[i],
                    'type': 'EXIT',
                    'price': close,
                    'pnl': (close - entry_price) * units,
                    'reason': f'{exit_period}日低点出场'
                })
                position = 0
                units = 0
            # 加仓
            elif units < 4 and close >= entry_price + 0.5 * atr * units:
                units += 1
                signals.append({
                    'date': df['ts'].iloc[i],
                    'type': 'ADD',
                    'price': close,
                    'units': units,
                    'reason': f'加仓第{units}个Unit'
                })
        
        elif position == -1:  # 空头
            stop = entry_price + 2 * atr
            if close >= stop:
                signals.append({
                    'date': df['ts'].iloc[i],
                    'type': 'STOP_LOSS',
                    'price': close,
                    'pnl': (entry_price - close) * units,
                    'reason': '止损出场'
                })
                position = 0
                units = 0
            elif close > df['highest_exit'].iloc[i-1]:
                signals.append({
                    'date': df['ts'].iloc[i],
                    'type': 'EXIT',
                    'price': close,
                    'pnl': (entry_price - close) * units,
                    'reason': f'{exit_period}日高点出场'
                })
                position = 0
                units = 0
            elif units < 4 and close <= entry_price - 0.5 * atr * units:
                units += 1
                signals.append({
                    'date': df['ts'].iloc[i],
                    'type': 'ADD',
                    'price': close,
                    'units': units,
                    'reason': f'加仓第{units}个Unit'
                })
    
    return signals

if __name__ == '__main__':
    symbol = sys.argv[1] if len(sys.argv) > 1 else 'BTC-USDT-SWAP'
    interval = sys.argv[2] if len(sys.argv) > 2 else '1D'
    
    print(f"🐢 海龟策略分析 {symbol} ({interval})")
    print("=" * 50)
    
    df = fetch_ohlcv(symbol, interval, 100)
    if df is None:
        print("❌ 获取数据失败")
        sys.exit(1)
    
    signals = turtle_breakout(df)
    
    if signals:
        print(f"\n📊 发现 {len(signals)} 个信号：\n")
        for s in signals[-10:]:
            emoji = {"BUY": "🟢", "SELL": "🔴", "EXIT": "⚪", "STOP_LOSS": "⚠️", "ADD": "➕"}.get(s['type'], "❓")
            date = s['date'].strftime('%Y-%m-%d')
            print(f"  {emoji} {date} | {s['type']} | ${s['price']:,.2f}")
            print(f"     {s['reason']}")
            if 'stop_loss' in s:
                print(f"     止损: ${s['stop_loss']:,.2f}")
            if 'pnl' in s:
                pnl_emoji = "💰" if s['pnl'] > 0 else "💸"
                print(f"     {pnl_emoji} 盈亏: ${s['pnl']:,.2f}")
            if 'units' in s:
                print(f"     仓位: {s['units']} Unit(s)")
            print()
    else:
        print("\n😴 当前无海龟突破信号")
    
    # 当前状态
    latest = df.iloc[-1]
    atr = df['atr'].iloc[-1]
    print(f"\n📍 当前状态:")
    print(f"  价格: ${latest['close']:,.2f}")
    print(f"  ATR(14): ${atr:,.2f}")
    print(f"  20日高点: ${df['highest_entry'].iloc[-1]:,.2f}")
    print(f"  20日低点: ${df['lowest_entry'].iloc[-1]:,.2f}")
    print(f"  2×ATR止损距离: ${2*atr:,.2f} ({2*atr/latest['close']*100:.2f}%)")
