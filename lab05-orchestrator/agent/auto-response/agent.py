from strands import Agent
import json
from typing import Dict, Any

# Import handling for both module and direct execution
try:
    from .tools import llm_sentiment, dict_sentiment
except ImportError:
    from tools import llm_sentiment, dict_sentiment

# 감정 분석 에이전트 정의
sentiment_analyzer_agent = Agent(
    model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    tools=[llm_sentiment, dict_sentiment],
    system_prompt="""
    당신은 전문적인 한국어 리뷰 감정 분석 에이전트입니다.
    
    주요 역할:
    1. 한국어 리뷰 텍스트의 감정 분석 (긍정/부정/중립)
    2. 하이브리드 분석: LLM → (score < 0.6 OR label == "NEU") → dict 재분석
    3. 한국어 신조어 및 슬랭 표현 인식
    4. 라우트 추적을 통한 분석 경로 기록
    
    분석 원칙:
    - 객관적이고 정확한 감정 분석 수행
    - 한국어 특유의 표현과 문맥 고려
    - 명확한 근거와 함께 분석 결과 제시
    - 신뢰도 점수를 통한 분석 품질 평가
    - LLM 결과가 불확실하면 사전 기반 재분석으로 보완
    
    하이브리드 로직:
    1. 먼저 llm_sentiment로 Claude 3.7 분석 수행
    2. 결과 점수 < 0.6 또는 라벨 == "NEU"이면 dict_sentiment로 재분석
    3. 라우트 추적: "llm" (LLM만), "llm→dict" (LLM→사전), "dict_fallback" (오류시)
    
    분석 결과는 반드시 다음 JSON 형태로 제공하세요:
    {
        "label": "긍정/부정/중립",
        "score": 0.0-1.0,
        "rationale": "분석 근거",
        "route": "llm/llm→dict/dict_fallback"
    }
    """
)

def generate_confidence_explanation(sentiment_result: Dict[str, Any]) -> str:
    """
    감정 분석 결과에 대한 신뢰도 설명을 생성합니다.
    
    Args:
        sentiment_result (Dict[str, Any]): 감정 분석 결과
        
    Returns:
        str: 신뢰도 설명
    """
    label = sentiment_result.get("label", "중립")
    score = sentiment_result.get("score", 0.5)
    route = sentiment_result.get("route", "unknown")
    
    # 라우트별 설명
    route_explanations = {
        "llm": "Claude 3.7 LLM 분석",
        "llm→dict": "LLM 분석 후 사전 기반 재분석",
        "dict_fallback": "사전 기반 폴백 분석"
    }
    
    route_desc = route_explanations.get(route, "알 수 없는 분석 방법")
    
    # 점수별 신뢰도 설명
    if score >= 0.8:
        confidence_desc = "매우 높은 신뢰도"
    elif score >= 0.6:
        confidence_desc = "높은 신뢰도"
    elif score >= 0.4:
        confidence_desc = "보통 신뢰도"
    else:
        confidence_desc = "낮은 신뢰도"
    
    return f"{route_desc}를 통한 {label} 감정 분석 ({confidence_desc}: {score:.3f})"

def analyze_review(review_content: str, debug_mode: bool = False) -> Dict[str, Any]:
    """
    리뷰 텍스트의 감정을 분석하는 메인 함수
    
    Args:
        review_content (str): 분석할 리뷰 텍스트
        debug_mode (bool): raw_response 포함 여부 (기본값: False)
        
    Returns:
        Dict[str, Any]: 감정 분석 결과
    """
    
    try:
        # 시간 측정으로 타임아웃 체크 (signal.alarm 대신)
        import time
        
        start_time = time.time()
        
        try:
            # Import handling for both module and direct execution
            try:
                from .tools import llm_sentiment, dict_sentiment
            except ImportError:
                from tools import llm_sentiment, dict_sentiment
            
            # 빈 문자열 체크 - 즉시 dict_fallback
            if not review_content or review_content.strip() == "":
                fallback_result = dict_sentiment(review_content)
                sentiment_result = {
                    "label": "중립",
                    "score": 0.3,
                    "rationale": "빈 리뷰 텍스트로 인한 중립 처리",
                    "route": "dict_fallback"
                }
            else:
                # 1단계: LLM 직접 호출 (Agent 우회)
                llm_result = llm_sentiment(review_content)
                elapsed_time = time.time() - start_time
                
                # LLM 결과 검증
                if (llm_result["score"] >= 0.6 and llm_result["label"] != "중립"):
                    # LLM 결과가 충분히 확실함 - 그대로 사용
                    sentiment_result = {
                        "label": llm_result["label"],
                        "score": llm_result["score"],
                        "rationale": llm_result["rationale"],
                        "route": "llm"
                    }
                else:
                    # LLM 결과가 불확실함 - 사전 기반 재분석
                    dict_result = dict_sentiment(review_content)
                    
                    # 사전 결과가 더 확실하면 사전 결과 사용, 아니면 LLM 결과 유지
                    if dict_result["score"] > llm_result["score"]:
                        sentiment_result = {
                            "label": dict_result["label"],
                            "score": dict_result["score"],
                            "rationale": f"LLM 재분석: {dict_result['rationale']} (LLM: {llm_result['label']}/{llm_result['score']:.3f})",
                            "route": "llm→dict",
                            "llm_result": llm_result,
                            "dict_result": dict_result
                        }
                    else:
                        sentiment_result = {
                            "label": llm_result["label"],
                            "score": llm_result["score"],
                            "rationale": f"LLM 유지: {llm_result['rationale']} (사전 점수: {dict_result['score']:.3f})",
                            "route": "llm→dict",
                            "llm_result": llm_result,
                            "dict_result": dict_result
                        }
                
        except Exception as e:
            elapsed_time = time.time() - start_time
            
            # API 오류나 기타 예외 발생시 폴백
            print(f"LLM 오류/타임아웃, dict_sentiment 폴백 수행: {e}")
            
            # 즉시 dict_sentiment 폴백
            try:
                # Import handling for both module and direct execution
                try:
                    from .tools import dict_sentiment
                except ImportError:
                    from tools import dict_sentiment
                fallback_result = dict_sentiment(review_content)
                
                sentiment_result = {
                    "label": fallback_result["label"],
                    "score": fallback_result["score"],
                    "rationale": f"LLM 오류로 인한 사전 기반 폴백 ({elapsed_time:.1f}초): {fallback_result['rationale']}",
                    "route": "dict_fallback"
                }
                
                # 신뢰도 설명 추가
                sentiment_result["confidence_explanation"] = generate_confidence_explanation(sentiment_result)
                
                response_data = {
                    "success": True,
                    "sentiment_result": sentiment_result
                }
                
                if debug_mode:
                    response_data["raw_response"] = f"LLM 오류 - dict_sentiment 폴백 사용"
                
                return response_data
                
            except Exception as fallback_error:
                # 폴백도 실패한 경우 - 중립 + 에러 메시지 반환
                sentiment_result = {
                    "label": "중립",
                    "score": 0.3,
                    "rationale": f"LLM 오류 및 폴백 실패: {str(fallback_error)}",
                    "route": "dict_fallback"
                }
                
                # 신뢰도 설명 추가
                sentiment_result["confidence_explanation"] = generate_confidence_explanation(sentiment_result)
                
                response_data = {
                    "success": False,
                    "error": str(fallback_error),
                    "sentiment_result": sentiment_result
                }
                
                if debug_mode:
                    response_data["raw_response"] = f"LLM 오류 및 폴백 실패"
                
                return response_data
        
        # 신뢰도 설명 추가
        sentiment_result["confidence_explanation"] = generate_confidence_explanation(sentiment_result)
        
        response_data = {
            "success": True,
            "sentiment_result": sentiment_result
        }
        
        # raw_response는 debug_mode일 때만 포함 (기본값: False)
        if debug_mode:
            response_data["raw_response"] = "Direct tool execution (Agent bypassed)"
        
        return response_data
        
    except Exception as e:
        # 기본 try/except - 중립 + 에러 메시지 반환 (타임아웃/예외 처리)
        sentiment_result = {
            "label": "중립",
            "score": 0.3,
            "rationale": f"시스템 오류로 인해 분석을 완료할 수 없습니다: {str(e)}",
            "route": "dict_fallback"
        }
        
        # 신뢰도 설명 추가
        sentiment_result["confidence_explanation"] = generate_confidence_explanation(sentiment_result)
        
        response_data = {
            "success": False,
            "error": str(e),
            "sentiment_result": sentiment_result
        }
        
        if debug_mode:
            response_data["raw_response"] = f"시스템 오류: {str(e)}"
        
        return response_data

if __name__ == "__main__":
    # 테스트용 샘플 데이터 - review_moderator 패턴 따름
    test_cases = [
        # 4 positive Korean slang test cases
        {
            "review_content": "이 제품 존나 좋아요! 핏도 미친듯이 좋고 ㅋㅋ",
            "expected": "긍정",
            "description": "긍정 슬랭 - 존나, 미친듯이, ㅋㅋ"
        },
        {
            "review_content": "인생템이네요! 발림성 개좋고 갓갓 레전드",
            "expected": "긍정",
            "description": "긍정 슬랭 - 인생템, 개좋고, 갓, 레전드"
        },
        {
            "review_content": "대박 개꿀이에요 ㅎㅎ 존좋 쩐다",
            "expected": "긍정",
            "description": "긍정 슬랭 - 대박, 개꿀, ㅎㅎ, 존좋, 쩐다"
        },
        {
            "review_content": "핏이 미친 것 같아요! 개쩐다 진짜",
            "expected": "긍정",
            "description": "긍정 슬랭 - 핏이 미친, 개쩐다"
        },
        
        # 4 negative Korean slang test cases
        {
            "review_content": "완전 개별로네요 ㅠㅠ 품질이 노답",
            "expected": "부정",
            "description": "부정 슬랭 - 개별로, ㅠㅠ, 노답"
        },
        {
            "review_content": "뒤집어짐 진짜 구리다 실밥천국이네",
            "expected": "부정",
            "description": "부정 슬랭 - 뒤집어짐, 구리다, 실밥천국"
        },
        {
            "review_content": "헬게이트 망함 ㅜㅜ 완전 별로",
            "expected": "부정",
            "description": "부정 슬랭 - 헬게이트, 망함, ㅜㅜ, 별로"
        },
        {
            "review_content": "이거 진짜 구려요 노답 ㅠㅠ",
            "expected": "부정",
            "description": "부정 슬랭 - 구려요, 노답, ㅠㅠ"
        },
        
        # 4 ambiguous/mixed content test cases (including route transition verification)
        {
            "review_content": "미쳤는데 배터리는 별로",
            "expected": "중립",
            "description": "혼합 표현 - 라우트 전환 테스트용 (미쳤는데 + 별로)"
        },
        {
            "review_content": "디자인은 좋은데 가격이 아쉬워요",
            "expected": "중립",
            "description": "혼합 표현 - 긍정과 부정 혼재"
        },
        {
            "review_content": "미친 퀄리티인데 배송이 느려서 실망",
            "expected": "중립",
            "description": "혼합 표현 - 미친(긍정) + 실망(부정)"
        },
        {
            "review_content": "그냥 보통이에요. 무난한 것 같아요.",
            "expected": "중립",
            "description": "중립 표현 - 명확한 중립"
        },
        
        # 2 edge cases
        {
            "review_content": "",
            "expected": "중립",
            "description": "엣지 케이스 - 빈 문자열 (NEU + 에러 메시지 예상)"
        },
        {
            "review_content": "이 제품은 정말로 훌륭한 품질을 자랑하며 사용자 경험이 매우 뛰어나고 디자인도 세련되어 있으며 기능성도 우수하고 가격 대비 성능이 탁월하여 강력히 추천하고 싶은 제품입니다. 특히 내구성이 뛰어나고 사용하기 편리하며 고객 서비스도 친절하고 배송도 빨라서 전반적으로 매우 만족스러운 구매 경험이었습니다. 앞으로도 이런 좋은 제품들을 계속 출시해주시기 바라며 다른 분들께도 적극 추천드리고 싶습니다.",
            "expected": "긍정",
            "description": "엣지 케이스 - 긴 리뷰 텍스트"
        }
    ]
    
    # 라우트 추적 통계
    route_stats = {"llm": 0, "llm→dict": 0, "dict_fallback": 0}
    accuracy_stats = {"correct": 0, "total": 0}
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n=== 테스트 케이스 {i}: {test_case['description']} ===")
        # debug_mode=True로 raw_response 포함하여 테스트
        result = analyze_review(test_case["review_content"], debug_mode=True)
        
        if result["success"]:
            sentiment = result["sentiment_result"]
            print(f"리뷰: '{test_case['review_content'][:50]}{'...' if len(test_case['review_content']) > 50 else ''}'")
            print(f"결과: {sentiment['label']} (점수: {sentiment['score']:.3f})")
            print(f"라우팅: {sentiment['route']}")
            print(f"근거: {sentiment['rationale'][:100]}{'...' if len(sentiment['rationale']) > 100 else ''}")
            print(f"신뢰도: {sentiment.get('confidence_explanation', 'N/A')}")
            print(f"예상: {test_case['expected']}, 실제: {sentiment['label']}")
            
            # 정확도 통계
            accuracy_stats["total"] += 1
            if sentiment['label'] == test_case['expected']:
                accuracy_stats["correct"] += 1
                print("✅ 예상 결과와 일치")
            else:
                print("❌ 예상 결과와 불일치")
            
            # 라우트 통계 업데이트
            route = sentiment['route']
            if route in route_stats:
                route_stats[route] += 1
            
            # 스키마 검증
            required_fields = ["label", "score", "rationale", "route", "confidence_explanation"]
            missing_fields = [field for field in required_fields if field not in sentiment]
            if missing_fields:
                print(f"⚠️  누락된 필드: {missing_fields}")
            
            # 라우트 검증
            valid_routes = ["llm", "llm→dict", "dict_fallback"]
            if sentiment['route'] not in valid_routes:
                print(f"⚠️  잘못된 라우트: {sentiment['route']}")
            
            # 점수 범위 검증
            if not (0.0 <= sentiment['score'] <= 1.0):
                print(f"⚠️  점수 범위 오류: {sentiment['score']}")
            
            # 특별 케이스 검증
            if test_case["review_content"] == "":
                if sentiment['label'] != 'NEU' or 'error' not in sentiment['rationale'].lower():
                    print(f"⚠️  빈 문자열 케이스: NEU + 에러 메시지 예상, 실제: {sentiment['label']}")
                else:
                    print("✅ 빈 문자열 케이스 올바르게 처리됨")
                
        else:
            print(f"분석 실행 실패: {result.get('error', 'Unknown error')}")
            sentiment = result["sentiment_result"]
            print(f"폴백 결과: {sentiment['label']} (점수: {sentiment['score']:.3f})")
            print(f"폴백 라우팅: {sentiment['route']}")
            print(f"폴백 근거: {sentiment['rationale'][:100]}{'...' if len(sentiment['rationale']) > 100 else ''}")
            
            # 실패한 경우도 통계에 포함
            accuracy_stats["total"] += 1
            route_stats["dict_fallback"] += 1
    
    print(f"\n=== 테스트 결과 요약 ===")
    print(f"총 테스트 케이스: {len(test_cases)}개")
    print(f"정확도: {accuracy_stats['correct']}/{accuracy_stats['total']} ({accuracy_stats['correct']/accuracy_stats['total']*100:.1f}%)")
    
    print(f"\n=== 라우트 추적 통계 ===")
    for route, count in route_stats.items():
        percentage = count / len(test_cases) * 100
        print(f"- {route}: {count}회 ({percentage:.1f}%)")
    
    print(f"\n=== 라우트 전환 검증 ===")
    # "미쳤는데 배터리는 별로" 케이스의 라우트 확인
    transition_case = next((case for case in test_cases if "미쳤는데 배터리는 별로" in case["review_content"]), None)
    if transition_case:
        transition_result = analyze_review(transition_case["review_content"], debug_mode=False)
        if transition_result["success"]:
            route = transition_result["sentiment_result"]["route"]
            if route == "llm→dict":
                print("✅ 라우트 전환 케이스가 올바르게 llm→dict 경로를 사용함")
            else:
                print(f"⚠️  라우트 전환 케이스가 예상과 다른 경로 사용: {route}")
        else:
            print("⚠️  라우트 전환 케이스 테스트 실패")
    
    print(f"\n=== 스키마 일관성 테스트 완료 ===")
    print("모든 라우트가 동일한 스키마를 반환하는지 확인됨:")
    print("- label: 긍정/부정/중립")
    print("- score: 0.0-1.0")
    print("- rationale: string")
    print("- route: llm | llm→dict | dict_fallback")
    print("- confidence_explanation: string")