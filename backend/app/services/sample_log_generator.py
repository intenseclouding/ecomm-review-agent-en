"""
샘플 로그 데이터 생성기
"""
import uuid
import random
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any
from ..models.product import AgentLog, AgentLogStep

def extract_sample_keywords(content: str) -> List[str]:
    """리뷰 내용에서 샘플 키워드 추출"""
    # 간단한 키워드 추출 (실제로는 더 정교한 로직 필요)
    common_keywords = {
        "음질": ["음질", "소리", "사운드"],
        "배터리": ["배터리", "충전", "전력"],
        "디자인": ["디자인", "외관", "모양", "색깔"],
        "품질": ["품질", "퀄리티", "만족"],
        "가격": ["가격", "비싸", "저렴", "가성비"],
        "배송": ["배송", "포장", "빠르", "늦"],
        "사용": ["사용", "편리", "불편"],
        "추천": ["추천", "좋", "만족", "훌륭"]
    }
    
    found_keywords = []
    content_lower = content.lower()
    
    for category, keywords in common_keywords.items():
        for keyword in keywords:
            if keyword in content_lower:
                found_keywords.append(keyword)
                break  # 카테고리당 하나씩만
    
    return found_keywords[:4]  # 최대 4개

def generate_sample_log(review_id: str, review_content: str, sentiment_label: str, seller_id: str = "SAMPLE-SELLER") -> AgentLog:
    """
    샘플 리뷰를 위한 가짜 로그 데이터 생성
    
    Args:
        review_id: 리뷰 ID
        review_content: 리뷰 내용
        sentiment_label: 감정 라벨 (긍정/부정/중립)
        seller_id: 셀러 ID
    
    Returns:
        생성된 AgentLog
    """
    
    # 기본 시간 설정 (과거 시간으로)
    base_time = datetime.now() - timedelta(minutes=random.randint(10, 1440))  # 10분~24시간 전
    
    # 단계별 설정
    steps_config = [
        {
            "step_name": "셀러 프롬프트 로드",
            "duration_range": (1500, 3000),
            "details": {
                "seller_id": seller_id,
                "prompts_loaded": {
                    "positive_templates": random.randint(2, 5),
                    "negative_templates": random.randint(2, 4),
                    "neutral_templates": random.randint(1, 3)
                },
                "selected_template_type": sentiment_label.lower(),
                "template_source": "seller_prompts.json"
            }
        },
        {
            "step_name": "리뷰 분석",
            "duration_range": (8000, 15000),
            "details": {
                "sentiment_analysis": {
                    "label": sentiment_label,
                    "confidence": round(random.uniform(0.7, 0.95), 2),
                    "polarity": round(random.uniform(-0.8, 0.8), 2)
                },
                "keywords_extracted": extract_sample_keywords(review_content),
                "topic_analysis": {
                    "primary_topic": random.choice(["품질", "배송", "가격", "디자인", "사용성"]),
                    "confidence": round(random.uniform(0.8, 0.95), 2)
                },
                "spam_check": {
                    "is_suspicious": False,
                    "risk_score": round(random.uniform(0.0, 0.2), 2),
                    "checks_passed": ["length_check", "keyword_check", "pattern_check"]
                }
            }
        },
        {
            "step_name": "개인화된 응답 생성",
            "duration_range": (10000, 18000),
            "details": {
                "base_template": get_sample_template(sentiment_label),
                "personalization_level": random.choice(["low", "medium", "high"]),
                "topic_addressed": random.choice(["품질", "배송", "가격"]),
                "keywords_mentioned": extract_sample_keywords(review_content)[:2],
                "generated_response": get_sample_response(sentiment_label),
                "template_modifications": random.randint(1, 3)
            }
        },
        {
            "step_name": "응답 적절성 검증",
            "duration_range": (5000, 10000),
            "details": {
                "validation_score": random.randint(75, 95),
                "issues_found": [],
                "sentiment_match": True,
                "length_appropriate": True,
                "tone_appropriate": True,
                "recommendation": "승인",
                "confidence_level": "high"
            }
        },
        {
            "step_name": "최종 결정",
            "duration_range": (3000, 8000),
            "details": {
                "final_decision": "승인",
                "confidence_score": random.randint(80, 95),
                "reasoning": get_sample_reasoning(sentiment_label),
                "auto_approved": False,
                "manual_review_required": False,
                "quality_score": round(random.uniform(0.8, 0.95), 2)
            }
        }
    ]
    
    # 단계별 시간 계산 및 로그 생성
    current_time = base_time
    log_steps = []
    
    for step_config in steps_config:
        duration = random.randint(*step_config["duration_range"])
        start_time = current_time
        end_time = current_time + timedelta(milliseconds=duration)
        
        log_steps.append(AgentLogStep(
            step_name=step_config["step_name"],
            start_time=start_time.isoformat(),
            end_time=end_time.isoformat(),
            duration_ms=duration,
            status="completed",
            details=step_config["details"]
        ))
        
        # 다음 단계까지 약간의 간격
        current_time = end_time + timedelta(milliseconds=random.randint(100, 500))
    
    total_duration = int((current_time - base_time).total_seconds() * 1000)
    
    log_id = f"LOG-{uuid.uuid4().hex[:8].upper()}"
    
    return AgentLog(
        id=log_id,
        review_id=review_id,
        session_id=log_id,
        start_time=base_time.isoformat(),
        end_time=current_time.isoformat(),
        total_duration_ms=total_duration,
        status="completed",
        steps=log_steps,
        metadata={
            "agent_version": "1.0.0",
            "model_used": "claude-3-sonnet",
            "total_tokens": random.randint(800, 1500),
            "processing_node": f"agent-worker-{random.randint(1, 3):02d}",
            "sample_data": True,
            "generated_at": datetime.now().isoformat()
        },
        is_sample=True
    )

def get_sample_template(sentiment_label: str) -> str:
    """감정에 따른 샘플 템플릿 반환"""
    templates = {
        "긍정": [
            "소중한 리뷰 감사합니다! 앞으로도 더 좋은 제품과 서비스로 보답하겠습니다.",
            "만족스러운 구매 경험을 해주셔서 정말 기쁩니다. 감사합니다!",
            "좋은 평가 주셔서 감사드립니다. 계속해서 품질 향상에 노력하겠습니다."
        ],
        "부정": [
            "불편을 끼쳐드려 죄송합니다. 개선할 수 있도록 노력하겠습니다.",
            "소중한 의견 감사합니다. 더 나은 서비스를 위해 참고하겠습니다.",
            "아쉬운 경험을 하셨군요. 앞으로 더욱 신경 쓰겠습니다."
        ],
        "중립": [
            "리뷰 작성해주셔서 감사합니다. 더 나은 경험을 위해 노력하겠습니다.",
            "소중한 의견 감사드립니다. 지속적으로 개선해나가겠습니다."
        ]
    }
    
    return random.choice(templates.get(sentiment_label, templates["중립"]))

def get_sample_response(sentiment_label: str) -> str:
    """감정에 따른 샘플 응답 반환"""
    responses = {
        "긍정": [
            "제품에 만족해주셔서 감사합니다. 지속적인 기술 혁신으로 더 나은 제품을 제공하겠습니다.",
            "좋은 리뷰 정말 감사드려요! 앞으로도 트렌디한 아이템으로 찾아뵐게요 👗",
            "아름다운 변화를 경험해주셔서 감사합니다 ✨ 계속해서 건강한 뷰티를 추구하겠습니다"
        ],
        "부정": [
            "상세한 사용 후기 감사드립니다. 고객 의견을 바탕으로 착용감 개선에 더욱 노력하겠습니다.",
            "피부에 맞지 않아 죄송합니다. 개인차를 고려한 제품 개발에 더욱 노력하겠습니다"
        ],
        "중립": [
            "솔직한 리뷰 감사해요! 사이즈 가이드 개선과 더 나은 핏을 위해 노력하겠습니다",
            "좋은 평가 감사드립니다. 배터리 성능 개선을 위해 지속적인 기술 개발에 노력하겠습니다."
        ]
    }
    
    return random.choice(responses.get(sentiment_label, responses["중립"]))

def get_sample_reasoning(sentiment_label: str) -> str:
    """감정에 따른 샘플 결정 근거 반환"""
    reasoning = {
        "긍정": [
            "긍정적 리뷰에 적절한 감사 표현과 개인화된 멘트가 포함되어 있음",
            "고객의 만족에 대한 공감과 지속적인 품질 향상 의지가 잘 표현됨",
            "브랜드 톤앤매너에 맞는 친근하고 전문적인 응답"
        ],
        "부정": [
            "고객의 불만을 인정하고 개선 의지를 명확히 표현함",
            "사과와 함께 구체적인 개선 방향을 제시하여 신뢰성 확보",
            "부정적 피드백에 대한 적절한 대응과 고객 중심적 자세"
        ],
        "중립": [
            "객관적 의견에 대한 감사와 지속적 개선 의지 표현",
            "균형잡힌 응답으로 고객과의 긍정적 관계 유지",
            "중립적 톤에 맞는 적절한 수준의 응답"
        ]
    }
    
    return random.choice(reasoning.get(sentiment_label, reasoning["중립"]))

def generate_all_sample_logs() -> List[AgentLog]:
    """모든 샘플 리뷰에 대한 로그 생성"""
    # 샘플 제품 데이터 로드
    try:
        with open('data/sample_products.json', 'r', encoding='utf-8') as f:
            products_data = json.load(f)
    except FileNotFoundError:
        print("샘플 제품 데이터를 찾을 수 없습니다.")
        return []
    
    sample_logs = []
    
    for product in products_data.get('products', []):
        for review in product.get('reviews', []):
            # seller_response가 있는 리뷰만 로그 생성
            if 'seller_response' in review:
                sentiment_label = "중립"
                
                # 감정 데이터가 있으면 사용
                if 'sentiment' in review and 'label' in review['sentiment']:
                    sentiment_label = review['sentiment']['label']
                
                log = generate_sample_log(
                    review_id=review['id'],
                    review_content=review['content'],
                    sentiment_label=sentiment_label,
                    seller_id=product['seller_id']
                )
                
                sample_logs.append(log)
    
    return sample_logs

if __name__ == "__main__":
    # 테스트 실행
    print("샘플 로그 생성 테스트...")
    
    # 단일 로그 생성 테스트
    test_log = generate_sample_log(
        "REV-TEST",
        "음질이 정말 좋아요! 추천합니다.",
        "긍정"
    )
    
    print(f"생성된 로그 ID: {test_log.id}")
    print(f"총 소요시간: {test_log.total_duration_ms}ms")
    print(f"단계 수: {len(test_log.steps)}")
    
    # 전체 샘플 로그 생성 테스트
    all_logs = generate_all_sample_logs()
    print(f"전체 샘플 로그 수: {len(all_logs)}")