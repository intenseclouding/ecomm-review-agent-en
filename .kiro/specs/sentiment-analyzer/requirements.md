# Requirements Document

## Introduction

한국어 리뷰 감정 분석을 위한 하이브리드 Strands 에이전트를 개발합니다. review_moderator와 동일한 간단한 구조로, Claude 3.7을 주 분석 엔진으로 사용하고 신뢰도가 낮을 때 한국어 신조어 사전으로 보완하는 2단계 시스템입니다. agent.py와 tools.py 두 파일만으로 구현합니다.

## Requirements

### Requirement 1

**User Story:** As a sentiment analysis system, I want to implement llm_sentiment and dict_sentiment tools with the same simple structure as review_moderator, so that I can provide accurate Korean sentiment analysis with minimal code complexity.

#### Acceptance Criteria

1. WHEN implementing llm_sentiment tool THEN the system SHALL call Claude 3.7 and return {"label": str, "score": float, "rationale": str}
2. WHEN implementing dict_sentiment tool THEN the system SHALL use Korean slang dictionary and return the same schema
3. WHEN implementing analyze_review function THEN the system SHALL follow review_moderator pattern with agent.py and tools.py only
4. WHEN LLM score < 0.6 OR label == "NEU" THEN the system SHALL call dict_sentiment for correction
5. WHEN returning results THEN the system SHALL include route: "llm" | "llm→dict" | "dict_fallback"

### Requirement 2

**User Story:** As a developer, I want the same file structure as review_moderator (agent.py + tools.py), so that the codebase is consistent and easy to maintain.

#### Acceptance Criteria

1. WHEN creating the agent THEN the system SHALL have only agent.py and tools.py files like review_moderator
2. WHEN defining tools THEN the system SHALL use @tool decorators for llm_sentiment, dict_sentiment functions
3. WHEN creating the main function THEN the system SHALL follow analyze_review pattern like moderate_review
4. WHEN handling errors THEN the system SHALL use the same try/catch pattern as review_moderator
5. WHEN testing THEN the system SHALL include __main__ section with test cases like review_moderator

### Requirement 3

**User Story:** As a Korean language specialist, I want comprehensive slang dictionary embedded in tools.py, so that the system can handle Korean expressions without external files.

#### Acceptance Criteria

1. WHEN defining positive expressions THEN the system SHALL include "존나", "개쩐다", "갓", "레전드", "대박", "킹왕짱", "개꿀", "존맛", "쩐다"
2. WHEN defining negative expressions THEN the system SHALL include "개별로", "노답", "쓰레기", "최악", "헬게이트", "망함", "별로"
3. WHEN defining emoticons THEN the system SHALL include "ㅋㅋ", "ㅎㅎ" (positive), "ㅠㅠ", "ㅜㅜ" (negative)
4. WHEN calculating scores THEN the system SHALL use weighted scoring like review_moderator's severity_score
5. WHEN dictionary is inconclusive THEN the system SHALL return original LLM result

### Requirement 4

**User Story:** As a system integrator, I want the agent to follow exact Strands patterns from review_moderator, so that it integrates seamlessly with existing infrastructure.

#### Acceptance Criteria

1. WHEN creating the agent THEN the system SHALL use same Agent() initialization pattern as review_moderation_agent
2. WHEN defining system prompt THEN the system SHALL follow the same detailed prompt structure as review_moderator
3. WHEN handling JSON responses THEN the system SHALL use the same parsing logic as review_moderator
4. WHEN implementing fallback THEN the system SHALL use the same manual execution pattern when JSON parsing fails
5. WHEN returning results THEN the system SHALL use the same success/error structure as moderate_review

### Requirement 5

**User Story:** As a performance engineer, I want efficient processing with the same reliability as review_moderator, so that the system provides consistent results within acceptable time limits.

#### Acceptance Criteria

1. WHEN processing reviews THEN the system SHALL complete analysis within 10 seconds like review_moderator
2. WHEN LLM fails THEN the system SHALL fallback to dictionary-only analysis like review_moderator's manual execution
3. WHEN threshold τ = 0.6 is not met THEN the system SHALL trigger dictionary re-analysis
4. WHEN dictionary suggests strong sentiment THEN the system SHALL override LLM result with confidence adjustment
5. WHEN system errors occur THEN the system SHALL return structured error response like review_moderator

### Requirement 6

**User Story:** As a quality assurance tester, I want the same testing approach as review_moderator, so that I can validate the system using familiar patterns and test cases.

#### Acceptance Criteria

1. WHEN testing the system THEN the system SHALL include __main__ section with test_cases array like review_moderator
2. WHEN testing hybrid logic THEN the system SHALL verify route tracking ("llm" vs "llm→dict") in test results
3. WHEN testing Korean expressions THEN the system SHALL achieve reasonable accuracy on positive/negative slang
4. WHEN testing edge cases THEN the system SHALL handle empty input, encoding issues like review_moderator
5. WHEN testing error scenarios THEN the system SHALL gracefully degrade to fallback methods like review_moderator