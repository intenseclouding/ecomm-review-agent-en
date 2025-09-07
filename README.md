# 제품 리뷰 자동화 시스템

Strands Agents를 활용한 AI 기반 제품 리뷰 분석 및 자동 댓글 생성 시스템입니다.

## 🆕 최신 업데이트 (2025년 1월)

### 향상된 사용자 인터페이스 ✨

- **푸터 디자인 개선**: 그라디언트 배경과 개발 도구 크레딧 섹션 추가
- **개발 투명성**: Amazon Nova Canvas, Amazon Q Developer, Kiro IDE 사용 명시
- **반응형 크레딧 레이아웃**: 모바일과 데스크톱에 최적화된 attribution 표시

### 키워드 및 감정 분석 시스템 확장 ✨

- **Review 데이터 모델 확장**: keywords, sentiment, analysis_completed, analysis_timestamp 필드 추가
- **구조화된 감정 데이터**: 감정 라벨, 신뢰도, 극성 점수를 포함한 상세 분석 결과
- **키워드 추출**: 리뷰에서 핵심 키워드 자동 추출 및 저장 (최대 6개로 최적화)
- **분석 상태 추적**: 분석 완료 여부 및 타임스탬프 기록
- **향상된 UI 컴포넌트**: KeywordTags, SentimentIndicator, HighlightedText 컴포넌트 구현

### Agent 로그 시스템 구축 ✨

- **상세 로그 추적**: 자동 응답 생성 과정의 모든 단계 기록
- **성능 모니터링**: 각 처리 단계별 소요 시간 측정
- **투명성 향상**: "Agent 로그확인하기" 버튼으로 처리 과정 공개
- **샘플 데이터 지원**: 기존 리뷰들을 위한 가짜 로그 데이터 생성
- **실시간 로그 뷰어**: AgentLogModal 컴포넌트로 단계별 처리 과정 시각화

### API 확장 및 최적화 ✨

- **새로운 엔드포인트**: Agent 로그 조회 및 통계 API 추가
- **캐싱 시스템**: 메모리 기반 캐싱으로 API 응답 성능 향상 (10분 TTL)
- **오류 처리 강화**: 로그 기능 실패 시에도 안정적인 서비스 제공
- **캐시 관리**: 자동 만료, 통계 조회, 수동 무효화 기능
- **캐시 시스템 개선**: SimpleCache 클래스 생성자 매개변수 수정 (`default_ttl` 사용)

## 🎯 주요 기능

### 1. 리뷰 자동 분석 ✨ (신규 업데이트)

- **감정 분석**: 긍정/부정/중립 감정 자동 분류 및 신뢰도 점수
- **키워드 추출**: 핵심 키워드 자동 추출 및 태그 표시 (최대 6개로 최적화)
- **스팸 탐지**: 가짜/스팸 리뷰 자동 감지
- **주제 분류**: 품질, 배송, 가격, 디자인 등 주제별 분류
- **분석 데이터 저장**: 키워드, 감정, 분석 완료 상태 및 타임스탬프 기록
- **구조화된 저장**: `analyze_review_for_storage()` 함수로 데이터베이스 직접 저장 지원 ✨
- **향상된 오류 처리**: 분석 실패 시에도 기본값으로 안전한 데이터 저장 보장 ✨

### 2. 리뷰 내용 검수 시스템 ✨ (신규 업데이트)

- **사전 검수**: 리뷰 작성 시 즉시 내용 검수 수행
- **공격적 언어 탐지**: 욕설, 비속어, 공격적 표현, 차별적 언어, 협박성 표현 자동 감지
- **선정적 내용 차단**: 부적절한 성적 표현 및 내용 필터링
- **스팸 방지**: 광고성 링크, 연락처, 홍보성 내용, 금융 스팸 차단
- **품질 기준**: 과도한 반복문자, 특수문자, 길이, 대문자 사용 검증
- **점수 기반 판정**: 심각도 점수(0-100)로 승인/경고/거부 자동 결정
- **상세 피드백**: 검수 실패 시 구체적인 문제점과 개선 제안 제공
- **즉시 차단**: 검수 실패 시 리뷰 저장하지 않고 에러 반환

### 3. 자동 댓글 생성

- **셀러 맞춤**: 브랜드별 톤앤매너 반영
- **감정 대응**: 리뷰 감정에 적절한 응답 생성
- **품질 검증**: 생성된 댓글의 적절성 자동 검증
- **승인 시스템**: 셀러의 최종 승인 후 게시

### 4. 실시간 처리 및 로깅

- **단계별 처리**: 검수 → 분석 → 자동 응답 생성 순차 처리
- **즉시 피드백**: 검수 실패 시 즉시 에러 메시지 표시
- **실시간 알림**: 분석 및 댓글 생성 상태 실시간 업데이트
- **Agent 로그 추적**: 각 처리 단계별 상세 로그 기록 및 확인 기능

## 🎨 UI/UX 개선사항

### 아마존 스타일 사이드바 네비게이션 (신규 추가)

- **Layout 컴포넌트**: 전체 페이지 레이아웃을 관리하는 컨테이너

  - 사이드바와 메인 콘텐츠 영역을 반응형으로 배치
  - 현재 제품 ID를 자동 감지하여 사이드바에 전달
  - 수동 제품 ID 전달도 지원하여 유연성 확보

- **Sidebar 컴포넌트**: 아마존과 유사한 제품 네비게이션

  - 고정 너비 280px (데스크톱), 반응형 축소 (태블릿 240px, 모바일 256px)
  - 제품을 카테고리별로 자동 그룹화 (전자제품, 패션, 화장품)
  - 카테고리 접기/펼치기 기능으로 공간 효율성 향상
  - 현재 보고 있는 제품 자동 하이라이트 표시

- **CategorySection 컴포넌트**: 카테고리별 제품 목록 관리

  - 아마존 스타일의 카테고리 헤더 디자인
  - 제품 개수 표시로 정보 제공 향상
  - 부드러운 접기/펼치기 애니메이션 (300ms transition)
  - 빈 카테고리 자동 숨김 처리

- **ProductItem 컴포넌트**: 개별 제품 항목 표시

  - 제품별 고유 이모지와 가격 정보 표시
  - 활성 상태 시 오렌지 하이라이트 (아마존 스타일)
  - 호버 효과와 부드러운 트랜지션
  - 제품명 말줄임 처리로 일관된 레이아웃 유지

- **useCurrentProduct 훅**: 현재 제품 자동 감지

  - URL 라우터를 통한 제품 ID 자동 추출
  - 페이지 변경 시 실시간 업데이트
  - 오류 처리로 안정성 확보

- **아마존 스타일 디자인 시스템**:
  - CSS 변수로 아마존 색상 팔레트 구현 (#ff9900, #232f3e, #b12704 등)
  - 아마존과 동일한 폰트 크기, 간격, 호버 효과
  - 반응형 사이드바 너비 조정
  - 커스텀 스크롤바 스타일링

### 메인 페이지 디자인 업데이트

- **스마트 이미지 시스템**: 실제 제품 이미지 우선 표시, 로드 실패 시 자동으로 그라디언트 배경으로 전환
- **이모지 기반 제품 표시**: 각 제품별 고유 이모지로 직관적 식별 (🎧, 👕, ✨, ⌚, 🧥)
- **그라디언트 카드 디자인**: 제품별 맞춤 그라디언트 배경으로 시각적 매력 향상
- **카테고리 아이콘 시스템**: 전자제품(📱), 패션(👕), 화장품(💄) 등 직관적 분류
- **AI 자동화 배지**: 각 제품에 "🤖 AI 자동화" 배지로 기능 강조
- **반응형 그리드 레이아웃**: 모바일, 태블릿, 데스크톱 모든 화면에 최적화
- **호버 애니메이션**: 카드에 마우스 오버 시 그림자 효과로 상호작용 향상
- **향상된 푸터 디자인**: 그라디언트 배경과 개발 도구 크레딧 섹션 추가 ✨

### 제품 상세 페이지 디자인 업데이트

- **일관된 시각적 아이덴티티**: 메인 페이지와 동일한 이모지 및 그라디언트 시스템 적용
- **향상된 제품 이미지 영역**:
  - 제품별 맞춤 그라디언트 배경 (blue-purple, pink-rose, yellow-orange, gray, indigo-blue)
  - 대형 이모지 (9xl 크기)로 제품 특성 강조
  - 펄스 애니메이션과 드롭 섀도우 효과로 시각적 임팩트 증대
- **장식적 UI 요소**:
  - 반투명 원형 요소들로 배경 장식
  - 바운스 애니메이션으로 생동감 추가
  - 백드롭 블러 효과가 적용된 카테고리 라벨
- **개선된 카드 디자인**:
  - 둥근 모서리 (rounded-xl) 적용
  - 향상된 그림자 효과 (shadow-xl)
  - 테두리 추가로 깔끔한 구분
- **반응형 레이아웃**: 데스크톱과 모바일에서 최적화된 2열 그리드

### 제품 카드 구성 요소

- **제품별 고유 이모지**: 🎧(이어폰), 👕(니트), ✨(세럼), ⌚(워치), 🧥(자켓)
- **맞춤 그라디언트**: blue-purple, pink-rose, yellow-orange, gray, indigo-blue
- **간결한 설명**: 각 제품의 핵심 특징을 한 줄로 요약
- **가격 정보**: 원화 표시로 명확한 가격 정보 제공

### 사용자 경험 개선

- **시각적 계층구조**: 명확한 정보 구조로 사용성 향상
- **일관된 색상 시스템**: 브랜드 아이덴티티를 반영한 컬러 팔레트
- **타이포그래피**: 가독성 높은 폰트 크기와 간격
- **접근성**: 색상 대비와 키보드 네비게이션 고려
- **스마트 이미지 처리**: 실제 제품 이미지와 이모지 기반 폴백 시스템으로 최적의 로딩 경험
- **애니메이션 효과**: 펄스, 바운스 등 CSS 애니메이션으로 생동감 있는 인터페이스
- **시각적 피드백**: 호버 상태, 로딩 상태 등 명확한 상호작용 피드백
- **오류 처리**: 이미지 로드 실패 시 자동 폴백으로 끊김 없는 사용자 경험

### 향상된 푸터 섹션 ✨ (신규 추가)

- **그라디언트 배경**: `from-gray-50 to-blue-50` 그라디언트로 시각적 깊이감 추가
- **개발 도구 크레딧**: 프로젝트에 사용된 AI 도구들에 대한 명확한 attribution
  - 🎨 **Amazon Nova Canvas**: 모든 제품 이미지 AI 생성 도구
  - 💻 **Amazon Q Developer**: 코드 생성 및 개발 지원 AI
  - 🔧 **Kiro IDE**: AI 기반 통합 개발 환경
- **반응형 레이아웃**: 모바일에서는 세로 배치, 데스크톱에서는 가로 배치
- **시각적 구분**: 구분선과 아이콘을 활용한 명확한 정보 계층
- **브랜드 일관성**: Strands Agents 브랜딩과 조화로운 디자인

## 🧭 아마존 스타일 사이드바 네비게이션

### 주요 특징

- **일관된 네비게이션**: 모든 페이지에서 동일한 사이드바 제공
- **자동 제품 감지**: URL 기반으로 현재 제품 자동 하이라이트
- **카테고리 그룹화**: 전자제품, 패션, 화장품으로 자동 분류
- **접기/펼치기**: 카테고리별 토글로 효율적인 공간 활용
- **반응형 디자인**: 화면 크기에 따른 자동 너비 조정

### 컴포넌트 구조

```
Layout
├── Sidebar
│   ├── CategorySection (전자제품)
│   │   ├── ProductItem (무선 이어폰)
│   │   └── ProductItem (스마트 워치)
│   ├── CategorySection (패션)
│   │   ├── ProductItem (크롭 니트)
│   │   └── ProductItem (데님 자켓)
│   └── CategorySection (화장품)
│       └── ProductItem (비타민 세럼)
└── MainContent
```

### 기술적 구현

- **useCurrentProduct 훅**: Next.js 라우터를 통한 제품 ID 자동 감지
- **productUtils**: 제품 데이터 변환 및 카테고리 그룹화 로직
- **CSS 변수**: 아마존 색상 팔레트 및 스타일 시스템
- **TypeScript 타입**: 강타입 제품 및 카테고리 데이터 구조

### 사용자 경험

- **빠른 네비게이션**: 사이드바에서 원클릭으로 제품 간 이동
- **시각적 피드백**: 현재 제품 오렌지 하이라이트로 위치 인식
- **효율적 탐색**: 카테고리별 그룹화로 원하는 제품 빠른 찾기
- **반응형 지원**: 모바일에서도 최적화된 사이드바 경험

## 🖼️ 스마트 이미지 시스템

### 이미지 처리 방식

시스템은 제품 이미지를 다음과 같이 처리합니다:

1. **우선 순위**: 실제 제품 이미지 (`/images/output/{product-id}.png`)
2. **자동 폴백**: 이미지 로드 실패 시 그라디언트 배경 + 이모지로 자동 전환
3. **일관된 디자인**: 폴백 시에도 제품별 고유 색상과 이모지 유지

### 이미지 파일 구조

```
frontend/public/images/output/
├── 1.png              # PROD-001 (무선 이어폰)
├── 2.png              # PROD-002 (크롭 니트)
├── 3.png              # PROD-003 (비타민 세럼)
├── 4.png              # PROD-004 (스마트 워치)
└── 5.png              # PROD-005 (데님 자켓)
```

### 폴백 시스템 특징

- **즉시 전환**: 이미지 로드 실패 시 JavaScript로 즉시 그라디언트 배경 표시
- **시각적 일관성**: 제품별 고유 색상 그라디언트와 이모지 유지
- **성능 최적화**: 이미지 로드 실패 시에도 빠른 렌더링
- **사용자 경험**: 끊김 없는 시각적 경험 제공

## 🏗️ 시스템 구조

```
product-review-automation/
├── frontend/           # React/Next.js 프론트엔드
│   ├── components/     # React 컴포넌트들
│   │   ├── Layout.tsx           # 전체 레이아웃 (사이드바 + 메인)
│   │   ├── Sidebar.tsx          # 아마존 스타일 사이드바
│   │   ├── CategorySection.tsx  # 카테고리별 제품 그룹
│   │   ├── ProductItem.tsx      # 개별 제품 항목
│   │   ├── ProductDetail.tsx    # 제품 상세 페이지
│   │   ├── ReviewList.tsx       # 리뷰 목록 (키워드/감정 표시)
│   │   ├── ReviewForm.tsx       # 리뷰 작성 폼
│   │   ├── ReviewAnalytics.tsx  # 리뷰 분석 통계 대시보드 ✨
│   │   ├── KeywordTags.tsx      # 키워드 태그 컴포넌트 ✨
│   │   ├── SentimentIndicator.tsx # 감정 표시 컴포넌트 ✨
│   │   ├── HighlightedText.tsx  # 키워드 하이라이팅 컴포넌트 ✨
│   │   ├── AgentLogButton.tsx   # Agent 로그 확인 버튼 ✨
│   │   └── AgentLogModal.tsx    # Agent 로그 뷰어 모달 ✨
│   ├── hooks/          # React 커스텀 훅
│   │   └── useCurrentProduct.ts # 현재 제품 ID 자동 감지
│   ├── types/          # TypeScript 타입 정의
│   │   └── product.ts           # 제품 관련 타입들 (분석 데이터 포함)
│   ├── utils/          # 유틸리티 함수들
│   │   └── productUtils.ts      # 제품 데이터 처리 함수들
│   ├── styles/         # CSS 스타일
│   │   └── globals.css          # 아마존 스타일 CSS 변수 및 클래스
│   └── public/images/output/    # 제품 이미지 파일들
├── backend/           # FastAPI 백엔드
│   ├── app/models/product.py    # 데이터 모델 (키워드/감정 분석 필드 추가) ✨
│   ├── app/api/reviews.py       # 리뷰 API (로그 조회 엔드포인트 추가) ✨
│   └── app/services/            # 백엔드 서비스들
│       ├── agent_log_service.py     # Agent 로그 관리 서비스 ✨
│       ├── log_collector.py         # 실시간 로그 수집기 ✨
│       ├── sample_log_generator.py  # 샘플 로그 데이터 생성기 ✨
│       ├── api_cache.py             # API 응답 캐싱 시스템 ✨
│       ├── log_utils.py             # 로그 유틸리티 함수들 ✨
│       └── init_sample_logs.py      # 샘플 로그 초기화 ✨
├── agents/            # Strands Agents
│   ├── review_analyzer/    # 리뷰 분석 에이전트 (키워드/감정 분석)
│   │   ├── agent.py        # 분석 에이전트 메인 로직
│   │   ├── tools.py        # 분석 도구들
│   │   └── content_moderation.py  # 리뷰 내용 검수 및 모더레이션 시스템 ✨
│   └── auto_responder/     # 자동 댓글 생성 에이전트
│       ├── agent.py        # 응답 생성 에이전트 메인 로직
│       └── tools.py        # 응답 생성 도구들
├── .kiro/steering/    # Kiro Steering 파일들
│   ├── auto-response.md    # 자동 댓글 작성 가이드라인
│   ├── port-management.md  # 포트 관리 가이드라인
│   ├── review-analysis.md  # 리뷰 분석 가이드라인
│   └── seller-prompts.md   # 셀러 프롬프트 관리 가이드라인
├── .kiro/specs/       # 기능 명세서들 ✨
│   ├── product-sidebar-menu/           # 아마존 스타일 사이드바 명세
│   ├── review-keyword-sentiment-analysis/  # 키워드/감정 분석 명세
│   └── agent-log-viewer/                   # Agent 로그 뷰어 명세
└── data/             # 샘플 데이터
    ├── agent_logs/   # Agent 로그 데이터 저장소 ✨
    ├── sample_products.json  # 샘플 제품 데이터
    └── seller_prompts.json   # 셀러 프롬프트 데이터
```

## 🚀 빠른 시작

### 1. 환경 설정

```bash
# 프로젝트 클론
git clone <repository-url>
cd product-review-automation

# Python 가상환경 생성 (권장)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 백엔드 의존성 설치
cd backend
pip install -r requirements.txt

# Agents 의존성 설치
cd ../agents
pip install -r requirements.txt

# 프론트엔드 의존성 설치
cd ../frontend
npm install
```

## 🏛️ 아키텍처 패턴

### 컴포넌트 기반 아키텍처

- **Layout 패턴**: 전체 페이지 레이아웃을 관리하는 컨테이너 컴포넌트
- **Composition 패턴**: Sidebar + MainContent 조합으로 유연한 레이아웃
- **Container/Presenter 패턴**: 로직과 UI 분리로 재사용성 향상

### 상태 관리 패턴

- **Custom Hooks**: useCurrentProduct로 제품 상태 자동 관리
- **Props Drilling 최소화**: Layout에서 currentProductId 중앙 관리
- **Local State**: 각 컴포넌트별 독립적인 상태 관리

### 데이터 처리 패턴

- **Utility Functions**: productUtils로 데이터 변환 로직 분리
- **Type Safety**: TypeScript 인터페이스로 데이터 구조 보장
- **Automatic Grouping**: 카테고리별 자동 그룹화 로직

### CSS 아키텍처

- **CSS Variables**: 아마존 색상 팔레트 중앙 관리
- **Component Classes**: 재사용 가능한 CSS 클래스 정의
- **Responsive Design**: Tailwind CSS 기반 반응형 구현

### 2. 자동 실행 스크립트 사용 (권장)

```bash
# 프로젝트 루트에서 실행
chmod +x run_demo.sh
./run_demo.sh
```

이 스크립트는 자동으로:

- 필수 도구 확인 (Python, Node.js, npm)
- 가상환경 생성 및 활성화
- 모든 의존성 설치
- 백엔드 및 프론트엔드 서버 동시 실행

### 3. 수동 서버 실행

**백엔드 서버:**

```bash
cd backend
python -m app.main
# 또는
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**프론트엔드 서버:**

```bash
cd frontend
npm run dev
```

- 백엔드: http://localhost:8000
- 프론트엔드: http://localhost:3000
- API 문서: http://localhost:8000/docs

### 4. 데모 확인

브라우저에서 다음 URL로 접속:

- **메인 페이지**: http://localhost:3000 (개선된 UI 디자인 및 향상된 푸터)
- **무선 이어폰**: http://localhost:3000/product/PROD-001
- **크롭 니트**: http://localhost:3000/product/PROD-002
- **비타민 세럼**: http://localhost:3000/product/PROD-003
- **스마트 워치**: http://localhost:3000/product/PROD-004
- **데님 자켓**: http://localhost:3000/product/PROD-005
- **API 문서**: http://localhost:8000/docs

### 5. 검수 시스템 테스트 ✨

리뷰 작성 시 다음과 같은 내용으로 검수 시스템을 테스트해볼 수 있습니다:

**정상 리뷰 (승인):**
```
이 제품 정말 좋아요! 품질도 만족스럽고 배송도 빨라서 만족합니다.
```

**부적절한 리뷰 (거부):**
```
이 제품 완전 쓰레기네요. 돈 아까워 죽겠어요.
```

**스팸성 리뷰 (거부):**
```
www.example.com에서 더 싸게 팔아요! 연락처: 010-1234-5678
```

**품질 문제 리뷰 (거부):**
```
ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ
```

## 🤖 Strands Agents 설정

### 필수 요구사항

1. **Strands Agents SDK 설치**

   ```bash
   pip install strands-agents strands-agents-tools
   ```

2. **AWS Bedrock 설정 (필요시)**

   ```bash
   # AWS CLI 설정
   aws configure

   # Bedrock 모델 액세스 권한 확인
   # https://docs.aws.amazon.com/bedrock/latest/userguide/model-access-modify.html
   ```

3. **MCP (Model Context Protocol) 설정**
   - Kiro IDE에서 MCP 서버 설정이 자동으로 구성됩니다
   - `.kiro/settings/mcp.json`에서 설정 확인 가능

### 에이전트 테스트

```bash
cd agents

# 리뷰 분석 에이전트 테스트
python -m review_analyzer.agent

# 자동 댓글 생성 에이전트 테스트
python -m auto_responder.agent

# 리뷰 검수 시스템 테스트 ✨
python -m review_analyzer.content_moderation
```

### 새로운 분석 함수 ✨

리뷰 분석 에이전트에 데이터베이스 저장용 구조화된 분석 함수가 추가되었습니다:

- **`analyze_review_for_storage()`**: Review 모델에 직접 저장할 수 있는 구조화된 분석 결과 반환
- **향상된 오류 처리**: 분석 실패 시에도 기본값으로 안전한 저장 보장
- **키워드 제한**: 최대 6개 키워드로 제한하여 UI 표시 최적화
- **구조화된 감정 데이터**: label, confidence, polarity를 포함한 상세 감정 분석

### 리뷰 검수 도구 ✨ (신규 추가)

리뷰 분석 에이전트에 강력한 내용 검수 도구가 추가되었습니다:

#### `moderate_review_content(review_text: str)`
- **다층 필터링**: 공격적/선정적/스팸성 내용 자동 탐지
- **정교한 패턴 매칭**: 정규식 기반 다중 패턴 검사
- **점수 기반 판정**: 심각도 점수 계산 및 자동 결정
- **상세 피드백**: 구체적인 문제점과 개선 제안

#### `get_moderation_statistics(reviews: List[str])`
- **일괄 검수**: 여러 리뷰 동시 검수 및 통계 생성
- **승인율 계산**: 전체 리뷰 대비 승인/거부/경고 비율
- **문제 패턴 분석**: 가장 흔한 문제 유형 식별

#### 검수 기준
- **공격적 언어**: +30점 (욕설, 비속어, 차별적 표현, 협박)
- **선정적 내용**: +25점 (성적 표현, 부적절한 내용)
- **스팸성 내용**: +20점 (URL, 연락처, 광고, 금융 스팸)
- **품질 문제**: +10-20점 (길이, 반복문자, 특수문자)
- **판정 기준**: 25점 이상 거부, 15점 이상 경고, 10점 이상 주의

### 사용 모델

- **Claude 3.7 Sonnet**: `us.anthropic.claude-3-7-sonnet-20250219-v1:0`
- Amazon Bedrock을 통해 접근

## 📝 사용 방법

### 1. 아마존 스타일 네비게이션 사용

- **사이드바 네비게이션**: 모든 페이지에서 일관된 제품 탐색 경험
  - 카테고리별 제품 그룹화 (전자제품, 패션, 화장품)
  - 현재 보고 있는 제품 자동 하이라이트
  - 카테고리 접기/펼치기로 효율적인 공간 활용
  - 제품별 이모지와 가격 정보 한눈에 확인

### 2. 메인 페이지 탐색

- 개선된 UI로 5개의 샘플 제품 확인
- **스마트 이미지 표시**: 실제 제품 이미지 또는 자동 폴백 그라디언트
- 제품별 고유 이모지(🎧, 👕, ✨, ⌚, 🧥)로 직관적 식별
- 카테고리별 아이콘 시스템으로 빠른 분류 인식
- AI 자동화 배지로 기능 강조
- 제품별 맞춤 그라디언트 카드로 시각적 매력 향상

### 3. 제품 페이지 접속

- 원하는 제품 카드 클릭하여 상세 페이지 이동
- **향상된 제품 상세 디자인**:
  - 메인 페이지와 일관된 이모지 및 그라디언트 시스템
  - 대형 애니메이션 이모지로 제품 특성 강조
  - 장식적 UI 요소와 백드롭 블러 효과
- 제품 정보, 기존 리뷰, AI 처리 현황 확인

### 4. 리뷰 작성

- "리뷰 작성" 버튼 클릭
- 이름, 평점, 리뷰 내용 입력
- "리뷰 등록" 버튼 클릭

### 5. AI 검수 및 자동 처리 확인 ✨ (업데이트)

- **1단계 - 내용 검수**: 리뷰 작성 즉시 부적절한 내용 검사
  - 공격적 언어 패턴 매칭 (욕설, 비속어, 차별적 표현, 협박)
  - 선정적 내용 필터링 (성적 표현, 부적절한 내용)
  - 스팸 탐지 (URL, 연락처, 광고성 내용, 금융 스팸)
  - 품질 검증 (길이, 반복문자, 특수문자, 대문자 사용)
  - 심각도 점수 계산 및 자동 판정 (승인/경고/거부)
- **검수 실패 시**: 리뷰 저장하지 않고 상세한 에러 메시지 표시
  - 구체적인 문제점 명시 (예: "공격적 언어 감지: 쓰레기")
  - 심각도 점수 및 개선 제안 제공
- **검수 통과 시**: 자동으로 Strands Agent가 분석 시작
- **키워드 추출 및 감정 분석**: 리뷰 내용에서 핵심 키워드와 감정 자동 분석
- 분석 완료 후 자동 댓글이 생성됨
- 생성된 댓글을 승인/거부할 수 있음

### 6. Agent 로그 확인 ✨ (신규 기능)

- **"Agent 로그확인하기" 버튼**: 각 자동 응답 옆에 표시
- **단계별 처리 과정**: 셀러 프롬프트 로드 → 리뷰 분석 → 응답 생성 → 검증 → 최종 결정
- **소요 시간 추적**: 각 단계별 처리 시간 및 전체 소요 시간 확인
- **상세 로그 정보**: 사용된 프롬프트, 분석 결과, 검증 점수 등 상세 정보

### 7. 결과 확인

- 승인된 댓글은 리뷰 하단에 표시
- **키워드 태그**: 추출된 키워드를 태그 형태로 표시 (구현 예정)
- **감정 표시기**: 감정 분석 결과를 색상과 이모지로 표시 (구현 예정)
- 리뷰 통계에서 AI 처리 현황 확인
- 실시간 통계로 시스템 효과 측정

## 🛠️ 커스터마이징

### 셀러 프롬프트 수정

`data/seller_prompts.json` 파일에서 셀러별 브랜드 톤앤매너와 응답 템플릿을 수정할 수 있습니다.

```json
{
  "SELLER-ID": {
    "brand_name": "브랜드명",
    "brand_personality": "브랜드 성격",
    "positive_response_templates": ["긍정적 리뷰 응답 템플릿들..."],
    "negative_response_templates": ["부정적 리뷰 응답 템플릿들..."]
  }
}
```

### 검수 시스템 커스터마이징 ✨

`agents/review_analyzer/content_moderation.py` 파일에서 검수 규칙을 수정할 수 있습니다:

#### 패턴 추가/수정

```python
# 공격적 언어 패턴 추가
AGGRESSIVE_PATTERNS = [
    r'(새로운패턴|추가패턴)',  # 새 패턴 추가
    # 기존 패턴들...
]

# 선정적 언어 패턴 수정
SEXUAL_PATTERNS = [
    r'(수정된패턴)',  # 패턴 수정
    # 기존 패턴들...
]
```

#### 점수 기준 조정

```python
# 심각도 점수 조정
if severity_score >= 25:  # 기본값: 25
    decision = "거부"
elif severity_score >= 15:  # 기본값: 15
    decision = "경고"
```

#### 새로운 검사 항목 추가

```python
# 커스텀 검사 로직 추가
def custom_check(review_text: str) -> int:
    # 사용자 정의 검사 로직
    return score

# moderate_review_content 함수에 추가
custom_score = custom_check(review_text)
severity_score += custom_score
```

### Kiro Steering 파일 수정

`.kiro/steering/` 폴더의 파일들을 수정하여 AI 에이전트의 동작을 조정할 수 있습니다:

- `review-analysis.md`: 리뷰 분석 가이드라인
- `auto-response.md`: 자동 댓글 작성 가이드라인
- `seller-prompts.md`: 셀러 프롬프트 관리 가이드라인

Steering 파일은 다음과 같이 동작합니다:

- **Always included**: 기본적으로 모든 상호작용에 포함
- **Conditional**: 특정 파일이 컨텍스트에 있을 때만 포함
- **Manual**: 사용자가 `#` 키를 통해 수동으로 포함

## 📊 데이터 모델 업데이트 ✨

### Review 모델 확장

리뷰 키워드 및 감정 분석 기능을 위해 Review 모델에 새로운 필드들이 추가되었습니다:

```python
class Review(BaseModel):
    # 기존 필드들
    id: str
    user_name: str
    rating: int
    content: str
    date: str
    verified_purchase: bool = True
    auto_response: Optional[str] = None
    response_approved: bool = False

    # 새로 추가된 분석 데이터 필드들 ✨
    keywords: Optional[List[str]] = None          # 추출된 키워드 목록
    sentiment: Optional[dict] = None              # 감정 분석 결과
    analysis_completed: bool = False              # 분석 완료 여부
    analysis_timestamp: Optional[str] = None      # 분석 완료 시간

    # Agent 로그 연결
    agent_log_id: Optional[str] = None           # 연결된 Agent 로그 ID
```

### 감정 분석 데이터 구조

```python
sentiment = {
    "label": "긍정|부정|중립",           # 감정 분류
    "confidence": 0.85,                # 신뢰도 (0-1)
    "polarity": 0.7                    # 극성 (-1~1, 부정~긍정)
}
```

### Agent 로그 데이터 모델

```python
class AgentLogStep(BaseModel):
    step_name: str                     # 단계명
    start_time: str                    # 시작 시간
    end_time: Optional[str] = None     # 종료 시간
    duration_ms: Optional[int] = None  # 소요 시간 (밀리초)
    status: str                        # 상태 (in_progress, completed, failed)
    details: dict = {}                 # 상세 정보
    error_message: Optional[str] = None # 오류 메시지

class AgentLog(BaseModel):
    id: str                           # 로그 ID
    review_id: str                    # 연결된 리뷰 ID
    session_id: str                   # 세션 ID
    start_time: str                   # 세션 시작 시간
    end_time: Optional[str] = None    # 세션 종료 시간
    total_duration_ms: Optional[int] = None  # 전체 소요 시간
    status: str                       # 전체 상태
    steps: List[AgentLogStep] = []    # 처리 단계들
    metadata: dict = {}               # 메타데이터
    is_sample: bool = False           # 샘플 데이터 여부
```

## 🔧 개발 정보

### API 엔드포인트

**기본 엔드포인트**:

- `GET /`: 루트 엔드포인트 (서비스 정보)
- `GET /health`: 헬스 체크

**제품 및 리뷰 관리**:

- `GET /api/products`: 모든 제품 조회
- `GET /api/products/{product_id}`: 특정 제품 조회
- `POST /api/products/{product_id}/reviews`: 리뷰 작성 (검수 시스템 + 자동 분석 트리거) ✨
- `GET /api/products/{product_id}/reviews`: 제품 리뷰 조회 (키워드/감정 포함)
- `GET /api/reviews/{review_id}`: 특정 리뷰 조회

**자동 댓글 관리**:

- `POST /api/reviews/{review_id}/approve-response`: 자동 댓글 승인
- `DELETE /api/reviews/{review_id}/response`: 자동 댓글 거부

**Agent 로그 및 분석** ✨ (신규):

- `GET /api/reviews/{review_id}/agent-log`: 특정 리뷰의 Agent 처리 로그 조회 (캐싱 적용)
- `GET /api/agent-logs/{log_id}`: 로그 ID로 Agent 로그 조회 (캐싱 적용)
- `GET /api/agent-logs/stats`: Agent 로그 통계 및 캐시 상태 조회

**캐싱 시스템**:

- 메모리 기반 SimpleCache 구현 (기본 TTL: 10분)
- 자동 만료 처리 및 통계 수집
- 캐시 히트율 모니터링 및 성능 최적화
- 개별 항목별 TTL 설정 가능
- 캐시 무효화 및 수동 정리 기능

### 기술 스택

**백엔드**:

- FastAPI 0.104.0+
- Uvicorn (ASGI 서버)
- Strands Agents SDK
- Pydantic 2.0+
- Python 3.8+

**프론트엔드**:

- Next.js 14.0.0
- React 18
- TypeScript 5
- Tailwind CSS 3.3+ (아마존 스타일 디자인 시스템)
- Axios 1.6+
- 반응형 사이드바 레이아웃
- 카테고리별 이모지 아이콘
- React Router 기반 네비게이션

**AI/ML**:

- Strands Agents SDK
- Claude 3.7 Sonnet (Amazon Bedrock)
- 키워드 추출 및 감정 분석 시스템 ✨
- **구조화된 분석 엔진**: `analyze_review_for_storage()` 함수로 데이터베이스 최적화 ✨
- **향상된 오류 처리**: 분석 실패 시 안전한 폴백 메커니즘 ✨
- **리뷰 검수 시스템**: 정규식 기반 다층 필터링 및 점수 기반 자동 판정 ✨
- TextBlob (감정 분석)
- scikit-learn (머신러닝)
- NumPy (수치 계산)

**개발 도구**:

- Kiro IDE (MCP 지원)
- ESLint (코드 품질)
- PostCSS & Autoprefixer (CSS 처리)
- Agent 로그 수집 및 분석 시스템 ✨
- API 응답 캐싱 시스템 ✨ (메모리 기반, 자동 만료, 통계 수집)

**UI/UX 디자인**:

- **아마존 스타일 사이드바**: 고정 네비게이션으로 일관된 사용자 경험
- **반응형 레이아웃**: 데스크톱(280px), 태블릿(240px), 모바일(256px) 최적화
- **카테고리 기반 네비게이션**: 제품을 카테고리별로 자동 그룹화
- **실시간 하이라이트**: 현재 페이지 제품 자동 감지 및 표시
- 제품별 맞춤 CSS 그라디언트 (시각적 매력)
- 이모지 기반 제품 아이콘 시스템 (직관적 식별)
- 호버 애니메이션 효과 (상호작용 향상)
- 아마존 색상 팔레트 (#ff9900, #232f3e, #b12704)
- 스마트 이미지 시스템 (실제 이미지 + 폴백 디자인)
- CSS 애니메이션 (펄스, 바운스, 드롭 섀도우)
- 백드롭 블러 및 반투명 효과
- 향상된 카드 디자인 (둥근 모서리, 그림자)
- 자동 오류 처리 (이미지 로드 실패 시 그라디언트 폴백)

## 🤝 기여하기

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 🆘 문제 해결

### 일반적인 문제들

1. **Strands Agents 설치 오류**

   ```bash
   pip install --upgrade strands-agents strands-agents-tools
   ```

2. **AWS Bedrock 권한 오류**

   - AWS 계정에서 Bedrock 모델 액세스 권한 확인
   - IAM 역할에 필요한 권한 추가
   - Claude 3.7 Sonnet 모델 액세스 활성화

3. **CORS 오류**

   - 백엔드 서버가 포트 8000에서 실행되는지 확인
   - 프론트엔드가 포트 3000에서 실행되는지 확인
   - FastAPI CORS 미들웨어 설정 확인

4. **모듈 import 오류**

   - Python 경로 설정 확인: `sys.path.append()`
   - 가상환경 활성화 확인
   - agents 폴더의 requirements.txt 설치 확인

5. **Next.js 빌드 오류**

   - Node.js 버전 확인 (18+ 권장)
   - `npm install` 재실행
   - `.next` 폴더 삭제 후 재빌드

6. **MCP 서버 연결 오류**

   - Kiro IDE에서 MCP 서버 상태 확인
   - `.kiro/settings/mcp.json` 설정 검증
   - uvx 및 uv 설치 확인

7. **제품 이미지 표시 문제**

   - 이미지 파일이 `frontend/public/images/output/` 경로에 있는지 확인
   - 파일명이 올바른지 확인 (1.png, 2.png, 3.png, 4.png, 5.png)
   - 이미지 로드 실패 시 자동으로 그라디언트 폴백이 표시됨
   - 브라우저 개발자 도구에서 네트워크 탭으로 이미지 로드 상태 확인

8. **사이드바 네비게이션 문제**

   - Layout 컴포넌트가 모든 페이지에 적용되었는지 확인
   - useCurrentProduct 훅이 올바르게 제품 ID를 감지하는지 확인
   - CSS 클래스가 globals.css에 정의되어 있는지 확인
   - 카테고리 데이터가 productUtils에서 올바르게 로드되는지 확인

9. **TypeScript 타입 오류**

   - `frontend/types/product.ts`에서 타입 정의 확인
   - SidebarProduct, CategoryGroup 인터페이스 일치성 확인
   - 컴포넌트 props 타입 정의 확인

10. **키워드 및 감정 분석 문제** ✨ (신규)

- Review 모델의 새 필드(keywords, sentiment, analysis_completed) 확인
- 분석 데이터가 API 응답에 포함되는지 확인
- 프론트엔드에서 분석 데이터를 올바르게 처리하는지 확인
- 분석 실패 시 기본값 처리 로직 확인
- **새로운 `analyze_review_for_storage()` 함수 사용 확인** ✨
- **구조화된 데이터 저장이 올바르게 작동하는지 확인** ✨
- **키워드 개수가 6개로 제한되는지 확인** ✨
- **UI 컴포넌트가 올바르게 렌더링되는지 확인** ✨

11. **리뷰 내용 검수 시스템 문제** ✨ (신규)

- `content_moderation.py` 모듈이 올바르게 import되는지 확인
- 검수 패턴(공격적/선정적/스팸성)이 정확히 작동하는지 확인
- 심각도 점수 계산이 올바른지 확인 (공격적: +30, 선정적: +25, 스팸: +20)
- 검수 실패 시 리뷰가 저장되지 않는지 확인
- 상세한 에러 메시지가 프론트엔드에 전달되는지 확인
- 검수 통계 기능이 올바르게 작동하는지 확인

12. **Agent 로그 시스템 문제** ✨ (신규)

- 로그 데이터가 `data/agent_logs/` 폴더에 저장되는지 확인
- API 엔드포인트 `/api/reviews/{review_id}/agent-log` 응답 확인
- AgentLogButton이 자동 응답이 있는 리뷰에만 표시되는지 확인
- 로그 모달에서 단계별 정보가 올바르게 표시되는지 확인
- **캐싱 시스템이 올바르게 작동하는지 확인** ✨

13. **API 캐싱 시스템 문제** ✨ (신규)

- SimpleCache 클래스의 TTL 설정이 올바른지 확인 (`default_ttl=600`)
- 캐시 히트/미스 통계가 정확히 수집되는지 확인
- 만료된 캐시 항목이 자동으로 정리되는지 확인
- 캐시 무효화 기능이 올바르게 작동하는지 확인

### 샘플 제품 정보

시스템에는 5개의 샘플 제품이 준비되어 있습니다:

1. **프리미엄 무선 이어폰** (PROD-001) - 전자제품 🎧

   - 가격: ₩89,000
   - 설명: 고음질 무선 이어폰
   - 그라디언트: blue-purple

2. **트렌디 크롭 니트** (PROD-002) - 패션 👕

   - 가격: ₩45,000
   - 설명: 부드러운 크롭 니트
   - 그라디언트: pink-rose

3. **글로우 비타민 세럼** (PROD-003) - 화장품 ✨

   - 가격: ₩32,000
   - 설명: 비타민 C 글로우 세럼
   - 그라디언트: yellow-orange

4. **스마트 워치** (PROD-004) - 전자제품 ⌚

   - 가격: ₩125,000
   - 설명: 건강 관리 스마트 워치
   - 그라디언트: gray

5. **캐주얼 데님 자켓** (PROD-005) - 패션 🧥
   - 가격: ₩68,000
   - 설명: 클래식 데님 자켓
   - 그라디언트: indigo-blue

### 자동 실행 스크립트 문제

`run_demo.sh` 실행 시 문제가 발생하면:

```bash
# 실행 권한 부여
chmod +x run_demo.sh

# 개별 단계별 실행
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
pip install -r agents/requirements.txt
cd frontend && npm install
```

### 커스텀 제품 이미지 추가

새로운 제품 이미지를 추가하려면:

1. **이미지 파일 준비**: PNG 형식 권장, 정사각형 비율 최적
2. **파일 위치**: `frontend/public/images/output/` 폴더에 저장
3. **파일명 규칙**: `{제품번호}.png` (예: `1.png`, `2.png`)
4. **자동 폴백**: 이미지가 없거나 로드 실패 시 자동으로 그라디언트 배경 표시

```bash
# 예시: 새 제품 이미지 추가
cp my-product-image.png frontend/public/images/output/6.png
```

## 🔧 캐싱 시스템 아키텍처

### SimpleCache 클래스 구현

- **메모리 기반**: 빠른 액세스를 위한 인메모리 캐싱
- **TTL 관리**: 항목별 개별 TTL 설정 및 자동 만료 처리
- **통계 수집**: 캐시 히트율, 액세스 횟수, 만료 항목 추적
- **자동 정리**: 만료된 항목 자동 감지 및 제거

### 캐시 사용 패턴

```python
# 캐시 인스턴스 생성 (10분 기본 TTL)
agent_log_cache = SimpleCache(default_ttl=600)

# 캐시 저장 (개별 TTL 설정 가능)
cache_log("review_log_REV-001", log_data, ttl=600)

# 캐시 조회
cached_data = get_cached_log("review_log_REV-001")

# 캐시 통계 조회
stats = get_cache_stats()
```

### 성능 최적화

- **Agent 로그 조회**: 10분 캐싱으로 반복 조회 성능 향상
- **자동 만료**: 메모리 사용량 최적화
- **통계 모니터링**: 캐시 효율성 실시간 추적

## 📋 구현 현황

### ✅ 완료된 기능

- **아마존 스타일 사이드바 메뉴**: 전체 구현 완료
  - Layout, Sidebar, CategorySection, ProductItem 컴포넌트
  - useCurrentProduct 훅으로 자동 제품 감지
  - 아마존 스타일 CSS 디자인 시스템
  - 반응형 레이아웃 및 카테고리 그룹화
- **리뷰 내용 검수 시스템**: 전체 구현 완료 ✨
  - **다층 필터링 시스템**: 공격적/선정적/스팸성 내용 자동 탐지
  - **정교한 패턴 매칭**: 정규식 기반 다중 패턴 검사
  - **점수 기반 판정**: 심각도 점수(0-100) 계산 및 자동 결정
  - **상세 피드백**: 구체적인 문제점과 개선 제안 제공
  - **통계 기능**: 검수 통계 및 일반적인 문제 패턴 분석
  - **테스트 케이스**: 6가지 시나리오로 검증된 검수 로직
- **제품 리뷰 시스템**: 기본 기능 완료
- **AI 자동 댓글 생성**: Strands Agent 기반 구현
- **스마트 이미지 시스템**: 실제 이미지 + 폴백 처리
- **향상된 푸터 디자인**: 개발 도구 크레딧 및 그라디언트 배경 적용 ✨
- **리뷰 키워드 및 감정 분석**: 전체 구현 완료 ✨
  - Review 모델에 keywords, sentiment, analysis_completed 필드 추가
  - 분석 타임스탬프 및 완료 상태 추적 기능
  - **구조화된 분석 함수**: `analyze_review_for_storage()` 구현 완료 ✨
  - **향상된 오류 처리**: 분석 실패 시 안전한 폴백 메커니즘 구현 ✨
  - **키워드 최적화**: 최대 6개 키워드로 제한하여 UI 성능 향상 ✨
  - **UI 컴포넌트**: KeywordTags, SentimentIndicator, HighlightedText 구현 완료 ✨
  - **분석 통계**: ReviewAnalytics 대시보드로 키워드 빈도 및 감정 분포 시각화 ✨
- **Agent 로그 시스템**: 전체 구현 완료 ✨
  - AgentLog, AgentLogStep 데이터 모델 구현
  - 로그 수집기 및 샘플 로그 생성기 구현
  - API 엔드포인트 및 캐싱 시스템 추가
  - **프론트엔드 구현**: AgentLogButton 및 AgentLogModal 컴포넌트 완료 ✨
  - **실시간 로그 뷰어**: 단계별 처리 과정 시각화 및 소요 시간 표시 ✨
- **API 캐싱 시스템**: 메모리 기반 캐싱 구현 완료 ✨
  - SimpleCache 클래스로 TTL 기반 캐싱
  - 자동 만료 처리 및 통계 수집
  - 캐시 히트율 모니터링 및 성능 최적화

### 🚧 진행 중인 기능

- **실시간 로그 기록**: 자동 응답 생성 과정에 로그 수집기 통합
- **고급 필터링**: 키워드 기반 리뷰 필터링 및 검색

### 📋 구현 예정 기능

- 실시간 알림 시스템
- 셀러 프롬프트 활용 내역 표시
- 로그 데이터 압축 및 아카이빙
- 성능 모니터링 대시보드

## 🎨 개발 도구 및 크레딧

### AI 기반 개발 환경

이 프로젝트는 최신 AI 개발 도구들을 활용하여 100% 완성되었습니다:

- **🤖 Strands Agents**: 리뷰 분석 및 자동 댓글 생성 AI 시스템
- **💻 Amazon Q Developer**: 코드 생성, 리팩토링, 디버깅 지원
- **🔧 Kiro IDE**: AI 기반 통합 개발 환경 및 코드 어시스턴트
- **🎨 Amazon Nova Canvas**: 모든 제품 이미지 AI 생성

### 개발 프로세스

- **AI 페어 프로그래밍**: Amazon Q Developer와의 협업으로 효율적인 코드 작성
- **자동화된 테스트**: AI 기반 테스트 케이스 생성 및 검증
- **지능형 리팩토링**: 코드 품질 향상을 위한 AI 제안 적용
- **실시간 디버깅**: Kiro의 AI 어시스턴트를 통한 즉시 문제 해결

### 시각적 자산

- **제품 이미지**: Amazon Nova Canvas로 생성된 고품질 AI 이미지
- **폴백 디자인**: 이미지 로드 실패 시 자동 그라디언트 배경 표시
- **일관된 디자인**: AI 도구를 활용한 통일된 시각적 아이덴티티

이 프로젝트는 AI 기반 개발 도구들의 강력함과 효율성을 보여주는 실제 사례입니다.

## 📞 지원

문제가 발생하거나 질문이 있으시면 이슈를 생성해주세요.
