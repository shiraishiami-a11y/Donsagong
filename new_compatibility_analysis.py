#!/usr/bin/env python3
"""
新しい相性分析: 1986年12月20日0時女性 vs 1986年5月26日5時男性
돈사공 천간 매트릭스 적용
"""

from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.manseryeok.calculator import ManseryeokCalculator

def get_season_from_month_branch(month_branch):
    """月支から季節判断"""
    seasons = {
        '寅': '春', '卯': '春', '辰': '春',
        '巳': '夏', '午': '夏', '未': '夏',
        '申': '秋', '酉': '秋', '戌': '秋',
        '亥': '冬', '子': '冬', '丑': '冬'
    }
    return seasons.get(month_branch, '不明')

def analyze_mu_to_other(target_stem):
    """戊土日干が他の天干に出会う時（돈사공 매트릭스）"""
    matrix = {
        '甲': ('大吉', '山に木が育ち名山になる。富命'),
        '乙': ('小吉', '大きな山が苗木に出会い小山になった'),
        '丙': ('吉', '火生土、強くしてくれる'),
        '丁': ('吉凶', '強くしてくれる。木と一緒にあると木が燃える'),
        '戊': ('平', '原局で一緒にある時は凶、大運で来る時は影響次第'),
        '己': ('凶', '山が平地に降りた。格が下がる'),
        '庚': ('凶', '土生金で力が抜ける。甲木を壊す'),
        '辛': ('凶', '甲木は弱く、乙木は壊れる'),
        '壬': ('平', 'ダムのように山が川を堰き止める。平衡状態'),
        '癸': ('大凶', '戊癸合。丙火を消して良くない')
    }
    return matrix.get(target_stem, ('平', ''))

def analyze_gyeong_to_other(target_stem):
    """庚金日干が他の天干に出会う時（돈사공 매트릭스）"""
    matrix = {
        '甲': ('大吉', '庚甲は最고의 관계. 도끼가 나무를 유용하게'),
        '乙': ('吉', '가위가 꽃을 아름답게 다듬음'),
        '丙': ('凶', '병경합. 쇠가 녹는다'),
        '丁': ('吉', '정화가 금을 단련시켜 보석으로'),
        '戊': ('凶', '토생금이지만 金이 더러워짐'),
        '己': ('凶', '같은 이유로 金이 더러워짐'),
        '庚': ('平', '같은 金끼리 경쟁'),
        '辛': ('凶', '辛이 庚을 녹슬게 함'),
        '壬': ('吉', '금생수. 깨끗한 물을 만듦'),
        '癸': ('吉', '금생수. 이슬을 만듦')
    }
    return matrix.get(target_stem, ('平', ''))

def analyze_daeun_direction(year_stem, gender):
    """대운 순역행 결정"""
    year_stem_index = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'].index(year_stem)
    is_yang_year = (year_stem_index % 2 == 0)
    
    if (is_yang_year and gender == 'male') or (not is_yang_year and gender == 'female'):
        return '順行'
    else:
        return '逆行'

def calculate_simple_daeun(saju, gender):
    """簡単な大運計算"""
    direction = analyze_daeun_direction(saju.year_stem, gender)
    
    month_stem_idx = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'].index(saju.month_stem)
    month_branch_idx = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥'].index(saju.month_branch)
    
    direction_num = 1 if direction == '順行' else -1
    
    daeun_list = []
    for i in range(8):
        new_stem_idx = (month_stem_idx + direction_num * (i + 1)) % 10
        new_branch_idx = (month_branch_idx + direction_num * (i + 1)) % 12
        
        new_stem = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'][new_stem_idx]
        new_branch = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥'][new_branch_idx]
        
        start_age = 6 + (i * 10)
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
        'direction': direction,
        'start_age': 6,
        'daeun_list': daeun_list
    }

def main():
    print("="*80)
    print("相性分析: 1986年12月20日0時女性 vs 1986年5月26日5時男性")
    print("="*80)
    
    calculator = ManseryeokCalculator()
    
    # Step 1: 万歳暦計算
    print("\n【STEP 1: 万歳暦 + 大運計算】")
    print("-"*60)
    
    # 女性: 1986年12月20日 0時
    female_birth = datetime(1986, 12, 20, 0, 0, 0)
    female_saju = calculator.calculate_saju(female_birth, 'female')
    
    # 男性: 1986年5月26日 5時
    male_birth = datetime(1986, 5, 26, 5, 0, 0)
    male_saju = calculator.calculate_saju(male_birth, 'male')
    
    print("\n■ 女性 (1986.12.20 00:00)")
    print(f"四柱: {female_saju}")
    print(f"日干: {female_saju.day_stem} (戊土)")
    print(f"月支: {female_saju.month_branch} (子 = 12月 = 冬)")
    
    # 女性大運計算
    female_daeun = calculate_simple_daeun(female_saju, 'female')
    print(f"\n大運方向: {female_daeun['direction']}")
    female_age = 2024 - 1986
    print(f"現在年齢: {female_age}歳")
    
    for daeun in female_daeun['daeun_list'][:5]:
        age_range = f"{daeun['start_age']}-{daeun['end_age']}歳"
        marker = " ← 現在" if daeun['start_age'] <= female_age <= daeun['end_age'] else ""
        print(f"第{daeun['order']}大運 {age_range}: {daeun['gan_ji']}{marker}")
    
    print("\n■ 男性 (1986.5.26 05:00)")
    print(f"四柱: {male_saju}")
    print(f"日干: {male_saju.day_stem} (庚金)")
    print(f"月支: {male_saju.month_branch} (巳 = 5月 = 夏)")
    
    # 男性大運計算
    male_daeun = calculate_simple_daeun(male_saju, 'male')
    print(f"\n大運方向: {male_daeun['direction']}")
    male_age = 2024 - 1986
    print(f"現在年齢: {male_age}歳")
    
    for daeun in male_daeun['daeun_list'][:5]:
        age_range = f"{daeun['start_age']}-{daeun['end_age']}歳"
        marker = " ← 現在" if daeun['start_age'] <= male_age <= daeun['end_age'] else ""
        print(f"第{daeun['order']}大運 {age_range}: {daeun['gan_ji']}{marker}")
    
    print("\n✅ STEP 1 完了")
    
    # Step 2: 천간 관계 분석
    print("\n【STEP 2: 天干関係分析（年干除く）】")
    print("-"*60)
    
    print("\n■ 月干関係")
    print(f"女性 {female_saju.month_stem} vs 男性 {female_saju.month_stem}")
    if female_saju.month_stem == male_saju.month_stem:
        print("→ 同じ天干 (競争関係)")
    
    print("\n■ 日干関係 ★★★（最重要）")
    print(f"女性 戊土 → 男性 {male_saju.day_stem}")
    result, desc = analyze_mu_to_other(male_saju.day_stem)
    symbol = "✅" if "吉" in result else "❌" if "凶" in result else "◆"
    print(f"女性から見て: {result} {symbol} - {desc}")
    
    print(f"男性 {male_saju.day_stem} → 女性 戊土")
    result, desc = analyze_gyeong_to_other(female_saju.day_stem)
    symbol = "✅" if "吉" in result else "❌" if "凶" in result else "◆"
    print(f"男性から見て: {result} {symbol} - {desc}")
    
    print("\n■ 時干関係")
    print(f"女性 {female_saju.hour_stem} vs 男性 {male_saju.hour_stem}")
    if female_saju.hour_stem == male_saju.hour_stem:
        print("→ 同じ天干 (競争関係)")
    else:
        print(f"→ 異なる天干関係")
    
    # Step 3: 계절 분석
    print("\n【STEP 3: 季節分析】")
    print("-"*60)
    
    female_season = get_season_from_month_branch(female_saju.month_branch)
    male_season = get_season_from_month_branch(male_saju.month_branch)
    
    print(f"女性: {female_season}生まれ (子月)")
    print(f"男性: {male_season}生まれ (巳月)")
    
    opposite_seasons = {'春': '秋', '夏': '冬', '秋': '春', '冬': '夏'}
    if male_season == opposite_seasons.get(female_season):
        print("✅ 反対季節 - 理想的な組み合わせ")
    elif female_season == male_season:
        print("❌ 同じ季節 - 普通")
    else:
        print("◆ 異なる季節 - まあまあ")
    
    # Step 4: 대운 흐름
    print("\n【STEP 4: 大運の流れ】")
    print("-"*60)
    
    print(f"女性: {female_daeun['direction']}")
    print(f"男性: {male_daeun['direction']}")
    
    if female_daeun['direction'] == male_daeun['direction']:
        print("✅ 同じ方向 - 人生の流れが合う")
    else:
        print("⚠️ 異なる方向 - 人生の流れが異なる")
    
    # Step 5: 종합 평가
    print("\n【STEP 5: 総合評価】")
    print("="*60)
    
    print("\n■ 女性（戊土）から見た男性（庚金）")
    result, desc = analyze_mu_to_other(male_saju.day_stem)
    print(f"日干関係: {result} - {desc}")
    
    print(f"\n■ 季節の相性")
    if male_season == opposite_seasons.get(female_season):
        print("冬生まれ女性 + 夏生まれ男性 = 理想的")
    
    print(f"\n■ 大運の同調性")
    if female_daeun['direction'] == male_daeun['direction']:
        print("同じ流れで進む")
    
    print("\n【最終評価】")
    
    # 점수 계산
    score = 50  # 基本点
    
    if "吉" in analyze_mu_to_other(male_saju.day_stem)[0]:
        score += 25
        print("• 女性から男性への日干関係: 良好 (+25点)")
    
    if male_season == opposite_seasons.get(female_season):
        score += 20
        print("• 反対季節の相性: 理想的 (+20点)")
    
    if female_daeun['direction'] == male_daeun['direction']:
        score += 15
        print("• 大運の方向: 同調 (+15点)")
    
    print(f"\n最終スコア: {score}/100")
    
    if score >= 80:
        grade = "★★★★★ 非常に良い"
    elif score >= 70:
        grade = "★★★★☆ 良い"
    elif score >= 60:
        grade = "★★★☆☆ まあまあ"
    else:
        grade = "★★☆☆☆ 普通"
    
    print(f"돈사공 評価: {grade}")
    
    print("\n【女性から見た相性のポイント】")
    print("• 戊土にとって庚金は凶 - 土生金で力が抜ける")
    print("• しかし冬生まれ + 夏生まれの季節相性は理想的")
    print("• 大運の流れが同じで人生の方向性が合う")

if __name__ == "__main__":
    main()