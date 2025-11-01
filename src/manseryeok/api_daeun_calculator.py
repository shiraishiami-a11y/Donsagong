"""
API 기반 대운 계산기
외부 절기 데이터를 실시간으로 가져와서 정확한 대운 계산
"""

from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional
import requests
import json

# 한국 표준시 (UTC+9)
KST = timezone(timedelta(hours=9))

# 10천간과 12지지
HEAVENLY_STEMS = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
EARTHLY_BRANCHES = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

# 분기절기만 사용 (중간 절기 제외)
QUARTER_TERMS = [
    '소한', '입춘',  # 1-2월
    '경칩', '청명',  # 3-4월  
    '입하', '망종',  # 5-6월
    '소서', '입추',  # 7-8월
    '백로', '한로',  # 9-10월
    '입동', '대설'   # 11-12월
]

class ApiDaeunCalculator:
    """API 기반 대운 계산기"""
    
    def __init__(self):
        self.api_url = "https://api.standardtable.com/lookup/calendar/gregorian/solarterm/{year}.json"
    
    def calculate_api_daeun(self, 
                           birth_datetime: datetime, 
                           year_stem: str, 
                           month_stem: str,
                           month_branch: str,
                           gender: str) -> Dict:
        """
        API 기반 대운 계산
        """
        
        # 1. 순행/역행 결정
        direction = self._determine_direction(year_stem, gender)
        
        # 2. 외부 API에서 절기 데이터 가져오기
        solar_terms = self._get_solar_terms_from_api(birth_datetime.year)
        
        # 3. 분기절기까지의 일수 계산
        days_to_term = self._calculate_days_to_quarter_term_api(
            birth_datetime, direction, solar_terms
        )
        
        # 4. 대운 시작 나이 계산 (반올림)
        start_age = self._calculate_start_age_round(days_to_term)
        
        # 5. 대운 목록 생성
        daeun_list = self._generate_daeun_list(
            start_age, month_stem, month_branch, direction
        )
        
        return {
            'direction': '순행' if direction == 1 else '역행',
            'days_to_term': days_to_term,
            'start_age': start_age,
            'calculation_method': 'API 분기절기 공식',
            'daeun_list': daeun_list
        }
    
    def _determine_direction(self, year_stem: str, gender: str) -> int:
        """순행/역행 결정"""
        year_stem_index = HEAVENLY_STEMS.index(year_stem)
        is_yang_year = (year_stem_index % 2 == 0)
        
        if (is_yang_year and gender == 'male') or (not is_yang_year and gender == 'female'):
            return 1  # 순행
        else:
            return -1  # 역행
    
    def _get_solar_terms_from_api(self, year: int) -> List[Dict]:
        """외부 API에서 절기 데이터 가져오기"""
        try:
            url = self.api_url.format(year=year)
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Standard Table API 형식으로 절기 이름 매핑
            solar_term_names = [
                '입춘', '우수', '경칩', '춘분', '청명', '곡우',  # 0-5
                '입하', '소만', '망종', '하지', '소서', '대서',  # 6-11
                '입추', '처서', '백로', '추분', '한로', '상강',  # 12-17
                '입동', '소설', '대설', '동지', '소한', '대한'   # 18-23
            ]
            
            # API 데이터를 우리 형식으로 변환
            solar_terms = []
            for item in data:
                if 0 <= item['solarterm'] <= 23:
                    solar_terms.append({
                        'name': solar_term_names[item['solarterm']],
                        'date': f"{item['year']}-{item['month']:02d}-{item['date']:02d}",
                        'month': item['month'],
                        'day': item['date']
                    })
            
            print(f'DEBUG: {year}년 절기 데이터 {len(solar_terms)}개 로드')
            return solar_terms
            
        except requests.RequestException as e:
            print(f'API 오류: {e}')
            return []
        except json.JSONDecodeError as e:
            print(f'JSON 파싱 오류: {e}')
            return []
    
    def _calculate_days_to_quarter_term_api(self, 
                                           birth_datetime: datetime, 
                                           direction: int, 
                                           solar_terms: List[Dict]) -> int:
        """API 데이터로 분기절기까지의 일수 계산"""
        birth_kst = self._to_kst(birth_datetime)
        
        # 분기절기만 필터링
        quarter_terms = [
            term for term in solar_terms 
            if term.get('name') in QUARTER_TERMS
        ]
        
        if not quarter_terms:
            print('WARNING: 분기절기 데이터 없음, 기본값 사용')
            return 15
        
        # 날짜순 정렬
        quarter_terms.sort(key=lambda x: x['date'])
        
        if direction == 1:  # 순행 - 다음 분기절기
            next_term = self._find_next_quarter_term_api(birth_kst, quarter_terms)
            if next_term:
                target_date = datetime.strptime(next_term['date'], '%Y-%m-%d')
                target_date = target_date.replace(tzinfo=KST)
                days = (target_date - birth_kst).days
                print(f'DEBUG 순행: {birth_kst.date()} → {next_term["name"]}({next_term["date"]}) = {days}일')
                return days
        
        else:  # 역행 - 이전 분기절기
            prev_term = self._find_previous_quarter_term_api(birth_kst, quarter_terms)
            if prev_term:
                target_date = datetime.strptime(prev_term['date'], '%Y-%m-%d')
                target_date = target_date.replace(tzinfo=KST)
                days = (birth_kst - target_date).days
                print(f'DEBUG 역행: {birth_kst.date()} → {prev_term["name"]}({prev_term["date"]}) = {days}일')
                return days
        
        return 15
    
    def _find_next_quarter_term_api(self, birth_kst: datetime, quarter_terms: List[Dict]) -> Optional[Dict]:
        """다음 분기절기 찾기"""
        for term in quarter_terms:
            term_date = datetime.strptime(term['date'], '%Y-%m-%d')
            term_date = term_date.replace(tzinfo=KST)
            if term_date > birth_kst:
                return term
        return None
    
    def _find_previous_quarter_term_api(self, birth_kst: datetime, quarter_terms: List[Dict]) -> Optional[Dict]:
        """이전 분기절기 찾기"""
        previous_term = None
        for term in quarter_terms:
            term_date = datetime.strptime(term['date'], '%Y-%m-%d')
            term_date = term_date.replace(tzinfo=KST)
            if term_date < birth_kst:
                previous_term = term
            else:
                break
        return previous_term
    
    def _calculate_start_age_round(self, days: int) -> int:
        """반올림 공식으로 시작 나이 계산"""
        calculated_age = days / 3
        start_age = round(calculated_age)
        
        print(f'DEBUG 계산: {days}일 ÷ 3 = {calculated_age:.2f} → 반올림 = {start_age}세')
        
        return max(start_age, 1)
    
    def _generate_daeun_list(self, start_age: int, month_stem: str, 
                           month_branch: str, direction: int) -> List[Dict]:
        """대운 목록 생성"""
        daeun_list = []
        
        month_stem_index = HEAVENLY_STEMS.index(month_stem)
        month_branch_index = EARTHLY_BRANCHES.index(month_branch)
        
        for i in range(10):
            age_start = start_age + (i * 10)
            age_end = age_start + 9
            
            # 대운 간지 계산
            daeun_stem_index = (month_stem_index + (i + 1) * direction) % 10
            daeun_branch_index = (month_branch_index + (i + 1) * direction) % 12
            
            daeun_stem = HEAVENLY_STEMS[daeun_stem_index]
            daeun_branch = EARTHLY_BRANCHES[daeun_branch_index]
            
            daeun_list.append({
                'order': i + 1,
                'start_age': age_start,
                'end_age': age_end,
                'stem': daeun_stem,
                'branch': daeun_branch,
                'ganzhi': daeun_stem + daeun_branch
            })
        
        return daeun_list
    
    def _to_kst(self, dt: datetime) -> datetime:
        """한국 표준시로 변환"""
        if dt.tzinfo is None:
            return dt.replace(tzinfo=KST)
        return dt.astimezone(KST)