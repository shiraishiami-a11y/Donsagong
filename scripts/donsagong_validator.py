#!/usr/bin/env python3
"""
돈사공 데이터 순수성 검증 도구
전통 명리학 용어 오염을 자동으로 감지하고 방지
"""

import re
import os
import json
from datetime import datetime
from typing import Dict, List, Tuple
from pathlib import Path

class DonsagongValidator:
    """돈사공 데이터 검증 클래스"""
    
    def __init__(self):
        # 금지된 전통 명리학 용어
        self.forbidden_terms = {
            '십신론': [
                '정관', '편관', '정재', '편재', '정인', '편인',
                '식신', '상관', '비견', '겁재', '건록', '제왕'
            ],
            '오행론': [
                '목생화', '화생토', '토생금', '금생수', '수생목',
                '금극목', '목극토', '토극수', '수극화', '화극금',
                '상생', '상극', '생극', '극생'
            ],
            '신강신약': [
                '신강', '신약', '일간이 강', '일간이 약',
                '일간 강약', '왕성', '쇠약', '태과', '불급'
            ],
            '전통해석': [
                '부족한 오행', '오행 균형', '오행 보충',
                '억부', '통관', '조후용신이 부족',
                '년주', '4주', '사주팔자'
            ]
        }
        
        # 돈사공 전용 허용 용어
        self.allowed_terms = {
            '핵심개념': [
                '용신은 무기', '일지지 합은 길', '조후용신 80%',
                '원국 20%', '3주 시스템', '월지지는 용신 불가'
            ],
            '길흉판단': [
                '대길', '길', '평', '흉', '대흉',
                '길흉', '소길', '무관계'
            ],
            '돈사공용어': [
                '천간 용신', '지지 용신', '조후 용신',
                '공통원국지지용신', '일지지', '방어막'
            ]
        }
        
        # 검증 결과 저장
        self.validation_results = []
        self.contamination_score = 100  # 시작 점수
        
    def scan_file(self, filepath: str) -> Dict[str, any]:
        """파일 스캔 및 오염도 검사"""
        results = {
            'file': filepath,
            'timestamp': datetime.now().isoformat(),
            'forbidden_found': [],
            'warnings': [],
            'score': 100
        }
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 금지어 검색
            for category, terms in self.forbidden_terms.items():
                for term in terms:
                    if term in content:
                        results['forbidden_found'].append({
                            'category': category,
                            'term': term,
                            'count': content.count(term)
                        })
                        results['score'] -= 10  # 금지어당 -10점
                        
            # 의심스러운 패턴 검색
            suspicious_patterns = [
                (r'부족.*보충', '부족을 보충하는 개념 발견'),
                (r'균형.*맞추', '균형을 맞추는 개념 발견'),
                (r'상생.*관계', '오행 상생 관계 언급'),
                (r'년.*월.*일.*시', '4주 체계 언급 가능성')
            ]
            
            for pattern, warning in suspicious_patterns:
                if re.search(pattern, content):
                    results['warnings'].append(warning)
                    results['score'] -= 5  # 경고당 -5점
                    
        except Exception as e:
            results['error'] = str(e)
            results['score'] = 0
            
        results['score'] = max(0, results['score'])  # 최소 0점
        return results
    
    def validate_directory(self, directory: str) -> List[Dict]:
        """디렉토리 전체 검증"""
        all_results = []
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(('.md', '.txt', '.py')):
                    filepath = os.path.join(root, file)
                    result = self.scan_file(filepath)
                    all_results.append(result)
                    
        return all_results
    
    def generate_report(self, results: List[Dict]) -> str:
        """검증 보고서 생성"""
        report = []
        report.append("="*50)
        report.append("돈사공 데이터 순수성 검증 보고서")
        report.append(f"검증 일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("="*50)
        report.append("")
        
        # 전체 점수 계산
        total_files = len(results)
        avg_score = sum(r['score'] for r in results) / total_files if total_files > 0 else 0
        
        # 위험도 평가
        if avg_score >= 90:
            risk_level = "🟢 안전"
        elif avg_score >= 70:
            risk_level = "🟡 주의"
        else:
            risk_level = "🔴 위험"
            
        report.append(f"전체 순수도 점수: {avg_score:.1f}/100")
        report.append(f"위험도 평가: {risk_level}")
        report.append(f"검사 파일 수: {total_files}")
        report.append("")
        
        # 오염된 파일 상세
        contaminated = [r for r in results if r['score'] < 100]
        if contaminated:
            report.append("⚠️ 오염 발견 파일:")
            report.append("-"*30)
            for result in contaminated:
                report.append(f"\n파일: {result['file']}")
                report.append(f"점수: {result['score']}/100")
                
                if result.get('forbidden_found'):
                    report.append("  금지어 발견:")
                    for item in result['forbidden_found']:
                        report.append(f"    - {item['term']} ({item['count']}회)")
                        
                if result.get('warnings'):
                    report.append("  경고:")
                    for warning in result['warnings']:
                        report.append(f"    - {warning}")
                        
        else:
            report.append("✅ 모든 파일이 깨끗합니다!")
            
        return "\n".join(report)
    
    def auto_clean(self, filepath: str) -> Tuple[bool, str]:
        """자동 정화 기능 (금지어 제거)"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            original_content = content
            cleaned = False
            
            # 금지어 자동 제거
            for category, terms in self.forbidden_terms.items():
                for term in terms:
                    if term in content:
                        # 금지어를 [제거됨]으로 표시
                        content = content.replace(term, f"[{term} 제거됨]")
                        cleaned = True
                        
            if cleaned:
                # 백업 생성
                backup_path = filepath + '.backup'
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(original_content)
                    
                # 정화된 내용 저장
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
                return True, f"정화 완료. 백업: {backup_path}"
            else:
                return False, "정화 불필요 (이미 깨끗함)"
                
        except Exception as e:
            return False, f"오류 발생: {str(e)}"

def main():
    """메인 실행 함수"""
    validator = DonsagongValidator()
    
    # 검증할 디렉토리 설정
    docs_dir = "/Users/shiraishiami/Desktop/Bluelamp/test-project/docs"
    
    print("돈사공 데이터 순수성 검증 시작...")
    print(f"대상 디렉토리: {docs_dir}")
    print("-"*50)
    
    # 검증 실행
    results = validator.validate_directory(docs_dir)
    
    # 보고서 생성 및 출력
    report = validator.generate_report(results)
    print(report)
    
    # 보고서 파일 저장
    report_path = f"validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\n보고서 저장: {report_path}")
    
    # 오염된 파일 자동 정화 옵션
    contaminated = [r for r in results if r['score'] < 100]
    if contaminated:
        response = input("\n오염된 파일을 자동으로 정화하시겠습니까? (y/n): ")
        if response.lower() == 'y':
            for result in contaminated:
                success, message = validator.auto_clean(result['file'])
                print(f"{result['file']}: {message}")

if __name__ == "__main__":
    main()