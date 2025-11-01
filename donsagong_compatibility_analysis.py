#!/usr/bin/env python3
"""
돈사공 시스템 기반 상세 상성 분석
Step 2: 돈사공 마스터 데이터베이스를 활용한 정확한 용신 분석
"""

from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.manseryeok.calculator import ManseryeokCalculator

def get_season_from_month_branch(month_branch):
    """월지지로 계절 판단"""
    seasons = {
        '寅': '봄', '卯': '봄', '辰': '봄',
        '巳': '여름', '午': '여름', '未': '여름',
        '申': '가을', '酉': '가을', '戌': '가을',
        '亥': '겨울', '子': '겨울', '丑': '겨울'
    }
    return seasons.get(month_branch, '알수없음')

def analyze_yongshin_bing(month_branch):
    """병화(丙火) 용신 분석"""
    season = get_season_from_month_branch(month_branch)
    
    cheongan_yongshin = {
        '봄': ['甲', '乙', '壬'],
        '여름': ['甲', '乙', '壬'],
        '가을': ['甲', '乙'],
        '겨울': ['戊', '甲', '乙']
    }
    
    jiji_yongshin = {
        '봄': ['辰'],
        '여름': ['辰', '申', '子'],
        '가을': ['寅'],
        '겨울': ['午', '戌', '未']
    }
    
    return {
        'season': season,
        'cheongan': cheongan_yongshin.get(season, []),
        'jiji': jiji_yongshin.get(season, [])
    }

def analyze_yongshin_mu(month_branch):
    """무토(戊土) 용신 분석"""
    season = get_season_from_month_branch(month_branch)
    
    cheongan_yongshin = {
        '봄': ['甲', '乙', '丙'],
        '여름': ['甲', '乙', '丙'],
        '가을': ['甲', '乙', '丙', '丁'],
        '겨울': ['丁', '丙', '甲', '乙']
    }
    
    jiji_yongshin = {
        '봄': ['辰'],
        '여름': ['辰', '申', '子'],
        '가을': ['寅', '卯', '辰'],
        '겨울': ['午', '戌', '未']
    }
    
    return {
        'season': season,
        'cheongan': cheongan_yongshin.get(season, []),
        'jiji': jiji_yongshin.get(season, [])
    }

def main():
    print("="*70)
    print("돈사공 시스템 기반 상세 상성 분석")
    print("="*70)
    
    calculator = ManseryeokCalculator()
    
    # Step 1: 만세력 계산
    print("\n【STEP 1: 만세력 계산】")
    print("-"*50)
    
    # 남성: 1968년 12월 2일 2시
    male_birth = datetime(1968, 12, 2, 2, 0, 0)
    male_saju = calculator.calculate_saju(male_birth, 'male')
    
    # 여성: 1986년 12월 20일 0시
    female_birth = datetime(1986, 12, 20, 0, 0, 0)
    female_saju = calculator.calculate_saju(female_birth, 'female')
    
    print("\n남성 (1968.12.2 02:00)")
    print(f"사주: {male_saju}")
    print(f"일간: {male_saju.day_stem} (丙火)")
    print(f"월지: {male_saju.month_branch} (亥 = 11월 = 겨울)")
    
    print("\n여성 (1986.12.20 00:00)")
    print(f"사주: {female_saju}")
    print(f"일간: {female_saju.day_stem} (戊土)")
    print(f"월지: {female_saju.month_branch} (子 = 12월 = 겨울)")
    
    # Step 2: 원국 용신 분석
    print("\n【STEP 2: 원국 용신 분석】")
    print("-"*50)
    
    # 남성 용신 분석 (丙火)
    male_yongshin = analyze_yongshin_bing(male_saju.month_branch)
    print("\n■ 남성 (丙火) 용신")
    print(f"계절: {male_yongshin['season']}")
    print(f"천간 용신: {', '.join(male_yongshin['cheongan'])}")
    print(f"지지 용신: {', '.join(male_yongshin['jiji'])}")
    
    # 여성 용신 분석 (戊土)
    female_yongshin = analyze_yongshin_mu(female_saju.month_branch)
    print("\n■ 여성 (戊土) 용신")
    print(f"계절: {female_yongshin['season']}")
    print(f"천간 용신: {', '.join(female_yongshin['cheongan'])}")
    print(f"지지 용신: {', '.join(female_yongshin['jiji'])}")
    
    # Step 3: 원국에서 용신 확인
    print("\n【STEP 3: 원국에서 용신 위치 확인】")
    print("-"*50)
    
    print("\n■ 남성 원국의 용신 보유 현황")
    print(f"월간 {male_saju.month_stem}: ", end="")
    if male_saju.month_stem in male_yongshin['cheongan']:
        print(f"✅ 천간 용신 보유 (일의 능력)")
    else:
        print("❌ 용신 아님")
    
    print(f"시간 {male_saju.hour_stem}: ", end="")
    if male_saju.hour_stem in male_yongshin['cheongan']:
        print(f"✅ 천간 용신 보유 (처세술)")
    else:
        print("❌ 용신 아님")
        
    print(f"일지 {male_saju.day_branch}: ", end="")
    if male_saju.day_branch in male_yongshin['jiji']:
        print(f"✅ 지지 용신 보유 (가정/건강)")
    else:
        print("❌ 용신 아님")
        
    print(f"시지 {male_saju.hour_branch}: ", end="")
    if male_saju.hour_branch in male_yongshin['jiji']:
        print(f"✅ 지지 용신 보유 (일의 결과)")
    else:
        print("❌ 용신 아님")
    
    print("\n■ 여성 원국의 용신 보유 현황")
    print(f"월간 {female_saju.month_stem}: ", end="")
    if female_saju.month_stem in female_yongshin['cheongan']:
        print(f"✅ 천간 용신 보유 (일의 능력)")
    else:
        print("❌ 용신 아님")
    
    print(f"시간 {female_saju.hour_stem}: ", end="")
    if female_saju.hour_stem in female_yongshin['cheongan']:
        print(f"✅ 천간 용신 보유 (처세술)")
    else:
        print("❌ 용신 아님")
        
    print(f"일지 {female_saju.day_branch}: ", end="")
    if female_saju.day_branch in female_yongshin['jiji']:
        print(f"✅ 지지 용신 보유 (가정/건강)")
    else:
        print("❌ 용신 아님")
        
    print(f"시지 {female_saju.hour_branch}: ", end="")
    if female_saju.hour_branch in female_yongshin['jiji']:
        print(f"✅ 지지 용신 보유 (일의 결과)")
    else:
        print("❌ 용신 아님")
    
    # Step 4: 상성 분석
    print("\n【STEP 4: 돈사공 기반 상성 분석】")
    print("-"*50)
    
    print("\n■ 일간 관계 분석")
    print(f"남성 丙火 → 여성 戊土: 火生土 관계")
    print("→ 돈사공 해석: 남성이 여성을 따뜻하게 감싸주는 관계")
    print("→ 남성의 열정이 여성의 안정감을 활성화시킴")
    
    print("\n■ 지지 관계 분석")
    print(f"남성 일지 午 vs 여성 일지 戌")
    print("→ 午戌 화국 반합: 매우 좋은 관계 ✅")
    print("→ 가정생활과 건강면에서 서로 보완")
    
    print("\n■ 조후 관점")
    print("남성: 겨울 생 丙火 → 따뜻함이 필요")
    print("여성: 겨울 생 戊土 → 따뜻함이 필요")
    print("→ 둘 다 겨울생으로 비슷한 조후 필요")
    print("→ 서로의 부족한 부분을 이해하기 쉬움")
    
    print("\n■ 종합 평가")
    print("="*50)
    print("1. 화생토(火生土) 관계로 기본 궁합 우수")
    print("2. 일지 午戌 반합으로 가정운 매우 좋음")
    print("3. 같은 계절(겨울)생으로 서로를 이해하기 쉬움")
    print("4. 남성의 용신이 여성을 도와주는 구조")
    print("\n돈사공 시스템 평가: ★★★★☆ (4.5/5)")
    print("매우 우수한 궁합으로 장기적 발전 가능성 높음")

if __name__ == "__main__":
    main()