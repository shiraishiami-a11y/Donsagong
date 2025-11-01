#!/usr/bin/env python3
"""
koyomi8.comから1900-2100年の節気データを自動収集
"""

import requests
import time
import json
import os
from datetime import datetime
import re
from urllib.parse import urlencode

def fetch_year_data(year):
    """指定年の節気データを取得"""
    url = "https://koyomi8.com/24sekki.html"
    
    # POSTデータ
    data = {
        'year': str(year),
        'submit': '計算実行'
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        print(f"{year}年のデータを取得中...")
        response = requests.post(url, data=data, headers=headers, timeout=30)
        response.encoding = 'utf-8'
        
        if response.status_code != 200:
            print(f"エラー: {year}年のデータ取得に失敗 (HTTP {response.status_code})")
            return None
            
        return response.text
    except Exception as e:
        print(f"エラー: {year}年のデータ取得に失敗 - {e}")
        return None

def parse_html_data(html_content, year):
    """HTMLから節気データを抽出"""
    if not html_content:
        return None
        
    # 節のみ（中気は除外）
    jeol_names = ['立春', '驚蟄', '清明', '立夏', '芒種', '小暑', '立秋', '白露', '寒露', '立冬', '大雪', '小寒']
    
    year_data = {}
    
    # HTMLから節気データを抽出
    for jeol_name in jeol_names:
        # 節気名とその後の日付時刻を探すパターン
        pattern = rf'{jeol_name}.*?(\d{{4}})/(\d{{1,2}})/(\d{{1,2}})\s+(\d{{1,2}}):(\d{{1,2}})'
        match = re.search(pattern, html_content)
        
        if match:
            jeol_year = int(match.group(1))
            month = int(match.group(2))
            day = int(match.group(3))
            hour = int(match.group(4))
            minute = int(match.group(5))
            
            # 小寒は翌年1月の場合がある
            if jeol_name == '小寒' and jeol_year == year + 1:
                year_data[jeol_name] = {
                    'year': jeol_year,
                    'month': month,
                    'day': day,
                    'hour': hour,
                    'minute': minute,
                    'second': 0
                }
            elif jeol_year == year:
                year_data[jeol_name] = {
                    'year': jeol_year,
                    'month': month,
                    'day': day,
                    'hour': hour,
                    'minute': minute,
                    'second': 0
                }
    
    return year_data if year_data else None

def collect_all_jeolip_data():
    """1900-2100年のすべての節気データを収集"""
    print("=" * 60)
    print("koyomi8.comから節気データを収集中...")
    print("対象期間: 1900-2100年")
    print("=" * 60)
    
    all_data = {}
    failed_years = []
    
    for year in range(1900, 2101):
        # リクエスト間隔を設ける（サーバー負荷軽減）
        if year > 1900:
            time.sleep(1)
        
        html_content = fetch_year_data(year)
        year_data = parse_html_data(html_content, year)
        
        if year_data:
            all_data[str(year)] = year_data
            print(f"✓ {year}年: {len(year_data)}個の節気を取得")
        else:
            failed_years.append(year)
            print(f"✗ {year}年: データ取得失敗")
        
        # 10年ごとに進捗表示
        if year % 10 == 0:
            completed = year - 1900 + 1
            total = 2101 - 1900
            progress = completed / total * 100
            print(f"進捗: {completed}/{total} ({progress:.1f}%)")
    
    print("\n" + "=" * 60)
    print(f"収集完了: {len(all_data)}年のデータを取得")
    if failed_years:
        print(f"失敗した年: {failed_years}")
    
    return all_data

def save_database(data, filename='koyomi8_jeolip_database_1900_2100.json'):
    """収集したデータをJSONファイルに保存"""
    filepath = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'data',
        filename
    )
    
    # dataディレクトリ作成
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\nデータベースを保存しました: {filepath}")
    return filepath

def validate_collected_data(data):
    """収集したデータの妥当性をチェック"""
    print("\n" + "=" * 40)
    print("データ検証中...")
    print("-" * 40)
    
    # 1986年のデータをチェック
    if '1986' in data:
        year_1986 = data['1986']
        if '芒種' in year_1986:
            mangzhong = year_1986['芒種']
            print(f"1986年芒種: {mangzhong['year']}/{mangzhong['month']:02d}/{mangzhong['day']:02d} {mangzhong['hour']:02d}:{mangzhong['minute']:02d}")
        else:
            print("1986年芒種データが見つかりません")
    
    # 統計情報
    total_entries = sum(len(year_data) for year_data in data.values())
    print(f"\n総エントリ数: {total_entries}")
    print(f"年数: {len(data)}")
    print(f"平均エントリ/年: {total_entries/len(data):.1f}")

def main():
    # データ収集
    jeolip_data = collect_all_jeolip_data()
    
    # データ検証
    validate_collected_data(jeolip_data)
    
    # 保存
    filepath = save_database(jeolip_data)
    
    print("\n完了!")
    print(f"データベースファイル: {filepath}")
    print(f"総年数: {len(jeolip_data)}年")

if __name__ == "__main__":
    main()