#!/usr/bin/env python3
"""
koyomi8.comからのデータ取得をテスト（1986年のみ）
"""

import requests
import re

def test_fetch_1986():
    """1986年のデータ取得をテスト"""
    url = "https://koyomi8.com/24sekki.html"
    
    data = {
        'year': '1986',
        'submit': '計算実行'
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        print("1986年のデータを取得中...")
        response = requests.post(url, data=data, headers=headers, timeout=30)
        response.encoding = 'utf-8'
        
        if response.status_code == 200:
            print("✓ データ取得成功")
            
            # レスポンスの一部を表示
            content = response.text
            print(f"レスポンス長: {len(content)} 文字")
            
            # 芒種を探す
            jeol_names = ['立春', '芒種', '立秋', '小寒']
            for jeol_name in jeol_names:
                pattern = rf'{jeol_name}.*?(\d{{4}})/(\d{{1,2}})/(\d{{1,2}})\s+(\d{{1,2}}):(\d{{1,2}})'
                match = re.search(pattern, content)
                
                if match:
                    year = match.group(1)
                    month = match.group(2)
                    day = match.group(3)
                    hour = match.group(4)
                    minute = match.group(5)
                    print(f"{jeol_name}: {year}/{month:0>2}/{day:0>2} {hour:0>2}:{minute:0>2}")
                else:
                    print(f"{jeol_name}: 見つかりません")
            
            # HTMLの一部を表示（デバッグ用）
            print("\n--- HTMLサンプル ---")
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if '芒種' in line or '立春' in line:
                    start = max(0, i-2)
                    end = min(len(lines), i+3)
                    for j in range(start, end):
                        marker = ">>> " if j == i else "    "
                        print(f"{marker}{lines[j]}")
                    break
                    
        else:
            print(f"✗ HTTP エラー: {response.status_code}")
            
    except Exception as e:
        print(f"✗ エラー: {e}")

if __name__ == "__main__":
    test_fetch_1986()