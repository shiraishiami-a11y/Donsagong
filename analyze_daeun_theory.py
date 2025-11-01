#!/usr/bin/env python3
"""
大運計算理論の詳細分析
期待値（1990/2/10）から逆算して正しい計算方法を探る
"""

from datetime import datetime, timedelta

def analyze_expected_calculation():
    """期待値から逆算分析"""
    print("=== 期待値から逆算分析 ===")
    
    birth_date = datetime(1986, 5, 26, 5, 0, 0)
    expected_start = datetime(1990, 2, 10)
    
    # 期待値までの日数
    expected_days = (expected_start - birth_date).days
    expected_years = expected_days / 365.25
    
    print(f"生年月日: {birth_date.strftime('%Y/%m/%d %H:%M')}")
    print(f"期待する大運開始: {expected_start.strftime('%Y/%m/%d')}")
    print(f"期間: {expected_days}日 ({expected_years:.3f}年)")
    
    # 3日=1年法則で必要な節入日までの日数を逆算
    if expected_years > 3:
        # 起運年齢が3歳の場合
        required_jeol_days = (expected_years - 3) * 3
        ideal_jeol_date = birth_date + timedelta(days=required_jeol_days)
        print(f"\n【起運年齢3歳の場合】")
        print(f"必要な節入日までの日数: {required_jeol_days:.1f}日")
        print(f"理想的な節入日: {ideal_jeol_date.strftime('%Y/%m/%d %H:%M')}")
        
    if expected_years > 4:
        # 起運年齢が4歳の場合
        required_jeol_days = (expected_years - 4) * 3
        ideal_jeol_date = birth_date + timedelta(days=required_jeol_days)
        print(f"\n【起運年齢4歳の場合】")
        print(f"必要な節入日までの日数: {required_jeol_days:.1f}日")
        print(f"理想的な節入日: {ideal_jeol_date.strftime('%Y/%m/%d %H:%M')}")
    
    if expected_years > 5:
        # 起運年齢が5歳の場合
        required_jeol_days = (expected_years - 5) * 3
        ideal_jeol_date = birth_date + timedelta(days=required_jeol_days)
        print(f"\n【起運年齢5歳の場合】")
        print(f"必要な節入日までの日数: {required_jeol_days:.1f}日")
        print(f"理想的な節入日: {ideal_jeol_date.strftime('%Y/%m/%d %H:%M')}")

def test_alternative_calculations():
    """代替計算方法のテスト"""
    print("\n=== 代替計算方法のテスト ===")
    
    birth_date = datetime(1986, 5, 26, 5, 0, 0)
    mangzhong_date = datetime(1986, 6, 6, 7, 44, 23)
    
    # 現在の計算方法
    days_diff = (mangzhong_date - birth_date).total_seconds() / 86400
    current_method = int(days_diff / 3)
    current_start = birth_date.replace(year=birth_date.year + current_method)
    
    print(f"現在の方法: 日数差 {days_diff:.1f}日 → {current_method}歳 → {current_start.strftime('%Y/%m/%d')}")
    
    # 方法1: 小数部分も考慮
    precise_years = days_diff / 3
    fractional_days = (precise_years % 1) * 365.25
    precise_start = birth_date.replace(year=birth_date.year + int(precise_years)) + timedelta(days=fractional_days)
    
    print(f"精密計算: {precise_years:.3f}年 → {precise_start.strftime('%Y/%m/%d')}")
    
    # 方法2: 1日=1年の法則（間違いかもしれませんが検証）
    if_1day_1year = int(days_diff)
    alt_start = birth_date.replace(year=birth_date.year + if_1day_1year)
    
    print(f"1日=1年の場合: {days_diff:.1f}日 → {if_1day_1year}歳 → {alt_start.strftime('%Y/%m/%d')}")
    
    # 方法3: 10日=1年の法則
    if_10day_1year = int(days_diff / 10)
    alt_start2 = birth_date.replace(year=birth_date.year + if_10day_1year)
    
    print(f"10日=1年の場合: {days_diff:.1f}日 → {if_10day_1year}歳 → {alt_start2.strftime('%Y/%m/%d')}")

def check_different_solar_terms():
    """異なる節気を使った場合の検証"""
    print("\n=== 異なる節気を使った場合の検証 ===")
    
    birth_date = datetime(1986, 5, 26, 5, 0, 0)
    expected_start = datetime(1990, 2, 10)
    
    # 1986年の主要な節気
    solar_terms = {
        '立夏': datetime(1986, 5, 6, 3, 24, 0),
        '芒種': datetime(1986, 6, 6, 7, 44, 23),
        '小暑': datetime(1986, 7, 7, 12, 45, 0),
        '立秋': datetime(1986, 8, 8, 2, 36, 0)
    }
    
    print("各節気を使った場合の大運開始日:")
    for term_name, term_date in solar_terms.items():
        days_diff = (term_date - birth_date).total_seconds() / 86400
        starting_age = int(days_diff / 3)
        calculated_start = birth_date.replace(year=birth_date.year + starting_age)
        
        diff_from_expected = (expected_start - calculated_start).days
        
        print(f"{term_name}: {days_diff:.1f}日 → {starting_age}歳 → {calculated_start.strftime('%Y/%m/%d')} (期待値との差: {diff_from_expected}日)")

def theoretical_investigation():
    """理論的な調査"""
    print("\n=== 理論的な調査 ===")
    
    birth_date = datetime(1986, 5, 26, 5, 0, 0)
    expected_start = datetime(1990, 2, 10)
    
    # 期待値に正確に合わせるために必要な条件を計算
    expected_days_total = (expected_start - birth_date).days
    
    print(f"期待される総日数: {expected_days_total}日")
    
    # さまざまな起運年齢での必要な節入日までの日数
    for age in range(1, 11):
        remaining_days = expected_days_total - (age * 365.25)
        required_jeol_days = remaining_days / 3 if remaining_days > 0 else 0
        
        if 0 < required_jeol_days < 365:  # 1年以内の妥当な範囲
            ideal_jeol = birth_date + timedelta(days=required_jeol_days)
            print(f"起運年齢{age}歳の場合: 節入日まで{required_jeol_days:.1f}日 → {ideal_jeol.strftime('%Y/%m/%d %H:%M')}")

def main():
    analyze_expected_calculation()
    test_alternative_calculations() 
    check_different_solar_terms()
    theoretical_investigation()

if __name__ == "__main__":
    main()