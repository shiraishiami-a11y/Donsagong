"""
돈사공 전용 엄격한 해석 시스템

## 🎯 핵심 목적
- 오직 돈사공 데이터베이스만 참조
- 임의 해석 절대 금지  
- 정확한 데이터 매칭만 수행
- 100% 데이터베이스 기반 해석

## 🛡️ 안전 장치
1. 파일에서 정확한 내용만 추출
2. 출처를 반드시 명시
3. 천간과 지지 분리 해석
4. 데이터 없으면 "확인 불가" 반환
5. 해석 전 반드시 파일 읽기
6. 매트릭스에서 정확한 값만 추출
7. 추측성 문장 금지

## 📚 참조 데이터베이스
- 천간: DONSAGONG_CHEONGAN_COMPLETE.md
- 지지: DONSAGONG_JIJI_COMPLETE.md  
- 용신: DONSAGONG_YONGSHIN_MATRIX.md
- 조후: DONSAGONG_JOHU_COMPLETE.md

## 🚀 사용법
```python
from src.manseryeok.donsagong_strict_analyzer import DonsagongStrictAnalyzer

analyzer = DonsagongStrictAnalyzer()

# 1. 천간 관계 해석
result = analyzer.get_cheongan_relationship('갑', '을')

# 2. 전체 사주 분석
analysis = analyzer.strict_analyze(
    ilgan='갑',
    other_gans=['을', '병', '기'],
    jiji_list=['자', '인']
)
print(analyzer.format_analysis_result(analysis))
```

⚠️ 주의: 이 시스템은 사용자가 "돈사공 엄격 해석" 명령을 할 때만 사용하세요.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Any


class DonsagongStrictAnalyzer:
    """
    돈사공 전용 엄격한 해석기
    - 천간: DONSAGONG_CHEONGAN_COMPLETE.md만 참조
    - 지지: DONSAGONG_JIJI_COMPLETE.md만 참조  
    - 용신: DONSAGONG_YONGSHIN_MATRIX.md만 참조
    - 조후: DONSAGONG_JOHU_COMPLETE.md만 참조
    """
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent.parent / "docs"
        self.cheongan_data = None
        self.jiji_data = None
        self.yongshin_data = None
        self.johu_data = None
        
        # 천간 이름 매핑
        self.cheongan_names = {
            '갑': '甲', '을': '乙', '병': '丙', '정': '丁', '무': '戊',
            '기': '己', '경': '庚', '신': '辛', '임': '壬', '계': '癸'
        }
        
        # 지지 이름 매핑
        self.jiji_names = {
            '자': '子', '축': '丑', '인': '寅', '묘': '卯', '진': '辰', '사': '巳',
            '오': '午', '미': '未', '신': '申', '유': '酉', '술': '戌', '해': '亥'
        }
        
    def _load_file_safe(self, file_path: str) -> str:
        """파일을 안전하게 읽기"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return f"❌ 파일을 찾을 수 없습니다: {file_path}"
        except Exception as e:
            return f"❌ 파일 읽기 오류: {str(e)}"
    
    def _ensure_data_loaded(self):
        """필요한 데이터 파일들을 로드"""
        if self.cheongan_data is None:
            cheongan_path = self.base_path / "DONSAGONG_CHEONGAN_COMPLETE.md"
            self.cheongan_data = self._load_file_safe(str(cheongan_path))
            
        if self.jiji_data is None:
            jiji_path = self.base_path / "DONSAGONG_JIJI_COMPLETE.md"
            self.jiji_data = self._load_file_safe(str(jiji_path))
            
        if self.yongshin_data is None:
            yongshin_path = self.base_path / "DONSAGONG_YONGSHIN_MATRIX.md"
            self.yongshin_data = self._load_file_safe(str(yongshin_path))
            
        if self.johu_data is None:
            johu_path = self.base_path / "DONSAGONG_JOHU_COMPLETE.md"
            self.johu_data = self._load_file_safe(str(johu_path))
    
    def get_cheongan_relationship(self, ilgan: str, target_gan: str) -> Dict[str, str]:
        """
        천간 관계 해석 - CHEONGAN_COMPLETE.md만 참조
        
        Args:
            ilgan: 일간 (예: '갑' 또는 '甲')
            target_gan: 대상 천간 (예: '을' 또는 '乙')
            
        Returns:
            Dict with 'result', 'source', 'data' keys
        """
        self._ensure_data_loaded()
        
        if self.cheongan_data and self.cheongan_data.startswith("❌"):
            return {
                'result': '확인 불가',
                'source': 'DONSAGONG_CHEONGAN_COMPLETE.md',
                'data': self.cheongan_data
            }
        
        if not self.cheongan_data:
            return {
                'result': '확인 불가',
                'source': 'DONSAGONG_CHEONGAN_COMPLETE.md',
                'data': 'cheongan_data가 로드되지 않음'
            }
        
        # 한글을 한자로 변환
        ilgan_hanja = self.cheongan_names.get(ilgan, ilgan)
        target_hanja = self.cheongan_names.get(target_gan, target_gan)
        
        # 일간별 섹션 찾기 - 실제 파일 구조에 맞게 수정
        # 예: ### 갑목(甲木) 일간 → 다른 천간들
        ilgan_pattern = f"### {ilgan}.*\\({ilgan_hanja}.*\\) 일간 → 다른 천간들"
        section_match = re.search(ilgan_pattern, self.cheongan_data)
        
        if not section_match:
            # 패턴을 더 유연하게 시도
            ilgan_pattern2 = f"### .*{ilgan_hanja}.*일간"
            section_match = re.search(ilgan_pattern2, self.cheongan_data)
            
        if not section_match:
            return {
                'result': '확인 불가',
                'source': 'DONSAGONG_CHEONGAN_COMPLETE.md',
                'data': f"일간 {ilgan}({ilgan_hanja}) 섹션을 찾을 수 없습니다."
            }
        
        # 해당 일간 섹션에서 대상 천간 행 찾기
        section_start = section_match.end()
        next_section = re.search(r"###", self.cheongan_data[section_start:])
        section_end = section_start + next_section.start() if next_section else len(self.cheongan_data)
        
        ilgan_section = self.cheongan_data[section_start:section_end]
        
        # 테이블에서 대상 천간 행 찾기
        # 실제 형태: | 甲 | 평 | 甲甲같이 원국에 함께 있을 때 흉. 대운으로 들어올 때는 길,흉에 따라 일이 발생 | 비견 |
        target_patterns = [
            f"\\| {target_hanja} \\| ([^|]+) \\| ([^|]+) \\| ([^|]+) \\|",
            f"\\| \\*\\*{target_hanja}\\*\\* \\| \\*\\*([^|]+)\\*\\* \\| \\*\\*([^|]+)\\*\\* \\| ([^|]+) \\|"  # 굵은 글씨 패턴
        ]
        
        target_match = None
        for pattern in target_patterns:
            target_match = re.search(pattern, ilgan_section)
            if target_match:
                break
        
        if not target_match:
            return {
                'result': '확인 불가',
                'source': 'DONSAGONG_CHEONGAN_COMPLETE.md',
                'data': f"일간 {ilgan}({ilgan_hanja})에서 대상 천간 {target_gan}({target_hanja}) 정보를 찾을 수 없습니다.\n섹션 일부: {ilgan_section[:200]}..."
            }
        
        gilhung = target_match.group(1).strip()
        description = target_match.group(2).strip()
        tongbyeon = target_match.group(3).strip()
        
        return {
            'result': f"일간 {ilgan}({ilgan_hanja}) → {target_gan}({target_hanja}): {gilhung}",
            'source': 'DONSAGONG_CHEONGAN_COMPLETE.md',
            'data': {
                'gilhung': gilhung,
                'description': description,
                'tongbyeon': tongbyeon,
                'raw_match': target_match.group(0)
            }
        }
    
    def get_jiji_relationship(self, target_jiji: str) -> Dict[str, str]:
        """
        지지 해석 - JIJI_COMPLETE.md만 참조
        
        Args:
            target_jiji: 대상 지지 (예: '자' 또는 '子')
            
        Returns:
            Dict with 'result', 'source', 'data' keys
        """
        self._ensure_data_loaded()
        
        if self.jiji_data and self.jiji_data.startswith("❌"):
            return {
                'result': '확인 불가',
                'source': 'DONSAGONG_JIJI_COMPLETE.md',
                'data': self.jiji_data
            }
        
        # 한글을 한자로 변환
        jiji_hanja = self.jiji_names.get(target_jiji, target_jiji)
        
        # 지지별 섹션 찾기
        jiji_pattern = f"## {target_jiji}\\({jiji_hanja}\\)|## {jiji_hanja}"
        section_match = re.search(jiji_pattern, self.jiji_data)
        
        if not section_match:
            return {
                'result': '확인 불가',
                'source': 'DONSAGONG_JIJI_COMPLETE.md',
                'data': f"지지 {target_jiji}({jiji_hanja}) 섹션을 찾을 수 없습니다."
            }
        
        # 해당 지지 섹션 추출
        section_start = section_match.start()
        next_section = re.search(r"^## ", self.jiji_data[section_start + 1:], re.MULTILINE)
        section_end = section_start + next_section.start() + 1 if next_section else len(self.jiji_data)
        
        jiji_section = self.jiji_data[section_start:section_end]
        
        return {
            'result': f"지지 {target_jiji}({jiji_hanja}) 정보 추출 완료",
            'source': 'DONSAGONG_JIJI_COMPLETE.md',
            'data': jiji_section[:500] + "..." if len(jiji_section) > 500 else jiji_section
        }
    
    def get_yongshin_info(self, ilgan: str, season: str = None) -> Dict[str, str]:
        """
        용신 정보 - YONGSHIN_MATRIX.md만 참조
        
        Args:
            ilgan: 일간 (예: '갑' 또는 '甲')
            season: 계절 정보 (선택사항)
            
        Returns:
            Dict with 'result', 'source', 'data' keys
        """
        self._ensure_data_loaded()
        
        if self.yongshin_data and self.yongshin_data.startswith("❌"):
            return {
                'result': '확인 불가',
                'source': 'DONSAGONG_YONGSHIN_MATRIX.md',
                'data': self.yongshin_data
            }
        
        # 한글을 한자로 변환
        ilgan_hanja = self.cheongan_names.get(ilgan, ilgan)
        
        # 일간별 용신 섹션 찾기
        ilgan_pattern = f"### {ilgan}목\\({ilgan_hanja}木\\) 일간|### {ilgan}화\\({ilgan_hanja}火\\) 일간|### {ilgan}토\\({ilgan_hanja}土\\) 일간|### {ilgan}금\\({ilgan_hanja}金\\) 일간|### {ilgan}수\\({ilgan_hanja}水\\) 일간"
        section_match = re.search(ilgan_pattern, self.yongshin_data)
        
        if not section_match:
            return {
                'result': '확인 불가',
                'source': 'DONSAGONG_YONGSHIN_MATRIX.md',
                'data': f"일간 {ilgan}({ilgan_hanja}) 용신 섹션을 찾을 수 없습니다."
            }
        
        # 해당 일간 섹션 추출
        section_start = section_match.start()
        next_section = re.search(r"^### ", self.yongshin_data[section_start + 1:], re.MULTILINE)
        section_end = section_start + next_section.start() + 1 if next_section else len(self.yongshin_data)
        
        yongshin_section = self.yongshin_data[section_start:section_end]
        
        return {
            'result': f"일간 {ilgan}({ilgan_hanja}) 용신 정보 추출 완료",
            'source': 'DONSAGONG_YONGSHIN_MATRIX.md',
            'data': yongshin_section[:500] + "..." if len(yongshin_section) > 500 else yongshin_section
        }
    
    def get_johu_info(self, ilgan: str, season: str = None) -> Dict[str, str]:
        """
        조후 정보 - JOHU_COMPLETE.md만 참조
        
        Args:
            ilgan: 일간 (예: '갑' 또는 '甲')
            season: 계절 정보 (선택사항)
            
        Returns:
            Dict with 'result', 'source', 'data' keys
        """
        self._ensure_data_loaded()
        
        if self.johu_data and self.johu_data.startswith("❌"):
            return {
                'result': '확인 불가',
                'source': 'DONSAGONG_JOHU_COMPLETE.md',
                'data': self.johu_data
            }
        
        # 한글을 한자로 변환
        ilgan_hanja = self.cheongan_names.get(ilgan, ilgan)
        
        # 일간별 조후 섹션 찾기 (더 유연한 패턴)
        ilgan_pattern = f"{ilgan}.*{ilgan_hanja}|{ilgan_hanja}"
        matches = re.finditer(ilgan_pattern, self.johu_data)
        
        relevant_sections = []
        for match in matches:
            # 매치 주변 컨텍스트 추출
            start = max(0, match.start() - 100)
            end = min(len(self.johu_data), match.end() + 200)
            context = self.johu_data[start:end]
            relevant_sections.append(context)
        
        if not relevant_sections:
            return {
                'result': '확인 불가',
                'source': 'DONSAGONG_JOHU_COMPLETE.md',
                'data': f"일간 {ilgan}({ilgan_hanja}) 조후 정보를 찾을 수 없습니다."
            }
        
        return {
            'result': f"일간 {ilgan}({ilgan_hanja}) 조후 정보 추출 완료",
            'source': 'DONSAGONG_JOHU_COMPLETE.md',
            'data': relevant_sections[0][:500] + "..." if len(relevant_sections[0]) > 500 else relevant_sections[0]
        }
    
    def strict_analyze(self, ilgan: str, other_gans: List[str] = None, jiji_list: List[str] = None) -> Dict[str, Any]:
        """
        돈사공 엄격 해석 - 데이터베이스만 참조하여 해석
        
        Args:
            ilgan: 일간
            other_gans: 분석할 다른 천간들
            jiji_list: 분석할 지지들
            
        Returns:
            완전한 분석 결과
        """
        results = {
            'ilgan': ilgan,
            'cheongan_analysis': {},
            'jiji_analysis': {},
            'yongshin_info': {},
            'johu_info': {},
            'safety_check': '✅ 오직 돈사공 데이터베이스만 참조함',
            'sources': []
        }
        
        # 천간 관계 분석
        if other_gans:
            for gan in other_gans:
                result = self.get_cheongan_relationship(ilgan, gan)
                results['cheongan_analysis'][gan] = result
                if result['source'] not in results['sources']:
                    results['sources'].append(result['source'])
        
        # 지지 분석
        if jiji_list:
            for jiji in jiji_list:
                result = self.get_jiji_relationship(jiji)
                results['jiji_analysis'][jiji] = result
                if result['source'] not in results['sources']:
                    results['sources'].append(result['source'])
        
        # 용신 정보
        yongshin_result = self.get_yongshin_info(ilgan)
        results['yongshin_info'] = yongshin_result
        if yongshin_result['source'] not in results['sources']:
            results['sources'].append(yongshin_result['source'])
        
        # 조후 정보
        johu_result = self.get_johu_info(ilgan)
        results['johu_info'] = johu_result
        if johu_result['source'] not in results['sources']:
            results['sources'].append(johu_result['source'])
        
        return results
    
    def format_analysis_result(self, analysis_result: Dict[str, Any]) -> str:
        """분석 결과를 읽기 쉽게 포맷팅"""
        output = []
        output.append("🔍 돈사공 엄격 해석 결과")
        output.append("=" * 50)
        output.append(f"📍 일간: {analysis_result['ilgan']}")
        output.append(f"🛡️ 안전장치: {analysis_result['safety_check']}")
        output.append(f"📚 참조 출처: {', '.join(analysis_result['sources'])}")
        output.append("")
        
        # 천간 관계 결과
        if analysis_result['cheongan_analysis']:
            output.append("🌟 천간 관계 분석")
            output.append("-" * 30)
            for gan, result in analysis_result['cheongan_analysis'].items():
                output.append(f"• {result['result']}")
                if isinstance(result['data'], dict) and 'description' in result['data']:
                    output.append(f"  └ {result['data']['description']}")
            output.append("")
        
        # 지지 분석 결과
        if analysis_result['jiji_analysis']:
            output.append("🏔️ 지지 분석")
            output.append("-" * 30)
            for jiji, result in analysis_result['jiji_analysis'].items():
                output.append(f"• {result['result']}")
            output.append("")
        
        # 용신 정보
        if analysis_result['yongshin_info']['result'] != '확인 불가':
            output.append("⚔️ 용신 정보")
            output.append("-" * 30)
            output.append(f"• {analysis_result['yongshin_info']['result']}")
            output.append("")
        
        # 조후 정보
        if analysis_result['johu_info']['result'] != '확인 불가':
            output.append("🌡️ 조후 정보")
            output.append("-" * 30)
            output.append(f"• {analysis_result['johu_info']['result']}")
            output.append("")
        
        return "\n".join(output)


# 사용 예시 및 테스트
def test_strict_analyzer():
    """엄격 분석기 테스트"""
    analyzer = DonsagongStrictAnalyzer()
    
    # 테스트 1: 갑목 일간 기본 분석
    print("=== 테스트 1: 갑목 일간 기본 분석 ===")
    result1 = analyzer.strict_analyze(
        ilgan='갑',
        other_gans=['을', '병', '기', '경'],
        jiji_list=['자', '인']
    )
    print(analyzer.format_analysis_result(result1))
    
    print("\n" + "="*60 + "\n")
    
    # 테스트 2: 개별 관계 확인
    print("=== 테스트 2: 개별 관계 확인 ===")
    cheongan_rel = analyzer.get_cheongan_relationship('갑', '경')
    print(f"천간 관계: {cheongan_rel['result']}")
    print(f"출처: {cheongan_rel['source']}")
    if isinstance(cheongan_rel['data'], dict):
        print(f"상세: {cheongan_rel['data']['description']}")
    
    print("\n" + "="*60 + "\n")
    
    # 테스트 3: 용신 정보
    print("=== 테스트 3: 용신 정보 ===")
    yongshin_info = analyzer.get_yongshin_info('갑')
    print(f"용신 정보: {yongshin_info['result']}")
    print(f"출처: {yongshin_info['source']}")
    
    print("\n" + "="*60 + "\n")
    
    # 테스트 4: 병화 일간 분석 (특별한 관계 확인)
    print("=== 테스트 4: 병화 일간 임수 관계 (특별 길함) ===")
    byeong_im = analyzer.get_cheongan_relationship('병', '임')
    print(f"병화-임수 관계: {byeong_im['result']}")
    if isinstance(byeong_im['data'], dict):
        print(f"설명: {byeong_im['data']['description']}")
        print(f"길흉: {byeong_im['data']['gilhung']}")
    
    print("\n" + "="*60 + "\n")
    
    # 테스트 5: 합(合) 관계들 - 돈사공에서는 모두 흉함
    print("=== 테스트 5: 합(合) 관계들 (돈사공에서는 모두 흉함) ===")
    hap_relations = [
        ('갑', '기'),  # 갑기합
        ('을', '경'),  # 을경합  
        ('병', '신'),  # 병신합
        ('정', '임'),  # 정임합
        ('무', '계')   # 무계합
    ]
    
    for ilgan, target in hap_relations:
        rel = analyzer.get_cheongan_relationship(ilgan, target)
        if isinstance(rel['data'], dict):
            print(f"{ilgan}-{target} 합: {rel['data']['gilhung']} - {rel['data']['description']}")
        else:
            print(f"{ilgan}-{target}: {rel['result']}")


def demo_strict_usage():
    """돈사공 엄격 해석 시스템 사용 데모"""
    print("🔮 돈사공 엄격 해석 시스템 데모")
    print("=" * 50)
    
    analyzer = DonsagongStrictAnalyzer()
    
    # 실제 사용 케이스: 사주 해석
    print("\n📋 사주 예시 해석")
    print("-" * 30)
    
    # 예시: 갑목 일간이 있는 사주
    saju_example = {
        'year_gan': '임', 'year_ji': '인',
        'month_gan': '정', 'month_ji': '해',
        'day_gan': '갑', 'day_ji': '오',
        'hour_gan': '기', 'hour_ji': '사'
    }
    
    ilgan = saju_example['day_gan']
    other_gans = [saju_example['year_gan'], saju_example['month_gan'], saju_example['hour_gan']]
    
    print(f"일간: {ilgan}")
    print(f"분석 대상 천간: {other_gans}")
    
    # 각 천간과의 관계 분석
    print(f"\n🌟 {ilgan}목 일간과 다른 천간들의 관계:")
    for gan in other_gans:
        rel = analyzer.get_cheongan_relationship(ilgan, gan)
        if isinstance(rel['data'], dict):
            print(f"  • {ilgan} → {gan}: {rel['data']['gilhung']}")
            print(f"    └ {rel['data']['description']}")
        else:
            print(f"  • {ilgan} → {gan}: {rel['result']}")
    
    # 용신 확인
    print(f"\n⚔️ {ilgan}목 일간의 용신:")
    yongshin = analyzer.get_yongshin_info(ilgan)
    if 'data' in yongshin and len(str(yongshin['data'])) > 100:
        print(f"  출처: {yongshin['source']}")
        print(f"  상태: {yongshin['result']}")
    
    print(f"\n✅ 모든 해석은 오직 돈사공 데이터베이스에서만 추출됨")
    print(f"📚 참조 파일: DONSAGONG_CHEONGAN_COMPLETE.md")


if __name__ == "__main__":
    test_strict_analyzer()
    print("\n" + "🔮" * 30 + "\n")
    demo_strict_usage()