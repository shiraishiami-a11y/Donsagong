#!/usr/bin/env python3
"""
節入日計算のデバッグスクリプト
1986年芒種の正確な計算を検証
"""

import ephem
from datetime import datetime, timezone, timedelta

KST = timezone(timedelta(hours=9))

def debug_mangzhong_1986():
    """1986年芒種の計算をデバッグ"""
    print("=== 1986年芒種（太陽黄経75度）の計算 ===")
    
    sun = ephem.Sun()
    observer = ephem.Observer()
    observer.long = '127.0'  # ソウル経度
    observer.lat = '37.5'    # ソウル緯度
    
    # 6月5日-10日の範囲で太陽黄経をチェック
    for day in range(5, 11):
        test_date = ephem.Date(f'1986/6/{day}')
        observer.date = test_date
        sun.compute(observer)
        
        longitude_deg = float(sun.hlon) * 180 / ephem.pi
        print(f"1986/6/{day}: 太陽黄経 {longitude_deg:.2f}度")
        
        if abs(longitude_deg - 75.0) < 1.0:
            print(f"  ← 芒種に最も近い（目標75度）")

def debug_solar_term_calculation():
    """節入時刻計算関数の直接テスト"""
    print("\n=== calculate_solar_term_time関数のテスト ===")
    
    from generate_jeolip_database import calculate_solar_term_time
    
    # 1986年芒種を計算
    mangzhong_time = calculate_solar_term_time(1986, 75.0)
    print(f"計算された1986年芒種: {mangzhong_time}")
    
    # 他の節も確認
    terms_to_test = [
        ('立春', 315.0),
        ('芒種', 75.0),
        ('大雪', 255.0)
    ]
    
    for name, longitude in terms_to_test:
        term_time = calculate_solar_term_time(1986, longitude)
        print(f"{name}（{longitude}度）: {term_time.strftime('%Y/%m/%d %H:%M')}")

if __name__ == "__main__":
    debug_mangzhong_1986()
    debug_solar_term_calculation()