"""
돈사공 해석 엔진

사주팔자를 돈사공 이론에 따라 해석하고 길흉 판단 및 상세 해석을 생성하는 모듈
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from .calculator import SajuPalja, HEAVENLY_STEMS, EARTHLY_BRANCHES
from .data_loader import DonsagongDataLoader, TenganRelation


@dataclass
class AnalysisResult:
    """해석 결과"""
    overall_fortune: str  # 전체 길흉
    detailed_analysis: Dict[str, str]  # 상세 분석
    recommendations: List[str]  # 권고사항
    warnings: List[str]  # 주의사항
    strengths: List[str]  # 장점
    weaknesses: List[str]  # 단점


@dataclass
class PillarAnalysis:
    """기둥별 분석"""
    pillar_name: str  # 연주/월주/일주/시주
    stem: str
    branch: str
    fortune: str
    description: str
    special_notes: List[str]


@dataclass
class RelationAnalysis:
    """관계 분석"""
    relation_type: str  # 천간관계/지지관계 등
    from_element: str
    to_element: str
    fortune: str
    description: str
    impact_level: str  # 강/중/약


class DonsagongAnalyzer:
    """돈사공 해석 엔진"""
    
    def __init__(self, data_loader: DonsagongDataLoader = None):
        """
        Args:
            data_loader: 돈사공 데이터 로더 (None이면 자동 생성)
        """
        self.data_loader = data_loader or DonsagongDataLoader()
        
        # 분석 가중치 설정
        self.weights = {
            'tengan_same_pillar': 0.4,    # 같은 기둥 내 천간 관계
            'tengan_cross_pillar': 0.3,   # 기둥 간 천간 관계
            'jiji_relation': 0.2,         # 지지 관계
            'seasonal_factor': 0.1        # 계절적 요인
        }
    
    def analyze_saju(self, saju: SajuPalja) -> AnalysisResult:
        """
        사주팔자 전체 분석
        
        Args:
            saju: 사주팔자 정보
        
        Returns:
            AnalysisResult: 종합 해석 결과
        """
        # 1. 기둥별 개별 분석
        pillar_analyses = self._analyze_pillars(saju)
        
        # 2. 천간 관계 분석
        tengan_relations = self._analyze_tengan_relations(saju)
        
        # 3. 지지 관계 분석
        jiji_relations = self._analyze_jiji_relations(saju)
        
        # 4. 계절별 요인 분석
        seasonal_analysis = self._analyze_seasonal_factors(saju)
        
        # 5. 종합 길흉 판단
        overall_fortune = self._calculate_overall_fortune(
            pillar_analyses, tengan_relations, jiji_relations, seasonal_analysis
        )
        
        # 6. 상세 해석 생성
        detailed_analysis = self._generate_detailed_analysis(
            saju, pillar_analyses, tengan_relations, jiji_relations, seasonal_analysis
        )
        
        # 7. 권고사항 및 주의사항 생성
        recommendations, warnings = self._generate_recommendations_and_warnings(
            overall_fortune, tengan_relations, jiji_relations
        )
        
        # 8. 장단점 분석
        strengths, weaknesses = self._analyze_strengths_and_weaknesses(
            tengan_relations, jiji_relations
        )
        
        return AnalysisResult(
            overall_fortune=overall_fortune,
            detailed_analysis=detailed_analysis,
            recommendations=recommendations,
            warnings=warnings,
            strengths=strengths,
            weaknesses=weaknesses
        )
    
    def _analyze_pillars(self, saju: SajuPalja) -> List[PillarAnalysis]:
        """기둥별 개별 분석"""
        pillars = [
            ('연주', saju.year_stem, saju.year_branch),
            ('월주', saju.month_stem, saju.month_branch),
            ('일주', saju.day_stem, saju.day_branch),
            ('시주', saju.hour_stem, saju.hour_branch)
        ]
        
        analyses = []
        
        for pillar_name, stem, branch in pillars:
            # 해당 기둥의 천간-지지 관계 분석
            analysis = self._analyze_single_pillar(pillar_name, stem, branch)
            analyses.append(analysis)
        
        return analyses
    
    def _analyze_single_pillar(self, pillar_name: str, stem: str, branch: str) -> PillarAnalysis:
        """단일 기둥 분석"""
        # 천간-지지 관계 조회 (간접적 관계)
        description = f"{stem}{branch} 조합"
        fortune = "평"
        special_notes = []
        
        # 특수한 조합 확인
        if self._is_special_combination(stem, branch):
            fortune = "길"
            special_notes.append("특별한 길한 조합")
        
        return PillarAnalysis(
            pillar_name=pillar_name,
            stem=stem,
            branch=branch,
            fortune=fortune,
            description=description,
            special_notes=special_notes
        )
    
    def _is_special_combination(self, stem: str, branch: str) -> bool:
        """특수 조합 확인"""
        # 돈사공에서 특별히 길한 조합들 확인
        special_combinations = {
            ('甲', '寅'), ('乙', '卯'), ('丙', '午'), ('丁', '巳'),
            ('戊', '辰'), ('己', '未'), ('庚', '申'), ('辛', '酉'),
            ('壬', '子'), ('癸', '亥')
        }
        
        return (stem, branch) in special_combinations
    
    def _analyze_tengan_relations(self, saju: SajuPalja) -> List[RelationAnalysis]:
        """천간 관계 분석"""
        stems = [saju.year_stem, saju.month_stem, saju.day_stem, saju.hour_stem]
        relations = []
        
        # 모든 천간 조합에 대해 관계 분석
        for i, from_stem in enumerate(stems):
            for j, to_stem in enumerate(stems):
                if i != j:  # 자기 자신과의 관계는 제외
                    relation = self.data_loader.get_tengan_relation(from_stem, to_stem)
                    
                    if relation:
                        impact_level = self._calculate_impact_level(i, j, relation.fortune)
                        
                        relations.append(RelationAnalysis(
                            relation_type="천간관계",
                            from_element=from_stem,
                            to_element=to_stem,
                            fortune=relation.fortune,
                            description=relation.description,
                            impact_level=impact_level
                        ))
        
        return relations
    
    def _analyze_jiji_relations(self, saju: SajuPalja) -> List[RelationAnalysis]:
        """지지 관계 분석"""
        branches = [saju.year_branch, saju.month_branch, saju.day_branch, saju.hour_branch]
        relations = []
        
        # 지지 간 특수 관계 확인 (합, 충, 형, 파 등)
        for i, from_branch in enumerate(branches):
            for j, to_branch in enumerate(branches):
                if i != j:
                    jiji_relations = self.data_loader.get_jiji_relations(from_branch, to_branch)
                    
                    for relation in jiji_relations:
                        impact_level = self._calculate_jiji_impact_level(i, j, relation.fortune)
                        
                        relations.append(RelationAnalysis(
                            relation_type=f"지지{relation.relation_type}",
                            from_element=from_branch,
                            to_element=to_branch,
                            fortune=relation.fortune,
                            description=relation.description,
                            impact_level=impact_level
                        ))
        
        return relations
    
    def _analyze_seasonal_factors(self, saju: SajuPalja) -> Dict[str, str]:
        """계절적 요인 분석"""
        birth_month = saju.birth_datetime.month
        
        # 계절 결정
        if birth_month in [3, 4, 5]:
            season = "봄"
        elif birth_month in [6, 7, 8]:
            season = "여름"
        elif birth_month in [9, 10, 11]:
            season = "가을"
        else:
            season = "겨울"
        
        seasonal_info = self.data_loader.get_seasonal_info(season)
        
        return {
            'season': season,
            'description': seasonal_info.description if seasonal_info else f"{season} 출생",
            'fortune': seasonal_info.fortune if seasonal_info else "평"
        }
    
    def _calculate_impact_level(self, from_pos: int, to_pos: int, fortune: str) -> str:
        """천간 관계 영향도 계산"""
        # 일간(position 2)이 관련된 관계는 영향도가 높음
        if from_pos == 2 or to_pos == 2:
            if "대흉" in fortune or "대길" in fortune:
                return "강"
            elif "흉" in fortune or "길" in fortune:
                return "중"
        
        # 인접한 기둥 간의 관계
        if abs(from_pos - to_pos) == 1:
            return "중"
        
        return "약"
    
    def _calculate_jiji_impact_level(self, from_pos: int, to_pos: int, fortune: str) -> str:
        """지지 관계 영향도 계산"""
        # 일지(position 2)가 관련된 관계는 영향도가 높음
        if from_pos == 2 or to_pos == 2:
            return "강" if "대흉" in fortune or "대길" in fortune else "중"
        
        return "중" if abs(from_pos - to_pos) == 1 else "약"
    
    def _calculate_overall_fortune(self, pillar_analyses: List[PillarAnalysis],
                                 tengan_relations: List[RelationAnalysis],
                                 jiji_relations: List[RelationAnalysis],
                                 seasonal_analysis: Dict) -> str:
        """전체 길흉 계산"""
        fortune_scores = {"대길": 2, "길": 1, "평": 0, "흉": -1, "대흉": -2}
        total_score = 0
        total_weight = 0
        
        # 천간 관계 점수
        for relation in tengan_relations:
            score = fortune_scores.get(relation.fortune, 0)
            weight = 1.0
            
            if relation.impact_level == "강":
                weight = 2.0
            elif relation.impact_level == "중":
                weight = 1.5
            
            total_score += score * weight
            total_weight += weight
        
        # 지지 관계 점수
        for relation in jiji_relations:
            score = fortune_scores.get(relation.fortune, 0)
            weight = 0.8  # 지지는 천간보다 약간 낮은 가중치
            
            if relation.impact_level == "강":
                weight = 1.6
            elif relation.impact_level == "중":
                weight = 1.2
            
            total_score += score * weight
            total_weight += weight
        
        # 평균 점수 계산
        if total_weight > 0:
            average_score = total_score / total_weight
            
            if average_score >= 1.0:
                return "길"
            elif average_score >= 0.5:
                return "소길"
            elif average_score <= -1.0:
                return "흉"
            elif average_score <= -0.5:
                return "소흉"
            else:
                return "평"
        
        return "평"
    
    def _generate_detailed_analysis(self, saju: SajuPalja,
                                  pillar_analyses: List[PillarAnalysis],
                                  tengan_relations: List[RelationAnalysis],
                                  jiji_relations: List[RelationAnalysis],
                                  seasonal_analysis: Dict) -> Dict[str, str]:
        """상세 분석 생성"""
        analysis = {}
        
        # 사주 기본 정보
        analysis['기본_사주'] = f"연주: {saju.year_stem}{saju.year_branch}, 월주: {saju.month_stem}{saju.month_branch}, 일주: {saju.day_stem}{saju.day_branch}, 시주: {saju.hour_stem}{saju.hour_branch}"
        
        # 일간 중심 분석
        day_stem = saju.day_stem
        analysis['일간_분석'] = f"{day_stem}일간의 특성과 다른 천간들과의 관계가 운명을 결정합니다."
        
        # 주요 길흉 관계
        major_relations = [r for r in tengan_relations if r.impact_level in ["강", "중"] and r.fortune in ["대길", "대흉", "길", "흉"]]
        
        if major_relations:
            analysis['주요_관계'] = "중요한 관계들: " + ", ".join([
                f"{r.from_element}→{r.to_element}({r.fortune})" for r in major_relations[:3]
            ])
        
        # 계절적 영향
        analysis['계절_영향'] = f"{seasonal_analysis['season']} 출생으로 {seasonal_analysis['description']}"
        
        return analysis
    
    def _generate_recommendations_and_warnings(self, overall_fortune: str,
                                             tengan_relations: List[RelationAnalysis],
                                             jiji_relations: List[RelationAnalysis]) -> Tuple[List[str], List[str]]:
        """권고사항 및 주의사항 생성"""
        recommendations = []
        warnings = []
        
        # 전체 길흉에 따른 기본 권고
        if overall_fortune in ["길", "소길"]:
            recommendations.append("현재 사주구조가 길하므로 적극적인 행동이 유리합니다.")
        elif overall_fortune in ["흉", "소흉"]:
            recommendations.append("신중한 처신과 인내가 필요한 시기입니다.")
        
        # 대흉 관계에 대한 경고
        dangerous_relations = [r for r in tengan_relations if "대흉" in r.fortune and r.impact_level == "강"]
        
        for relation in dangerous_relations:
            warnings.append(f"{relation.from_element}→{relation.to_element} 관계가 매우 흉하니 주의가 필요합니다.")
        
        # 합(合) 관계 경고 (돈사공에서는 합이 흉)
        for relation in tengan_relations:
            if "합" in relation.description:
                warnings.append(f"{relation.from_element}{relation.to_element} 합 관계로 인한 어려움이 예상됩니다.")
        
        return recommendations, warnings
    
    def _analyze_strengths_and_weaknesses(self, tengan_relations: List[RelationAnalysis],
                                        jiji_relations: List[RelationAnalysis]) -> Tuple[List[str], List[str]]:
        """장단점 분석"""
        strengths = []
        weaknesses = []
        
        # 길한 관계들을 장점으로
        good_relations = [r for r in tengan_relations if r.fortune in ["대길", "길"] and r.impact_level in ["강", "중"]]
        
        for relation in good_relations:
            strengths.append(f"{relation.from_element}→{relation.to_element}: {relation.description}")
        
        # 흉한 관계들을 단점으로
        bad_relations = [r for r in tengan_relations if r.fortune in ["대흉", "흉"] and r.impact_level in ["강", "중"]]
        
        for relation in bad_relations:
            weaknesses.append(f"{relation.from_element}→{relation.to_element}: {relation.description}")
        
        return strengths, weaknesses
    
    def get_specific_analysis(self, saju: SajuPalja, analysis_type: str) -> Dict:
        """특정 분석 유형 조회"""
        if analysis_type == "wealth":
            return self._analyze_wealth_potential(saju)
        elif analysis_type == "career":
            return self._analyze_career_potential(saju)
        elif analysis_type == "health":
            return self._analyze_health_factors(saju)
        elif analysis_type == "relationship":
            return self._analyze_relationship_potential(saju)
        else:
            return {"error": "지원하지 않는 분석 유형입니다."}
    
    def _analyze_wealth_potential(self, saju: SajuPalja) -> Dict:
        """재물 운세 분석"""
        day_stem = saju.day_stem
        
        # 돈사공에서 재성 관계 분석
        wealth_analysis = {
            "potential": "평",
            "description": "일반적인 재운",
            "recommendations": []
        }
        
        # 일간별 재성 관계 확인
        all_relations = self.data_loader.get_all_tengan_relations(day_stem)
        
        for to_gan, relation in all_relations.items():
            if "부" in relation.description or "귀" in relation.description:
                if relation.fortune in ["길", "대길"]:
                    wealth_analysis["potential"] = "길"
                    wealth_analysis["description"] = f"{day_stem}→{to_gan}: {relation.description}"
                    break
        
        return wealth_analysis
    
    def _analyze_career_potential(self, saju: SajuPalja) -> Dict:
        """직업 운세 분석"""
        # 월주와 일간의 관계로 직업적 적성 판단
        month_stem = saju.month_stem
        day_stem = saju.day_stem
        
        relation = self.data_loader.get_tengan_relation(day_stem, month_stem)
        
        career_analysis = {
            "aptitude": "일반",
            "description": "평범한 직업 운세",
            "suitable_fields": []
        }
        
        if relation and relation.fortune in ["길", "대길"]:
            career_analysis["aptitude"] = "길"
            career_analysis["description"] = f"월간과의 관계가 좋아 직업운이 양호합니다: {relation.description}"
        
        return career_analysis
    
    def _analyze_health_factors(self, saju: SajuPalja) -> Dict:
        """건강 요소 분석"""
        # 일간과 시간의 관계로 건강 판단
        day_stem = saju.day_stem
        hour_stem = saju.hour_stem
        
        health_analysis = {
            "overall": "평",
            "concerns": [],
            "recommendations": []
        }
        
        relation = self.data_loader.get_tengan_relation(day_stem, hour_stem)
        
        if relation and "흉" in relation.fortune:
            health_analysis["overall"] = "주의"
            health_analysis["concerns"].append(f"일시 관계에 주의: {relation.description}")
            health_analysis["recommendations"].append("규칙적인 생활과 건강관리가 중요합니다.")
        
        return health_analysis
    
    def _analyze_relationship_potential(self, saju: SajuPalja) -> Dict:
        """인간관계 분석"""
        # 모든 천간 관계의 종합적 분석
        relationship_analysis = {
            "social_fortune": "평",
            "relationship_quality": "보통",
            "advice": []
        }
        
        # 전체 관계의 길흉 비율 계산
        all_stems = [saju.year_stem, saju.month_stem, saju.day_stem, saju.hour_stem]
        good_relations = 0
        bad_relations = 0
        
        for i, from_stem in enumerate(all_stems):
            for j, to_stem in enumerate(all_stems):
                if i != j:
                    relation = self.data_loader.get_tengan_relation(from_stem, to_stem)
                    if relation:
                        if relation.fortune in ["길", "대길"]:
                            good_relations += 1
                        elif relation.fortune in ["흉", "대흉"]:
                            bad_relations += 1
        
        if good_relations > bad_relations:
            relationship_analysis["social_fortune"] = "길"
            relationship_analysis["relationship_quality"] = "양호"
            relationship_analysis["advice"].append("원만한 대인관계가 가능합니다.")
        elif bad_relations > good_relations:
            relationship_analysis["social_fortune"] = "흉"
            relationship_analysis["relationship_quality"] = "주의"
            relationship_analysis["advice"].append("인간관계에서 신중함이 필요합니다.")
        
        return relationship_analysis