# Implementation Plan

- [x] 1. Set up project structure and database schema
  - Create agents/keyword_extractor directory structure with __init__.py, agent.py, tools.py, prompts.py
  - Implement SQLite database schema with reviews, keywords, and review_keywords tables
  - Create database initialization and connection utilities
  - _Requirements: 3.4, 2.5_

- [x] 2. Implement core agent class and Strands SDK integration
  - Create KeywordExtractorAgent class inheriting from Strands Agent base
  - Set up agent configuration and initialization
  - Register the three required tools with proper signatures
  - _Requirements: 3.2, 3.4_

- [x] 3. Implement keyword extraction functionality
  - [x] 3.1 Create Claude 3.7 integration for keyword extraction
    - Set up Bedrock client connection
    - Implement LLM prompt for Korean colloquial expression handling
    - Create extract_keywords tool that returns 1-5 keywords in JSON format
    - _Requirements: 1.1, 1.2, 1.4_

  - [x] 3.2 Add product-specific term prioritization logic
    - Enhance prompt to prioritize product-related keywords (핏, 발림성, 색상, etc.)
    - Test extraction with colloquial expressions like "핏이 미친듯", "발림성 개좋고"
    - Validate output format matches {"keywords": ["keyword1", "keyword2", ...]}
    - _Requirements: 1.3, 1.4_

- [x] 4. Implement review and keyword storage
  - [x] 4.1 Create upsert_review tool implementation
    - Implement INSERT OR REPLACE logic for reviews table
    - Add INSERT OR IGNORE logic for keywords table to prevent duplicates
    - Create many-to-many relationship management for review_keywords table
    - _Requirements: 2.2, 2.5, 3.1_

  - [x] 4.2 Add database transaction handling
    - Wrap upsert operations in database transactions
    - Ensure data consistency across all three tables
    - Test rollback behavior on failures
    - _Requirements: 3.3_

- [x] 5. Implement keyword-based search functionality
  - Create search_reviews_by_keyword tool implementation
  - Join keywords and review_keywords tables to find matching reviews
  - Return results with review_id and text fields only
  - Sort results by creation date (newest first)
  - _Requirements: 2.1, 2.3, 2.4_

- [ ] 6. Create comprehensive test suite
  - [ ] 6.1 Write unit tests for keyword extraction
    - Test Korean colloquial expression handling
    - Verify 1-5 keyword limit enforcement
    - Test product-specific term prioritization
    - _Requirements: 1.1, 1.2, 1.3_

  - [ ] 6.2 Write integration tests for database operations
    - Test upsert_review with various keyword combinations
    - Verify duplicate keyword prevention
    - Test search functionality with multiple reviews
    - _Requirements: 2.2, 2.5_

  - [ ] 6.3 Write API compatibility tests
    - Verify tool signatures match requirements exactly
    - Test JSON input/output formats
    - Ensure drop-in replacement compatibility
    - _Requirements: 3.2, 3.4_

- [x] 7. Integration and deployment preparation
  - Create agent registration and configuration files
  - Test complete workflow: extract → upsert → search
  - Verify API contract compliance with existing systems
  - Document usage examples and integration steps
  - _Requirements: 3.1, 3.2_