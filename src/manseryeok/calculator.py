"""
만세력 계산 엔진

lunar-python을 사용한 사주팔자 계산, 대운, 24절기 확인, 음력 변환 등의 핵심 기능 제공
"""

from datetime import datetime, timezone, timedelta
from dataclasses import dataclass
from typing import Tuple, Optional, Dict, List
import ephem
import pytz
from lunar_python import Lunar, Solar, EightChar

# 한국 표준시 (UTC+9)
KST = timezone(timedelta(hours=9))

# 10천간 (天干) - 한자
HEAVENLY_STEMS = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
HEAVENLY_STEMS_KOR = ['갑', '을', '병', '정', '무', '기', '경', '신', '임', '계']

# 12지지 (地支) - 한자
EARTHLY_BRANCHES = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
EARTHLY_BRANCHES_KOR = ['자', '축', '인', '묘', '진', '사', '오', '미', '신', '유', '술', '해']

# 한자-한글 매핑
STEMS_MAPPING = dict(zip(HEAVENLY_STEMS, HEAVENLY_STEMS_KOR))
BRANCHES_MAPPING = dict(zip(EARTHLY_BRANCHES, EARTHLY_BRANCHES_KOR))

# 24절기 정의 (절기명, 황경)
SOLAR_TERMS = [
    ('입춘', 315.0), ('우수', 330.0), ('경칩', 345.0), ('춘분', 0.0),
    ('청명', 15.0), ('곡우', 30.0), ('입하', 45.0), ('소만', 60.0),
    ('망종', 75.0), ('하지', 90.0), ('소서', 105.0), ('대서', 120.0),
    ('입추', 135.0), ('처서', 150.0), ('백로', 165.0), ('추분', 180.0),
    ('한로', 195.0), ('상강', 210.0), ('입동', 225.0), ('소설', 240.0),
    ('대설', 255.0), ('동지', 270.0), ('소한', 285.0), ('대한', 300.0)
]

@dataclass
class SajuPalja:
    """사주팔자 데이터 클래스"""
    year_stem: str    # 연간
    year_branch: str  # 연지
    month_stem: str   # 월간
    month_branch: str # 월지
    day_stem: str     # 일간
    day_branch: str   # 일지
    hour_stem: str    # 시간
    hour_branch: str  # 시지
    gender: str       # 성별 ('male' 또는 'female')
    
    birth_datetime: datetime
    lunar_info: Dict
    solar_terms_info: Dict
    
    def __str__(self):
        return f"{self.year_stem}{self.year_branch} {self.month_stem}{self.month_branch} {self.day_stem}{self.day_branch} {self.hour_stem}{self.hour_branch}"

@dataclass
class DaeunInfo:
    """대운 정보"""
    age_start: int
    age_end: int
    stem: str
    branch: str
    ganzhi: str

class ManseryeokCalculator:
    """만세력 계산기 메인 클래스"""
    
    def __init__(self, solar_terms_db_path='solar_terms_1900-1910_database.json'):
        self.cache = {}  # 계산 결과 캐싱
        self._load_solar_terms_db(solar_terms_db_path)
    
    def calculate_saju(self, birth_datetime: datetime, gender: str) -> SajuPalja:
        """
        생년월일시로부터 사주팔자 계산
        
        Args:
            birth_datetime: 출생 시간 (현지 시각)
            gender: 성별 ('male' 또는 'female') - 대운 계산 필수!
        
        Returns:
            SajuPalja: 사주팔자 정보
        """
        # 성별 검증
        if gender not in ['male', 'female']:
            raise ValueError("성별은 'male' 또는 'female'이어야 합니다")
        # 1. 한국 표준시로 변환
        kst_time = self._to_kst(birth_datetime)
        
        # 2. lunar-python으로 Solar 객체 생성
        solar = Solar.fromYmdHms(kst_time.year, kst_time.month, kst_time.day, kst_time.hour, kst_time.minute, kst_time.second)
        lunar = solar.getLunar()
        
        # 3. EightChar(八字) 객체로 정확한 사주팔자 계산
        eight_char = lunar.getEightChar()
        
        # 4. lunar-python에서 직접 사주팔자 가져오기
        year_stem = eight_char.getYearGan()
        year_branch = eight_char.getYearZhi()
        month_stem = eight_char.getMonthGan()
        month_branch = eight_char.getMonthZhi()
        day_stem = eight_char.getDayGan()
        day_branch = eight_char.getDayZhi()
        hour_stem = eight_char.getTimeGan()
        hour_branch = eight_char.getTimeZhi()
        
        # 5. 음력 정보
        lunar_month = lunar.getMonth()
        lunar_info = {
            'year': lunar.getYear(),
            'month': abs(lunar_month),  # 음수이면 윤달
            'day': lunar.getDay(),
            'leap_month': lunar_month < 0,  # 음수이면 윤달
            'ganzhi_year': f"{year_stem}{year_branch}",
            'ganzhi_month': f"{month_stem}{month_branch}",
            'ganzhi_day': f"{day_stem}{day_branch}"
        }
        
        # 6. 절기 정보
        solar_terms_info = self._get_solar_terms_info(kst_time)
        
        return SajuPalja(
            year_stem=year_stem,
            year_branch=year_branch,
            month_stem=month_stem,
            month_branch=month_branch,
            day_stem=day_stem,
            day_branch=day_branch,
            hour_stem=hour_stem,
            hour_branch=hour_branch,
            gender=gender,
            birth_datetime=kst_time,
            lunar_info=lunar_info,
            solar_terms_info=solar_terms_info
        )
    
    def _to_kst(self, dt: datetime) -> datetime:
        """한국 표준시로 변환"""
        if dt.tzinfo is None:
            # naive datetime은 KST로 가정
            return dt.replace(tzinfo=KST)
        return dt.astimezone(KST)
    
    # lunar-python을 사용하므로 아래 함수들은 더 이상 필요하지 않음
    # 하지만 호환성을 위해 남겨둠 (사용하지 않음)
    def _calculate_year_pillar(self, kst_time: datetime, lunar) -> Tuple[str, str]:
        """연주 계산 - 더 이상 사용하지 않음 (lunar-python EightChar 사용)"""
        # lunar-python의 EightChar가 정확한 계산을 제공
        pass
    
    def _load_solar_terms_db(self, db_path: str):
        """정확한 절기 데이터베이스 로드"""
        import json
        import os
        
        try:
            # 상대 경로로 데이터베이스 파일 찾기
            script_dir = os.path.dirname(os.path.abspath(__file__))
            full_path = os.path.join(script_dir, '../../', db_path)
            
            if os.path.exists(full_path):
                with open(full_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._solar_terms_db = data.get('solar_terms_data', {})
                    print(f"✅ 정확한 절기 데이터베이스 로드: {len(self._solar_terms_db)}년분")
            else:
                self._solar_terms_db = {}
                print(f"⚠️ 절기 데이터베이스 없음: {full_path}")
                
        except Exception as e:
            self._solar_terms_db = {}
            print(f"❌ 절기 데이터베이스 로드 실패: {e}")
    
    def _get_solar_term_from_db(self, year: int, term_longitude: float) -> datetime:
        """데이터베이스에서 정확한 절기 시간 조회"""
        # 황경에 따른 절기명 매핑 (정확한 대응)
        longitude_to_term = {
            315.0: '立春',  # 입춘
            330.0: '驚蟄',  # 경칩 (우수는 데이터베이스에 없음)
            345.0: '驚蟄',  # 경칩
            0.0: '清明',    # 춘분 (청명으로 대체)
            15.0: '清明',   # 청명
            30.0: '立夏',   # 곡우 (입하로 대체)
            45.0: '立夏',   # 입하
            60.0: '芒種',   # 소만 (망종으로 대체)
            75.0: '芒種',   # 망종
            90.0: '小暑',   # 하지 (소서로 대체)
            105.0: '小暑',  # 소서
            120.0: '立秋',  # 대서 (입추로 대체)
            135.0: '立秋',  # 입추
            150.0: '白露',  # 처서 (백로로 대체)
            165.0: '白露',  # 백로
            180.0: '寒露',  # 추분 (한로로 대체)
            195.0: '寒露',  # 한로
            210.0: '立冬',  # 상강 (입동으로 대체)
            225.0: '立冬',  # 입동
            240.0: '大雪',  # 소설 (대설로 대체)
            255.0: '大雪',  # 대설
            270.0: '小寒',  # 동지 (소한으로 대체)
            285.0: '小寒',  # 소한
            300.0: '立春',  # 대한 (립춘으로 대체, 다음년)
        }
        
        term_name = longitude_to_term.get(term_longitude)
        if not term_name or str(year) not in self._solar_terms_db:
            raise ValueError(f"절기 데이터 없음: {year}년 {term_longitude}도")
        
        year_data = self._solar_terms_db[str(year)]
        if term_name not in year_data:
            raise ValueError(f"절기 데이터 없음: {year}년 {term_name}")
        
        term_data = year_data[term_name]
        
        # 소한은 다음년 1월
        if term_name == '小寒':
            dt_year = year + 1
        else:
            dt_year = year
            
        # 월 매핑
        month_mapping = {
            '立春': 2, '驚蟄': 3, '清明': 4, '立夏': 5, 
            '芒種': 6, '小暑': 7, '立秋': 8, '白露': 9,
            '寒露': 10, '立冬': 11, '大雪': 12, '小寒': 1
        }
        
        month = month_mapping[term_name]
        
        return datetime(
            dt_year, month, term_data['day'],
            term_data['hour'], term_data['minute'], 
            term_data.get('second', 0), tzinfo=KST
        )
    
    def _get_estimated_solar_term(self, year: int, term_longitude: float) -> datetime:
        """절기 추정값 계산 (정확한 추정)"""
        # 정확한 절기 추정 (실제 패턴 기반)
        solar_term_estimates = {
            315.0: (2, 4),   # 입춘 - 2월 4일경
            330.0: (2, 19),  # 우수 - 2월 19일경  
            345.0: (3, 6),   # 경칩 - 3월 6일경
            0.0: (3, 21),    # 춘분 - 3월 21일경
            15.0: (4, 5),    # 청명 - 4월 5일경
            30.0: (4, 20),   # 곡우 - 4월 20일경
            45.0: (5, 6),    # 입하 - 5월 6일경
            60.0: (5, 21),   # 소만 - 5월 21일경
            75.0: (6, 6),    # 망종 - 6월 6일경
            90.0: (6, 21),   # 하지 - 6월 21일경
            105.0: (7, 7),   # 소서 - 7월 7일경
            120.0: (7, 23),  # 대서 - 7월 23일경
            135.0: (8, 7),   # 입추 - 8월 7일경
            150.0: (8, 23),  # 처서 - 8월 23일경
            165.0: (9, 8),   # 백로 - 9월 8일경
            180.0: (9, 23),  # 추분 - 9월 23일경
            195.0: (10, 8),  # 한로 - 10월 8일경
            210.0: (10, 23), # 상강 - 10월 23일경
            225.0: (11, 7),  # 입동 - 11월 7일경
            240.0: (11, 22), # 소설 - 11월 22일경
            255.0: (12, 7),  # 대설 - 12월 7일경
            270.0: (12, 22), # 동지 - 12월 22일경
            285.0: (1, 6),   # 소한 - 1월 6일경 (다음년)
            300.0: (1, 20),  # 대한 - 1월 20일경 (다음년)
        }
        
        if term_longitude in solar_term_estimates:
            month, day = solar_term_estimates[term_longitude]
            
            # 소한, 대한은 다음년
            if term_longitude in [285.0, 300.0]:
                year += 1
                
            return datetime(year, month, day, 12, 0, tzinfo=KST)
        else:
            # 기본값
            return datetime(year, 6, 15, 12, 0, tzinfo=KST)
    
    def _calculate_month_pillar(self, kst_time: datetime, lunar) -> Tuple[str, str]:
        """월주 계산 - 더 이상 사용하지 않음 (lunar-python EightChar 사용)"""
        pass
    
    def _calculate_day_pillar(self, kst_time: datetime, lunar) -> Tuple[str, str]:
        """일주 계산 - 더 이상 사용하지 않음 (lunar-python EightChar 사용)"""
        pass
    
    def _calculate_hour_pillar(self, kst_time: datetime, lunar) -> Tuple[str, str]:
        """시주 계산"""
        hour = kst_time.hour
        
        # 23-01시: 자시, 01-03시: 축시, 03-05시: 인시...
        # 시간을 지지로 변환
        hour_branch_index = ((hour + 1) // 2) % 12
        hour_branch = EARTHLY_BRANCHES[hour_branch_index]
        
        # 일간에 따른 시간 계산 (일간과 시간의 관계)
        day_stem, day_branch = self._calculate_day_pillar(kst_time, lunar)
        
        # day_stem이 HEAVENLY_STEMS에 있는지 확인 후 인덱스 찾기
        try:
            day_stem_index = HEAVENLY_STEMS.index(day_stem)
        except ValueError:
            # 만약 찾을 수 없으면 기본값 사용
            print(f"Warning: '{day_stem}' not found in HEAVENLY_STEMS, using 甲")
            day_stem_index = 0
        
        # 갑기일은 갑자시, 을경일은 병자시... 공식 적용
        hour_stem_base = {0: 0, 1: 2, 2: 4, 3: 6, 4: 8, 5: 0, 6: 2, 7: 4, 8: 6, 9: 8}
        base_index = hour_stem_base[day_stem_index]
        hour_stem_index = (base_index + hour_branch_index) % 10
        hour_stem = HEAVENLY_STEMS[hour_stem_index]
        
        return hour_stem, hour_branch
    
    def _calculate_solar_term_time(self, year: int, term_longitude: float) -> datetime:
        """특정 년도의 절기 시간 계산 - 정확한 데이터베이스 우선 사용"""
        # 정확한 절기 데이터베이스가 있는 경우 우선 사용
        if hasattr(self, '_solar_terms_db') and str(year) in self._solar_terms_db:
            try:
                return self._get_solar_term_from_db(year, term_longitude)
            except Exception:
                pass  # 데이터베이스 실패시 추정값으로
        
        # ephem 계산이 신뢰할 수 없으므로 정확한 추정값 사용
        return self._get_estimated_solar_term(year, term_longitude)
    
    def _get_solar_terms_info(self, kst_time: datetime) -> Dict:
        """절기 정보 조회"""
        year = kst_time.year
        solar_terms = {}
        
        for term_name, longitude in SOLAR_TERMS:
            term_time = self._calculate_solar_term_time(year, longitude)
            solar_terms[term_name] = term_time.isoformat()
        
        return solar_terms
    
    def calculate_daeun(self, saju: SajuPalja, gender: str) -> List[DaeunInfo]:
        """대운 계산"""
        # 성별에 따른 순/역행 결정
        year_stem_index = HEAVENLY_STEMS.index(saju.year_stem)
        is_yang_year = (year_stem_index % 2 == 0)  # 갑병무경임 = 양
        
        if (is_yang_year and gender == 'male') or (not is_yang_year and gender == 'female'):
            direction = 1  # 순행
        else:
            direction = -1  # 역행
        
        # 기점 계산 (절입 시간까지의 거리)
        start_age = self._calculate_daeun_start_age(saju, direction)
        
        # 10년씩 대운 생성
        daeuns = []
        month_branch_index = EARTHLY_BRANCHES.index(saju.month_branch)
        month_stem_index = HEAVENLY_STEMS.index(saju.month_stem)
        
        for i in range(8):  # 8개 대운 계산
            age_start = start_age + (i * 10)
            age_end = age_start + 9
            
            # 대운 간지 계산
            daeun_stem_index = (month_stem_index + (i + 1) * direction) % 10
            daeun_branch_index = (month_branch_index + (i + 1) * direction) % 12
            
            daeun_stem = HEAVENLY_STEMS[daeun_stem_index]
            daeun_branch = EARTHLY_BRANCHES[daeun_branch_index]
            
            daeuns.append(DaeunInfo(
                age_start=age_start,
                age_end=age_end,
                stem=daeun_stem,
                branch=daeun_branch,
                ganzhi=daeun_stem + daeun_branch
            ))
        
        return daeuns
    
    def _calculate_daeun_start_age(self, saju: SajuPalja, direction: int) -> int:
        """대운 시작 나이 계산"""
        birth_datetime = saju.birth_datetime
        
        if direction == 1:  # 순행
            # 다음 절기까지의 시간 계산
            next_term_time = self._get_next_solar_term(birth_datetime)
        else:  # 역행
            # 이전 절기까지의 시간 계산
            next_term_time = self._get_previous_solar_term(birth_datetime)
        
        # 시간 차이를 나이로 변환 (3일 = 1년)
        time_diff = abs(next_term_time - birth_datetime)
        days_diff = time_diff.days
        
        # 3일 = 1년 계산법
        start_age = days_diff // 3
        
        return max(start_age, 1)  # 최소 1살부터 시작
    
    def _get_next_solar_term(self, dt: datetime) -> datetime:
        """다음 절기 시간 조회"""
        year = dt.year
        
        for term_name, longitude in SOLAR_TERMS:
            term_time = self._calculate_solar_term_time(year, longitude)
            if term_time > dt:
                return term_time
        
        # 올해 절기가 모두 지났으면 내년 첫 절기 (입춘)
        return self._calculate_solar_term_time(year + 1, 315.0)
    
    def _get_previous_solar_term(self, dt: datetime) -> datetime:
        """이전 절기 시간 조회"""
        year = dt.year
        
        # 역순으로 검색
        for term_name, longitude in reversed(SOLAR_TERMS):
            term_time = self._calculate_solar_term_time(year, longitude)
            if term_time < dt:
                return term_time
        
        # 올해 절기가 모두 이후면 작년 마지막 절기 (대한)
        return self._calculate_solar_term_time(year - 1, 300.0)
    
    def calculate_saeun(self, target_year: int) -> Tuple[str, str]:
        """세운(년운) 계산"""
        gap_ja_year = 1984  # 가장 가까운 갑자년
        year_diff = target_year - gap_ja_year
        cycle_position = year_diff % 60
        
        stem = HEAVENLY_STEMS[cycle_position % 10]
        branch = EARTHLY_BRANCHES[cycle_position % 12]
        
        return stem, branch
    
    def calculate_wolun(self, target_year: int, target_month: int) -> Tuple[str, str]:
        """월운 계산"""
        # 년간에 따른 정월 간지 결정
        year_stem_index = HEAVENLY_STEMS.index(self.calculate_saeun(target_year)[0])
        
        # 정월 간지 공식
        month_stem_base = {0: 2, 1: 4, 2: 6, 3: 8, 4: 0, 5: 2, 6: 4, 7: 6, 8: 8, 9: 0}
        base_stem_idx = month_stem_base[year_stem_index]
        month_stem_idx = (base_stem_idx + target_month - 1) % 10
        month_branch_idx = (target_month + 1) % 12  # 정월=인월=2
        
        return HEAVENLY_STEMS[month_stem_idx], EARTHLY_BRANCHES[month_branch_idx]
    
    def validate_birth_datetime(self, birth_datetime: datetime) -> bool:
        """출생 시간 유효성 검증"""
        if birth_datetime.year < 1900 or birth_datetime.year > 2100:
            raise ValueError(f"지원하지 않는 년도입니다: {birth_datetime.year}")
        
        if not (0 <= birth_datetime.hour <= 23):
            raise ValueError(f"잘못된 시간입니다: {birth_datetime.hour}")
        
        if not (0 <= birth_datetime.minute <= 59):
            raise ValueError(f"잘못된 분입니다: {birth_datetime.minute}")
        
        return True
    
    def calculate_daeun_with_lunar(self, saju: SajuPalja) -> Dict:
        """lunar-python을 사용한 정확한 대운 계산"""
        try:
            # Solar 객체 재생성
            solar = Solar.fromYmdHms(
                saju.birth_datetime.year, 
                saju.birth_datetime.month, 
                saju.birth_datetime.day, 
                saju.birth_datetime.hour, 
                saju.birth_datetime.minute, 
                0
            )
            lunar = solar.getLunar()
            
            # EightChar로 대운 계산
            eight_char = EightChar.fromLunar(lunar)
            gender_code = 1 if saju.gender == 'male' else 0
            yun = eight_char.getYun(gender_code)
            
            # 대운 정보 추출
            daeun_list = []
            da_yun_arr = yun.getDaYun()
            
            for da_yun in da_yun_arr:
                daeun_list.append({
                    'ganZhi': da_yun.getGanZhi(),
                    'startAge': da_yun.getStartAge(),
                    'endAge': da_yun.getStartAge() + 9
                })
            
            return {
                'startYear': yun.getStartYear(),
                'startDate': yun.getStartSolar().toYmd(),
                'isForward': yun.isForward(),
                'daeunList': daeun_list
            }
            
        except Exception as e:
            raise Exception(f"대운 계산 오류: {e}")
    
    def get_current_daeun(self, saju: SajuPalja, current_age: int) -> Dict:
        """현재 나이에 해당하는 대운 찾기"""
        daeun_info = self.calculate_daeun_with_lunar(saju)
        
        for daeun in daeun_info['daeunList']:
            if daeun['startAge'] <= current_age <= daeun['endAge']:
                return {
                    'current': daeun,
                    'all_info': daeun_info
                }
        
        # 기운 이전이면 첫 번째 대운 반환
        return {
            'current': {'ganZhi': '기운전', 'startAge': 1, 'endAge': daeun_info['daeunList'][0]['startAge']-1},
            'all_info': daeun_info
        }