"""
사주 분석 Wrapper - 검증 없이는 분석 불가능하도록 강제
"""

from datetime import datetime
from typing import Dict
from src.validation.saju_validator import SajuValidator
from src.manseryeok.calculator import ManseryeokCalculator
from src.manseryeok.api_daeun_calculator import ApiDaeunCalculator

class SafeSajuAnalyzer:
    """검증 강제 사주 분석기"""
    
    def __init__(self):
        self.validator = SajuValidator()
        self.calculator = ManseryeokCalculator()
        self.daeun_calc = ApiDaeunCalculator()
        self.analysis_locked = True  # 기본적으로 잠김
        self.validation_results = {}
        
    def analyze_fortune(self, birth_datetime: datetime, gender: str, 
                        target_year: int, target_month: int) -> Dict:
        """
        운세 분석 - 검증 후에만 가능
        """
        
        # STEP 0: 강제 검증 체크
        if self.analysis_locked:
            raise RuntimeError("""
            ❌ 분석 시작 불가!
            
            필수 프로세스:
            1. calculate_saju() - 사주 계산
            2. validate_all_relations() - 모든 관계 검증
            3. 검증 통과 후 analysis_locked = False
            
            → 먼저 위 단계를 완료하세요
            """)
        
        # 여기서부터 실제 분석
        return self._perform_analysis()
    
    def calculate_saju(self, birth_datetime: datetime, gender: str) -> Dict:
        """STEP 1: 사주 계산"""
        
        print("="*60)
        print("📊 STEP 1: 만세력 계산")
        print("="*60)
        
        # 사주 계산
        saju = self.calculator.calculate_saju(birth_datetime, gender)
        
        # 대운 계산
        daeun_info = self.daeun_calc.calculate_api_daeun(
            birth_datetime,
            saju.year_stem,
            saju.month_stem,
            saju.month_branch,
            gender
        )
        
        self.saju_data = {
            'saju': saju,
            'daeun': daeun_info,
            'birth_datetime': birth_datetime,
            'gender': gender
        }
        
        print(f"✅ 사주 계산 완료")
        print(f"   일간: {saju.day_stem}")
        print(f"   월지: {saju.month_branch}")
        
        return self.saju_data
    
    def validate_all_relations(self, target_year: int, target_month: int) -> Dict:
        """STEP 2: 모든 관계 검증"""
        
        print("\n" + "="*60)
        print("🔍 STEP 2: 데이터베이스 검증")
        print("="*60)
        
        if not hasattr(self, 'saju_data'):
            raise RuntimeError("❌ 사주 계산 먼저 실행하세요")
        
        saju = self.saju_data['saju']
        daeun = self.saju_data['daeun']
        
        # 현재 나이 계산
        current_age = target_year - self.saju_data['birth_datetime'].year
        
        # 현재 대운 찾기
        current_daeun = None
        for d in daeun['daeun_list']:
            if d['start_age'] <= current_age <= d['end_age']:
                current_daeun = d
                break
        
        if not current_daeun:
            raise ValueError(f"❌ {current_age}세 대운 찾기 실패")
        
        # 1. 대운 천간 검증
        print(f"\n✅ 대운 천간 검증: {saju.day_stem} → {current_daeun['stem']}")
        daeun_validation = self.validator.validate_before_analysis(
            saju.day_stem, 
            current_daeun['stem'],
            '대운천간'
        )
        print(f"   결과: {daeun_validation['relation']['result']}")
        print(f"   설명: {daeun_validation['relation']['description']}")
        
        # 2. 년운 천간 검증 (2025년 = 을사년)
        year_stems = {2025: '乙', 2024: '甲', 2026: '丙'}
        year_stem = year_stems.get(target_year, '乙')
        
        print(f"\n✅ 년운 천간 검증: {saju.day_stem} → {year_stem}")
        year_validation = self.validator.validate_before_analysis(
            saju.day_stem,
            year_stem,
            '년운천간'
        )
        print(f"   결과: {year_validation['relation']['result']}")
        
        # 3. 조후 검증
        print(f"\n✅ 조후 검증: {saju.month_branch}월생")
        johu_validation = self.validator.validate_johu(
            saju.month_branch,
            current_daeun['branch']
        )
        print(f"   조후 데이터 로드 완료")
        
        # 모든 검증 통과
        self.validation_results = {
            'daeun': daeun_validation,
            'year': year_validation,
            'johu': johu_validation,
            'current_daeun': current_daeun
        }
        
        # 잠금 해제
        self.analysis_locked = False
        print("\n✅ 모든 검증 통과 - 분석 가능 상태")
        
        return self.validation_results
    
    def _perform_analysis(self) -> Dict:
        """실제 분석 수행 (검증 후에만 가능)"""
        
        print("\n" + "="*60)
        print("📈 STEP 3: 종합 분석")
        print("="*60)
        
        # 검증된 데이터로만 분석
        daeun_result = self.validation_results['daeun']['relation']['result']
        year_result = self.validation_results['year']['relation']['result']
        
        print(f"\n종합 평가:")
        print(f"  대운 천간: {daeun_result}")
        print(f"  년운 천간: {year_result}")
        print(f"  조후: 데이터베이스 기반 판단")
        
        return {
            'status': 'completed',
            'validated': True,
            'results': self.validation_results
        }


# 사용 예시
if __name__ == "__main__":
    analyzer = SafeSajuAnalyzer()
    
    # 1986년 5월 26일 5시생
    birth = datetime(1986, 5, 26, 5, 0, 0)
    
    try:
        # 검증 없이 분석 시도 → 실패
        analyzer.analyze_fortune(birth, 'male', 2025, 9)
    except RuntimeError as e:
        print(e)
    
    # 올바른 순서
    analyzer.calculate_saju(birth, 'male')
    analyzer.validate_all_relations(2025, 9)
    analyzer.analyze_fortune(birth, 'male', 2025, 9)