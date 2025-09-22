from strands import Agent
from .tools import check_profanity, check_image_product_match, check_rating_consistency
import json
import logging
import time
from datetime import datetime
from typing import Dict, Any, List, Optional

# 로거 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 리뷰 검수 에이전트 정의
review_moderation_agent = Agent(
    model="us.anthropic.claude-3-5-sonnet-20241022-v2:0",
    tools=[check_profanity, check_image_product_match, check_rating_consistency],
    system_prompt="""
    당신은 지능적인 리뷰 검수 전문가입니다.
    
    🎯 목표: 리뷰의 적절성을 종합적으로 판단하세요.
    
    🛠️ 사용 가능한 도구들:
    - check_profanity: 욕설/선정적 표현 검사
    - check_image_product_match: 이미지와 제품의 관련성 검증
    - check_rating_consistency: 별점과 리뷰 내용의 일치성 분석
    
    🧠 검수 접근법:
    1. 먼저 리뷰를 분석하고 어떤 검수가 필요한지 판단하세요
    2. 상황에 맞는 도구들을 선택하여 실행하세요
    3. 각 도구의 결과를 종합하여 최종 판단하세요
    4. 검수 과정에서의 추론 과정을 설명하세요
    
    💡 지능적 판단 원칙:
    - 의심스러운 부분을 우선적으로 검사
    - 이미지가 없으면 이미지 검수는 건너뛰기
    - 맥락을 고려한 종합적 판단
    - 각 결정의 근거를 명확히 제시
    
    📋 응답 형식:
    {
        "reasoning": "검수 과정에서의 추론과 판단 근거",
        "profanity_check": {"status": "PASS/FAIL", "reason": "이유", "confidence": 0.0-1.0},
        "image_match": {"status": "PASS/FAIL/SKIP", "reason": "이유", "confidence": 0.0-1.0},
        "rating_consistency": {"status": "PASS/FAIL", "reason": "이유", "confidence": 0.0-1.0},
        "overall_status": "PASS/FAIL",
        "failed_checks": ["실패한 검수 항목들"],
        "checks_performed": ["실행된 검수 항목들"],
        "summary": "전체 검수 결과 요약"
    }
    """
)

def moderate_review(
    review_content: str,
    rating: int,
    product_data: Dict[str, Any],
    media_files: Optional[List[Dict]] = None
) -> Dict[str, Any]:
    """
    리뷰를 종합적으로 검수하는 메인 함수
    
    Args:
        review_content (str): 리뷰 내용
        rating (int): 별점 (1-5)
        product_data (Dict[str, Any]): 제품 정보
        media_files (Optional[List[Dict]]): 업로드된 미디어 파일들
        
    Returns:
        Dict[str, Any]: 검수 결과
    """
    
    # 미디어 파일 정보를 문자열로 변환
    media_info = "없음"
    if media_files and len(media_files) > 0:
        media_info = f"{len(media_files)}개 - " + ", ".join([f"{m.get('filename', 'unknown')} ({m.get('url', 'no-url')})" for m in media_files])
    
    moderation_prompt = f"""
    🔍 리뷰 검수 요청
    
    📝 리뷰 정보:
    - 내용: "{review_content}"
    - 별점: {rating}점 (1-5점 척도)
    - 제품: {product_data.get('name', 'Unknown')} ({product_data.get('category', 'Unknown')})
    - 이미지: {media_info}
    
    🤔 분석해보세요:
    이 리뷰에서 어떤 부분이 의심스럽거나 검수가 필요한지 먼저 판단하세요.
    
    💭 단계별 사고:
    1. 이 리뷰의 전반적인 특징은 무엇인가요?
    2. 별점과 내용이 일치하는 것 같나요?
    3. 부적절한 표현이 있을 가능성은 어떤가요?
    4. 이미지가 있다면 제품과 관련이 있을까요?
    
    🛠️ 필요한 도구를 선택하여 검수를 수행하고, 각 단계에서의 판단 근거를 설명해주세요.
    
    ⚖️ 최종 판단 기준:
    - 모든 검수 항목이 PASS여야 전체 PASS
    - 하나라도 FAIL이면 전체 FAIL
    - SKIP된 항목은 전체 결과에 영향 없음
    """
    
    start_time = time.time()
    review_id = f"rev_{int(time.time() * 1000)}"
    
    # 검수 시작 로그
    logger.info(json.dumps({
        "event": "moderation_start",
        "review_id": review_id,
        "review_content": review_content[:50] + "..." if len(review_content) > 50 else review_content,
        "rating": rating,
        "product": product_data.get('name', 'Unknown'),
        "has_media": bool(media_files and len(media_files) > 0),
        "timestamp": datetime.now().isoformat()
    }, ensure_ascii=False))
    
    try:
        # Agent를 사용한 자율적 검수 수행
        logger.info(json.dumps({
            "event": "agent_autonomous_analysis_start",
            "review_id": review_id,
            "agent": "review_moderation_agent",
            "prompt_length": len(moderation_prompt),
            "analysis_mode": "autonomous",
            "timestamp": datetime.now().isoformat()
        }, ensure_ascii=False))
        
        agent_start_time = time.time()
        
        # Agent 실행 (직접 호출 방식)
        agent_response = review_moderation_agent(moderation_prompt)
        
        agent_execution_time = time.time() - agent_start_time
        
        logger.info(json.dumps({
            "event": "agent_autonomous_analysis_complete",
            "review_id": review_id,
            "execution_time": round(agent_execution_time, 3),
            "response_length": len(str(agent_response)),
            "analysis_mode": "autonomous",
            "timestamp": datetime.now().isoformat()
        }, ensure_ascii=False))
        
        # Agent 응답 파싱
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
                
                moderation_result = json.loads(json_text)
            else:
                # AgentResult 객체를 문자열로 변환 후 JSON 파싱
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
                
                moderation_result = json.loads(json_text)
            
            # Agent 자율 판단 결과 로그
            logger.info(json.dumps({
                "event": "agent_autonomous_decision",
                "review_id": review_id,
                "overall_status": moderation_result.get("overall_status", "UNKNOWN"),
                "checks_performed": moderation_result.get("checks_performed", []),
                "failed_checks": moderation_result.get("failed_checks", []),
                "agent_reasoning": moderation_result.get("reasoning", "No reasoning provided")[:100] + "..." if len(moderation_result.get("reasoning", "")) > 100 else moderation_result.get("reasoning", "No reasoning provided"),
                "decision_mode": "autonomous",
                "timestamp": datetime.now().isoformat()
            }, ensure_ascii=False))
            
            total_execution_time = time.time() - start_time
            
            # 자율 검수 완료 로그
            logger.info(json.dumps({
                "event": "autonomous_moderation_complete",
                "review_id": review_id,
                "total_execution_time": round(total_execution_time, 3),
                "agent_execution_time": round(agent_execution_time, 3),
                "final_status": moderation_result.get("overall_status", "UNKNOWN"),
                "execution_mode": "agent_autonomous",
                "tools_used_count": len(moderation_result.get("checks_performed", [])),
                "timestamp": datetime.now().isoformat()
            }, ensure_ascii=False))
            
            return {
                "success": True,
                "moderation_result": moderation_result,
                "raw_response": str(agent_response),
                "execution_time": round(total_execution_time, 3),
                "review_id": review_id,
                "execution_mode": "agent_autonomous",
                "agent_reasoning": moderation_result.get("reasoning", "No reasoning provided")
            }
            
        except (json.JSONDecodeError, ValueError, KeyError) as parse_error:
            logger.error(json.dumps({
                "event": "agent_response_parse_error",
                "review_id": review_id,
                "error": str(parse_error),
                "raw_response": str(agent_response)[:200] + "..." if len(str(agent_response)) > 200 else str(agent_response),
                "timestamp": datetime.now().isoformat()
            }, ensure_ascii=False))
            
            # 파싱 실패 시 폴백으로 직접 검수 수행
            logger.warning(json.dumps({
                "event": "fallback_to_manual_moderation",
                "review_id": review_id,
                "reason": "agent_autonomous_response_parse_failed",
                "fallback_mode": "manual_sequential",
                "timestamp": datetime.now().isoformat()
            }, ensure_ascii=False))
            
            return _manual_moderation_fallback(review_content, rating, product_data, media_files, review_id, start_time)
        
    except Exception as e:
        logger.error(json.dumps({
            "event": "agent_execution_error",
            "review_id": review_id,
            "error_type": type(e).__name__,
            "error_message": str(e),
            "timestamp": datetime.now().isoformat()
        }, ensure_ascii=False))
        
        # Agent 자율 실행 실패 시 폴백으로 직접 검수 수행
        logger.warning(json.dumps({
            "event": "fallback_to_manual_moderation",
            "review_id": review_id,
            "reason": "agent_autonomous_execution_failed",
            "fallback_mode": "manual_sequential",
            "timestamp": datetime.now().isoformat()
        }, ensure_ascii=False))
        
        return _manual_moderation_fallback(review_content, rating, product_data, media_files, review_id, start_time)

def _manual_moderation_fallback(
    review_content: str,
    rating: int,
    product_data: Dict[str, Any],
    media_files: Optional[List[Dict]],
    review_id: str,
    start_time: float
) -> Dict[str, Any]:
    """
    Agent 실행 실패 시 폴백으로 사용되는 직접 검수 함수
    """
    try:
        from .tools import check_profanity, check_rating_consistency, check_image_product_match
        
        logger.info(json.dumps({
            "event": "manual_moderation_start",
            "review_id": review_id,
            "execution_mode": "fallback_sequential",
            "reason": "agent_autonomous_failed",
            "timestamp": datetime.now().isoformat()
        }, ensure_ascii=False))
        
        # 욕설 검사
        logger.info(json.dumps({
            "event": "tool_call_start",
            "review_id": review_id,
            "tool": "check_profanity",
            "timestamp": datetime.now().isoformat()
        }, ensure_ascii=False))
        
        profanity_result = check_profanity(review_content)
        
        logger.info(json.dumps({
            "event": "tool_call_complete",
            "review_id": review_id,
            "tool": "check_profanity",
            "result": profanity_result.get("status", "UNKNOWN"),
            "confidence": profanity_result.get("confidence", 0.0),
            "timestamp": datetime.now().isoformat()
        }, ensure_ascii=False))
        
        # 별점 일치성 검사
        logger.info(json.dumps({
            "event": "tool_call_start",
            "review_id": review_id,
            "tool": "check_rating_consistency",
            "timestamp": datetime.now().isoformat()
        }, ensure_ascii=False))
        
        consistency_result = check_rating_consistency(rating, review_content)
        
        logger.info(json.dumps({
            "event": "tool_call_complete",
            "review_id": review_id,
            "tool": "check_rating_consistency",
            "result": consistency_result.get("status", "UNKNOWN"),
            "confidence": consistency_result.get("confidence", 0.0),
            "timestamp": datetime.now().isoformat()
        }, ensure_ascii=False))
        
        # 이미지 검사 (있는 경우에만)
        if media_files and len(media_files) > 0:
            logger.info(json.dumps({
                "event": "tool_call_start",
                "review_id": review_id,
                "tool": "check_image_product_match",
                "timestamp": datetime.now().isoformat()
            }, ensure_ascii=False))
            
            image_result = check_image_product_match(media_files, product_data)
            
            logger.info(json.dumps({
                "event": "tool_call_complete",
                "review_id": review_id,
                "tool": "check_image_product_match",
                "result": image_result.get("status", "UNKNOWN"),
                "confidence": image_result.get("confidence", 0.0),
                "timestamp": datetime.now().isoformat()
            }, ensure_ascii=False))
            
            checks_performed = ["profanity_check", "image_match", "rating_consistency"]
        else:
            image_result = {"status": "SKIP", "reason": "업로드된 이미지가 없습니다.", "confidence": 1.0}
            checks_performed = ["profanity_check", "rating_consistency"]
            
            logger.info(json.dumps({
                "event": "tool_call_skipped",
                "review_id": review_id,
                "tool": "check_image_product_match",
                "reason": "no_media_files",
                "timestamp": datetime.now().isoformat()
            }, ensure_ascii=False))
        
        # 실패한 검수 항목 수집
        failed_checks = []
        if profanity_result["status"] == "FAIL":
            failed_checks.append("profanity_check")
        if consistency_result["status"] == "FAIL":
            failed_checks.append("rating_consistency")
        if image_result["status"] == "FAIL":
            failed_checks.append("image_match")
        
        overall_status = "FAIL" if failed_checks else "PASS"
        
        moderation_result = {
            "profanity_check": profanity_result,
            "image_match": image_result,
            "rating_consistency": consistency_result,
            "overall_status": overall_status,
            "failed_checks": failed_checks,
            "checks_performed": checks_performed,
            "summary": f"폴백 검수 완료 - {overall_status}"
        }
        
        total_execution_time = time.time() - start_time
        
        logger.info(json.dumps({
            "event": "manual_moderation_complete",
            "review_id": review_id,
            "total_execution_time": round(total_execution_time, 3),
            "final_status": overall_status,
            "timestamp": datetime.now().isoformat()
        }, ensure_ascii=False))
        
        return {
            "success": True,
            "moderation_result": moderation_result,
            "raw_response": "폴백 직접 검수 수행",
            "execution_time": round(total_execution_time, 3),
            "review_id": review_id
        }
        
    except Exception as e:
        logger.error(json.dumps({
            "event": "manual_moderation_error",
            "review_id": review_id,
            "error_type": type(e).__name__,
            "error_message": str(e),
            "timestamp": datetime.now().isoformat()
        }, ensure_ascii=False))
        
        return {
            "success": False,
            "error": str(e),
            "moderation_result": {
                "profanity_check": {"status": "FAIL", "reason": "시스템 오류", "confidence": 0.0},
                "image_match": {"status": "SKIP", "reason": "시스템 오류", "confidence": 0.0},
                "rating_consistency": {"status": "FAIL", "reason": "시스템 오류", "confidence": 0.0},
                "overall_status": "FAIL",
                "failed_checks": ["system_error"],
                "checks_performed": [],
                "summary": f"시스템 오류로 인해 검수를 완료할 수 없습니다: {str(e)}"
            },
            "execution_time": round(time.time() - start_time, 3),
            "review_id": review_id
        }

def generate_error_messages(moderation_result: Dict[str, Any]) -> List[str]:
    """
    검수 실패 시 사용자에게 표시할 에러 메시지를 생성합니다.
    
    Args:
        moderation_result (Dict[str, Any]): 검수 결과
        
    Returns:
        List[str]: 에러 메시지 목록
    """
    messages = []
    failed_checks = moderation_result.get("failed_checks", [])
    
    if "profanity_check" in failed_checks:
        reason = moderation_result.get("profanity_check", {}).get("reason", "부적절한 언어가 포함되어 있습니다.")
        messages.append(f"언어 검수 실패: {reason}")
    
    if "image_match" in failed_checks:
        reason = moderation_result.get("image_match", {}).get("reason", "업로드된 이미지가 제품과 관련이 없습니다.")
        messages.append(f"이미지 검수 실패: {reason}")
    
    if "rating_consistency" in failed_checks:
        reason = moderation_result.get("rating_consistency", {}).get("reason", "별점과 리뷰 내용이 일치하지 않습니다.")
        messages.append(f"별점 일치성 검수 실패: {reason}")
    
    if "system_error" in failed_checks:
        messages.append("시스템 오류로 인해 검수를 완료할 수 없습니다. 잠시 후 다시 시도해주세요.")
    
    return messages
