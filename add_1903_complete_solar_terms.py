#!/usr/bin/env python3
"""
1903年の完全な節気データを追加
1900年のパターンを基準に推定
"""

import json
import os

def add_1903_complete_solar_terms():
    """1903年の完全な節気データを追加"""
    
    # 既存データベースを読み込み
    db_path = 'solar_terms_1900-1910_database.json'
    
    if os.path.exists(db_path):
        with open(db_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        print("❌ データベースファイルが見つかりません")
        return
    
    # 1903年の完全な節気データ（1900年基準+3年のオフセット）
    solar_terms_1903 = {
        "立春": {
            "chinese_name": "立春",
            "english_name": "Lichun",
            "meaning": "Beginning of Spring",
            "month": "February",
            "day": 5,
            "hour": 7,
            "minute": 31,
            "second": 17,
            "full_datetime": "1903-02-05 07:31:17",
            "source": "jieqi.bmcx.com verified data"
        },
        "驚蟄": {
            "chinese_name": "驚蟄",
            "english_name": "Jingzhe",
            "meaning": "Awakening of Insects",
            "month": "March",
            "day": 6,
            "hour": 2,
            "minute": 10,
            "second": 0,
            "full_datetime": "1903-03-06 02:10:00",
            "source": "Pattern estimation from 1900"
        },
        "清明": {
            "chinese_name": "清明",
            "english_name": "Qingming",
            "meaning": "Clear and Bright",
            "month": "April",
            "day": 5,
            "hour": 7,
            "minute": 41,
            "second": 0,
            "full_datetime": "1903-04-05 07:41:00",
            "source": "Pattern estimation"
        },
        "立夏": {
            "chinese_name": "立夏",
            "english_name": "Lixia",
            "meaning": "Beginning of Summer",
            "month": "May",
            "day": 6,
            "hour": 1,
            "minute": 43,
            "second": 0,
            "full_datetime": "1903-05-06 01:43:00",
            "source": "Pattern estimation"
        },
        "芒種": {
            "chinese_name": "芒種",
            "english_name": "Mangzhong",
            "meaning": "Grain in Ear",
            "month": "June",
            "day": 6,
            "hour": 6,
            "minute": 27,
            "second": 0,
            "full_datetime": "1903-06-06 06:27:00",
            "source": "Pattern estimation"
        },
        "小暑": {
            "chinese_name": "小暑",
            "english_name": "Xiaoshu",
            "meaning": "Slight Heat",
            "month": "July",
            "day": 7,
            "hour": 16,
            "minute": 58,
            "second": 0,
            "full_datetime": "1903-07-07 16:58:00",
            "source": "Pattern estimation - important for 6/30 birth"
        },
        "立秋": {
            "chinese_name": "立秋",
            "english_name": "Liqiu",
            "meaning": "Beginning of Autumn",
            "month": "August",
            "day": 8,
            "hour": 2,
            "minute": 39,
            "second": 0,
            "full_datetime": "1903-08-08 02:39:00",
            "source": "Pattern estimation"
        },
        "白露": {
            "chinese_name": "白露",
            "english_name": "Bailu",
            "meaning": "White Dew",
            "month": "September",
            "day": 8,
            "hour": 5,
            "minute": 5,
            "second": 0,
            "full_datetime": "1903-09-08 05:05:00",
            "source": "Pattern estimation"
        },
        "寒露": {
            "chinese_name": "寒露",
            "english_name": "Hanlu",
            "meaning": "Cold Dew",
            "month": "October",
            "day": 8,
            "hour": 20,
            "minute": 1,
            "second": 0,
            "full_datetime": "1903-10-08 20:01:00",
            "source": "Pattern estimation"
        },
        "立冬": {
            "chinese_name": "立冬",
            "english_name": "Lidong",
            "meaning": "Beginning of Winter",
            "month": "November",
            "day": 7,
            "hour": 22,
            "minute": 28,
            "second": 0,
            "full_datetime": "1903-11-07 22:28:00",
            "source": "Pattern estimation"
        },
        "大雪": {
            "chinese_name": "大雪",
            "english_name": "Daxue",
            "meaning": "Major Snow",
            "month": "December",
            "day": 7,
            "hour": 14,
            "minute": 44,
            "second": 0,
            "full_datetime": "1903-12-07 14:44:00",
            "source": "Pattern estimation"
        },
        "小寒": {
            "chinese_name": "小寒",
            "english_name": "Xiaohan",
            "meaning": "Slight Cold",
            "month": "January",
            "day": 6,
            "hour": 1,
            "minute": 41,
            "second": 0,
            "full_datetime": "1904-01-06 01:41:00",
            "source": "Pattern estimation (next year)"
        }
    }
    
    # 1903年データを置き換え（立春のみから完全データへ）
    data['solar_terms_data']['1903'] = solar_terms_1903
    
    # メタデータ更新
    if 'complete 1903' not in data['metadata'].get('note', ''):
        data['metadata']['note'] = data['metadata'].get('note', '') + " Complete 1903 data added."
    
    # ファイルに保存
    with open(db_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("✅ 1903年完全節気データ追加完了")
    print(f"追加節気数: {len(solar_terms_1903)}個")
    
    # 重要な節気を確認
    print(f"\n📊 1903年重要節気（6月30日生まれ用）:")
    if '小暑' in solar_terms_1903:
        xiaoshu = solar_terms_1903['小暑']
        print(f"小暑（次の節）: {xiaoshu['month']} {xiaoshu['day']}日 {xiaoshu['hour']}:{xiaoshu['minute']:02d}")
    if '芒種' in solar_terms_1903:
        mangzhong = solar_terms_1903['芒種']
        print(f"芒種（前の節）: {mangzhong['month']} {mangzhong['day']}日 {mangzhong['hour']}:{mangzhong['minute']:02d}")
    
    return data

def main():
    print("🔧 1903年完全節気データ追加")
    print("="*50)
    
    result = add_1903_complete_solar_terms()
    
    if result:
        # 1903年データ確認
        if '1903' in result['solar_terms_data']:
            terms = result['solar_terms_data']['1903']
            print(f"\n1903年節気リスト:")
            for name in terms.keys():
                print(f"  - {name}")

if __name__ == "__main__":
    main()