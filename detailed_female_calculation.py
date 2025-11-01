#!/usr/bin/env python3
"""
女性の命式の詳細計算過程表示
"""

from datetime import datetime, timezone, timedelta
from accurate_daeun_calculator import AccurateDaeunCalculator
import sys
import os

# 만세력 계산기 임포트
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.manseryeok.calculator import ManseryeokCalculator

KST = timezone(timedelta(hours=9))

def detailed_female_calculation():
    """女性B（夏生まれ）の詳細計算"""
    
    print("=" * 80)
    print("🔍 女性B（夏生まれ）の詳細計算過程")
    print("=" * 80)
    
    # テストケース：女性B（夏生まれ）
    birth_date = datetime(1986, 7, 20, 14, 45, tzinfo=KST)
    gender = 'female'
    
    print(f"📅 生年月日時: {birth_date.strftime('%Y年%m月%d日 %H時%M分')} KST")
    print(f"👤 性別: {gender}")
    print()
    
    # ステップ1: 四柱計算
    print("【ステップ1】四柱計算")
    print("-" * 40)
    
    calculator = ManseryeokCalculator()
    saju = calculator.calculate_saju(birth_date, gender)
    
    print(f"年柱: {saju.year_stem}{saju.year_branch}")
    print(f"月柱: {saju.month_stem}{saju.month_branch}")
    print(f"日柱: {saju.day_stem}{saju.day_branch}")
    print(f"時柱: {saju.hour_stem}{saju.hour_branch}")
    print(f"完整四柱: {saju.year_stem}{saju.year_branch} {saju.month_stem}{saju.month_branch} {saju.day_stem}{saju.day_branch} {saju.hour_stem}{saju.hour_branch}")
    print()
    
    # ステップ2: 順逆行判定
    print("【ステップ2】順逆行判定")
    print("-" * 40)
    
    stems = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
    year_stem_index = stems.index(saju.year_stem)
    is_yang = (year_stem_index % 2 == 0)
    
    print(f"年干: {saju.year_stem}")
    print(f"年干インデックス: {year_stem_index}")
    print(f"陽干判定: {is_yang} ({'陽干' if is_yang else '陰干'})")
    print(f"性別: {gender}")
    
    # 順逆行ルール：(陽干 and 男性) or (陰干 and 女性) = 順行
    if (is_yang and gender == 'male') or (not is_yang and gender == 'female'):
        direction = '順行'
        direction_en = 'forward'
    else:
        direction = '逆行'
        direction_en = 'backward'
    
    print(f"判定ルール: (陽干 and 男性) or (陰干 and 女性) = 順行")
    print(f"実際: ({is_yang} and {gender == 'male'}) or ({not is_yang} and {gender == 'female'}) = {(is_yang and gender == 'male') or (not is_yang and gender == 'female')}")
    print(f"結果: {direction}")
    print()
    
    # ステップ3: 節入日の特定
    print("【ステップ3】関連節入日の特定")
    print("-" * 40)
    
    # AccurateDaeunCalculatorのデータベースから節入日取得
    daeun_calc = AccurateDaeunCalculator()
    
    if direction_en == 'forward':
        print("順行の場合: 次の節入日を探す")
        jeol_date = daeun_calc._get_next_jeol(birth_date)
        jeol_type = "次の節"
    else:
        print("逆行の場合: 前の節入日を探す")
        jeol_date = daeun_calc._get_previous_jeol(birth_date)
        jeol_type = "前の節"
    
    print(f"生年月日時: {birth_date.strftime('%Y/%m/%d %H:%M:%S')}")
    print(f"{jeol_type}入日: {jeol_date.strftime('%Y/%m/%d %H:%M:%S')}")
    print()
    
    # ステップ4: 日数差計算
    print("【ステップ4】日数差計算")
    print("-" * 40)
    
    time_diff = abs(jeol_date - birth_date)
    days_diff = time_diff.days + (time_diff.seconds / 86400)
    
    print(f"時間差: {time_diff}")
    print(f"日数換算: {time_diff.days}日 + {time_diff.seconds}秒")
    print(f"秒を日数に変換: {time_diff.seconds}秒 ÷ 86400秒/日 = {time_diff.seconds / 86400:.6f}日")
    print(f"総日数差: {time_diff.days} + {time_diff.seconds / 86400:.6f} = {days_diff:.6f}日")
    print()
    
    # ステップ5: 3日=1年法則適用
    print("【ステップ5】3日=1年法則適用")
    print("-" * 40)
    
    precise_years = days_diff / 3
    starting_age_integer = int(precise_years)
    fractional_years = precise_years - starting_age_integer
    
    print(f"3日=1年法則: {days_diff:.6f}日 ÷ 3 = {precise_years:.6f}年")
    print(f"整数部分（起運年齢）: {starting_age_integer}歳")
    print(f"小数部分: {fractional_years:.6f}年")
    print()
    
    # ステップ6: 制限適用
    print("【ステップ6】制限適用")
    print("-" * 40)
    
    final_age = max(1, min(starting_age_integer, 10))
    
    print(f"制限範囲: 1歳 ≤ 起運年齢 ≤ 10歳")
    print(f"計算値: {starting_age_integer}歳")
    print(f"制限後: {final_age}歳")
    
    if final_age != starting_age_integer:
        print(f"⚠️ 制限が適用されました: {starting_age_integer}歳 → {final_age}歳")
    else:
        print("✅ 制限範囲内のため変更なし")
    print()
    
    # ステップ7: 精密大運開始日計算
    print("【ステップ7】精密大運開始日計算")
    print("-" * 40)
    
    # 基準日：生年月日 + 起運年齢（整数部）
    base_start_date = birth_date.replace(year=birth_date.year + final_age)
    
    # 小数部分を日数に変換
    fractional_days = fractional_years * 365.25
    
    # 精密開始日
    precise_start_date = base_start_date + timedelta(days=fractional_days)
    
    print(f"基準開始日: 生年月日 + 起運年齢")
    print(f"           = {birth_date.strftime('%Y年%m月%d日')} + {final_age}年")
    print(f"           = {base_start_date.strftime('%Y年%m月%d日')}")
    print()
    print(f"小数部分の日数換算: {fractional_years:.6f}年 × 365.25日/年 = {fractional_days:.1f}日")
    print()
    print(f"精密大運開始日: 基準開始日 + 小数部分")
    print(f"               = {base_start_date.strftime('%Y年%m月%d日')} + {fractional_days:.1f}日")
    print(f"               = {precise_start_date.strftime('%Y年%m月%d日 %H:%M')}")
    print()
    
    # 計算式まとめ
    print("【計算式まとめ】")
    print("-" * 40)
    print(f"1. 順逆行: 陽干「{saju.year_stem}」+ 女性 → {direction}")
    print(f"2. 節入日: {jeol_type}入日 = {jeol_date.strftime('%Y/%m/%d %H:%M')}")
    print(f"3. 日数差: |{jeol_date.strftime('%m/%d %H:%M')} - {birth_date.strftime('%m/%d %H:%M')}| = {days_diff:.6f}日")
    print(f"4. 起運年: {days_diff:.6f} ÷ 3 = {precise_years:.6f}年 = {final_age}歳 + {fractional_years:.6f}年")
    print(f"5. 開始日: {birth_date.strftime('%Y/%m/%d')} + {final_age}年 + {fractional_days:.1f}日 = {precise_start_date.strftime('%Y/%m/%d %H:%M')}")
    
    return {
        'birth_date': birth_date,
        'saju': saju,
        'direction': direction,
        'jeol_date': jeol_date,
        'days_diff': days_diff,
        'starting_age': final_age,
        'precise_start': precise_start_date
    }

def main():
    result = detailed_female_calculation()
    
    print("\n" + "=" * 80)
    print("📊 最終結果")
    print("=" * 80)
    print(f"生年月日: {result['birth_date'].strftime('%Y年%m月%d日 %H時%M分')}")
    print(f"四柱: {result['saju'].year_stem}{result['saju'].year_branch} {result['saju'].month_stem}{result['saju'].month_branch} {result['saju'].day_stem}{result['saju'].day_branch} {result['saju'].hour_stem}{result['saju'].hour_branch}")
    print(f"大運方向: {result['direction']}")
    print(f"起運年齢: {result['starting_age']}歳")
    print(f"精密大運開始日: {result['precise_start'].strftime('%Y年%m月%d日 %H時%M分')}")

if __name__ == "__main__":
    main()