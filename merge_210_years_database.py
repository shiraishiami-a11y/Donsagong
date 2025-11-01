#!/usr/bin/env python3
"""
210年節気データベース統合スクリプト
既存の solar_terms_1900_2100_COMPLETE.json (201年分) と
新規の solar_terms_2101_2109_complete.json (9年分) を統合し
solar_terms_1900_2109_COMPLETE.json (210年分) を作成
"""

import json
from datetime import datetime

def merge_solar_terms_databases():
    """2つの節気データベースを統合"""

    print("=" * 70)
    print("210年節気データベース統合処理")
    print("1900-2100年(201年分) + 2101-2109年(9年分) = 1900-2109年(210年分)")
    print("=" * 70)

    # 既存の201年分データを読み込み
    print("\n1. 既存データ読み込み: solar_terms_1900_2100_COMPLETE.json")
    try:
        with open('solar_terms_1900_2100_COMPLETE.json', 'r', encoding='utf-8') as f:
            data_1900_2100 = json.load(f)
        print(f"   ✅ {len(data_1900_2100['solar_terms_data'])}年分のデータを読み込み")
    except FileNotFoundError:
        print("   ❌ エラー: solar_terms_1900_2100_COMPLETE.json が見つかりません")
        return False
    except json.JSONDecodeError as e:
        print(f"   ❌ JSONエラー: {e}")
        return False

    # 新規の9年分データを読み込み
    print("\n2. 新規データ読み込み: solar_terms_2101_2109_complete.json")
    try:
        with open('solar_terms_2101_2109_complete.json', 'r', encoding='utf-8') as f:
            data_2101_2109 = json.load(f)
        print(f"   ✅ {len(data_2101_2109['solar_terms_data'])}年分のデータを読み込み")
    except FileNotFoundError:
        print("   ❌ エラー: solar_terms_2101_2109_complete.json が見つかりません")
        return False
    except json.JSONDecodeError as e:
        print(f"   ❌ JSONエラー: {e}")
        return False

    # データ整合性チェック
    print("\n3. データ整合性チェック")
    base_years = len(data_1900_2100['solar_terms_data'])
    additional_years = len(data_2101_2109['solar_terms_data'])

    if base_years != 201:
        print(f"   ⚠️  警告: 基本データが期待される201年ではありません ({base_years}年)")
    if additional_years != 9:
        print(f"   ⚠️  警告: 追加データが期待される9年ではありません ({additional_years}年)")

    # 重複年チェック
    base_years_set = set(data_1900_2100['solar_terms_data'].keys())
    additional_years_set = set(data_2101_2109['solar_terms_data'].keys())
    overlap = base_years_set.intersection(additional_years_set)

    if overlap:
        print(f"   ⚠️  警告: データに重複する年があります: {sorted(overlap)}")
    else:
        print("   ✅ 年データに重複はありません")

    # 統合データベース作成
    print("\n4. 統合データベース作成")
    merged_database = {
        'metadata': {
            'title': 'Chinese Solar Terms (24節気) Database 1900-2109',
            'description': 'Complete 24 solar terms data for 210 years (1900-2109) - Final complete database for Saju calculation',
            'calculation_method': 'Astronomical calculation using ephemeris library',
            'sources': [
                'PyEphem astronomical computation library',
                'Based on JPL ephemeris data',
                'Calculated for Beijing meridian (120°E)',
                'Merged from multiple computation batches'
            ],
            'time_zone': 'Beijing time (UTC+8)',
            'precision': 'Second-level precision',
            'created': datetime.now().strftime('%Y-%m-%d'),
            'total_years': base_years + additional_years,
            'year_range': '1900-2109',
            'solar_terms_count_per_year': 24,
            'total_solar_terms': (base_years + additional_years) * 24,
            'note': '210-year complete dataset including both 節気(jieqi) and 中気(zhongqi). Ready for 12-jieqi extraction.',
            'composition': {
                'base_data': f'1900-2100 ({base_years} years)',
                'additional_data': f'2101-2109 ({additional_years} years)',
                'merge_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        },
        'solar_terms_data': {}
    }

    # 基本データを統合
    merged_database['solar_terms_data'].update(data_1900_2100['solar_terms_data'])

    # 追加データを統合
    merged_database['solar_terms_data'].update(data_2101_2109['solar_terms_data'])

    total_merged_years = len(merged_database['solar_terms_data'])
    print(f"   ✅ 統合完了: {total_merged_years}年分のデータ")

    # 年範囲チェック
    years = [int(year) for year in merged_database['solar_terms_data'].keys()]
    min_year = min(years)
    max_year = max(years)
    print(f"   📅 年範囲: {min_year}年 - {max_year}年")

    # 統合データベース保存
    print("\n5. 統合データベース保存")
    output_file = 'solar_terms_1900_2109_COMPLETE.json'
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(merged_database, f, ensure_ascii=False, indent=2)
        print(f"   ✅ 保存完了: {output_file}")
    except Exception as e:
        print(f"   ❌ 保存エラー: {e}")
        return False

    # 最終統計
    print("\n" + "=" * 70)
    print("✅ 210年節気データベース統合完了")
    print("=" * 70)
    print(f"総年数: {total_merged_years}年")
    print(f"年範囲: {min_year}-{max_year}年")
    print(f"総節気数: {total_merged_years * 24}個 (各年24節気)")
    print(f"出力ファイル: {output_file}")
    print("\n🎯 次のステップ: 中気除去処理で12節気データベース作成")
    print("   - remove_zhongqi_from_database.py を実行")
    print("   - 入力: solar_terms_1900_2109_COMPLETE.json")
    print("   - 出力: solar_terms_1900_2109_JIEQI_ONLY.json")

    return True

if __name__ == "__main__":
    success = merge_solar_terms_databases()
    if not success:
        print("\n❌ 統合処理が失敗しました")
        exit(1)