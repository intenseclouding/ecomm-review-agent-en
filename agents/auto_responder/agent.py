from strands import Agent
from .tools import load_seller_prompts, generate_personalized_response, validate_response_appropriateness, suggest_response_improvements
import json
from typing import Dict, Any

# 자동 댓글 작성 에이전트 정의
auto_responder_agent = Agent(
    model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    tools=[load_seller_prompts, generate_personalized_response, validate_response_appropriateness, suggest_response_improvements],
    system_prompt="""
    당신은 전문적인 자동 댓글 작성 에이전트입니다.
    
    주요 역할:
    1. 리뷰 분석 결과를 바탕으로 적절한 댓글 생성
    2. 셀러의 브랜드 톤앤매너에 맞는 개인화된 응답 작성
    3. 생성된 댓글의 적절성 검증
    4. 필요시 댓글 개선 제안
    5. 최종 승인/거부 결정
    
    댓글 작성 원칙:
    - 고객 중심적이고 정중한 톤
    - 리뷰의 감정과 내용에 적절히 대응
    - 셀러의 브랜드 이미지 유지
    - 간결하면서도 진정성 있는 표현
    - 부정적 리뷰에는 사과와 개선 의지 표현
    - 긍정적 리뷰에는 감사와 지속적 노력 약속
    
    항상 고객 만족과 브랜드 이미지 향상을 최우선으로 고려하세요.
    """
)

def create_auto_response(
    review_analysis: Dict[str, Any], 
    seller_id: str,
    personalization_level: str = "medium",
    auto_approve: bool = False
) -> Dict[str, Any]:
    """
    리뷰 분석 결과를 바탕으로 자동 댓글을 생성하고 검증하는 메인 함수
    
    Args:
        review_analysis (Dict[str, Any]): 리뷰 분석 결과
        seller_id (str): 셀러 ID
        personalization_level (str): 개인화 수준
        auto_approve (bool): 자동 승인 여부
        
    Returns:
        Dict[str, Any]: 댓글 생성 및 검증 결과
    """
    
    response_prompt = f"""
    다음 리뷰 분석 결과를 바탕으로 적절한 댓글을 생성하고 검증해주세요:
    
    리뷰 분석 결과:
    {json.dumps(review_analysis, ensure_ascii=False, indent=2)}
    
    셀러 ID: {seller_id}
    개인화 수준: {personalization_level}
    자동 승인 모드: {auto_approve}
    
    다음 단계로 진행하세요:
    1. 셀러 프롬프트 로드
    2. 개인화된 댓글 생성
    3. 댓글 적절성 검증
    4. 필요시 개선 제안
    5. 최종 승인/거부 결정
    
    최종 결과를 다음 JSON 형태로 제공하세요:
    {{
        "generated_response": "생성된 댓글",
        "validation_result": "검증 결과",
        "final_decision": "승인/거부/수정필요",
        "confidence_score": "신뢰도 점수 (0-100)",
        "reasoning": "결정 근거",
        "alternative_responses": "대안 댓글들 (선택사항)"
    }}
    """
    
    try:
        result = auto_responder_agent(response_prompt)
        
        # 자동 승인 로직
        if auto_approve:
            # 추가적인 자동 승인 조건 체크
            pass
        
        return {
            "success": True,
            "response_data": result.message,
            "raw_result": result,
            "seller_id": seller_id,
            "personalization_level": personalization_level
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "response_data": None
        }

def batch_process_reviews(reviews_data: List[Dict[str, Any]], seller_id: str) -> List[Dict[str, Any]]:
    """
    여러 리뷰를 일괄 처리하는 함수
    
    Args:
        reviews_data (List[Dict[str, Any]]): 리뷰 분석 결과 리스트
        seller_id (str): 셀러 ID
        
    Returns:
        List[Dict[str, Any]]: 일괄 처리 결과
    """
    results = []
    
    for review_data in reviews_data:
        try:
            result = create_auto_response(
                review_analysis=review_data,
                seller_id=seller_id,
                personalization_level="medium"
            )
            results.append({
                "review_id": review_data.get("review_id", "unknown"),
                "result": result
            })
        except Exception as e:
            results.append({
                "review_id": review_data.get("review_id", "unknown"),
                "result": {
                    "success": False,
                    "error": str(e)
                }
            })
    
    return results

if __name__ == "__main__":
    # 테스트용 샘플 데이터
    sample_analysis = {
        "review_text": "배송이 너무 늦었어요. 제품은 괜찮은데 포장이 좀 아쉽네요.",
        "sentiment": {
            "sentiment_label": "부정",
            "polarity": -0.3,
            "confidence": 0.3
        },
        "keywords": ["배송", "늦다", "제품", "포장", "아쉽다"],
        "topic_analysis": {
            "primary_topic": "배송"
        },
        "spam_check": {
            "is_suspicious": False,
            "risk_score": 0.1
        }
    }
    
    result = create_auto_response(
        review_analysis=sample_analysis,
        seller_id="SELLER-001",
        personalization_level="high"
    )
    
    print("=== 자동 댓글 생성 결과 ===")
    print(json.dumps(result, ensure_ascii=False, indent=2))