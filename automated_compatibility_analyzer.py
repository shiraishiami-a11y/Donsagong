#!/usr/bin/env python3
"""
돈사공 상성 분석 완전 자동화 프로그램
一度の入力で完全自動分析
"""

from datetime import datetime
import sys
import os
import re
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.manseryeok.calculator import ManseryeokCalculator

# 천간 매트릭스 완전 하드코딩
CHEONGAN_MATRIX = {
    '甲': {  # 갑목 일간 → 다른 천간들
        '甲': ('평', '원국 함께 있을 때 흉'),
        '乙': ('흉', '을이 갑을 타고 올라서 뺏긴다'),
        '丙': ('길', '부명이 되게 한다'),
        '丁': ('길흉', '계절에 따라 다름'),
        '戊': ('길', '귀명'),
        '己': ('대흉', '갑기합. 나무를 쓰러뜨린다'),
        '庚': ('대흉', '갑경충. 나무를 쪼갠다'),
        '辛': ('흉', '예의 있어지나 신경질적'),
        '壬': ('흉', '병치례'),
        '癸': ('길흉', '수생목, 목을 강하게')
    },
    '乙': {  # 을목 일간 → 다른 천간들
        '甲': ('길', '동료제감 - 갑목을 타고 오른다'),
        '乙': ('평', '원국 함께 있을 때 흉'),
        '丙': ('대길', '꽃이 태양을 만나 귀해진다'),
        '丁': ('길흉', '계절에 따라 다름'),
        '戊': ('길', '바람을 막아서 부가 된다'),
        '己': ('길', '들판에 꽃이 되기에 좋다'),
        '庚': ('대흉', '을경합. 꽃이 죽는다'),
        '辛': ('흉', '가위로 꽃을 자른다'),
        '壬': ('흉', '물을 줘서 꽃을 키운다'),
        '癸': ('길흉', '이슬을 줘서 더욱 예쁜 꽃')
    },
    '丙': {  # 병화 일간 → 다른 천간들
        '甲': ('길', '합일이 생김 - 나무를 키움'),
        '乙': ('길', '합일이 생김 - 꽃을 키움'),
        '丙': ('평', '원국 함께 있을 때 흉'),
        '丁': ('흉', '불, 여름은 이기고 가을겨울은 당한다'),
        '戊': ('무', '감탄이 있어야 가치가 있다'),
        '己': ('무', '태양으로 乙을 키우니 가치가 적다'),
        '庚': ('흉', '병경합. 태양이 철에 의해 꺼진다'),
        '辛': ('대흉', '병신합. 빛이 의미 없어진다'),
        '壬': ('길', '해결사 역할'),
        '癸': ('길흉', '계절에 따라 다름')
    },
    '丁': {  # 정화 일간 → 다른 천간들
        '甲': ('길', '등불이 나무를 밝힌다'),
        '乙': ('길', '꽃과 등불의 조화'),
        '丙': ('흉', '태양에 등불이 무의미'),
        '丁': ('평', '원국 함께 있을 때 흉'),
        '戊': ('길', '화생토'),
        '己': ('길', '화생토'),
        '庚': ('길', '정화가 금을 단련'),
        '辛': ('길', '보석을 만든다'),
        '壬': ('흉', '물이 불을 끈다'),
        '癸': ('흉', '이슬이 등불을 끈다')
    },
    '戊': {  # 무토 일간 → 다른 천간들
        '甲': ('대길', '산에 나무가 자라 명산이 된다. 부명'),
        '乙': ('소길', '큰 산이 묘목을 만나 아산으로'),
        '丙': ('길', '화생토, 강하게 해준다'),
        '丁': ('길흉', '강하게 해준다. 목과 같이 있으면 안됨'),
        '戊': ('평', '원국 함께 있을 때 흉'),
        '己': ('흉', '산이 땅에 내려왔다. 격이 낮아짐'),
        '庚': ('흉', '토생금 해서 밑이주느라 힘 빠진다'),
        '辛': ('흉', '감목은 약하게, 을목은 깨진다'),
        '壬': ('평', '댐처럼 산이 강을 막아냄'),
        '癸': ('대흉', '무계합. 병화를 없애서 안 좋다')
    },
    '己': {  # 기토 일간 → 다른 천간들
        '甲': ('흉', '갑기합. 욕심부리게 만든다'),
        '乙': ('길', '들판에 꽃을 피울 수 있다'),
        '丙': ('길', '乙이오면 수확물이 생긴다'),
        '丁': ('길', '화생토. 가을겨울에는 필요'),
        '戊': ('흉', '언제든 당할 위험이 있다'),
        '己': ('평', '원국 함께 있을 때 흉'),
        '庚': ('흉', '감목이 우박을 맞는다'),
        '辛': ('흉', '감목이 우박을 맞는다'),
        '壬': ('흉', '물바다 된다'),
        '癸': ('평', '제방, 둑과 같다')
    },
    '庚': {  # 경금 일간 → 다른 천간들
        '甲': ('길', '정화 같이 있으면 매우 길'),
        '乙': ('흉', '을경합. 서로 피곤하다'),
        '丙': ('길', '찬 金의 성향이 따뜻해진다'),
        '丁': ('길', '내가 기물이 되어 용도가 좋아진다'),
        '戊': ('길', '토생금 되어 힘이 강해진다, 약간 우둔'),
        '己': ('길', '토생금 되어 힘이 강해진다'),
        '庚': ('평', '원국 함께 있을 때 흉'),
        '辛': ('흉', '내 것을 나누어 먹으니 좋지 않다'),
        '壬': ('길', '물을 만들어 낸다'),
        '癸': ('길흉', '물을 만들어내나 나도 녹슨다')
    },
    '辛': {  # 신금 일간 → 다른 천간들
        '甲': ('흉', '보석이 나무에 묻힌다'),
        '乙': ('길', '보석이 꽃을 장식'),
        '丙': ('대길', '병신합. 보석이 빛난다'),
        '丁': ('길', '정화가 보석을 단련'),
        '戊': ('흉', '보석이 흙에 묻힌다'),
        '己': ('흉', '보석이 더러워진다'),
        '庚': ('흉', '큰 금이 작은 금을 압도'),
        '辛': ('평', '원국 함께 있을 때 흉'),
        '壬': ('길', '금생수'),
        '癸': ('길', '금생수')
    },
    '壬': {  # 임수 일간 → 다른 천간들
        '甲': ('길', '수생목'),
        '乙': ('길', '수생목'),
        '丙': ('흉', '수극화'),
        '丁': ('흉', '수극화'),
        '戊': ('평', '토극수이지만 댐 역할'),
        '己': ('흉', '토극수'),
        '庚': ('길', '금생수'),
        '辛': ('길', '금생수'),
        '壬': ('평', '원국 함께 있을 때 흉'),
        '癸': ('흉', '큰 물이 작은 물을 흡수')
    },
    '癸': {  # 계수 일간 → 다른 천간들
        '甲': ('길', '수생목'),
        '乙': ('길', '수생목'),
        '丙': ('길흉', '계절에 따라 다름'),
        '丁': ('흉', '이슬이 등불을 끈다'),
        '戊': ('대흉', '무계합'),
        '己': ('평', '기토가 계수를 막음'),
        '庚': ('길', '금생수'),
        '辛': ('길', '금생수'),
        '壬': ('흉', '작은 물이 큰 물에 흡수'),
        '癸': ('평', '원국 함께 있을 때 흉')
    }
}

def parse_input(input_str):
    """입력 파싱 및 검증"""
    # 정규식으로 입력 파싱
    pattern = r'남성\s*(\d{4})/(\d{1,2})/(\d{1,2})/(\d{1,2})시.*여성\s*(\d{4})/(\d{1,2})/(\d{1,2})/(\d{1,2})시'
    match = re.search(pattern, input_str)
    
    if not match:
        raise ValueError("입력 형식이 잘못되었습니다. 예: 남성 1986/5/26/5시, 여성 1986/12/20/0시")
    
    male_year, male_month, male_day, male_hour = map(int, match.groups()[:4])
    female_year, female_month, female_day, female_hour = map(int, match.groups()[4:])
    
    # 날짜 유효성 검증
    try:
        male_birth = datetime(male_year, male_month, male_day, male_hour)
        female_birth = datetime(female_year, female_month, female_day, female_hour)
    except ValueError as e:
        raise ValueError(f"유효하지 않은 날짜입니다: {e}")
    
    return male_birth, female_birth

def get_season_from_branch(branch):
    """지지로 계절 판단"""
    seasons = {
        '寅': '봄', '卯': '봄', '辰': '봄',
        '巳': '여름', '午': '여름', '未': '여름', 
        '申': '가을', '酉': '가을', '戌': '가을',
        '亥': '겨울', '子': '겨울', '丑': '겨울'
    }
    return seasons.get(branch, '미상')

def analyze_cheongan_relation(day_stem1, target_stem):
    """천간 관계 분석"""
    if day_stem1 in CHEONGAN_MATRIX and target_stem in CHEONGAN_MATRIX[day_stem1]:
        return CHEONGAN_MATRIX[day_stem1][target_stem]
    return ('평', '일반 관계')

def calculate_daeun_direction(year_stem, gender):
    """대운 순역행 판단"""
    stems = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
    year_index = stems.index(year_stem)
    is_yang = (year_index % 2 == 0)
    
    if (is_yang and gender == 'male') or (not is_yang and gender == 'female'):
        return '순행'
    return '역행'

def check_donsagong_principles(male_saju, female_saju):
    """돈사공 원칙 위반 체크"""
    violations = []
    
    # 지지 궁합 금지 체크는 생략 (자동으로 안 보므로)
    # 년간 사용 금지도 자동으로 안 보므로 패스
    
    return violations

def calculate_score(male_saju, female_saju):
    """점수 계산"""
    score_male = 50  # 남성 기본 점수
    score_female = 50  # 여성 기본 점수
    
    # 일간 관계 (가장 중요 - 30점)
    male_to_female = analyze_cheongan_relation(male_saju.day_stem, female_saju.day_stem)
    female_to_male = analyze_cheongan_relation(female_saju.day_stem, male_saju.day_stem)
    
    if '길' in male_to_female[0]:
        score_male += 30
    elif '흉' in male_to_female[0]:
        score_male -= 20
    
    if '길' in female_to_male[0]:
        score_female += 30
    elif '흉' in female_to_male[0]:
        score_female -= 20
    
    # 월간 관계 (15점)
    male_month_to_female = analyze_cheongan_relation(male_saju.month_stem, female_saju.month_stem)
    female_month_to_male = analyze_cheongan_relation(female_saju.month_stem, male_saju.month_stem)
    
    if '길' in male_month_to_female[0]:
        score_male += 15
    elif '흉' in male_month_to_female[0]:
        score_male -= 10
        
    if '길' in female_month_to_male[0]:
        score_female += 15
    elif '흉' in female_month_to_male[0]:
        score_female -= 10
    
    # 계절 상성 (15점)
    male_season = get_season_from_branch(male_saju.month_branch)
    female_season = get_season_from_branch(female_saju.month_branch)
    
    opposite_seasons = {'봄': '가을', '여름': '겨울', '가을': '봄', '겨울': '여름'}
    if male_season == opposite_seasons.get(female_season):
        score_male += 15
        score_female += 15
    elif male_season == female_season:
        score_male -= 5
        score_female -= 5
    
    # 대운 방향 (10점)
    male_direction = calculate_daeun_direction(male_saju.year_stem, 'male')
    female_direction = calculate_daeun_direction(female_saju.year_stem, 'female')
    
    if male_direction == female_direction:
        score_male += 10
        score_female += 10
    
    return score_male, score_female

def main():
    print("="*60)
    print("돈사공 상성 분석 자동화 프로그램")
    print("="*60)
    
    # 입력 받기
    print("\n생년월일시를 입력해주세요:")
    print("형식: 남성 YYYY/MM/DD/HH시, 여성 YYYY/MM/DD/HH시")
    print("예시: 남성 1986/5/26/5시, 여성 1986/12/20/0시")
    
    input_str = input("\n입력: ")
    
    try:
        # 1. 입력 파싱 및 검증
        male_birth, female_birth = parse_input(input_str)
        
        # 2. 만세력 계산
        calculator = ManseryeokCalculator()
        male_saju = calculator.calculate_saju(male_birth, 'male')
        female_saju = calculator.calculate_saju(female_birth, 'female')
        
        print(f"\n【사주 원국】")
        print(f"남성: {male_saju}")
        print(f"여성: {female_saju}")
        
        # 3. 돈사공 원칙 체크
        violations = check_donsagong_principles(male_saju, female_saju)
        if violations:
            print(f"\n⚠️ 돈사공 원칙 위반: {', '.join(violations)}")
        
        # 4. 천간 관계 분석
        print(f"\n【천간 관계 분석】")
        
        # 월간 관계
        male_month_rel = analyze_cheongan_relation(male_saju.month_stem, female_saju.month_stem)
        female_month_rel = analyze_cheongan_relation(female_saju.month_stem, male_saju.month_stem)
        print(f"월간: 남성→여성 {male_month_rel[0]}, 여성→남성 {female_month_rel[0]}")
        
        # 일간 관계 (최중요)
        male_day_rel = analyze_cheongan_relation(male_saju.day_stem, female_saju.day_stem)
        female_day_rel = analyze_cheongan_relation(female_saju.day_stem, male_saju.day_stem)
        print(f"일간: 남성→여성 {male_day_rel[0]}, 여성→남성 {female_day_rel[0]} ★")
        
        # 시간 관계
        male_hour_rel = analyze_cheongan_relation(male_saju.hour_stem, female_saju.hour_stem)
        female_hour_rel = analyze_cheongan_relation(female_saju.hour_stem, male_saju.hour_stem)
        print(f"시간: 남성→여성 {male_hour_rel[0]}, 여성→남성 {female_hour_rel[0]}")
        
        # 5. 계절 분석
        male_season = get_season_from_branch(male_saju.month_branch)
        female_season = get_season_from_branch(female_saju.month_branch)
        print(f"\n【계절 상성】")
        print(f"남성: {male_season}, 여성: {female_season}")
        
        opposite_seasons = {'봄': '가을', '여름': '겨울', '가을': '봄', '겨울': '여름'}
        if male_season == opposite_seasons.get(female_season):
            print("✅ 반대 계절 - 이상적")
        elif male_season == female_season:
            print("❌ 같은 계절 - 보통")
        else:
            print("◆ 다른 계절 - 무난")
        
        # 6. 대운 방향
        male_direction = calculate_daeun_direction(male_saju.year_stem, 'male')
        female_direction = calculate_daeun_direction(female_saju.year_stem, 'female')
        print(f"\n【대운 방향】")
        print(f"남성: {male_direction}, 여성: {female_direction}")
        if male_direction == female_direction:
            print("✅ 같은 방향 - 인생 흐름 동조")
        else:
            print("⚠️ 다른 방향 - 인생 흐름 상이")
        
        # 7. 점수 계산 및 최종 평가
        score_male, score_female = calculate_score(male_saju, female_saju)
        
        print(f"\n【최종 평가】")
        print(f"남성 관점 점수: {score_male}/100")
        print(f"여성 관점 점수: {score_female}/100")
        
        def get_grade(score):
            if score >= 80: return "★★★★★"
            elif score >= 70: return "★★★★☆"
            elif score >= 60: return "★★★☆☆"
            elif score >= 50: return "★★☆☆☆"
            else: return "★☆☆☆☆"
        
        print(f"남성에게는: {get_grade(score_male)} 관계")
        print(f"여성에게는: {get_grade(score_female)} 관계")
        
        # 8. 득점/실점 요약
        print(f"\n【관계 특징】")
        if score_male > score_female:
            print("남성에게 더 유리한 관계")
        elif score_female > score_male:
            print("여성에게 더 유리한 관계")
        else:
            print("서로 균형잡힌 관계")
        
        print(f"\n남성 득점: 일간관계 {male_day_rel[0]}")
        print(f"여성 득점: 일간관계 {female_day_rel[0]}")
        
    except Exception as e:
        print(f"❌ 오류: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())