#!/usr/bin/env python3
"""
koyomi8.comのCSV機能を使ったデータ取得テスト
"""

import requests
import re

def test_csv_fetch():
    """CSV表示機能をテスト"""
    # まず通常のページにアクセス
    url = "https://koyomi8.com/24sekki.html"
    
    data = {
        'year': '1986',
        'submit': '計算実行'
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    session = requests.Session()
    
    try:
        print("1. 通常ページアクセス中...")
        response1 = session.post(url, data=data, headers=headers, timeout=30)
        
        # CSVボタンをクリック
        print("2. CSV表示を試行中...")
        csv_data = {
            'year': '1986',
            'csv': 'CSV表示'  # CSVボタンのvalue
        }
        
        response2 = session.post(url, data=csv_data, headers=headers, timeout=30)
        response2.encoding = 'utf-8'
        
        print(f"CSV レスポンス長: {len(response2.text)} 文字")
        
        # CSVデータを解析
        lines = response2.text.split('\n')
        print("CSV データ:")
        for i, line in enumerate(lines[:20]):  # 最初の20行
            if line.strip():
                print(f"{i}: {line}")
        
        # データが見つからない場合、別の方法を試す
        if '1986' not in response2.text and 'csv' not in response2.text.lower():
            print("\n3. ページ内の全データを探索...")
            
            # 完全なHTMLを保存してデバッグ
            with open('debug_1986.html', 'w', encoding='utf-8') as f:
                f.write(response1.text)
            print("デバッグ用HTMLを保存: debug_1986.html")
            
    except Exception as e:
        print(f"エラー: {e}")

def alternative_approach():
    """別のアプローチ：直接URLパラメータでアクセス"""
    print("\n=== 別のアプローチ ===")
    
    # URLパラメータで直接アクセスを試す
    url = "https://koyomi8.com/24sekki.html?year=1986&submit=計算実行"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.encoding = 'utf-8'
        
        print(f"GET レスポンス長: {len(response.text)} 文字")
        
        # デバッグ用に保存
        with open('debug_1986_get.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        print("GETレスポンスを保存: debug_1986_get.html")
        
    except Exception as e:
        print(f"エラー: {e}")

if __name__ == "__main__":
    test_csv_fetch()
    alternative_approach()