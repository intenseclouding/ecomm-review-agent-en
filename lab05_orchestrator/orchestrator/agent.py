import logging
from typing import Any, Dict, List

from pydantic import BaseModel, Field
from strands import Agent
from strands_tools import editor, file_read, file_write
from sub_agents.review_moderator.agent import moderate_review
from sub_agents.keyword_extractor.agent import extract_keywords
from sub_agents.sentiment_analyzer.agent import analyze_sentiment

# Configure the root strands logger
logging.getLogger("strands").setLevel(logging.INFO)

# Add a handler to see the logs
logging.basicConfig(
    format="%(levelname)s | %(name)s | %(message)s", 
    handlers=[logging.StreamHandler()]
)

ORCHESTRATOR_PROMPT = """
    당신은 리뷰 분석 워크플로우를 관리하는 오케스트레이터입니다.
    사용자가 입력하는 리뷰 데이터를 기반으로 다음 agent 와 순서를 참고하여 리뷰를 검수하고 분석한 후 자동답글을 생성하세요. 
    
    <작업규칙>
    각 agent의 결과는 반드시 {comment_id}_{agent_name}_{timestamp}.md에 저장합니다.
    </작업규칙>

    <분석용에이전트들>
    활용해야 하는 리뷰 분석 Agent (순서대로 실행):
    1. 리뷰 검수 
    2. 키워드 추출   
    3. 감정 분석 
    4. 자동 응답 생성 
    </분석용에이전트들>

    <작업순서>
    1. 리뷰 검수 후 적격하지 않다고 판단할 경우 이후 단계를 진행하지 않고 종료합니다. 종료 시 부적격 사유를 응답합니다.
    2. 리뷰 검수에서 정상적으로 통과할 경우, 감정 분석과 키워드 추출을 순서대로 진행하고 리뷰를 분석합니다. 
    3. 마지막으로 자동응답 생성을 완료합니다. 
    4. 저장된 md파일들에 대해 모두 종합하여 응답합니다.
    </작업순서>

    """

class KeywordHighlight(BaseModel):
    keyword: str = Field(description="기준 키워드")
    sentences: List[str] = Field(description="키워드에 맞는 문장들")

class ReviewAnalysis(BaseModel):
    """Complete review analysis."""
    moderation_result: Dict[str, Any] = Field(description="리뷰 검수 결과")
    keyword_highlighted_list: List[KeywordHighlight] = Field(description="키워드 분석에서 키워드에 맞는 문장들")
    sentiment: str = Field(description="감정 분석 결과")
    auto_response: str = Field(description="자동 응답 생성 결과")

def comprehensive_analyzer(review_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    리뷰에 대한 자동 응답을 생성하는 메인 함수

    Args:
        review (str): 분석할 리뷰 텍스트

    Returns:
        Dict[str, Any]: 자동 응답 결과
    """

    # 각 요청마다 새로운 Agent 생성
    orchestrator_agent = Agent(
        model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
        tools=[moderate_review, extract_keywords, analyze_sentiment, generate_auto_reponse, file_read, file_write, editor],
        callback_handler=None,
        system_prompt=ORCHESTRATOR_PROMPT
    )

    # 리뷰에 대한 자동 응답 생성
    orchestrator_agent(review_data)
    orchestrator_agent.structured_output(
        ReviewAnalysis,
        "리뷰데이터에 대한 분석 결과를 구조화된 형태로 추출하시오"
    )


