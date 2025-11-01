#!/usr/bin/env python3
"""
複数の命式での大運計算システムテスト
"""

from datetime import datetime, timezone, timedelta
from accurate_daeun_calculator import AccurateDaeunCalculator
import sys
import os

# 만세력 계산기 임포트
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.manseryeok.calculator import ManseryeokCalculator

KST = timezone(timedelta(hours=9))

def create_test_cases():
    """テストケースを作成"""
    test_cases = [
        {
            'name': '男性A（検証済み）',
            'birth_date': datetime(1986, 5, 26, 5, 0, tzinfo=KST),
            'gender': 'male',
            'description': '期待値との比較検証済み'
        },
        {
            'name': '女性A（検証済み）',
            'birth_date': datetime(1986, 12, 20, 0, 0, tzinfo=KST),
            'gender': 'female',
            'description': '期待値との比較検証済み'
        },
        {
            'name': '男性B（春生まれ）',
            'birth_date': datetime(1986, 3, 15, 10, 30, tzinfo=KST),
            'gender': 'male',
            'description': '春（驚蟄後）生まれのテスト'
        },
        {
            'name': '女性B（夏生まれ）',
            'birth_date': datetime(1986, 7, 20, 14, 45, tzinfo=KST),
            'gender': 'female',
            'description': '夏（小暑後）生まれのテスト'
        },
        {
            'name': '男性C（秋生まれ）',
            'birth_date': datetime(1986, 9, 30, 8, 15, tzinfo=KST),
            'gender': 'male',
            'description': '秋（白露後）生まれのテスト'
        },
        {
            'name': '女性C（冬生まれ）',
            'birth_date': datetime(1986, 1, 20, 22, 0, tzinfo=KST),
            'gender': 'female',
            'description': '冬（大寒前）生まれのテスト'
        }
    ]
    
    return test_cases

def test_saju_calculation(birth_date, gender):
    """四柱計算のテスト"""
    try:
        calculator = ManseryeokCalculator()
        saju = calculator.calculate_saju(birth_date, gender)
        
        return {
            'year_stem': saju.year_stem,
            'year_branch': saju.year_branch,
            'month_stem': saju.month_stem,
            'month_branch': saju.month_branch,
            'day_stem': saju.day_stem,
            'day_branch': saju.day_branch,
            'hour_stem': saju.hour_stem,
            'hour_branch': saju.hour_branch,
            'ganzi': f"{saju.year_stem}{saju.year_branch} {saju.month_stem}{saju.month_branch} {saju.day_stem}{saju.day_branch} {saju.hour_stem}{saju.hour_branch}"
        }
    except Exception as e:
        return {'error': str(e)}

def test_daeun_calculation(birth_date, gender):
    """大運計算のテスト"""
    try:
        # 万世力で四柱取得
        calculator = ManseryeokCalculator()
        saju = calculator.calculate_saju(birth_date, gender)
        
        # 性別を英語に変換
        gender_en = 'male' if gender == 'male' else 'female'
        
        # 大運計算
        daeun_calc = AccurateDaeunCalculator()
        starting_age = daeun_calc.calculate_starting_age(
            birth_date, 
            gender_en, 
            saju.year_stem
        )
        
        return {
            'starting_age': starting_age,
            'year_stem': saju.year_stem,
            'direction': '順行' if ((stems.index(saju.year_stem) % 2 == 0 and gender == 'male') or 
                                   (stems.index(saju.year_stem) % 2 == 1 and gender == 'female')) else '逆行'
        }
        
    except Exception as e:
        return {'error': str(e)}

def analyze_test_result(test_case, saju_result, daeun_result):
    """テスト結果の分析"""
    print(f"\n{'='*60}")
    print(f"【{test_case['name']}】{test_case['description']}")
    print(f"生年月日: {test_case['birth_date'].strftime('%Y/%m/%d %H:%M')} ({test_case['gender']})")
    print(f"{'='*60}")
    
    # 四柱結果
    if 'error' in saju_result:
        print(f"❌ 四柱計算エラー: {saju_result['error']}")
        return
    
    print(f"📋 四柱: {saju_result['ganzi']}")
    print(f"   年干: {saju_result['year_stem']} (陽干: {stems.index(saju_result['year_stem']) % 2 == 0})")
    
    # 大運結果
    if 'error' in daeun_result:
        print(f"❌ 大運計算エラー: {daeun_result['error']}")
        return
    
    print(f"🔮 大運方向: {daeun_result['direction']}")
    print(f"🎯 起運年齢: {daeun_result['starting_age']}歳")
    
    # 大運開始日の計算（概算）
    start_year = test_case['birth_date'].year + daeun_result['starting_age']
    estimated_start = test_case['birth_date'].replace(year=start_year)
    print(f"📅 大運開始日（概算）: {estimated_start.strftime('%Y/%m/%d')}")

def run_comprehensive_test():
    """包括的なテスト実行"""
    print("🧪 大運計算システム包括テスト")
    print("="*80)
    
    test_cases = create_test_cases()
    
    for test_case in test_cases:
        # 四柱計算
        saju_result = test_saju_calculation(test_case['birth_date'], test_case['gender'])
        
        # 大運計算  
        daeun_result = test_daeun_calculation(test_case['birth_date'], test_case['gender'])
        
        # 結果分析
        analyze_test_result(test_case, saju_result, daeun_result)
    
    print(f"\n{'='*80}")
    print("📊 テスト完了")

def test_edge_cases():
    """エッジケースのテスト"""
    print(f"\n{'='*80}")
    print("🔍 エッジケースのテスト")
    print(f"{'='*80}")
    
    edge_cases = [
        {
            'name': '節入日直前',
            'birth_date': datetime(1986, 6, 6, 7, 40, 0, tzinfo=KST),  # 芒種4分前
            'gender': 'male',
            'description': '芒種の4分前生まれ'
        },
        {
            'name': '節入日直後', 
            'birth_date': datetime(1986, 6, 6, 7, 50, 0, tzinfo=KST),  # 芒種6分後
            'gender': 'male',
            'description': '芒種の6分後生まれ'
        },
        {
            'name': '年末生まれ',
            'birth_date': datetime(1986, 12, 31, 23, 59, 0, tzinfo=KST),
            'gender': 'female',
            'description': '年末ギリギリ生まれ'
        }
    ]
    
    for case in edge_cases:
        saju_result = test_saju_calculation(case['birth_date'], case['gender'])
        daeun_result = test_daeun_calculation(case['birth_date'], case['gender'])
        analyze_test_result(case, saju_result, daeun_result)

# 天干のリスト（順逆判定用）
stems = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']

def main():
    try:
        # 基本テスト
        run_comprehensive_test()
        
        # エッジケース
        test_edge_cases()
        
    except Exception as e:
        print(f"❌ テスト実行エラー: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()