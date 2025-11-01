#!/usr/bin/env python3
"""
1908年10月10日10時生まれ男子の詳細計算
"""

from datetime import datetime, timezone, timedelta
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.manseryeok.calculator import ManseryeokCalculator

KST = timezone(timedelta(hours=9))

def calculate_1908_male():
    """1908年10月10日男子の詳細計算"""
    
    print("=" * 80)
    print("🔮 1908年10月10日10時生まれ男子の完全計算")
    print("=" * 80)
    
    # 基本情報
    birth_date = datetime(1908, 10, 10, 10, 0, tzinfo=KST)
    gender = 'male'
    
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
    
    print(f"年干: {saju.year_stem} (インデックス: {year_stem_index})")
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
    
    # ステップ3: 節入日の推定（1908年データがないため）
    print("【ステップ3】関連節入日の推定")
    print("-" * 40)
    
    # 1908年10月10日の場合、寒露（10月8日頃）と立冬（11月7日頃）の間
    if direction_en == 'forward':
        print("順行の場合: 次の節入日を探す")
        # 立冬（11月7日頃）を推定
        estimated_lidong = datetime(1908, 11, 7, 15, 0, tzinfo=KST)  # 推定
        jeol_name = "立冬"
        jeol_type = "次の節"
        jeol_date = estimated_lidong
    else:
        print("逆行の場合: 前の節入日を探す")  
        # 寒露（10月8日頃）を推定
        estimated_hanlu = datetime(1908, 10, 8, 12, 0, tzinfo=KST)  # 推定
        jeol_name = "寒露"
        jeol_type = "前の節"
        jeol_date = estimated_hanlu
    
    print(f"生年月日時: {birth_date.strftime('%Y/%m/%d %H:%M:%S')}")
    print(f"{jeol_type}入日: {jeol_date.strftime('%Y/%m/%d %H:%M:%S')} ({jeol_name}・推定)")
    print("⚠️ 1908年の正確な節入日データがないため推定値を使用")
    print()
    
    # ステップ4: 日数差計算
    print("【ステップ4】日数差計算")
    print("-" * 40)
    
    if direction_en == 'forward':
        time_diff = jeol_date - birth_date
    else:
        time_diff = birth_date - jeol_date
        
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
    
    final_age = max(0, min(starting_age_integer, 10))
    
    print(f"制限範囲: 0歳 ≤ 起運年齢 ≤ 10歳")
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
    
    if final_age == 0:
        # 0歳の場合は生年月日をベースに計算
        fractional_days = precise_years * 365.25
        precise_start_date = birth_date + timedelta(days=fractional_days)
        
        print(f"0歳計算: 生年月日 + 全期間")
        print(f"期間: {precise_years:.6f}年 = {fractional_days:.1f}日")
        print(f"精密大運開始日: {birth_date.strftime('%Y年%m月%d日')} + {fractional_days:.1f}日")
        print(f"                = {precise_start_date.strftime('%Y年%m月%d日 %H:%M')}")
    else:
        # 通常計算
        base_start_date = birth_date.replace(year=birth_date.year + final_age)
        fractional_days = fractional_years * 365.25
        precise_start_date = base_start_date + timedelta(days=fractional_days)
        
        print(f"基準開始日: 生年月日 + 起運年齢")
        print(f"           = {birth_date.strftime('%Y年%m月%d日')} + {final_age}年")
        print(f"           = {base_start_date.strftime('%Y年%m月%d日')}")
        print(f"小数部分の日数換算: {fractional_years:.6f}年 × 365.25日/年 = {fractional_days:.1f}日")
        print(f"精密大運開始日: {base_start_date.strftime('%Y年%m月%d日')} + {fractional_days:.1f}日")
        print(f"                = {precise_start_date.strftime('%Y年%m月%d日 %H:%M')}")
    print()
    
    # 計算式まとめ
    print("【計算式まとめ】")
    print("-" * 40)
    print(f"1. 순역행: 음간「{saju.year_stem}」+ 남성 → {direction}")
    print(f"2. 절입일: {jeol_type}입일 = {jeol_date.strftime('%Y/%m/%d %H:%M')} ({jeol_name})")
    print(f"3. 일수차: {days_diff:.6f}일")
    print(f"4. 기운년: {days_diff:.6f} ÷ 3 = {precise_years:.6f}년 = {final_age}세")
    print(f"5. 개시일: {precise_start_date.strftime('%Y/%m/%d')}")
    
    return {
        'birth_date': birth_date,
        'saju': saju,
        'direction': direction,
        'jeol_date': jeol_date,
        'jeol_name': jeol_name,
        'days_diff': days_diff,
        'starting_age': final_age,
        'precise_start': precise_start_date
    }

def main():
    result = calculate_1908_male()
    
    print(f"\n{'='*80}")
    print("📊 最終結果")
    print("="*80)
    print(f"生年月日: {result['birth_date'].strftime('%Y年%m月%d日 %H時%M分')}")
    print(f"四柱: {result['saju'].year_stem}{result['saju'].year_branch} {result['saju'].month_stem}{result['saju'].month_branch} {result['saju'].day_stem}{result['saju'].day_branch} {result['saju'].hour_stem}{result['saju'].hour_branch}")
    print(f"大運方向: {result['direction']}")
    print(f"起運年齢: {result['starting_age']}歳")
    print(f"精密大運開始日: {result['precise_start'].strftime('%Y年%m月%d日 %H時%M分')}")
    print()
    print("⚠️ 注意: 1908年の正確な節入日データベースがないため推定値を使用しました。")
    print("   より正確な計算には1908年の節気データが必要です。")

if __name__ == "__main__":
    main()