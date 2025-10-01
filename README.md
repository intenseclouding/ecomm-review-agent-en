# 🛍️ E-commerce Review Analysis System

AI 에이전트 기반 이커머스 리뷰 분석 및 관리 시스템입니다. Strands 프레임워크와 Claude Sonnet을 활용하여 리뷰 검수, 키워드 추출, 감정 분석, 자동 응답 등의 기능을 제공하고, AgentCore를 통해 Agent 배포 및 운영까지 체험해봅니다.

## 📋 프로젝트 개요

이 프로젝트는 이커머스 플랫폼의 고객 리뷰를 AI로 자동 분석하고 관리하는 시스템입니다. 각 Lab은 독립적인 기능을 담당하며, 단계별로 더 복잡한 AI 에이전트 기능을 구현합니다.

### 🎯 주요 목표
- **리뷰 품질 관리**: 부적절한 리뷰 자동 검수
- **고객 인사이트 추출**: 키워드 및 감정 분석을 통한 제품 개선점 도출
- **고객 서비스 자동화**: AI 기반 자동 응답 시스템
- **통합 관리**: 모든 분석 기능의 오케스트레이션
- **클라우드 배포**: Amazon Bedrock AgentCore를 통한 프로덕션 배포

## 🏗️ 프로젝트 구조

```
📦 ecomm-review-agent/
├── 📁 lab01_review_sentiment_analyzer/ # 감정 분석 시스템
├── 📁 lab02_review_keyword_extractor/  # 키워드 추출 시스템
├── 📁 lab03_review_moderator/          # 리뷰 검수 시스템
├── 📁 lab04_review_auto_response/      # 자동 응답 시스템
├── 📁 lab05_orchestrator/              # 통합 오케스트레이터
├── 📁 images/                          # 테스트용 이미지
├── 📄 requirements.txt                 # 프로젝트 의존성
├── 📄 setup_venv.sh                    # 가상환경 설정 스크립트
└── 📄 README.md                        # 이 파일
```

## 🚀 Lab별 상세 설명

### Lab 01: Sentiment Analyzer (감정 분석 시스템) ✅
**완성도: 100%**

리뷰의 감정을 분석하여 긍정/부정/중립을 판별하는 시스템입니다.

**주요 기능:**
- 하이브리드 감정 분석 (LLM + 사전 기반)
- 한국어 슬랭/신조어 인식
- 신뢰도 점수 제공
- 분석 경로 추적 (llm/llm→dict/dict_fallback)

**실행 방법:**
```bash
cd lab01_review_sentiment_analyzer
streamlit run streamlit_app.py
```

**특징:**
- "존좋", "개좋다", "노답", "헬게이트" 등 한국어 인터넷 용어 지원
- LLM 불확실할 때 사전 기반 재분석 자동 실행
- 상세한 분석 근거 제공

**최근 개선사항:**
- Agent 로직 개선 및 최적화
- UI 업데이트로 사용성 향상

---

### Lab 02: Keyword Extractor (키워드 추출 시스템) ✅
**완성도: 100%**

리뷰에서 제품 특성 관련 키워드를 자동 추출하는 시스템입니다.

**주요 기능:**
- 제품 특성 키워드 추출 (음질, 배터리, 착용감 등)
- 키워드별 관련 리뷰 검색
- 데이터베이스 저장 및 관리
- 에이전트 디버깅 정보 제공

**실행 방법:**
```bash
cd lab02_review_keyword_extractor
streamlit run streamlit_app.py
```

**특징:**
- 최대 3개 핵심 키워드만 추출
- 감정 표현 제외 (객관적 특성만)
- 한국어 특화 키워드 사전

**최근 개선사항:**
- JSON 포맷에서 TXT 포맷으로 변경 (registered_keywords.json → registered_keywords.txt)
- 키워드 관리 간소화 및 가독성 향상

---

### Lab 03: Review Moderator (리뷰 검수 시스템) ✅
**완성도: 100%**

부적절한 리뷰를 자동으로 검수하는 시스템입니다.

**주요 기능:**
- 욕설/선정성 검사
- 이미지-텍스트 매칭 검증
- 별점-내용 일치성 분석
- 종합적인 PASS/FAIL 판정

**실행 방법:**
```bash
cd lab03_review_moderator
streamlit run streamlit_app.py
```

**사용 기술:**
- Strands Agent Framework
- Claude 3.7 Sonnet
- PIL 기반 이미지 분석
- SQLite 데이터베이스

**최근 개선사항:**
- PIL (Python Imaging Library) 기반 접근법으로 전환
- 단일 이미지 지원으로 개선
- 이미지 처리 성능 최적화

---

### Lab 04: Auto Response (자동 응답 시스템) ✅
**완성도: 80%**

고객 리뷰에 대한 AI 기반 자동 응답을 생성하는 시스템입니다.

**주요 기능:**
- 리뷰 감정에 따른 맞춤형 응답
- 브랜드 톤앤매너 반영
- 고객 만족도 향상 응답 생성
- 응답 품질 평가 시스템

**실행 방법:**
```bash
cd lab04_review_auto_response
streamlit run streamlit_app.py
```

**기술 스택:**
- Strands Agent + Claude 3.7
- 응답 템플릿 시스템
- 브랜드 가이드라인 준수

**최근 개선사항:**
- UI 간소화 및 불필요한 기능 제거
- 자동 응답 로직 개선

---

### Lab 05: Orchestrator (통합 오케스트레이터) ✅
**완성도: 90%**

모든 분석 기능을 통합하여 자동화된 워크플로우를 제공하는 시스템입니다.

**주요 기능:**
- 리뷰 입력 시 자동으로 모든 분석 실행
- 감정 분석 → 키워드 추출 → 검수 → 자동 응답 순차 실행
- 대시보드를 통한 통합 결과 시각화
- Sub-agent 기반 아키텍처

**실행 방법:**
```bash
cd lab05_orchestrator
streamlit run streamlit_app.py
```

**기술 스택:**
- Multi-Agent 오케스트레이션
- Sub-agent 패턴 (sentiment_analyzer, keyword_extractor, review_moderator, auto_responser)
- 데이터 파이프라인 관리
- 실시간 모니터링

**최근 개선사항:**
- Orchestrator 구조 개선
- Sub-agents 통합 및 최적화
- 종합 리뷰 분석 워크플로우 완성

## 🛠️ 설치 및 설정

### 1. 자동 설정 (권장)

```bash
# 가상환경 자동 생성 및 의존성 설치
./setup_venv.sh
```

### 2. 수동 설정

```bash
# Python 3.8+ 필요
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
```

### 3. 실행

각 Lab을 독립적으로 실행할 수 있습니다:

```bash
# Lab 01 실행 (감정 분석)
cd lab01_review_sentiment_analyzer && streamlit run streamlit_app.py

# Lab 02 실행 (키워드 추출)
cd lab02_review_keyword_extractor && streamlit run streamlit_app.py

# Lab 03 실행 (리뷰 검수)
cd lab03_review_moderator && streamlit run streamlit_app.py

# Lab 04 실행 (자동 응답)
cd lab04_review_auto_response && streamlit run streamlit_app.py

# Lab 05 실행 (오케스트레이터)
cd lab05_orchestrator && streamlit run streamlit_app.py
```

## 📊 테스트 데이터

각 시스템에는 다음과 같은 샘플 데이터가 포함되어 있습니다:

- **긍정 리뷰**: "이 제품 정말 좋아요! 음질도 훌륭하고 배터리도 오래 갑니다."
- **부정 리뷰**: "완전 쓰레기네요. 돈 아까워요."
- **이미지 포함 리뷰**: 꽃 사진, 이어폰 사진과 함께 제공
- **한국어 슬랭**: "존좋", "개좋다", "노답", "헬게이트" 등

## 🎯 현재 개발 상태

| Lab | 기능 | 상태 | 완성도 |
|-----|------|------|--------|
| Lab 01 | 감정 분석 | ✅ 완료 | 100% |
| Lab 02 | 키워드 추출 | ✅ 완료 | 100% |
| Lab 03 | 리뷰 검수 | ✅ 완료 | 100% |
| Lab 04 | 자동 응답 | ✅ 거의 완료 | 80% |
| Lab 05 | 오케스트레이터 | ✅ 거의 완료 | 90% |

## 📝 TODO & 로드맵

### 🔥 우선순위 높음
- [ ] **Lab 4 (Auto Response) 완성**
  - [x] 기본 자동 응답 로직 구현
  - [x] UI 간소화
  - [ ] 응답 품질 평가 메트릭 추가 (20%)

- [ ] **Lab 5 (Orchestrator) 완성**
  - [x] Multi-Agent 워크플로우 설계
  - [x] Sub-agents 통합 (sentiment_analyzer, keyword_extractor, review_moderator, auto_responser)
  - [x] 통합 대시보드 UI 개발
  - [ ] 배치 처리 시스템 구현 (10%)

### 🚀 프로덕션 배포
- [ ] **AWS Bedrock AgentCore 배포**
  - [ ] Bedrock AgentCore 통합 설계
  - [ ] 클라우드 아키텍처 구성
  - [ ] API Gateway & Lambda 설정
  - [ ] DynamoDB 스키마 설계

### ⚡ 성능 개선
- [ ] **비동기 멀티 리뷰 처리 시스템**
  - [ ] SQS 기반 큐 시스템 구현
  - [ ] 병렬 처리 최적화
  - [ ] 실시간 모니터링 대시보드
  - [ ] 처리량 스케일링 자동화

### 🔧 기술적 개선
- [x] 프로젝트 설정 파일 추가 (requirements.txt, setup_venv.sh)
- [ ] 에러 핸들링 및 복원력 강화
- [ ] 성능 모니터링 및 로깅 시스템
- [ ] 단위 테스트 및 통합 테스트 추가
- [ ] 데이터베이스 마이그레이션 시스템
- [ ] 보안 강화 (API 키 관리, 데이터 암호화)

## 🤝 기여 방법

1. Fork the repository
2. Create feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Create Pull Request

## 📚 참고 자료

- [Strands Framework Documentation](https://strands.ai)
- [Claude 3.7 Sonnet API](https://docs.anthropic.com)
- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock)
- [Streamlit Documentation](https://docs.streamlit.io)

## 📄 라이선스

MIT License - 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

---

**개발자**: YejinKM
**버전**: 2.0.0
**마지막 업데이트**: 2025년 10월

## 📌 최근 변경사항 (v2.0.0)

- Lab 01-05 전체 개선 및 최적화
- Lab 구조 재구성 (감정 분석 → 키워드 추출 → 검수 순서로 변경)
- 프로젝트 설정 자동화 (requirements.txt, setup_venv.sh 추가)
- Lab 04 자동 응답 시스템 구현 (80% 완성)
- Lab 05 오케스트레이터 Sub-agent 아키텍처 구현 (90% 완성)
- 키워드 관리 시스템 개선 (JSON → TXT)
- PIL 기반 이미지 처리로 전환

> 💡 **팁**: 각 Lab은 독립적으로 실행 가능하며, 전체 시스템의 이해를 위해 순차적으로 체험해보시는 것을 권장합니다.