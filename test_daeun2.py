#!/usr/bin/env python3
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.manseryeok.calculator import ManseryeokCalculator

# テスト
calculator = ManseryeokCalculator()

female_birth = datetime(1986, 12, 20, 0)
female_saju = calculator.calculate_saju(female_birth, 'female')

print(f"女性四柱: {female_saju}")
female_daeuns = calculator.calculate_daeun(female_saju, 'female')

print(f"\n大運リスト:")
for i, d in enumerate(female_daeuns[:5]):
    print(f"  第{i+1}大運: {d.ganzhi}")
    print(f"    age_start: {d.age_start}")
    print(f"    age_end: {d.age_end}")
    
# 実際の起運年齢を計算
if female_daeuns:
    actual_starting_age = female_daeuns[0].age_start - female_birth.year
    print(f"\n起運年齢: {actual_starting_age}歳")
