#!/usr/bin/env python3
"""
1903年6月30日0時女子の命式計算をデバッグ
節入日との関係を詳細に確認
"""

from datetime import datetime, timezone, timedelta
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.manseryeok.calculator import ManseryeokCalculator

KST = timezone(timedelta(hours=9))

def debug_1903_calculation():
    """1903年6月30日の命式計算を詳細確認"""
    
    birth_date = datetime(1903, 6, 30, 0, 0, tzinfo=KST)
    gender = 'female'
    
    print("="*80)
    print("🔍 1903年6月30日0時生まれ女子の命式デバッグ")
    print("="*80)
    print(f"生年月日時: {birth_date}")
    print()
    
    # 節入日の確認
    print("【節入日確認】")
    print("-"*40)
    
    # 立春（年の境界）
    lichun_1903 = datetime(1903, 2, 5, 7, 31, 17, tzinfo=KST)
    print(f"1903年立春: {lichun_1903}")
    
    # 芒種（6月の節気）
    mangzhong_1903 = datetime(1903, 6, 6, 6, 27, tzinfo=KST) 
    print(f"1903年芒種: {mangzhong_1903}")
    
    # 小暑（7月の節気）
    xiaoshu_1903 = datetime(1903, 7, 7, 16, 58, tzinfo=KST)
    print(f"1903年小暑: {xiaoshu_1903}")
    
    print()
    print("生年月日との関係:")
    print(f"  立春 < 生年月日 ✓ (1903年生まれ)")
    print(f"  芒種 < 生年月日 < 小暑 → 午月（6月節気）")
    print()
    
    # ManseryeokCalculatorで計算
    print("【ManseryeokCalculator計算】")
    print("-"*40)
    
    calculator = ManseryeokCalculator()
    saju = calculator.calculate_saju(birth_date, gender)
    
    print(f"年柱: {saju.year_stem}{saju.year_branch}")
    print(f"月柱: {saju.month_stem}{saju.month_branch}")
    print(f"日柱: {saju.day_stem}{saju.day_branch}")
    print(f"時柱: {saju.hour_stem}{saju.hour_branch}")
    print()
    
    # 年柱の詳細計算
    print("【年柱の詳細計算】")
    print("-"*40)
    year_num = 1903
    # 天干: (年 - 3) % 10
    year_stem_idx = (year_num - 3) % 10  # 1903 - 3 = 1900, 1900 % 10 = 0
    # 地支: (年 - 3) % 12  
    year_branch_idx = (year_num - 3) % 12  # 1900 % 12 = 4
    
    stems = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
    branches = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
    
    print(f"年干計算: (1903 - 3) % 10 = {year_stem_idx} → {stems[year_stem_idx]} (×)")
    print(f"年支計算: (1903 - 3) % 12 = {year_branch_idx} → {branches[year_branch_idx]} (×)")
    
    # 六十花甲による正しい計算
    print()
    print("【六十花甲による計算】")
    cycle_base_year = 1864  # 甲子年
    years_since = year_num - cycle_base_year  # 1903 - 1864 = 39
    cycle_position = years_since % 60  # 39
    
    year_stem_correct = cycle_position % 10  # 39 % 10 = 9
    year_branch_correct = cycle_position % 12  # 39 % 12 = 3
    
    print(f"基準年(甲子): 1864年")
    print(f"経過年数: 1903 - 1864 = {years_since}年")
    print(f"60年周期位置: {cycle_position}")
    print(f"年干: {cycle_position} % 10 = {year_stem_correct} → {stems[year_stem_correct]}")
    print(f"年支: {cycle_position} % 12 = {year_branch_correct} → {branches[year_branch_correct]}")
    print(f"正しい年柱: {stems[year_stem_correct]}{branches[year_branch_correct]}")
    print()
    
    # 月柱の詳細計算
    print("【月柱の詳細計算】")
    print("-"*40)
    
    # 節気による月判定
    if birth_date >= mangzhong_1903 and birth_date < xiaoshu_1903:
        month_branch = "午"
        month_branch_idx = 6  # 午は7番目（0起点で6）
        print(f"節気月: 午月（芒種〜小暑）")
    else:
        print("節気月の判定エラー")
        
    # 月干の計算：年干からの算出
    # 戊年の場合の月干
    year_stem_for_month = year_stem_correct  # 癸 = 9
    month_stem_table = [
        ['甲', '丙', '戊', '庚', '壬'],  # 甲・己の年
        ['乙', '丁', '己', '辛', '癸'],  # 乙・庚の年
        ['丙', '戊', '庚', '壬', '甲'],  # 丙・辛の年
        ['丁', '己', '辛', '癸', '乙'],  # 丁・壬の年
        ['戊', '庚', '壬', '甲', '丙'],  # 戊・癸の年
    ]
    
    # 癸年（9）は戊・癸グループ（インデックス4）
    month_stem_row = 4
    # 午月（6月）は5番目の月
    month_position = 5  # 0から数えて5
    month_stem = month_stem_table[month_stem_row][month_position % 5]
    
    print(f"年干{stems[year_stem_correct]}の午月の月干: {month_stem}")
    print(f"正しい月柱: {month_stem}{month_branch}")
    
    return saju

if __name__ == "__main__":
    debug_1903_calculation()