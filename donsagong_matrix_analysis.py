#!/usr/bin/env python3
"""
돈사공 천간 100 매트릭스 정확한 적용
각 천간의 길흉을 정확히 판단
"""

from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.manseryeok.calculator import ManseryeokCalculator

def analyze_bing_to_other(target_stem):
    """병화(丙) 일간이 다른 천간을 만날 때"""
    matrix = {
        '甲': ('길', '합일이 생김 - 나무를 키움'),
        '乙': ('길', '합일이 생김 - 꽃을 키움'),
        '丙': ('평', '원국에 함께 있을 때 흉, 대운으로 들어올 때는 원국 영향'),
        '丁': ('흉', '불, 여름은 이기고, 가을겨울은 당한다'),
        '戊': ('무', '감탄이 있어야 가치가 있다'),
        '己': ('무', '태양으로 乙을 키우니 가치가 적다'),
        '庚': ('흉', '병경합. 태양이 철에 의해 꺼진다'),
        '辛': ('대흉', '병신합. 빛이 의미 없어진다'),
        '壬': ('길', '해결사 역할'),
        '癸': ('길흉', '계절에 따라 다름')
    }
    return matrix.get(target_stem, ('평', ''))

def analyze_mu_to_other(target_stem):
    """무토(戊) 일간이 다른 천간을 만날 때"""
    matrix = {
        '甲': ('대길', '산에 나무가 자라 명산이 된다. 부(富)명'),
        '乙': ('소길', '큰 산이 묘목을 만나 아산으로 줄어들었다'),
        '丙': ('길', '화생토, 강하게 해준다'),
        '丁': ('길흉', '강하게 해준다. 목과 같이 있으면 안됨'),
        '戊': ('평', '원국에 함께 있을 때 흉, 대운으로 들어올 때는 원국 영향'),
        '己': ('흉', '산이 땅에 내려왔다. 격이 낮아짐'),
        '庚': ('흉', '토생금 해서 밑이주느라 힘 빠진다'),
        '辛': ('흉', '감목은 약하게, 을목은 깨진다'),
        '壬': ('평', '댐처럼 산이 강을 막아냄. 평형상태'),
        '癸': ('대흉', '무계합. 병화를 없애서 안 좋다')
    }
    return matrix.get(target_stem, ('평', ''))

def analyze_gi_to_other(target_stem):
    """기토(己) 일간이 다른 천간을 만날 때"""
    matrix = {
        '甲': ('흉', '갑기합. 욕심부리게 만든다'),
        '乙': ('길', '들판에 꽃을 피울 수 있다'),
        '丙': ('길', '乙이오면 수확물(財)이 생긴다'),
        '丁': ('길', '화생토. 가을겨울에는 필요'),
        '戊': ('흉', '언제든 당할 위험이 있다, 큰놈에게 뺏긴다'),
        '己': ('평', '원국에 함께 있을 때 흉, 대운으로 들어올 때는 원국 영향'),
        '庚': ('흉', '감목이 우박을 맞는다'),
        '辛': ('흉', '감목이 우박을 맞는다'),
        '壬': ('흉', '물바다 된다 (가난해진다)'),
        '癸': ('평', '제방, 둑과 같다, 가난은 막았다')
    }
    return matrix.get(target_stem, ('평', ''))

def analyze_gye_to_other(target_stem):
    """계수(癸) 일간이 다른 천간을 만날 때 - 역방향 필요"""
    # 상대방이 癸를 만날 때를 역으로 추정
    if target_stem == '庚':
        return ('길', '금생수 - 庚이 癸를 생함')
    elif target_stem == '戊':
        return ('대흉', '무계합')
    else:
        return ('평', '일반적 관계')

def analyze_gyeong_to_other(target_stem):
    """경금(庚) 일간이 다른 천간을 만날 때 - 역방향 필요"""
    if target_stem == '癸':
        return ('길', '금생수')
    elif target_stem == '丙':
        return ('흉', '병경합')
    else:
        return ('평', '일반적 관계')

def analyze_im_to_other(target_stem):
    """임수(壬) 일간이 다른 천간을 만날 때 - 역방향 필요"""
    if target_stem == '己':
        return ('흉', '己가 壬를 막음')
    elif target_stem == '戊':
        return ('평', '戊가 壬를 막지만 평형')
    else:
        return ('평', '일반적 관계')

def main():
    print("="*80)
    print("돈사공 천간 100 매트릭스 정확한 분석")
    print("="*80)
    
    calculator = ManseryeokCalculator()
    
    # 만세력 계산
    male_birth = datetime(1968, 12, 2, 2, 0, 0)
    male_saju = calculator.calculate_saju(male_birth, 'male')
    
    female_birth = datetime(1986, 12, 20, 0, 0, 0)
    female_saju = calculator.calculate_saju(female_birth, 'female')
    
    print("\n【사주 원국】")
    print(f"남성: {male_saju}")
    print(f"여성: {female_saju}")
    
    print("\n" + "="*60)
    print("천간 관계 분석 (돈사공 매트릭스)")
    print("="*60)
    
    # 월간 관계
    print("\n■ 월간 관계")
    print(f"남성 癸 → 여성 庚")
    result, desc = analyze_gye_to_other(female_saju.month_stem)
    print(f"남성 입장: {result} - {desc}")
    
    print(f"여성 庚 → 남성 癸")
    result, desc = analyze_gyeong_to_other(male_saju.month_stem)
    print(f"여성 입장: {result} - {desc}")
    
    # 일간 관계 (가장 중요!)
    print("\n■ 일간 관계 ★★★")
    print(f"남성 丙 → 여성 戊")
    result, desc = analyze_bing_to_other(female_saju.day_stem)
    symbol = "✅" if "길" in result else "❌" if "흉" in result else "◆"
    print(f"남성 입장: {result} {symbol} - {desc}")
    
    print(f"여성 戊 → 남성 丙")
    result, desc = analyze_mu_to_other(male_saju.day_stem)
    symbol = "✅" if "길" in result else "❌" if "흉" in result else "◆"
    print(f"여성 입장: {result} {symbol} - {desc}")
    
    # 시간 관계
    print("\n■ 시간 관계")
    print(f"남성 己 → 여성 壬")
    result, desc = analyze_gi_to_other(female_saju.hour_stem)
    symbol = "✅" if "길" in result else "❌" if "흉" in result else "◆"
    print(f"남성 입장: {result} {symbol} - {desc}")
    
    print(f"여성 壬 → 남성 己")
    result, desc = analyze_im_to_other(male_saju.hour_stem)
    symbol = "✅" if "길" in result else "❌" if "흉" in result else "◆"
    print(f"여성 입장: {result} {symbol} - {desc}")
    
    print("\n" + "="*60)
    print("종합 평가")
    print("="*60)
    
    print("\n【남성 입장에서의 평가】")
    print("• 일간: 丙→戊 = 무 (감탄이 있어야 가치)")
    print("• 월간: 癸→庚 = 길 (금생수)")
    print("• 시간: 己→壬 = 흉 (물바다가 됨)")
    print("→ 여성이 남성을 도와주는 관계")
    
    print("\n【여성 입장에서의 평가】")
    print("• 일간: 戊→丙 = 길 (화생토, 강하게 해줌)")
    print("• 월간: 庚→癸 = 길 (금생수)")
    print("• 시간: 壬→己 = 흉 (己가 막음)")
    print("→ 남성이 여성을 강하게 해주는 관계")
    
    print("\n【최종 판정】")
    print("• 일간 관계: 여성에게 유리, 남성에게는 보통")
    print("• 월간 관계: 서로 좋음")
    print("• 시간 관계: 서로 안 맞음")
    print("\n돈사공 평가: ★★★☆☆")
    print("남녀 입장 차이가 있는 관계. 여성에게 더 유리한 궁합")

if __name__ == "__main__":
    main()