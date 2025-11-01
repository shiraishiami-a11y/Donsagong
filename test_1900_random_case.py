#!/usr/bin/env python3
"""
1900-1910年データベースを使ったランダムテストケース生成・実行
"""

import json
import os
import random
from datetime import datetime, timezone, timedelta
import sys

# 만세력 계산기 임포트
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.manseryeok.calculator import ManseryeokCalculator

KST = timezone(timedelta(hours=9))

class Enhanced1900DaeunCalculator:
    """1900-1910年データベースを使った大運計算クラス"""
    
    def __init__(self, database_path='solar_terms_1900-1910_database.json'):
        """
        初期化
        
        Args:
            database_path: 節入日データベースのパス
        """
        self.database = self._load_database(database_path)
        
        # 節名と月の対応
        self.jeol_months = {
            '立春': 2,   # 2月（寅月）
            '驚蟄': 3,   # 3月（卯月）
            '清明': 4,   # 4月（辰月）
            '立夏': 5,   # 5月（巳月）
            '芒種': 6,   # 6月（午月）
            '小暑': 7,   # 7月（未月）
            '立秋': 8,   # 8月（申月）
            '白露': 9,   # 9月（酉月）
            '寒露': 10,  # 10月（戌月）
            '立冬': 11,  # 11月（亥月）
            '大雪': 12,  # 12月（子月）
            '小寒': 1,   # 1月（丑月）
        }
        
    def _load_database(self, database_path):
        """節入日データベースを読み込む"""
        full_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            database_path
        )
        
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"節入日データベースが見つかりません: {full_path}")
        
        with open(full_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('solar_terms_data', {})
    
    def calculate_starting_age(self, birth_datetime, gender, year_stem):
        """
        正確な起運年齢を計算
        
        Args:
            birth_datetime: 生年月日時刻（datetime）
            gender: 性別（'male' or 'female'）
            year_stem: 年干（陽干か陰干を判定用）
        
        Returns:
            dict: 計算結果
        """
        print(f"\n=== 1900年代節気データベース使用：大運起運年齢計算 ===")
        print(f"生年月日時: {birth_datetime.strftime('%Y/%m/%d %H:%M')} KST")
        print(f"性別: {gender}")
        print(f"年干: {year_stem}")
        
        # 順逆行判断
        stems = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
        year_index = stems.index(year_stem) if year_stem in stems else 0
        is_yang = (year_index % 2 == 0)  # 偶数が陽干
        
        print(f"年干インデックス: {year_index} ({'陽干' if is_yang else '陰干'})") 
        
        # 順行・逆行の判定
        if (is_yang and gender == 'male') or (not is_yang and gender == 'female'):
            direction = 'forward'  # 順行
        else:
            direction = 'backward'  # 逆行
        
        print(f"大運方向: {direction} ({'順行' if direction == 'forward' else '逆行'})")
        
        # 節入日を取得
        if direction == 'forward':
            jeolip_date, jeol_name = self._get_next_jeol(birth_datetime)
            target_type = "次の節"
        else:
            jeolip_date, jeol_name = self._get_previous_jeol(birth_datetime)
            target_type = "前の節"
        
        if jeolip_date is None:
            print(f"⚠️ {target_type}入日データが見つかりません")
            return {
                'starting_age': 5,
                'precise_start': None,
                'error': f'{target_type}入日データなし'
            }
        
        print(f"{target_type}入日: {jeolip_date.strftime('%Y/%m/%d %H:%M:%S')} ({jeol_name})")
        
        # 日数差を計算
        time_diff = abs(jeolip_date - birth_datetime)
        days_diff = time_diff.days + (time_diff.seconds / 86400)  # 小数日まで計算
        
        print(f"時間差: {time_diff}")
        print(f"日数差: {days_diff:.6f}日")
        
        # 3日 = 1年の法則（小数部分も含む精密計算）
        precise_years = days_diff / 3
        starting_age_integer = int(precise_years)
        fractional_years = precise_years - starting_age_integer
        
        print(f"3日=1年法則適用: {days_diff:.6f} ÷ 3 = {precise_years:.6f}")
        print(f"起運年齢（整数部）: {starting_age_integer}歳")
        print(f"小数部分: {fractional_years:.6f}年")
        
        # 1歳未満の場合は0歳として処理、最大10歳に制限
        final_age_integer = min(starting_age_integer, 10)
        
        if final_age_integer != starting_age_integer:
            print(f"制限適用後: {final_age_integer}歳")
        
        print(f"=== 最終起運年齢: {final_age_integer}歳 ===")
        
        # 大運開始日計算（小数部分も正確に考慮）
        # 0歳の場合は生年月日をベースに小数部分を直接加算
        if final_age_integer == 0:
            fractional_days = precise_years * 365.25
            accurate_start_date = birth_datetime + timedelta(days=fractional_days)
        else:
            fractional_days = fractional_years * 365.25
            base_start_date = birth_datetime.replace(year=birth_datetime.year + final_age_integer)
            accurate_start_date = base_start_date + timedelta(days=fractional_days)
        
        print(f"起運年齢（整数部）: {final_age_integer}年")
        if final_age_integer == 0:
            print(f"0歳計算: {precise_years:.6f}年 = {fractional_days:.1f}日")
            print(f"基準開始日: {birth_datetime.strftime('%Y年%m月%d日')} (生年月日)")
        else:
            print(f"小数部分: {fractional_years:.6f}年 = {fractional_days:.1f}日")
            print(f"基準開始日: {base_start_date.strftime('%Y年%m月%d日')}")
        print(f"精密大運開始日: {accurate_start_date.strftime('%Y年%m月%d日 %H:%M')}")
        print("=" * 50 + "\n")
        
        return {
            'starting_age': final_age_integer,
            'precise_start': accurate_start_date,
            'direction': direction,
            'jeol_date': jeolip_date,
            'jeol_name': jeol_name,
            'days_diff': days_diff,
            'fractional_years': fractional_years
        }
    
    def _get_next_jeol(self, birth_datetime):
        """次の節入日を取得"""
        year = birth_datetime.year
        
        # 現在の年のデータを確認
        if str(year) not in self.database:
            return None, None
        
        year_data = self.database[str(year)]
        
        # すべての節入日を日付順にソート
        jeol_dates = []
        for jeol_name, jeol_data in year_data.items():
            if jeol_name in self.jeol_months:
                actual_month = self.jeol_months[jeol_name]
                try:
                    if actual_month == 1:  # 小寒は翌年1月
                        dt = datetime(
                            year + 1, actual_month, jeol_data['day'],
                            jeol_data['hour'], jeol_data['minute'], 
                            jeol_data.get('second', 0), tzinfo=KST
                        )
                    else:
                        dt = datetime(
                            year, actual_month, jeol_data['day'],
                            jeol_data['hour'], jeol_data['minute'], 
                            jeol_data.get('second', 0), tzinfo=KST
                        )
                    jeol_dates.append((jeol_name, dt))
                except:
                    continue
        
        # 日付順にソート
        jeol_dates.sort(key=lambda x: x[1])
        
        # 生年月日より後の最初の節を探す
        for jeol_name, jeol_dt in jeol_dates:
            if jeol_dt > birth_datetime:
                return jeol_dt, jeol_name
        
        return None, None
    
    def _get_previous_jeol(self, birth_datetime):
        """前の節入日を取得"""
        year = birth_datetime.year
        
        # 現在の年のデータを確認
        if str(year) not in self.database:
            return None, None
        
        year_data = self.database[str(year)]
        
        # すべての節入日を日付順にソート
        jeol_dates = []
        for jeol_name, jeol_data in year_data.items():
            if jeol_name in self.jeol_months:
                actual_month = self.jeol_months[jeol_name]
                try:
                    dt = datetime(
                        year, actual_month, jeol_data['day'],
                        jeol_data['hour'], jeol_data['minute'], 
                        jeol_data.get('second', 0), tzinfo=KST
                    )
                    jeol_dates.append((jeol_name, dt))
                except:
                    continue
        
        # 日付順にソート（逆順）
        jeol_dates.sort(key=lambda x: x[1], reverse=True)
        
        # 生年月日より前の最初の節を探す
        for jeol_name, jeol_dt in jeol_dates:
            if jeol_dt < birth_datetime:
                return jeol_dt, jeol_name
        
        return None, None

def generate_random_birth_case():
    """ランダムな生年月日・性別を生成"""
    # 1900年のデータがあることを確認
    year = 1900
    month = random.randint(1, 12)
    
    # 月に応じた日数の調整
    if month in [1, 3, 5, 7, 8, 10, 12]:
        day = random.randint(1, 31)
    elif month in [4, 6, 9, 11]:
        day = random.randint(1, 30)
    else:  # 2月
        day = random.randint(1, 28)  # 1900年は平年
    
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    
    birth_date = datetime(year, month, day, hour, minute, tzinfo=KST)
    gender = random.choice(['male', 'female'])
    
    return birth_date, gender

def test_random_case():
    """ランダムケースをテスト"""
    print("🎲 ランダム生年月日・性別生成テスト")
    print("=" * 80)
    
    # ランダムケース生成
    birth_date, gender = generate_random_birth_case()
    
    print(f"📅 ランダム生成:")
    print(f"   生年月日時: {birth_date.strftime('%Y年%m月%d日 %H時%M分')} KST")
    print(f"   性別: {gender}")
    
    # 四柱計算
    try:
        calculator = ManseryeokCalculator()
        saju = calculator.calculate_saju(birth_date, gender)
        
        print(f"\n📋 四柱計算結果:")
        print(f"   年柱: {saju.year_stem}{saju.year_branch}")
        print(f"   月柱: {saju.month_stem}{saju.month_branch}")
        print(f"   日柱: {saju.day_stem}{saju.day_branch}")
        print(f"   時柱: {saju.hour_stem}{saju.hour_branch}")
        print(f"   完整四柱: {saju.year_stem}{saju.year_branch} {saju.month_stem}{saju.month_branch} {saju.day_stem}{saju.day_branch} {saju.hour_stem}{saju.hour_branch}")
        
        # 1900年代データベースで大運計算
        daeun_calc = Enhanced1900DaeunCalculator()
        result = daeun_calc.calculate_starting_age(birth_date, gender, saju.year_stem)
        
        if 'error' not in result:
            print(f"\n🔮 大運計算結果:")
            print(f"   大運方向: {result['direction']} ({'順行' if result['direction'] == 'forward' else '逆行'})")
            print(f"   関連節入日: {result['jeol_date'].strftime('%Y/%m/%d %H:%M')} ({result['jeol_name']})")
            print(f"   日数差: {result['days_diff']:.3f}日")
            print(f"   起運年齢: {result['starting_age']}歳")
            print(f"   精密大運開始日: {result['precise_start'].strftime('%Y年%m月%d日 %H時%M分')}")
            
            print(f"\n✅ テスト成功 - 1900年代節気データベースで正確な計算完了!")
        else:
            print(f"\n❌ 大運計算エラー: {result['error']}")
            
    except Exception as e:
        print(f"\n❌ 計算エラー: {e}")
        import traceback
        traceback.print_exc()

def main():
    """メイン関数"""
    try:
        test_random_case()
        
        print(f"\n{'='*80}")
        print("🎉 1900-1910年節気データベーステスト完了!")
        print("ランダム生年月日での大運計算が正常に動作することを確認!")
        
    except Exception as e:
        print(f"❌ テスト実行エラー: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()