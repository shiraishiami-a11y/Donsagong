#!/usr/bin/env python3
"""
期待値ケースの直接テスト: 1900年12月10日女性
期待結果: 生後0年10ヶ月16日、初大運1901年10月25日ごろ
"""

import sys
import os
from datetime import datetime, timezone, timedelta

# 万世暦計算機とデータベース計算機をインポート
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.manseryeok.calculator import ManseryeokCalculator
from test_1900_random_case import Enhanced1900DaeunCalculator

KST = timezone(timedelta(hours=9))

def test_expected_case():
    """期待値ケースをテスト"""
    print("🎯 期待値ケーステスト")
    print("=" * 80)
    
    # 期待値ケース
    birth_date = datetime(1900, 12, 10, 13, 10, tzinfo=KST)
    gender = 'female'
    expected_start = datetime(1901, 10, 25, tzinfo=KST)
    
    print(f"📅 テストケース:")
    print(f"   生年月日時: {birth_date.strftime('%Y年%m月%d日 %H時%M分')} KST")
    print(f"   性別: {gender}")
    print(f"   期待初大運: {expected_start.strftime('%Y年%m月%d日')}ごろ")
    print(f"   期待起運期間: 生後0年10ヶ月16日")
    
    # 四柱計算
    try:
        calculator = ManseryeokCalculator()
        saju = calculator.calculate_saju(birth_date, gender)
        
        print(f"\n📋 四柱計算結果:")
        print(f"   年柱: {saju.year_stem}{saju.year_branch}")
        print(f"   月柱: {saju.month_stem}{saju.month_branch}")
        print(f"   日柱: {saju.day_stem}{saju.day_branch}")
        print(f"   時柱: {saju.hour_stem}{saju.hour_branch}")
        print(f"   完整四柱: {saju.year_stem}{saju.year_branch} {saju.month_stem}{saju.month_branch} {saju.day_stem}{saju.day_branch} {saju.hour_stem}{saju.hour_branch}")
        
        # 大運計算
        daeun_calc = Enhanced1900DaeunCalculator()
        result = daeun_calc.calculate_starting_age(birth_date, gender, saju.year_stem)
        
        if 'error' not in result:
            print(f"\n🔮 大運計算結果:")
            print(f"   大運方向: {result['direction']} ({'順行' if result['direction'] == 'forward' else '逆行'})")
            print(f"   関連節入日: {result['jeol_date'].strftime('%Y/%m/%d %H:%M')} ({result['jeol_name']})")
            print(f"   日数差: {result['days_diff']:.3f}日")
            print(f"   起運年齢: {result['starting_age']}歳")
            print(f"   精密大運開始日: {result['precise_start'].strftime('%Y年%m月%d日 %H時%M分')}")
            
            # 期待値との比較
            print(f"\n📊 期待値との比較:")
            calc_start = result['precise_start']
            diff_days = (calc_start - expected_start).days
            print(f"   計算結果: {calc_start.strftime('%Y年%m月%d日')}")
            print(f"   期待値: {expected_start.strftime('%Y年%m月%d日')}")
            print(f"   差: {diff_days}日")
            
            # 起運期間の計算
            birth_to_start = calc_start - birth_date
            months = birth_to_start.days / 30.44
            years = int(months // 12)
            remaining_months = int(months % 12)
            remaining_days = int((months % 1) * 30.44)
            
            print(f"   計算起運期間: 生後{years}年{remaining_months}ヶ月{remaining_days}日")
            print(f"   期待起運期間: 生後0年10ヶ月16日")
            
            if abs(diff_days) <= 30:  # 1ヶ月以内の誤差
                print(f"   ✅ 精度良好 (誤差{abs(diff_days)}日)")
            else:
                print(f"   ❌ 精度不足 (誤差{abs(diff_days)}日)")
                
        else:
            print(f"\n❌ 大運計算エラー: {result['error']}")
            
    except Exception as e:
        print(f"\n❌ 計算エラー: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_expected_case()