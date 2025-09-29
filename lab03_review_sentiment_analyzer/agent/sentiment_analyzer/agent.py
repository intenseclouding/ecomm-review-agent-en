from strands import Agent

# 감정 분석 Agent 생성
sentiment_agent = Agent(
    model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    system_prompt=(
        "당신은 리뷰 감정 분석 전문가입니다.\n"
        "리뷰 텍스트를 분석하여 감정을 분류하고 점수를 매깁니다.\n\n"
        "감정 분류:\n"
        "- positive: 긍정적 감정 (만족, 기쁨, 추천 등)\n"
        "- negative: 부정적 감정 (불만, 실망, 비추천 등)\n"
        "- neutral: 중립적 감정 (객관적 서술, 단순 정보 등)\n\n"
        "감정 점수: -1.0 (매우 부정) ~ 1.0 (매우 긍정)\n\n"
        # 주의사항 (optional):
        # "- 반어법, 비꼬는 표현('정말 좋네요' + 부정적 맥락)을 주의깊게 감지하세요\n"
        # "- 복합 감정이 있는 경우 전체적인 주된 감정을 파악하세요\n"
        # "- 한국어 완곡 표현을 고려하세요: '나쁘지 않다'는 긍정적, '그럭저럭'은 보통 만족\n"
        # "- 도메인별 전문용어의 맥락을 파악하세요 (예: 게임의 '어려움'은 긍정적일 수 있음)\n"
        # "- 비교 표현('~보다 나아요')의 상대적 의미를 고려하세요\n"
        # "- 텍스트가 너무 짧거나 모호한 경우 confidence를 낮게 설정하세요\n\n"

        "결과를 JSON 형식으로 반환하세요:\n"
        "{\n"
        "  \"sentiment\": \"positive|negative|neutral\",\n"
        "  \"score\": 0.8,\n"
        "  \"confidence\": 0.9,\n"
        "  \"reason\": \"분석 근거\"\n"
        "}"
    )
)

def analyze_sentiment(review_content: str) -> dict:
    """
    리뷰 텍스트의 감정을 분석하는 메인 함수 (Strands Agent 사용)

    Args:
        review_content (str): 분석할 리뷰 텍스트

    Returns:
        dict: 감정 분석 결과
    """
    try:
        # Strands Agent 호출
        agent_response = sentiment_agent(review_content)

        # Agent 응답 파싱
        if isinstance(agent_response, str):
            # JSON 응답 파싱
            import json
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
            # AgentResult 객체를 문자열로 변환 후 JSON 파싱
            agent_response_str = str(agent_response)
            import json
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
            "sentiment_result": result,
            "raw_response": str(agent_response)
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "sentiment_result": {
                "sentiment": "neutral",
                "score": 0.5,
                "confidence": 0.3,
                "reason": f"분석 중 오류 발생: {str(e)}"
            }
        }
