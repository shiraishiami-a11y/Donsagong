#!/usr/bin/env python3
"""
koyomi8.comのHTML構造を詳しく分析
"""

import requests
import re

def analyze_html_structure():
    """HTMLの構造を詳しく分析"""
    url = "https://koyomi8.com/24sekki.html"
    
    data = {
        'year': '1986',
        'submit': '計算実行'
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.post(url, data=data, headers=headers, timeout=30)
        response.encoding = 'utf-8'
        content = response.text
        
        print("=== HTML構造分析 ===")
        
        # 節気に関連する行を抽出
        lines = content.split('\n')
        jeol_related_lines = []
        
        for i, line in enumerate(lines):
            if any(jeol in line for jeol in ['立春', '芒種', '立秋', '小寒', '驚蟄', '清明']):
                jeol_related_lines.append((i, line.strip()))
        
        print("節気関連の行:")
        for line_num, line in jeol_related_lines:
            print(f"{line_num}: {line}")
        
        print("\n=== テーブル構造の探索 ===")
        
        # JavaScriptで動的に生成される可能性を考慮
        # <td id="T1"></td> などのIDを持つ要素を探す
        id_patterns = []
        for i in range(1, 25):  # T1-T24, K1-K24
            id_patterns.extend([f'id="T{i}"', f'id="K{i}"'])
        
        for pattern in id_patterns[:10]:  # 最初の10個をチェック
            if pattern in content:
                print(f"見つかった: {pattern}")
        
        # JavaScriptコードを探す
        print("\n=== JavaScript探索 ===")
        js_lines = []
        for i, line in enumerate(lines):
            if 'document.getElementById' in line or 'innerHTML' in line:
                js_lines.append((i, line.strip()))
        
        print("JavaScript関連の行:")
        for line_num, line in js_lines[:20]:  # 最初の20行
            print(f"{line_num}: {line}")
            
    except Exception as e:
        print(f"エラー: {e}")

if __name__ == "__main__":
    analyze_html_structure()