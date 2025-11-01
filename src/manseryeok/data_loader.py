"""
돈사공 데이터베이스 로더

DONSAGONG_MASTER_DATABASE.md 파일을 파싱하여 돈사공 해석 데이터를 로드하고 관리하는 모듈
"""

import os
import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class TenganRelation:
    """천간 관계 정보"""
    from_gan: str
    to_gan: str
    fortune: str  # 길/흉/평/무 등
    description: str
    note: str = ""


@dataclass
class JijiRelation:
    """지지 관계 정보"""
    from_ji: str
    to_ji: str
    relation_type: str  # 합/충/형/파 등
    fortune: str
    description: str


@dataclass
class SeasonInfo:
    """계절별 정보"""
    season: str
    description: str
    fortune: str


class DonsagongDataLoader:
    """돈사공 데이터베이스 로더"""
    
    def __init__(self, db_file_path: str = None):
        """
        Args:
            db_file_path: 돈사공 데이터베이스 파일 경로
        """
        if db_file_path is None:
            # 기본 경로 설정
            current_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            db_file_path = os.path.join(current_dir, "DONSAGONG_MASTER_DATABASE.md")
        
        self.db_file_path = db_file_path
        
        # 데이터 저장소
        self.tengan_relations: Dict[str, Dict[str, TenganRelation]] = {}
        self.jiji_relations: Dict[str, List[JijiRelation]] = {}
        self.seasonal_info: Dict[str, SeasonInfo] = {}
        self.yongshin_info: Dict[str, Dict] = {}
        self.johoo_info: Dict[str, Dict] = {}
        
        # 데이터 로드
        self._load_data()
    
    def _load_data(self):
        """데이터베이스 파일 로드 및 파싱"""
        if not os.path.exists(self.db_file_path):
            raise FileNotFoundError(f"돈사공 데이터베이스 파일을 찾을 수 없습니다: {self.db_file_path}")
        
        try:
            with open(self.db_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 각 섹션별로 파싱
            self._parse_tengan_matrix(content)
            self._parse_jiji_relations(content)
            self._parse_seasonal_info(content)
            self._parse_yongshin_info(content)
            self._parse_johoo_info(content)
            
        except Exception as e:
            raise Exception(f"데이터베이스 파일 로드 실패: {str(e)}")
    
    def _parse_tengan_matrix(self, content: str):
        """천간 100매트릭스 파싱"""
        # 천간명 매핑
        gan_map = {
            '갑': '甲', '을': '乙', '병': '丙', '정': '丁', '무': '戊',
            '기': '己', '경': '庚', '신': '辛', '임': '壬', '계': '癸'
        }
        
        # 각 천간별 섹션 찾기
        tengan_sections = re.findall(r'### (.+?)\s*→\s*다른 천간들.*?\n(.*?)(?=###|\n---|\Z)', content, re.DOTALL)
        
        for section_title, section_content in tengan_sections:
            # 천간명 추출 (예: "갑목(甲木)" -> "甲")
            from_gan_match = re.search(r'([갑을병정무기경신임계])', section_title)
            if not from_gan_match:
                continue
            
            from_gan_korean = from_gan_match.group(1)
            from_gan = gan_map.get(from_gan_korean, from_gan_korean)
            
            if from_gan not in self.tengan_relations:
                self.tengan_relations[from_gan] = {}
            
            # 테이블 행 파싱
            table_rows = re.findall(r'\|\s*([甲乙丙丁戊己庚辛壬癸])\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]*)\s*\|', section_content)
            
            for to_gan, fortune, description, note in table_rows:
                # 데이터 정리
                fortune = fortune.strip()
                description = description.strip()
                note = note.strip() if note else ""
                
                # 관계 정보 저장
                relation = TenganRelation(
                    from_gan=from_gan,
                    to_gan=to_gan,
                    fortune=fortune,
                    description=description,
                    note=note
                )
                self.tengan_relations[from_gan][to_gan] = relation
    
    def _parse_jiji_relations(self, content: str):
        """지지 관계 파싱"""
        # 지지 합/충/형 섹션 찾기
        jiji_sections = re.findall(r'## .*?지지.*?\n(.*?)(?=##|\Z)', content, re.DOTALL)
        
        for section_content in jiji_sections:
            # 관계별로 파싱 (예: 삼합, 육합, 충, 형 등)
            relation_blocks = re.findall(r'### (.+?)\n(.*?)(?=###|\n---|\Z)', section_content, re.DOTALL)
            
            for relation_title, relation_content in relation_blocks:
                self._parse_jiji_relation_block(relation_title, relation_content)
    
    def _parse_jiji_relation_block(self, relation_title: str, content: str):
        """개별 지지 관계 블록 파싱"""
        # 표 형태 데이터 파싱
        table_rows = re.findall(r'\|([^|]+)\|([^|]+)\|([^|]+)\|', content)
        
        for row in table_rows:
            if len(row) >= 3:
                jiji_combo = row[0].strip()
                fortune = row[1].strip()
                description = row[2].strip()
                
                # 지지 조합 분리 (예: "자축인" -> ["자", "축", "인"])
                if len(jiji_combo) >= 2:
                    for i, from_ji in enumerate(jiji_combo):
                        for j, to_ji in enumerate(jiji_combo):
                            if i != j:
                                relation = JijiRelation(
                                    from_ji=from_ji,
                                    to_ji=to_ji,
                                    relation_type=relation_title,
                                    fortune=fortune,
                                    description=description
                                )
                                
                                if from_ji not in self.jiji_relations:
                                    self.jiji_relations[from_ji] = []
                                
                                self.jiji_relations[from_ji].append(relation)
    
    def _parse_seasonal_info(self, content: str):
        """계절별 정보 파싱"""
        seasonal_sections = re.findall(r'## .*?계절.*?\n(.*?)(?=##|\Z)', content, re.DOTALL)
        
        for section_content in seasonal_sections:
            # 계절별 데이터 추출
            season_blocks = re.findall(r'### (.+?)\n(.*?)(?=###|\n---|\Z)', section_content, re.DOTALL)
            
            for season_title, season_content in season_blocks:
                season_info = SeasonInfo(
                    season=season_title.strip(),
                    description=season_content.strip(),
                    fortune="평"  # 기본값
                )
                
                self.seasonal_info[season_title.strip()] = season_info
    
    def _parse_yongshin_info(self, content: str):
        """용신 정보 파싱"""
        yongshin_sections = re.findall(r'## .*?용신.*?\n(.*?)(?=##|\Z)', content, re.DOTALL)
        
        for section_content in yongshin_sections:
            # 용신별 정보 추출
            self.yongshin_info = self._extract_structured_data(section_content, "용신")
    
    def _parse_johoo_info(self, content: str):
        """조후 정보 파싱"""
        johoo_sections = re.findall(r'## .*?조후.*?\n(.*?)(?=##|\Z)', content, re.DOTALL)
        
        for section_content in johoo_sections:
            # 조후별 정보 추출
            self.johoo_info = self._extract_structured_data(section_content, "조후")
    
    def _extract_structured_data(self, content: str, data_type: str) -> Dict:
        """구조화된 데이터 추출 공통 함수"""
        data = {}
        
        # 하위 섹션별로 파싱
        subsections = re.findall(r'### (.+?)\n(.*?)(?=###|\n---|\Z)', content, re.DOTALL)
        
        for title, subcontent in subsections:
            # 테이블이나 리스트 형태 데이터 파싱
            structured_content = self._parse_content_structure(subcontent)
            data[title.strip()] = structured_content
        
        return data
    
    def _parse_content_structure(self, content: str) -> Dict:
        """내용 구조 파싱"""
        result = {
            'description': '',
            'items': [],
            'conditions': {}
        }
        
        # 테이블 형태 파싱
        table_rows = re.findall(r'\|([^|]+)\|([^|]+)\|', content)
        if table_rows:
            for row in table_rows:
                if len(row) >= 2:
                    key = row[0].strip()
                    value = row[1].strip()
                    result['conditions'][key] = value
        
        # 일반 텍스트 설명
        text_content = re.sub(r'\|[^|]+\|[^|]+\|', '', content).strip()
        if text_content:
            result['description'] = text_content
        
        return result
    
    # 데이터 조회 메서드들
    
    def get_tengan_relation(self, from_gan: str, to_gan: str) -> Optional[TenganRelation]:
        """천간 관계 조회"""
        return self.tengan_relations.get(from_gan, {}).get(to_gan)
    
    def get_jiji_relations(self, from_ji: str, to_ji: str) -> List[JijiRelation]:
        """지지 관계 조회"""
        relations = self.jiji_relations.get(from_ji, [])
        return [r for r in relations if r.to_ji == to_ji]
    
    def get_seasonal_info(self, season: str) -> Optional[SeasonInfo]:
        """계절 정보 조회"""
        return self.seasonal_info.get(season)
    
    def get_yongshin_info(self, key: str) -> Optional[Dict]:
        """용신 정보 조회"""
        return self.yongshin_info.get(key)
    
    def get_johoo_info(self, key: str) -> Optional[Dict]:
        """조후 정보 조회"""
        return self.johoo_info.get(key)
    
    def get_all_tengan_relations(self, from_gan: str) -> Dict[str, TenganRelation]:
        """특정 천간의 모든 관계 조회"""
        return self.tengan_relations.get(from_gan, {})
    
    def search_relations_by_fortune(self, fortune: str) -> List[TenganRelation]:
        """길흉별 관계 검색"""
        results = []
        
        for from_gan, relations in self.tengan_relations.items():
            for to_gan, relation in relations.items():
                if fortune in relation.fortune:
                    results.append(relation)
        
        return results
    
    def validate_data(self) -> bool:
        """데이터 무결성 검증"""
        try:
            # 천간 데이터 검증
            expected_gans = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
            
            for gan in expected_gans:
                if gan not in self.tengan_relations:
                    print(f"누락된 천간: {gan}")
                    return False
                
                if len(self.tengan_relations[gan]) < 9:  # 자기 자신 제외 9개
                    print(f"불완전한 천간 관계: {gan}")
                    return False
            
            print("데이터베이스 검증 완료")
            return True
            
        except Exception as e:
            print(f"데이터 검증 실패: {str(e)}")
            return False
    
    def get_database_stats(self) -> Dict:
        """데이터베이스 통계 정보"""
        total_tengan_relations = sum(len(relations) for relations in self.tengan_relations.values())
        total_jiji_relations = sum(len(relations) for relations in self.jiji_relations.values())
        
        return {
            'tengan_entries': len(self.tengan_relations),
            'total_tengan_relations': total_tengan_relations,
            'jiji_entries': len(self.jiji_relations),
            'total_jiji_relations': total_jiji_relations,
            'seasonal_info': len(self.seasonal_info),
            'yongshin_info': len(self.yongshin_info),
            'johoo_info': len(self.johoo_info)
        }