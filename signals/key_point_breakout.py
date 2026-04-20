#!/usr/bin/env python3
"""
Livermore 关键点突破信号 — 加密货币永续合约版
基于 Jesse Livermore 的关键点理论
"""
import pandas as pd
import numpy as np
import requests
import sys
from datetime import datetime

def fetch_ohlcv(symbol='BTC-USDT', interval='1D', limit=100):
    """从 CoinGecko 或 OKX 获取OHLCV数据"""
    # 使用 OKX 公开接口
    inst_id = f"{symbol}" if '-SWAP' in symbol else f"{symbol}"
    url = f"https://www.okx.com/api/v5/market/candles?instId={inst_id}&bar={interval}&limit={limit}"
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

def key_point_breakout(df, lookback=20, volume_mult=1.5):
    """
    Livermore 关键点突破策略
    
    做多信号:
    1. 收盘价突破N日最高点
    2. 成交量 > N日平均成交量 × 1.5
    
    做空信号:
    1. 收盘价跌破N日最低点
    2. 成交量 > N日平均成交量 × 1.5
    """
    df['highest'] = df['high'].rolling(lookback).max()
    df['lowest'] = df['low'].rolling(lookback).min()
    df['avg_vol'] = df['vol'].rolling(lookback).mean()
    
    signals = []
    for i in range(lookback, len(df)):
        close = df['close'].iloc[i]
        vol = df['vol'].iloc[i]
        prev_high = df['highest'].iloc[i-1]
        prev_low = df['lowest'].iloc[i-1]
        avg_vol = df['avg_vol'].iloc[i]
        
        if close > prev_high and vol > avg_vol * volume_mult:
            signals.append({
                'date': df['ts'].iloc[i],
                'type': 'BUY',
                'price': close,
                'reason': f'突破{lookback}日高点 {prev_high:.2f}',
                'volume_ratio': vol / avg_vol
            })
        elif close < prev_low and vol > avg_vol * volume_mult:
            signals.append({
                'date': df['ts'].iloc[i],
                'type': 'SELL',
                'price': close,
                'reason': f'跌破{lookback}日低点 {prev_low:.2f}',
                'volume_ratio': vol / avg_vol
            })
    
    return signals

def calculate_position_size(capital, entry, stop_loss, risk_pct=0.02):
    """仓位计算：单笔风险不超过总资金2%"""
    risk_amount = capital * risk_pct
    risk_per_unit = abs(entry - stop_loss)
    if risk_per_unit == 0:
        return 0
    return risk_amount / risk_per_unit

if __name__ == '__main__':
    symbol = sys.argv[1] if len(sys.argv) > 1 else 'BTC-USDT-SWAP'
    interval = sys.argv[2] if len(sys.argv) > 2 else '1D'
    
    print(f"🔍 分析 {symbol} ({interval})")
    print("=" * 50)
    
    df = fetch_ohlcv(symbol, interval, 100)
    if df is None:
        print("❌ 获取数据失败")
        sys.exit(1)
    
    signals = key_point_breakout(df, lookback=20, volume_mult=1.3)
    
    if signals:
        print(f"\n📊 发现 {len(signals)} 个关键点信号：\n")
        for s in signals[-5:]:  # 显示最近5个
            emoji = "🟢" if s['type'] == 'BUY' else "🔴"
            print(f"  {emoji} {s['date'].strftime('%Y-%m-%d')} | {s['type']} | ${s['price']:,.2f}")
            print(f"     原因: {s['reason']}")
            print(f"     量比: {s['volume_ratio']:.2f}x")
            print()
    else:
        print("\n😴 当前无关键点突破信号")
    
    # 当前状态
    latest = df.iloc[-1]
    print(f"\n📍 当前状态:")
    print(f"  价格: ${latest['close']:,.2f}")
    print(f"  20日高点: ${df['highest'].iloc[-1]:,.2f}")
    print(f"  20日低点: ${df['lowest'].iloc[-1]:,.2f}")
    print(f"  距离高点: {((df['highest'].iloc[-1] - latest['close']) / latest['close'] * 100):.2f}%")
    print(f"  距离低点: {((latest['close'] - df['lowest'].iloc[-1]) / latest['close'] * 100):.2f}%")
