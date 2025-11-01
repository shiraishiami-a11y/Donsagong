#!/usr/bin/env python3
"""
ランダム生年月日での四柱推命・大運計算テスト
節気データベースの精度検証用
"""

import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

class RandomSajuTester:
    def __init__(self):
        # 干支の定義
        self.heavenly_stems = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
        self.earthly_branches = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

        # 月支の対応（節気ベース）
        self.month_branches = {
            '立春': '寅', '驚蟄': '卯', '清明': '辰', '立夏': '巳',
            '芒種': '午', '小暑': '未', '立秋': '申', '白露': '酉',
            '寒露': '戌', '立冬': '亥', '大雪': '子', '小寒': '丑'
        }

        # 節気データベース読み込み
        self.solar_terms_db = self.load_solar_terms_database()

    def load_solar_terms_database(self) -> Dict:
        """210年節気データベースを読み込み"""
        try:
            with open('solar_terms_1900_2109_JIEQI_ONLY.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ 節気データベース読み込みエラー: {e}")
            return {}

    def generate_random_birth_data(self, num_cases: int = 10) -> List[Dict]:
        """ランダムな生年月日データを生成"""
        birth_cases = []

        for i in range(num_cases):
            # ランダム年（1920-2090年）
            year = random.randint(1920, 2090)

            # ランダム月日
            month = random.randint(1, 12)
            day = random.randint(1, 28)  # 安全のため28日まで

            # ランダム時刻
            hour = random.randint(0, 23)
            minute = random.randint(0, 59)

            # ランダム性別
            gender = random.choice(['男', '女'])

            birth_datetime = datetime(year, month, day, hour, minute)

            birth_case = {
                'case_id': i + 1,
                'birth_datetime': birth_datetime,
                'gender': gender,
                'formatted_date': birth_datetime.strftime('%Y年%m月%d日 %H時%M分'),
                'year': year,
                'month': month,
                'day': day,
                'hour': hour,
                'minute': minute
            }

            birth_cases.append(birth_case)

        return birth_cases

    def find_current_month_branch(self, birth_date: datetime) -> Tuple[str, str]:
        """生年月日から現在の月支を節気で判定"""
        year_str = str(birth_date.year)

        if year_str not in self.solar_terms_db.get('solar_terms_data', {}):
            return '未確定', '節気データなし'

        year_solar_terms = self.solar_terms_db['solar_terms_data'][year_str]

        # 生年月日より前の最新節気を探す
        current_solar_term = None
        solar_term_date = None

        for term_name, term_data in year_solar_terms.items():
            term_datetime_str = term_data['full_datetime']
            term_datetime = datetime.strptime(term_datetime_str, '%Y-%m-%d %H:%M:%S')

            if term_datetime <= birth_date:
                if current_solar_term is None or term_datetime > solar_term_date:
                    current_solar_term = term_name
                    solar_term_date = term_datetime

        # 前年の小寒もチェック（年始生まれの場合）
        if current_solar_term is None:
            prev_year_str = str(birth_date.year - 1)
            if prev_year_str in self.solar_terms_db.get('solar_terms_data', {}):
                prev_year_terms = self.solar_terms_db['solar_terms_data'][prev_year_str]
                if '小寒' in prev_year_terms:
                    xiaozhan_data = prev_year_terms['小寒']
                    xiaozhan_datetime = datetime.strptime(xiaozhan_data['full_datetime'], '%Y-%m-%d %H:%M:%S')
                    if xiaozhan_datetime <= birth_date:
                        current_solar_term = '小寒'
                        solar_term_date = xiaozhan_datetime

        if current_solar_term and current_solar_term in self.month_branches:
            month_branch = self.month_branches[current_solar_term]
            return month_branch, f'{current_solar_term}月({solar_term_date.strftime("%m/%d %H:%M")})'

        return '未確定', '節気判定失敗'

    def calculate_year_stem_branch(self, year: int) -> str:
        """年干支を計算"""
        # 基準年: 1984年甲子
        base_year = 1984
        base_index = 0  # 甲子

        year_diff = year - base_year
        stem_index = (base_index + year_diff) % 10
        branch_index = (base_index + year_diff) % 12

        return self.heavenly_stems[stem_index] + self.earthly_branches[branch_index]

    def calculate_day_stem_branch(self, birth_date: datetime) -> str:
        """日干支を計算（簡易版）"""
        # 基準日: 1984年1月1日甲子
        base_date = datetime(1984, 1, 1)
        days_diff = (birth_date.date() - base_date.date()).days

        stem_index = days_diff % 10
        branch_index = days_diff % 12

        return self.heavenly_stems[stem_index] + self.earthly_branches[branch_index]

    def calculate_hour_stem_branch(self, birth_date: datetime, day_stem: str) -> str:
        """時干支を計算"""
        hour = birth_date.hour

        # 時支の計算
        time_branches = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
        hour_branch_index = ((hour + 1) // 2) % 12
        hour_branch = time_branches[hour_branch_index]

        # 時干の計算（日干から推算）
        day_stem_index = self.heavenly_stems.index(day_stem)

        # 12時間分のテーブル（各行は12時間分）
        hour_stem_table = [
            ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸', '甲', '乙'],  # 甲己日
            ['丙', '丁', '戊', '己', '庚', '辛', '壬', '癸', '甲', '乙', '丙', '丁'],  # 乙庚日
            ['戊', '己', '庚', '辛', '壬', '癸', '甲', '乙', '丙', '丁', '戊', '己'],  # 丙辛日
            ['庚', '辛', '壬', '癸', '甲', '乙', '丙', '丁', '戊', '己', '庚', '辛'],  # 丁壬日
            ['壬', '癸', '甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']   # 戊癸日
        ]

        table_index = day_stem_index // 2
        hour_stem = hour_stem_table[table_index][hour_branch_index]

        return hour_stem + hour_branch

    def calculate_saju(self, birth_case: Dict) -> Dict:
        """四柱推命を計算"""
        birth_date = birth_case['birth_datetime']

        # 年柱
        year_pillar = self.calculate_year_stem_branch(birth_date.year)

        # 月柱（節気ベース）
        month_branch, month_info = self.find_current_month_branch(birth_date)
        # 月干は年干から推算（簡易版）
        year_stem = year_pillar[0]
        year_stem_index = self.heavenly_stems.index(year_stem)
        month_branch_index = self.earthly_branches.index(month_branch) if month_branch != '未確定' else 0

        month_stem_table = [
            ['丙', '丁', '戊', '己', '庚', '辛', '壬', '癸', '甲', '乙', '丙', '丁'],  # 甲己年
            ['戊', '己', '庚', '辛', '壬', '癸', '甲', '乙', '丙', '丁', '戊', '己'],  # 乙庚年
            ['庚', '辛', '壬', '癸', '甲', '乙', '丙', '丁', '戊', '己', '庚', '辛'],  # 丙辛年
            ['壬', '癸', '甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'],  # 丁壬年
            ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸', '甲', '乙']   # 戊癸年
        ]

        table_index = year_stem_index // 2
        month_stem = month_stem_table[table_index][month_branch_index]
        month_pillar = month_stem + month_branch

        # 日柱
        day_pillar = self.calculate_day_stem_branch(birth_date)

        # 時柱
        hour_pillar = self.calculate_hour_stem_branch(birth_date, day_pillar[0])

        return {
            'year_pillar': year_pillar,
            'month_pillar': month_pillar,
            'day_pillar': day_pillar,
            'hour_pillar': hour_pillar,
            'month_info': month_info,
            'solar_term_used': month_info
        }

    def calculate_daeun(self, birth_case: Dict, saju: Dict) -> Dict:
        """大運を計算"""
        birth_date = birth_case['birth_datetime']
        gender = birth_case['gender']
        year_stem = saju['year_pillar'][0]

        # 陰陽判定
        is_yang_year = self.heavenly_stems.index(year_stem) % 2 == 0
        is_male = gender == '男'

        # 順逆判定
        if (is_yang_year and is_male) or (not is_yang_year and not is_male):
            direction = '順行'
        else:
            direction = '逆行'

        # 次の節気を找す
        year_str = str(birth_date.year)
        if year_str not in self.solar_terms_db.get('solar_terms_data', {}):
            return {'error': '節気データなし'}

        year_solar_terms = self.solar_terms_db['solar_terms_data'][year_str]

        # 生年月日より後の最初の節気を探す
        next_solar_term = None
        next_solar_term_date = None

        for term_name, term_data in year_solar_terms.items():
            term_datetime_str = term_data['full_datetime']
            term_datetime = datetime.strptime(term_datetime_str, '%Y-%m-%d %H:%M:%S')

            if term_datetime > birth_date:
                if next_solar_term is None or term_datetime < next_solar_term_date:
                    next_solar_term = term_name
                    next_solar_term_date = term_datetime

        # 次年の節気もチェック
        if next_solar_term is None:
            next_year_str = str(birth_date.year + 1)
            if next_year_str in self.solar_terms_db.get('solar_terms_data', {}):
                next_year_terms = self.solar_terms_db['solar_terms_data'][next_year_str]
                for term_name, term_data in next_year_terms.items():
                    term_datetime_str = term_data['full_datetime']
                    term_datetime = datetime.strptime(term_datetime_str, '%Y-%m-%d %H:%M:%S')

                    if next_solar_term is None or term_datetime < next_solar_term_date:
                        next_solar_term = term_name
                        next_solar_term_date = term_datetime
                    break  # 最初の節気のみ

        if next_solar_term_date:
            # 節入日までの日数計算
            days_to_solar_term = (next_solar_term_date - birth_date).days

            # 大運開始年齢（3日=1年法則）
            daeun_start_age = days_to_solar_term / 3

            # 大運開始日
            daeun_start_date = birth_date + timedelta(days=days_to_solar_term)

            return {
                'direction': direction,
                'next_solar_term': next_solar_term,
                'next_solar_term_date': next_solar_term_date.strftime('%Y-%m-%d %H:%M:%S'),
                'days_to_solar_term': days_to_solar_term,
                'daeun_start_age': round(daeun_start_age, 2),
                'daeun_start_date': daeun_start_date.strftime('%Y-%m-%d'),
                'calculation_basis': f'{days_to_solar_term}日 ÷ 3 = {daeun_start_age:.2f}年'
            }

        return {'error': '次の節気が見つかりません'}

    def run_test_cases(self) -> List[Dict]:
        """テストケースを実行"""
        print("=" * 80)
        print("節気データベース精度検証 - ランダム四柱推命テスト")
        print("=" * 80)

        # ランダムデータ生成
        birth_cases = self.generate_random_birth_data(10)

        results = []

        for case in birth_cases:
            print(f"\n【ケース{case['case_id']}】")
            print(f"生年月日: {case['formatted_date']}")
            print(f"性別: {case['gender']}")

            # 四柱推命計算
            saju = self.calculate_saju(case)
            print(f"四柱: {saju['year_pillar']} {saju['month_pillar']} {saju['day_pillar']} {saju['hour_pillar']}")
            print(f"月支判定: {saju['month_info']}")

            # 大運計算
            daeun = self.calculate_daeun(case, saju)
            if 'error' not in daeun:
                print(f"大運: {daeun['direction']}")
                print(f"次節気: {daeun['next_solar_term']} ({daeun['next_solar_term_date']})")
                print(f"節入まで: {daeun['days_to_solar_term']}日")
                print(f"大運開始: {daeun['daeun_start_age']}歳 ({daeun['daeun_start_date']})")
            else:
                print(f"大運計算エラー: {daeun['error']}")

            # 結果保存
            result = {
                'case_info': case,
                'saju': saju,
                'daeun': daeun
            }
            results.append(result)

        return results

def main():
    """メイン実行"""
    tester = RandomSajuTester()

    if not tester.solar_terms_db:
        print("❌ 節気データベースが読み込めません")
        return

    print(f"✅ 節気データベース読み込み完了")
    print(f"対象年範囲: {min(tester.solar_terms_db['solar_terms_data'].keys())}-{max(tester.solar_terms_db['solar_terms_data'].keys())}")

    # テスト実行
    results = tester.run_test_cases()

    # 結果保存
    output_file = 'random_saju_test_results.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)

    print(f"\n💾 テスト結果保存: {output_file}")
    print("🎯 節気データベースの実用性検証完了")

if __name__ == "__main__":
    main()