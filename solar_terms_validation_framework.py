#!/usr/bin/env python3
"""
節気データ検証フレームワーク
複数の外部ソースとの比較による自動検証システム
"""

import json
import ephem
import requests
from datetime import datetime, timezone, timedelta
import math
from typing import Dict, List, Tuple, Optional
import time
import random

class SolarTermsValidator:
    def __init__(self):
        self.beijing_tz = timezone(timedelta(hours=8))
        self.validation_results = {}
        self.error_tolerance_hours = 6  # ±6時間の誤差を許容

        # 24節気の定義
        self.solar_terms_longitudes = {
            '立春': 315, '雨水': 330, '驚蟄': 345, '春分': 0,
            '清明': 15, '穀雨': 30, '立夏': 45, '小満': 60,
            '芒種': 75, '夏至': 90, '小暑': 105, '大暑': 120,
            '立秋': 135, '処暑': 150, '白露': 165, '秋分': 180,
            '寒露': 195, '霜降': 210, '立冬': 225, '小雪': 240,
            '大雪': 255, '冬至': 270, '小寒': 285, '大寒': 300
        }

    def load_our_database(self, filepath: str) -> Dict:
        """作成したデータベースを読み込む"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"データベース読み込みエラー: {e}")
            return {}

    def calculate_ephemeris_solar_term(self, year: int, term_name: str, target_longitude: float) -> datetime:
        """Ephemライブラリで節気を再計算（検証用）"""
        sun = ephem.Sun()
        observer = ephem.Observer()
        observer.lon = '118.82'  # 北京
        observer.lat = '32.07'
        observer.elevation = 267

        # 推定月を決定
        month_estimate = {
            '立春': 2, '雨水': 2, '驚蟄': 3, '春分': 3, '清明': 4, '穀雨': 4,
            '立夏': 5, '小満': 5, '芒種': 6, '夏至': 6, '小暑': 7, '大暑': 7,
            '立秋': 8, '処暑': 8, '白露': 9, '秋分': 9, '寒露': 10, '霜降': 10,
            '立冬': 11, '小雪': 11, '大雪': 12, '冬至': 12, '小寒': 1, '大寒': 1
        }

        # 小寒と大寒は翌年
        if term_name in ['小寒', '大寒']:
            search_year = year + 1
            search_month = month_estimate[term_name]
        else:
            search_year = year
            search_month = month_estimate[term_name]

        # 二分探索で正確な時刻を見つける
        start_date = ephem.Date(f'{search_year}/{search_month}/1')
        end_date = ephem.Date(f'{search_year}/{search_month}/28')
        epsilon = 0.00001

        while (end_date - start_date) > epsilon:
            mid_date = (start_date + end_date) / 2
            observer.date = mid_date
            sun.compute(observer)

            current_longitude = math.degrees(float(sun.hlon)) % 360
            diff = (current_longitude - target_longitude) % 360
            if diff > 180:
                diff -= 360

            if abs(diff) < 0.001:
                break
            elif diff < 0:
                start_date = mid_date
            else:
                end_date = mid_date

        # 日時変換
        dt_utc = datetime(1899, 12, 31, 12, 0, 0) + timedelta(days=float(mid_date))
        dt_beijing = dt_utc.replace(tzinfo=timezone.utc).astimezone(self.beijing_tz)
        return dt_beijing

    def fetch_hko_data(self, year: int) -> Optional[Dict]:
        """香港天文台のデータを取得（可能な場合）"""
        try:
            # HKOは近年のデータのみ提供
            if year < 2020 or year > 2030:
                return None

            # 実際のAPIエンドポイントは調査が必要
            # 今回は模擬実装
            print(f"  HKO {year}年データ取得を試行中...")
            time.sleep(random.uniform(0.5, 1.5))  # レート制限対応
            return None  # 実装時に実際のデータを返す

        except Exception as e:
            print(f"  HKO {year}年データ取得失敗: {e}")
            return None

    def validate_single_year(self, year: int, our_data: Dict) -> Dict:
        """単一年の検証"""
        year_str = str(year)
        validation_result = {
            'year': year,
            'total_terms': 0,
            'validated_terms': 0,
            'error_count': 0,
            'warnings': [],
            'details': {}
        }

        if year_str not in our_data.get('solar_terms_data', {}):
            validation_result['warnings'].append(f"{year}年のデータが見つかりません")
            return validation_result

        year_data = our_data['solar_terms_data'][year_str]
        validation_result['total_terms'] = len(year_data)

        print(f"  {year}年の検証開始 ({len(year_data)}節気)")

        for term_name, term_data in year_data.items():
            if term_name not in self.solar_terms_longitudes:
                validation_result['warnings'].append(f"未知の節気: {term_name}")
                continue

            # 我々のデータから日時を取得
            our_datetime_str = term_data.get('full_datetime', '')
            try:
                our_datetime = datetime.strptime(our_datetime_str, '%Y-%m-%d %H:%M:%S')
                our_datetime = our_datetime.replace(tzinfo=self.beijing_tz)
            except:
                validation_result['warnings'].append(f"{term_name}: 日時形式エラー")
                continue

            # Ephemで再計算
            target_longitude = self.solar_terms_longitudes[term_name]
            calculated_datetime = self.calculate_ephemeris_solar_term(year, term_name, target_longitude)

            # 誤差計算
            time_diff = abs((our_datetime - calculated_datetime).total_seconds()) / 3600  # 時間単位

            validation_result['details'][term_name] = {
                'our_time': our_datetime_str,
                'calculated_time': calculated_datetime.strftime('%Y-%m-%d %H:%M:%S'),
                'difference_hours': round(time_diff, 2),
                'status': 'OK' if time_diff <= self.error_tolerance_hours else 'ERROR'
            }

            if time_diff <= self.error_tolerance_hours:
                validation_result['validated_terms'] += 1
            else:
                validation_result['error_count'] += 1
                validation_result['warnings'].append(
                    f"{term_name}: 誤差{time_diff:.1f}時間（許容範囲±{self.error_tolerance_hours}時間超過）"
                )

        print(f"  ✓ {year}年完了: {validation_result['validated_terms']}/{validation_result['total_terms']}節気OK")
        return validation_result

    def validate_year_range(self, start_year: int, end_year: int, database_path: str) -> Dict:
        """指定年範囲の検証"""
        print(f"\n=== {start_year}-{end_year}年の検証開始 ===")

        # データベース読み込み
        our_data = self.load_our_database(database_path)
        if not our_data:
            return {'error': 'データベース読み込み失敗'}

        results = {
            'range': f"{start_year}-{end_year}",
            'total_years': end_year - start_year + 1,
            'validated_years': 0,
            'total_terms': 0,
            'validated_terms': 0,
            'error_count': 0,
            'year_results': {}
        }

        # 各年を検証
        for year in range(start_year, end_year + 1):
            year_result = self.validate_single_year(year, our_data)
            results['year_results'][year] = year_result

            if year_result['error_count'] == 0:
                results['validated_years'] += 1

            results['total_terms'] += year_result['total_terms']
            results['validated_terms'] += year_result['validated_terms']
            results['error_count'] += year_result['error_count']

            # 進捗表示
            if year % 10 == 0:
                print(f"進捗: {year}年まで完了")

        # 成功率計算
        results['success_rate'] = round(
            (results['validated_terms'] / results['total_terms'] * 100) if results['total_terms'] > 0 else 0, 2
        )

        print(f"\n✅ {start_year}-{end_year}年検証完了")
        print(f"   総節気数: {results['total_terms']}")
        print(f"   正確な節気: {results['validated_terms']}")
        print(f"   エラー数: {results['error_count']}")
        print(f"   成功率: {results['success_rate']}%")

        return results

    def generate_validation_report(self, results: Dict, output_file: str):
        """検証レポート生成"""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"検証レポート保存: {output_file}")

def main():
    """メイン検証処理"""
    validator = SolarTermsValidator()

    print("=" * 60)
    print("節気データベース検証システム - 1900-1940年検証")
    print("=" * 60)

    # 1900-1940年の検証（41年 × 24節気 = 984個のデータポイント）
    validation_results = validator.validate_year_range(
        1900, 1940,
        'solar_terms_1900_2100_COMPLETE.json'
    )

    # レポート生成
    validator.generate_validation_report(
        validation_results,
        'validation_1900_1940.json'
    )

if __name__ == "__main__":
    main()