# 키워드 추출기 에이전트

한국어 리뷰에서 키워드를 자동으로 추출하고 키워드 기반 검색을 제공하는 Strands Agent입니다.

## 개요

이 에이전트는 Claude 3.7을 활용하여 한국어 구어체 표현에서도 정확한 키워드를 추출하며, 기존 시스템과의 완전한 호환성을 보장합니다.

### 주요 기능

- **키워드 추출**: 리뷰 텍스트에서 1-5개의 핵심 키워드 자동 추출
- **키워드 저장**: 추출된 키워드와 리뷰를 데이터베이스에 저장
- **키워드 검색**: 키워드 기반 리뷰 검색 기능
- **한국어 지원**: 구어체 표현 처리 ("핏이 미친듯" → "핏")

## 파일 구조

```
agents/keyword_extractor/
├── __init__.py          # 패키지 초기화
├── agent.py            # Strands Agent 정의
├── tools.py            # 도구 구현 (extract_keywords, upsert_review, search_reviews_by_keyword)
├── prompts.py          # 키워드 추출 프롬프트
└── README.md           # 이 파일
```

## 사용법

### Strands Agent 사용

```python
from keyword_extractor.agent import keyword_extractor_agent

# Strands Agent 직접 호출
response = keyword_extractor_agent.run(
    "다음 리뷰에서 키워드를 추출해주세요: '핏이 좋고 발림성도 만족해요'"
)
```

### 도구 직접 사용

```python
from keyword_extractor.tools import extract_keywords, upsert_review, search_reviews_by_keyword

# 키워드 추출
keywords = extract_keywords("핏이 좋아요")
# 결과: {"keywords": ["핏"]}

# 리뷰와 키워드 저장
upsert_review(123, "핏이 좋아요", keywords["keywords"])

# 키워드로 리뷰 검색
results = search_reviews_by_keyword("핏")
# 결과: [{"review_id": 123, "text": "핏이 좋아요"}]
```

## API 참조

### extract_keywords(review: str) -> dict

리뷰 텍스트에서 1-5개의 키워드를 추출합니다.

**매개변수:**
- `review` (str): 키워드를 추출할 리뷰 텍스트

**반환값:**
```json
{
    "keywords": ["키워드1", "키워드2", "키워드3"]
}
```

### upsert_review(review_id: int, text: str, keywords: list[str]) -> None

리뷰와 키워드를 데이터베이스에 저장하거나 업데이트합니다.

**매개변수:**
- `review_id` (int): 리뷰의 고유 식별자
- `text` (str): 리뷰 텍스트 내용
- `keywords` (list[str]): 리뷰와 연관된 키워드 목록

### search_reviews_by_keyword(keyword: str) -> list[dict]

키워드로 리뷰를 검색합니다.

**매개변수:**
- `keyword` (str): 검색할 키워드

**반환값:**
```json
[
    {
        "review_id": 123,
        "text": "리뷰 텍스트"
    }
]
```

## 데이터베이스 스키마

```sql
-- 리뷰 테이블
CREATE TABLE reviews (
    id INTEGER PRIMARY KEY,
    text TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 키워드 테이블
CREATE TABLE keywords (
    id INTEGER PRIMARY KEY,
    keyword TEXT UNIQUE NOT NULL
);

-- 리뷰-키워드 관계 테이블
CREATE TABLE review_keywords (
    review_id TEXT,
    keyword_id INTEGER,
    PRIMARY KEY (review_id, keyword_id),
    FOREIGN KEY (review_id) REFERENCES reviews(id),
    FOREIGN KEY (keyword_id) REFERENCES keywords(id)
);
```

## 특징

- **한국어 구어체 지원**: "핏이 미친듯", "발림성 개좋고" 등의 표현에서 핵심 키워드 추출
- **제품 특성 우선순위**: 핏, 발림성, 색상, 질감 등 제품 관련 용어를 우선적으로 추출
- **감정 표현 제외**: 좋다, 나쁘다, 만족 등의 감정 표현은 키워드에서 제외
- **중복 방지**: INSERT OR IGNORE를 사용하여 키워드 중복 방지
- **트랜잭션 지원**: 데이터 일관성을 위한 트랜잭션 처리