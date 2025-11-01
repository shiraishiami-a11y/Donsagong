#!/usr/bin/env python3
"""
1909年節気データ追加スクリプト
1908年データを基準に推定
"""

import json
import os

def add_1909_solar_terms():
    """1909年節気データを追加"""
    
    # 既存データベースを読み込み
    db_path = 'solar_terms_1900-1910_database.json'
    
    if os.path.exists(db_path):
        with open(db_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        print("❌ データベースファイルが見つかりません")
        return
    
    # 1909年節気データ（1908年を基準に推定）
    solar_terms_1909 = {
        "立春": {
            "chinese_name": "立春",
            "english_name": "Lichun",
            "meaning": "Beginning of Spring",
            "month": "February",
            "day": 4,
            "hour": 20,
            "minute": 25,
            "second": 0,
            "full_datetime": "1909-02-04 20:25:00",
            "source": "Pattern-based estimation from 1908 data"
        },
        "驚蟄": {
            "chinese_name": "驚蟄",
            "english_name": "Jingzhe",
            "meaning": "Awakening of Insects",
            "month": "March",
            "day": 6,
            "hour": 15,
            "minute": 10,
            "second": 0,
            "full_datetime": "1909-03-06 15:10:00",
            "source": "Pattern-based estimation"
        },
        "清明": {
            "chinese_name": "清明",
            "english_name": "Qingming",
            "meaning": "Clear and Bright",
            "month": "April",
            "day": 5,
            "hour": 21,
            "minute": 15,
            "second": 0,
            "full_datetime": "1909-04-05 21:15:00",
            "source": "Pattern-based estimation"
        },
        "立夏": {
            "chinese_name": "立夏",
            "english_name": "Lixia",
            "meaning": "Beginning of Summer",
            "month": "May",
            "day": 6,
            "hour": 15,
            "minute": 40,
            "second": 0,
            "full_datetime": "1909-05-06 15:40:00",
            "source": "Pattern-based estimation"
        },
        "芒種": {
            "chinese_name": "芒種",
            "english_name": "Mangzhong",
            "meaning": "Grain in Ear",
            "month": "June",
            "day": 6,
            "hour": 20,
            "minute": 5,
            "second": 0,
            "full_datetime": "1909-06-06 20:05:00",
            "source": "Pattern-based estimation"
        },
        "小暑": {
            "chinese_name": "小暑",
            "english_name": "Xiaoshu",
            "meaning": "Slight Heat",
            "month": "July",
            "day": 8,
            "hour": 5,
            "minute": 40,
            "second": 0,
            "full_datetime": "1909-07-08 05:40:00",
            "source": "Pattern-based estimation"
        },
        "立秋": {
            "chinese_name": "立秋",
            "english_name": "Liqiu",
            "meaning": "Beginning of Autumn",
            "month": "August",
            "day": 8,
            "hour": 16,
            "minute": 15,
            "second": 0,
            "full_datetime": "1909-08-08 16:15:00",
            "source": "Pattern-based estimation"
        },
        "白露": {
            "chinese_name": "白露",
            "english_name": "Bailu",
            "meaning": "White Dew",
            "month": "September",
            "day": 8,
            "hour": 19,
            "minute": 25,
            "second": 0,
            "full_datetime": "1909-09-08 19:25:00",
            "source": "Pattern-based estimation"
        },
        "寒露": {
            "chinese_name": "寒露",
            "english_name": "Hanlu",
            "meaning": "Cold Dew",
            "month": "October",
            "day": 9,
            "hour": 8,
            "minute": 40,
            "second": 0,
            "full_datetime": "1909-10-09 08:40:00",
            "source": "Pattern-based estimation"
        },
        "立冬": {
            "chinese_name": "立冬",
            "english_name": "Lidong",
            "meaning": "Beginning of Winter",
            "month": "November",
            "day": 8,
            "hour": 10,
            "minute": 5,
            "second": 0,
            "full_datetime": "1909-11-08 10:05:00",
            "source": "Pattern-based estimation"
        },
        "大雪": {
            "chinese_name": "大雪",
            "english_name": "Daxue",
            "meaning": "Major Snow",
            "month": "December",
            "day": 8,
            "hour": 4,
            "minute": 20,
            "second": 0,
            "full_datetime": "1909-12-08 04:20:00",
            "source": "Pattern-based estimation for daeun calculation"
        },
        "小寒": {
            "chinese_name": "小寒",
            "english_name": "Xiaohan",
            "meaning": "Slight Cold",
            "month": "January",
            "day": 6,
            "hour": 15,
            "minute": 15,
            "second": 0,
            "full_datetime": "1910-01-06 15:15:00",
            "source": "Pattern-based estimation (next year)"
        }
    }
    
    # 1909年データを追加
    data['solar_terms_data']['1909'] = solar_terms_1909
    
    # メタデータを更新
    if '1909' not in data['metadata'].get('note', ''):
        data['metadata']['note'] = data['metadata'].get('note', '') + " 1909 data added with estimations."
    
    # ファイルに保存
    with open(db_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("✅ 1909年節気データ追加完了")
    print(f"追加節気数: {len(solar_terms_1909)}個")
    
    # 重要な節気を確認
    print(f"\n📊 1909年重要節気:")
    daxue = solar_terms_1909['大雪']
    print(f"大雪: {daxue['month']} {daxue['day']}日 {daxue['hour']}:{daxue['minute']:02d}")
    
    return data

def main():
    print("🔧 1909年節気データ追加")
    print("="*50)
    
    result = add_1909_solar_terms()
    
    if result:
        years = list(result['solar_terms_data'].keys())
        print(f"\n現在のデータベース年度: {sorted(years)}")
        print(f"総年数: {len(years)}年分")

if __name__ == "__main__":
    main()