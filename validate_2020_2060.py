#!/usr/bin/env python3
"""
2020-2060年（40年分）の節気データ検証スクリプト
960個の節気データポイントを天文学的計算と比較検証
"""

import json
import sys
from solar_terms_validation_framework import SolarTermsValidator

def main():
    """2020-2060年の節気データ検証を実行"""
    validator = SolarTermsValidator()

    print("=" * 70)
    print("2020-2060年 節気データ検証システム")
    print("検証期間: 40年間 × 24節気 = 960データポイント")
    print("許容誤差: ±6時間")
    print("=" * 70)

    # 2020-2060年の検証実行
    results = validator.validate_year_range(
        2020, 2060,
        'solar_terms_1900_2100_COMPLETE.json'
    )

    if 'error' in results:
        print(f"❌ 検証エラー: {results['error']}")
        sys.exit(1)

    # 結果サマリー表示
    print("\n" + "=" * 70)
    print("🔍 検証結果サマリー")
    print("=" * 70)
    print(f"検証期間: {results['range']}")
    print(f"総年数: {results['total_years']}年")
    print(f"完全正確年数: {results['validated_years']}年")
    print(f"総節気数: {results['total_terms']}個")
    print(f"正確節気数: {results['validated_terms']}個")
    print(f"エラー数: {results['error_count']}個")
    print(f"成功率: {results['success_rate']}%")

    # エラー年/節気の詳細分析
    error_years = []
    error_details = []

    for year, year_result in results['year_results'].items():
        if year_result['error_count'] > 0:
            error_years.append(year)
            for term_name, term_detail in year_result['details'].items():
                if term_detail['status'] == 'ERROR':
                    error_details.append({
                        'year': year,
                        'term': term_name,
                        'our_time': term_detail['our_time'],
                        'calculated_time': term_detail['calculated_time'],
                        'difference_hours': term_detail['difference_hours']
                    })

    # エラー分析結果表示
    if error_details:
        print("\n" + "=" * 70)
        print("⚠️  問題のある節気詳細")
        print("=" * 70)
        print(f"エラーのある年数: {len(error_years)}年")
        print(f"エラー年: {sorted(error_years)}")
        print(f"\nエラー詳細（上位10件）:")

        # 誤差の大きい順にソート
        error_details_sorted = sorted(error_details, key=lambda x: x['difference_hours'], reverse=True)
        for i, error in enumerate(error_details_sorted[:10]):
            print(f"  {i+1:2d}. {error['year']}年 {error['term']}: "
                  f"誤差{error['difference_hours']:.1f}時間")
            print(f"      我々: {error['our_time']}")
            print(f"      計算: {error['calculated_time']}")
    else:
        print("\n✅ 全節気が許容範囲内で正確です！")

    # 結果をJSONファイルに保存
    output_file = 'validation_2020_2060.json'
    validator.generate_validation_report(results, output_file)

    print(f"\n📊 詳細レポート保存完了: {output_file}")
    print("\n" + "=" * 70)
    print("検証完了")
    print("=" * 70)

if __name__ == "__main__":
    main()