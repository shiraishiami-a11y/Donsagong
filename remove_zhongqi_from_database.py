#!/usr/bin/env python3
"""
節気データベースから中気を除去
24節気 → 12節気（節気のみ）に変換
"""

import json
from datetime import datetime
from typing import Dict, List

class ZhongqiRemover:
    def __init__(self):
        # 中気リスト（除去する対象）
        self.zhongqi_list = [
            '雨水',   # 330度
            '春分',   # 0度
            '穀雨',   # 30度
            '小満',   # 60度
            '夏至',   # 90度
            '大暑',   # 120度
            '処暑',   # 150度
            '秋分',   # 180度
            '霜降',   # 210度
            '小雪',   # 240度
            '冬至',   # 270度
            '大寒'    # 300度
        ]

        # 節気リスト（残すべき12節気）
        self.jieqi_list = [
            '立春',   # 315度
            '驚蟄',   # 345度（啓蟄）
            '清明',   # 15度
            '立夏',   # 45度
            '芒種',   # 75度
            '小暑',   # 105度
            '立秋',   # 135度
            '白露',   # 165度
            '寒露',   # 195度
            '立冬',   # 225度
            '大雪',   # 255度
            '小寒'    # 285度
        ]

        # 処理統計
        self.stats = {
            'total_years': 0,
            'processed_years': 0,
            'skipped_years': 0,
            'removed_zhongqi_count': 0,
            'kept_jieqi_count': 0
        }

    def load_database(self, filepath: str) -> Dict:
        """データベースを読み込み"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ データベース読み込みエラー: {e}")
            return {}

    def is_zhongqi(self, term_name: str) -> bool:
        """中気かどうかを判定"""
        return term_name in self.zhongqi_list

    def is_jieqi(self, term_name: str) -> bool:
        """節気かどうかを判定"""
        return term_name in self.jieqi_list

    def process_single_year(self, year: str, year_data: Dict) -> Dict:
        """単一年のデータを処理"""
        original_count = len(year_data)
        cleaned_data = {}
        removed_count = 0
        kept_count = 0

        print(f"  {year}年: 元データ{original_count}個", end=" → ")

        for term_name, term_data in year_data.items():
            if self.is_zhongqi(term_name):
                # 中気は除去
                removed_count += 1
                continue
            elif self.is_jieqi(term_name):
                # 節気は保持
                cleaned_data[term_name] = term_data
                kept_count += 1
            else:
                # 未知の節気名は警告して保持
                print(f"\n  ⚠️ 未知の節気: {term_name} (保持)")
                cleaned_data[term_name] = term_data
                kept_count += 1

        final_count = len(cleaned_data)
        print(f"処理後{final_count}個 (除去:{removed_count}, 保持:{kept_count})")

        # 統計更新
        self.stats['removed_zhongqi_count'] += removed_count
        self.stats['kept_jieqi_count'] += kept_count

        return cleaned_data

    def remove_zhongqi_from_database(self, database: Dict) -> Dict:
        """データベース全体から中気を除去"""
        print("=" * 60)
        print("中気除去処理開始")
        print("=" * 60)

        if 'solar_terms_data' not in database:
            print("❌ 節気データが見つかりません")
            return database

        solar_terms_data = database['solar_terms_data']
        cleaned_solar_terms_data = {}

        self.stats['total_years'] = len(solar_terms_data)

        for year, year_data in solar_terms_data.items():
            original_count = len(year_data)

            # 1900-1909年は既に12節気のみの場合があるので、中気があるかチェック
            has_zhongqi = any(self.is_zhongqi(term_name) for term_name in year_data.keys())

            if not has_zhongqi:
                # 中気がない年はそのまま保持
                cleaned_solar_terms_data[year] = year_data
                self.stats['skipped_years'] += 1
                print(f"  {year}年: スキップ (既に12節気のみ)")
                continue

            # 中気がある年は処理
            cleaned_year_data = self.process_single_year(year, year_data)
            cleaned_solar_terms_data[year] = cleaned_year_data
            self.stats['processed_years'] += 1

        # メタデータを更新
        updated_database = database.copy()
        updated_database['solar_terms_data'] = cleaned_solar_terms_data

        # メタデータの更新
        updated_database['metadata']['description'] = 'Complete 12 solar terms (節気) data for 210 years (1900-2109)'
        updated_database['metadata']['data_structure'] = {
            '1900-2109': '12節気のみ（中気除去済み）'
        }
        updated_database['metadata']['note'] = '四柱推命計算専用：12節気のみのクリーンデータベース'
        updated_database['metadata']['processed'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        updated_database['metadata']['solar_terms_count_per_year'] = 12

        return updated_database

    def validate_cleaned_database(self, database: Dict) -> bool:
        """クリーンアップ後のデータベースを検証"""
        print("\n" + "=" * 60)
        print("データ検証開始")
        print("=" * 60)

        if 'solar_terms_data' not in database:
            print("❌ 節気データが見つかりません")
            return False

        solar_terms_data = database['solar_terms_data']
        validation_passed = True
        error_count = 0

        for year, year_data in solar_terms_data.items():
            expected_count = 12
            actual_count = len(year_data)

            # 節気数チェック
            if actual_count != expected_count:
                print(f"❌ {year}年: 期待{expected_count}個、実際{actual_count}個")
                validation_passed = False
                error_count += 1
                continue

            # 中気が残っていないかチェック
            remaining_zhongqi = [name for name in year_data.keys() if self.is_zhongqi(name)]
            if remaining_zhongqi:
                print(f"❌ {year}年: 中気が残存 {remaining_zhongqi}")
                validation_passed = False
                error_count += 1
                continue

            # 必要な節気がすべて揃っているかチェック
            missing_jieqi = [name for name in self.jieqi_list if name not in year_data]
            if missing_jieqi:
                print(f"⚠️ {year}年: 節気欠損 {missing_jieqi}")

            print(f"✅ {year}年: 正常 (12節気)")

        if validation_passed:
            print(f"\n🎉 検証完了: 全年度が正常です")
        else:
            print(f"\n❌ 検証失敗: {error_count}年でエラー")

        return validation_passed

    def print_statistics(self):
        """処理統計を表示"""
        print("\n" + "=" * 60)
        print("処理統計")
        print("=" * 60)
        print(f"総年数: {self.stats['total_years']}年")
        print(f"処理年数: {self.stats['processed_years']}年")
        print(f"スキップ年数: {self.stats['skipped_years']}年")
        print(f"除去した中気数: {self.stats['removed_zhongqi_count']}個")
        print(f"保持した節気数: {self.stats['kept_jieqi_count']}個")

        # 期待値計算
        expected_removed = self.stats['processed_years'] * 12  # 処理年数 × 12中気
        expected_kept = self.stats['total_years'] * 12  # 全年数 × 12節気

        print(f"\n期待除去数: {expected_removed}個")
        print(f"期待保持数: {expected_kept}個")

        if self.stats['removed_zhongqi_count'] == expected_removed:
            print("✅ 中気除去: 完璧")
        else:
            print("❌ 中気除去: 異常")

def main():
    """メイン処理"""
    remover = ZhongqiRemover()

    # データベース読み込み
    print("中気除去ツール v2.0 - 210年対応版")
    print("入力ファイル: solar_terms_1900_2109_COMPLETE.json")

    database = remover.load_database('solar_terms_1900_2109_COMPLETE.json')
    if not database:
        return

    # 中気除去処理
    cleaned_database = remover.remove_zhongqi_from_database(database)

    # 検証
    validation_result = remover.validate_cleaned_database(cleaned_database)

    # 統計表示
    remover.print_statistics()

    if validation_result:
        # 保存
        output_file = 'solar_terms_1900_2109_JIEQI_ONLY.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(cleaned_database, f, ensure_ascii=False, indent=2)

        print(f"\n💾 保存完了: {output_file}")
        print("🎯 12節気専用データベースが完成しました！")
    else:
        print("\n❌ 検証エラーのため保存を中止しました")

if __name__ == "__main__":
    main()