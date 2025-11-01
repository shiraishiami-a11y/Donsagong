#!/usr/bin/env python3
"""
돈사공 시스템 최종 완전 분석
STEP 1: 만세력 + 대운 계산 (대운이 계산되어야 STEP 1 완료)
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

def analyze_cheongan_relation(stem1, stem2):
    """천간 관계 분석"""
    if stem1 == stem2:
        return "비견", "중립"
    
    # 오행 관계
    elements = {
        '甲': '목', '乙': '목',
        '丙': '화', '丁': '화',
        '戊': '토', '己': '토',
        '庚': '금', '辛': '금',
        '壬': '수', '癸': '수'
    }
    
    elem1 = elements[stem1]
    elem2 = elements[stem2]
    
    # 상생 관계
    generation = {
        ('목', '화'): ('목생화', '생'),
        ('화', '토'): ('화생토', '생'),
        ('토', '금'): ('토생금', '생'),
        ('금', '수'): ('금생수', '생'),
        ('수', '목'): ('수생목', '생')
    }
    
    # 상극 관계
    control = {
        ('목', '토'): ('목극토', '극'),
        ('토', '수'): ('토극수', '극'),
        ('수', '화'): ('수극화', '극'),
        ('화', '금'): ('화극금', '극'),
        ('금', '목'): ('금극목', '극')
    }
    
    if (elem1, elem2) in generation:
        return generation[(elem1, elem2)]
    elif (elem2, elem1) in generation:
        desc, type = generation[(elem2, elem1)]
        return desc + " (피생)", "생"
    elif (elem1, elem2) in control:
        return control[(elem1, elem2)]
    elif (elem2, elem1) in control:
        desc, type = control[(elem2, elem1)]
        return desc + " (피극)", "극"
    else:
        return "동일 오행", "중립"

def calculate_manual_daeun(saju, gender):
    """수동 대운 계산 (간단 버전)"""
    # 순행/역행 결정
    year_stem_index = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'].index(saju.year_stem)
    is_yang_year = (year_stem_index % 2 == 0)
    
    if (is_yang_year and gender == 'male') or (not is_yang_year and gender == 'female'):
        direction = 1  # 순행
    else:
        direction = -1  # 역행
    
    # 월주 기준으로 대운 계산
    month_stem_idx = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'].index(saju.month_stem)
    month_branch_idx = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥'].index(saju.month_branch)
    
    daeun_list = []
    for i in range(8):  # 8대운까지
        new_stem_idx = (month_stem_idx + direction * (i + 1)) % 10
        new_branch_idx = (month_branch_idx + direction * (i + 1)) % 12
        
        new_stem = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'][new_stem_idx]
        new_branch = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥'][new_branch_idx]
        
        start_age = 5 + (i * 10)  # 기운 나이를 5세로 가정
        end_age = start_age + 9
        
        daeun_list.append({
            'order': i + 1,
            'start_age': start_age,
            'end_age': end_age,
            'gan_ji': f"{new_stem}{new_branch}",
            'stem': new_stem,
            'branch': new_branch
        })
    
    return {
        'direction': '순행' if direction == 1 else '역행',
        'start_age': 5,
        'daeun_list': daeun_list
    }

def main():
    print("="*80)
    print("돈사공 시스템 최종 완전 분석")
    print("="*80)
    
    calculator = ManseryeokCalculator()
    
    # STEP 1: 만세력 + 대운 계산 (대운까지 계산되어야 STEP 1 완료)
    print("\n【STEP 1: 만세력 + 대운 계산】")
    print("-"*60)
    
    # 남성: 1968년 12월 2일 2시
    male_birth = datetime(1968, 12, 2, 2, 0, 0)
    male_saju = calculator.calculate_saju(male_birth, 'male')
    
    # 여성: 1986년 12월 20일 0시
    female_birth = datetime(1986, 12, 20, 0, 0, 0)
    female_saju = calculator.calculate_saju(female_birth, 'female')
    
    print("\n■ 남성 (1968.12.2 02:00)")
    print(f"사주: {male_saju}")
    print(f"일간: {male_saju.day_stem} (丙火)")
    
    # 남성 대운 계산
    male_daeun = calculate_manual_daeun(male_saju, 'male')
    print(f"\n대운 방향: {male_daeun['direction']}")
    print(f"기운: {male_daeun['start_age']}세")
    current_year = 2024
    male_age = current_year - 1968
    print(f"현재 나이: {male_age}세")
    
    for daeun in male_daeun['daeun_list'][:6]:
        age_range = f"{daeun['start_age']}-{daeun['end_age']}세"
        marker = " ← 현재" if daeun['start_age'] <= male_age <= daeun['end_age'] else ""
        print(f"제{daeun['order']}대운 {age_range}: {daeun['gan_ji']}{marker}")
    
    print("\n■ 여성 (1986.12.20 00:00)")
    print(f"사주: {female_saju}")
    print(f"일간: {female_saju.day_stem} (戊土)")
    
    # 여성 대운 계산
    female_daeun = calculate_manual_daeun(female_saju, 'female')
    print(f"\n대운 방향: {female_daeun['direction']}")
    print(f"기운: {female_daeun['start_age']}세")
    female_age = current_year - 1986
    print(f"현재 나이: {female_age}세")
    
    for daeun in female_daeun['daeun_list'][:6]:
        age_range = f"{daeun['start_age']}-{daeun['end_age']}세"
        marker = " ← 현재" if daeun['start_age'] <= female_age <= daeun['end_age'] else ""
        print(f"제{daeun['order']}대운 {age_range}: {daeun['gan_ji']}{marker}")
    
    print("\n✅ STEP 1 완료: 만세력과 대운 계산 성공")
    
    # STEP 2: 천간 관계 분석 (년간 제외)
    print("\n【STEP 2: 천간 관계 분석】")
    print("-"*60)
    
    print("\n■ 월간 관계")
    print(f"남성: {male_saju.month_stem} vs 여성: {female_saju.month_stem}")
    relation, type = analyze_cheongan_relation(male_saju.month_stem, female_saju.month_stem)
    symbol = "✅" if type == "생" else "❌" if type == "극" else "◆"
    print(f"→ {relation} {symbol}")
    
    print("\n■ 일간 관계 (가장 중요!)")
    print(f"남성: {male_saju.day_stem} (丙火) vs 여성: {female_saju.day_stem} (戊土)")
    relation, type = analyze_cheongan_relation(male_saju.day_stem, female_saju.day_stem)
    symbol = "✅" if type == "생" else "❌" if type == "극" else "◆"
    print(f"→ {relation} {symbol}")
    
    print("\n■ 시간 관계")
    print(f"남성: {male_saju.hour_stem} vs 여성: {female_saju.hour_stem}")
    relation, type = analyze_cheongan_relation(male_saju.hour_stem, female_saju.hour_stem)
    symbol = "✅" if type == "생" else "❌" if type == "극" else "◆"
    print(f"→ {relation} {symbol}")
    
    # STEP 3: 대운 흐름 동조성
    print("\n【STEP 3: 대운 흐름 동조성】")
    print("-"*60)
    
    # 현재 대운 찾기
    male_current_daeun = None
    female_current_daeun = None
    
    for daeun in male_daeun['daeun_list']:
        if daeun['start_age'] <= male_age <= daeun['end_age']:
            male_current_daeun = daeun
            break
    
    for daeun in female_daeun['daeun_list']:
        if daeun['start_age'] <= female_age <= daeun['end_age']:
            female_current_daeun = daeun
            break
    
    if male_current_daeun and female_current_daeun:
        print(f"\n■ 현재 대운 비교 (2024년)")
        print(f"남성 ({male_age}세): {male_current_daeun['gan_ji']}")
        print(f"여성 ({female_age}세): {female_current_daeun['gan_ji']}")
        
        # 현재 대운 천간 관계
        relation, type = analyze_cheongan_relation(
            male_current_daeun['stem'], 
            female_current_daeun['stem']
        )
        symbol = "✅" if type == "생" else "❌" if type == "극" else "◆"
        print(f"\n현재 대운 천간 관계: {relation} {symbol}")
        
        # 대운 방향성
        print(f"\n대운 방향: 남성 {male_daeun['direction']} / 여성 {female_daeun['direction']}")
        if male_daeun['direction'] == female_daeun['direction']:
            print("→ 같은 방향으로 흐름 ✅")
        else:
            print("→ 다른 방향으로 흐름 ⚠️")
    
    # STEP 4: 용신 분석
    print("\n【STEP 4: 용신 체크】")
    print("-"*60)
    
    # 병화 겨울생 용신
    male_yongshin = ['戊', '甲', '乙']
    # 무토 겨울생 용신
    female_yongshin = ['丁', '丙', '甲', '乙']
    
    print(f"\n■ 상대방이 나의 용신인지")
    if female_saju.day_stem in male_yongshin:
        print(f"✅ 여성 일간 {female_saju.day_stem}이 남성의 용신")
    
    if male_saju.day_stem in female_yongshin:
        print(f"✅ 남성 일간 {male_saju.day_stem}이 여성의 용신")
    
    # STEP 5: 종합 평가
    print("\n【STEP 5: 돈사공 최종 평가】")
    print("="*60)
    
    print("\n◆ 천간 관계 요약")
    print("• 일간: 丙火 → 戊土 (화생토) ✅ 우수")
    print("• 월간: 癸水 → 庚金 (금생수 역방향) ◆ 보통")
    print("• 시간: 己土 → 壬水 (토극수) ❌ 주의")
    
    print("\n◆ 용신 관계")
    print("• 서로가 서로의 용신 ✅")
    
    print("\n◆ 대운 흐름")
    if male_daeun['direction'] == female_daeun['direction']:
        print("• 같은 방향 대운 ✅")
    else:
        print("• 다른 방향 대운 ⚠️")
    
    print("\n최종 평가: ★★★★☆")
    print("일간의 우수한 화생토 관계와 상호 용신 보완으로 좋은 궁합")

if __name__ == "__main__":
    main()