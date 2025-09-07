from strands import tool
import json
import random
from typing import Dict, List, Any, Optional

@tool
def load_seller_prompts(seller_id: str) -> Dict[str, Any]:
    """
    특정 셀러의 자동댓글 프롬프트를 로드합니다.
    
    Args:
        seller_id (str): 셀러 ID
        
    Returns:
        Dict[str, Any]: 셀러의 프롬프트 설정
    """
    try:
        with open('data/seller_prompts.json', 'r', encoding='utf-8') as f:
            all_prompts = json.load(f)
        
        seller_prompts = all_prompts.get(seller_id, all_prompts.get("default", {}))
        
        return {
            "success": True,
            "seller_id": seller_id,
            "prompts": seller_prompts
        }
    except FileNotFoundError:
        # 기본 프롬프트 반환
        return {
            "success": False,
            "seller_id": seller_id,
            "prompts": {
                "positive_response_templates": [
                    "소중한 리뷰 감사합니다! 앞으로도 더 좋은 제품과 서비스로 보답하겠습니다.",
                    "만족스러운 구매 경험을 해주셔서 정말 기쁩니다. 감사합니다!",
                    "좋은 평가 주셔서 감사드립니다. 계속해서 품질 향상에 노력하겠습니다."
                ],
                "negative_response_templates": [
                    "불편을 끼쳐드려 죄송합니다. 개선할 수 있도록 노력하겠습니다.",
                    "소중한 의견 감사합니다. 더 나은 서비스를 위해 참고하겠습니다.",
                    "아쉬운 경험을 하셨군요. 앞으로 더욱 신경 쓰겠습니다."
                ],
                "neutral_response_templates": [
                    "리뷰 작성해주셔서 감사합니다. 더 나은 경험을 위해 노력하겠습니다.",
                    "소중한 의견 감사드립니다. 지속적으로 개선해나가겠습니다."
                ]
            }
        }

@tool
def generate_personalized_response(
    review_analysis: Dict[str, Any], 
    seller_prompts: Dict[str, Any],
    personalization_level: str = "medium"
) -> Dict[str, Any]:
    """
    리뷰 분석 결과와 셀러 프롬프트를 바탕으로 개인화된 댓글을 생성합니다.
    
    Args:
        review_analysis (Dict[str, Any]): 리뷰 분석 결과
        seller_prompts (Dict[str, Any]): 셀러 프롬프트 설정
        personalization_level (str): 개인화 수준 (low, medium, high)
        
    Returns:
        Dict[str, Any]: 생성된 댓글과 메타데이터
    """
    
    # 감정에 따른 템플릿 선택
    sentiment = review_analysis.get("sentiment", {}).get("sentiment_label", "중립")
    
    if sentiment == "긍정":
        templates = seller_prompts.get("positive_response_templates", [])
    elif sentiment == "부정":
        templates = seller_prompts.get("negative_response_templates", [])
    else:
        templates = seller_prompts.get("neutral_response_templates", [])
    
    if not templates:
        templates = ["소중한 리뷰 감사합니다."]
    
    # 기본 템플릿 선택
    base_template = random.choice(templates)
    
    # 개인화 요소 추가
    personalized_response = base_template
    
    if personalization_level in ["medium", "high"]:
        # 주제별 맞춤 멘트 추가
        topic = review_analysis.get("topic_analysis", {}).get("primary_topic", "")
        
        topic_responses = {
            "품질": "제품 품질에 대한 소중한 의견 감사합니다.",
            "배송": "배송 관련 피드백 감사드립니다.",
            "가격": "가격에 대한 의견 잘 참고하겠습니다.",
            "디자인": "디자인에 대한 평가 감사합니다.",
            "사용성": "사용 경험을 공유해주셔서 감사합니다.",
            "서비스": "서비스에 대한 피드백 감사드립니다."
        }
        
        if topic in topic_responses:
            personalized_response += f" {topic_responses[topic]}"
    
    if personalization_level == "high":
        # 키워드 기반 추가 개인화
        keywords = review_analysis.get("keywords", [])
        if keywords:
            key_keyword = keywords[0] if keywords else ""
            if key_keyword:
                personalized_response += f" '{key_keyword}'에 대한 언급 특히 감사드립니다."
    
    return {
        "generated_response": personalized_response,
        "sentiment_matched": sentiment,
        "topic_addressed": review_analysis.get("topic_analysis", {}).get("primary_topic", ""),
        "personalization_level": personalization_level,
        "template_used": base_template
    }

@tool
def validate_response_appropriateness(
    generated_response: str, 
    review_analysis: Dict[str, Any],
    seller_guidelines: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    생성된 댓글이 적절한지 검증합니다.
    
    Args:
        generated_response (str): 생성된 댓글
        review_analysis (Dict[str, Any]): 원본 리뷰 분석 결과
        seller_guidelines (Dict[str, Any]): 셀러 가이드라인
        
    Returns:
        Dict[str, Any]: 검증 결과
    """
    
    issues = []
    score = 100
    
    # 길이 체크
    if len(generated_response) < 10:
        issues.append("댓글이 너무 짧습니다")
        score -= 20
    elif len(generated_response) > 200:
        issues.append("댓글이 너무 깁니다")
        score -= 10
    
    # 부적절한 표현 체크
    inappropriate_words = ["바보", "멍청", "짜증", "화나", "최악"]
    for word in inappropriate_words:
        if word in generated_response:
            issues.append(f"부적절한 표현 포함: {word}")
            score -= 30
    
    # 감정 일치도 체크
    review_sentiment = review_analysis.get("sentiment", {}).get("sentiment_label", "중립")
    
    positive_indicators = ["감사", "기쁘", "만족", "좋", "훌륭"]
    negative_indicators = ["죄송", "미안", "개선", "노력"]
    
    response_sentiment = "중립"
    if any(word in generated_response for word in positive_indicators):
        response_sentiment = "긍정"
    elif any(word in generated_response for word in negative_indicators):
        response_sentiment = "부정"
    
    # 감정 불일치 체크
    if review_sentiment == "부정" and response_sentiment == "긍정":
        issues.append("부정적 리뷰에 부적절한 긍정적 응답")
        score -= 25
    elif review_sentiment == "긍정" and response_sentiment == "부정":
        issues.append("긍정적 리뷰에 부적절한 부정적 응답")
        score -= 15
    
    # 전반적인 평가
    if score >= 80:
        recommendation = "승인"
    elif score >= 60:
        recommendation = "수정 후 승인"
    else:
        recommendation = "재작성 필요"
    
    return {
        "is_appropriate": score >= 60,
        "score": score,
        "issues": issues,
        "recommendation": recommendation,
        "sentiment_match": review_sentiment == response_sentiment or response_sentiment == "중립"
    }

@tool
def suggest_response_improvements(
    generated_response: str,
    validation_result: Dict[str, Any],
    review_analysis: Dict[str, Any]
) -> Dict[str, Any]:
    """
    댓글 개선 제안을 생성합니다.
    
    Args:
        generated_response (str): 원본 생성 댓글
        validation_result (Dict[str, Any]): 검증 결과
        review_analysis (Dict[str, Any]): 리뷰 분석 결과
        
    Returns:
        Dict[str, Any]: 개선 제안
    """
    
    suggestions = []
    improved_response = generated_response
    
    # 검증 결과의 이슈들을 바탕으로 개선 제안
    for issue in validation_result.get("issues", []):
        if "너무 짧습니다" in issue:
            suggestions.append("더 구체적이고 따뜻한 표현을 추가해보세요")
            improved_response += " 고객님의 소중한 의견을 바탕으로 더욱 발전하는 모습 보여드리겠습니다."
        
        elif "너무 깁니다" in issue:
            suggestions.append("더 간결하고 핵심적인 메시지로 줄여보세요")
            # 간단한 버전 제안
            improved_response = "소중한 리뷰 감사합니다. 더 나은 서비스로 보답하겠습니다."
        
        elif "부적절한 표현" in issue:
            suggestions.append("더 정중하고 전문적인 표현으로 수정해보세요")
            # 부적절한 단어 제거 (실제로는 더 정교한 로직 필요)
            inappropriate_words = ["바보", "멍청", "짜증", "화나", "최악"]
            for word in inappropriate_words:
                improved_response = improved_response.replace(word, "")
        
        elif "감정 불일치" in issue:
            review_sentiment = review_analysis.get("sentiment", {}).get("sentiment_label", "중립")
            if review_sentiment == "부정":
                suggestions.append("고객의 불만을 인정하고 개선 의지를 보여주세요")
                improved_response = "불편을 끼쳐드려 죄송합니다. 소중한 의견을 바탕으로 개선하도록 노력하겠습니다."
            elif review_sentiment == "긍정":
                suggestions.append("고객의 만족에 감사를 표현하세요")
                improved_response = "만족스러운 구매 경험을 해주셔서 감사합니다. 앞으로도 좋은 제품으로 보답하겠습니다."
    
    return {
        "original_response": generated_response,
        "improved_response": improved_response,
        "suggestions": suggestions,
        "improvement_score": min(validation_result.get("score", 0) + 20, 100)
    }