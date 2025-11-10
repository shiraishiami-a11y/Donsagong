"""
ドンサゴン吉凶判定サービス
DONSAGONG_MASTER_DATABASE.mdに基づいた大運の吉凶レベル判定
"""
from datetime import datetime
from typing import Dict, List, Literal, Optional, Tuple

# 吉凶レベル型（7段階）
FortuneLevel = Literal["大吉", "吉", "中吉", "小吉", "平", "凶", "大凶"]

# 月地支から季節を取得するマッピング
MONTH_BRANCH_TO_SEASON = {
    "寅": "봄",  # 2月
    "卯": "봄",  # 3月
    "辰": "봄",  # 4月
    "巳": "여름",  # 5月
    "午": "여름",  # 6月
    "未": "여름",  # 7月
    "申": "가을",  # 8月
    "酉": "가을",  # 9月
    "戌": "가을",  # 10月
    "亥": "겨울",  # 11月
    "子": "겨울",  # 12月
    "丑": "겨울",  # 1月
}


class FortuneAnalyzer:
    """ドンサゴン吉凶判定エンジン"""

    def __init__(self):
        """初期化"""
        # 天干100マトリックス
        self.tengan_matrix = self._load_tengan_matrix()

        # 地支144マトリックス
        self.jiji_matrix = self._load_jiji_matrix()

        # 調候用神表（月地支別）
        self.johoo_table = self._load_johoo_table()

    def analyze_daeun_fortune(
        self,
        day_stem: str,
        day_branch: str,
        hour_stem: str,
        hour_branch: str,
        month_branch: str,
        daeun_stem: str,
        daeun_branch: str,
    ) -> FortuneLevel:
        """
        大運の吉凶レベルを7段階で判定

        新ロジック（2025-11-10確定）:
        - 日柱50% + 時柱20% + 調候30% = 100%
        - 各柱内: 天干70% + 地支30%（三合時は40%）
        - 三合成立時は地支を吉(+1)扱い

        Args:
            day_stem: 日干
            day_branch: 日支
            hour_stem: 時干
            hour_branch: 時支
            month_branch: 月地支（季節判定用）
            daeun_stem: 大運天干
            daeun_branch: 大運地支

        Returns:
            吉凶レベル（7段階）
        """
        # 天干の吉凶を取得
        day_stem_fortune = self._check_tengan_relation(day_stem, daeun_stem)
        hour_stem_fortune = self._check_tengan_relation(hour_stem, daeun_stem)

        # 地支の吉凶を取得
        day_branch_fortune = self._check_jiji_relation(day_branch, daeun_branch)
        hour_branch_fortune = self._check_jiji_relation(hour_branch, daeun_branch)

        # 調候判定
        johoo_fortune = self._check_johoo(month_branch, daeun_branch, day_stem)

        # スコア化
        score_map = {"大吉": 2, "吉": 1, "平": 0, "凶": -1, "大凶": -2}
        day_stem_score = score_map.get(day_stem_fortune, 0)
        hour_stem_score = score_map.get(hour_stem_fortune, 0)
        johoo_score = score_map.get(johoo_fortune, 0)

        # 三合チェック
        day_sangap = self._is_sangap(day_branch, daeun_branch)
        hour_sangap = self._is_sangap(hour_branch, daeun_branch)

        # 地支スコアと重み（三合時は吉+1扱い＆重み0.4）
        if day_sangap:
            day_branch_score = 1  # 吉扱い
            day_jiji_weight = 0.4
        else:
            day_branch_score = score_map.get(day_branch_fortune, 0)
            day_jiji_weight = 0.3

        if hour_sangap:
            hour_branch_score = 1  # 吉扱い
            hour_jiji_weight = 0.4
        else:
            hour_branch_score = score_map.get(hour_branch_fortune, 0)
            hour_jiji_weight = 0.3

        # 柱スコア計算
        day_pillar = day_stem_score * 0.7 + day_branch_score * day_jiji_weight
        hour_pillar = hour_stem_score * 0.7 + hour_branch_score * hour_jiji_weight

        # 最終スコア（日柱50% + 時柱20% + 調候30%）
        total_score = day_pillar * 0.5 + hour_pillar * 0.2 + johoo_score * 0.3

        # 7段階に変換
        return self._score_to_fortune(total_score)

    def _check_tengan_relation(self, from_stem: str, to_stem: str) -> str:
        """
        天干関係を判定

        ドンサゴン原則:
        - 天干の合(合)は基本的に凶
        - 天干マトリックスに基づく判定

        Args:
            from_stem: 基準天干（日干または時干）
            to_stem: 対象天干（大運天干）

        Returns:
            吉凶判定（'大吉', '吉', '平', '凶', '大凶'）
        """
        # 同じ天干は平（大運では吉凶に応じて変化）
        if from_stem == to_stem:
            return "平"

        # マトリックスから関係を取得
        relation = self.tengan_matrix.get(from_stem, {}).get(to_stem, "平")
        return relation

    def _check_jiji_relation(self, from_branch: str, to_branch: str) -> str:
        """
        地支関係を判定

        ドンサゴン原則:
        - 地支の合(合)は無条件吉
        - 充(沖)は凶

        Args:
            from_branch: 基準地支（日支または時支）
            to_branch: 対象地支（大運地支）

        Returns:
            吉凶判定（'大吉', '吉', '平', '凶', '大凶'）
        """
        # 同じ地支は平
        if from_branch == to_branch:
            return "平"

        # マトリックスから関係を取得
        relation = self.jiji_matrix.get(from_branch, {}).get(to_branch, "平")
        return relation

    def _is_sangap(self, branch1: str, branch2: str) -> bool:
        """
        三合（サンガプ）判定

        三合グループ（六合は除外）:
        - 木局: 寅・午・戌
        - 火局: 巳・酉・丑
        - 金局: 申・子・辰
        - 水局: 亥・卯・未

        Args:
            branch1: 地支1
            branch2: 地支2

        Returns:
            True: 三合成立, False: 三合なし
        """
        sangap_groups = [
            {"寅", "午", "戌"},  # 木局
            {"巳", "酉", "丑"},  # 火局
            {"申", "子", "辰"},  # 金局
            {"亥", "卯", "未"},  # 水局
        ]
        for group in sangap_groups:
            if branch1 in group and branch2 in group:
                return True
        return False

    def _check_johoo(self, month_branch: str, daeun_branch: str, day_stem: str) -> str:
        """
        調候用神判定（大運地支ベース）

        ドンサゴン原則:
        - 調候用神 80% : 原局 20%（最重要）
        - 季節の反対が良い（夏生まれ→冬大運が吉）
        - 特殊規則: 丁火・辛金日干は秋冬が良い（月地支無関係）

        Args:
            month_branch: 原局月地支
            daeun_branch: 大運地支（調候判定用）
            day_stem: 日干（特殊規則判定用）

        Returns:
            吉凶判定（'大吉', '吉', '平', '凶', '大凶'）
        """
        # 特殊規則: 丁火・辛金は独自の調候を使用
        if day_stem in ["丁", "辛"]:
            return self._check_special_johoo(daeun_branch)

        # 原局の季節を取得
        season = MONTH_BRANCH_TO_SEASON.get(month_branch, "봄")

        # 調候表から吉凶を取得（大運地支ベース）
        johoo_data = self.johoo_table.get(month_branch, {})
        fortune = johoo_data.get(daeun_branch, "平")

        return fortune

    def _check_special_johoo_by_stem(self, daeun_stem: str) -> str:
        """
        丁火・辛金の特殊調候判定（天干ベース）

        Args:
            daeun_stem: 大運天干

        Returns:
            吉凶判定
        """
        # 秋冬の天干（金水系）
        autumn_winter = ["庚", "辛", "壬", "癸"]

        if daeun_stem in autumn_winter:
            return "吉"  # 秋冬は小吉

        # 夏（火系）
        summer = ["丙", "丁"]
        if daeun_stem in summer:
            return "凶"

        # 春・土は平
        return "平"

    def _check_special_johoo(self, daeun_branch: str) -> str:
        """
        丁火・辛金の特殊調候判定

        丁火・辛金日干は秋冬調候が良い（一運・健康運のみ該当）

        Args:
            daeun_branch: 大運地支

        Returns:
            吉凶判定
        """
        # 秋冬の地支リスト
        autumn_winter = ["申", "酉", "戌", "亥", "子", "丑"]

        if daeun_branch in autumn_winter:
            return "吉"  # 秋冬は小吉

        # 夏は凶
        summer = ["巳", "午", "未"]
        if daeun_branch in summer:
            return "凶"

        # 春は平
        return "平"

    def _fortune_to_score(self, fortune: str) -> float:
        """吉凶をスコアに変換"""
        score_map = {
            "大吉": 2.0,
            "吉": 1.0,
            "小吉": 0.5,
            "平": 0.0,
            "小凶": -0.5,
            "凶": -1.0,
            "大凶": -2.0,
        }
        return score_map.get(fortune, 0.0)

    def _score_to_fortune(self, score: float) -> FortuneLevel:
        """スコアを7段階吉凶レベルに変換"""
        if score >= 1.5:
            return "大吉"
        elif score >= 0.7:
            return "吉"
        elif score >= 0.4:
            return "中吉"
        elif score >= 0.1:
            return "小吉"
        elif score > -0.3:
            return "平"
        elif score > -0.6:
            return "凶"
        else:
            return "大凶"

    def _load_tengan_matrix(self) -> Dict[str, Dict[str, str]]:
        """
        天干100マトリックスをロード
        DONSAGONG_MASTER_DATABASE.mdの天干マトリックスを簡略化して実装
        """
        return {
            "甲": {
                "甲": "平", "乙": "凶", "丙": "吉", "丁": "吉", "戊": "吉",
                "己": "大凶", "庚": "大凶", "辛": "凶", "壬": "凶", "癸": "吉"
            },
            "乙": {
                "甲": "吉", "乙": "平", "丙": "大吉", "丁": "吉", "戊": "吉",
                "己": "吉", "庚": "大凶", "辛": "凶", "壬": "凶", "癸": "吉"
            },
            "丙": {
                "甲": "吉", "乙": "吉", "丙": "平", "丁": "凶", "戊": "平",
                "己": "平", "庚": "凶", "辛": "大凶", "壬": "吉", "癸": "凶"
            },
            "丁": {
                "甲": "吉", "乙": "吉", "丙": "凶", "丁": "平", "戊": "吉",
                "己": "吉", "庚": "吉", "辛": "大凶", "壬": "大凶", "癸": "凶"
            },
            "戊": {
                "甲": "大吉", "乙": "吉", "丙": "吉", "丁": "吉", "戊": "平",
                "己": "凶", "庚": "凶", "辛": "凶", "壬": "平", "癸": "大凶"
            },
            "己": {
                "甲": "凶", "乙": "吉", "丙": "吉", "丁": "吉", "戊": "凶",
                "己": "平", "庚": "凶", "辛": "凶", "壬": "凶", "癸": "平"
            },
            "庚": {
                "甲": "吉", "乙": "大凶", "丙": "吉", "丁": "吉", "戊": "吉",
                "己": "吉", "庚": "平", "辛": "大凶", "壬": "吉", "癸": "吉"
            },
            "辛": {
                "甲": "吉", "乙": "吉", "丙": "大凶", "丁": "大凶", "戊": "凶",
                "己": "平", "庚": "凶", "辛": "平", "壬": "大吉", "癸": "吉"
            },
            "壬": {
                "甲": "吉", "乙": "吉", "丙": "大吉", "丁": "大凶", "戊": "吉",
                "己": "凶", "庚": "大吉", "辛": "凶", "壬": "平", "癸": "凶"
            },
            "癸": {
                "甲": "吉", "乙": "吉", "丙": "凶", "丁": "凶", "戊": "凶",
                "己": "凶", "庚": "吉", "辛": "凶", "壬": "凶", "癸": "平"
            }
        }

    def _load_jiji_matrix(self) -> Dict[str, Dict[str, str]]:
        """
        地支144マトリックスをロード
        DONSAGONG_MASTER_DATABASE.mdの地支マトリックスを簡略化して実装

        主要な関係:
        - 合: 吉
        - 充: 凶
        - 三合: 大吉
        """
        return {
            "寅": {
                "寅": "平", "卯": "凶", "辰": "吉", "巳": "吉", "午": "大吉", "未": "吉",
                "申": "大凶", "酉": "大凶", "戌": "吉", "亥": "平", "子": "凶", "丑": "凶"
            },
            "卯": {
                "寅": "吉", "卯": "平", "辰": "吉", "巳": "吉", "午": "平", "未": "大吉",
                "申": "大凶", "酉": "大凶", "戌": "平", "亥": "平", "子": "凶", "丑": "凶"
            },
            "辰": {
                "寅": "吉", "卯": "吉", "辰": "平", "巳": "大凶", "午": "凶", "未": "凶",
                "申": "平", "酉": "凶", "戌": "大凶", "亥": "平", "子": "平", "丑": "大凶"
            },
            "巳": {
                "寅": "吉", "卯": "吉", "辰": "大凶", "巳": "平", "午": "大凶", "未": "凶",
                "申": "凶", "酉": "吉", "戌": "凶", "亥": "大凶", "子": "凶", "丑": "吉"
            },
            "午": {
                "寅": "吉", "卯": "吉", "辰": "大凶", "巳": "凶", "午": "平", "未": "凶",
                "申": "平", "酉": "凶", "戌": "大吉", "亥": "平", "子": "凶", "丑": "吉"
            },
            "未": {
                "寅": "吉", "卯": "大吉", "辰": "凶", "巳": "凶", "午": "凶", "未": "平",
                "申": "吉", "酉": "平", "戌": "凶", "亥": "大吉", "子": "大吉", "丑": "凶"
            },
            "申": {
                "寅": "平", "卯": "凶", "辰": "吉", "巳": "平", "午": "平", "未": "平",
                "申": "平", "酉": "平", "戌": "凶", "亥": "平", "子": "吉", "丑": "凶"
            },
            "酉": {
                "寅": "凶", "卯": "凶", "辰": "凶", "巳": "吉", "午": "凶", "未": "凶",
                "申": "凶", "酉": "平", "戌": "凶", "亥": "凶", "子": "凶", "丑": "吉"
            },
            "戌": {
                "寅": "大吉", "卯": "凶", "辰": "大凶", "巳": "平", "午": "大吉", "未": "凶",
                "申": "吉", "酉": "平", "戌": "平", "亥": "平", "子": "平", "丑": "凶"
            },
            "亥": {
                "寅": "吉", "卯": "大吉", "辰": "凶", "巳": "大凶", "午": "凶", "未": "大吉",
                "申": "平", "酉": "平", "戌": "大吉", "亥": "平", "子": "凶", "丑": "凶"
            },
            "子": {
                "寅": "吉", "卯": "吉", "辰": "吉", "巳": "平", "午": "凶", "未": "凶",
                "申": "吉", "酉": "平", "戌": "凶", "亥": "大凶", "子": "平", "丑": "大凶"
            },
            "丑": {
                "寅": "吉", "卯": "吉", "辰": "凶", "巳": "吉", "午": "大吉", "未": "凶",
                "申": "平", "酉": "吉", "戌": "凶", "亥": "平", "子": "吉", "丑": "平"
            }
        }

    def _load_johoo_table(self) -> Dict[str, Dict[str, str]]:
        """
        調候用神表をロード
        DONSAGONG_MASTER_DATABASE.mdの調候用神吉凶表を実装

        月地支別に、大運地支の吉凶を判定
        """
        return {
            # 寅月生（2月）
            "寅": {
                "寅": "吉", "卯": "吉", "辰": "吉",
                "巳": "吉", "午": "大吉", "未": "吉",
                "申": "大凶", "酉": "大凶", "戌": "大凶",
                "亥": "大凶", "子": "大凶", "丑": "大凶"
            },
            # 卯月生（3月）
            "卯": {
                "寅": "吉", "卯": "吉", "辰": "吉",
                "巳": "大吉", "午": "大吉", "未": "大吉",
                "申": "凶", "酉": "凶", "戌": "凶",
                "亥": "凶", "子": "凶", "丑": "凶"
            },
            # 辰月生（4月）
            "辰": {
                "寅": "吉", "卯": "吉", "辰": "吉",
                "巳": "吉", "午": "吉", "未": "吉",
                "申": "吉", "酉": "吉", "戌": "凶",
                "亥": "凶", "子": "凶", "丑": "凶"
            },
            # 巳月生（5月）
            "巳": {
                "寅": "吉", "卯": "吉", "辰": "吉",
                "巳": "凶", "午": "凶", "未": "凶",
                "申": "吉", "酉": "吉", "戌": "吉",
                "亥": "吉", "子": "吉", "丑": "吉"
            },
            # 午月生（6月）
            "午": {
                "寅": "吉", "卯": "吉", "辰": "吉",
                "巳": "凶", "午": "凶", "未": "凶",
                "申": "吉", "酉": "吉", "戌": "吉",
                "亥": "大吉", "子": "大吉", "丑": "大吉"
            },
            # 未月生（7月）
            "未": {
                "寅": "吉", "卯": "吉", "辰": "吉",
                "巳": "凶", "午": "凶", "未": "凶",
                "申": "吉", "酉": "吉", "戌": "凶",
                "亥": "大吉", "子": "大吉", "丑": "吉"
            },
            # 申月生（8月）
            "申": {
                "寅": "吉", "卯": "吉", "辰": "吉",
                "巳": "大吉", "午": "大吉", "未": "大吉",
                "申": "凶", "酉": "凶", "戌": "吉",
                "亥": "凶", "子": "凶", "丑": "凶"
            },
            # 酉月生（9月）
            "酉": {
                "寅": "吉", "卯": "吉", "辰": "吉",
                "巳": "大吉", "午": "大吉", "未": "大吉",
                "申": "凶", "酉": "凶", "戌": "凶",
                "亥": "凶", "子": "凶", "丑": "凶"
            },
            # 戌月生（10月）
            "戌": {
                "寅": "吉", "卯": "吉", "辰": "吉",
                "巳": "吉", "午": "吉", "未": "吉",
                "申": "吉", "酉": "吉", "戌": "吉",
                "亥": "凶", "子": "凶", "丑": "凶"
            },
            # 亥月生（11月）
            "亥": {
                "寅": "吉", "卯": "吉", "辰": "吉",
                "巳": "大吉", "午": "大吉", "未": "大吉",
                "申": "凶", "酉": "凶", "戌": "吉",
                "亥": "大凶", "子": "大凶", "丑": "大凶"
            },
            # 子月生（12月）
            "子": {
                "寅": "吉", "卯": "吉", "辰": "吉",
                "巳": "大吉", "午": "大吉", "未": "大吉",
                "申": "凶", "酉": "凶", "戌": "大吉",
                "亥": "大凶", "子": "平", "丑": "大凶"
            },
            # 丑月生（1月）
            "丑": {
                "寅": "吉", "卯": "吉", "辰": "吉",
                "巳": "大吉", "午": "大吉", "未": "大吉",
                "申": "凶", "酉": "凶", "戌": "吉",
                "亥": "大吉", "子": "大吉", "丑": "平"
            }
        }
