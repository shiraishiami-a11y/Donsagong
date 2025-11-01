#!/usr/bin/env python3
"""
正しい太陽黄経と節入日の対応を確認・修正
"""

import ephem
from datetime import datetime

def check_correct_solar_longitudes():
    """正しい太陽黄経を確認"""
    print("=== 正しい太陽黄経の確認 ===")
    
    # 実際の2024年の節入日で太陽黄経を確認
    known_dates = [
        ('立春', '2024/2/4'),   # 春の始まり
        ('驚蟄', '2024/3/5'),   # 
        ('清明', '2024/4/4'),   # 
        ('立夏', '2024/5/5'),   # 夏の始まり
        ('芒種', '2024/6/5'),   # 
        ('小暑', '2024/7/6'),   # 
        ('立秋', '2024/8/7'),   # 秋の始まり
        ('白露', '2024/9/7'),   # 
        ('寒露', '2024/10/8'),  # 
        ('立冬', '2024/11/7'),  # 冬の始まり
        ('大雪', '2024/12/6'),  # 
        ('小寒', '2025/1/5'),   # 
    ]
    
    sun = ephem.Sun()
    observer = ephem.Observer()
    observer.long = '127.0'
    observer.lat = '37.5'
    
    for name, date_str in known_dates:
        test_date = ephem.Date(date_str)
        observer.date = test_date
        sun.compute(observer)
        
        longitude_deg = float(sun.hlon) * 180 / ephem.pi
        print(f"{name}: {date_str} → 太陽黄経 {longitude_deg:.1f}度")

def check_1986_june():
    """1986年6月の詳細確認"""
    print("\n=== 1986年6月の太陽黄経詳細 ===")
    
    sun = ephem.Sun()
    observer = ephem.Observer()
    observer.long = '127.0'
    observer.lat = '37.5'
    
    # 6月1日-30日
    for day in [1, 5, 6, 7, 10, 15, 20, 25, 30]:
        test_date = ephem.Date(f'1986/6/{day}')
        observer.date = test_date
        sun.compute(observer)
        
        longitude_deg = float(sun.hlon) * 180 / ephem.pi
        print(f"1986/6/{day}: 太陽黄経 {longitude_deg:.1f}度")
        
        # 75度に近いかチェック
        if abs(longitude_deg - 75.0) < 5.0:
            print(f"  ← 芒種（75度）に近い")

if __name__ == "__main__":
    check_correct_solar_longitudes()
    check_1986_june()