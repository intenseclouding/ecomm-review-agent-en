# 제품 리뷰 자동화 시스템

Strands Agents를 활용한 AI 기반 제품 리뷰 분석 및 자동 댓글 생성 시스템입니다.

<img width="2282" height="1177" alt="image" src="https://github.com/user-attachments/assets/9d479cc5-8687-4faf-9b71-19b6076d799c" />

<img width="2292" height="1168" alt="image" src="https://github.com/user-attachments/assets/9eaa7bd9-91ec-4121-9a8f-459575e7406c" />

<img width="754" height="1152" alt="image" src="https://github.com/user-attachments/assets/00384f22-abe2-4738-91fe-efea5c15b753" />

<img width="931" height="1116" alt="image" src="https://github.com/user-attachments/assets/7903cdf2-b813-482a-ae2f-db5fc5e0017e" />



## 🎯 주요 기능

### 🤖 AI 기반 리뷰 분석
- **감정 분석**: 긍정/부정/중립 분류 및 신뢰도 점수 (Claude 3.7 Sonnet 기반)
- **키워드 추출**: 제품 품질, 배송, 가격, 디자인, 사용성 등 핵심 키워드 자동 추출 (최대 6개)
- **스팸 탐지**: 가짜/스팸 리뷰 자동 감지 및 필터링
- **주제 분류**: 품질, 배송, 가격, 디자인, 사용성, 서비스 등 6개 카테고리 자동 분류
- **구조화된 데이터**: 분석 결과를 JSON 형태로 저장하여 추후 활용 가능

### 🛡️ 리뷰 내용 검수 시스템
- **다층 필터링**: 공격적 언어(+30점), 선정적 내용(+25점), 스팸성 내용(+20점) 자동 탐지
- **정규식 기반 검수**: 욕설, 비속어, 광고성 링크, 연락처 정보 등 패턴 매칭
- **점수 기반 판정**: 0-49점(승인), 50-79점(경고), 80점 이상(거부)
- **상세 피드백**: 검수 실패 시 구체적인 문제점과 개선 제안 제공
- **즉시 차단**: 검수 실패 시 리뷰 저장하지 않고 에러 반환으로 사전 차단

### ✨ 사용자 경험 개선
- **간소화된 리뷰 작성**: 사용자명 입력 불필요, 자동 생성
- **직관적인 평점 선택**: 이모지와 함께 표시되는 드롭다운
- **실시간 상태 표시**: 등록 중 로딩 스피너 및 상태 메시지
- **상세한 오류 안내**: 검수 실패 시 구체적인 문제점과 개선 방안 제시

### 💬 자동 댓글 생성
- **브랜드 맞춤**: `data/seller_prompts.json`에서 제품별 톤앤매너 설정
- **감정 기반 응답**: 긍정/부정/중립 리뷰에 따른 적절한 응답 자동 생성
- **승인 시스템**: 셀러의 최종 승인 후 고객에게 표시 (승인/거부 버튼)
- **Strands Agent 기반**: Auto Responder Agent가 Claude 3.7 Sonnet으로 고품질 응답 생성

### 📊 실시간 모니터링 및 분석
- **Agent 로그 시스템**: 리뷰 분석 및 응답 생성의 모든 단계 기록 및 시각화
- **성능 메트릭**: 각 처리 단계별 소요 시간 측정 및 성공률 추적
- **통계 대시보드**: 총 리뷰 수, 긍정 리뷰 수, 분석 완료 수, 댓글 승인 수, 평균 평점 표시
- **실시간 상태 추적**: 분석 진행 상황 및 완료 상태 실시간 업데이트
- **투명한 처리 과정**: AgentLogModal을 통한 단계별 처리 내역 상세 확인

## 🎨 UI/UX 특징

### 아마존 스타일 네비게이션
- 카테고리별 제품 그룹화 (전자제품, 패션, 화장품)
- 현재 제품 자동 하이라이트 및 반응형 디자인
- 280px 고정 사이드바 (모바일 최적화)

### 스마트 이미지 시스템
- 실제 제품 이미지 우선 표시
- 로드 실패 시 자동 그라디언트 폴백
- 제품별 고유 이모지 (🎧, 👕, ✨, ⌚, 🧥)
- 고정 높이 컨테이너 (384px)로 일관된 레이아웃 유지

### 개발 도구 크레딧
- 🎨 Amazon Nova Canvas (이미지 생성)
- 💻 Amazon Q Developer (코드 생성)
- 🔧 Kiro IDE (개발 환경)

## 🏗️ 시스템 구조

```
product-review-automation/
├── frontend/                    # Next.js React 애플리케이션
│   ├── components/             # UI 컴포넌트 (ReviewList, ReviewForm, AgentLogModal 등)
│   ├── pages/                  # 페이지 라우팅 (메인, 제품 상세)
│   ├── types/                  # TypeScript 타입 정의
│   └── services/               # API 서비스 레이어
├── backend/                     # FastAPI 백엔드 서버
│   ├── app/api/               # REST API 엔드포인트 (products, reviews)
│   ├── app/models/            # 데이터 모델 (Product, Review)
│   └── app/services/          # 비즈니스 로직 (캐싱, 로그 관리)
├── agents/                      # Strands Agents 구현
│   ├── review_analyzer/       # 리뷰 분석 Agent (감정, 키워드, 검수)
│   └── auto_responder/        # 자동 응답 생성 Agent
├── .kiro/                      # Kiro IDE 설정 및 Steering 문서
│   ├── settings/              # MCP 서버 설정
│   └── steering/              # AI 가이드라인 문서
└── data/                       # 데이터 저장소
    ├── sample_products.json   # 샘플 제품 데이터
    ├── seller_prompts.json    # 브랜드별 프롬프트
    └── agent_logs/            # Agent 실행 로그
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
- **프론트엔드**: http://localhost:3000
- **백엔드 API**: http://localhost:8000/docs
- **주요 API 엔드포인트**:
  - `GET /api/products` - 전체 제품 목록 조회
  - `GET /api/products/{product_id}` - 특정 제품 상세 정보
  - `POST /api/products/{product_id}/reviews` - 리뷰 작성 (검수 및 분석 포함)
  - `GET /api/products/{product_id}/reviews` - 제품별 리뷰 목록
  - `POST /api/reviews/{review_id}/approve-response` - 자동 응답 승인
  - `DELETE /api/reviews/{review_id}/response` - 자동 응답 거부
  - `GET /api/reviews/{review_id}/agent-log` - Agent 처리 로그 조회
  - `GET /health` - 서버 상태 확인

### 검수 시스템 테스트
```bash
# 정상 리뷰: "이 제품 정말 좋아요!"
# 부적절한 리뷰: "완전 쓰레기네요"
# 스팸 리뷰: "www.example.com 연락처: 010-1234-5678"
```

### 리뷰 작성 폼 특징
- **간소화된 입력**: 사용자명 입력 불필요 (자동 생성)
- **평점 선택**: 1-5점 드롭다운 메뉴 (⭐ 이모지와 함께 표시)
- **리뷰 내용**: 최소 10자 이상 입력 필수, 플레이스홀더 가이드 제공
- **구매 확인**: 체크박스로 구매 확인 여부 선택 (기본값: 체크됨)
- **실시간 검수**: 등록 시 즉시 AI 검수 수행
- **상세 피드백**: 검수 실패 시 구체적인 문제점 및 개선 제안 제공
- **로딩 상태**: 등록 중 스피너 애니메이션 및 "등록 중..." 메시지
- **성공/실패 표시**: 컬러 코딩된 상태 메시지 (녹색: 성공, 빨간색: 실패)

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

### 사용 모델 및 기술
- **LLM**: Claude 3.7 Sonnet (`us.anthropic.claude-3-7-sonnet-20250219-v1:0`) via Amazon Bedrock
- **검수 시스템**: 정규식 기반 다층 필터링 (공격적 언어 +30점, 선정적 내용 +25점, 스팸 +20점)
- **Agent Framework**: Strands Agents SDK with tool-based architecture
- **분석 도구**: 감정 분석, 키워드 추출, 스팸 탐지, 주제 분류 도구

## 🏛️ 컴포넌트 아키텍처

### 핵심 컴포넌트
- **ReviewList.tsx**: 리뷰 목록 표시, 감정/키워드 시각화, 승인/거부 버튼
- **ReviewForm.tsx**: 간소화된 리뷰 작성 폼, 실시간 검수 및 상태 표시
- **AgentLogModal.tsx**: Agent 처리 과정 단계별 시각화 모달
- **SentimentIndicator.tsx**: 감정 분석 결과 시각적 표시 (이모지 + 신뢰도)
- **KeywordTags.tsx**: 추출된 키워드 태그 표시 및 클릭 이벤트
- **HighlightedText.tsx**: 리뷰 텍스트 내 키워드 하이라이팅

### 레이아웃 컴포넌트
- **Layout.tsx**: 전체 페이지 레이아웃 및 헤더
- **Sidebar.tsx**: 아마존 스타일 카테고리 네비게이션 (280px 고정)
- **ProductDetail.tsx**: 제품 상세 정보 및 리뷰 섹션 통합
  - 고정 높이 레이아웃 (384px)으로 공간 효율성 최적화
  - 주요 특징 표시 로직 (2열 그리드, 최대 4개 + 더보기 표시)으로 정보량 증대
  - AI 자동화 안내를 제품 정보 하단으로 재배치
  - **구매 기능 UI**: 구매하기/장바구니 버튼 및 배송 정보 표시
  - 컴팩트한 디자인으로 정보 밀도 최적화
  - 반응형 디자인 및 시각적 계층구조 개선
  - 텍스트 말줄임 처리로 긴 특징명 최적화

## 📝 사용 방법

### 1. 제품 탐색 및 구매
- 아마존 스타일 사이드바로 카테고리별 제품 탐색
- 현재 제품 자동 하이라이트 및 반응형 디자인
- **구매 기능**: 🛒 구매하기 / 🛍️ 장바구니 버튼 (데모용)
- **배송 정보**: 당일 주문 시 익일 배송, 무료배송 혜택 표시

### 2. 리뷰 작성 프로세스
1. **리뷰 작성 시작**: 
   - 리뷰가 없는 제품의 경우: 리뷰 목록 하단의 "리뷰 작성" 버튼 클릭
   - 리뷰가 있는 제품의 경우: 리뷰 목록 상단의 "리뷰 작성" 버튼 클릭
2. **평점 선택**: 1-5점 드롭다운 (⭐ 이모지 표시)
3. **리뷰 내용 입력**: 최소 10자 이상, 플레이스홀더 가이드 제공
4. **구매 확인**: 체크박스 선택 (기본값: 체크됨)
5. **등록**: 실시간 AI 검수 → 분석 → 자동 응답 생성

### 3. AI 처리 파이프라인
1. **검수 단계**: 공격적/선정적/스팸성 내용 자동 차단
2. **분석 단계**: 감정 분석, 키워드 추출, 주제 분류
3. **응답 생성**: 브랜드 맞춤 자동 댓글 생성
4. **승인 대기**: 셀러의 최종 승인 후 고객에게 표시

### 4. 모니터링 및 관리
- **실시간 상태**: 분석 진행 상황 및 완료 상태 표시
- **Agent 로그**: "Agent 로그확인하기" 버튼으로 처리 과정 투명화
- **승인 관리**: 자동 생성된 응답의 승인/거부 처리

## 🛠️ 커스터마이징 가이드

### 셀러 프롬프트 수정
```json
// data/seller_prompts.json
{
  "PROD-001": {
    "brand_name": "TechSound",
    "tone": "친근하고 전문적인",
    "key_messages": ["음질", "편의성", "가성비"]
  }
}
```

### 검수 시스템 조정
```python
# agents/review_analyzer/content_moderation.py
SCORING_WEIGHTS = {
    "aggressive": 30,    # 공격적 언어 점수
    "sexual": 25,        # 선정적 내용 점수  
    "spam": 20,          # 스팸성 내용 점수
    "quality": 15        # 품질 기준 점수
}
```

### AI Agent 가이드라인
- `.kiro/steering/review-analysis.md`: 리뷰 분석 기준 및 우선순위
- `.kiro/steering/tech.md`: 기술 스택 및 개발 표준
- `.kiro/steering/structure.md`: 프로젝트 구조 및 네이밍 규칙

## 📊 데이터 모델

### Review 모델 (완전한 리뷰 데이터)
```typescript
interface Review {
  // 기본 정보
  id: string;
  user_name: string;           // 자동 생성 (사용자XXXXXX)
  rating: number;              // 1-5점
  content: string;             // 리뷰 내용
  date: string;                // ISO 날짜
  verified_purchase: boolean;   // 구매 확인 여부
  
  // AI 분석 결과
  keywords?: string[];         // 추출된 키워드 (최대 6개)
  sentiment?: {                // 감정 분석 결과
    label: "긍정" | "부정" | "중립";
    confidence: number;        // 신뢰도 (0-1)
    polarity: number;          // 극성 (-1 ~ 1)
  };
  analysis_completed: boolean; // 분석 완료 여부
  analysis_timestamp?: string; // 분석 완료 시간
  
  // 자동 응답 관련
  auto_response?: string;      // AI 생성 응답
  response_approved?: boolean; // 응답 승인 여부
  seller_response?: {          // 기존 셀러 응답 (샘플 데이터)
    content: string;
    date: string;
  };
  
  // 로그 연결
  agent_log_id?: string;       // Agent 처리 로그 ID
}
```

### ReviewCreate 모델 (API 입력)
```typescript
interface ReviewCreate {
  rating: number;              // 필수: 1-5점
  content: string;             // 필수: 리뷰 내용 (최소 10자)
  user_name?: string;          // 선택: 미제공시 자동 생성
  verified_purchase?: boolean; // 선택: 기본값 true
}
```

### Agent 로그 모델
```typescript
interface AgentLog {
  review_id: string;           // 연결된 리뷰 ID
  steps: Array<{               // 처리 단계별 로그
    step_name: string;         // 단계명
    start_time: string;        // 시작 시간
    end_time: string;          // 종료 시간
    duration_ms: number;       // 소요 시간 (밀리초)
    status: "success" | "error"; // 처리 상태
    details: any;              // 상세 정보
  }>;
  total_duration_ms: number;   // 전체 처리 시간
  created_at: string;          // 로그 생성 시간
}
```

## 🔧 기술 스택

### Backend (Python)
- **FastAPI 0.104.0+**: 고성능 웹 프레임워크, 자동 API 문서 생성
- **Uvicorn**: ASGI 서버, 비동기 처리 지원
- **Pydantic 2.0+**: 데이터 검증 및 직렬화
- **Strands Agents SDK**: AI Agent 개발 프레임워크
- **메모리 캐싱**: SimpleCache (TTL: 10분)

### Frontend (TypeScript)
- **Next.js 14.0+**: React 기반 풀스택 프레임워크 (Pages Router)
- **React 18**: 함수형 컴포넌트 및 Hooks 패턴
- **TypeScript 5**: 강타입 언어로 타입 안전성 보장
- **Tailwind CSS 3.3+**: 유틸리티 기반 CSS, 아마존 스타일 디자인
- **Axios 1.6+**: HTTP 클라이언트 라이브러리

### AI/ML Stack
- **Claude 3.7 Sonnet**: Amazon Bedrock을 통한 LLM 접근
- **Strands Agents**: Tool 기반 확장 가능한 Agent 아키텍처
- **정규식 엔진**: 다층 필터링 검수 시스템
- **자연어 처리**: 감정 분석, 키워드 추출, 주제 분류

### Development Tools
- **Kiro IDE**: AI 기반 통합 개발 환경, MCP 지원
- **ESLint + Prettier**: 코드 품질 및 포맷팅
- **Git**: 버전 관리 및 협업

## 🆘 문제 해결

### 일반적인 문제
- **Strands Agents 설치**: `pip install --upgrade strands-agents strands-agents-tools`
- **AWS Bedrock 권한**: IAM 역할 및 Claude 3.7 Sonnet 모델 액세스 확인
- **CORS 오류**: 백엔드(8000), 프론트엔드(3000) 포트 확인
- **이미지 표시**: `frontend/public/images/output/` 경로 및 자동 폴백 확인
- **리뷰 작성 오류**: 
  - 내용이 비어있으면 클라이언트 측에서 경고 표시
  - 검수 실패 시 상세한 오류 메시지와 함께 리뷰 저장되지 않음
  - 사용자명은 자동 생성되므로 입력 불필요

### 샘플 제품
1. 무선 이어폰 (PROD-001) 🎧 - ₩89,000
2. 크롭 니트 (PROD-002) 👕 - ₩45,000  
3. 비타민 세럼 (PROD-003) ✨ - ₩32,000
4. 스마트 워치 (PROD-004) ⌚ - ₩125,000
5. 데님 자켓 (PROD-005) 🧥 - ₩68,000

## 🔄 최근 업데이트

### v1.7.0 - 제품 특징 표시 최적화
- **향상된 특징 레이아웃**:
  - 2열 그리드 레이아웃 적용으로 공간 효율성 극대화
  - 최대 4개 특징 표시로 정보량 증가 (기존 2개 → 4개)
  - 텍스트 말줄임(truncate) 적용으로 긴 특징명 처리 개선
- **개선된 시각적 요소**:
  - 불릿 포인트 크기 조정 (mr-2 → mr-1.5) 및 flex-shrink-0 적용
  - 더보기 표시를 중앙 정렬로 변경하여 시각적 균형 개선
  - 그리드 기반 레이아웃으로 일관된 정렬 유지
- **사용자 경험 향상**:
  - 더 많은 제품 특징을 한눈에 확인 가능
  - 컴팩트한 디자인 유지하면서 정보 밀도 향상
  - 반응형 디자인으로 다양한 화면 크기 지원

### v1.6.0 - 제품 상세 페이지 컴팩트 디자인 적용
- **공간 효율성 극대화**:
  - 텍스트 크기 최적화 (text-2xl, text-xl, text-sm, text-xs)로 더 많은 정보를 효과적으로 표시
  - 간격 조정 (mb-1, mb-2, mb-3)으로 컴팩트한 레이아웃 구현
  - 주요 특징을 2개로 제한하여 핵심 정보에 집중
- **향상된 시각적 밀도**:
  - 카테고리 태그 크기 축소 (px-2 py-1, text-xs)로 공간 절약
  - 가격 정보 및 평점 표시 영역 최적화
  - 구매 버튼 크기 조정 (px-4 py-2, text-sm)으로 균형 잡힌 배치
- **개선된 정보 계층구조**:
  - 배송 정보 텍스트 크기 축소 (text-xs)로 보조 정보 명확화
  - 특징 목록 스타일링 최적화 (space-y-0.5, w-1 h-1)
  - 전체적인 시각적 일관성 향상

### v1.5.0 - 전자상거래 UI 완성 및 구매 기능 추가
- **구매 기능 인터페이스 추가**:
  - 🛒 구매하기 버튼: 메인 구매 액션 (오렌지 그라디언트)
  - 🛍️ 장바구니 버튼: 보조 구매 액션 (그레이 그라디언트)
  - 데모용 알림 메시지로 기능 안내
- **배송 정보 표시**:
  - 🚚 당일 주문 시 익일 배송 안내
  - 무료배송 혜택 강조 표시
  - 회색 배경의 정보 박스로 시각적 구분
- **향상된 전자상거래 경험**:
  - 실제 쇼핑몰과 유사한 구매 플로우 제공
  - 호버 효과 및 애니메이션으로 인터랙션 개선
  - 반응형 버튼 레이아웃 (flex-1으로 균등 분할)

### v1.4.0 - 사용자 경험 최적화 및 UI 개선
- **리뷰 작성 플로우 개선**:
  - 리뷰 작성 버튼을 제품 상세 페이지에서 제거하여 UI 간소화
  - 리뷰가 없는 경우에만 ReviewList 컴포넌트에서 작성 버튼 표시
  - 더 직관적인 사용자 여정 제공
- **제품 정보 레이아웃 최적화**:
  - AI 자동화 안내 섹션을 제품 정보 하단으로 이동
  - 공간 효율성을 높여 핵심 정보에 집중
  - 시각적 계층구조 개선으로 정보 접근성 향상
- **사용자 인터페이스 개선**:
  - 불필요한 버튼 제거로 페이지 복잡도 감소
  - 컴팩트한 디자인으로 모바일 경험 향상
  - 일관된 정보 배치로 사용성 개선

### v1.3.0 - 제품 상세 페이지 UI 최적화
- **공간 효율성 개선**: 제품 정보 섹션의 레이아웃을 최적화하여 더 많은 정보를 효과적으로 표시
- **향상된 시각적 계층구조**:
  - 제품 이미지와 정보를 고정 높이(384px) 컨테이너로 균형 잡힌 배치
  - 주요 특징을 3개로 제한하고 "+N개 더 보기" 표시로 간결성 유지
  - 텍스트 크기와 간격 조정으로 가독성 향상
- **개선된 사용자 인터페이스**:
  - AI 자동화 안내 섹션을 더 컴팩트하게 재설계
  - 버튼과 정보 블록의 시각적 균형 개선
  - 반응형 디자인 최적화로 다양한 화면 크기 지원

### v1.2.0 - 리뷰 작성 UX 개선
- **간소화된 리뷰 폼**: 사용자명 입력 필드 제거, 자동 생성으로 변경
- **향상된 사용자 경험**: 
  - 평점 선택 시 이모지 표시로 직관성 향상
  - 리뷰 내용 입력 시 상세한 플레이스홀더 가이드 제공
  - 등록 중 로딩 상태 및 진행 상황 표시
- **개선된 오류 처리**:
  - 검수 실패 시 상세한 피드백 제공
  - 클라이언트 측 유효성 검사 강화
  - 컬러 코딩된 상태 메시지로 결과 명확화

### 기술적 변경사항
- **ProductDetail.tsx**: 제품 특징 표시 최적화 및 레이아웃 개선
  - 특징 표시를 2열 그리드 레이아웃으로 변경 (grid-cols-2)
  - 최대 표시 특징 수 증가 (2개 → 4개)로 정보량 향상
  - 텍스트 말줄임(truncate) 적용으로 긴 특징명 처리 개선
  - 불릿 포인트 간격 조정 (mr-2 → mr-1.5) 및 flex-shrink-0 적용
  - 더보기 표시를 col-span-2와 text-center로 중앙 정렬
  - 컴팩트 디자인 적용 및 공간 효율성 개선
  - 텍스트 크기 체계적 축소 (text-3xl→text-2xl, text-2xl→text-xl, text-base→text-sm, text-sm→text-xs)
  - 간격 최적화 (mb-4→mb-3, mb-3→mb-2, mb-2→mb-1, space-y-3→space-y-2)
  - 카테고리 태그 크기 축소 (px-3 py-1→px-2 py-1, text-sm→text-xs)
  - 구매 버튼 크기 조정 (px-6 py-3→px-4 py-2, text-sm 추가)
  - 배송 정보 텍스트 크기 축소 (text-sm→text-xs, mx-2→mx-1)
  - 전자상거래 UI 완성 및 구매 기능 추가
  - 구매하기/장바구니 버튼 추가 (그라디언트 스타일링)
  - 배송 정보 섹션 추가 (당일 주문 익일 배송, 무료배송)
  - 데모용 알림 메시지로 기능 안내
  - 호버 효과 및 transform 애니메이션 적용
  - 반응형 버튼 레이아웃 (flex-1으로 균등 분할)
  - 리뷰 작성 버튼 제거로 UI 간소화
  - AI 자동화 안내 섹션을 제품 정보 하단으로 재배치
  - 고정 높이 컨테이너 적용 (h-96)으로 일관된 레이아웃 유지
- **ReviewList.tsx**: 리뷰 작성 플로우 개선
  - 리뷰가 없는 경우에만 작성 버튼 표시
  - 더 직관적인 사용자 여정 제공
  - 구문 오류 수정 및 안정성 향상
- **ReviewForm.tsx**: `user_name` 필드 제거, 자동 생성 로직 적용
- **ReviewCreate 모델**: `user_name`을 Optional로 변경, 기본값 설정
- **백엔드 API**: 사용자명 미제공 시 자동 생성 로직 추가
- **Agent 통합**: 검수와 분석을 하나의 파이프라인으로 통합

## 📄 라이선스
MIT 라이선스
