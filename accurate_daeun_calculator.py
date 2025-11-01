#!/usr/bin/env python3
"""
正確な大運起運数計算モジュール
節入日データベースを使用して3日=1年の法則で起運年齢を計算
"""

import json
import os
from datetime import datetime, timezone, timedelta
from typing import Tuple, Dict, Optional

# タイムゾーン定義
KST = timezone(timedelta(hours=9))

class AccurateDaeunCalculator:
    """正確な大運計算クラス"""
    
    def __init__(self, database_path='solar_terms_1900-1910_database.json'):
        """
        初期化
        
        Args:
            database_path: 節入日データベースのパス
        """
        self.database = self._load_database(database_path)
        
        # 節名と月の対応（実際の月）
        self.jeol_months = {
            '立春': 2,   # 2月（寅月）
            '驚蟄': 3,   # 3月（卯月）
            '清明': 4,   # 4月（辰月）
            '立夏': 5,   # 5月（巳月）
            '芒種': 6,   # 6月（午月）
            '小暑': 7,   # 7月（未月）
            '立秋': 8,   # 8月（申月）
            '白露': 9,   # 9月（酉月）
            '寒露': 10,  # 10月（戌月）
            '立冬': 11,  # 11月（亥月）
            '大雪': 12,  # 12月（子月）
            '小寒': 1,   # 1月（丑月）
        }
        
    def _load_database(self, database_path):
        """節入日データベースを読み込む"""
        full_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            database_path
        )
        
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"節入日データベースが見つかりません: {full_path}")
        
        with open(full_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def calculate_starting_age(self, birth_datetime, gender, year_stem):
        """
        正確な起運年齢を計算
        
        Args:
            birth_datetime: 生年月日時刻（datetime）
            gender: 性別（'male' or 'female'）
            year_stem: 年干（陽干か陰干を判定用）
        
        Returns:
            起運年齢（歳）
        """
        print(f"\n=== 大運起運年齢計算過程 ===")
        print(f"生年月日時: {birth_datetime.strftime('%Y/%m/%d %H:%M')} KST")
        print(f"性別: {gender}")
        print(f"年干: {year_stem}")
        
        # 順逆行判断
        stems = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
        year_index = stems.index(year_stem) if year_stem in stems else 0
        is_yang = (year_index % 2 == 0)  # 偶数が陽干
        
        print(f"年干インデックス: {year_index} ({'陽干' if is_yang else '陰干'})")
        
        # 順行・逆行の判定
        if (is_yang and gender == 'male') or (not is_yang and gender == 'female'):
            direction = 'forward'  # 順行
        else:
            direction = 'backward'  # 逆行
        
        print(f"大運方向: {direction} ({'順行' if direction == 'forward' else '逆行'})")
        
        # 節入日を取得
        if direction == 'forward':
            jeolip_date = self._get_next_jeol(birth_datetime)
            target_type = "次の節"
        else:
            jeolip_date = self._get_previous_jeol(birth_datetime)
            target_type = "前の節"
        
        if jeolip_date is None:
            print(f"⚠️ {target_type}入日データが見つかりません")
            return 5  # デフォルト値
        
        print(f"{target_type}入日: {jeolip_date.strftime('%Y/%m/%d %H:%M:%S')} KST")
        
        # 日数差を計算
        time_diff = abs(jeolip_date - birth_datetime)
        days_diff = time_diff.days + (time_diff.seconds / 86400)  # 小数日まで計算
        
        print(f"時間差: {time_diff}")
        print(f"日数差: {days_diff:.6f}日")
        
        # 3日 = 1年の法則（小数部分も含む精密計算）
        precise_years = days_diff / 3
        starting_age_integer = int(precise_years)
        
        print(f"3日=1年法則適用: {days_diff:.6f} ÷ 3 = {precise_years:.6f}")
        print(f"起運年齢（整数部）: {starting_age_integer}歳")
        print(f"小数部分: {precise_years - starting_age_integer:.6f}年")
        
        # 最小0歳、最大10歳に制限（整数部のみ）
        final_age_integer = max(0, min(starting_age_integer, 10))
        
        if final_age_integer != starting_age_integer:
            print(f"制限適用後: {final_age_integer}歳")
        
        print(f"=== 最終起運年齢: {final_age_integer}歳 ===")
        
        # 大運開始日計算
        # 制限が適用された場合の処理
        if final_age_integer != starting_age_integer and final_age_integer == 10:
            # 10歳制限の場合：単純に生年月日 + 10年
            accurate_start_date = birth_datetime.replace(year=birth_datetime.year + 10)
            fractional_years = 0
            fractional_days = 0
        elif final_age_integer != starting_age_integer and final_age_integer == 0:
            # 0歳制限の場合：実際の小数部分を使用
            fractional_days = precise_years * 365.25
            accurate_start_date = birth_datetime + timedelta(days=fractional_days)
            fractional_years = precise_years
        else:
            # 制限なしの場合：通常計算
            fractional_years = precise_years - final_age_integer
            fractional_days = fractional_years * 365.25
            
            if final_age_integer == 0:
                # 0歳で制限なしの場合
                fractional_days = precise_years * 365.25
                accurate_start_date = birth_datetime + timedelta(days=fractional_days)
            else:
                # 通常の場合
                base_start_date = birth_datetime.replace(year=birth_datetime.year + final_age_integer)
                accurate_start_date = base_start_date + timedelta(days=fractional_days)
        
        print(f"起運年齢（整数部）: {final_age_integer}年")
        print(f"小数部分: {fractional_years:.6f}年 = {fractional_days:.1f}日")
        if final_age_integer > 0 and 'base_start_date' in locals():
            print(f"基準開始日: {base_start_date.strftime('%Y年%m月%d日')}")
        print(f"精密大運開始日: {accurate_start_date.strftime('%Y年%m月%d日 %H:%M')}")
        
        print("=" * 40 + "\n")
        
        return {
            'starting_age': final_age_integer,
            'direction': direction,
            'jeol_date': jeolip_date,
            'jeol_name': self._get_jeol_name_from_date(jeolip_date),
            'days_diff': days_diff,
            'precise_start': accurate_start_date
        }
    
    def _get_next_jeol(self, birth_datetime):
        """次の節入日を取得"""
        year = birth_datetime.year
        month = birth_datetime.month
        
        # 現在の年のデータを確認
        if str(year) not in self.database.get('solar_terms_data', {}):
            return None
        
        year_data = self.database['solar_terms_data'][str(year)]
        
        # すべての節入日を日付順にソート
        jeol_dates = []
        for jeol_name, jeol_data in year_data.items():
            # データベースの日付を修正（monthとdayが逆の可能性）
            actual_month = self.jeol_months.get(jeol_name)
            if actual_month:
                # 正しい月で日時を作成
                try:
                    if actual_month == 1:  # 小寒は翌年1月
                        dt = datetime(
                            year + 1, actual_month, jeol_data['day'],
                            jeol_data['hour'], jeol_data['minute'], jeol_data['second'],
                            tzinfo=KST
                        )
                    else:
                        dt = datetime(
                            year, actual_month, jeol_data['day'],
                            jeol_data['hour'], jeol_data['minute'], jeol_data['second'],
                            tzinfo=KST
                        )
                    jeol_dates.append((jeol_name, dt))
                except:
                    # 日付作成エラーの場合はスキップ
                    continue
        
        # 日付順にソート
        jeol_dates.sort(key=lambda x: x[1])
        
        # 生年月日より後の最初の節を探す
        for jeol_name, jeol_dt in jeol_dates:
            if jeol_dt > birth_datetime:
                return jeol_dt
        
        # 今年の節がすべて過ぎている場合、翌年の立春を返す
        next_year = year + 1
        if str(next_year) in self.database.get('solar_terms_data', {}) and '立春' in self.database['solar_terms_data'][str(next_year)]:
            lichun_data = self.database['solar_terms_data'][str(next_year)]['立春']
            try:
                return datetime(
                    next_year, 2, lichun_data['day'],
                    lichun_data['hour'], lichun_data['minute'], lichun_data['second'],
                    tzinfo=KST
                )
            except:
                pass
        
        return None
    
    def _get_previous_jeol(self, birth_datetime):
        """前の節入日を取得"""
        year = birth_datetime.year
        
        # 現在の年のデータを確認
        if str(year) not in self.database.get('solar_terms_data', {}):
            return None
        
        year_data = self.database['solar_terms_data'][str(year)]
        
        # すべての節入日を日付順にソート
        jeol_dates = []
        for jeol_name, jeol_data in year_data.items():
            actual_month = self.jeol_months.get(jeol_name)
            if actual_month:
                try:
                    if actual_month == 1:  # 小寒は前年として扱う
                        dt = datetime(
                            year, actual_month, jeol_data['day'],
                            jeol_data['hour'], jeol_data['minute'], jeol_data['second'],
                            tzinfo=KST
                        )
                    else:
                        dt = datetime(
                            year, actual_month, jeol_data['day'],
                            jeol_data['hour'], jeol_data['minute'], jeol_data['second'],
                            tzinfo=KST
                        )
                    jeol_dates.append((jeol_name, dt))
                except:
                    continue
        
        # 日付順にソート（逆順）
        jeol_dates.sort(key=lambda x: x[1], reverse=True)
        
        # 生年月日より前の最初の節を探す
        for jeol_name, jeol_dt in jeol_dates:
            if jeol_dt < birth_datetime:
                return jeol_dt
        
        # 今年の節がすべて後の場合、前年の大雪を返す
        prev_year = year - 1
        if str(prev_year) in self.database.get('solar_terms_data', {}) and '大雪' in self.database['solar_terms_data'][str(prev_year)]:
            daeseol_data = self.database['solar_terms_data'][str(prev_year)]['大雪']
            try:
                return datetime(
                    prev_year, 12, daeseol_data['day'],
                    daeseol_data['hour'], daeseol_data['minute'], daeseol_data['second'],
                    tzinfo=KST
                )
            except:
                pass
        
        return None
    
    def _get_jeol_name_from_date(self, jeol_date):
        """日付から節名を取得"""
        if jeol_date is None:
            return "不明"
        
        year = jeol_date.year
        month = jeol_date.month
        
        # 月から節名を推定
        month_to_jeol = {
            2: "立春",
            3: "驚蟄", 
            4: "清明",
            5: "立夏",
            6: "芒種",
            7: "小暑",
            8: "立秋",
            9: "白露",
            10: "寒露",
            11: "立冬",
            12: "大雪",
            1: "小寒"
        }
        
        return month_to_jeol.get(month, "不明")


# テスト用
if __name__ == "__main__":
    calculator = AccurateDaeunCalculator()
    
    # テストケース
    test_cases = [
        {
            'birth': datetime(1986, 5, 26, 5, 0, tzinfo=KST),
            'gender': 'male',
            'year_stem': '丙'
        },
        {
            'birth': datetime(1986, 12, 20, 0, 0, tzinfo=KST),
            'gender': 'female', 
            'year_stem': '丙'
        }
    ]
    
    for case in test_cases:
        starting_age = calculator.calculate_starting_age(
            case['birth'], 
            case['gender'],
            case['year_stem']
        )
        
        print(f"生年月日: {case['birth'].strftime('%Y/%m/%d %H時')}")
        print(f"性別: {case['gender']}")
        print(f"年干: {case['year_stem']}")
        print(f"起運年齢: {starting_age}歳")
        print("-" * 40)