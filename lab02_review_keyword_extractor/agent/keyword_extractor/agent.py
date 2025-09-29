from strands import Agent
import json

from agent.keyword_extractor.tools import get_all_keywords

# 키워드 매칭 Agent
keyword_agent = Agent(
    model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    tools=[get_all_keywords],
    system_prompt="""
    당신은 키워드 기반 리뷰 분석 전문가입니다.

    ## 핵심 역할:
    - 리뷰 텍스트에서 한국어 특성과 문맥을 고려해 의미있는 키워드를 정확하게 추출
    - 등록된 키워드와의 정밀한 매칭

    ## 작업 프로세스:
    1. **등록된 키워드 조회**: get_all_keywords 도구를 사용하여 등록된 키워드 목록 획득
    2. **리뷰 텍스트 분석**: 등록된 키워드를 참고하여 리뷰에서 관련 키워드와 구문 식별
    3. **매칭 수행**:
       - 완전 일치 우선
       - 부분 일치 및 유사어 고려
       - 의미론적 유사어 고려

    ## 응답 형식:
    {
        "matched_keywords": [
            {
                "keyword": "매칭된 키워드",
                "match_type": "exact|partial|semantic",
                "original_phrase": "리뷰에서 발견된 원본 구문"
            }
        ]
    }

    ## 주의사항:
    - 한국어 특성 (조사, 어미 변화) 고려하여 매칭
    - 부정문에서 사용된 키워드도 포함하되 구분하여 처리
    - 중복 키워드는 제거하고 최적의 매칭만 유지
    - 응답은 반드시 유효한 JSON 형식만 제공하고 다른 설명이나 텍스트는 포함하지 마세요
    """
)

def search_keywords(review_text: str) -> dict:
   
    # Agent 실행
    agent_response = keyword_agent(f"""
    리뷰: {review_text}

위 리뷰에서 등록된 키워드와 매칭되는 내용을 찾아주세요.

중요: 응답은 오직 JSON 형식만 제공하고, 다른 설명이나 텍스트는 일체 포함하지 마세요.
    """)


    # Agent 응답 파싱 (문자열 응답에서 JSON 추출)
    try:
        if isinstance(agent_response, str):
            # JSON 응답 파싱
            if "```json" in agent_response:
                json_start = agent_response.find("```json") + 7
                json_end = agent_response.find("```", json_start)
                json_text = agent_response[json_start:json_end].strip()
            elif "{" in agent_response and "}" in agent_response:
                json_start = agent_response.find("{")
                json_end = agent_response.rfind("}") + 1
                json_text = agent_response[json_start:json_end]
            else:
                raise ValueError("JSON 형태를 찾을 수 없습니다.")

            result = json.loads(json_text)
        else:
            # AgentResult 객체 처리
            agent_response_str = str(agent_response)
            if "```json" in agent_response_str:
                json_start = agent_response_str.find("```json") + 7
                json_end = agent_response_str.find("```", json_start)
                json_text = agent_response_str[json_start:json_end].strip()
            elif "{" in agent_response_str and "}" in agent_response_str:
                json_start = agent_response_str.find("{")
                json_end = agent_response_str.rfind("}") + 1
                json_text = agent_response_str[json_start:json_end]
            else:
                raise ValueError("AgentResult에서 JSON 형태를 찾을 수 없습니다.")

            result = json.loads(json_text)

        return {
            "success": True,
            "analysis_result": result,
            "raw_response": str(agent_response)
        }

    except (json.JSONDecodeError, ValueError) as e:
        return {
            "success": False,
            "error": f"Agent 응답 파싱 실패: {str(e)}",
            "raw_response": str(agent_response)
        }