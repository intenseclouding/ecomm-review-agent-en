from strands import tool
import json
import boto3
from typing import Dict, Any

@tool
def llm_sentiment(review_text: str) -> Dict[str, Any]:
    """
    Claude 3.7을 사용한 한국어 감정 분석
    
    Args:
        review_text (str): 분석할 리뷰 텍스트
        
    Returns:
        Dict[str, Any]: 감정 분석 결과
        {
            "label": "POS/NEG/NEU",
            "score": 0.0-1.0,
            "rationale": "분석 근거"
        }
    """
    try:
        # Bedrock 클라이언트 초기화 (AWS 설정과 일치하도록 us-east-1 사용)
        bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
        
        # 간단하고 빠른 한국어 감정분석 프롬프트
        prompt = f"""한국어 리뷰 감정 분석:

"{review_text}"

한국어 슬랭 고려: 존나/개쩐다/갓/레전드(긍정), 개별로/노답/별로(부정), ㅋㅋ(긍정), ㅠㅠ(부정)

JSON 응답: {{"label": "POS/NEG/NEU", "score": 0.0-1.0, "rationale": "근거"}}"""
        
        # Bedrock API 호출 (타임아웃 없이 빠른 응답 기대)
        response = bedrock.invoke_model(
            modelId="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 200,  # 토큰 수 줄여서 빠른 응답
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            })
        )
        
        # 응답 파싱
        response_body = json.loads(response['body'].read())
        claude_response = response_body['content'][0]['text']
        
        # review_moderator와 정확히 동일한 JSON 파싱 전략
        try:
            sentiment_result = None
            
            # 방법 1: ```json 블록에서 추출
            if "```json" in claude_response:
                json_start = claude_response.find("```json") + 7
                json_end = claude_response.find("```", json_start)
                if json_end > json_start:
                    json_text = claude_response[json_start:json_end].strip()
                    sentiment_result = json.loads(json_text)
            
            # 방법 2: 마지막 완전한 JSON 객체 찾기
            if not sentiment_result and "{" in claude_response and "}" in claude_response:
                json_start = claude_response.rfind("{")
                json_end = claude_response.rfind("}") + 1
                if json_end > json_start:
                    json_text = claude_response[json_start:json_end]
                    try:
                        sentiment_result = json.loads(json_text)
                    except json.JSONDecodeError:
                        # 방법 3: 첫 번째 완전한 JSON 객체 시도
                        json_start = claude_response.find("{")
                        json_end = claude_response.find("}") + 1
                        if json_end > json_start:
                            json_text = claude_response[json_start:json_end]
                            sentiment_result = json.loads(json_text)
            
            if not sentiment_result:
                raise ValueError("JSON 형태를 찾을 수 없습니다.")
            
            # 결과 검증 및 정규화
            label = sentiment_result.get("label", "NEU")
            score = float(sentiment_result.get("score", 0.5))
            rationale = sentiment_result.get("rationale", "")
            
            # 점수 범위 검증
            score = max(0.0, min(1.0, score))
            
            # 라벨 검증 및 한국어 변환
            label_map = {"POS": "긍정", "NEG": "부정", "NEU": "중립"}
            if label not in ["POS", "NEG", "NEU"]:
                label = "중립"
                score = 0.5
                rationale = f"잘못된 라벨로 인한 중립 처리"
            else:
                label = label_map[label]
            
            return {
                "label": label,
                "score": round(score, 3),
                "rationale": rationale
            }
            
        except (json.JSONDecodeError, ValueError) as e:
            # JSON 파싱 실패 시 폴백
            return {
                "label": "NEU",
                "score": 0.3,
                "rationale": f"Claude 응답 파싱 실패: {str(e)[:100]}"
            }
            
    except Exception as e:
        # API 호출 실패 시 폴백
        return {
            "label": "NEU",
            "score": 0.3,
            "rationale": f"Claude API 호출 실패: {str(e)[:100]}"
        }

def _normalize_text(text: str) -> str:
    """
    텍스트 정규화 함수 (소문자 변환, 연속 공백 정리)
    
    Args:
        text (str): 정규화할 텍스트
        
    Returns:
        str: 정규화된 텍스트
    """
    import re
    # 소문자 변환 및 연속 공백을 단일 공백으로 변환
    normalized = re.sub(r'\s+', ' ', text.lower().strip())
    return normalized

@tool
def dict_sentiment(review_text: str) -> Dict[str, Any]:
    """
    한국어 슬랭 사전 기반 감정 분석
    
    Args:
        review_text (str): 분석할 리뷰 텍스트
        
    Returns:
        Dict[str, Any]: 감정 분석 결과
        {
            "label": "POS/NEG/NEU",
            "score": 0.0-1.0,
            "rationale": "분석 근거"
        }
    """
    # 한국어 슬랭 사전 (하드코딩) - 요구사항에 따른 정확한 패턴
    positive_patterns = [
        "인생템", "핏이 미친", "발림성 개좋고", "개쩐다", "갓", "레전드", 
        "대박", "개꿀", "존좋", "쩐다", "ㅋㅋ", "ㅎㅎ"
    ]
    
    negative_patterns = [
        "뒤집어짐", "노답", "구리다", "실밥천국", "헬게이트", "망함", "별로", 
        "ㅠㅠ", "ㅜㅜ"
    ]
    
    # 문맥에 따라 달라지는 표현들 - "미쳤다"를 ambiguous 카테고리로 이동
    ambiguous_patterns = {
        "미친": {
            "positive_contexts": ["맛", "핏", "서비스", "품질", "퀄리티", "디자인", "색깔", "예쁘", "좋", "대박", "쩐다"],
            "negative_contexts": ["환불", "실망", "배송", "불만", "화나", "짜증", "별로"]
        },
        "미쳤": {
            "positive_contexts": ["맛", "핏", "서비스", "품질", "퀄리티", "디자인", "색깔", "예쁘", "좋", "대박", "쩐다"],
            "negative_contexts": ["환불", "실망", "배송", "불만", "화나", "짜증", "별로"]
        }
    }
    
    # 텍스트 정규화
    normalized_text = _normalize_text(review_text)
    
    positive_score = 0
    negative_score = 0
    found_patterns = []
    
    # 긍정 패턴 검사
    for pattern in positive_patterns:
        if pattern.lower() in normalized_text:
            positive_score += 1
            found_patterns.append(f"긍정: '{pattern}'")
    
    # 부정 패턴 검사
    for pattern in negative_patterns:
        if pattern.lower() in normalized_text:
            negative_score += 1
            found_patterns.append(f"부정: '{pattern}'")
    
    # 애매한 표현 문맥 분석
    for ambiguous_word, contexts in ambiguous_patterns.items():
        if ambiguous_word in normalized_text:
            # 긍정 문맥 확인
            positive_context_found = any(ctx in normalized_text for ctx in contexts["positive_contexts"])
            # 부정 문맥 확인
            negative_context_found = any(ctx in normalized_text for ctx in contexts["negative_contexts"])
            
            if positive_context_found and not negative_context_found:
                positive_score += 1
                found_patterns.append(f"긍정 문맥: '{ambiguous_word}' (긍정적 맥락)")
            elif negative_context_found and not positive_context_found:
                negative_score += 1
                found_patterns.append(f"부정 문맥: '{ambiguous_word}' (부정적 맥락)")
            else:
                found_patterns.append(f"중립 문맥: '{ambiguous_word}' (애매한 맥락)")
    
    # 감정 라벨 및 점수 계산
    total_patterns = positive_score + negative_score
    
    if total_patterns == 0:
        # 패턴이 없으면 중립
        label = "중립"
        score = 0.5
        rationale = "감정 표현 패턴을 찾을 수 없음"
    elif positive_score > negative_score:
        # 긍정이 더 많음
        label = "긍정"
        confidence = positive_score / total_patterns
        score = 0.6 + (confidence * 0.4)  # 0.6-1.0 범위
        rationale = f"긍정 패턴 {positive_score}개, 부정 패턴 {negative_score}개 발견"
    elif negative_score > positive_score:
        # 부정이 더 많음
        label = "부정"
        confidence = negative_score / total_patterns
        score = 0.6 + (confidence * 0.4)  # 0.6-1.0 범위
        rationale = f"부정 패턴 {negative_score}개, 긍정 패턴 {positive_score}개 발견"
    else:
        # 긍정과 부정이 같음
        label = "중립"
        score = 0.5
        rationale = f"긍정 패턴 {positive_score}개, 부정 패턴 {negative_score}개로 균형"
    
    # 발견된 패턴이 있으면 rationale에 추가
    if found_patterns:
        rationale += f" (발견된 패턴: {', '.join(found_patterns[:3])})"  # 최대 3개만 표시
    
    return {
        "label": label,
        "score": round(score, 3),
        "rationale": rationale
    }