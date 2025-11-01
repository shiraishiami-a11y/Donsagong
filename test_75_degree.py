#!/usr/bin/env python3
"""
太陽黄経75度がいつになるかを1年通して調べる
"""

import ephem
from datetime import datetime

def find_75_degree_in_1986():
    """1986年中の太陽黄経75度を探す"""
    print("=== 1986年中の太陽黄経75度の検索 ===")
    
    sun = ephem.Sun()
    observer = ephem.Observer()
    observer.long = '127.0'
    observer.lat = '37.5'
    
    # 1年間毎日チェック
    for month in range(1, 13):
        days_in_month = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month-1]  # 1986年は平年
        if month == 2:
            days_in_month = 28  # 1986年は平年
            
        for day in range(1, days_in_month + 1):
            try:
                test_date = ephem.Date(f'1986/{month}/{day}')
                observer.date = test_date
                sun.compute(observer)
                
                longitude_deg = float(sun.hlon) * 180 / ephem.pi
                
                # 75度に近い日をチェック
                if abs(longitude_deg - 75.0) < 1.0:
                    print(f"1986/{month:02d}/{day:02d}: 太陽黄経 {longitude_deg:.2f}度")
                    if abs(longitude_deg - 75.0) < 0.1:
                        print(f"  ← 非常に近い！")
            except:
                continue

def check_calculation_function():
    """calculate_solar_term_time関数の詳細動作確認"""
    print("\n=== calculate_solar_term_time関数の動作確認 ===")
    
    from generate_jeolip_database import calculate_solar_term_time
    
    # 芒種（75度）を1986年で計算
    result = calculate_solar_term_time(1986, 75.0)
    print(f"1986年、太陽黄経75度: {result}")
    
    # 他の年でも試してみる
    for year in [1985, 1986, 1987]:
        result = calculate_solar_term_time(year, 75.0)
        print(f"{year}年、太陽黄経75度: {result}")

if __name__ == "__main__":
    find_75_degree_in_1986()
    check_calculation_function()