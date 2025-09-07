# 제품 리뷰 자동화 시스템 프로젝트 구조

## 전체 폴더 구조
```
product-review-automation/
├── frontend/                          # 제품 상세 페이지 (React/Next.js)
│   ├── components/
│   │   ├── ProductDetail.tsx
│   │   ├── ReviewForm.tsx
│   │   └── ReviewList.tsx
│   ├── pages/
│   │   └── product/[id].tsx
│   └── package.json
├── backend/                           # API 서버 (FastAPI)
│   ├── app/
│   │   ├── models/
│   │   │   ├── product.py
│   │   │   └── review.py
│   │   ├── api/
│   │   │   ├── products.py
│   │   │   └── reviews.py
│   │   └── main.py
│   └── requirements.txt
├── agents/                            # Strands Agents
│   ├── review_analyzer/               # 리뷰 분석 에이전트
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   └── tools.py
│   ├── auto_responder/                # 자동 댓글 작성 에이전트
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   └── tools.py
│   └── requirements.txt
├── .kiro/
│   └── steering/                      # Kiro Steering 파일들
│       ├── review-analysis.md
│       ├── auto-response.md
│       └── seller-prompts.md
└── data/
    ├── seller_prompts.json            # 셀러별 자동댓글 프롬프트
    └── sample_products.json           # 샘플 제품 데이터
```

## 주요 컴포넌트

### 1. Frontend (React/Next.js)
- 제품 상세 페이지
- 리뷰 작성 폼
- 실시간 리뷰 표시

### 2. Backend (FastAPI)
- RESTful API
- 데이터베이스 연동
- Strands Agent 트리거

### 3. Strands Agents
- **Review Analyzer**: 리뷰 감정분석, 키워드 추출
- **Auto Responder**: 자동 댓글 생성 및 승인

### 4. Steering Files
- 리뷰 분석 가이드라인
- 자동 댓글 작성 규칙
- 셀러별 프롬프트 관리