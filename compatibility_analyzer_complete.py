#!/usr/bin/env python3
"""
돈사공 相性分析 完全版
月干・日干・時干の全関係 + 大運分析を含む
"""

from datetime import datetime
import sys
import os
import re
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.manseryeok.calculator import ManseryeokCalculator
from accurate_daeun_calculator import AccurateDaeunCalculator

# 調候表（月支別の吉凶判定）
JOHU_TABLE = {
    '寅': {'寅': '小吉', '卯': '小吉', '辰': '小吉',
           '巳': '中吉', '午': '大吉', '未': '中吉',
           '申': '大凶', '酉': '大凶', '戌': '大凶',
           '亥': '大凶', '子': '大凶', '丑': '大凶'},
    '卯': {'寅': '小吉', '卯': '小吉', '辰': '小吉',
           '巳': '大吉', '午': '大吉', '未': '大吉',
           '申': '凶', '酉': '凶', '戌': '凶',
           '亥': '凶', '子': '凶', '丑': '凶'},
    '辰': {'寅': '吉', '卯': '吉', '辰': '吉',
           '巳': '吉', '午': '吉', '未': '吉',
           '申': '吉', '酉': '吉', '戌': '凶',
           '亥': '凶', '子': '凶', '丑': '凶'},
    '巳': {'寅': '小吉', '卯': '小吉', '辰': '小吉',
           '巳': '凶', '午': '凶', '未': '凶',
           '申': '小吉', '酉': '小吉', '戌': '小吉',
           '亥': '吉', '子': '吉', '丑': '吉'},
    '午': {'寅': '中吉', '卯': '小吉', '辰': '小吉',
           '巳': '凶', '午': '凶', '未': '凶',
           '申': '吉', '酉': '吉', '戌': '吉',
           '亥': '大吉', '子': '大吉', '丑': '大吉'},
    '未': {'寅': '小吉', '卯': '小吉', '辰': '小吉',
           '巳': '凶', '午': '凶', '未': '凶',
           '申': '小吉', '酉': '小吉', '戌': '凶',
           '亥': '大吉', '子': '大吉', '丑': '吉'},
    '申': {'寅': '吉', '卯': '吉', '辰': '吉',
           '巳': '大吉', '午': '大吉', '未': '大吉',
           '申': '凶', '酉': '凶', '戌': '吉',
           '亥': '凶', '子': '凶', '丑': '凶'},
    '酉': {'寅': '小吉', '卯': '小吉', '辰': '小吉',
           '巳': '大吉', '午': '大吉', '未': '大吉',
           '申': '凶', '酉': '凶', '戌': '凶',
           '亥': '凶', '子': '凶', '丑': '凶'},
    '戌': {'寅': '小吉', '卯': '小吉', '辰': '小吉',
           '巳': '吉', '午': '吉', '未': '吉',
           '申': '小吉', '酉': '小吉', '戌': '小吉',
           '亥': '凶', '子': '凶', '丑': '凶'},
    '亥': {'寅': '小吉', '卯': '小吉', '辰': '小吉',
           '巳': '大吉', '午': '大吉', '未': '大吉',
           '申': '凶', '酉': '凶', '戌': '中吉',
           '亥': '中大凶', '子': '中大凶', '丑': '中大凶'},
    '子': {'寅': '小吉', '卯': '小吉', '辰': '小吉',
           '巳': '大吉', '午': '大吉', '未': '大吉',
           '申': '凶', '酉': '凶', '戌': '大吉',
           '亥': '中大凶', '子': '中大凶', '丑': '中大凶'},
    '丑': {'寅': '吉', '卯': '吉', '辰': '吉',
           '巳': '大吉', '午': '大吉', '未': '大吉',
           '申': '凶', '酉': '凶', '戌': '吉',
           '亥': '中大吉', '子': '中大吉', '丑': '凶'}
}

# 調候の吉凶を点数に変換
JOHU_SCORES = {
    '大吉': 100,
    '中大吉': 95,
    '中吉': 80,
    '吉': 70,
    '小吉': 60,
    '平': 50,
    '凶': 30,
    '中大凶': 10,
    '大凶': 5
}

# 天干マトリックス完全ハードコーディング
CHEONGAN_MATRIX = {
    '甲': {
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
    '乙': {
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
    '丙': {
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
    '丁': {
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
    '戊': {
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
    '己': {
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
    '庚': {
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
    '辛': {
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
    '壬': {
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
    '癸': {
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
    input_str = input_str.replace('　', ' ').replace('，', ',').replace('、', ',')
    
    patterns = [
        r'男性\s*(\d{4})[/\-年](\d{1,2})[/\-月](\d{1,2})[日]?\s*[/\-]?\s*(\d{1,2})[時時間].*女性\s*(\d{4})[/\-年](\d{1,2})[/\-月](\d{1,2})[日]?\s*[/\-]?\s*(\d{1,2})[時時間]',
        r'男性(\d{4})[/\-年](\d{1,2})[/\-月](\d{1,2})[日]?\s*[/\-]?\s*(\d{1,2})[時時間].*女性(\d{4})[/\-年](\d{1,2})[/\-月](\d{1,2})[日]?\s*[/\-]?\s*(\d{1,2})[時時間]',
        r'男性[:\s]*(\d{4})[/\-](\d{1,2})[/\-](\d{1,2})[/\-\s]*(\d{1,2}).*女性[:\s]*(\d{4})[/\-](\d{1,2})[/\-](\d{1,2})[/\-\s]*(\d{1,2})',
        r'(\d{4})[/\-](\d{1,2})[/\-](\d{1,2})[/\-\s]*(\d{1,2}).*(\d{4})[/\-](\d{1,2})[/\-](\d{1,2})[/\-\s]*(\d{1,2})'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, input_str)
        if match:
            try:
                male_year, male_month, male_day, male_hour = map(int, match.groups()[:4])
                female_year, female_month, female_day, female_hour = map(int, match.groups()[4:])
                
                male_birth = datetime(male_year, male_month, male_day, male_hour)
                female_birth = datetime(female_year, female_month, female_day, female_hour)
                
                return male_birth, female_birth
            except ValueError:
                continue
    
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

def get_symbol(relation):
    """関係から記号を取得"""
    if '大吉' in relation:
        return '🌟'
    elif '吉' in relation:
        return '✨'
    elif '大凶' in relation:
        return '💔'
    elif '凶' in relation:
        return '⚠️'
    elif '無' in relation or '平' in relation:
        return '◆'
    else:
        return '○'

def get_relation_score(relation):
    """天干関係を点数に変換"""
    if '大吉' in relation:
        return 100
    elif '吉' in relation:
        return 70
    elif '平' in relation or '無' in relation:
        return 50
    elif '大凶' in relation:
        return 10
    elif '凶' in relation:
        return 30
    else:
        return 50

def check_yongshin(day_stem, month_branch, target):
    """用神チェック - データベースに基づいて判定"""
    # 用神データベース（簡略版）
    YONGSHIN_DB = {
        '庚': {  # 庚金
            '春': {'天干': ['丙', '甲'], '地支': ['辰']},
            '夏': {'天干': ['壬', '甲'], '地支': ['辰', '申', '子']},
            '秋': {'天干': ['丁', '丙', '甲', '壬'], '地支': ['寅']},
            '冬': {'天干': ['戊', '丁', '甲'], '地支': ['寅', '午', '戌', '未']}
        },
        '戊': {  # 戊土
            '春': {'天干': ['甲', '乙', '丙'], '地支': ['辰']},
            '夏': {'天干': ['甲', '乙', '丙'], '地支': ['辰', '申', '子']},
            '秋': {'天干': ['甲', '乙', '丙', '丁'], '地支': ['寅', '卯', '辰']},
            '冬': {'天干': ['丁', '丙', '甲', '乙'], '地支': ['午', '戌', '未']}
        },
        '丁': {  # 丁火（特殊）
            '春': {'天干': ['甲', '乙', '庚'], '地支': ['辰']},
            '夏': {'天干': [], '地支': ['辰', '申', '子']},
            '秋': {'天干': ['甲', '乙', '庚', '戊', '己'], '地支': ['寅']},
            '冬': {'天干': ['甲', '乙', '庚', '戊', '己'], '地支': ['午', '戌', '未']}
        },
        '壬': {  # 壬水
            '春': {'天干': ['庚', '辛'], '地支': ['辰']},
            '夏': {'天干': ['庚', '辛'], '地支': ['辰', '申']},
            '秋': {'天干': ['甲', '丙', '庚', '辛'], '地支': ['寅']},
            '冬': {'天干': ['丙', '戊'], '地支': ['午', '戌', '未']}
        }
        # 他の天干も同様に追加可能
    }
    
    # 季節を取得
    season = get_season_from_branch(month_branch)
    
    # 該当する用神データを取得
    if day_stem in YONGSHIN_DB and season in YONGSHIN_DB[day_stem]:
        yongshin_data = YONGSHIN_DB[day_stem][season]
        # targetが天干か地支かを判定して用神チェック
        if len(target) == 1:  # 天干
            return target in yongshin_data.get('天干', [])
        else:  # 地支
            return target in yongshin_data.get('地支', [])
    
    return False

def check_spouse_palace_yongshin(person_saju):
    """配偶者宮（日支）が用神かチェック"""
    return check_yongshin(person_saju.day_stem, person_saju.month_branch, person_saju.day_branch)

def evaluate_daeun_for_person(person_saju, current_daeun):
    """本人の原局に対する大運の評価（天干30% + 調候60% + 用神10%）"""
    
    # 1. 天干関係の評価（30%）
    tiangang_relation = analyze_cheongan_relation(person_saju.day_stem, current_daeun['stem'])
    tiangang_score = get_relation_score(tiangang_relation[0])
    
    # 2. 調候の評価（60%）
    month_branch = person_saju.month_branch
    daeun_branch = current_daeun['branch']
    
    if month_branch in JOHU_TABLE and daeun_branch in JOHU_TABLE[month_branch]:
        johu_rating = JOHU_TABLE[month_branch][daeun_branch]
        johu_score = JOHU_SCORES.get(johu_rating, 50)
    else:
        johu_score = 50  # デフォルト値
    
    # 3. 用神チェック（10%）
    # 大運の天干・地支が用神かチェック
    daeun_stem_is_yongshin = check_yongshin(person_saju.day_stem, person_saju.month_branch, current_daeun['stem'])
    daeun_branch_is_yongshin = check_yongshin(person_saju.day_stem, person_saju.month_branch, current_daeun['branch'])
    
    if daeun_stem_is_yongshin or daeun_branch_is_yongshin:
        yongshin_score = 100
    else:
        yongshin_score = 50
    
    # 総合点数計算
    total_score = (tiangang_score * 0.3) + (johu_score * 0.6) + (yongshin_score * 0.1)
    
    return {
        'total': total_score,
        'tiangang': tiangang_score,
        'johu': johu_score,
        'yongshin': yongshin_score,
        'tiangang_rel': tiangang_relation[0],
        'johu_rating': johu_rating if month_branch in JOHU_TABLE and daeun_branch in JOHU_TABLE[month_branch] else '平'
    }

def calculate_daeun(saju, gender, birth_date):
    """詳細大運計算 - 正確な節入日データベースを使用"""
    stems = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
    branches = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
    
    # 順逆行判断
    year_index = stems.index(saju.year_stem)
    is_yang = (year_index % 2 == 0)
    
    if (is_yang and gender == 'male') or (not is_yang and gender == 'female'):
        direction = 1  # 順行
        direction_str = '順行'
    else:
        direction = -1  # 逆行
        direction_str = '逆行'
    
    # 月柱から大運計算
    month_stem_idx = stems.index(saju.month_stem)
    month_branch_idx = branches.index(saju.month_branch)
    
    # 正確な起運年齢計算（節入日データベース使用）
    try:
        from datetime import timezone, timedelta
        # KST変換が必要な場合
        KST = timezone(timedelta(hours=9))
        if birth_date.tzinfo is None:
            birth_date_kst = birth_date.replace(tzinfo=KST)
        else:
            birth_date_kst = birth_date.astimezone(KST)
            
        accurate_calc = AccurateDaeunCalculator()
        starting_age = accurate_calc.calculate_starting_age(
            birth_date_kst, 
            gender, 
            saju.year_stem
        )
        print(f"📌 正確な起運年齢計算完了: {starting_age}歳（{direction_str}）")
    except Exception as e:
        # データベースエラーの場合は簡易計算にフォールバック
        print(f"⚠️ 節入日データベースアクセスエラー、簡易計算を使用: {e}")
        day_factor = birth_date.day % 10
        if direction == 1:  # 順行
            starting_age = 1 + day_factor  # 1-10歳
        else:  # 逆行
            starting_age = 10 - day_factor  # 1-10歳
        starting_age = max(1, min(starting_age, 10))  # 1-10歳の範囲に制限
    
    daeun_list = []
    for i in range(10):  # 10大運まで計算
        new_stem_idx = (month_stem_idx + direction * (i + 1)) % 10
        new_branch_idx = (month_branch_idx + direction * (i + 1)) % 12
        
        new_stem = stems[new_stem_idx]
        new_branch = branches[new_branch_idx]
        
        # 起運年齢計算
        start_age = starting_age + (i * 10)
        end_age = start_age + 9
        
        daeun_list.append({
            'order': i + 1,
            'start_age': start_age,
            'end_age': end_age,
            'stem': new_stem,
            'branch': new_branch,
            'ganzi': f"{new_stem}{new_branch}"
        })
    
    return {
        'direction': direction_str,
        'starting_age': starting_age,
        'list': daeun_list
    }

def calculate_score(male_saju, female_saju, male_current_daeun=None, female_current_daeun=None):
    """詳細スコア計算"""
    score_male = 50
    score_female = 50
    details_male = []
    details_female = []
    
    # 日干関係（最重要 - 30点）
    male_day_rel = analyze_cheongan_relation(male_saju.day_stem, female_saju.day_stem)
    female_day_rel = analyze_cheongan_relation(female_saju.day_stem, male_saju.day_stem)
    
    if '大吉' in male_day_rel[0]:
        score_male += 40
        details_male.append("日干：大吉 +40")
    elif '吉' in male_day_rel[0]:
        score_male += 30
        details_male.append("日干：吉 +30")
    elif '大凶' in male_day_rel[0]:
        score_male -= 30
        details_male.append("日干：大凶 -30")
    elif '凶' in male_day_rel[0]:
        score_male -= 20
        details_male.append("日干：凶 -20")
    
    if '大吉' in female_day_rel[0]:
        score_female += 40
        details_female.append("日干：大吉 +40")
    elif '吉' in female_day_rel[0]:
        score_female += 30
        details_female.append("日干：吉 +30")
    elif '大凶' in female_day_rel[0]:
        score_female -= 30
        details_female.append("日干：大凶 -30")
    elif '凶' in female_day_rel[0]:
        score_female -= 20
        details_female.append("日干：凶 -20")
    
    # 月干関係（15点）
    male_month_rel = analyze_cheongan_relation(male_saju.month_stem, female_saju.month_stem)
    female_month_rel = analyze_cheongan_relation(female_saju.month_stem, male_saju.month_stem)
    
    if '吉' in male_month_rel[0]:
        score_male += 15
        details_male.append("月干：吉 +15")
    elif '凶' in male_month_rel[0]:
        score_male -= 10
        details_male.append("月干：凶 -10")
        
    if '吉' in female_month_rel[0]:
        score_female += 15
        details_female.append("月干：吉 +15")
    elif '凶' in female_month_rel[0]:
        score_female -= 10
        details_female.append("月干：凶 -10")
    
    # 時干関係（10点）
    male_hour_rel = analyze_cheongan_relation(male_saju.hour_stem, female_saju.hour_stem)
    female_hour_rel = analyze_cheongan_relation(female_saju.hour_stem, male_saju.hour_stem)
    
    if '吉' in male_hour_rel[0]:
        score_male += 10
        details_male.append("時干：吉 +10")
    elif '凶' in male_hour_rel[0]:
        score_male -= 5
        details_male.append("時干：凶 -5")
        
    if '吉' in female_hour_rel[0]:
        score_female += 10
        details_female.append("時干：吉 +10")
    elif '凶' in female_hour_rel[0]:
        score_female -= 5
        details_female.append("時干：凶 -5")
    
    # 季節相性（15点）
    male_season = get_season_from_branch(male_saju.month_branch)
    female_season = get_season_from_branch(female_saju.month_branch)
    
    opposite_seasons = {'春': '秋', '夏': '冬', '秋': '春', '冬': '夏'}
    if male_season == opposite_seasons.get(female_season):
        score_male += 15
        score_female += 15
        details_male.append("季節：反対 +15")
        details_female.append("季節：反対 +15")
    elif male_season == female_season:
        score_male -= 5
        score_female -= 5
        details_male.append("季節：同じ -5")
        details_female.append("季節：同じ -5")
    
    # 大運と日柱の一致ボーナス
    if male_current_daeun and female_current_daeun:
        if f"{male_current_daeun['stem']}{male_current_daeun['branch']}" == f"{female_saju.day_stem}{female_saju.day_branch}":
            score_male += 5
            details_male.append("大運ボーナス +5")
        
        if f"{female_current_daeun['stem']}{female_current_daeun['branch']}" == f"{male_saju.day_stem}{male_saju.day_branch}":
            score_female += 5
            details_female.append("大運ボーナス +5")
    
    return score_male, score_female, details_male, details_female

def main():
    print("="*60)
    print("💝 相性診断プログラム【完全版】")
    print("="*60)
    
    print("\n二人の生年月日と出生時間を教えてください。")
    print("\n【入力例】")
    print("  男性 1986/5/26/5時, 女性 1986/12/20/0時")
    print("  男性1986年5月26日5時、女性1986年12月20日0時")
    
    input_str = input("\n入力 >>> ")
    
    if not input_str.strip():
        print("\n入力がありません。サンプルデータで実行しますか？ (y/n)")
        if input().lower() == 'y':
            input_str = "男性 1986/5/26/5時, 女性 1986/12/20/0時"
            print(f"サンプル: {input_str}")
        else:
            return 0
    
    try:
        # 1. 入力解析
        male_birth, female_birth = parse_input_flexible(input_str)
        
        print("\n分析中...")
        
        # 2. 万歳暦計算
        calculator = ManseryeokCalculator()
        male_saju = calculator.calculate_saju(male_birth, 'male')
        female_saju = calculator.calculate_saju(female_birth, 'female')
        
        print(f"\n📋 【四柱】")
        print(f"男性({male_birth.year}年): {male_saju}")
        print(f"女性({female_birth.year}年): {female_saju}")
        
        # 配偶者運チェック
        male_has_spouse_luck = check_spouse_palace_yongshin(male_saju)
        female_has_spouse_luck = check_spouse_palace_yongshin(female_saju)
        
        print(f"\n🔮 【配偶者運】")
        if male_has_spouse_luck:
            print(f"  男性：配偶者宮に用神あり ✨（良い配偶者運）")
        else:
            print(f"  男性：配偶者宮に用神なし（通常の配偶者運）")
        
        if female_has_spouse_luck:
            print(f"  女性：配偶者宮に用神あり ✨（良い配偶者運）")
        else:
            print(f"  女性：配偶者宮に用神なし（通常の配偶者運）")
        
        # 3. 天干関係詳細分析（月・日・時）
        print(f"\n🔍 【天干関係詳細】")
        print("-" * 40)
        
        # 月干関係
        male_month_rel = analyze_cheongan_relation(male_saju.month_stem, female_saju.month_stem)
        female_month_rel = analyze_cheongan_relation(female_saju.month_stem, male_saju.month_stem)
        print(f"【月干】")
        print(f"  男性{male_saju.month_stem}→女性{female_saju.month_stem}: {male_month_rel[0]} {get_symbol(male_month_rel[0])}")
        print(f"  女性{female_saju.month_stem}→男性{male_saju.month_stem}: {female_month_rel[0]} {get_symbol(female_month_rel[0])}")
        
        # 日干関係（最重要）
        male_day_rel = analyze_cheongan_relation(male_saju.day_stem, female_saju.day_stem)
        female_day_rel = analyze_cheongan_relation(female_saju.day_stem, male_saju.day_stem)
        print(f"\n【日干】★最重要★")
        print(f"  男性{male_saju.day_stem}→女性{female_saju.day_stem}: {male_day_rel[0]} {get_symbol(male_day_rel[0])}")
        print(f"  女性{female_saju.day_stem}→男性{male_saju.day_stem}: {female_day_rel[0]} {get_symbol(female_day_rel[0])}")
        
        # 時干関係
        male_hour_rel = analyze_cheongan_relation(male_saju.hour_stem, female_saju.hour_stem)
        female_hour_rel = analyze_cheongan_relation(female_saju.hour_stem, male_saju.hour_stem)
        print(f"\n【時干】")
        print(f"  男性{male_saju.hour_stem}→女性{female_saju.hour_stem}: {male_hour_rel[0]} {get_symbol(male_hour_rel[0])}")
        print(f"  女性{female_saju.hour_stem}→男性{male_saju.hour_stem}: {female_hour_rel[0]} {get_symbol(female_hour_rel[0])}")
        
        # 4. 大運計算と分析
        print(f"\n📊 【大運分析】")
        print("-" * 40)
        
        # 簡易版の大運計算を使用（万歳暦システムにバグがあるため）
        male_daeun = calculate_daeun(male_saju, 'male', male_birth)
        female_daeun = calculate_daeun(female_saju, 'female', female_birth)
        
        current_year = datetime.now().year
        male_age = current_year - male_birth.year
        female_age = current_year - female_birth.year
        
        # 現在大運を見つける
        male_current_daeun = None
        female_current_daeun = None
        
        for daeun in male_daeun['list']:
            if daeun['start_age'] <= male_age <= daeun['end_age']:
                male_current_daeun = daeun
                break
        
        for daeun in female_daeun['list']:
            if daeun['start_age'] <= female_age <= daeun['end_age']:
                female_current_daeun = daeun
                break
        
        # 各自の大運評価
        if male_current_daeun and female_current_daeun:
            male_eval = evaluate_daeun_for_person(male_saju, male_current_daeun)
            female_eval = evaluate_daeun_for_person(female_saju, female_current_daeun)
            
            print(f"【男性】{male_age}歳 - 第{male_current_daeun['order']}大運 {male_current_daeun['ganzi']}")
            print(f"  大運評価：{male_eval['total']:.0f}点")
            print(f"  ├ 天干関係({male_saju.day_stem}→{male_current_daeun['stem']}): {male_eval['tiangang_rel']} ({male_eval['tiangang']}点)")
            print(f"  ├ 調候({male_saju.month_branch}月生→{male_current_daeun['branch']}): {male_eval['johu_rating']} ({male_eval['johu']}点)")
            print(f"  └ 用神: {male_eval['yongshin']}点")
            
            print(f"\n【女性】{female_age}歳 - 第{female_current_daeun['order']}大運 {female_current_daeun['ganzi']}")
            print(f"  大運評価：{female_eval['total']:.0f}点")
            print(f"  ├ 天干関係({female_saju.day_stem}→{female_current_daeun['stem']}): {female_eval['tiangang_rel']} ({female_eval['tiangang']}点)")
            print(f"  ├ 調候({female_saju.month_branch}月生→{female_current_daeun['branch']}): {female_eval['johu_rating']} ({female_eval['johu']}点)")
            print(f"  └ 用神: {female_eval['yongshin']}点")
            
            # 大運同調性判定（点数差5点以内）
            score_diff = abs(male_eval['total'] - female_eval['total'])
            print(f"\n【大運の同調性】")
            if score_diff <= 5:
                print(f"  ✅ 運の流れが同調しています（差: {score_diff:.0f}点）")
                print(f"     お二人とも同じような運気の波に乗っています")
            elif score_diff <= 10:
                print(f"  ○ 運の流れがほぼ同調（差: {score_diff:.0f}点）")
                print(f"     少し差はありますが、似た運気です")
            else:
                print(f"  △ 運の流れに差があります（差: {score_diff:.0f}点）")
                print(f"     それぞれ異なる運気の中にいます")
            
            # 大運と相手日柱の一致チェック（ボーナス）
            bonus_points = 0
            bonus_messages = []
            
            if f"{male_current_daeun['stem']}{male_current_daeun['branch']}" == f"{female_saju.day_stem}{female_saju.day_branch}":
                bonus_points += 5
                bonus_messages.append(f"  ⭐ 男性の大運が女性の日柱と一致！（+5点）")
            
            if f"{female_current_daeun['stem']}{female_current_daeun['branch']}" == f"{male_saju.day_stem}{male_saju.day_branch}":
                bonus_points += 5
                bonus_messages.append(f"  ⭐ 女性の大運が男性の日柱と一致！（+5点）")
            
            if bonus_messages:
                print("\n【特別ボーナス】")
                for msg in bonus_messages:
                    print(msg)
        
        # 今後の大運予測
        print(f"\n【今後の大運】")
        print("男性の大運：")
        for i, daeun in enumerate(male_daeun['list'][:4]):
            marker = " ← 現在" if daeun == male_current_daeun else ""
            print(f"  {daeun['start_age']:2}-{daeun['end_age']:2}歳: {daeun['ganzi']}{marker}")
        
        print("\n女性の大運：")
        for i, daeun in enumerate(female_daeun['list'][:4]):
            marker = " ← 現在" if daeun == female_current_daeun else ""
            print(f"  {daeun['start_age']:2}-{daeun['end_age']:2}歳: {daeun['ganzi']}{marker}")
        
        # 5. 季節分析
        male_season = get_season_from_branch(male_saju.month_branch)
        female_season = get_season_from_branch(female_saju.month_branch)
        
        print(f"\n🍃 【季節相性】")
        print(f"男性: {male_season} × 女性: {female_season}")
        
        opposite_seasons = {'春': '秋', '夏': '冬', '秋': '春', '冬': '夏'}
        if male_season == opposite_seasons.get(female_season):
            print("✨ 理想的な季節の組み合わせ")
        elif male_season == female_season:
            print("◆ 同じ季節")
        else:
            print("○ 良い季節の組み合わせ")
        
        # 6. スコア計算と最終評価
        score_male, score_female, details_m, details_f = calculate_score(male_saju, female_saju)
        
        def get_grade(score):
            if score >= 80: return "★★★★★", "素晴らしい"
            elif score >= 70: return "★★★★☆", "とても良い"
            elif score >= 60: return "★★★☆☆", "良い"
            elif score >= 50: return "★★☆☆☆", "まあまあ"
            else: return "★☆☆☆☆", "要努力"
        
        grade_m, desc_m = get_grade(score_male)
        grade_f, desc_f = get_grade(score_female)
        
        print(f"\n💫 【総合評価】")
        print("-" * 40)
        print(f"\n男性にとって: {grade_m} {desc_m}関係（{score_male}点）")
        for detail in details_m:
            print(f"  {detail}")
        
        print(f"\n女性にとって: {grade_f} {desc_f}関係（{score_female}点）")
        for detail in details_f:
            print(f"  {detail}")
        
        # 7. 関係の特徴とアドバイス
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
    except Exception as e:
        print(f"\n❌ エラーが発生しました: {e}")
        print("もう一度お試しください。")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())