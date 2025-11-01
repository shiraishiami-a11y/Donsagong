#!/usr/bin/env python3
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.manseryeok.calculator import ManseryeokCalculator

# テスト
calculator = ManseryeokCalculator()

male_birth = datetime(1986, 5, 26, 5)
female_birth = datetime(1986, 12, 20, 0)

male_saju = calculator.calculate_saju(male_birth, 'male')
female_saju = calculator.calculate_saju(female_birth, 'female')

print(f"男性四柱: {male_saju}")
male_daeuns = calculator.calculate_daeun(male_saju, 'male')
print(f"男性大運（最初の3つ）:")
for d in male_daeuns[:3]:
    print(f"  {d.age_start}-{d.age_end}歳: {d.ganzhi}")

print(f"\n女性四柱: {female_saju}")
female_daeuns = calculator.calculate_daeun(female_saju, 'female')
print(f"女性大運（最初の3つ）:")
for d in female_daeuns[:3]:
    print(f"  {d.age_start}-{d.age_end}歳: {d.ganzhi}")
