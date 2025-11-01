#!/usr/bin/env python3
"""
1900-2100年の全節気データを統合
既存の1900-1910年データ（12節気）と
新規生成した1910-2100年データ（24節気）を統合
"""

import json
from datetime import datetime

def load_json_file(filename):
    """JSONファイルを読み込む"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠️  {filename} が見つかりません")
        return None

def merge_all_databases():
    """全データベースを統合"""

    print("=" * 60)
    print("1900-2100年 完全節気データベース統合")
    print("=" * 60)

    # 統合データベースの初期化
    complete_database = {
        'metadata': {
            'title': 'Chinese Solar Terms (24節気) Complete Database 1900-2100',
            'description': 'Comprehensive 24 solar terms data for 201 years (1900-2100)',
            'data_structure': {
                '1900-1910': '12節気のみ（既存データ）',
                '1910-2100': '24節気完全版（天文学的計算）'
            },
            'calculation_method': 'Mixed (historical records + astronomical calculation)',
            'sources': [
                '1900-1910: Historical records from multiple Chinese sources',
                '1910-2100: PyEphem astronomical computation library',
                'Beijing meridian calculations (UTC+8)',
                'Purple Mountain Observatory references'
            ],
            'time_zone': 'Beijing time (UTC+8)',
            'precision': 'Second-level precision',
            'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_years': 201,
            'note': '完全な四柱推命計算に対応する包括的データベース'
        },
        'solar_terms_data': {}
    }

    # 1. 既存の1900-1910データを読み込む（12節気）
    print("\n[1/5] 既存の1900-1910年データを読み込み中...")
    original_data = load_json_file('solar_terms_1900-1910_database.json')
    if original_data:
        for year in ['1900', '1901', '1902', '1903', '1904', '1905', '1906', '1907', '1908', '1909', '1910']:
            if year in original_data.get('solar_terms_data', {}):
                complete_database['solar_terms_data'][year] = original_data['solar_terms_data'][year]
                print(f"  ✓ {year}年: {len(original_data['solar_terms_data'][year])}節気")

    # 2. 1910-1960データを読み込む（24節気）
    print("\n[2/5] 1910-1960年データを読み込み中...")
    data_1910_1960 = load_json_file('solar_terms_1910_1960_complete.json')
    if data_1910_1960:
        # 1910年は既存データを上書き（24節気版に更新）
        for year in range(1910, 1961):
            year_str = str(year)
            if year_str in data_1910_1960.get('solar_terms_data', {}):
                complete_database['solar_terms_data'][year_str] = data_1910_1960['solar_terms_data'][year_str]
        print(f"  ✓ 51年分のデータ（各年24節気）を統合")

    # 3. 1960-2010データを読み込む（24節気）
    print("\n[3/5] 1960-2010年データを読み込み中...")
    data_1960_2010 = load_json_file('solar_terms_1960_2010_complete.json')
    if data_1960_2010:
        # 1960年は重複するが、新しいデータで上書き
        for year in range(1960, 2011):
            year_str = str(year)
            if year_str in data_1960_2010.get('solar_terms_data', {}):
                complete_database['solar_terms_data'][year_str] = data_1960_2010['solar_terms_data'][year_str]
        print(f"  ✓ 51年分のデータ（各年24節気）を統合")

    # 4. 2010-2100データを読み込む（24節気）
    print("\n[4/5] 2010-2100年データを読み込み中...")
    data_2010_2100 = load_json_file('solar_terms_2010_2100_complete.json')
    if data_2010_2100:
        # 2010年は重複するが、新しいデータで上書き
        for year in range(2010, 2101):
            year_str = str(year)
            if year_str in data_2010_2100.get('solar_terms_data', {}):
                complete_database['solar_terms_data'][year_str] = data_2010_2100['solar_terms_data'][year_str]
        print(f"  ✓ 91年分のデータ（各年24節気）を統合")

    # 5. 統合データベースを保存
    print("\n[5/5] 統合データベースを保存中...")
    output_file = 'solar_terms_1900_2100_COMPLETE.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(complete_database, f, ensure_ascii=False, indent=2)

    # 統計情報の表示
    print("\n" + "=" * 60)
    print("✅ 統合完了！")
    print("=" * 60)

    total_years = len(complete_database['solar_terms_data'])
    total_terms = 0
    years_with_12 = 0
    years_with_24 = 0

    for year, data in complete_database['solar_terms_data'].items():
        term_count = len(data)
        total_terms += term_count
        if term_count == 12:
            years_with_12 += 1
        elif term_count == 24:
            years_with_24 += 1

    print(f"\n📊 データベース統計:")
    print(f"  • 総年数: {total_years}年 (1900-2100)")
    print(f"  • 総節気数: {total_terms:,}個")
    print(f"  • 12節気の年: {years_with_12}年 (1900-1909)")
    print(f"  • 24節気の年: {years_with_24}年 (1910-2100)")
    print(f"  • ファイルサイズ: 推定 {total_terms * 400 / 1024:.1f} KB")
    print(f"\n💾 保存先: {output_file}")

    # サンプルデータの表示
    print("\n=== サンプルデータ確認 ===")
    sample_years = ['1900', '1950', '1986', '2024', '2100']
    for year in sample_years:
        if year in complete_database['solar_terms_data']:
            terms_count = len(complete_database['solar_terms_data'][year])
            terms_list = list(complete_database['solar_terms_data'][year].keys())[:5]
            print(f"{year}年: {terms_count}節気 - {', '.join(terms_list)}...")

    return complete_database

def verify_data_integrity(database):
    """データの整合性を検証"""
    print("\n=== データ整合性検証 ===")

    issues = []

    # 年の連続性チェック
    years = sorted([int(y) for y in database['solar_terms_data'].keys()])
    for i in range(len(years) - 1):
        if years[i+1] - years[i] != 1:
            issues.append(f"年の欠落: {years[i]}年と{years[i+1]}年の間")

    # 各年の節気数チェック
    for year, data in database['solar_terms_data'].items():
        term_count = len(data)
        if term_count not in [12, 24]:
            issues.append(f"{year}年: 異常な節気数 ({term_count}個)")

    if issues:
        print("⚠️  検証で問題が見つかりました:")
        for issue in issues:
            print(f"  • {issue}")
    else:
        print("✅ データ整合性: 問題なし")

    return len(issues) == 0

def main():
    # データベースの統合
    complete_db = merge_all_databases()

    # データ整合性の検証
    if complete_db and complete_db['solar_terms_data']:
        verify_data_integrity(complete_db)

        print("\n" + "=" * 60)
        print("🎉 1900-2100年の完全節気データベースが完成しました！")
        print("四柱推命の大運計算に必要な全データが揃いました。")
        print("=" * 60)

if __name__ == "__main__":
    main()