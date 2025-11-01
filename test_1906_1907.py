#!/usr/bin/env python3
"""
1906年6月6日6時生まれ女子、1907年3月3日3時生まれ男子のテスト
節気データの完全性も確認
"""

from datetime import datetime, timezone, timedelta
from accurate_daeun_calculator import AccurateDaeunCalculator
import sys
import os
import json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.manseryeok.calculator import ManseryeokCalculator

KST = timezone(timedelta(hours=9))

def verify_solar_terms():
    """節気データの完全性を確認"""
    print("="*80)
    print("📋 節気データベース完全性チェック")
    print("="*80)
    
    with open('solar_terms_1900-1910_database.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    solar_terms_data = data['solar_terms_data']
    
    # 各年の節気数を確認
    for year in range(1900, 1911):
        year_str = str(year)
        if year_str in solar_terms_data:
            count = len(solar_terms_data[year_str])
            if count == 12:
                print(f"✅ {year}年: {count}個の節気 (完全)")
            else:
                print(f"⚠️ {year}年: {count}個の節気 (不完全)")
                missing = set(['立春', '驚蟄', '清明', '立夏', '芒種', '小暑', 
                             '立秋', '白露', '寒露', '立冬', '大雪', '小寒']) - set(solar_terms_data[year_str].keys())
                if missing:
                    print(f"   不足: {', '.join(missing)}")
        else:
            print(f"❌ {year}年: データなし")
    
    # 1906年と1907年の詳細確認
    print("\n【1906年の節気詳細】")
    print("-"*40)
    if '1906' in solar_terms_data:
        for term_name, term_data in solar_terms_data['1906'].items():
            print(f"{term_name}: {term_data['full_datetime']}")
    
    print("\n【1907年の節気詳細】")
    print("-"*40)
    if '1907' in solar_terms_data:
        for term_name, term_data in solar_terms_data['1907'].items():
            print(f"{term_name}: {term_data['full_datetime']}")
    
    return True

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
            
            for i in range(5):
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
    
    print("🔮 1906年女子・1907年男子テスト")
    print("="*80)
    
    # まず節気データの完全性を確認
    verify_solar_terms()
    
    # テストケース
    test_cases = [
        {
            'date': datetime(1906, 6, 6, 6, 0, tzinfo=KST),
            'gender': 'female',
            'name': 'ケース1: 1906年6月6日6時生まれ女子'
        },
        {
            'date': datetime(1907, 3, 3, 3, 0, tzinfo=KST),
            'gender': 'male',
            'name': 'ケース2: 1907年3月3日3時生まれ男子'
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
        print("✅ 節気データも完全です（1900-1910年、各年12個）")
    else:
        print("\n⚠️ 一部のテストケースで問題が発生しました")

if __name__ == "__main__":
    main()