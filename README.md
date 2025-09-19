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
├── 📁 lab01-review-moderator/          # 리뷰 검수 시스템
├── 📁 lab02-review-keyword-extractor/  # 키워드 추출 시스템
├── 📁 lab03-review-sentiment-analyzer/ # 감정 분석 시스템
├── 📁 lab04-review-auto-response/      # 자동 응답 시스템 (미완성)
├── 📁 lab05-orchestrator/              # 통합 오케스트레이터 (미완성)
├── 📁 lab06-bedrock-deployment/        # AWS Bedrock 배포 (예정)
├── 📁 images/                          # 테스트용 이미지
└── 📄 README.md                        # 이 파일
```

## 🚀 Lab별 상세 설명

### Lab 01: Review Moderator (리뷰 검수 시스템) ✅
**완성도: 100%**

부적절한 리뷰를 자동으로 검수하는 시스템입니다.

**주요 기능:**
- 욕설/선정성 검사
- 이미지-텍스트 매칭 검증
- 별점-내용 일치성 분석
- 종합적인 PASS/FAIL 판정

**실행 방법:**
```bash
cd lab01-review-moderator
streamlit run streamlit_app.py
```

**사용 기술:**
- Strands Agent Framework
- Claude 3.7 Sonnet
- 이미지 분석 (Base64 처리)
- SQLite 데이터베이스

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
cd lab02-review-keyword-extractor
streamlit run streamlit_app.py
```

**특징:**
- 최대 3개 핵심 키워드만 추출
- 감정 표현 제외 (객관적 특성만)
- 한국어 특화 키워드 사전

---

### Lab 03: Sentiment Analyzer (감정 분석 시스템) ✅
**완성도: 100%**

리뷰의 감정을 분석하여 긍정/부정/중립을 판별하는 시스템입니다.

**주요 기능:**
- 하이브리드 감정 분석 (LLM + 사전 기반)
- 한국어 슬랭/신조어 인식
- 신뢰도 점수 제공
- 분석 경로 추적 (llm/llm→dict/dict_fallback)

**실행 방법:**
```bash
cd lab03-review-sentiment-analyzer
streamlit run streamlit_app.py
```

**특징:**
- "존좋", "개좋다", "노답", "헬게이트" 등 한국어 인터넷 용어 지원
- LLM 불확실할 때 사전 기반 재분석 자동 실행
- 상세한 분석 근거 제공

---

### Lab 04: Auto Response (자동 응답 시스템) 🚧
**완성도: 0% (미완성)**

고객 리뷰에 대한 AI 기반 자동 응답을 생성하는 시스템입니다.

**예정 기능:**
- 리뷰 감정에 따른 맞춤형 응답
- 브랜드 톤앤매너 반영
- 고객 만족도 향상 응답 생성
- 응답 품질 평가 시스템

**기술 스택:**
- Strands Agent + Claude 3.7
- 응답 템플릿 시스템
- 브랜드 가이드라인 준수

---

### Lab 05: Orchestrator (통합 오케스트레이터) 🚧
**완성도: 0% (미완성)**

모든 분석 기능을 통합하여 자동화된 워크플로우를 제공하는 시스템입니다.

**예정 기능:**
- 리뷰 입력 시 자동으로 모든 분석 실행
- 검수 → 키워드 추출 → 감정 분석 → 자동 응답 순차 실행
- 대시보드를 통한 통합 결과 시각화
- 배치 처리 및 스케줄링

**기술 스택:**
- Multi-Agent 오케스트레이션
- 비동기 처리 (asyncio)
- 데이터 파이프라인 관리
- 실시간 모니터링

---

### Lab 06: Bedrock Deployment (AWS 배포) 🔮
**완성도: 0% (예정)**

Amazon Bedrock AgentCore를 통한 프로덕션 환경 배포입니다.

**예정 기능:**
- AWS Bedrock AgentCore 통합
- 클라우드 네이티브 아키텍처
- 오토 스케일링 및 로드 밸런싱
- 비동기 멀티 리뷰 처리
- API Gateway 및 Lambda 통합

**기술 스택:**
- Amazon Bedrock AgentCore
- AWS Lambda & API Gateway
- Amazon DynamoDB
- Amazon SQS (비동기 처리)
- CloudWatch 모니터링

## 🛠️ 설치 및 설정

### 1. 환경 준비

```bash
# Python 3.8+ 필요
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install streamlit pillow strands
```

### 2. 실행

각 Lab을 독립적으로 실행할 수 있습니다:

```bash
# Lab 01 실행
cd lab01-review-moderator && streamlit run streamlit_app.py

# Lab 02 실행
cd lab02-review-keyword-extractor && streamlit run streamlit_app.py

# Lab 03 실행
cd lab03-review-sentiment-analyzer && streamlit run streamlit_app.py
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
| Lab 01 | 리뷰 검수 | ✅ 완료 | 100% |
| Lab 02 | 키워드 추출 | ✅ 완료 | 100% |
| Lab 03 | 감정 분석 | ✅ 완료 | 100% |
| Lab 04 | 자동 응답 | 🚧 개발 중 | 0% |
| Lab 05 | 오케스트레이터 | 🚧 개발 중 | 0% |
| Lab 06 | AWS 배포 | 🔮 계획 중 | 0% |

## 📝 TODO & 로드맵

### 🔥 우선순위 높음
- [ ] **Lab 4 (Auto Response) 구현**
  - [ ] 감정별 응답 템플릿 설계
  - [ ] 브랜드 톤앤매너 반영 시스템
  - [ ] 응답 품질 평가 메트릭

- [ ] **Lab 5 (Orchestrator) 구현**
  - [ ] Multi-Agent 워크플로우 설계
  - [ ] 통합 대시보드 UI 개발
  - [ ] 배치 처리 시스템 구현

### 🚀 프로덕션 배포
- [ ] **Lab 6 (AWS Bedrock AgentCore 배포)**
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
**버전**: 1.0.0
**마지막 업데이트**: 2024년 9월

> 💡 **팁**: 각 Lab은 독립적으로 실행 가능하며, 전체 시스템의 이해를 위해 순차적으로 체험해보시는 것을 권장합니다.