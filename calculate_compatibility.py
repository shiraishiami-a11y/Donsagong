#!/usr/bin/env python3
"""
四柱推命相性診断 - 만세력計算エンジン使用
"""

from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.manseryeok.calculator import ManseryeokCalculator

def main():
    calculator = ManseryeokCalculator()
    
    # 男性: 1968年12月2日 2時生まれ
    male_birth = datetime(1968, 12, 2, 2, 0, 0)
    male_saju = calculator.calculate_saju(male_birth, 'male')
    
    # 女性: 1986年12月20日 0時生まれ
    female_birth = datetime(1986, 12, 20, 0, 0, 0)
    female_saju = calculator.calculate_saju(female_birth, 'female')
    
    print("="*60)
    print("四柱推命 命式計算結果 (만세력システム使用)")
    print("="*60)
    
    print("\n【男性】1968年12月2日 2時生まれ")
    print("-"*40)
    print(f"四柱: {male_saju}")
    print(f"年柱: {male_saju.year_stem}{male_saju.year_branch}")
    print(f"月柱: {male_saju.month_stem}{male_saju.month_branch}")
    print(f"日柱: {male_saju.day_stem}{male_saju.day_branch}")
    print(f"時柱: {male_saju.hour_stem}{male_saju.hour_branch}")
    print(f"日主: {male_saju.day_stem}")
    
    print("\n【女性】1986年12月20日 0時生まれ")
    print("-"*40)
    print(f"四柱: {female_saju}")
    print(f"年柱: {female_saju.year_stem}{female_saju.year_branch}")
    print(f"月柱: {female_saju.month_stem}{female_saju.month_branch}")
    print(f"日柱: {female_saju.day_stem}{female_saju.day_branch}")
    print(f"時柱: {female_saju.hour_stem}{female_saju.hour_branch}")
    print(f"日主: {female_saju.day_stem}")
    
    print("\n" + "="*60)
    print("相性分析")
    print("="*60)
    
    # 五行相性分析
    stems_element = {
        '甲': '木', '乙': '木',
        '丙': '火', '丁': '火',
        '戊': '土', '己': '土',
        '庚': '金', '辛': '金',
        '壬': '水', '癸': '水'
    }
    
    male_element = stems_element[male_saju.day_stem]
    female_element = stems_element[female_saju.day_stem]
    
    print(f"\n男性日主: {male_saju.day_stem}({male_element})")
    print(f"女性日主: {female_saju.day_stem}({female_element})")
    
    # 相生相剋関係
    generation = {
        '木': '火', '火': '土', '土': '金', '金': '水', '水': '木'
    }
    
    if generation.get(male_element) == female_element:
        print(f"\n五行関係: {male_element}生{female_element} - 男性が女性を生かす関係")
    elif generation.get(female_element) == male_element:
        print(f"\n五行関係: {female_element}生{male_element} - 女性が男性を生かす関係")
    elif male_element == female_element:
        print(f"\n五行関係: 同じ{male_element} - 比和の関係（同質のエネルギー）")
    else:
        print(f"\n五行関係: {male_element}と{female_element} - 特殊な相互作用")
    
    # 大運計算
    print("\n" + "="*60)
    print("大運情報")
    print("="*60)
    
    try:
        male_daeun = calculator.calculate_daeun_with_lunar(male_saju)
        female_daeun = calculator.calculate_daeun_with_lunar(female_saju)
        
        print("\n【男性の大運】")
        print(f"起運: {male_daeun['startAge']}歳")
        for i, daeun in enumerate(male_daeun['daeunList'][:5], 1):
            print(f"第{i}大運 ({daeun['startAge']}-{daeun['endAge']}歳): {daeun['ganZhi']}")
        
        print("\n【女性の大運】")
        print(f"起運: {female_daeun['startAge']}歳")
        for i, daeun in enumerate(female_daeun['daeunList'][:5], 1):
            print(f"第{i}大運 ({daeun['startAge']}-{daeun['endAge']}歳): {daeun['ganZhi']}")
    except Exception as e:
        print(f"大運計算エラー: {e}")

if __name__ == "__main__":
    main()