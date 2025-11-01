"""
사주 분석 강제 검증 시스템
- 데이터베이스 참조 없이는 분석 불가능하도록 강제
- 모든 답변은 검증 후에만 출력
"""

import json
from typing import Dict, Optional, Tuple
from pathlib import Path

class SajuValidator:
    """사주 분석 필수 검증 클래스"""
    
    def __init__(self):
        self.db_path = Path("/Users/shiraishiami/Desktop/Bluelamp/test-project/docs/DONSAGONG_MASTER_DATABASE.md")
        self.matrix_cache = {}
        self.validation_log = []
        
    def validate_before_analysis(self, day_stem: str, target_stem: str, analysis_type: str) -> Dict:
        """
        분석 전 필수 검증
        Returns: 검증된 데이터만 반환
        """
        
        # STEP 1: 데이터베이스 파일 존재 확인
        if not self.db_path.exists():
            raise FileNotFoundError(f"❌ 데이터베이스 없음: {self.db_path}")
        
        # STEP 2: 천간 매트릭스 로드
        matrix_data = self.load_stem_matrix(day_stem)
        if not matrix_data:
            raise ValueError(f"❌ {day_stem} 일간 매트릭스 없음")
        
        # STEP 3: 타겟 천간과의 관계 확인
        relation = self.get_stem_relation(day_stem, target_stem, matrix_data)
        if relation is None:
            raise ValueError(f"❌ {day_stem} → {target_stem} 관계 데이터 없음")
        
        # STEP 4: 검증 로그 기록
        self.validation_log.append({
            'type': analysis_type,
            'day_stem': day_stem,
            'target_stem': target_stem,
            'result': relation,
            'source': 'DONSAGONG_MASTER_DATABASE.md'
        })
        
        return {
            'validated': True,
            'relation': relation,
            'source_line': matrix_data.get('line_number'),
            'log': self.validation_log
        }
    
    def load_stem_matrix(self, day_stem: str) -> Optional[Dict]:
        """천간 매트릭스 로드"""
        
        # 캐시 확인
        if day_stem in self.matrix_cache:
            return self.matrix_cache[day_stem]
        
        # 데이터베이스에서 로드
        with open(self.db_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 천간 매트릭스 섹션 찾기
        stem_names = {
            '갑': '甲', '을': '乙', '병': '丙', '정': '丁', '무': '戊',
            '기': '己', '경': '庚', '신': '辛', '임': '壬', '계': '癸'
        }
        
        # 해당 일간 섹션 찾기
        korean_name = self.get_korean_name(day_stem)
        # 경금(庚金) 형식으로 찾기
        section_marker = f"### {korean_name}({day_stem}金) 일간 → 다른 천간들"
        if section_marker not in content:
            # 다른 오행들 시도
            for element in ['木', '火', '土', '金', '水']:
                section_marker = f"### {korean_name}({day_stem}{element}) 일간 → 다른 천간들"
                if section_marker in content:
                    break
        
        if section_marker not in content:
            return None
            
        # 매트릭스 파싱
        lines = content.split('\n')
        matrix_data = {'relations': {}}
        
        in_section = False
        for i, line in enumerate(lines):
            if section_marker in line:
                in_section = True
                matrix_data['line_number'] = i + 1
                continue
            
            if in_section:
                if line.startswith('###'):  # 다음 섹션
                    break
                    
                if '|' in line and not line.startswith('|---'):
                    parts = [p.strip() for p in line.split('|')]
                    if len(parts) >= 4:
                        stem = parts[1]
                        result = parts[2]
                        desc = parts[3]
                        
                        if stem in stem_names.values():
                            matrix_data['relations'][stem] = {
                                'result': result,
                                'description': desc
                            }
        
        # 캐시 저장
        self.matrix_cache[day_stem] = matrix_data
        return matrix_data
    
    def get_stem_relation(self, day_stem: str, target_stem: str, matrix_data: Dict) -> Optional[Dict]:
        """특정 천간 관계 추출"""
        relations = matrix_data.get('relations', {})
        return relations.get(target_stem)
    
    def get_korean_name(self, stem: str) -> str:
        """한자를 한글로 변환"""
        mapping = {
            '甲': '갑목', '乙': '을목', '丙': '병화', '丁': '정화', '戊': '무토',
            '己': '기토', '庚': '경금', '辛': '신금', '壬': '임수', '癸': '계수'
        }
        return mapping.get(stem, stem)
    
    def validate_johu(self, month_branch: str, target_branch: str) -> Dict:
        """조후 검증"""
        
        # 데이터베이스에서 조후 매트릭스 로드
        with open(self.db_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 월지별 조후 찾기
        johu_marker = f"### {month_branch}월생 조후"
        
        if johu_marker not in content:
            raise ValueError(f"❌ {month_branch}월생 조후 데이터 없음")
        
        # 조후 데이터 파싱
        lines = content.split('\n')
        johu_data = {}
        
        in_section = False
        for line in lines:
            if johu_marker in line:
                in_section = True
                continue
                
            if in_section:
                if line.startswith('###'):
                    break
                    
                # 조후 데이터 파싱
                if '봄:' in line or '여름:' in line or '가을:' in line or '겨울:' in line:
                    season, values = line.split(':', 1)
                    johu_data[season.strip()] = values.strip()
        
        return {
            'validated': True,
            'johu_data': johu_data,
            'source': 'DONSAGONG_MASTER_DATABASE.md'
        }
    
    def force_validation_check(self) -> bool:
        """강제 검증 체크"""
        if not self.validation_log:
            raise RuntimeError("""
            ❌ 검증 없이 분석 시도됨!
            
            필수 체크리스트:
            1. [ ] 데이터베이스 로드
            2. [ ] 천간 매트릭스 확인
            3. [ ] 조후 데이터 확인
            4. [ ] 용신 데이터 확인
            
            → validate_before_analysis() 먼저 실행하세요
            """)
        return True


# 사용 예시
if __name__ == "__main__":
    validator = SajuValidator()
    
    # 경금 일간 vs 정화 검증
    try:
        result = validator.validate_before_analysis('庚', '丁', '대운천간')
        print(f"✅ 검증 완료: 경금→정화 = {result['relation']['result']}")
        print(f"   설명: {result['relation']['description']}")
    except Exception as e:
        print(f"❌ 검증 실패: {e}")