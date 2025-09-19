# Requirements Document

## Introduction

이 문서는 리뷰 텍스트에서 핵심 키워드를 추출하고 키워드 기반 검색 기능을 제공하는 키워드 추출 및 검색 시스템의 요구사항을 정의합니다. 이 시스템은 고객이 궁금해할 만한 핵심 키워드를 자동으로 추출하고, 추출된 키워드를 통해 관련 리뷰를 빠르게 검색할 수 있는 기능을 제공합니다.

**기술적 제약사항:**
- Strands Agent SDK(Python)로 구현
- Claude 3.7(Bedrock)을 추출 엔진으로 사용
- 저장소는 SQLite 사용
- 기존 시스템의 API 계약(엔드포인트·요청/응답 JSON)을 변경 없이 유지 (드롭인 교체)

## Requirements

### Requirement 1

**User Story:** As a system administrator, I want the system to automatically extract 1-5 relevant keywords from review text, so that customers can quickly find reviews about specific product features.

#### Acceptance Criteria

1. WHEN a review text is provided THEN the system SHALL return 1-5 keywords in JSON format
2. WHEN the review contains colloquial expressions like "핏이 미친듯" or "발림성 개좋고" THEN the system SHALL extract only the core keywords like "핏" and "발림성"
3. WHEN the review contains product-specific terms THEN the system SHALL prioritize those terms in extraction
5. WHEN keywords are extracted THEN the output format SHALL be {"keywords": ["keyword1", "keyword2", ...]}

### Requirement 2

**User Story:** As a customer, I want to search reviews by keywords, so that I can quickly find reviews mentioning specific product aspects I'm interested in.

#### Acceptance Criteria

1. WHEN a keyword is provided for search THEN the system SHALL return a list of reviews containing that keyword
2. WHEN storing keywords THEN the system SHALL prevent duplicate keyword insertion using INSERT OR IGNORE
3. WHEN returning search results THEN the response SHALL include review_id and text fields
4. WHEN no specific sorting is requested THEN the system SHALL return results sorted by creation date (newest first)
5. WHEN storing review-keyword relationships THEN the system SHALL use a many-to-many relationship structure

### Requirement 3

**User Story:** As a developer, I want the new keyword extraction system to integrate seamlessly with existing review pipeline, so that I can replace the current system without changing API contracts.

#### Acceptance Criteria

1. WHEN a new review is created THEN the system SHALL automatically generate and store keywords
2. WHEN the existing system calls are replaced with the new agent THEN the system SHALL work without endpoint or schema changes
3. WHEN integrating with existing systems THEN the process SHALL maintain data consistency
4. WHEN the agent is deployed THEN it SHALL provide the following tool signatures:
   - extract_keywords(review:str)->dict
   - upsert_review(review_id:int, text:str, keywords:list[str])->None
   - search_reviews_by_keyword(keyword:str)->list[dict]

**Database Schema Requirements:**
- reviews(id PK, text, created_at)
- keywords(id PK, keyword UNIQUE)
- review_keywords(review_id, keyword_id, PK(review_id,keyword_id))

**Out of Scope:**
- 감정 태깅/점수화 (Sentiment tagging/scoring)
- 다중 키워드 AND/OR 고급 검색 (Advanced multi-keyword search)
- UI 하이라이트 스펙 (UI highlighting specifications)