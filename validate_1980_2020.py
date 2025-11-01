#!/usr/bin/env python3
"""
1980-2020年（40年分）の節気データ検証スクリプト
solar_terms_validation_framework.pyを使用して検証実行
"""

from solar_terms_validation_framework import SolarTermsValidator
import json
import time

def main():
    """1980-2020年の節気データ検証実行"""
    print("=" * 80)
    print("1980-2020年（40年分）節気データ検証システム")
    print("期間: 1980年～2020年（40年 × 24節気 = 960個のデータポイント）")
    print("=" * 80)

    # バリデーター初期化
    validator = SolarTermsValidator()

    # 検証開始時刻記録
    start_time = time.time()

    # 1980-2020年の検証実行
    results = validator.validate_year_range(
        1980, 2020,
        'solar_terms_1900_2100_COMPLETE.json'
    )

    # 検証時間計算
    validation_time = time.time() - start_time
    results['validation_time_seconds'] = round(validation_time, 2)
    results['validation_time_minutes'] = round(validation_time / 60, 2)

    # 詳細レポート生成
    validator.generate_validation_report(
        results,
        'validation_1980_2020.json'
    )

    # 検証結果サマリー表示
    print("\n" + "=" * 80)
    print("検証結果サマリー")
    print("=" * 80)

    if 'error' in results:
        print(f"❌ エラー: {results['error']}")
        return

    print(f"📊 検証期間: {results['range']}")
    print(f"⏱️  検証時間: {results['validation_time_minutes']:.1f}分")
    print(f"📅 検証年数: {results['total_years']}年")
    print(f"🎯 総節気数: {results['total_terms']}個")
    print(f"✅ 正確な節気: {results['validated_terms']}個")
    print(f"❌ エラー数: {results['error_count']}個")
    print(f"📈 成功率: {results['success_rate']}%")

    # エラーがある年を特定
    error_years = []
    error_details = []

    for year, year_result in results['year_results'].items():
        if year_result['error_count'] > 0:
            error_years.append(year)
            for warning in year_result['warnings']:
                if "誤差" in warning and "超過" in warning:
                    error_details.append(f"  {year}年: {warning}")

    if error_years:
        print(f"\n⚠️  問題のある年: {len(error_years)}年")
        print(f"   年リスト: {', '.join(map(str, sorted(error_years)))}")
        print(f"\n❌ エラー詳細:")
        for detail in error_details[:10]:  # 最初の10件のみ表示
            print(detail)
        if len(error_details) > 10:
            print(f"   ... 他{len(error_details)-10}件")
    else:
        print("\n🎉 全ての年で節気データが正確です！")

    print(f"\n📄 詳細レポート: validation_1980_2020.json")
    print("=" * 80)

if __name__ == "__main__":
    main()