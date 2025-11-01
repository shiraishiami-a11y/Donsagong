#!/usr/bin/env python3
"""
1909年12月12日12時生まれ男子の命式と大運を計算
lunar-python統合版で正確な計算
"""

from datetime import datetime, timezone, timedelta
from accurate_daeun_calculator import AccurateDaeunCalculator
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.manseryeok.calculator import ManseryeokCalculator

KST = timezone(timedelta(hours=9))

def test_1909_male():
    """1909年12月12日12時生まれ男子のテスト"""
    
    print("="*80)
    print("📊 1909年12月12日12時生まれ男子")
    print("="*80)
    
    birth_date = datetime(1909, 12, 12, 12, 0, tzinfo=KST)
    gender = 'male'
    
    print(f"生年月日時: {birth_date.strftime('%Y年%m月%d日 %H時%M分')} KST")
    print(f"性別: {gender}")
    print()
    
    try:
        # 四柱計算（lunar-python使用）
        print("【四柱計算】")
        print("-" * 40)
        
        calculator = ManseryeokCalculator()
        saju = calculator.calculate_saju(birth_date, gender)
        
        print(f"年柱: {saju.year_stem}{saju.year_branch}")
        print(f"月柱: {saju.month_stem}{saju.month_branch}")
        print(f"日柱: {saju.day_stem}{saju.day_branch}")
        print(f"時柱: {saju.hour_stem}{saju.hour_branch}")
        print(f"完整四柱: {saju.year_stem}{saju.year_branch} {saju.month_stem}{saju.month_branch} {saju.day_stem}{saju.day_branch} {saju.hour_stem}{saju.hour_branch}")
        print()
        
        # 大運計算
        print("【大運計算】")
        print("-" * 40)
        
        daeun_calc = AccurateDaeunCalculator('solar_terms_1900-1910_database.json')
        result = daeun_calc.calculate_starting_age(birth_date, gender, saju.year_stem)
        
        if isinstance(result, dict) and 'error' not in result:
            print(f"✅ 大運計算成功")
            print(f"大運方向: {result['direction']} ({'順行' if result['direction'] == 'forward' else '逆行'})")
            print(f"関連節入日: {result['jeol_date'].strftime('%Y/%m/%d %H:%M')} ({result['jeol_name']})")
            print(f"日数差: {result['days_diff']:.3f}日")
            print(f"起運年齢: {result['starting_age']}歳")
            print(f"精密大運開始日: {result['precise_start'].strftime('%Y年%m月%d日 %H時%M分')}")
            print()
            
            # 大運周期計算
            print("【大運周期】")
            print("-" * 40)
            
            stems = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
            branches = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
            
            month_stem_idx = stems.index(saju.month_stem)
            month_branch_idx = branches.index(saju.month_branch)
            
            if result['direction'] == 'forward':
                direction_sign = 1
            else:
                direction_sign = -1
            
            for i in range(8):  # 8個の大運
                daeun_stem_idx = (month_stem_idx + direction_sign * (i + 1)) % 10
                daeun_branch_idx = (month_branch_idx + direction_sign * (i + 1)) % 12
                
                daeun_stem = stems[daeun_stem_idx]
                daeun_branch = branches[daeun_branch_idx]
                
                age_start = result['starting_age'] + i * 10
                age_end = age_start + 9
                year_start = birth_date.year + age_start
                year_end = birth_date.year + age_end
                
                print(f"第{i+1}大運: {daeun_stem}{daeun_branch} ({age_start}-{age_end}歳, {year_start}-{year_end}年)")
            
            print()
            
            # 結果サマリー
            print("【最終結果】")
            print("-" * 40)
            print(f"命式: {saju.year_stem}{saju.year_branch} {saju.month_stem}{saju.month_branch} {saju.day_stem}{saju.day_branch} {saju.hour_stem}{saju.hour_branch}")
            print(f"起運年齢: {result['starting_age']}歳")
            print(f"大運開始: {result['precise_start'].strftime('%Y年%m月%d日')}")
            print(f"大運方向: {'順行' if result['direction'] == 'forward' else '逆行'}")
            
            # 判定ロジックの説明
            print()
            print("【判定ロジック】")
            print("-" * 40)
            print(f"年干: {saju.year_stem}")
            stem_index = stems.index(saju.year_stem)
            is_yang = (stem_index % 2 == 0)
            print(f"陰陽: {'陽干' if is_yang else '陰干'}")
            print(f"性別: 男性")
            print(f"結果: {'陰干' if not is_yang else '陽干'} + 男性 = {'逆行' if not is_yang else '順行'}")
            
        else:
            print(f"❌ 大運計算エラー: {result}")
            
    except Exception as e:
        print(f"❌ システムエラー: {e}")
        import traceback
        traceback.print_exc()

def main():
    test_1909_male()

if __name__ == "__main__":
    main()