#!/usr/bin/env python3
"""
돈사공 相性分析 完全自動化プログラム（日本語版）
一度の入力で完全自動分析
"""

from datetime import datetime
import sys
import os
import re
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.manseryeok.calculator import ManseryeokCalculator

# 天干マトリックス完全ハードコーディング
CHEONGAN_MATRIX = {
    '甲': {  # 甲木日干 → 他の天干
        '甲': ('平', '原局で一緒にある時は凶'),
        '乙': ('凶', '乙が甲を乗っ取る'),
        '丙': ('吉', '副名になる'),
        '丁': ('吉凶', '季節による'),
        '戊': ('吉', '貴名'),
        '己': ('大凶', '甲己合。木を倒す'),
        '庚': ('大凶', '甲庚冲。木を割る'),
        '辛': ('凶', '礼儀正しくなるが神経質に'),
        '壬': ('凶', '病置例'),
        '癸': ('吉凶', '水生木、木を強くする')
    },
    '乙': {  # 乙木日干 → 他の天干
        '甲': ('吉', '同僚制感 - 甲木に乗って上昇'),
        '乙': ('平', '原局で一緒にある時は凶'),
        '丙': ('大吉', '花が太陽に会って貴くなる'),
        '丁': ('吉凶', '季節による'),
        '戊': ('吉', '風を防いで富になる'),
        '己': ('吉', '野原に花が咲く'),
        '庚': ('大凶', '乙庚合。花が死ぬ'),
        '辛': ('凶', 'ハサミで花を切る'),
        '壬': ('凶', '水をやって花を育てる'),
        '癸': ('吉凶', '露を与えてより美しい花に')
    },
    '丙': {  # 丙火日干 → 他の天干
        '甲': ('吉', '合一が生じる - 木を育てる'),
        '乙': ('吉', '合一が生じる - 花を育てる'),
        '丙': ('平', '原局で一緒にある時は凶'),
        '丁': ('凶', '火、夏は勝ち秋冬は負ける'),
        '戊': ('無', '感嘆があって価値がある'),
        '己': ('無', '太陽で乙を育てるので価値が少ない'),
        '庚': ('凶', '丙庚合。太陽が鉄で消える'),
        '辛': ('大凶', '丙辛合。光が無意味になる'),
        '壬': ('吉', '解決者の役割'),
        '癸': ('吉凶', '季節による')
    },
    '丁': {  # 丁火日干 → 他の天干
        '甲': ('吉', 'ランプが木を照らす'),
        '乙': ('吉', '花とランプの調和'),
        '丙': ('凶', '太陽にランプは無意味'),
        '丁': ('平', '原局で一緒にある時は凶'),
        '戊': ('吉', '火生土'),
        '己': ('吉', '火生土'),
        '庚': ('吉', '丁火が金を鍛錬'),
        '辛': ('吉', '宝石を作る'),
        '壬': ('凶', '水が火を消す'),
        '癸': ('凶', '露がランプを消す')
    },
    '戊': {  # 戊土日干 → 他の天干
        '甲': ('大吉', '山に木が育ち名山になる。富名'),
        '乙': ('小吉', '大きな山が苗木に会い小山に'),
        '丙': ('吉', '火生土、強くしてくれる'),
        '丁': ('吉凶', '強くする。木と一緒にいると駄目'),
        '戊': ('平', '原局で一緒にある時は凶'),
        '己': ('凶', '山が地に降りた。格が下がる'),
        '庚': ('凶', '土生金で力が抜ける'),
        '辛': ('凶', '甲木は弱く、乙木は壊れる'),
        '壬': ('平', 'ダムのように山が川を止める'),
        '癸': ('大凶', '戊癸合。丙火を消して良くない')
    },
    '己': {  # 己土日干 → 他の天干
        '甲': ('凶', '甲己合。欲張りになる'),
        '乙': ('吉', '野原に花を咲かせる'),
        '丙': ('吉', '乙が来れば収穫物が生じる'),
        '丁': ('吉', '火生土。秋冬には必要'),
        '戊': ('凶', 'いつでも奪われる危険'),
        '己': ('平', '原局で一緒にある時は凶'),
        '庚': ('凶', '甲木が雹に打たれる'),
        '辛': ('凶', '甲木が雹に打たれる'),
        '壬': ('凶', '水浸しになる'),
        '癸': ('平', '堤防、堤のようだ')
    },
    '庚': {  # 庚金日干 → 他の天干
        '甲': ('吉', '丁火と一緒なら大吉'),
        '乙': ('凶', '乙庚合。お互い疲れる'),
        '丙': ('吉', '冷たい金の性向が温かくなる'),
        '丁': ('吉', '道具になって用途が良くなる'),
        '戊': ('吉', '土生金で力が強くなる、やや鈍感'),
        '己': ('吉', '土生金で力が強くなる'),
        '庚': ('平', '原局で一緒にある時は凶'),
        '辛': ('凶', '私のものを分けて食べるので良くない'),
        '壬': ('吉', '水を作り出す'),
        '癸': ('吉凶', '水を作るが錆びる')
    },
    '辛': {  # 辛金日干 → 他の天干
        '甲': ('凶', '宝石が木に埋もれる'),
        '乙': ('吉', '宝石が花を飾る'),
        '丙': ('大吉', '丙辛合。宝石が輝く'),
        '丁': ('吉', '丁火が宝石を鍛錬'),
        '戊': ('凶', '宝石が土に埋もれる'),
        '己': ('凶', '宝石が汚れる'),
        '庚': ('凶', '大きな金が小さな金を圧倒'),
        '辛': ('平', '原局で一緒にある時は凶'),
        '壬': ('吉', '金生水'),
        '癸': ('吉', '金生水')
    },
    '壬': {  # 壬水日干 → 他の天干
        '甲': ('吉', '水生木'),
        '乙': ('吉', '水生木'),
        '丙': ('凶', '水克火'),
        '丁': ('凶', '水克火'),
        '戊': ('平', '土克水だがダムの役割'),
        '己': ('凶', '土克水'),
        '庚': ('吉', '金生水'),
        '辛': ('吉', '金生水'),
        '壬': ('平', '原局で一緒にある時は凶'),
        '癸': ('凶', '大きな水が小さな水を吸収')
    },
    '癸': {  # 癸水日干 → 他の天干
        '甲': ('吉', '水生木'),
        '乙': ('吉', '水生木'),
        '丙': ('吉凶', '季節による'),
        '丁': ('凶', '露がランプを消す'),
        '戊': ('大凶', '戊癸合'),
        '己': ('平', '己土が癸水を止める'),
        '庚': ('吉', '金生水'),
        '辛': ('吉', '金生水'),
        '壬': ('凶', '小さな水が大きな水に吸収'),
        '癸': ('平', '原局で一緒にある時は凶')
    }
}

def parse_input(input_str):
    """入力解析と検証"""
    # 正規表現で入力解析
    pattern = r'男性\s*(\d{4})/(\d{1,2})/(\d{1,2})/(\d{1,2})時.*女性\s*(\d{4})/(\d{1,2})/(\d{1,2})/(\d{1,2})時'
    match = re.search(pattern, input_str)
    
    if not match:
        raise ValueError("入力形式が間違っています。例: 男性 1986/5/26/5時, 女性 1986/12/20/0時")
    
    male_year, male_month, male_day, male_hour = map(int, match.groups()[:4])
    female_year, female_month, female_day, female_hour = map(int, match.groups()[4:])
    
    # 日付の有効性検証
    try:
        male_birth = datetime(male_year, male_month, male_day, male_hour)
        female_birth = datetime(female_year, female_month, female_day, female_hour)
    except ValueError as e:
        raise ValueError(f"無効な日付です: {e}")
    
    return male_birth, female_birth

def get_season_from_branch(branch):
    """地支から季節判断"""
    seasons = {
        '寅': '春', '卯': '春', '辰': '春',
        '巳': '夏', '午': '夏', '未': '夏', 
        '申': '秋', '酉': '秋', '戌': '秋',
        '亥': '冬', '子': '冬', '丑': '冬'
    }
    return seasons.get(branch, '不明')

def analyze_cheongan_relation(day_stem1, target_stem):
    """天干関係分析"""
    if day_stem1 in CHEONGAN_MATRIX and target_stem in CHEONGAN_MATRIX[day_stem1]:
        return CHEONGAN_MATRIX[day_stem1][target_stem]
    return ('平', '一般関係')

def calculate_daeun_direction(year_stem, gender):
    """大運順逆行判断"""
    stems = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
    year_index = stems.index(year_stem)
    is_yang = (year_index % 2 == 0)
    
    if (is_yang and gender == 'male') or (not is_yang and gender == 'female'):
        return '順行'
    return '逆行'

def check_donsagong_principles(male_saju, female_saju):
    """돈사공原則違反チェック"""
    violations = []
    
    # 地支相性禁止チェックは省略（自動で見ないため）
    # 年干使用禁止も自動で見ないためパス
    
    return violations

def calculate_score(male_saju, female_saju):
    """スコア計算"""
    score_male = 50  # 男性基本スコア
    score_female = 50  # 女性基本スコア
    
    # 日干関係（最重要 - 30点）
    male_to_female = analyze_cheongan_relation(male_saju.day_stem, female_saju.day_stem)
    female_to_male = analyze_cheongan_relation(female_saju.day_stem, male_saju.day_stem)
    
    if '吉' in male_to_female[0]:
        score_male += 30
    elif '凶' in male_to_female[0]:
        score_male -= 20
    
    if '吉' in female_to_male[0]:
        score_female += 30
    elif '凶' in female_to_male[0]:
        score_female -= 20
    
    # 月干関係（15点）
    male_month_to_female = analyze_cheongan_relation(male_saju.month_stem, female_saju.month_stem)
    female_month_to_male = analyze_cheongan_relation(female_saju.month_stem, male_saju.month_stem)
    
    if '吉' in male_month_to_female[0]:
        score_male += 15
    elif '凶' in male_month_to_female[0]:
        score_male -= 10
        
    if '吉' in female_month_to_male[0]:
        score_female += 15
    elif '凶' in female_month_to_male[0]:
        score_female -= 10
    
    # 季節相性（15点）
    male_season = get_season_from_branch(male_saju.month_branch)
    female_season = get_season_from_branch(female_saju.month_branch)
    
    opposite_seasons = {'春': '秋', '夏': '冬', '秋': '春', '冬': '夏'}
    if male_season == opposite_seasons.get(female_season):
        score_male += 15
        score_female += 15
    elif male_season == female_season:
        score_male -= 5
        score_female -= 5
    
    # 大運方向（10点）
    male_direction = calculate_daeun_direction(male_saju.year_stem, 'male')
    female_direction = calculate_daeun_direction(female_saju.year_stem, 'female')
    
    if male_direction == female_direction:
        score_male += 10
        score_female += 10
    
    return score_male, score_female

def main():
    print("="*60)
    print("돈사공 相性分析 自動化プログラム")
    print("="*60)
    
    # 入力受付
    print("\n生年月日時を入力してください:")
    print("形式: 男性 YYYY/MM/DD/HH時, 女性 YYYY/MM/DD/HH時")
    print("例: 男性 1986/5/26/5時, 女性 1986/12/20/0時")
    
    input_str = input("\n入力: ")
    
    try:
        # 1. 入力解析と検証
        male_birth, female_birth = parse_input(input_str)
        
        # 2. 万歳暦計算
        calculator = ManseryeokCalculator()
        male_saju = calculator.calculate_saju(male_birth, 'male')
        female_saju = calculator.calculate_saju(female_birth, 'female')
        
        print(f"\n【四柱原局】")
        print(f"男性: {male_saju}")
        print(f"女性: {female_saju}")
        
        # 3. 돈사공原則チェック
        violations = check_donsagong_principles(male_saju, female_saju)
        if violations:
            print(f"\n⚠️ 돈사공原則違反: {', '.join(violations)}")
        
        # 4. 天干関係分析
        print(f"\n【天干関係分析】")
        
        # 月干関係
        male_month_rel = analyze_cheongan_relation(male_saju.month_stem, female_saju.month_stem)
        female_month_rel = analyze_cheongan_relation(female_saju.month_stem, male_saju.month_stem)
        print(f"月干: 男性→女性 {male_month_rel[0]}, 女性→男性 {female_month_rel[0]}")
        
        # 日干関係（最重要）
        male_day_rel = analyze_cheongan_relation(male_saju.day_stem, female_saju.day_stem)
        female_day_rel = analyze_cheongan_relation(female_saju.day_stem, male_saju.day_stem)
        print(f"日干: 男性→女性 {male_day_rel[0]}, 女性→男性 {female_day_rel[0]} ★")
        
        # 時干関係
        male_hour_rel = analyze_cheongan_relation(male_saju.hour_stem, female_saju.hour_stem)
        female_hour_rel = analyze_cheongan_relation(female_saju.hour_stem, male_saju.hour_stem)
        print(f"時干: 男性→女性 {male_hour_rel[0]}, 女性→男性 {female_hour_rel[0]}")
        
        # 5. 季節分析
        male_season = get_season_from_branch(male_saju.month_branch)
        female_season = get_season_from_branch(female_saju.month_branch)
        print(f"\n【季節相性】")
        print(f"男性: {male_season}, 女性: {female_season}")
        
        opposite_seasons = {'春': '秋', '夏': '冬', '秋': '春', '冬': '夏'}
        if male_season == opposite_seasons.get(female_season):
            print("✅ 反対季節 - 理想的")
        elif male_season == female_season:
            print("❌ 同じ季節 - 普通")
        else:
            print("◆ 異なる季節 - 無難")
        
        # 6. 大運方向
        male_direction = calculate_daeun_direction(male_saju.year_stem, 'male')
        female_direction = calculate_daeun_direction(female_saju.year_stem, 'female')
        print(f"\n【大運方向】")
        print(f"男性: {male_direction}, 女性: {female_direction}")
        if male_direction == female_direction:
            print("✅ 同じ方向 - 人生の流れが同調")
        else:
            print("⚠️ 異なる方向 - 人生の流れが相違")
        
        # 7. スコア計算と最終評価
        score_male, score_female = calculate_score(male_saju, female_saju)
        
        print(f"\n【最終評価】")
        print(f"男性観点スコア: {score_male}/100")
        print(f"女性観点スコア: {score_female}/100")
        
        def get_grade(score):
            if score >= 80: return "★★★★★"
            elif score >= 70: return "★★★★☆"
            elif score >= 60: return "★★★☆☆"
            elif score >= 50: return "★★☆☆☆"
            else: return "★☆☆☆☆"
        
        print(f"男性にとって: {get_grade(score_male)} 関係")
        print(f"女性にとって: {get_grade(score_female)} 関係")
        
        # 8. 得点/失点要約
        print(f"\n【関係特徴】")
        if score_male > score_female:
            print("男性に有利な関係")
        elif score_female > score_male:
            print("女性に有利な関係")
        else:
            print("お互いバランスの取れた関係")
        
        print(f"\n男性得点: 日干関係 {male_day_rel[0]}")
        print(f"女性得点: 日干関係 {female_day_rel[0]}")
        
    except Exception as e:
        print(f"❌ エラー: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())