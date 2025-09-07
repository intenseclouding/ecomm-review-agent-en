# 제품 리뷰 자동화 시스템

Strands Agents를 활용한 AI 기반 제품 리뷰 분석 및 자동 댓글 생성 시스템입니다.

<img width="2282" height="1177" alt="image" src="https://github.com/user-attachments/assets/9d479cc5-8687-4faf-9b71-19b6076d799c" />

<img width="2292" height="1168" alt="image" src="https://github.com/user-attachments/assets/9eaa7bd9-91ec-4121-9a8f-459575e7406c" />

<img width="754" height="1152" alt="image" src="https://github.com/user-attachments/assets/00384f22-abe2-4738-91fe-efea5c15b753" />

<img width="931" height="1116" alt="image" src="https://github.com/user-attachments/assets/7903cdf2-b813-482a-ae2f-db5fc5e0017e" />



## 🎯 주요 기능

### 🤖 AI 기반 리뷰 분석
- 감정 분석 (긍정/부정/중립) 및 키워드 추출
- 스팸 탐지 및 주제별 분류
- 구조화된 데이터 저장 및 분석 상태 추적

### 🛡️ 리뷰 내용 검수 시스템
- 공격적/선정적/스팸성 내용 자동 탐지
- 점수 기반 판정 (승인/경고/거부)
- 상세 피드백 및 개선 제안 제공

### 💬 자동 댓글 생성
- 브랜드별 톤앤매너 반영
- 감정 기반 적절한 응답 생성
- 셀러 승인 시스템

### 📊 실시간 모니터링
- Agent 로그 시스템으로 처리 과정 투명화
- 성능 메트릭 및 통계 대시보드
- 아마존 스타일 UI 및 스마트 이미지 시스템

## 🎨 UI/UX 특징

### 아마존 스타일 네비게이션
- 카테고리별 제품 그룹화 (전자제품, 패션, 화장품)
- 현재 제품 자동 하이라이트 및 반응형 디자인
- 280px 고정 사이드바 (모바일 최적화)

### 스마트 이미지 시스템
- 실제 제품 이미지 우선 표시
- 로드 실패 시 자동 그라디언트 폴백
- 제품별 고유 이모지 (🎧, 👕, ✨, ⌚, 🧥)

### 개발 도구 크레딧
- 🎨 Amazon Nova Canvas (이미지 생성)
- 💻 Amazon Q Developer (코드 생성)
- 🔧 Kiro IDE (개발 환경)

## 🏗️ 시스템 구조

```
product-review-automation/
├── frontend/           # Next.js React 애플리케이션
├── backend/            # FastAPI 백엔드 서버
├── agents/             # Strands Agents (리뷰 분석, 자동 응답)
├── .kiro/              # Kiro IDE 설정 및 문서
└── data/               # 샘플 데이터 및 Agent 로그
```

## 🚀 빠른 시작

### 자동 실행 (권장)
```bash
chmod +x run_demo.sh
./run_demo.sh
```

### 수동 실행
```bash
# 1. 의존성 설치
python -m venv venv && source venv/bin/activate
pip install -r backend/requirements.txt -r agents/requirements.txt
cd frontend && npm install

# 2. 서버 실행
cd backend && uvicorn app.main:app --reload --port 8000 &
cd frontend && npm run dev
```

### 접속 URL
- 프론트엔드: http://localhost:3000
- 백엔드 API: http://localhost:8000/docs

### 검수 시스템 테스트
```bash
# 정상 리뷰: "이 제품 정말 좋아요!"
# 부적절한 리뷰: "완전 쓰레기네요"
# 스팸 리뷰: "www.example.com 연락처: 010-1234-5678"
```

## 🤖 Strands Agents 설정

### 필수 요구사항
```bash
pip install strands-agents strands-agents-tools
aws configure  # Bedrock 액세스용
```

### Agent 테스트
```bash
cd agents
python -m review_analyzer.agent          # 리뷰 분석
python -m auto_responder.agent           # 자동 응답
python -m review_analyzer.content_moderation  # 검수 시스템
```

### 사용 모델
- Claude 3.7 Sonnet (Amazon Bedrock)
- 정규식 기반 검수 시스템 (점수: 공격적 +30, 선정적 +25, 스팸 +20)

## 📝 사용 방법

1. **제품 탐색**: 아마존 스타일 사이드바로 카테고리별 제품 탐색
2. **리뷰 작성**: 제품 페이지에서 "리뷰 작성" → 내용 입력 → 등록
3. **AI 검수**: 자동 내용 검수 (공격적/선정적/스팸성 내용 차단)
4. **자동 분석**: 키워드 추출 및 감정 분석 수행
5. **댓글 생성**: 브랜드 맞춤 자동 댓글 생성
6. **로그 확인**: "Agent 로그확인하기" 버튼으로 처리 과정 투명화

## 🛠️ 커스터마이징

### 셀러 프롬프트 수정
`data/seller_prompts.json`에서 브랜드별 톤앤매너 설정

### 검수 시스템 수정
`agents/review_analyzer/content_moderation.py`에서 패턴 및 점수 기준 조정

### Kiro Steering 파일
`.kiro/steering/`에서 AI 에이전트 동작 가이드라인 수정

## 📊 데이터 모델

### Review 모델
- 기본 필드: id, user_name, rating, content, date
- 분석 필드: keywords, sentiment, analysis_completed
- 로그 연결: agent_log_id

### Agent 로그 모델
- 단계별 처리 시간 및 상태 추적
- 상세 정보 및 오류 메시지 기록

## 🔧 기술 스택

### Backend
- FastAPI + Uvicorn + Pydantic
- Strands Agents SDK + Claude 3.7 Sonnet
- 메모리 기반 캐싱 (TTL: 10분)

### Frontend  
- Next.js + React + TypeScript
- Tailwind CSS (아마존 스타일)
- 반응형 사이드바 레이아웃

### AI/ML
- 정규식 기반 검수 시스템
- 키워드 추출 및 감정 분석
- Agent 로그 시스템

## 🆘 문제 해결

### 일반적인 문제
- **Strands Agents 설치**: `pip install --upgrade strands-agents strands-agents-tools`
- **AWS Bedrock 권한**: IAM 역할 및 Claude 3.7 Sonnet 모델 액세스 확인
- **CORS 오류**: 백엔드(8000), 프론트엔드(3000) 포트 확인
- **이미지 표시**: `frontend/public/images/output/` 경로 및 자동 폴백 확인

### 샘플 제품
1. 무선 이어폰 (PROD-001) 🎧 - ₩89,000
2. 크롭 니트 (PROD-002) 👕 - ₩45,000  
3. 비타민 세럼 (PROD-003) ✨ - ₩32,000
4. 스마트 워치 (PROD-004) ⌚ - ₩125,000
5. 데님 자켓 (PROD-005) 🧥 - ₩68,000

## 📄 라이선스
MIT 라이선스
