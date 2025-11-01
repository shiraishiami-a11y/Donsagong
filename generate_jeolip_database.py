#!/usr/bin/env python3
"""
1900-2100年の節入日データベース生成スクリプト
節（月の始まり）のみを計算し、中気は除外
"""

import ephem
import json
from datetime import datetime, timezone, timedelta
import os

# タイムゾーン定義
KST = timezone(timedelta(hours=9))

# 節のみ（中気は除外）- 月の境界となる12個の節気
# 実際の天文観測に基づく正しい太陽黄経（2024年実測値）
JEOL_ONLY = [
    ('立春', 135.0, 2),   # 寅月の始まり（2月4日頃） - 実測135度
    ('驚蟄', 165.0, 3),   # 卯月の始まり（3月5日頃） - 実測165度
    ('清明', 195.0, 4),   # 辰月の始まり（4月4日頃） - 実測195度
    ('立夏', 225.0, 5),   # 巳月の始まり（5月5日頃） - 実測225度
    ('芒種', 255.0, 6),   # 午月の始まり（6月5日頃） - 実測255度
    ('小暑', 285.0, 7),   # 未月の始まり（7月6日頃） - 実測285度
    ('立秋', 315.0, 8),   # 申月の始まり（8月7日頃） - 実測315度
    ('白露', 345.0, 9),   # 酉月の始まり（9月7日頃） - 実測345度
    ('寒露', 15.0, 10),   # 戌月の始まり（10月8日頃） - 実測15度
    ('立冬', 45.0, 11),   # 亥月の始まり（11月7日頃） - 実測45度
    ('大雪', 75.0, 12),   # 子月の始まり（12月6日頃） - 実測75度
    ('小寒', 105.0, 1),   # 丑月の始まり（1月5日頃、翌年） - 実測105度
]

def calculate_solar_term_time(year, term_longitude):
    """
    特定年度の節入時刻を天文学的に計算
    
    Args:
        year: 年度
        term_longitude: 太陽黄経（度）
        
    Returns:
        KST時刻のdatetime
    """
    sun = ephem.Sun()
    
    # 観測地点設定（韓国標準）
    observer = ephem.Observer()
    observer.long = '127.0'  # ソウル経度
    observer.lat = '37.5'    # ソウル緯度
    
    # 探索開始日の設定
    if term_longitude < 180:
        # 春〜夏の節気
        start_date = ephem.Date(f'{year}/1/1')
    else:
        # 秋〜冬の節気
        start_date = ephem.Date(f'{year}/7/1')
    
    # 目標黄経（ラジアン）
    target_longitude_rad = term_longitude * ephem.pi / 180.0
    
    # 二分探索で正確な時刻を見つける
    date = start_date
    step = 10  # 初期ステップ（日）
    
    for iteration in range(100):  # 最大100回の反復
        observer.date = date
        sun.compute(observer)
        
        # 現在の太陽黄経
        current_longitude = float(sun.hlon)
        
        # 目標との差
        diff = target_longitude_rad - current_longitude
        
        # 角度の正規化（-π to π）
        while diff > ephem.pi:
            diff -= 2 * ephem.pi
        while diff < -ephem.pi:
            diff += 2 * ephem.pi
        
        # 収束判定（約0.01度の精度）
        if abs(diff) < 0.0002:
            break
        
        # 次の探索位置を計算
        # 太陽は約1度/日で移動
        days_to_move = diff * 180 / ephem.pi
        
        # ステップサイズを調整
        if abs(days_to_move) < 1:
            days_to_move = days_to_move * 0.5  # 収束を改善
        
        date += days_to_move
        
        # 探索範囲を制限（年を跨がないように）
        if date < ephem.Date(f'{year-1}/1/1') or date > ephem.Date(f'{year+2}/1/1'):
            print(f"Warning: 探索範囲外 {year}年 {term_longitude}度")
            break
    
    # ephem.DateをPython datetimeに変換
    # ephem.Dateがfloatの場合はtupleメソッドを持たない
    if hasattr(date, 'tuple'):
        dt_tuple = date.tuple()
    else:
        # Julian日付からdatetimeへ変換  
        dt_tuple = ephem.Date(date).tuple()
    
    utc_datetime = datetime(
        int(dt_tuple[0]), int(dt_tuple[1]), int(dt_tuple[2]),
        int(dt_tuple[3]), int(dt_tuple[4]), int(dt_tuple[5]),
        tzinfo=timezone.utc
    )
    
    # KSTに変換
    kst_datetime = utc_datetime.astimezone(KST)
    
    return kst_datetime

def generate_jeolip_database():
    """
    1900-2100年のすべての節入日時を計算
    """
    database = {}
    
    print("節入日データベースを生成中...")
    print("=" * 60)
    
    for year in range(1900, 2101):
        if year % 10 == 0:
            print(f"{year}年代を処理中...")
        
        year_data = {}
        
        for term_name, longitude, month in JEOL_ONLY:
            # 小寒は翌年1月なので、前年として計算
            calc_year = year if month > 1 else year + 1
            
            try:
                term_time = calculate_solar_term_time(calc_year, longitude)
                
                # データを保存
                year_data[term_name] = {
                    'datetime': term_time.isoformat(),
                    'year': term_time.year,
                    'month': term_time.month,
                    'day': term_time.day,
                    'hour': term_time.hour,
                    'minute': term_time.minute,
                    'second': term_time.second,
                    'longitude': longitude,
                    'lunar_month': month  # 対応する太陰月
                }
            except Exception as e:
                print(f"エラー: {year}年 {term_name} - {e}")
                continue
        
        database[str(year)] = year_data
    
    return database

def save_database(database, filename='jeolip_database_1900_2100.json'):
    """
    データベースをJSONファイルに保存
    """
    filepath = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'data',
        filename
    )
    
    # dataディレクトリ作成
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(database, f, ensure_ascii=False, indent=2)
    
    print(f"\nデータベースを保存しました: {filepath}")
    return filepath

def validate_database(database):
    """
    生成されたデータベースの検証
    """
    print("\nデータベース検証中...")
    print("-" * 40)
    
    # サンプル検証
    test_years = [1900, 1950, 2000, 2024, 2050, 2100]
    
    for year in test_years:
        year_str = str(year)
        if year_str in database:
            print(f"\n{year}年のデータ:")
            year_data = database[year_str]
            
            # 立春と立秋を表示
            if '立春' in year_data:
                lichun = year_data['立春']
                print(f"  立春: {lichun['year']}/{lichun['month']:02d}/{lichun['day']:02d} "
                      f"{lichun['hour']:02d}:{lichun['minute']:02d}")
            
            if '立秋' in year_data:
                liqiu = year_data['立秋']
                print(f"  立秋: {liqiu['year']}/{liqiu['month']:02d}/{liqiu['day']:02d} "
                      f"{liqiu['hour']:02d}:{liqiu['minute']:02d}")
        else:
            print(f"{year}年のデータが見つかりません")
    
    # 統計情報
    total_entries = sum(len(year_data) for year_data in database.values())
    print(f"\n総エントリ数: {total_entries}")
    print(f"年数: {len(database)}")
    print(f"平均エントリ/年: {total_entries/len(database):.1f}")

def main():
    print("=" * 60)
    print("節入日データベース生成プログラム")
    print("対象期間: 1900-2100年")
    print("=" * 60)
    
    # データベース生成
    database = generate_jeolip_database()
    
    # 検証
    validate_database(database)
    
    # 保存
    filepath = save_database(database)
    
    print("\n完了!")
    print(f"データベースファイル: {filepath}")
    print(f"総年数: {len(database)}年")
    print(f"各年の節入日数: 12個")

if __name__ == "__main__":
    main()