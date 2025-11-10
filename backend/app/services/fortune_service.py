"""
年月日運計算サービス
lunar-pythonを使用して年運・月運・日運の干支を計算し、
ドンサゴンマトリックスで吉凶判定を行う
"""
import calendar
import json
import os
from datetime import datetime
from typing import Dict, List, Literal, Tuple

from lunar_python import Solar

# 10天干 (漢字)
HEAVENLY_STEMS = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]

# 12地支 (漢字)
EARTHLY_BRANCHES = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

# 吉凶レベル型
FortuneLevel = Literal["大吉", "小吉", "吉", "吉凶", "平", "凶", "大凶"]

# 五行要素型
FiveElement = Literal["wood", "fire", "earth", "metal", "water"]

# ドンサゴン吉凶マッピング（7段階システム対応）
DONSAGONG_FORTUNE_MAP = {
    "대길": "大吉",
    "소길": "小吉",
    "길": "吉",
    "길흉": "平",  # 7段階システムでは「吉凶」は「平」にマッピング
    "평": "平",
    "흉": "凶",
    "대흉": "大凶",
    "무": "平"  # 無は平として扱う
}


class FortuneCalculator:
    """年月日運計算エンジン"""

    def __init__(self):
        """初期化"""
        # ドンサゴン天干マトリックスを読み込む
        self.cheongan_matrix = self._load_cheongan_matrix()

    def _load_cheongan_matrix(self) -> Dict:
        """ドンサゴン天干マトリックスを読み込む"""
        matrix_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "data",
            "donsagong_cheongan_matrix.json"
        )
        with open(matrix_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data["천간_100_매트릭스"]

    def calculate_year_fortune(
        self,
        birth_year: int,
        birth_month: int,
        birth_day: int,
        day_stem: str,
        target_year: int,
    ) -> Tuple[str, str, FortuneLevel, str]:
        """
        年運を計算

        Args:
            birth_year: 生まれた年
            birth_month: 生まれた月
            birth_day: 生まれた日
            day_stem: 日干
            target_year: 対象年

        Returns:
            (年天干, 年地支, 吉凶レベル, 十神)
        """
        # 立春以降の日付を使用（四柱推命では立春が年の切り替わり）
        # target_yearの7月1日の干支を取得（確実に立春後）
        solar = Solar.fromYmd(target_year, 7, 1)
        lunar = solar.getLunar()
        eight_char = lunar.getEightChar()
        year_stem = eight_char.getYearGan()  # 年天干
        year_branch = eight_char.getYearZhi()  # 年地支

        # 吉凶判定（簡易版）
        fortune_level = self._calculate_fortune_level(day_stem, year_stem, year_branch)

        # 十神計算（簡易版）
        sipsin = self._calculate_sipsin(day_stem, year_stem)

        return year_stem, year_branch, fortune_level, sipsin

    def calculate_month_fortune(
        self,
        day_stem: str,
        target_year: int,
        target_month: int,
    ) -> Tuple[str, str, FortuneLevel, str]:
        """
        月運を計算

        Args:
            day_stem: 日干
            target_year: 対象年
            target_month: 対象月（1-12）

        Returns:
            (月天干, 月地支, 吉凶レベル, 十神)
        """
        # 節気後の日付を使用（四柱推命では節入日が月の切り替わり）
        # target_year/target_monthの15日の干支を取得（確実に節気後）
        solar = Solar.fromYmd(target_year, target_month, 15)
        lunar = solar.getLunar()
        eight_char = lunar.getEightChar()
        month_stem = eight_char.getMonthGan()  # 月天干
        month_branch = eight_char.getMonthZhi()  # 月地支

        # 吉凶判定（簡易版）
        fortune_level = self._calculate_fortune_level(day_stem, month_stem, month_branch)

        # 十神計算（簡易版）
        sipsin = self._calculate_sipsin(day_stem, month_stem)

        return month_stem, month_branch, fortune_level, sipsin

    def calculate_day_fortune(
        self,
        day_stem: str,
        target_year: int,
        target_month: int,
        target_day: int,
    ) -> Tuple[str, str, FortuneLevel, str]:
        """
        日運を計算

        Args:
            day_stem: 日干
            target_year: 対象年
            target_month: 対象月
            target_day: 対象日

        Returns:
            (日天干, 日地支, 吉凶レベル, 十神)
        """
        # 指定日の干支を取得
        solar = Solar.fromYmd(target_year, target_month, target_day)
        lunar = solar.getLunar()
        eight_char = lunar.getEightChar()
        calc_day_stem = eight_char.getDayGan()  # 日天干
        calc_day_branch = eight_char.getDayZhi()  # 日地支

        # 吉凶判定（簡易版）
        fortune_level = self._calculate_fortune_level(day_stem, calc_day_stem, calc_day_branch)

        # 十神計算（簡易版）
        sipsin = self._calculate_sipsin(day_stem, calc_day_stem)

        return calc_day_stem, calc_day_branch, fortune_level, sipsin

    def get_actual_year_pillar(
        self,
        target_year: int,
        target_month: int,
        target_day: int,
    ) -> Tuple[str, str]:
        """
        指定日時点での実際の年柱を取得（立春考慮）

        Args:
            target_year: 対象年
            target_month: 対象月
            target_day: 対象日

        Returns:
            (年天干, 年地支)
        """
        solar = Solar.fromYmd(target_year, target_month, target_day)
        lunar = solar.getLunar()
        eight_char = lunar.getEightChar()
        return eight_char.getYearGan(), eight_char.getYearZhi()

    def get_actual_month_pillar(
        self,
        target_year: int,
        target_month: int,
        target_day: int,
    ) -> Tuple[str, str]:
        """
        指定日時点での実際の月柱を取得（節気考慮）

        Args:
            target_year: 対象年
            target_month: 対象月
            target_day: 対象日

        Returns:
            (月天干, 月地支)
        """
        solar = Solar.fromYmd(target_year, target_month, target_day)
        lunar = solar.getLunar()
        eight_char = lunar.getEightChar()
        return eight_char.getMonthGan(), eight_char.getMonthZhi()

    def calculate_year_list(
        self,
        birth_year: int,
        birth_month: int,
        birth_day: int,
        day_stem: str,
        daeun_start_age: int,
    ) -> List[Dict]:
        """
        大運期間（10年分）の年運リストを計算

        Args:
            birth_year: 生まれた年
            birth_month: 生まれた月
            birth_day: 生まれた日
            day_stem: 日干
            daeun_start_age: 大運開始年齢

        Returns:
            年運情報のリスト
        """
        year_list = []
        current_year = datetime.now().year

        for i in range(10):
            age = daeun_start_age + i
            year = birth_year + age
            year_stem, year_branch, fortune_level, sipsin = self.calculate_year_fortune(
                birth_year, birth_month, birth_day, day_stem, year
            )

            year_list.append(
                {
                    "id": i + 1,
                    "year": year,
                    "age": age,
                    "yearStem": year_stem,
                    "yearBranch": year_branch,
                    "fortuneLevel": fortune_level,
                    "sipsin": sipsin,
                    "isCurrent": year == current_year,
                }
            )

        return year_list

    def calculate_month_list(
        self,
        day_stem: str,
        target_year: int,
    ) -> List[Dict]:
        """
        指定年の月運リスト（12ヶ月分）を計算

        Args:
            day_stem: 日干
            target_year: 対象年

        Returns:
            月運情報のリスト
        """
        month_list = []
        current_year = datetime.now().year
        current_month = datetime.now().month

        for month in range(1, 13):
            month_stem, month_branch, fortune_level, sipsin = self.calculate_month_fortune(
                day_stem, target_year, month
            )

            month_list.append(
                {
                    "id": month,
                    "year": target_year,
                    "month": month,
                    "monthStem": month_stem,
                    "monthBranch": month_branch,
                    "fortuneLevel": fortune_level,
                    "sipsin": sipsin,
                    "isCurrent": target_year == current_year and month == current_month,
                }
            )

        return month_list

    def calculate_day_list(
        self,
        day_stem: str,
        target_year: int,
        target_month: int,
    ) -> List[Dict]:
        """
        指定年月の日運リスト（28-31日分）を計算

        Args:
            day_stem: 日干
            target_year: 対象年
            target_month: 対象月

        Returns:
            日運情報のリスト
        """
        day_list = []
        days_in_month = calendar.monthrange(target_year, target_month)[1]
        today = datetime.now().date()

        for day in range(1, days_in_month + 1):
            calc_day_stem, calc_day_branch, fortune_level, sipsin = self.calculate_day_fortune(
                day_stem, target_year, target_month, day
            )

            is_today = (
                target_year == today.year
                and target_month == today.month
                and day == today.day
            )

            day_list.append(
                {
                    "id": day,
                    "year": target_year,
                    "month": target_month,
                    "day": day,
                    "dayStem": calc_day_stem,
                    "dayBranch": calc_day_branch,
                    "fortuneLevel": fortune_level,
                    "sipsin": sipsin,
                    "isToday": is_today,
                }
            )

        return day_list

    def _calculate_fortune_level(
        self,
        day_stem: str,
        target_stem: str,
        target_branch: str,
    ) -> FortuneLevel:
        """
        吉凶レベルを計算（ドンサゴンマトリックス使用）

        Args:
            day_stem: 日干
            target_stem: 対象天干
            target_branch: 対象地支

        Returns:
            吉凶レベル
        """
        # ドンサゴン天干マトリックスから吉凶を取得
        if day_stem in self.cheongan_matrix and target_stem in self.cheongan_matrix[day_stem]:
            donsagong_result = self.cheongan_matrix[day_stem][target_stem]["길흉"]
            # 韓国語の吉凶を日本語にマッピング
            return DONSAGONG_FORTUNE_MAP.get(donsagong_result, "平")

        # マトリックスにない場合はデフォルト
        return "平"

    def _is_合(self, stem1: str, stem2: str) -> bool:
        """天干の合（合化）判定"""
        合_pairs = [
            ("甲", "己"),
            ("乙", "庚"),
            ("丙", "辛"),
            ("丁", "壬"),
            ("戊", "癸"),
        ]
        return (stem1, stem2) in 合_pairs or (stem2, stem1) in 合_pairs

    def _calculate_sipsin(self, day_stem: str, target_stem: str) -> str:
        """
        十神を計算（簡易版）

        Args:
            day_stem: 日干
            target_stem: 対象天干

        Returns:
            十神名
        """
        # TODO: 正確な十神計算ロジックを実装
        # 現在は簡易的な実装
        if day_stem == target_stem:
            return "比肩"

        # 五行相生相剋による十神判定（簡易版）
        stem_to_element = {
            "甲": "wood",
            "乙": "wood",
            "丙": "fire",
            "丁": "fire",
            "戊": "earth",
            "己": "earth",
            "庚": "metal",
            "辛": "metal",
            "壬": "water",
            "癸": "water",
        }

        day_element = stem_to_element.get(day_stem, "")
        target_element = stem_to_element.get(target_stem, "")

        # 簡易的な十神マッピング
        if day_element == target_element:
            return "比肩" if day_stem == target_stem else "劫財"

        # デフォルト
        return "正官"

    def get_element_from_stem(self, stem: str) -> FiveElement:
        """天干から五行要素を取得"""
        element_map: Dict[str, FiveElement] = {
            "甲": "wood",
            "乙": "wood",
            "丙": "fire",
            "丁": "fire",
            "戊": "earth",
            "己": "earth",
            "庚": "metal",
            "辛": "metal",
            "壬": "water",
            "癸": "water",
        }
        return element_map.get(stem, "earth")

    def get_element_from_branch(self, branch: str) -> FiveElement:
        """地支から五行要素を取得"""
        element_map: Dict[str, FiveElement] = {
            "寅": "wood",
            "卯": "wood",
            "巳": "fire",
            "午": "fire",
            "辰": "earth",
            "戌": "earth",
            "丑": "earth",
            "未": "earth",
            "申": "metal",
            "酉": "metal",
            "亥": "water",
            "子": "water",
        }
        return element_map.get(branch, "earth")
