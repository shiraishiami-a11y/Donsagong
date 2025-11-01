#!/usr/bin/env python3
"""
lunar-pythonライブラリを使用して1906年6月6日6時の命式を計算
"""

from datetime import datetime
import sys

# lunar-pythonライブラリの確認とインストール指示
try:
    from lunar_python import Solar, Lunar, EightChar
    print("✅ lunar-pythonライブラリが見つかりました")
except ImportError:
    print("❌ lunar-pythonライブラリがインストールされていません")
    print("インストール方法: pip install lunar-python")
    sys.exit(1)

def calculate_with_lunar():
    """lunar-pythonで1906年6月6日6時生まれ女子の命式を計算"""
    
    print("="*80)
    print("🌙 lunar-pythonライブラリによる命式計算")
    print("="*80)
    
    # 生年月日時を設定
    year = 1906
    month = 6
    day = 6
    hour = 6
    minute = 0
    
    print(f"生年月日時: {year}年{month}月{day}日 {hour}時{minute}分")
    print()
    
    try:
        # Solarオブジェクトを作成
        solar = Solar.fromYmdHms(year, month, day, hour, minute, 0)
        
        # 旧暦に変換
        lunar = solar.getLunar()
        
        # 八字（四柱）を取得
        eight_char = lunar.getEightChar()
        
        print("【lunar-pythonの計算結果】")
        print("-"*40)
        
        # 年柱
        year_gan = eight_char.getYearGan()
        year_zhi = eight_char.getYearZhi()
        print(f"年柱: {year_gan}{year_zhi}")
        
        # 月柱
        month_gan = eight_char.getMonthGan()
        month_zhi = eight_char.getMonthZhi()
        print(f"月柱: {month_gan}{month_zhi}")
        
        # 日柱
        day_gan = eight_char.getDayGan()
        day_zhi = eight_char.getDayZhi()
        print(f"日柱: {day_gan}{day_zhi}")
        
        # 時柱
        hour_gan = eight_char.getTimeGan()
        hour_zhi = eight_char.getTimeZhi()
        print(f"時柱: {hour_gan}{hour_zhi}")
        
        print()
        print(f"完整四柱: {year_gan}{year_zhi} {month_gan}{month_zhi} {day_gan}{day_zhi} {hour_gan}{hour_zhi}")
        
        # 節気情報も取得
        print()
        print("【節気情報】")
        print("-"*40)
        
        # 現在の節気
        jie_qi = solar.getJieQi()
        print(f"当日の節気: {jie_qi if jie_qi else 'なし'}")
        
        # 前後の節気
        prev_jie = solar.getPrevJie()
        prev_qi = solar.getPrevQi()
        next_jie = solar.getNextJie()
        next_qi = solar.getNextQi()
        
        if prev_jie:
            print(f"前の節: {prev_jie.getName()} ({prev_jie.getSolar().toYmdHms()})")
        if prev_qi:
            print(f"前の気: {prev_qi.getName()} ({prev_qi.getSolar().toYmdHms()})")
        if next_jie:
            print(f"次の節: {next_jie.getName()} ({next_jie.getSolar().toYmdHms()})")
        if next_qi:
            print(f"次の気: {next_qi.getName()} ({next_qi.getSolar().toYmdHms()})")
            
    except Exception as e:
        print(f"❌ エラー: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    print("【比較】")
    print("-"*40)
    print("ManseryeokCalculator: 丙午 甲午 辛巳 辛卯")
    print("lunar-python: （上記の結果）")
    print()
    print("月柱に注目: ")
    print("  ManseryeokCalculator: 甲午")
    print(f"  lunar-python: {month_gan}{month_zhi if 'month_gan' in locals() else '計算失敗'}")

def main():
    calculate_with_lunar()

if __name__ == "__main__":
    main()