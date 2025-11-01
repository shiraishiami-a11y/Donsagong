#!/usr/bin/env python3
"""
1908年10月10日10時生まれ男子の正確な大運計算テスト
修正版AccurateDaeunCalculatorと正確な節気データベース使用
"""

from datetime import datetime, timezone, timedelta
from accurate_daeun_calculator import AccurateDaeunCalculator
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.manseryeok.calculator import ManseryeokCalculator

KST = timezone(timedelta(hours=9))

def test_1908_male_accurate():
    """1908年男子の修正版システムでの正確計算"""
    
    print("=" * 80)
    print("🎯 1908年10月10日10時生まれ男子の正確計算（修正版システム）")
    print("=" * 80)
    
    # 基本情報
    birth_date = datetime(1908, 10, 10, 10, 0, tzinfo=KST)
    gender = 'male'
    
    print(f"📅 生年月日時: {birth_date.strftime('%Y年%m月%d日 %H時%M分')} KST")
    print(f"👤 性別: {gender}")
    print()
    
    try:
        # ステップ1: 修正版四柱計算
        print("【ステップ1】修正版四柱計算")
        print("-" * 40)
        
        calculator = ManseryeokCalculator()
        saju = calculator.calculate_saju(birth_date, gender)
        
        print(f"四柱結果: {saju.year_stem}{saju.year_branch} {saju.month_stem}{saju.month_branch} {saju.day_stem}{saju.day_branch} {saju.hour_stem}{saju.hour_branch}")
        
        # 期待値検証
        expected_ganzi = "戊申 壬戌 戊戌 丁巳"
        actual_ganzi = f"{saju.year_stem}{saju.year_branch} {saju.month_stem}{saju.month_branch} {saju.day_stem}{saju.day_branch} {saju.hour_stem}{saju.hour_branch}"
        
        print(f"期待値: {expected_ganzi}")
        print(f"計算値: {actual_ganzi}")
        print(f"年干検証: {saju.year_stem} {'✅' if saju.year_stem == '戊' else '❌'}")
        print()
        
        # ステップ2: 正確な大運計算
        print("【ステップ2】正確な大運計算（修正版AccurateDaeunCalculator）")
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
            
            # 최종 결과
            print("【최종 결과 검증】")
            print("-" * 40)
            print(f"사주: {actual_ganzi}")
            print(f"기운연령: {result['starting_age']}세")
            print(f"대운개시일: {result['precise_start'].strftime('%Y년%m월%d일')}")
            
            # 1908년 절기 데이터 사용 확인
            if '1908' in str(result['jeol_date']):
                print("✅ 1908년 절기 데이터 정상 사용")
            else:
                print("⚠️ 추정 데이터 사용 중")
                
        else:
            print(f"❌ 대운계산 오류: {result}")
            
    except Exception as e:
        print(f"❌ 시스템 오류: {e}")
        import traceback
        traceback.print_exc()
    
    print(f"\n{'='*80}")
    print("🏁 1908년 정확계산 테스트 완료")

def main():
    test_1908_male_accurate()

if __name__ == "__main__":
    main()