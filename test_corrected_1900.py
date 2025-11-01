#!/usr/bin/env python3
"""
修正版：正しい年干「庚」での1900年大運計算テスト
"""

from datetime import datetime, timezone, timedelta
import json
import os

KST = timezone(timedelta(hours=9))

def corrected_daeun_calculation():
    """正しい年干での大運計算"""
    print("🔧 修正版：1900年12月10日女性の大運計算")
    print("=" * 80)
    
    # テストケース
    birth_date = datetime(1900, 12, 10, 13, 10, tzinfo=KST)
    gender = 'female'
    correct_year_stem = '庚'  # 正しい年干
    
    print(f"📅 生年月日時: {birth_date.strftime('%Y年%m月%d日 %H時%M分')} KST")
    print(f"👤 性別: {gender}")
    print(f"🔧 修正年干: {correct_year_stem} (庚子年)")
    print(f"💡 期待値: 生後0年10ヶ月、1901年10月25日ごろ")
    print()
    
    # ステップ1: 順逆行判定
    print("【ステップ1】順逆行判定")
    print("-" * 40)
    
    stems = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
    year_index = stems.index(correct_year_stem)
    is_yang = (year_index % 2 == 0)
    
    print(f"年干: {correct_year_stem} (インデックス: {year_index})")
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
    
    # ステップ2: 関連節入日の特定
    print("【ステップ2】関連節入日の特定")
    print("-" * 40)
    
    # 1900年節気データを読み込み
    database_path = 'solar_terms_1900-1910_database.json'
    with open(database_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    year_1900 = data['solar_terms_data']['1900']
    
    if direction_en == 'forward':
        print("順行の場合: 次の節入日を探す")
        # 小寒（1月）
        xiaoshi = year_1900['小寒']
        jeol_date = datetime(1901, 1, xiaoshi['day'], xiaoshi['hour'], xiaoshi['minute'], tzinfo=KST)
        jeol_name = "小寒"
        jeol_type = "次の節"
    else:
        print("逆行の場合: 前の節入日を探す")
        # 大雪（12月）
        daxue = year_1900['大雪']
        jeol_date = datetime(1900, 12, daxue['day'], daxue['hour'], daxue['minute'], tzinfo=KST)
        jeol_name = "大雪"
        jeol_type = "前の節"
    
    print(f"生年月日時: {birth_date.strftime('%Y/%m/%d %H:%M:%S')}")
    print(f"{jeol_type}入日: {jeol_date.strftime('%Y/%m/%d %H:%M:%S')} ({jeol_name})")
    print()
    
    # ステップ3: 日数差計算
    print("【ステップ3】日数差計算")
    print("-" * 40)
    
    if direction_en == 'forward':
        time_diff = jeol_date - birth_date  # 順行
    else:
        time_diff = birth_date - jeol_date  # 逆行
    
    days_diff = time_diff.days + (time_diff.seconds / 86400)
    
    print(f"時間差: {time_diff}")
    print(f"日数換算: {time_diff.days}日 + {time_diff.seconds}秒")
    print(f"秒を日数に変換: {time_diff.seconds}秒 ÷ 86400秒/日 = {time_diff.seconds / 86400:.6f}日")
    print(f"総日数差: {time_diff.days} + {time_diff.seconds / 86400:.6f} = {days_diff:.6f}日")
    print()
    
    # ステップ4: 3日=1年法則適用
    print("【ステップ4】3日=1年法則適用")
    print("-" * 40)
    
    precise_years = days_diff / 3
    starting_age_integer = int(precise_years)
    fractional_years = precise_years - starting_age_integer
    
    print(f"3日=1年法則: {days_diff:.6f}日 ÷ 3 = {precise_years:.6f}年")
    print(f"整数部分（起運年齢）: {starting_age_integer}歳")
    print(f"小数部分: {fractional_years:.6f}年")
    print()
    
    # ステップ5: 制限適用
    print("【ステップ5】制限適用")
    print("-" * 40)
    
    final_age = min(starting_age_integer, 10)  # 0歳も許可
    
    print(f"制限範囲: 0歳 ≤ 起運年齢 ≤ 10歳")
    print(f"計算値: {starting_age_integer}歳")
    print(f"制限後: {final_age}歳")
    
    if final_age != starting_age_integer:
        print(f"⚠️ 制限が適用されました: {starting_age_integer}歳 → {final_age}歳")
    else:
        print("✅ 制限範囲内のため変更なし")
    print()
    
    # ステップ6: 精密大運開始日計算
    print("【ステップ6】精密大運開始日計算")
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
    print(f"1. 순역행: 양간「{correct_year_stem}」+ 여성 → {direction}")
    print(f"2. 절입일: {jeol_type}입일 = {jeol_date.strftime('%Y/%m/%d %H:%M')} ({jeol_name})")
    print(f"3. 일수차: {days_diff:.6f}일")
    print(f"4. 기운년: {days_diff:.6f} ÷ 3 = {precise_years:.6f}년 = {final_age}세")
    print(f"5. 개시일: {precise_start_date.strftime('%Y/%m/%d')}")
    
    # 期待値との比較
    print()
    print("【期待値との比較】")
    print("-" * 40)
    expected_date = datetime(1901, 10, 25, tzinfo=KST)
    diff_days = (precise_start_date - expected_date).days
    
    print(f"計算結果: {precise_start_date.strftime('%Y年%m月%d日')}")
    print(f"期待値: {expected_date.strftime('%Y年%m月%d日')}ごろ")
    print(f"誤差: {abs(diff_days)}日")
    
    accuracy = (1 - abs(diff_days) / 365) * 100
    print(f"精度: {accuracy:.1f}%")
    
    if abs(diff_days) <= 15:
        print("✅ 高精度！(15日以内)")
    elif abs(diff_days) <= 30:
        print("✅ 良好精度(30日以内)")
    else:
        print("⚠️ 精度要改善")
    
    return {
        'birth_date': birth_date,
        'correct_year_stem': correct_year_stem,
        'direction': direction,
        'jeol_date': jeol_date,
        'jeol_name': jeol_name,
        'days_diff': days_diff,
        'starting_age': final_age,
        'precise_start': precise_start_date,
        'accuracy': accuracy
    }

def main():
    result = corrected_daeun_calculation()
    
    print(f"\\n{'='*80}")
    print("🎉 修正版テスト完了!")
    print(f"正しい年干「{result['correct_year_stem']}」により大幅精度向上!")
    print(f"最終精度: {result['accuracy']:.1f}%")

if __name__ == "__main__":
    main()