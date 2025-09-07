# Technology Stack

## Frontend Technologies

### Core Framework
- **Next.js 14.0+**: React 기반 풀스택 프레임워크
  - App Router 사용 (pages/ 디렉토리 구조)
  - Server-side rendering (SSR) 및 Static generation 지원
  - API Routes 활용한 백엔드 통합

### UI/UX Libraries
- **React 18**: 함수형 컴포넌트 및 Hooks 패턴 사용
- **TypeScript 5**: 강타입 언어로 타입 안전성 보장
- **Tailwind CSS 3.3+**: 유틸리티 기반 CSS 프레임워크
  - 아마존 스타일 디자인 시스템 구현
  - 반응형 디자인 (모바일 우선)
  - 커스텀 CSS 변수 활용

### State Management & Data Fetching
- **React Hooks**: useState, useEffect, useContext 등 내장 훅 활용
- **Custom Hooks**: useCurrentProduct 등 재사용 가능한 로직 분리
- **Axios 1.6+**: HTTP 클라이언트 라이브러리
- **SWR/React Query**: 서버 상태 관리 (필요시 도입 예정)

### Development Tools
- **ESLint**: 코드 품질 및 일관성 유지
- **Prettier**: 코드 포맷팅 자동화
- **PostCSS & Autoprefixer**: CSS 후처리 및 브라우저 호환성

## Backend Technologies

### Core Framework
- **FastAPI 0.104.0+**: 고성능 Python 웹 프레임워크
  - 자동 API 문서 생성 (OpenAPI/Swagger)
  - 타입 힌트 기반 데이터 검증
  - 비동기 처리 지원 (async/await)

### Data & Validation
- **Pydantic 2.0+**: 데이터 모델링 및 검증
  - BaseModel 클래스 기반 구조화된 데이터
  - 자동 타입 변환 및 검증
  - JSON 직렬화/역직렬화

### Server & Deployment
- **Uvicorn**: ASGI 서버 (개발 및 프로덕션)
- **Gunicorn**: 프로덕션 환경 WSGI 서버 (필요시)

## AI/ML Technologies

### AI Agent Framework
- **Strands Agents SDK**: 핵심 AI Agent 개발 프레임워크
  - Agent 정의 및 실행 환경
  - Tool 기반 확장 가능한 아키텍처
  - 비동기 처리 및 스트리밍 지원

### Language Models
- **Claude 3.7 Sonnet**: 주요 LLM 모델
  - Amazon Bedrock을 통한 접근
  - 모델 ID: `us.anthropic.claude-3-7-sonnet-20250219-v1:0`
  - 고품질 텍스트 생성 및 분석

### ML Libraries
- **TextBlob**: 기본 감정 분석 및 텍스트 처리
- **scikit-learn**: 머신러닝 알고리즘 및 전처리
- **NumPy**: 수치 계산 및 배열 처리
- **NLTK**: 자연어 처리 (키워드 추출, 토큰화)
- **정규식 기반 검수**: 다층 필터링 시스템으로 부적절한 내용 자동 탐지

## Database & Storage

### Primary Database
- **DynamoDB**: NoSQL 데이터베이스 (프로덕션)
  - 서버리스 확장성
  - 글로벌 보조 인덱스 (GSI) 활용
  - 트랜잭션 지원

### Caching Layer
- **ElastiCache Redis**: 인메모리 캐싱
  - API 응답 캐싱 (TTL: 10분)
  - 세션 데이터 저장
  - 실시간 데이터 캐싱

### File Storage
- **Amazon S3**: 정적 파일 및 로그 저장
  - 제품 이미지 저장
  - Agent 로그 아카이빙
  - 백업 데이터 저장

## Development Environment

### Version Control
- **Git**: 소스 코드 버전 관리
- **GitHub**: 원격 저장소 및 협업 플랫폼
- **GitHub Actions**: CI/CD 파이프라인

### Package Management
- **npm**: Node.js 패키지 관리 (Frontend)
- **pip**: Python 패키지 관리 (Backend/Agents)
- **venv**: Python 가상환경 관리

### IDE & Tools
- **Kiro IDE**: AI 기반 통합 개발 환경
  - MCP (Model Context Protocol) 지원
  - Steering 파일 기반 컨텍스트 관리
  - Agent 개발 및 테스트 지원

## Cloud Infrastructure (AWS)

### Compute Services
- **AWS Lambda**: 서버리스 컴퓨팅 (AgentCore 배포)
- **API Gateway**: RESTful API 엔드포인트 관리
- **CloudFront**: CDN 및 정적 파일 배포

### AI/ML Services
- **Amazon Bedrock**: LLM 모델 접근 및 관리
- **Amazon Comprehend**: 추가 텍스트 분석 (필요시)
- **Amazon Translate**: 다국어 지원 (향후 계획)

### Monitoring & Logging
- **CloudWatch**: 로그 수집 및 모니터링
- **X-Ray**: 분산 추적 및 성능 분석
- **CloudTrail**: API 호출 감사 로그

### Security & Identity
- **AWS IAM**: 권한 및 역할 관리
- **AWS Cognito**: 사용자 인증 및 인가 (향후 계획)
- **AWS KMS**: 데이터 암호화 키 관리

## Development Workflow

### Code Quality
- **TypeScript**: 프론트엔드 타입 안전성
- **Python Type Hints**: 백엔드 타입 안전성
- **ESLint + Prettier**: 코드 스타일 일관성
- **Pre-commit Hooks**: 커밋 전 자동 검증

### Testing Strategy
- **Jest**: JavaScript/TypeScript 단위 테스트
- **React Testing Library**: React 컴포넌트 테스트
- **pytest**: Python 단위 및 통합 테스트
- **Playwright**: End-to-End 테스트 (향후 계획)

### Build & Deployment
- **Next.js Build**: 프론트엔드 빌드 및 최적화
- **AgentCore CLI**: Agent 배포 및 관리
- **GitHub Actions**: 자동화된 CI/CD 파이프라인

## Performance Considerations

### Frontend Optimization
- **Code Splitting**: 번들 크기 최적화
- **Image Optimization**: WebP 포맷 및 지연 로딩
- **Caching Strategy**: 브라우저 캐싱 및 CDN 활용
- **Bundle Analysis**: webpack-bundle-analyzer 사용

### Backend Optimization
- **Async Processing**: 비동기 요청 처리
- **Connection Pooling**: 데이터베이스 연결 최적화
- **Response Compression**: gzip 압축 적용
- **API Rate Limiting**: 요청 제한 및 보호

### Database Optimization
- **Query Optimization**: 효율적인 DynamoDB 쿼리 패턴
- **Indexing Strategy**: GSI/LSI 최적 설계
- **Batch Operations**: 대량 데이터 처리 최적화
- **TTL Management**: 자동 데이터 만료 처리

## Security Best Practices

### Data Protection
- **Input Validation**: Pydantic 기반 데이터 검증
- **SQL Injection Prevention**: ORM 사용 및 파라미터화 쿼리
- **XSS Protection**: React의 기본 XSS 방어 + 추가 검증
- **CSRF Protection**: SameSite 쿠키 및 토큰 기반 보호

### API Security
- **HTTPS Only**: 모든 통신 암호화
- **CORS Configuration**: 적절한 CORS 정책 설정
- **Rate Limiting**: API 남용 방지
- **Authentication**: JWT 기반 인증 (향후 구현)

### Infrastructure Security
- **IAM Least Privilege**: 최소 권한 원칙
- **VPC Security Groups**: 네트워크 레벨 보안
- **Secrets Management**: AWS Secrets Manager 활용
- **Audit Logging**: 모든 중요 작업 로깅

## Monitoring & Observability

### Application Monitoring
- **LangFuse**: Agent 실행 추적 및 분석
- **AgentCore Observability**: Agent 성능 모니터링
- **Custom Metrics**: 비즈니스 메트릭 수집
- **Agent 로그 시스템**: 단계별 처리 과정 추적 및 성능 측정
- **API 캐싱**: 메모리 기반 SimpleCache (TTL: 10분)

### Infrastructure Monitoring
- **CloudWatch Dashboards**: 시스템 메트릭 시각화
- **Alarms & Notifications**: 자동 알림 시스템
- **Log Aggregation**: 중앙화된 로그 관리

### Performance Tracking
- **Response Time Monitoring**: API 응답 시간 추적
- **Error Rate Tracking**: 오류율 모니터링
- **Resource Utilization**: CPU, 메모리, 네트워크 사용량

## Development Standards

### Coding Conventions
- **Naming**: camelCase (JS/TS), snake_case (Python)
- **File Organization**: 기능별 폴더 구조
- **Import Order**: 외부 라이브러리 → 내부 모듈 → 상대 경로
- **Component Structure**: 단일 책임 원칙 준수

### Documentation
- **Code Comments**: 복잡한 로직에 대한 명확한 설명
- **API Documentation**: OpenAPI/Swagger 자동 생성
- **README Files**: 각 모듈별 사용법 및 설정 가이드
- **Type Definitions**: 명확한 타입 정의 및 인터페이스

### Version Management
- **Semantic Versioning**: MAJOR.MINOR.PATCH 형식
- **Dependency Updates**: 정기적인 의존성 업데이트
- **Breaking Changes**: 명확한 마이그레이션 가이드 제공
- **Changelog**: 버전별 변경사항 문서화