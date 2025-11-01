#!/usr/bin/env python3
"""
돈사공 相性分析 プログラム（ユーザーフレンドリー版）
柔軟な入力に対応
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

def parse_input_flexible(input_str):
    """柔軟な入力解析"""
    # 全角スペースや特殊文字を半角に正規化
    input_str = input_str.replace('　', ' ').replace('，', ',').replace('、', ',')
    
    # 色々なパターンを試す
    patterns = [
        # 標準形式
        r'男性\s*(\d{4})[/\-年](\d{1,2})[/\-月](\d{1,2})[日]?\s*[/\-]?\s*(\d{1,2})[時時間].*女性\s*(\d{4})[/\-年](\d{1,2})[/\-月](\d{1,2})[日]?\s*[/\-]?\s*(\d{1,2})[時時間]',
        # スペースがない場合
        r'男性(\d{4})[/\-年](\d{1,2})[/\-月](\d{1,2})[日]?\s*[/\-]?\s*(\d{1,2})[時時間].*女性(\d{4})[/\-年](\d{1,2})[/\-月](\d{1,2})[日]?\s*[/\-]?\s*(\d{1,2})[時時間]',
        # カンマやスペースで区切られている
        r'男性[:\s]*(\d{4})[/\-](\d{1,2})[/\-](\d{1,2})[/\-\s]*(\d{1,2}).*女性[:\s]*(\d{4})[/\-](\d{1,2})[/\-](\d{1,2})[/\-\s]*(\d{1,2})',
        # 数字だけでマッチ（最後の手段）
        r'(\d{4})[/\-](\d{1,2})[/\-](\d{1,2})[/\-\s]*(\d{1,2}).*(\d{4})[/\-](\d{1,2})[/\-](\d{1,2})[/\-\s]*(\d{1,2})'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, input_str)
        if match:
            try:
                male_year, male_month, male_day, male_hour = map(int, match.groups()[:4])
                female_year, female_month, female_day, female_hour = map(int, match.groups()[4:])
                
                # 日付の有効性チェック
                male_birth = datetime(male_year, male_month, male_day, male_hour)
                female_birth = datetime(female_year, female_month, female_day, female_hour)
                
                return male_birth, female_birth
            except ValueError:
                continue
    
    # どのパターンにも一致しない場合
    raise ValueError("入力を認識できませんでした。再度お試しください。")

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
    print("💝 相性診断プログラム")
    print("="*60)
    
    # より親切な入力案内
    print("\n二人の生年月日と出生時間を教えてください。")
    print("\n【入力例】")
    print("  男性 1986/5/26/5時, 女性 1986/12/20/0時")
    print("  男性1986年5月26日5時、女性1986年12月20日0時")
    print("  1986/5/26/5 1986/12/20/0")
    print("\n形式は自由です。男性の情報を先に入力してください。")
    
    input_str = input("\n入力 >>> ")
    
    # 入力が空の場合のサンプル提供
    if not input_str.strip():
        print("\n入力がありません。サンプルデータで実行しますか？ (y/n)")
        if input().lower() == 'y':
            input_str = "男性 1986/5/26/5時, 女性 1986/12/20/0時"
            print(f"サンプル: {input_str}")
        else:
            return 0
    
    try:
        # 1. 柔軟な入力解析
        male_birth, female_birth = parse_input_flexible(input_str)
        
        print("\n分析中...")
        
        # 2. 万歳暦計算
        calculator = ManseryeokCalculator()
        male_saju = calculator.calculate_saju(male_birth, 'male')
        female_saju = calculator.calculate_saju(female_birth, 'female')
        
        print(f"\n📋 【四柱】")
        print(f"男性: {male_saju}")
        print(f"女性: {female_saju}")
        
        # 3. 天干関係分析
        print(f"\n🔍 【天干関係】")
        
        # 日干関係（最重要）
        male_day_rel = analyze_cheongan_relation(male_saju.day_stem, female_saju.day_stem)
        female_day_rel = analyze_cheongan_relation(female_saju.day_stem, male_saju.day_stem)
        
        symbol_m = "✨" if '吉' in male_day_rel[0] else "⚠️" if '凶' in male_day_rel[0] else "◆"
        symbol_f = "✨" if '吉' in female_day_rel[0] else "⚠️" if '凶' in female_day_rel[0] else "◆"
        
        print(f"男性→女性: {male_day_rel[0]} {symbol_m}")
        print(f"女性→男性: {female_day_rel[0]} {symbol_f}")
        
        # 4. 季節分析
        male_season = get_season_from_branch(male_saju.month_branch)
        female_season = get_season_from_branch(female_saju.month_branch)
        
        opposite_seasons = {'春': '秋', '夏': '冬', '秋': '春', '冬': '夏'}
        season_match = ""
        if male_season == opposite_seasons.get(female_season):
            season_match = "✨ 理想的な季節の組み合わせ"
        elif male_season == female_season:
            season_match = "◆ 同じ季節"
        else:
            season_match = "○ 良い季節の組み合わせ"
        
        print(f"\n🍃 【季節相性】")
        print(f"男性: {male_season} × 女性: {female_season}")
        print(season_match)
        
        # 5. スコア計算と最終評価
        score_male, score_female = calculate_score(male_saju, female_saju)
        
        def get_grade(score):
            if score >= 80: return "★★★★★", "素晴らしい"
            elif score >= 70: return "★★★★☆", "とても良い"
            elif score >= 60: return "★★★☆☆", "良い"
            elif score >= 50: return "★★☆☆☆", "まあまあ"
            else: return "★☆☆☆☆", "要努力"
        
        grade_m, desc_m = get_grade(score_male)
        grade_f, desc_f = get_grade(score_female)
        
        print(f"\n💫 【総合評価】")
        print(f"\n男性にとって: {grade_m} {desc_m}関係（{score_male}点）")
        print(f"女性にとって: {grade_f} {desc_f}関係（{score_female}点）")
        
        # 6. 関係の特徴とアドバイス
        print(f"\n💞 【関係の特徴】")
        
        if score_male > score_female + 20:
            print("男性が女性から元気やパワーをもらいやすい関係です。")
            print("女性は献身的になりがちなので、感謝の気持ちを忘れずに。")
            print("時には女性をリードして、支える側に回ることも大切です。")
        elif score_female > score_male + 20:
            print("女性が男性に支えられて輝く関係です。")
            print("男性は与える喜びを感じられる素敵なパートナーシップ。")
            print("女性からの感謝と愛情表現が、関係をより深めます。")
        elif abs(score_male - score_female) <= 20:
            if score_male >= 70 and score_female >= 70:
                print("お互いが自然体でいられる理想的な関係です。")
                print("相手の良さを認め合い、成長し合えるパートナー。")
                print("この素晴らしいバランスを大切に育んでいきましょう。")
            elif score_male >= 50 and score_female >= 50:
                print("お互いを尊重し合える安定した関係です。")
                print("時には新鮮な刺激を加えて、関係に変化を。")
                print("相手への感謝を言葉にすることで、絆が深まります。")
            else:
                print("お二人の個性が強く、調整が必要な関係です。")
                print("違いを認め合い、歩み寄ることで成長できます。")
                print("コミュニケーションを大切に、理解を深めていきましょう。")
        
    except ValueError as e:
        print(f"\n😔 申し訳ございません: {e}")
        print("\n【ヒント】")
        print("・男性と女性の情報を順番に入力してください")
        print("・生年月日（YYYY/MM/DD）と時間（HH時）が必要です")
        print("・例: 男性 1990/3/15/14時, 女性 1992/8/20/9時")
    except Exception as e:
        print(f"\n❌ エラーが発生しました: {e}")
        print("もう一度お試しください。")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())