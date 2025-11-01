#!/usr/bin/env python3
"""
210年節気データベース最終検証
solar_terms_1900_2109_JIEQI_ONLY.json の完整性を徹底検証
期待値: 210年 × 12節気 = 2,520個の正確なデータ
"""

import json
from datetime import datetime
from typing import Dict, List, Set

class Final210YearValidator:
    def __init__(self):
        # 必要な12節気リスト
        self.required_jieqi = {
            '立春', '驚蟄', '清明', '立夏', '芒種', '小暑',
            '立秋', '白露', '寒露', '立冬', '大雪', '小寒'
        }

        # 除去されるべき12中気リスト
        self.forbidden_zhongqi = {
            '雨水', '春分', '穀雨', '小満', '夏至', '大暑',
            '処暑', '秋分', '霜降', '小雪', '冬至', '大寒'
        }

        # 検証統計
        self.validation_stats = {
            'total_years': 0,
            'valid_years': 0,
            'invalid_years': 0,
            'total_jieqi_count': 0,
            'missing_jieqi': [],
            'forbidden_found': [],
            'year_errors': []
        }

    def load_database(self, filepath: str) -> Dict:
        """データベースファイルを読み込み"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ ファイルが見つかりません: {filepath}")
            return {}
        except json.JSONDecodeError as e:
            print(f"❌ JSON解析エラー: {e}")
            return {}
        except Exception as e:
            print(f"❌ ファイル読み込みエラー: {e}")
            return {}

    def validate_metadata(self, database: Dict) -> bool:
        """メタデータの検証"""
        print("=" * 70)
        print("📋 メタデータ検証")
        print("=" * 70)

        if 'metadata' not in database:
            print("❌ メタデータが見つかりません")
            return False

        metadata = database['metadata']

        # 基本フィールドチェック
        expected_fields = ['title', 'description', 'total_years', 'year_range']
        for field in expected_fields:
            if field in metadata:
                print(f"✅ {field}: {metadata[field]}")
            else:
                print(f"⚠️ {field}: 見つかりません")

        # 年数チェック
        if 'total_years' in metadata:
            expected_total = 210
            actual_total = metadata['total_years']
            if actual_total == expected_total:
                print(f"✅ 総年数: {actual_total}年 (期待値: {expected_total}年)")
            else:
                print(f"❌ 総年数不一致: {actual_total}年 (期待値: {expected_total}年)")
                return False

        return True

    def validate_single_year(self, year: str, year_data: Dict) -> Dict:
        """単一年のデータを詳細検証"""
        validation_result = {
            'year': year,
            'valid': True,
            'jieqi_count': len(year_data),
            'missing_jieqi': [],
            'forbidden_found': [],
            'unknown_terms': [],
            'errors': []
        }

        # 節気数チェック
        expected_count = 12
        actual_count = len(year_data)
        if actual_count != expected_count:
            validation_result['valid'] = False
            validation_result['errors'].append(f"節気数不正: {actual_count}個 (期待: {expected_count}個)")

        # 各節気をチェック
        found_jieqi = set(year_data.keys())

        # 必要な節気の欠損チェック
        missing = self.required_jieqi - found_jieqi
        if missing:
            validation_result['valid'] = False
            validation_result['missing_jieqi'] = list(missing)
            validation_result['errors'].append(f"節気欠損: {missing}")

        # 禁止されている中気の存在チェック
        forbidden = self.forbidden_zhongqi & found_jieqi
        if forbidden:
            validation_result['valid'] = False
            validation_result['forbidden_found'] = list(forbidden)
            validation_result['errors'].append(f"中気残存: {forbidden}")

        # 未知の節気チェック
        all_known = self.required_jieqi | self.forbidden_zhongqi
        unknown = found_jieqi - all_known
        if unknown:
            validation_result['unknown_terms'] = list(unknown)
            validation_result['errors'].append(f"未知の節気: {unknown}")

        return validation_result

    def validate_all_years(self, database: Dict) -> bool:
        """全年度のデータを検証"""
        print("\n" + "=" * 70)
        print("📅 210年データ完整性検証")
        print("=" * 70)

        if 'solar_terms_data' not in database:
            print("❌ 節気データが見つかりません")
            return False

        solar_terms_data = database['solar_terms_data']
        self.validation_stats['total_years'] = len(solar_terms_data)

        # 年範囲チェック
        years = [int(year) for year in solar_terms_data.keys()]
        min_year = min(years)
        max_year = max(years)
        expected_min = 1900
        expected_max = 2109

        print(f"年範囲: {min_year}年 - {max_year}年")
        if min_year == expected_min and max_year == expected_max:
            print(f"✅ 年範囲正常 (期待: {expected_min}-{expected_max})")
        else:
            print(f"❌ 年範囲異常 (期待: {expected_min}-{expected_max})")
            return False

        # 年数チェック
        expected_years = 210
        actual_years = len(years)
        if actual_years == expected_years:
            print(f"✅ 年数正常: {actual_years}年")
        else:
            print(f"❌ 年数異常: {actual_years}年 (期待: {expected_years}年)")
            return False

        # 各年を詳細検証
        print(f"\n📊 各年詳細検証開始 ({actual_years}年)...")
        valid_count = 0
        invalid_count = 0
        total_jieqi = 0

        for year_str in sorted(solar_terms_data.keys(), key=int):
            year_data = solar_terms_data[year_str]
            result = self.validate_single_year(year_str, year_data)

            total_jieqi += result['jieqi_count']

            if result['valid']:
                valid_count += 1
                if int(year_str) % 20 == 0:  # 20年ごとに表示
                    print(f"✅ {year_str}年: 正常 (12節気)")
            else:
                invalid_count += 1
                print(f"❌ {year_str}年: エラー - {', '.join(result['errors'])}")
                self.validation_stats['year_errors'].append(result)

                # 詳細エラー統計
                self.validation_stats['missing_jieqi'].extend(result['missing_jieqi'])
                self.validation_stats['forbidden_found'].extend(result['forbidden_found'])

        # 統計更新
        self.validation_stats['valid_years'] = valid_count
        self.validation_stats['invalid_years'] = invalid_count
        self.validation_stats['total_jieqi_count'] = total_jieqi

        print(f"\n📈 検証完了")
        print(f"正常年: {valid_count}年")
        print(f"異常年: {invalid_count}年")
        print(f"総節気数: {total_jieqi}個")

        return invalid_count == 0

    def validate_expected_total(self) -> bool:
        """期待総数の検証"""
        print("\n" + "=" * 70)
        print("🎯 期待値検証")
        print("=" * 70)

        expected_total_jieqi = 210 * 12  # 210年 × 12節気
        actual_total = self.validation_stats['total_jieqi_count']

        print(f"期待総節気数: {expected_total_jieqi}個")
        print(f"実際総節気数: {actual_total}個")

        if actual_total == expected_total_jieqi:
            print("✅ 総節気数: 完璧一致")
            return True
        else:
            print(f"❌ 総節気数不一致: 差分 {expected_total_jieqi - actual_total}個")
            return False

    def generate_validation_report(self) -> str:
        """検証レポート生成"""
        report = []
        report.append("=" * 70)
        report.append("210年節気データベース最終検証レポート")
        report.append("=" * 70)
        report.append(f"検証日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"対象ファイル: solar_terms_1900_2109_JIEQI_ONLY.json")
        report.append("")

        # 基本統計
        report.append("📊 基本統計")
        report.append(f"総年数: {self.validation_stats['total_years']}年")
        report.append(f"正常年: {self.validation_stats['valid_years']}年")
        report.append(f"異常年: {self.validation_stats['invalid_years']}年")
        report.append(f"総節気数: {self.validation_stats['total_jieqi_count']}個")
        report.append("")

        # 期待値比較
        expected_total = 210 * 12
        report.append("🎯 期待値比較")
        report.append(f"期待総節気数: {expected_total}個")
        report.append(f"実際総節気数: {self.validation_stats['total_jieqi_count']}個")

        if self.validation_stats['total_jieqi_count'] == expected_total:
            report.append("✅ 結果: 完璧一致")
        else:
            diff = expected_total - self.validation_stats['total_jieqi_count']
            report.append(f"❌ 結果: {diff}個の差分あり")

        report.append("")

        # エラー詳細
        if self.validation_stats['year_errors']:
            report.append("❌ エラー詳細")
            for error in self.validation_stats['year_errors'][:10]:  # 最初の10件
                report.append(f"{error['year']}年: {', '.join(error['errors'])}")
            if len(self.validation_stats['year_errors']) > 10:
                remaining = len(self.validation_stats['year_errors']) - 10
                report.append(f"... 他{remaining}件のエラー")
        else:
            report.append("✅ エラーなし: 全年度が正常")

        report.append("")
        report.append("=" * 70)

        return "\n".join(report)

    def run_complete_validation(self, filepath: str) -> bool:
        """完全検証の実行"""
        print("🚀 210年節気データベース最終検証開始")
        print(f"対象ファイル: {filepath}")

        # データベース読み込み
        database = self.load_database(filepath)
        if not database:
            return False

        # メタデータ検証
        metadata_valid = self.validate_metadata(database)

        # 全年度検証
        years_valid = self.validate_all_years(database)

        # 期待総数検証
        total_valid = self.validate_expected_total()

        # 最終判定
        all_valid = metadata_valid and years_valid and total_valid

        # レポート生成・表示
        report = self.generate_validation_report()
        print("\n" + report)

        # レポートファイル保存
        report_file = 'FINAL_210_YEAR_VALIDATION_REPORT.md'
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"\n📄 検証レポート保存: {report_file}")

        if all_valid:
            print("\n🎉 検証完了: 210年節気データベースは完璧です！")
            print("✅ 210年 × 12節気 = 2,520個のデータが全て正常")
            print("✅ 四柱推命計算用データベースとして使用可能")
        else:
            print("\n❌ 検証失敗: データベースに問題があります")

        return all_valid

def main():
    """メイン実行"""
    validator = Final210YearValidator()

    filepath = 'solar_terms_1900_2109_JIEQI_ONLY.json'
    success = validator.run_complete_validation(filepath)

    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)