"""
命式計算サービス
lunar-python + 210年節気DBを使用した正確な四柱推命計算
"""
import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from lunar_python import EightChar, Lunar, Solar
from .fortune_analyzer import FortuneAnalyzer

# 韓国標準時 (UTC+9)
KST = timezone(timedelta(hours=9))

# 10天干 (漢字)
HEAVENLY_STEMS = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]

# 12地支 (漢字)
EARTHLY_BRANCHES = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

# 吉凶レベルマッピング
FORTUNE_LEVEL_MAP = {1: "大凶", 2: "凶", 3: "平", 4: "吉", 5: "大吉"}

FORTUNE_LEVEL_REVERSE_MAP = {"大凶": 1, "凶": 2, "平": 3, "吉": 4, "大吉": 5}


class SolarTermsDB:
    """210年節気データベースローダー"""

    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            # プロジェクトルートの210年節気DBを読み込み
            project_root = Path(__file__).parent.parent.parent.parent
            db_path = project_root / "solar_terms_1900_2109_JIEQI_ONLY.json"

        self.db_path = Path(db_path)
        self.data: Dict = {}
        self._load_db()

    def _load_db(self):
        """210年節気DBを読み込み"""
        try:
            with open(self.db_path, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
                # データ構造: {"solar_terms_data": {"1900": {...}, "1901": {...}}}
                self.data = raw_data.get("solar_terms_data", {})
                print(f"✅ 210年節気DB読み込み成功: {len(self.data)}年分")
        except FileNotFoundError:
            raise FileNotFoundError(f"210年節気DBが見つかりません: {self.db_path}")
        except Exception as e:
            raise Exception(f"210年節気DB読み込みエラー: {e}")

    def get_jieqi_datetime(self, year: int, jieqi_name: str) -> datetime:
        """
        指定された年の節気の正確な日時を取得

        Args:
            year: 西暦年（1900-2109）
            jieqi_name: 節気名（例: "立春", "驚蟄"）

        Returns:
            節気の正確な日時（KST）
        """
        if not (1900 <= year <= 2109):
            raise ValueError(f"対応範囲外の年: {year} (1900-2109年のみ対応)")

        year_data = self.data.get(str(year))
        if not year_data:
            raise ValueError(f"節気データなし: {year}年")

        jieqi_data = year_data.get(jieqi_name)
        if not jieqi_data:
            raise ValueError(f"節気データなし: {year}年 {jieqi_name}")

        # 節気データから日時を構築
        # 注意: DBは北京時間（UTC+8）なので、KSTに変換（+1時間）
        dt = datetime(
            year,
            jieqi_data["month"],
            jieqi_data["day"],
            jieqi_data["hour"],
            jieqi_data["minute"],
            jieqi_data.get("second", 0),
            tzinfo=timezone(timedelta(hours=8)),  # 北京時間
        )

        # KSTに変換
        return dt.astimezone(KST)

    def get_next_jieqi(self, dt: datetime) -> Tuple[str, datetime]:
        """
        指定日時の次の節気を取得

        Args:
            dt: 基準日時（KST）

        Returns:
            (節気名, 節気日時)
        """
        year = dt.year

        # 節気リスト（月節のみ、12個）
        jieqi_names = [
            "立春",
            "驚蟄",
            "清明",
            "立夏",
            "芒種",
            "小暑",
            "立秋",
            "白露",
            "寒露",
            "立冬",
            "大雪",
            "小寒",
        ]

        # 今年の節気をチェック
        for jieqi_name in jieqi_names:
            try:
                jieqi_dt = self.get_jieqi_datetime(year, jieqi_name)
                if jieqi_dt > dt:
                    return jieqi_name, jieqi_dt
            except ValueError:
                continue

        # 今年の節気が全て過ぎていたら、来年の立春
        try:
            next_year_lichun = self.get_jieqi_datetime(year + 1, "立春")
            return "立春", next_year_lichun
        except ValueError:
            raise ValueError(f"次の節気が見つかりません: {dt}")

    def get_previous_jieqi(self, dt: datetime) -> Tuple[str, datetime]:
        """
        指定日時の前の節気を取得

        Args:
            dt: 基準日時（KST）

        Returns:
            (節気名, 節気日時)
        """
        year = dt.year

        # 節気リスト（逆順）
        jieqi_names = [
            "小寒",
            "大雪",
            "立冬",
            "寒露",
            "白露",
            "立秋",
            "小暑",
            "芒種",
            "立夏",
            "清明",
            "驚蟄",
            "立春",
        ]

        # 今年の節気をチェック（逆順）
        for jieqi_name in jieqi_names:
            try:
                jieqi_dt = self.get_jieqi_datetime(year, jieqi_name)
                if jieqi_dt < dt:
                    return jieqi_name, jieqi_dt
            except ValueError:
                continue

        # 今年の節気が全て後なら、去年の小寒
        try:
            prev_year_xiaohan = self.get_jieqi_datetime(year - 1, "小寒")
            return "小寒", prev_year_xiaohan
        except ValueError:
            raise ValueError(f"前の節気が見つかりません: {dt}")


class SajuCalculator:
    """命式計算エンジン"""

    def __init__(self, solar_terms_db: Optional[SolarTermsDB] = None):
        self.solar_terms_db = solar_terms_db or SolarTermsDB()
        self.fortune_analyzer = FortuneAnalyzer()

    def calculate(self, birth_datetime: datetime, gender: str, name: Optional[str] = None) -> Dict:
        """
        命式計算のメインメソッド

        Args:
            birth_datetime: 生年月日時（ISO 8601形式、KST推奨）
            gender: 性別（'male' or 'female'）
            name: 名前（オプション）

        Returns:
            命式データ（辞書形式）
        """
        # 1. 入力バリデーション
        self._validate_input(birth_datetime, gender)

        # 2. KSTに変換
        kst_time = self._to_kst(birth_datetime)

        # 3. lunar-pythonで四柱計算
        solar = Solar.fromYmdHms(
            kst_time.year,
            kst_time.month,
            kst_time.day,
            kst_time.hour,
            kst_time.minute,
            kst_time.second,
        )
        lunar = solar.getLunar()
        eight_char = lunar.getEightChar()

        # 4. 四柱データ取得
        year_stem = eight_char.getYearGan()
        year_branch = eight_char.getYearZhi()
        month_stem = eight_char.getMonthGan()
        month_branch = eight_char.getMonthZhi()
        day_stem = eight_char.getDayGan()
        day_branch = eight_char.getDayZhi()
        hour_stem = eight_char.getTimeGan()
        hour_branch = eight_char.getTimeZhi()

        # 5. 大運計算（吉凶判定を含む）
        daeun_info = self._calculate_daeun(
            eight_char, kst_time, gender,
            day_stem, day_branch, month_branch, hour_stem, hour_branch
        )

        # 6. 吉凶レベル判定（原局全体）
        fortune_level = self._calculate_fortune_level(
            year_stem, year_branch, month_stem, month_branch, day_stem, day_branch, hour_stem, hour_branch
        )

        # 7. レスポンス構築
        return {
            "name": name,
            "birthDatetime": kst_time.isoformat(),
            "gender": gender,
            "yearStem": year_stem,
            "yearBranch": year_branch,
            "monthStem": month_stem,
            "monthBranch": month_branch,
            "dayStem": day_stem,
            "dayBranch": day_branch,
            "hourStem": hour_stem,
            "hourBranch": hour_branch,
            "daeunNumber": daeun_info["daeunNumber"],
            "isForward": daeun_info["isForward"],
            "afterBirthYears": daeun_info["afterBirthYears"],
            "afterBirthMonths": daeun_info["afterBirthMonths"],
            "afterBirthDays": daeun_info["afterBirthDays"],
            "firstDaeunDate": daeun_info["firstDaeunDate"],
            "daeunList": daeun_info["daeunList"],
            "fortuneLevel": fortune_level,
            "createdAt": datetime.now(KST).isoformat(),
        }

    def _validate_input(self, birth_datetime: datetime, gender: str):
        """入力バリデーション"""
        # 年範囲チェック
        year = birth_datetime.year
        if not (1900 <= year <= 2109):
            raise ValueError(f"対応範囲外の日付です（1900-2109年のみ）: {year}年")

        # 性別チェック
        if gender not in ["male", "female"]:
            raise ValueError("genderは'male'または'female'である必要があります")

    def _to_kst(self, dt: datetime) -> datetime:
        """KST（韓国標準時 UTC+9）に変換"""
        if dt.tzinfo is None:
            # naive datetimeはKSTと仮定
            return dt.replace(tzinfo=KST)
        return dt.astimezone(KST)

    def _calculate_daeun(
        self,
        eight_char: EightChar,
        birth_datetime: datetime,
        gender: str,
        day_stem: str,
        day_branch: str,
        month_branch: str,
        hour_stem: str,
        hour_branch: str
    ) -> Dict:
        """
        大運計算（吉凶判定を含む）

        Args:
            eight_char: lunar-pythonのEightCharオブジェクト
            birth_datetime: 生年月日時（KST）
            gender: 性別（'male' or 'female'）
            day_stem: 日干
            day_branch: 日支
            month_branch: 月地支（調候判定用）
            hour_stem: 時干
            hour_branch: 時支

        Returns:
            大運情報
        """
        # lunar-pythonで大運計算
        # 重要: lunar-pythonの性別コード（実際の動作）
        #   getYun(0) = 女性
        #   getYun(1) = 男性
        gender_code = 1 if gender == "male" else 0
        yun = eight_char.getYun(gender_code)

        # 順行/逆行
        is_forward = yun.isForward()

        # 大運開始年齢計算（生後年数）
        start_year = yun.getStartYear()
        start_month = yun.getStartMonth()
        start_day = yun.getStartDay()

        # 第一大運開始日
        first_daeun_date_obj = yun.getStartSolar()
        first_daeun_date = f"{first_daeun_date_obj.getYear()}-{first_daeun_date_obj.getMonth():02d}-{first_daeun_date_obj.getDay():02d}"

        # 大運リスト取得
        da_yun_arr = yun.getDaYun()

        daeun_list = []

        # 大運数（start_year）から始まる大運を生成
        # lunar-pythonのgetStartAge()は0, 10, 20...を返すが、
        # 実際の開始年齢は大運数（start_year）で決まる
        #
        # 重要: lunar-pythonのgetDaYun()は次の順序で大運を返す:
        #   - da_yun_arr[0]: 現在の柱（出生時）= 干支なし
        #   - da_yun_arr[1]: 第1大運（10年後）
        #   - da_yun_arr[2]: 第2大運（20年後）
        #   ...
        # したがって、da_yun_arr[1]から開始して、年齢はstart_yearから始める
        for idx in range(10):  # 最大10個
            # lunar-python配列のインデックスは1から開始（0はスキップ）
            da_yun = da_yun_arr[idx + 1] if (idx + 1) < len(da_yun_arr) else None

            if da_yun is None:
                break

            # 年齢範囲計算
            start_age = start_year + idx * 10
            end_age = start_age + 9

            # 干支取得
            gan_zhi = da_yun.getGanZhi()
            daeun_stem = gan_zhi[0] if len(gan_zhi) >= 1 else ""
            daeun_branch = gan_zhi[1] if len(gan_zhi) >= 2 else ""

            # 吉凶レベル判定（ドンサゴン分析）
            fortune_level_str = self.fortune_analyzer.analyze_daeun_fortune(
                day_stem=day_stem,
                day_branch=day_branch,
                hour_stem=hour_stem,
                hour_branch=hour_branch,
                month_branch=month_branch,
                daeun_stem=daeun_stem,
                daeun_branch=daeun_branch
            )

            # 現在の大運かどうか判定
            current_age = self._calculate_current_age(birth_datetime)
            is_current = start_age <= current_age <= end_age

            daeun_list.append(
                {
                    "id": idx + 1,  # 1から開始するID
                    "sajuId": "",  # エンドポイントで設定
                    "startAge": start_age,
                    "endAge": end_age,
                    "daeunStem": daeun_stem,
                    "daeunBranch": daeun_branch,
                    "fortuneLevel": fortune_level_str,
                    "sipsin": None,  # 将来実装
                    "isCurrent": is_current,
                }
            )

        return {
            "daeunNumber": start_year,
            "isForward": is_forward,
            "afterBirthYears": start_year,
            "afterBirthMonths": start_month,
            "afterBirthDays": start_day,
            "firstDaeunDate": first_daeun_date,
            "daeunList": daeun_list,
        }

    def _calculate_current_age(self, birth_datetime: datetime) -> int:
        """現在の年齢を計算"""
        now = datetime.now(KST)
        age = now.year - birth_datetime.year
        if (now.month, now.day) < (birth_datetime.month, birth_datetime.day):
            age -= 1
        return max(age, 0)

    def _calculate_fortune_level(
        self,
        year_stem: str,
        year_branch: str,
        month_stem: str,
        month_branch: str,
        day_stem: str,
        day_branch: str,
        hour_stem: str,
        hour_branch: str,
    ) -> str:
        """
        吉凶レベル判定（暫定実装）

        将来的にドンサゴンマトリックスを使用して判定

        Returns:
            吉凶レベル（'大吉', '吉', '平', '凶', '大凶'）
        """
        # 暫定: 全て「平」を返す
        # TODO: ドンサゴンマトリックス統合
        return "平"
