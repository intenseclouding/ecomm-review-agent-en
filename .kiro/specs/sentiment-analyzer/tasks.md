# Implementation Plan

- [x] 1. Create basic agent structure following review_moderator pattern
  - Create agents/sentiment_analyzer directory with only agent.py and tools.py files
  - Implement Agent() initialization identical to review_moderation_agent pattern
  - Set up Claude 3.7 model connection using same model ID as review_moderator
  - Create basic __init__.py file for module structure
  - _Requirements: 2.1, 2.2, 4.1, 4.2_

- [x] 2. Implement llm_sentiment tool with streamlined Claude 3.7 integration
  - Create @tool decorated llm_sentiment function in tools.py
  - Implement Korean-specific sentiment analysis prompt with forced single-line JSON response
  - Add Bedrock API integration using same pattern as check_profanity tool
  - Implement single robust JSON parser: normal parsing → regex JSON capture → json.loads()
  - Return structured response: {"label": str, "score": float, "rationale": str}
  - _Requirements: 1.1, 1.2, 4.3, 4.4_

- [x] 2.1 Create __init__.py file for proper module structure
  - Add empty __init__.py file in agents/sentiment_analyzer directory
  - _Requirements: 2.1_

- [x] 3. Implement simplified dict_sentiment tool with refined Korean slang dictionary
  - Create @tool decorated dict_sentiment function in tools.py
  - Embed hardcoded Korean slang dictionary directly in tools.py (no external files)
  - Include positive phrase patterns: "인생템", "핏이 미친", "발림성 개좋고", "개쩐다", "갓", "레전드", "대박", "개꿀", "존좋", "쩐다"
  - Include negative expressions: "뒤집어짐", "노답", "구리다", "실밥천국", "헬게이트", "망함", "별로"
  - Move "미쳤다" to ambiguous category with context correction (맛/핏/서비스=positive, 환불/실망=negative)
  - Add simple normalization function (lowercase, consecutive space cleanup)
  - Include emoticons: "ㅋㅋ", "ㅎㅎ" (positive), "ㅠㅠ", "ㅜㅜ" (negative)
  - _Requirements: 3.1, 3.2, 3.3, 3.4_

- [x] 4. Implement analyze_review main function with hybrid routing logic
  - Update analyze_review function in agent.py to follow exact review_moderator pattern
  - Implement minimal Korean sentiment prompt (8-12 lines) for JSON stability instead of detailed prompt
  - Add core hybrid logic: LLM → (score < 0.6 OR label == "NEU") → dict re-analysis
  - Include route tracking: "llm", "llm→dict", "dict_fallback"
  - Add basic try/except with NEU + error message return on timeout/exceptions
  - _Requirements: 1.4, 2.3, 4.4, 5.5_

- [x] 5. Implement streamlined JSON parsing and fallback
  - Update JSON parsing to match review_moderator's exact multi-method strategy
  - Implement immediate dict_sentiment fallback on parsing failure OR timeout
  - No retry loops after fallback - finalize result immediately (prevent loops)
  - Set LLM timeout to 5 seconds with immediate dictionary fallback
  - Ensure all routes return consistent schema: {"label","score","rationale","route"}
  - Route values: "llm" | "llm→dict" | "dict_fallback" (for errors)
  - Include raw_response field as debug option only (default disabled)
  - _Requirements: 4.4, 4.5, 5.1, 5.2, 5.4_

- [x] 6. Implement focused testing with 10-15 core cases
  - Update __main__ section with test_cases array like review_moderator
  - Include 4 positive Korean slang test cases
  - Include 4 negative Korean slang test cases  
  - Include 4 ambiguous/mixed content test cases (include "미쳤는데 배터리는 별로" for route transition verification)
  - Include 2 edge cases: empty string (expect NEU + error message), long review
  - Verify route tracking changes (llm vs llm→dict)
  - Skip encoding/performance/bulk testing for MVP
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

- [x] 7. Validate basic system integration and performance
  - Test complete analysis workflow end-to-end once
  - Verify response within 10 seconds (simple check, no strict benchmarking)
  - Test LLM timeout (5s) setting with immediate dictionary fallback
  - Ensure basic Korean slang accuracy
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_