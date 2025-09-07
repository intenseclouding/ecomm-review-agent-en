from strands import Agent
from .tools import sentiment_analysis, extract_keywords, detect_spam_or_fake, categorize_review_topic
from .content_moderation import moderate_review_content
import json
from typing import Dict, Any

# 리뷰 분석 에이전트 정의
review_analyzer_agent = Agent(
    model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    tools=[sentiment_analysis, extract_keywords, detect_spam_or_fake, categorize_review_topic],
    system_prompt="""
    당신은 전문적인 리뷰 분석 에이전트입니다. 
    
    주요 역할:
    1. 고객 리뷰의 감정을 정확히 분석
    2. 리뷰에서 핵심 키워드 추출
    3. 스팸이나 가짜 리뷰 탐지
    4. 리뷰 주제 카테고리 분류
    5. 종합적인 분석 결과 제공
    
    분석 시 고려사항:
    - 한국어 텍스트의 미묘한 감정 표현 이해
    - 문맥상 숨겨진 의미 파악
    - 객관적이고 공정한 분석
    - 셀러에게 유용한 인사이트 제공
    
    항상 JSON 형태로 구조화된 분석 결과를 제공하세요.
    """
)

def moderate_and_analyze_review(review_text: str, product_id: str = None) -> Dict[str, Any]:
    """
    리뷰 검수 후 분석을 수행하는 메인 함수
    
    Args:
        review_text (str): 검수 및 분석할 리뷰 텍스트
        product_id (str): 제품 ID (선택사항)
        
    Returns:
        Dict[str, Any]: 검수 및 분석 결과
    """
    
    try:
        # 1. 먼저 내용 검수 수행
        moderation_result = moderate_review_content(review_text)
        
        # 검수 실패 시 즉시 반환
        if not moderation_result["is_approved"]:
            return {
                "success": False,
                "moderation_failed": True,
                "moderation_result": moderation_result,
                "error": f"리뷰 검수 실패: {moderation_result['reason']}",
                "structured_data": None
            }
        
        # 2. 검수 통과 시 분석 수행
        return analyze_review_for_storage(review_text, product_id)
        
    except Exception as e:
        return {
            "success": False,
            "moderation_failed": False,
            "error": str(e),
            "structured_data": None
        }

def analyze_review_for_storage(review_text: str, product_id: str = None) -> Dict[str, Any]:
    """
    리뷰를 분석하여 데이터베이스 저장용 구조화된 결과를 반환하는 함수
    
    Args:
        review_text (str): 분석할 리뷰 텍스트
        product_id (str): 제품 ID (선택사항)
        
    Returns:
        Dict[str, Any]: Review 모델에 저장할 수 있는 구조화된 분석 결과
    """
    
    try:
        # 1. 감정 분석 수행
        sentiment_result = sentiment_analysis(review_text)
        
        # 2. 키워드 추출 (최대 6개로 제한)
        keywords_result = extract_keywords(review_text, max_keywords=6)
        
        # 3. 스팸 검사
        spam_result = detect_spam_or_fake(review_text)
        
        # 4. 주제 분류
        topic_result = categorize_review_topic(review_text, keywords_result)
        
        # Review 모델에 맞는 구조화된 결과 생성
        structured_result = {
            "keywords": keywords_result,
            "sentiment": {
                "label": sentiment_result["sentiment_label"],
                "confidence": sentiment_result["confidence"],
                "polarity": sentiment_result["polarity"]
            },
            "analysis_completed": True,
            "analysis_timestamp": None,  # 호출하는 곳에서 설정
            "spam_check": spam_result,
            "topic_analysis": topic_result
        }
        
        return {
            "success": True,
            "moderation_passed": True,
            "structured_data": structured_result,
            "raw_analysis": {
                "sentiment": sentiment_result,
                "keywords": keywords_result,
                "spam_check": spam_result,
                "topic_analysis": topic_result
            }
        }
        
    except Exception as e:
        # 분석 실패 시 기본값 반환
        return {
            "success": False,
            "error": str(e),
            "structured_data": {
                "keywords": [],
                "sentiment": {
                    "label": "중립",
                    "confidence": 0.5,
                    "polarity": 0.0
                },
                "analysis_completed": False,
                "analysis_timestamp": None
            }
        }

def analyze_review(review_text: str, product_id: str = None) -> Dict[str, Any]:
    """
    리뷰를 종합적으로 분석하는 메인 함수 (기존 호환성 유지)
    
    Args:
        review_text (str): 분석할 리뷰 텍스트
        product_id (str): 제품 ID (선택사항)
        
    Returns:
        Dict[str, Any]: 종합 분석 결과
    """
    
    analysis_prompt = f"""
    다음 리뷰를 종합적으로 분석해주세요:
    
    리뷰 내용: "{review_text}"
    제품 ID: {product_id or "미제공"}
    
    다음 단계로 분석을 진행하세요:
    1. 감정 분석 수행
    2. 주요 키워드 추출 (최대 8개)
    3. 스팸/가짜 리뷰 검사
    4. 추출된 키워드를 바탕으로 주제 분류
    
    최종적으로 다음 형태의 JSON으로 결과를 정리해주세요:
    {
        "review_text": "원본 리뷰 텍스트",
        "sentiment": "감정분석 결과",
        "keywords": "키워드 리스트",
        "spam_check": "스팸 검사 결과",
        "topic_analysis": "주제 분류 결과",
        "overall_assessment": "전반적인 평가 및 권장사항",
        "seller_insights": "셀러를 위한 인사이트"
    }
    """
    
    try:
        result = review_analyzer_agent(analysis_prompt)
        return {
            "success": True,
            "analysis": result.message,
            "raw_result": result
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "analysis": None
        }

if __name__ == "__main__":
    # 테스트용 샘플 리뷰
    sample_review = "이 제품 정말 좋아요! 배송도 빠르고 품질도 만족스럽습니다. 가격 대비 성능이 훌륭하네요. 다음에도 또 구매할 예정입니다."
    
    result = analyze_review(sample_review, "PROD-001")
    print("=== 리뷰 분석 결과 ===")
    print(json.dumps(result, ensure_ascii=False, indent=2))