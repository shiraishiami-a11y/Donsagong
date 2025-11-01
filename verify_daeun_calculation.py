#!/usr/bin/env python3
"""
大運計算の詳細検証スクリプト
期待値：1990年2月10日頃と実際の計算結果を比較
"""

from datetime import datetime, timezone, timedelta
from accurate_daeun_calculator import AccurateDaeunCalculator

def manual_calculation_check():
    """手動計算による検証"""
    print("=== 手動計算による大運開始日検証 ===")
    
    # テストケース
    birth_date = datetime(1986, 5, 26, 5, 0, tzinfo=timezone(timedelta(hours=9)))
    expected_start = datetime(1990, 2, 10)  # 期待される開始日
    
    print(f"生年月日: {birth_date.strftime('%Y/%m/%d %H:%M')}")
    print(f"期待する大運開始日: {expected_start.strftime('%Y/%m/%d')}")
    
    # 期待値から逆算
    expected_diff = expected_start - birth_date.replace(tzinfo=None)
    expected_days = expected_diff.days
    expected_years = expected_days / 365.25
    
    print(f"期待値からの逆算:")
    print(f"  日数差: {expected_days}日")
    print(f"  年数: {expected_years:.6f}年")
    
    # 3日=1年法則で逆算
    required_jeol_days = expected_years * 365.25 * 3
    print(f"  必要な節入日までの日数: {required_jeol_days:.1f}日")
    
    # 実際の計算
    calc = AccurateDaeunCalculator()
    calculated_age = calc.calculate_starting_age(birth_date, 'male', '丙')
    
    return expected_start

def alternative_calculation():
    """別の計算方法の検証"""
    print("\n=== 別の大運計算方法 ===")
    
    birth_date = datetime(1986, 5, 26, 5, 0)
    
    # 伝統的な計算方法：節気からの日数 ÷ 3 = 年数
    # 1986年の芒種は6月6日頃のはず
    
    # 手動で芒種を設定（データベースと比較用）
    estimated_mangzhong = datetime(1986, 6, 6, 13, 0)  # 概算
    
    days_to_jeol = (estimated_mangzhong - birth_date).days
    years_by_3day_rule = days_to_jeol / 3
    
    print(f"概算芒種日: {estimated_mangzhong.strftime('%Y/%m/%d %H:%M')}")
    print(f"節入日までの日数: {days_to_jeol}日")
    print(f"3日=1年法則: {days_to_jeol} ÷ 3 = {years_by_3day_rule:.3f}年")
    
    # 大運開始日計算
    start_date = birth_date.replace(year=birth_date.year + int(years_by_3day_rule))
    fractional_days = (years_by_3day_rule % 1) * 365.25
    accurate_start = start_date + timedelta(days=fractional_days)
    
    print(f"計算された大運開始日: {accurate_start.strftime('%Y/%m/%d')}")

if __name__ == "__main__":
    expected = manual_calculation_check()
    alternative_calculation()
    
    print("\n=== 検証結果 ===")
    print("期待値（1990/2/10）と実際の計算（1990/5/30）に約3.5ヶ月の差があります")
    print("可能な原因:")
    print("1. 節入日データの精度")
    print("2. 3日=1年法則の適用方法")
    print("3. 起運年齢の解釈")
    print("4. 暦法の違い（太陽暦 vs 太陰暦）")