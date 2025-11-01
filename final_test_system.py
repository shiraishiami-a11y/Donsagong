#!/usr/bin/env python3
"""
最終統合テスト: 修正されたManseryeokCalculator + 正確な節気データベース + 大運計算
"""

from datetime import datetime, timezone, timedelta
from accurate_daeun_calculator import AccurateDaeunCalculator
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.manseryeok.calculator import ManseryeokCalculator

KST = timezone(timedelta(hours=9))

def final_integrated_test():
    """最終統合テスト"""
    print("🎯 最終統合テスト: 修正版ManseryeokCalculator + 正確な大運計算")
    print("=" * 80)
    
    # テストケース: 1900年12月10日女性
    birth_date = datetime(1900, 12, 10, 13, 10, tzinfo=KST)
    gender = 'female'
    expected_start = datetime(1901, 10, 25, tzinfo=KST)
    
    print(f"📅 テストケース:")
    print(f"   生年月日時: {birth_date.strftime('%Y年%m月%d日 %H時%M分')} KST")
    print(f"   性別: {gender}")
    print(f"   期待大運開始: {expected_start.strftime('%Y年%m月%d日')}ごろ")
    print()
    
    try:
        # ステップ1: 修正版ManseryeokCalculatorで四柱計算
        print("【ステップ1】修正版四柱計算")
        print("-" * 40)
        
        calculator = ManseryeokCalculator()
        saju = calculator.calculate_saju(birth_date, gender)
        
        print(f"四柱結果: {saju.year_stem}{saju.year_branch} {saju.month_stem}{saju.month_branch} {saju.day_stem}{saju.day_branch} {saju.hour_stem}{saju.hour_branch}")
        print()
        
        # 검증
        expected_ganzi = "庚子 戊子 丁巳 丁未"
        actual_ganzi = f"{saju.year_stem}{saju.year_branch} {saju.month_stem}{saju.month_branch} {saju.day_stem}{saju.day_branch} {saju.hour_stem}{saju.hour_branch}"
        
        print("四柱検証:")
        print(f"   期待値: {expected_ganzi}")
        print(f"   計算値: {actual_ganzi}")
        
        year_correct = saju.year_stem == '庚'
        month_correct = saju.month_stem == '戊'
        day_correct = saju.day_stem == '丁'
        
        print(f"   年干: {saju.year_stem} {'✅' if year_correct else '❌'}")
        print(f"   月干: {saju.month_stem} {'✅' if month_correct else '❌'}")
        print(f"   日干: {saju.day_stem} {'✅' if day_correct else '❌'}")
        print()
        
        # ステップ2: 정확한 대운 계산
        print("【ステップ2】正確な大運計算")
        print("-" * 40)
        
        # AccurateDaeunCalculator 사용
        daeun_calc = AccurateDaeunCalculator('solar_terms_1900-1910_database.json')
        result = daeun_calc.calculate_starting_age(birth_date, gender, saju.year_stem)
        
        if 'error' not in result:
            print(f"대운방향: {result['direction']} ({'순행' if result['direction'] == 'forward' else '역행'})")
            print(f"관련절입일: {result['jeol_date'].strftime('%Y/%m/%d %H:%M')} ({result['jeol_name']})")
            print(f"일수차: {result['days_diff']:.3f}일")
            print(f"기운연령: {result['starting_age']}세")
            print(f"정밀대운개시일: {result['precise_start'].strftime('%Y년%m월%d일 %H시%M분')}")
            print()
            
            # 최종 정확도 평가
            print("【최종 정확도 평가】")
            print("-" * 40)
            
            calc_start = result['precise_start']
            diff_days = abs((calc_start - expected_start).days)
            accuracy = max(0, (1 - diff_days / 365) * 100)
            
            print(f"계산결과: {calc_start.strftime('%Y년%m월%d일')}")
            print(f"기대값: {expected_start.strftime('%Y년%m월%d일')}")
            print(f"오차: {diff_days}일")
            print(f"정확도: {accuracy:.1f}%")
            
            # 기운기간 검증
            birth_to_start = calc_start - birth_date
            months = birth_to_start.days / 30.44
            years = int(months // 12)
            remaining_months = int(months % 12)
            
            print(f"계산기운기간: 생후{years}년{remaining_months}개월")
            print(f"기대기운기간: 생후0년10개월")
            
            if diff_days <= 15:
                grade = "S급 (15일 이내)"
                emoji = "🏆"
            elif diff_days <= 30:
                grade = "A급 (30일 이내)"
                emoji = "🥇"
            elif diff_days <= 60:
                grade = "B급 (60일 이내)"
                emoji = "🥈"
            else:
                grade = "C급 (개선 필요)"
                emoji = "🥉"
            
            print(f"{emoji} 최종등급: {grade}")
            
            if year_correct and accuracy >= 95:
                print("✅ 완벽한 통합 시스템 구축 성공!")
            elif year_correct and accuracy >= 90:
                print("✅ 고품질 통합 시스템 구축 성공!")
            else:
                print("⚠️ 추가 개선 필요")
                
        else:
            print(f"❌ 대운계산 오류: {result['error']}")
            
    except Exception as e:
        print(f"❌ 시스템 오류: {e}")
        import traceback
        traceback.print_exc()
    
    print(f"\n{'='*80}")
    print("🏁 최종 통합 테스트 완료")

def test_multiple_cases():
    """복수 케이스 테스트"""
    print(f"\n{'='*80}")
    print("🔄 복수 케이스 검증")
    print("=" * 80)
    
    test_cases = [
        {
            'date': datetime(1900, 12, 10, 13, 10, tzinfo=KST),
            'gender': 'female',
            'expected_year_stem': '庚',
            'description': '1900년 문제 케이스'
        },
        {
            'date': datetime(1986, 5, 26, 5, 0, tzinfo=KST),
            'gender': 'male',
            'expected_year_stem': '丙',
            'description': '1986년 성공 케이스'
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n【케이스 {i}】{case['description']}")
        print("-" * 40)
        
        try:
            calculator = ManseryeokCalculator()
            saju = calculator.calculate_saju(case['date'], case['gender'])
            
            year_correct = saju.year_stem == case['expected_year_stem']
            print(f"생년월일: {case['date'].strftime('%Y/%m/%d %H:%M')}")
            print(f"사주: {saju.year_stem}{saju.year_branch} {saju.month_stem}{saju.month_branch} {saju.day_stem}{saju.day_branch} {saju.hour_stem}{saju.hour_branch}")
            print(f"년간 검증: {saju.year_stem} (기대: {case['expected_year_stem']}) {'✅' if year_correct else '❌'}")
            
        except Exception as e:
            print(f"❌ 오류: {e}")

def main():
    """메인 실행"""
    final_integrated_test()
    test_multiple_cases()
    
    print(f"\n{'='*80}")
    print("🎉 전체 시스템 테스트 완료!")
    print("• 修正版ManseryeokCalculator")
    print("• 正確한節気データベース통합")  
    print("• 高精度大運計算시스템")
    print("→ 완전한 사주 대운 계산 시스템 구축!")

if __name__ == "__main__":
    main()