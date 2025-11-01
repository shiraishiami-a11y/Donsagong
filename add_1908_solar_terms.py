#!/usr/bin/env python3
"""
1908년 절기 데이터 수동 추가
기존 1900년 데이터와 표준 패턴을 바탕으로 추정
"""

import json
import os

def add_1908_solar_terms():
    """1908년 절기 데이터를 기존 데이터베이스에 추가"""
    
    # 기존 데이터베이스 로드
    db_path = 'solar_terms_1900-1910_database.json'
    
    if os.path.exists(db_path):
        with open(db_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        print("❌ 기존 데이터베이스 파일이 없습니다.")
        return
    
    # 1908년 절기 데이터 (표준 패턴 기반 추정)
    solar_terms_1908 = {
        "立春": {
            "chinese_name": "立春",
            "english_name": "Lichun",
            "meaning": "Beginning of Spring",
            "month": "February",
            "day": 4,
            "hour": 14,
            "minute": 30,
            "second": 0,
            "full_datetime": "1908-02-04 14:30:00",
            "source": "Pattern-based estimation from 1900 data"
        },
        "驚蟄": {
            "chinese_name": "驚蟄",
            "english_name": "Jingzhe",
            "meaning": "Awakening of Insects",
            "month": "March",
            "day": 6,
            "hour": 9,
            "minute": 15,
            "second": 0,
            "full_datetime": "1908-03-06 09:15:00",
            "source": "Pattern-based estimation"
        },
        "清明": {
            "chinese_name": "清明",
            "english_name": "Qingming",
            "meaning": "Clear and Bright",
            "month": "April",
            "day": 5,
            "hour": 15,
            "minute": 20,
            "second": 0,
            "full_datetime": "1908-04-05 15:20:00",
            "source": "Pattern-based estimation"
        },
        "立夏": {
            "chinese_name": "立夏",
            "english_name": "Lixia",
            "meaning": "Beginning of Summer",
            "month": "May",
            "day": 6,
            "hour": 9,
            "minute": 45,
            "second": 0,
            "full_datetime": "1908-05-06 09:45:00",
            "source": "Pattern-based estimation"
        },
        "芒種": {
            "chinese_name": "芒種",
            "english_name": "Mangzhong",
            "meaning": "Grain in Ear",
            "month": "June",
            "day": 6,
            "hour": 14,
            "minute": 10,
            "second": 0,
            "full_datetime": "1908-06-06 14:10:00",
            "source": "Pattern-based estimation"
        },
        "小暑": {
            "chinese_name": "小暑",
            "english_name": "Xiaoshu",
            "meaning": "Slight Heat",
            "month": "July",
            "day": 7,
            "hour": 23,
            "minute": 45,
            "second": 0,
            "full_datetime": "1908-07-07 23:45:00",
            "source": "Pattern-based estimation"
        },
        "立秋": {
            "chinese_name": "立秋",
            "english_name": "Liqiu",
            "meaning": "Beginning of Autumn",
            "month": "August",
            "day": 8,
            "hour": 10,
            "minute": 20,
            "second": 0,
            "full_datetime": "1908-08-08 10:20:00",
            "source": "Pattern-based estimation"
        },
        "白露": {
            "chinese_name": "白露",
            "english_name": "Bailu",
            "meaning": "White Dew",
            "month": "September",
            "day": 8,
            "hour": 13,
            "minute": 30,
            "second": 0,
            "full_datetime": "1908-09-08 13:30:00",
            "source": "Pattern-based estimation"
        },
        "寒露": {
            "chinese_name": "寒露",
            "english_name": "Hanlu",
            "meaning": "Cold Dew",
            "month": "October",
            "day": 8,
            "hour": 14,
            "minute": 45,
            "second": 0,
            "full_datetime": "1908-10-08 14:45:00",
            "source": "Pattern-based estimation for daeun calculation"
        },
        "立冬": {
            "chinese_name": "立冬",
            "english_name": "Lidong",
            "meaning": "Beginning of Winter",
            "month": "November",
            "day": 7,
            "hour": 16,
            "minute": 10,
            "second": 0,
            "full_datetime": "1908-11-07 16:10:00",
            "source": "Pattern-based estimation for daeun calculation"
        },
        "大雪": {
            "chinese_name": "大雪",
            "english_name": "Daxue",
            "meaning": "Major Snow",
            "month": "December",
            "day": 7,
            "hour": 22,
            "minute": 25,
            "second": 0,
            "full_datetime": "1908-12-07 22:25:00",
            "source": "Pattern-based estimation"
        },
        "小寒": {
            "chinese_name": "小寒",
            "english_name": "Xiaohan",
            "meaning": "Slight Cold",
            "month": "January",
            "day": 6,
            "hour": 9,
            "minute": 20,
            "second": 0,
            "full_datetime": "1909-01-06 09:20:00",
            "source": "Pattern-based estimation (next year)"
        }
    }
    
    # 1908년 데이터 추가
    data['solar_terms_data']['1908'] = solar_terms_1908
    
    # 메타데이터 업데이트
    data['metadata']['description'] += " (1908 added with estimations)"
    data['metadata']['note'] += " 1908 data estimated from 1900 patterns."
    
    # 파일 저장
    with open(db_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("✅ 1908년 절기 데이터 추가 완료")
    print(f"추가된 절기: {len(solar_terms_1908)}개")
    
    # 중요한 절기 확인
    hanlu = solar_terms_1908['寒露']
    lidong = solar_terms_1908['立冬']
    
    print(f"\n📊 1908년 중요 절기:")
    print(f"寒露 (한로): {hanlu['month']} {hanlu['day']}일 {hanlu['hour']}:{hanlu['minute']:02d}")
    print(f"立冬 (입동): {lidong['month']} {lidong['day']}일 {lidong['hour']}:{lidong['minute']:02d}")
    
    return data

def main():
    print("🔧 1908년 절기 데이터베이스 확장")
    print("="*50)
    
    result = add_1908_solar_terms()
    
    if result:
        years = list(result['solar_terms_data'].keys())
        print(f"\n현재 데이터베이스 년도: {sorted(years)}")
        print(f"총 {len(years)}년분 데이터")
        
        # 1908년 데이터 확인
        if '1908' in years:
            terms_1908 = len(result['solar_terms_data']['1908'])
            print(f"1908년: {terms_1908}개 절기 ✅")

if __name__ == "__main__":
    main()