#!/usr/bin/env python3
"""
돈사공 시스템 정확한 규칙 적용 상성 분석
- 지지 궁합 제외
- 반대 계절이 좋음
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

def get_opposite_season(season):
    """반대 계절 반환"""
    opposites = {
        '봄': '가을',
        '여름': '겨울',
        '가을': '봄',
        '겨울': '여름'
    }
    return opposites.get(season, '알수없음')

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
    print("돈사공 시스템 정확한 규칙 적용 분석")
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
    print(f"월지: {male_saju.month_branch} (亥 = 11월)")
    
    print("\n여성 (1986.12.20 00:00)")
    print(f"사주: {female_saju}")
    print(f"일간: {female_saju.day_stem} (戊土)")
    print(f"월지: {female_saju.month_branch} (子 = 12월)")
    
    # Step 2: 계절 분석
    male_season = get_season_from_month_branch(male_saju.month_branch)
    female_season = get_season_from_month_branch(female_saju.month_branch)
    
    print("\n【STEP 2: 계절 분석】")
    print("-"*50)
    print(f"남성 출생 계절: {male_season} (亥)")
    print(f"여성 출생 계절: {female_season} (子)")
    print(f"\n계절 비교: 둘 다 {male_season}생")
    print("❌ 같은 계절 출생 - 반대 계절이 아니므로 보통")
    print(f"이상적인 조합: {male_season}생 + {get_opposite_season(male_season)}생")
    
    # Step 3: 원국 용신 분석
    print("\n【STEP 3: 원국 용신 분석】")
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
    
    # Step 4: 천간 관계 분석 (지지 궁합 제외!)
    print("\n【STEP 4: 천간 관계 분석】")
    print("-"*50)
    print("※ 돈사공 원칙: 지지끼리는 궁합을 보지 않음!")
    
    print("\n■ 일간 관계")
    print(f"남성 일간: 丙火")
    print(f"여성 일간: 戊土")
    print("→ 火生土 관계: 남성이 여성을 생하는 관계")
    
    print("\n■ 천간 구성 분석")
    print(f"남성 천간: {male_saju.year_stem}, {male_saju.month_stem}, {male_saju.day_stem}, {male_saju.hour_stem}")
    print(f"여성 천간: {female_saju.year_stem}, {female_saju.month_stem}, {female_saju.day_stem}, {female_saju.hour_stem}")
    
    # 천간 매칭 확인
    print("\n■ 상대방이 나의 용신인지 확인")
    
    # 여성의 천간이 남성의 용신인가?
    female_cheongans = [female_saju.year_stem, female_saju.month_stem, 
                        female_saju.day_stem, female_saju.hour_stem]
    male_yongshin_match = [c for c in female_cheongans if c in male_yongshin['cheongan']]
    
    if male_yongshin_match:
        print(f"✅ 여성 천간 중 {', '.join(male_yongshin_match)}가 남성의 용신")
    else:
        print("❌ 여성 천간 중 남성의 용신 없음")
    
    # 남성의 천간이 여성의 용신인가?
    male_cheongans = [male_saju.year_stem, male_saju.month_stem, 
                      male_saju.day_stem, male_saju.hour_stem]
    female_yongshin_match = [c for c in male_cheongans if c in female_yongshin['cheongan']]
    
    if female_yongshin_match:
        print(f"✅ 남성 천간 중 {', '.join(female_yongshin_match)}가 여성의 용신")
    else:
        print("❌ 남성 천간 중 여성의 용신 없음")
    
    # Step 5: 종합 평가
    print("\n【STEP 5: 돈사공 기준 종합 평가】")
    print("="*50)
    
    score = 50  # 기본 점수
    
    # 화생토 관계 (+20)
    print("1. 일간 관계: 火生土 (+20점)")
    score += 20
    
    # 계절 체크 (-10 같은 계절)
    if male_season == female_season:
        print("2. 계절: 같은 계절 출생 (-10점)")
        score -= 10
    else:
        opposite_season = get_opposite_season(male_season)
        if female_season == opposite_season:
            print("2. 계절: 반대 계절 출생 (+20점)")
            score += 20
        else:
            print("2. 계절: 다른 계절 출생 (+5점)")
            score += 5
    
    # 용신 체크
    if male_yongshin_match:
        print(f"3. 여성이 남성의 용신 보유 (+15점)")
        score += 15
    
    if female_yongshin_match:
        print(f"4. 남성이 여성의 용신 보유 (+15점)")
        score += 15
    
    # 여성의 일간이 남성의 용신인지 특별 체크
    if female_saju.day_stem in male_yongshin['cheongan']:
        print(f"5. 여성 일간 {female_saju.day_stem}이 남성의 용신 (+10점)")
        score += 10
    
    # 남성의 일간이 여성의 용신인지 특별 체크
    if male_saju.day_stem in female_yongshin['cheongan']:
        print(f"6. 남성 일간 {male_saju.day_stem}이 여성의 용신 (+10점)")
        score += 10
    
    print(f"\n최종 점수: {score}/100")
    
    if score >= 80:
        grade = "★★★★★ 매우 우수"
    elif score >= 70:
        grade = "★★★★☆ 우수"
    elif score >= 60:
        grade = "★★★☆☆ 양호"
    elif score >= 50:
        grade = "★★☆☆☆ 보통"
    else:
        grade = "★☆☆☆☆ 주의 필요"
    
    print(f"돈사공 시스템 평가: {grade}")
    
    print("\n【핵심 포인트】")
    print("• 火生土 관계로 남성이 여성을 지원하는 구조")
    print("• 같은 겨울생으로 조후(계절 균형)이 유사")
    print("• 남성 일간 丙火가 여성의 천간 용신에 해당")
    print("• 지지 궁합은 돈사공에서 보지 않음")

if __name__ == "__main__":
    main()