# 설계 문서

## 개요

감정 분석기는 한국어 리뷰 감정 분석을 위해 설계된 하이브리드 Strands 에이전트입니다. review_moderator와 정확히 동일한 간단한 구조를 따르며, 두 개의 파일(agent.py와 tools.py)만 사용하고, Claude 3.7을 주요 분석 엔진으로 사용하며, 신뢰도가 낮을 때 한국어 슬랭 사전으로 폴백합니다. 시스템은 한국어 전자상거래 리뷰에 대한 정확한 감정 분류를 제공하기 위해 라우트 추적과 함께 2단계 분석 접근법을 구현합니다.

## 아키텍처

### 시스템 구성요소

감정 분석기는 검증된 review_moderator 아키텍처 패턴을 따릅니다:

```
sentiment_analyzer/
├── agent.py          # 메인 에이전트 로직 및 오케스트레이션
└── tools.py          # 도구 구현 (llm_sentiment, dict_sentiment)
```

### 분석 흐름

1. **주요 분석 (LLM 라우트)**
   - Claude 3.7이 한국어 리뷰 텍스트를 분석
   - 신뢰도 점수와 함께 구조화된 감정을 반환
   - 라우트: "llm"

2. **하이브리드 결정 로직**
   - LLM 신뢰도 < 0.6 또는 라벨 == "NEU"인 경우
   - 사전 기반 재분석 트리거
   - 라우트: "llm→dict"

3. **폴백 분석 (사전 라우트)**
   - LLM이 완전히 실패했을 때
   - 순수 사전 기반 분석
   - 라우트: "dict_fallback"

### 통합 패턴

에이전트는 review_moderator에서 확립된 정확한 Strands 통합 패턴을 따릅니다:
- Claude 3.7 모델과 동일한 Agent() 초기화
- 동일한 시스템 프롬프트 구조 및 세부 수준
- 여러 폴백 전략을 가진 동일한 JSON 응답 파싱
- JSON 파싱 실패 시 동일한 수동 실행 패턴
- 동일한 오류 처리 및 구조화된 응답 형식

## 구성요소 및 인터페이스

### 에이전트 구성요소 (agent.py)

**sentiment_analysis_agent**: 메인 Strands 에이전트 인스턴스
- 모델: "us.anthropic.claude-3-7-sonnet-20250219-v1:0" (review_moderator와 동일)
- 도구: [llm_sentiment, dict_sentiment]
- 시스템 프롬프트: 상세한 한국어 감정 분석 지침

**analyze_review()**: 메인 분석 함수
- 입력: review_content (str)
- 출력: 라우트 추적이 포함된 구조화된 감정 결과
- 패턴: moderate_review() 구조와 동일

**generate_confidence_explanation()**: 헬퍼 함수
- 신뢰도 점수 및 라우트 결정 설명
- 패턴: review_moderator의 generate_error_messages()와 유사

### 도구 구성요소 (tools.py)

**@tool llm_sentiment(content: str)**: 주요 LLM 기반 분석
- Bedrock API를 통한 Claude 3.7 사용 (check_profanity와 동일한 패턴)
- 반환: {"label": str, "score": float, "rationale": str}
- 폴백: API 실패 시 사전 분석

**@tool dict_sentiment(content: str)**: 사전 기반 분석
- 내장된 한국어 슬랭 사전 (외부 파일 없음)
- 가중치 점수 시스템 (review_moderator의 severity_score와 유사)
- 반환: llm_sentiment와 동일한 스키마

### 한국어 슬랭 사전

모든 로직을 두 파일에 포함하는 review_moderator 패턴을 따라 tools.py에 직접 내장:

**긍정 표현**:
- 슬랭: "존나", "개쩐다", "갓", "레전드", "대박", "킹왕짱", "개꿀", "존맛", "쩐다"
- 이모티콘: "ㅋㅋ", "ㅎㅎ"
- 가중치: 강도에 따라 +2 ~ +5

**부정 표현**:
- 슬랭: "개별로", "노답", "쓰레기", "최악", "헬게이트", "망함", "별로"
- 이모티콘: "ㅠㅠ", "ㅜㅜ"
- 가중치: 강도에 따라 -2 ~ -5

**점수 알고리즘**:
- 감지된 표현들의 가중합
- 0.0-1.0 범위로 정규화
- 임계값 기반 라벨 할당 (POS/NEG/NEU)

## 데이터 모델

### 입력 스키마
```python
{
    "review_content": str  # 분석할 한국어 리뷰 텍스트
}
```

### 출력 스키마
```python
{
    "success": bool,
    "sentiment_result": {
        "label": str,           # "POS", "NEG", "NEU"
        "score": float,         # 0.0-1.0 신뢰도
        "rationale": str,       # 분석 설명
        "route": str,           # "llm", "llm→dict", "dict_fallback"
        "llm_result": dict,     # 원본 LLM 분석 (해당하는 경우)
        "dict_result": dict,    # 사전 분석 (해당하는 경우)
        "confidence_explanation": str
    },
    "raw_response": str  # 디버깅용 (review_moderator와 동일)
}
```

### 도구 응답 스키마
```python
{
    "label": str,      # "POS", "NEG", "NEU"
    "score": float,    # 0.0-1.0
    "rationale": str   # 분석 설명
}
```

## 오류 처리

review_moderator의 정확한 오류 처리 패턴을 따름:

### JSON 파싱 전략
1. **방법 1**: ```json 블록에서 추출
2. **방법 2**: 마지막 완전한 JSON 객체 찾기
3. **방법 3**: 첫 번째 완전한 JSON 객체 찾기
4. **폴백**: 수동 도구 실행

### API 실패 처리
- **LLM 도구 실패**: dict_sentiment로 자동 폴백
- **완전한 시스템 실패**: dict_fallback 라우트와 함께 구조화된 오류 반환
- **타임아웃 처리**: 10초 제한 (review_moderator와 동일)

### 오류 응답 구조
```python
{
    "success": False,
    "error": str,
    "sentiment_result": {
        "label": "NEU",
        "score": 0.0,
        "rationale": "시스템 오류 발생",
        "route": "error",
        "confidence_explanation": "시스템 오류로 인한 분석 실패"
    }
}
```

## 테스트 전략

### 테스트 구조
review_moderator의 __main__ 섹션 패턴을 따름:

```python
if __name__ == "__main__":
    test_cases = [
        # 긍정적인 한국어 슬랭
        {"review_content": "이거 존나 좋네요! 대박이에요!", "expected": "POS"},
        
        # 부정적인 한국어 슬랭  
        {"review_content": "개별로네요. 완전 쓰레기", "expected": "NEG"},
        
        # 혼합/중립
        {"review_content": "그냥 보통이에요", "expected": "NEU"},
        
        # 엣지 케이스
        {"review_content": "", "expected": "NEU"},
        {"review_content": "ㅋㅋㅋㅋ", "expected": "POS"}
    ]
```

### 테스트 검증
- **라우트 추적**: 올바른 라우트 할당 확인
- **하이브리드 로직**: LLM→dict 전환 테스트
- **한국어 정확도**: 슬랭 감지 검증
- **오류 시나리오**: 우아한 성능 저하 테스트
- **성능**: 10초 완료 보장

### 통합 테스트
- **API 연결성**: Bedrock Claude 3.7 접근
- **폴백 메커니즘**: 사전 전용 작업
- **오류 복구**: 시스템 복원력 테스트

## 설계 결정 및 근거

### 1. 정확한 review_moderator 패턴
**결정**: 동일한 파일 구조 및 코드 패턴 사용
**근거**: 검증된 신뢰성, 일관된 코드베이스, 쉬운 유지보수

### 2. 주요 엔진으로서의 Claude 3.7
**결정**: review_moderator 이미지 분석과 동일한 모델
**근거**: 일관된 성능, 확립된 API 패턴, 한국어 언어 능력

### 3. 내장 사전 접근법
**결정**: 슬랭 사전을 tools.py에 직접 포함
**근거**: review_moderator의 자체 포함 패턴을 따름, 외부 종속성 없음

### 4. 하이브리드 임계값 (τ = 0.6)
**결정**: LLM 신뢰도 < 0.6 또는 라벨 == "NEU"일 때 사전 분석 트리거
**근거**: 엣지 케이스에 대한 LLM 정확도와 사전 커버리지 간의 균형

### 5. 라우트 추적
**결정**: 모든 응답에 라우트 정보 포함
**근거**: 디버깅 능력, 성능 모니터링, 품질 보증

### 6. 가중치 점수 시스템
**결정**: 슬랭 표현에 대한 강도 기반 가중치 사용
**근거**: 이진 감지보다 더 세밀한 분석, review_moderator의 severity_score와 유사

### 7. 동일한 JSON 파싱 전략
**결정**: review_moderator와 동일한 다중 방법 JSON 추출
**근거**: Claude 응답 변화에 대한 검증된 견고성

### 8. 10초 성능 목표
**결정**: review_moderator와 동일한 타임아웃
**근거**: 일관된 사용자 경험, 확립된 성능 기준

이 설계는 검증된 하이브리드 접근법을 통해 전문화된 한국어 감정 분석 기능을 제공하면서 감정 분석기가 기존 시스템과 원활하게 통합되도록 보장합니다.