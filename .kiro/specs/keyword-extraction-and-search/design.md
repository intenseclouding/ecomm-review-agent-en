# Design Document

## Overview

키워드 추출 및 검색 시스템은 리뷰 텍스트에서 핵심 키워드를 자동으로 추출하고, 키워드 기반 검색 기능을 제공하는 Strands Agent입니다. Claude 3.7을 활용하여 한국어 구어체 표현에서도 정확한 키워드를 추출하며, 기존 시스템과의 완전한 호환성을 보장합니다.

## Architecture

### System Components

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Client API    │───▶│  Keyword Agent   │───▶│   SQLite DB     │
│                 │    │                  │    │                 │
│ - extract       │    │ - extract_keywords│    │ - reviews       │
│ - search        │    │ - upsert_review   │    │ - keywords      │
│ - upsert        │    │ - search_reviews  │    │ - review_keywords│
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │   Claude 3.7     │
                       │   (Bedrock)      │
                       └──────────────────┘
```

### Agent Structure

```
agents/keyword_extractor/
├── __init__.py
├── agent.py          # Main agent class
├── tools.py          # Tool implementations
└── prompts.py        # LLM prompts
```

## Data Model

### Database Schema

```sql
-- 리뷰 테이블
CREATE TABLE reviews (
    id INTEGER PRIMARY KEY,
    text TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 키워드 테이블 (중복 방지)
CREATE TABLE keywords (
    id INTEGER PRIMARY KEY,
    keyword TEXT UNIQUE NOT NULL
);

-- 리뷰-키워드 관계 테이블 (다대다)
CREATE TABLE review_keywords (
    review_id INTEGER,
    keyword_id INTEGER,
    PRIMARY KEY (review_id, keyword_id),
    FOREIGN KEY (review_id) REFERENCES reviews(id),
    FOREIGN KEY (keyword_id) REFERENCES keywords(id)
);

-- 검색 성능을 위한 인덱스
CREATE INDEX idx_keywords_keyword ON keywords(keyword);
CREATE INDEX idx_review_keywords_keyword_id ON review_keywords(keyword_id);
```

## Tool Specifications

### 1. extract_keywords(review: str) -> dict

**Purpose:** 리뷰 텍스트에서 1-5개의 핵심 키워드를 추출

**Input:**
```json
{
    "review": "핏이 미친듯이 좋고 발림성도 개좋아요. 색상도 예뻐서 만족합니다."
}
```

**Output:**
```json
{
    "keywords": ["핏", "발림성", "색상"]
}
```

**Implementation Logic:**
1. Claude 3.7에 한국어 키워드 추출 프롬프트 전송
2. 구어체 표현에서 핵심 명사 추출
3. 제품 관련 용어 우선순위 부여
4. 1-5개 키워드로 제한하여 반환

### 2. upsert_review(review_id: int, text: str, keywords: list[str]) -> None

**Purpose:** 리뷰와 키워드를 데이터베이스에 저장/업데이트

**Input:**
```json
{
    "review_id": 123,
    "text": "핏이 미친듯이 좋고 발림성도 개좋아요.",
    "keywords": ["핏", "발림성"]
}
```

**Implementation Logic:**
1. 리뷰 테이블에 INSERT OR REPLACE
2. 각 키워드를 keywords 테이블에 INSERT OR IGNORE
3. review_keywords 관계 테이블 업데이트
4. 트랜잭션으로 데이터 일관성 보장

### 3. search_reviews_by_keyword(keyword: str) -> list[dict]

**Purpose:** 키워드로 관련 리뷰 검색

**Input:**
```json
{
    "keyword": "핏"
}
```

**Output:**
```json
[
    {
        "review_id": 123,
        "text": "핏이 미친듯이 좋고 발림성도 개좋아요."
    },
    {
        "review_id": 456,
        "text": "핏은 좋은데 색상이 아쉬워요."
    }
]
```

**Implementation Logic:**
1. 키워드로 keyword_id 조회
2. review_keywords 테이블 조인하여 관련 리뷰 검색
3. 생성일 기준 내림차순 정렬
4. review_id와 text 필드만 반환

## LLM Prompt Design

### Keyword Extraction Prompt

```
당신은 한국어 리뷰에서 핵심 키워드를 추출하는 전문가입니다.

주어진 리뷰 텍스트에서 고객이 관심을 가질 만한 핵심 키워드 1-5개를 추출해주세요.

규칙:
1. 구어체 표현에서 핵심 명사만 추출 (예: "핏이 미친듯" → "핏")
2. 제품 특성 관련 용어 우선 (핏, 발림성, 색상, 질감 등)
3. 감정 표현은 제외 (좋다, 나쁘다, 만족 등)
4. 최대 5개까지만 추출

리뷰: {review_text}

JSON 형식으로 응답해주세요:
{"keywords": ["키워드1", "키워드2", ...]}
```

## Integration Points

### API Compatibility

기존 시스템의 API 엔드포인트와 완전 호환:

```python
# 기존 호출 방식 그대로 유지
result = agent.extract_keywords("리뷰 텍스트")
agent.upsert_review(123, "리뷰 텍스트", ["키워드1", "키워드2"])
reviews = agent.search_reviews_by_keyword("핏")
```

### Data Flow

1. **리뷰 생성 시:**
   ```
   새 리뷰 → extract_keywords() → upsert_review() → DB 저장
   ```

2. **키워드 검색 시:**
   ```
   검색 요청 → search_reviews_by_keyword() → 관련 리뷰 반환
   ```

## Implementation Plan

### Phase 1: Core Agent Setup
- Agent 클래스 및 기본 구조 생성
- SQLite 데이터베이스 스키마 구현
- 기본 도구 스켈레톤 작성

### Phase 2: Keyword Extraction
- Claude 3.7 연동 구현
- 한국어 키워드 추출 프롬프트 최적화
- extract_keywords 도구 완성

### Phase 3: Data Management
- upsert_review 도구 구현
- 데이터베이스 트랜잭션 처리
- 키워드 중복 방지 로직

### Phase 4: Search Functionality
- search_reviews_by_keyword 도구 구현
- 검색 결과 정렬 및 포맷팅
- 성능 최적화

### Phase 5: Integration Testing
- 기존 시스템과의 호환성 테스트
- API 계약 준수 확인
- 드롭인 교체 검증