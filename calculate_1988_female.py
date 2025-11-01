#!/usr/bin/env python3
"""
1988年4月18日女性の大運計算
"""

from datetime import datetime, timezone, timedelta
import sys
import os

# 만세력 계산기 임포트
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.manseryeok.calculator import ManseryeokCalculator

KST = timezone(timedelta(hours=9))

def calculate_1988_female():
    """1988年4月18日女性の大運計算"""
    
    print("=" * 80)
    print("🔍 1988年4月18日女性の大運計算")
    print("=" * 80)
    
    # 基本情報
    birth_date = datetime(1988, 4, 18, 12, 0, tzinfo=KST)  # 12時と仮定
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
    print(f"완전사주: {saju.year_stem}{saju.year_branch} {saju.month_stem}{saju.month_branch} {saju.day_stem}{saju.day_branch} {saju.hour_stem}{saju.hour_branch}")
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
    
    # ステップ3: 関連節入日の特定（1988年は1986年データがないので推定）
    print("【ステップ3】関連節入日の特定")
    print("-" * 40)
    
    # 1988年4月18日の場合、清明（4月4日頃）と立夏（5月5日頃）の間
    if direction_en == 'forward':
        print("順行の場合: 次の節入日を探す")
        # 立夏（5月5日頃）を推定
        estimated_lichun = datetime(1988, 5, 5, 15, 0, tzinfo=KST)  # 推定
        jeol_name = "立夏"
        jeol_type = "次の節"
    else:
        print("逆行の場合: 前の節入日を探す")  
        # 清明（4月4日頃）を推定
        estimated_qingming = datetime(1988, 4, 4, 22, 30, tzinfo=KST)  # 推定
        jeol_name = "清明"
        jeol_type = "前の節"
        
    jeol_date = estimated_lichun if direction_en == 'forward' else estimated_qingming
    
    print(f"生年月日時: {birth_date.strftime('%Y/%m/%d %H:%M:%S')}")
    print(f"{jeol_type}入日: {jeol_date.strftime('%Y/%m/%d %H:%M:%S')} ({jeol_name}・推定)")
    print("⚠️ 1988年の正確な節入日データがないため推定値を使用")
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
    
    # 계산식 정리
    print("【計算式まとめ】")
    print("-" * 40)
    print(f"1. 순역행: {('음간' if not is_yang else '양간')}「{saju.year_stem}」+ 여성 → {direction}")
    print(f"2. 절입일: {jeol_type}입일 = {jeol_date.strftime('%Y/%m/%d %H:%M')} ({jeol_name})")
    print(f"3. 일수차: |{jeol_date.strftime('%m/%d %H:%M')} - {birth_date.strftime('%m/%d %H:%M')}| = {days_diff:.6f}일")
    print(f"4. 기운년: {days_diff:.6f} ÷ 3 = {precise_years:.6f}년 = {final_age}세 + {fractional_years:.6f}년")
    print(f"5. 개시일: {birth_date.strftime('%Y/%m/%d')} + {final_age}년 + {fractional_days:.1f}일 = {precise_start_date.strftime('%Y/%m/%d %H:%M')}")
    
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
    result = calculate_1988_female()
    
    print("\n" + "=" * 80)
    print("📊 최종결과")
    print("=" * 80)
    print(f"생년월일: {result['birth_date'].strftime('%Y년%m월%d일 %H시%M분')}")
    print(f"사주: {result['saju'].year_stem}{result['saju'].year_branch} {result['saju'].month_stem}{result['saju'].month_branch} {result['saju'].day_stem}{result['saju'].day_branch} {result['saju'].hour_stem}{result['saju'].hour_branch}")
    print(f"대운방향: {result['direction']}")
    print(f"기운연령: {result['starting_age']}세")
    print(f"정밀대운개시일: {result['precise_start'].strftime('%Y년%m월%d일 %H시%M분')}")
    print()
    print("⚠️ 주의: 1988년의 정확한 절입일 데이터베이스가 없어 추정값을 사용했습니다.")
    print("   실제 사용시에는 1988년의 정확한 절기 데이터가 필요합니다.")

if __name__ == "__main__":
    main()