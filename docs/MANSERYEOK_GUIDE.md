# 만세력 완전 가이드

> **만세력 계산 + 구현 + 프로세스 통합 가이드**
> 
> 정확한 사주팔자 계산과 돈사공 분석을 위한 완전 매뉴얼

---

## 🎯 만세력 기본 원리

### 사주팔자 (四柱八字) 구성
- **연주(年柱)**: 출생연도의 간지 (입춘 기준)
- **월주(月柱)**: 출생월의 간지 (절입 시간 기준)
- **일주(日柱)**: 출생일의 간지
- **시주(時柱)**: 출생시간의 간지

### 10간 12지 체계
```python
# 천간 (天干) - 10개
HEAVENLY_STEMS = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
HEAVENLY_STEMS_KOR = ['갑', '을', '병', '정', '무', '기', '경', '신', '임', '계']

# 지지 (地支) - 12개  
EARTHLY_BRANCHES = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
EARTHLY_BRANCHES_KOR = ['자', '축', '인', '묘', '진', '사', '오', '미', '신', '유', '술', '해']
```

---

## 📊 사주/만세력 관련 질문 처리 프로세스

### 🔴 필수 참조 데이터베이스 목록
```yaml
핵심 계산기:
  - /src/manseryeok/calculator.py           # 메인 만세력 계산기
  - /src/manseryeok/api_daeun_calculator.py # API 기반 대운 계산기

데이터베이스:
  - /docs/DONSAGONG_MASTER_DATABASE.md      # 용신/조후 통합 매트릭스
  - /docs/DONSAGONG_ANALYSIS_SYSTEM_V2.md   # 체계적 분석 순서
  - /docs/MANSERYEOK_GUIDE.md              # 이 파일 (만세력 가이드)

이미지 자료:
  - /learning-materials/용신/*.png          # 용신 원본 자료
```

### Step 1: 만세력 도구 확인 ⚡ **최우선**
```bash
# 1. 만세력 관련 파일 검색
Glob: **/*.py (Python 계산기 파일)
Glob: src/manseryeok/* (만세력 모듈)  
Glob: src/*manseryeok*.py (만세력 관련 파일)

# 2. 사용 가능한 계산기 확인
- ManseryeokCalculator 클래스
- calculator.py 파일
```

### Step 2: 계산기 활용
```python
from datetime import datetime
from src.manseryeok.calculator import ManseryeokCalculator

# 생년월일시 -> datetime 객체 변환
birth_datetime = datetime(year, month, day, hour, minute)
calculator = ManseryeokCalculator()

# 사주 계산 (성별 필수!)
saju = calculator.calculate_saju(birth_datetime, 'male')  # or 'female'

# 대운 계산
daeun_info = calculator.calculate_daeun_with_lunar(saju)
```

### Step 3: 돈사공 분석 적용
```
1. 일간 확인
2. DONSAGONG_COMPLETE.md에서 해당 일간 용신 조회
3. DONSAGONG_ANALYSIS_GUIDE.md로 대운별 용신 분석 수행
```

---

## 🔧 만세력 상세 구현

### 24절기 정확한 절입 시간 계산

#### 절기 정의 (황경 기준)
```python
SOLAR_TERMS = [
    ('입춘', 315.0), ('우수', 330.0), ('경칩', 345.0), ('춘분', 0.0),
    ('청명', 15.0), ('곡우', 30.0), ('입하', 45.0), ('소만', 60.0),
    ('망종', 75.0), ('하지', 90.0), ('소서', 105.0), ('대서', 120.0),
    ('입추', 135.0), ('처서', 150.0), ('백로', 165.0), ('추분', 180.0),
    ('한로', 195.0), ('상강', 210.0), ('입동', 225.0), ('소설', 240.0),
    ('대설', 255.0), ('동지', 270.0), ('소한', 285.0), ('대한', 300.0)
]
```

#### 천문학적 계산 방법
```python
import ephem
from datetime import datetime, timezone, timedelta

# 한국 표준시 (UTC+9)
KST = timezone(timedelta(hours=9))

def calculate_solar_term_time(year, term_longitude):
    """특정 년도의 절기 시간 계산"""
    sun = ephem.Sun()
    start_date = ephem.Date(f'{year}/1/1')
    
    observer = ephem.Observer()
    observer.long = '127.0'  # 서울 경도
    observer.lat = '37.5'    # 서울 위도
    
    # 태양 황경이 목표 각도에 도달하는 시점 찾기
    date = start_date
    for _ in range(400):  # 최대 400일 탐색
        observer.date = date
        sun.compute(observer)
        
        longitude = float(sun.hlong) * 180 / ephem.pi
        diff = (term_longitude - longitude + 360) % 360
        if diff > 180:
            diff -= 360
            
        if abs(diff) < 0.001:  # 0.001도 미만의 오차
            break
            
        date += diff / 360.0
    
    # UTC를 KST로 변환
    utc_datetime = datetime.utcfromtimestamp(float(date))
    kst_time = utc_datetime.replace(tzinfo=timezone.utc).astimezone(KST)
    
    return kst_time
```

### 대운 계산 시스템

#### 대운 순/역행 결정
```python
def calculate_daeun_direction(year_stem, gender):
    """대운 순/역행 결정"""
    # 년간의 음양 판별
    year_stem_index = HEAVENLY_STEMS.index(year_stem)
    is_yang_year = (year_stem_index % 2 == 0)  # 갑병무경임 = 양
    
    # 순/역행 결정
    if (is_yang_year and gender == 'male') or (not is_yang_year and gender == 'female'):
        return 1   # 순행
    else:
        return -1  # 역행
```

#### 대운 시작 나이 계산
```python
def calculate_daeun_start_age(birth_datetime, direction):
    """대운 시작 나이 계산 (3일 = 1년 법칙)"""
    if direction == 1:  # 순행
        next_term_time = get_next_solar_term(birth_datetime)
    else:  # 역행
        next_term_time = get_previous_solar_term(birth_datetime)
    
    # 시간 차이를 나이로 변환
    time_diff = abs(next_term_time - birth_datetime)
    days_diff = time_diff.days
    
    # 3일 = 1년 계산법
    start_age = days_diff // 3
    return max(start_age, 1)  # 최소 1살부터 시작
```

---

## ⚡ 필수 체크포인트

### 사주 계산 시
- [ ] 만세력 계산기 파일 존재 확인
- [ ] Python 환경에서 lunar-python 라이브러리 사용 가능 확인
- [ ] **성별 정보 포함** (대운 계산 필수!)
- [ ] 한국 표준시(KST) 적용
- [ ] 절입 시간 정확성 확인

### 용신 분석 시  
- [ ] DONSAGONG_COMPLETE.md 파일 참조
- [ ] 천간/지지 용신 분리 분석
- [ ] 계절별 용신 매트릭스 적용
- [ ] 월지지 용신 제외 원칙 준수

---

## ❌ 오류 방지

### 하지 말아야 할 것들
- ❌ 수동으로 간지 계산 시도  
- ❌ 대략적인 사주 추정  
- ❌ 만세력 도구 확인 없이 답변
- ❌ 성별 정보 누락
- ❌ 시간대 변환 무시

### 반드시 해야 할 것들  
- ✅ 도구 존재 여부 먼저 확인  
- ✅ 정확한 계산기 사용  
- ✅ 용신 매트릭스 기반 분석
- ✅ 절입 시간 기준 월주 계산
- ✅ 대운 순/역행 정확히 판별

---

## 🔍 고급 활용

### lunar-python 라이브러리 활용
```python
from lunar_python import Lunar, Solar, EightChar

# Solar 객체 생성
solar = Solar.fromYmdHms(year, month, day, hour, minute, second)
lunar = solar.getLunar()

# EightChar로 정확한 사주 계산
eight_char = EightChar.fromLunar(lunar)
gender_code = 1 if gender == 'male' else 0
yun = eight_char.getYun(gender_code)

# 대운 정보 추출
da_yun_arr = yun.getDaYun()
for da_yun in da_yun_arr:
    ganZhi = da_yun.getGanZhi()
    startAge = da_yun.getStartAge()
    endAge = da_yun.getStartAge() + 9
```

### 특수 상황 처리

#### 윤달 처리
```python
lunar_month = lunar.getMonth()
lunar_info = {
    'year': lunar.getYear(),
    'month': abs(lunar_month),
    'day': lunar.getDay(),
    'leap_month': lunar_month < 0  # 음수이면 윤달
}
```

#### 자시 처리 (23-01시)
```python
def adjust_hour_for_zishi(hour):
    """자시 보정 (23시를 다음날 자시로 처리)"""
    if hour == 23:
        return 0  # 다음날 자시로 처리
    return hour
```

---

## 🎯 실전 사용법

### 기본 사용 예시
```python
# 1. 도구 확인
from src.manseryeok.calculator import ManseryeokCalculator

# 2. 사주 계산
birth_datetime = datetime(2015, 7, 23, 20, 0, 0)
calculator = ManseryeokCalculator()
saju = calculator.calculate_saju(birth_datetime, 'male')

# 3. 결과 확인
print(f'사주: {saju.year_stem}{saju.year_branch} '
      f'{saju.month_stem}{saju.month_branch} '
      f'{saju.day_stem}{saju.day_branch} '
      f'{saju.hour_stem}{saju.hour_branch}')
print(f'일간: {saju.day_stem}')

# 4. 대운 계산
daeun_info = calculator.calculate_daeun_with_lunar(saju)
for i, daeun in enumerate(daeun_info['daeunList'][:3], 1):
    print(f'제{i}대운 ({daeun["startAge"]}-{daeun["endAge"]}세): {daeun["ganZhi"]}')
```

### 돈사공 분석 연계
```python
# 5. 용신 분석을 위한 준비
day_stem = saju.day_stem  # 일간
birth_season = get_season_from_month(saju.birth_datetime.month)

# 6. DONSAGONG_COMPLETE.md 용신 매트릭스에서 
#    해당 일간의 계절별 용신 조회
# 7. DONSAGONG_ANALYSIS_GUIDE.md로 대운 분석 수행
```

---

## 📚 참고 데이터베이스

### 핵심 참조 파일
- **DONSAGONG_COMPLETE.md**: 천간/지지/조후/용신 통합 데이터
- **DONSAGONG_ANALYSIS_GUIDE.md**: 7단계 풀이법과 해석 방법
- **src/manseryeok/calculator.py**: 만세력 계산 엔진

### 지원 라이브러리
- **lunar-python**: 음양력 변환 및 정확한 간지 계산
- **ephem**: 천문학적 절기 시간 계산
- **pytz**: 시간대 처리

---

*최종 업데이트: 2025년 1월*
*만세력 완전 가이드 v1.0*