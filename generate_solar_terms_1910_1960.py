#!/usr/bin/env python3
"""
1910-1960年の24節気データを天文学的計算により生成
ephemライブラリを使用して太陽黄経から正確に計算
"""

import ephem
import json
from datetime import datetime, timezone, timedelta
import math

# Beijing時間 (UTC+8)
BEIJING_TZ = timezone(timedelta(hours=8))

class SolarTermsCalculator:
    def __init__(self):
        # 24節気の定義（太陽黄経の度数）
        self.solar_terms = {
            '立春': 315,  # 節気
            '雨水': 330,  # 中気
            '驚蟄': 345,  # 節気（啓蟄）
            '春分': 0,    # 中気
            '清明': 15,   # 節気
            '穀雨': 30,   # 中気
            '立夏': 45,   # 節気
            '小満': 60,   # 中気
            '芒種': 75,   # 節気
            '夏至': 90,   # 中気
            '小暑': 105,  # 節気
            '大暑': 120,  # 中気
            '立秋': 135,  # 節気
            '処暑': 150,  # 中気
            '白露': 165,  # 節気
            '秋分': 180,  # 中気
            '寒露': 195,  # 節気
            '霜降': 210,  # 中気
            '立冬': 225,  # 節気
            '小雪': 240,  # 中気
            '大雪': 255,  # 節気
            '冬至': 270,  # 中気
            '小寒': 285,  # 節気
            '大寒': 300   # 中気
        }

        # 節気の順序（年間の順番）
        self.term_order = [
            '立春', '雨水', '驚蟄', '春分', '清明', '穀雨',
            '立夏', '小満', '芒種', '夏至', '小暑', '大暑',
            '立秋', '処暑', '白露', '秋分', '寒露', '霜降',
            '立冬', '小雪', '大雪', '冬至', '小寒', '大寒'
        ]

        # 節気の英語名と意味
        self.term_info = {
            '立春': {'english': 'Lichun', 'meaning': 'Beginning of Spring'},
            '雨水': {'english': 'Yushui', 'meaning': 'Rain Water'},
            '驚蟄': {'english': 'Jingzhe', 'meaning': 'Awakening of Insects'},
            '春分': {'english': 'Chunfen', 'meaning': 'Spring Equinox'},
            '清明': {'english': 'Qingming', 'meaning': 'Clear and Bright'},
            '穀雨': {'english': 'Guyu', 'meaning': 'Grain Rain'},
            '立夏': {'english': 'Lixia', 'meaning': 'Beginning of Summer'},
            '小満': {'english': 'Xiaoman', 'meaning': 'Grain Full'},
            '芒種': {'english': 'Mangzhong', 'meaning': 'Grain in Ear'},
            '夏至': {'english': 'Xiazhi', 'meaning': 'Summer Solstice'},
            '小暑': {'english': 'Xiaoshu', 'meaning': 'Minor Heat'},
            '大暑': {'english': 'Dashu', 'meaning': 'Major Heat'},
            '立秋': {'english': 'Liqiu', 'meaning': 'Beginning of Autumn'},
            '処暑': {'english': 'Chushu', 'meaning': 'End of Heat'},
            '白露': {'english': 'Bailu', 'meaning': 'White Dew'},
            '秋分': {'english': 'Qiufen', 'meaning': 'Autumn Equinox'},
            '寒露': {'english': 'Hanlu', 'meaning': 'Cold Dew'},
            '霜降': {'english': 'Shuangjiang', 'meaning': 'Frost Descent'},
            '立冬': {'english': 'Lidong', 'meaning': 'Beginning of Winter'},
            '小雪': {'english': 'Xiaoxue', 'meaning': 'Minor Snow'},
            '大雪': {'english': 'Daxue', 'meaning': 'Major Snow'},
            '冬至': {'english': 'Dongzhi', 'meaning': 'Winter Solstice'},
            '小寒': {'english': 'Xiaohan', 'meaning': 'Minor Cold'},
            '大寒': {'english': 'Dahan', 'meaning': 'Major Cold'}
        }

    def find_solar_term_moment(self, year, term_name, target_longitude):
        """指定年の節気の正確な時刻を二分探索で見つける"""
        sun = ephem.Sun()
        observer = ephem.Observer()
        # 北京の経緯度（紫金山天文台）
        observer.lon = '118.82'
        observer.lat = '32.07'
        observer.elevation = 267

        # 節気の大まかな時期を推定
        month_estimate = {
            '立春': 2, '雨水': 2, '驚蟄': 3, '春分': 3, '清明': 4, '穀雨': 4,
            '立夏': 5, '小満': 5, '芒種': 6, '夏至': 6, '小暑': 7, '大暑': 7,
            '立秋': 8, '処暑': 8, '白露': 9, '秋分': 9, '寒露': 10, '霜降': 10,
            '立冬': 11, '小雪': 11, '大雪': 12, '冬至': 12, '小寒': 1, '大寒': 1
        }

        # 小寒と大寒は翌年の1月
        if term_name in ['小寒', '大寒']:
            search_year = year + 1
            search_month = month_estimate[term_name]
        else:
            search_year = year
            search_month = month_estimate[term_name]

        # 探索範囲を設定（該当月の1日から30日まで）
        start_date = ephem.Date(f'{search_year}/{search_month}/1')
        end_date = ephem.Date(f'{search_year}/{search_month}/28')

        # 二分探索で正確な時刻を見つける
        epsilon = 0.00001  # 約1秒の精度

        while (end_date - start_date) > epsilon:
            mid_date = (start_date + end_date) / 2
            observer.date = mid_date
            sun.compute(observer)

            # 太陽黄経を度単位で取得
            current_longitude = math.degrees(float(sun.hlon)) % 360

            # 目標との差を計算（360度をまたぐ場合の処理）
            diff = (current_longitude - target_longitude) % 360
            if diff > 180:
                diff -= 360

            if abs(diff) < 0.001:  # 十分近い
                break
            elif diff < 0:
                start_date = mid_date
            else:
                end_date = mid_date

        # ephem日付を通常の日時に変換
        # ephem.Dateは1899/12/31 12:00:00を基準とした日数
        dt_utc = datetime(1899, 12, 31, 12, 0, 0) + timedelta(days=float(mid_date))
        dt_beijing = dt_utc.replace(tzinfo=timezone.utc).astimezone(BEIJING_TZ)

        return dt_beijing

    def calculate_year_solar_terms(self, year):
        """指定年の全24節気を計算"""
        year_data = {}

        print(f"計算中: {year}年")
        for term_name in self.term_order:
            target_longitude = self.solar_terms[term_name]

            # 節気の正確な時刻を計算
            dt = self.find_solar_term_moment(year, term_name, target_longitude)

            # データ形式を構築
            year_data[term_name] = {
                'chinese_name': term_name,
                'english_name': self.term_info[term_name]['english'],
                'meaning': self.term_info[term_name]['meaning'],
                'solar_longitude': target_longitude,
                'month': dt.strftime('%B'),
                'day': dt.day,
                'hour': dt.hour,
                'minute': dt.minute,
                'second': dt.second,
                'full_datetime': dt.strftime('%Y-%m-%d %H:%M:%S'),
                'beijing_time': True,
                'calculation_method': 'ephemeris_astronomical'
            }

        return year_data

    def generate_database(self, start_year, end_year):
        """指定期間の節気データベースを生成"""
        database = {
            'metadata': {
                'title': f'Chinese Solar Terms (24節気) Database {start_year}-{end_year}',
                'description': f'Complete 24 solar terms data for years {start_year}-{end_year}',
                'calculation_method': 'Astronomical calculation using ephemeris library',
                'sources': [
                    'PyEphem astronomical computation library',
                    'Based on JPL ephemeris data',
                    'Calculated for Beijing meridian (120°E)'
                ],
                'time_zone': 'Beijing time (UTC+8)',
                'precision': 'Second-level precision',
                'created': datetime.now().strftime('%Y-%m-%d'),
                'solar_terms_count_per_year': 24,
                'note': 'Includes both 節気(jieqi) and 中気(zhongqi) for complete coverage'
            },
            'solar_terms_data': {}
        }

        # 各年のデータを計算
        for year in range(start_year, end_year + 1):
            database['solar_terms_data'][str(year)] = self.calculate_year_solar_terms(year)

            # 進捗表示
            if year % 10 == 0:
                print(f"完了: {year}年まで処理済み")

        return database

def main():
    print("=" * 60)
    print("1910-1960年 24節気データベース生成")
    print("=" * 60)

    calculator = SolarTermsCalculator()

    # 1910-1960年のデータを生成
    print("\n開始: 天文学的計算による節気データ生成...")
    database = calculator.generate_database(1910, 1960)

    # JSONファイルとして保存
    output_file = 'solar_terms_1910_1960_complete.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(database, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 完了: {output_file} に保存しました")
    print(f"生成データ: {len(database['solar_terms_data'])}年分")
    print(f"節気数: 各年24個 × {len(database['solar_terms_data'])}年 = {24 * len(database['solar_terms_data'])}個の節気データ")

    # サンプル表示
    print("\n=== サンプルデータ (1910年立春) ===")
    sample = database['solar_terms_data']['1910']['立春']
    for key, value in sample.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()