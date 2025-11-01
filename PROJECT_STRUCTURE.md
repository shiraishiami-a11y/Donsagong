# 📁 DONSAGONG Master 프로젝트 구조

## 🏗️ 디렉토리 구조

```
donsagong-master/
│
├── 📚 docs/                        # 핵심 문서
│   ├── DONSAGONG_MASTER_DATABASE.md    # 통합 마스터 DB v2.1
│   ├── DONSAGONG_ANALYSIS_SYSTEM_V2.md # 분석 프로세스
│   ├── DONSAGONG_QUALITY_CONTROL.md    # 품질 검증
│   ├── MANSERYEOK_GUIDE.md            # 만세력 가이드
│   └── README.md                       # 프로젝트 소개
│
├── 🎓 learning-materials/          # 학습 자료
│   ├── 대운/                      # 대운 관련 이미지
│   │   └── *.png (064-091)
│   ├── 용신/                      # 용신 관련 이미지
│   │   └── *.png (002-016)
│   └── 조후/                      # 조후 관련 이미지
│
├── 🔧 src/                         # 소스 코드
│   ├── manseryeok/                # 만세력 계산기
│   │   ├── calculator.py
│   │   └── api_daeun_calculator.py
│   └── validation/                # 검증 도구
│       └── saju_validator.py
│
└── 💾 backup/                      # 백업 데이터
    └── 20250907_210348/           # 이전 버전 백업

```

## 📝 파일 역할

### 핵심 데이터베이스
- **MASTER_DATABASE.md**: 모든 매트릭스와 해석 규칙 통합본
- **ANALYSIS_SYSTEM_V2.md**: 실제 분석 수행 순서
- **QUALITY_CONTROL.md**: AI 오염 방지 및 순수성 보장

### 학습 자료
- **PNG 파일들**: 원본 학습 자료 (절대 수정 금지)
- 새 자료 추가 시 해당 카테고리 폴더에 저장

### 도구
- **calculator.py**: 만세력 계산
- **saju_validator.py**: 데이터 검증

## 🔄 업데이트 프로세스

1. **새 학습 자료 입수**
   - `/learning-materials/` 적절한 폴더에 저장
   
2. **데이터베이스 업데이트**
   - `MASTER_DATABASE.md` 수정
   - 버전 번호 증가 (현재 v2.1)
   
3. **검증**
   - `QUALITY_CONTROL.md` 체크리스트 확인
   - 순수 돈사공 지식만 포함 확인
   
4. **백업**
   - 중요 변경 시 `/backup/` 폴더에 저장

## ⚠️ 주의사항

- **절대 금지**: 오행론, 십신론 등 전통 명리학 혼입
- **필수 준수**: 돈사공 고유 용어와 체계만 사용
- **품질 유지**: 모든 업데이트는 원본 학습자료 기반

## 🎯 프로젝트 목표

지속적으로 발전하는 **돈사공 지식 베이스** 구축
- 순수성 100% 유지
- AI 학습 최적화
- 체계적 데이터 관리