#!/usr/bin/env python3
"""
複数のテストケース検証
1903年6月30日0時生まれ女子、1909年12月12日12時生まれ男子
"""

from datetime import datetime, timezone, timedelta
from accurate_daeun_calculator import AccurateDaeunCalculator
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.manseryeok.calculator import ManseryeokCalculator

KST = timezone(timedelta(hours=9))

def test_case(birth_date, gender, case_name):
    """個別ケースのテスト"""
    
    print(f"\n{'='*80}")
    print(f"📊 {case_name}")
    print("="*80)
    print(f"生年月日時: {birth_date.strftime('%Y年%m月%d日 %H時%M分')} KST")
    print(f"性別: {gender}")
    print()
    
    try:
        # 四柱計算
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
            
            # 大運周期計算（10年ごと）
            print("【大運周期】")
            print("-" * 40)
            start_year = result['precise_start'].year
            start_age = result['starting_age']
            
            # 月柱の干支を取得して大運を進める
            stems = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
            branches = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
            
            # 月柱のインデックスを取得
            month_stem_idx = stems.index(saju.month_stem)
            month_branch_idx = branches.index(saju.month_branch)
            
            # 順行か逆行かで進む方向を決める
            if result['direction'] == 'forward':
                direction_sign = 1
            else:
                direction_sign = -1
            
            # 最初の5つの大運を表示
            for i in range(5):
                daeun_stem_idx = (month_stem_idx + direction_sign * (i + 1)) % 10
                daeun_branch_idx = (month_branch_idx + direction_sign * (i + 1)) % 12
                
                daeun_stem = stems[daeun_stem_idx]
                daeun_branch = branches[daeun_branch_idx]
                
                age_start = start_age + i * 10
                age_end = age_start + 9
                year_start = birth_date.year + age_start
                year_end = birth_date.year + age_end
                
                print(f"第{i+1}大運: {daeun_stem}{daeun_branch} ({age_start}-{age_end}歳, {year_start}-{year_end}年)")
            
            print()
            
            # 結果サマリー
            print("【結果サマリー】")
            print("-" * 40)
            print(f"命式: {saju.year_stem}{saju.year_branch} {saju.month_stem}{saju.month_branch} {saju.day_stem}{saju.day_branch} {saju.hour_stem}{saju.hour_branch}")
            print(f"起運年齢: {result['starting_age']}歳")
            print(f"大運開始: {result['precise_start'].strftime('%Y年%m月%d日')}")
            print(f"大運方向: {'順行' if result['direction'] == 'forward' else '逆行'}")
            
            return True
            
        else:
            print(f"❌ 大運計算エラー: {result}")
            return False
            
    except Exception as e:
        print(f"❌ システムエラー: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """メインテスト実行"""
    
    print("🔮 複数ケース統合テスト")
    print("="*80)
    
    test_cases = [
        {
            'date': datetime(1903, 6, 30, 0, 0, tzinfo=KST),
            'gender': 'female',
            'name': 'ケース1: 1903年6月30日0時生まれ女子'
        },
        {
            'date': datetime(1909, 12, 12, 12, 0, tzinfo=KST),
            'gender': 'male',
            'name': 'ケース2: 1909年12月12日12時生まれ男子'
        }
    ]
    
    results = []
    for case in test_cases:
        success = test_case(case['date'], case['gender'], case['name'])
        results.append((case['name'], success))
    
    # 最終結果
    print(f"\n{'='*80}")
    print("📈 テスト結果まとめ")
    print("="*80)
    
    for name, success in results:
        status = "✅ 成功" if success else "❌ 失敗"
        print(f"{name}: {status}")
    
    all_success = all(r[1] for r in results)
    if all_success:
        print("\n🎉 すべてのテストケースが成功しました！")
    else:
        print("\n⚠️ 一部のテストケースで問題が発生しました")

if __name__ == "__main__":
    main()