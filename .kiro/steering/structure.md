# Project Structure

## Overall Architecture

```
product-review-automation/
├── frontend/                          # Next.js React 애플리케이션
├── backend/                           # FastAPI 백엔드 서버
├── agents/                            # Strands Agents 구현
├── .kiro/                            # Kiro IDE 설정 및 문서
├── data/                             # 샘플 데이터 및 설정
├── infrastructure/                    # 인프라 코드 (향후 추가)
└── docs/                             # 프로젝트 문서 (향후 추가)
```

## Frontend Structure (`frontend/`)

### Directory Organization
```
frontend/
├── components/                        # 재사용 가능한 React 컴포넌트
│   ├── Layout.tsx                    # 전체 페이지 레이아웃
│   ├── Sidebar.tsx                   # 아마존 스타일 사이드바
│   ├── CategorySection.tsx           # 카테고리별 제품 그룹
│   ├── ProductItem.tsx               # 개별 제품 항목
│   ├── ProductDetail.tsx             # 제품 상세 정보
│   ├── ReviewList.tsx                # 리뷰 목록 표시
│   ├── ReviewForm.tsx                # 리뷰 작성 폼
│   ├── ReviewAnalytics.tsx           # 리뷰 분석 대시보드
│   ├── KeywordTags.tsx               # 키워드 태그 컴포넌트
│   ├── SentimentIndicator.tsx        # 감정 표시 컴포넌트
│   ├── HighlightedText.tsx           # 키워드 하이라이팅
│   ├── AgentLogButton.tsx            # Agent 로그 확인 버튼
│   └── AgentLogModal.tsx             # Agent 로그 뷰어 모달
├── pages/                            # Next.js 페이지 라우팅
│   ├── index.tsx                     # 메인 페이지 (제품 목록)
│   ├── product/                      # 제품 관련 페이지
│   │   └── [id].tsx                  # 동적 제품 상세 페이지
│   └── _app.tsx                      # 앱 전역 설정
├── hooks/                            # 커스텀 React 훅
│   └── useCurrentProduct.ts          # 현재 제품 ID 감지 훅
├── types/                            # TypeScript 타입 정의
│   └── product.ts                    # 제품 관련 타입들
├── utils/                            # 유틸리티 함수
│   └── productUtils.ts               # 제품 데이터 처리 함수
├── services/                         # API 서비스 레이어
│   └── productApiService.ts          # 제품 API 호출 함수
├── styles/                           # 스타일 파일
│   └── globals.css                   # 전역 CSS 및 Tailwind 설정
├── public/                           # 정적 파일
│   └── images/                       # 이미지 파일
│       └── output/                   # 제품 이미지 (AI 생성)
├── __tests__/                        # 테스트 파일
│   ├── DataConsistency.integration.test.tsx
│   └── RatingCalculator.test.ts
├── package.json                      # 의존성 및 스크립트
├── tsconfig.json                     # TypeScript 설정
├── tailwind.config.js                # Tailwind CSS 설정
└── next.config.js                    # Next.js 설정
```

### Component Naming Conventions
- **PascalCase**: 모든 React 컴포넌트 파일명 (`ProductDetail.tsx`)
- **Descriptive Names**: 기능을 명확히 나타내는 이름 사용
- **Single Responsibility**: 하나의 컴포넌트는 하나의 책임만 가짐

### Import Patterns
```typescript
// 1. 외부 라이브러리
import React, { useState, useEffect } from 'react';
import axios from 'axios';

// 2. 내부 타입 및 인터페이스
import { Product, Review } from '../types/product';

// 3. 내부 컴포넌트 및 훅
import { useCurrentProduct } from '../hooks/useCurrentProduct';

// 4. 상대 경로 import
import './ProductDetail.module.css';
```

## Backend Structure (`backend/`)

### Directory Organization
```
backend/
├── app/                              # 메인 애플리케이션 코드
│   ├── main.py                       # FastAPI 애플리케이션 진입점
│   ├── models/                       # 데이터 모델 정의
│   │   ├── __init__.py
│   │   ├── product.py                # 제품 모델
│   │   └── review.py                 # 리뷰 모델 (키워드/감정 분석 포함)
│   ├── api/                          # API 엔드포인트
│   │   ├── __init__.py
│   │   ├── products.py               # 제품 관련 API
│   │   └── reviews.py                # 리뷰 관련 API (로그 조회 포함)
│   └── services/                     # 비즈니스 로직 서비스
│       ├── __init__.py
│       ├── product_data_service.py   # 제품 데이터 서비스
│       ├── agent_log_service.py      # Agent 로그 관리
│       ├── sample_log_generator.py   # 샘플 로그 생성
│       ├── api_cache.py              # API 캐싱 시스템
│       └── log_utils.py              # 로그 유틸리티
├── tests/                            # 테스트 파일
│   ├── __init__.py
│   ├── test_api_integration.py       # API 통합 테스트
│   └── test_product_data_service.py  # 서비스 단위 테스트
├── requirements.txt                  # Python 의존성
└── Dockerfile                        # Docker 설정 (향후 추가)
```

### Python Naming Conventions
- **snake_case**: 모든 파일명, 함수명, 변수명
- **PascalCase**: 클래스명 (`ProductDataService`)
- **UPPER_CASE**: 상수 (`DEFAULT_TTL = 600`)

### Module Import Patterns
```python
# 1. 표준 라이브러리
import os
import json
from datetime import datetime
from typing import List, Optional, Dict

# 2. 외부 라이브러리
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# 3. 내부 모듈 (절대 경로)
from app.models.product import Product
from app.services.agent_log_service import AgentLogService

# 4. 상대 경로 (같은 패키지 내)
from .product_data_service import ProductDataService
```

## Agents Structure (`agents/`)

### Directory Organization
```
agents/
├── review_analyzer/                  # 리뷰 분석 Agent
│   ├── __init__.py
│   ├── agent.py                      # 메인 Agent 로직
│   ├── tools.py                      # Agent 도구들
│   └── content_moderation.py         # 리뷰 내용 검수 시스템
├── auto_responder/                   # 자동 댓글 생성 Agent
│   ├── __init__.py
│   ├── agent.py                      # 메인 Agent 로직
│   └── tools.py                      # Agent 도구들
├── requirements.txt                  # Agent 의존성
└── shared/                           # 공통 유틸리티 (향후 추가)
    ├── __init__.py
    └── utils.py
```

### Agent Development Patterns
- **Single Purpose**: 각 Agent는 명확한 단일 목적을 가짐
- **Tool-based Architecture**: 기능을 Tool로 분리하여 재사용성 향상
- **Error Handling**: 모든 Agent 실행에 적절한 오류 처리 구현
- **Logging**: 상세한 실행 로그 기록으로 디버깅 지원

## Kiro Configuration (`.kiro/`)

### Directory Organization
```
.kiro/
├── settings/                         # Kiro 설정 파일
│   └── mcp.json                      # MCP 서버 설정
├── steering/                         # Steering 문서
│   ├── product.md                    # 제품 개요
│   ├── tech.md                       # 기술 스택
│   ├── structure.md                  # 프로젝트 구조 (이 파일)
│   ├── port-management.md            # 포트 관리 가이드라인
│   └── seller-prompts.md             # 셀러 프롬프트 관리
└── specs/                            # 기능 명세서
    ├── product-sidebar-menu/         # 사이드바 메뉴 명세
    ├── review-keyword-sentiment-analysis/  # 키워드/감정 분석 명세
    ├── rating-data-consistency/      # 데이터 일관성 명세
    ├── sidebar-all-products-view/    # 전체 제품 뷰 명세
    └── agent-log-viewer/             # Agent 로그 뷰어 명세
```

### Steering File Conventions
- **Descriptive Names**: 기능을 명확히 나타내는 파일명
- **Markdown Format**: 모든 steering 파일은 `.md` 확장자 사용
- **Front Matter**: 필요시 YAML front matter로 inclusion 모드 설정
- **Clear Structure**: 일관된 헤더 구조 및 섹션 구성

## Data Structure (`data/`)

### Directory Organization
```
data/
├── sample_products.json              # 샘플 제품 데이터
├── seller_prompts.json               # 셀러별 프롬프트 설정
├── agent_logs/                       # Agent 실행 로그 저장소
│   ├── review_log_REV-001.json
│   ├── review_log_REV-002.json
│   └── ...
├── cache/                            # 캐시 데이터 (gitignore)
└── temp/                             # 임시 파일 (gitignore)
```

### Data File Conventions
- **JSON Format**: 모든 데이터 파일은 JSON 형식 사용
- **Descriptive Names**: 데이터 용도를 명확히 나타내는 파일명
- **Structured Format**: 일관된 데이터 구조 및 스키마 유지
- **Agent Logs**: `review_log_REV-{ID}.json` 형식으로 저장
- **Cache Management**: 임시 파일은 gitignore 처리

## File Naming Conventions

### General Rules
- **Lowercase with hyphens**: 폴더명 (`review-analyzer`, `agent-logs`)
- **camelCase**: JavaScript/TypeScript 파일 및 변수
- **snake_case**: Python 파일 및 변수
- **PascalCase**: React 컴포넌트 및 Python 클래스
- **kebab-case**: CSS 클래스 및 HTML 속성

### Specific Patterns
```
# React 컴포넌트
ProductDetail.tsx
ReviewForm.tsx
AgentLogModal.tsx

# Python 모듈
product_data_service.py
agent_log_service.py
content_moderation.py

# 설정 파일
package.json
requirements.txt
tsconfig.json

# 문서 파일
README.md
workshop-todo.md
port-management.md
```

## Import and Export Patterns

### Frontend (TypeScript/React)
```typescript
// Named exports (권장)
export const ProductDetail: React.FC<ProductDetailProps> = ({ productId }) => {
  // 컴포넌트 로직
};

// Default export (페이지 컴포넌트)
export default function ProductPage() {
  // 페이지 로직
}

// Type exports
export type { Product, Review, AgentLog } from './types/product';
```

### Backend (Python)
```python
# 명시적 import (권장)
from app.models.product import Product
from app.services.agent_log_service import AgentLogService

# 모듈 레벨 exports
__all__ = ['Product', 'Review', 'AgentLog']
```

## Configuration Management

### Environment Variables
```bash
# Development
NODE_ENV=development
NEXT_PUBLIC_API_URL=http://localhost:8000

# Production
NODE_ENV=production
NEXT_PUBLIC_API_URL=https://api.example.com
```

### Configuration Files
- **Frontend**: `next.config.js`, `tailwind.config.js`, `tsconfig.json`
- **Backend**: `requirements.txt`, `pyproject.toml` (향후)
- **Agents**: `requirements.txt`, `agentcore.yaml` (향후)

## Testing Structure

### Frontend Tests
```
frontend/__tests__/
├── components/                       # 컴포넌트 테스트
│   ├── ProductDetail.test.tsx
│   └── ReviewForm.test.tsx
├── hooks/                           # 훅 테스트
│   └── useCurrentProduct.test.ts
├── utils/                           # 유틸리티 테스트
│   └── productUtils.test.ts
└── integration/                     # 통합 테스트
    └── DataConsistency.integration.test.tsx
```

### Backend Tests
```
backend/tests/
├── unit/                            # 단위 테스트
│   ├── test_product_service.py
│   └── test_agent_log_service.py
├── integration/                     # 통합 테스트
│   └── test_api_integration.py
└── fixtures/                        # 테스트 데이터
    ├── sample_products.json
    └── sample_reviews.json
```

## Build and Deployment Structure

### Build Artifacts
```
# Frontend build
frontend/.next/                      # Next.js 빌드 출력
frontend/out/                        # Static export (필요시)

# Backend build
backend/dist/                        # 빌드된 Python 패키지 (향후)

# Agent deployment
agents/build/                        # AgentCore 빌드 출력 (향후)
```

### Deployment Configuration
```
infrastructure/                      # 인프라 코드 (향후 추가)
├── cloudformation/                  # CloudFormation 템플릿
│   ├── main.yaml
│   ├── network-stack.yaml
│   ├── dynamodb-stack.yaml
│   └── serverless-stack.yaml
├── scripts/                         # 배포 스크립트
│   ├── deploy.sh
│   └── rollback.sh
└── environments/                    # 환경별 설정
    ├── dev.yaml
    ├── staging.yaml
    └── prod.yaml
```

## Code Organization Principles

### Single Responsibility
- 각 파일과 함수는 하나의 명확한 책임만 가짐
- 컴포넌트는 단일 UI 요소 또는 기능에 집중
- 서비스는 특정 도메인 로직에만 집중

### Separation of Concerns
- **Presentation Layer**: React 컴포넌트 (UI 로직)
- **Business Logic**: 서비스 레이어 (비즈니스 로직)
- **Data Layer**: 모델 및 API (데이터 처리)
- **Infrastructure**: 설정 및 배포 (인프라 관리)

### Dependency Direction
- 상위 레벨 모듈은 하위 레벨 모듈에 의존
- 인터페이스를 통한 의존성 역전 (필요시)
- 순환 의존성 방지

### Reusability
- 공통 로직은 유틸리티 함수로 분리
- 재사용 가능한 컴포넌트는 `components/` 폴더에 배치
- 공통 타입은 `types/` 폴더에 정의

## Documentation Standards

### Code Documentation
- **JSDoc**: JavaScript/TypeScript 함수 및 클래스 문서화
- **Docstrings**: Python 함수 및 클래스 문서화
- **Inline Comments**: 복잡한 로직에 대한 설명
- **Type Annotations**: 모든 함수 매개변수 및 반환값 타입 명시

### Project Documentation
- **README.md**: 프로젝트 개요 및 시작 가이드
- **API Documentation**: OpenAPI/Swagger 자동 생성
- **Architecture Docs**: 시스템 아키텍처 및 설계 문서
- **Deployment Guides**: 배포 및 운영 가이드