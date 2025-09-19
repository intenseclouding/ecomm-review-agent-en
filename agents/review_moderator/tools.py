from strands import tool
import re
import json
from typing import Dict, List, Any, Optional

@tool
def check_profanity(content: str) -> Dict[str, Any]:
    """
    Amazon Bedrock Claude API 사용하여 리뷰 내용의 선정적/욕설 표현을 검수합니다.
    
    Args:
        content (str): 검사할 리뷰 내용
        
    Returns:
        Dict[str, Any]: 검사 결과
    """
    try:
        import boto3
        import json
        
        # Bedrock 클라이언트 초기화 (Claude 4.0 -> 3.5 사용)
        bedrock = boto3.client('bedrock-runtime', region_name='us-west-2')
        
        # Claude에게 보낼 프롬프트
        prompt = f"""
다음 리뷰 내용이 부적절한 표현을 포함하고 있는지 검수해주세요:

리뷰 내용: "{content}"

검수 기준:
1. 욕설, 비속어, 공격적 언어
2. 성적, 선정적 표현
3. 혐오 발언, 차별적 표현
4. 위협적, 폭력적 표현
5. 스팸성, 광고성 내용

한국어의 미묘한 뉘앙스와 맥락을 고려하여 판단해주세요.

응답은 다음 JSON 형식으로만 제공해주세요:
{{
  "is_appropriate": true/false,
  "confidence": 0.0-1.0,
  "detected_issues": ["감지된 문제점들"],
  "severity": "low/medium/high",
  "reason": "판단 근거"
}}
"""
        
        # Bedrock API 호출 (Claude Sonnet 4->3.5)
        response = bedrock.invoke_model(
            modelId="anthropic.claude-3-5-sonnet-20241022-v2:0",
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
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
        
        # JSON 응답 파싱
        try:
            if "```json" in claude_response:
                json_start = claude_response.find("```json") + 7
                json_end = claude_response.find("```", json_start)
                json_text = claude_response[json_start:json_end].strip()
            elif "{" in claude_response and "}" in claude_response:
                json_start = claude_response.find("{")
                json_end = claude_response.rfind("}") + 1
                json_text = claude_response[json_start:json_end]
            else:
                raise ValueError("JSON 형태를 찾을 수 없습니다.")
            
            moderation_result = json.loads(json_text)
            
            # 결과 반환
            if moderation_result.get("is_appropriate", True):
                return {
                    "status": "PASS",
                    "reason": moderation_result.get("reason", "적절한 표현입니다."),
                    "confidence": moderation_result.get("confidence", 0.9),
                    "severity": moderation_result.get("severity", "none")
                }
            else:
                return {
                    "status": "FAIL",
                    "reason": moderation_result.get("reason", "부적절한 표현이 감지되었습니다."),
                    "detected_issues": moderation_result.get("detected_issues", []),
                    "severity": moderation_result.get("severity", "medium"),
                    "confidence": moderation_result.get("confidence", 0.9)
                }
                
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Claude 응답 파싱 실패, 정규식 폴백: {e}")
            # 정규식 폴백으로 진행
            
    except Exception as e:
        # Claude API 실패 시 정규식 방식으로 폴백
        print(f"Claude API 오류, 정규식 폴백: {e}")
        
        # 강화된 한국어 욕설/부적절 표현 패턴
        profanity_patterns = [
            # 강한 욕설
            r'(씨발|시발|개새끼|병신|미친놈|좆|꺼져|죽어|개놈|새끼)',
            # 성적 표현
            r'(섹스|성관계|야동|포르노|음란|변태|야한|19금)',
            # 공격적 표현
            r'(개같은|개소리|개빡|개짜증|개못생긴|개쓰레기|개바보)',
            # 혐오 표현
            r'(쓰레기|똥|더러운|역겨운|구역질|토나와|징그러운)',
            # 비하 표현
            r'(바보|멍청|한심|찌질|루저|패배자|못생긴)',
            # 위협적 표현
            r'(죽이고|때리고|박살|망해|엿먹어|꺼져)',
            # 차별적 표현
            r'(장애인|정신병|미친|돌아이|또라이)'
        ]
        
        detected_words = []
        severity_score = 0
        
        for pattern in profanity_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                detected_words.extend(matches)
                severity_score += len(matches) * 10
        
        # 심각도 평가 (더 엄격한 기준)
        if severity_score >= 20:  # 30 -> 20으로 낮춤
            status = "FAIL"
            reason = f"심각한 욕설/부적절 표현이 감지되었습니다: {', '.join(detected_words)} (폴백 분석)"
        elif severity_score >= 5:  # 10 -> 5로 낮춤
            status = "FAIL"
            reason = f"부적절한 표현이 감지되었습니다: {', '.join(detected_words)} (폴백 분석)"
        else:
            status = "PASS"
            reason = "적절한 표현입니다. (폴백 분석)"
        
        return {
            "status": status,
            "reason": reason,
            "detected_words": detected_words,
            "severity_score": severity_score,
            "confidence": 0.6  # 폴백이므로 낮은 신뢰도
        }

@tool
def check_image_product_match(media_files: List[Dict], product_data: Dict) -> Dict[str, Any]:
    """
    Claude Vision API를 사용하여 업로드된 이미지와 제품의 관련성을 검증합니다.
    
    Args:
        media_files (List[Dict]): 업로드된 미디어 파일 정보
        product_data (Dict): 제품 정보
        
    Returns:
        Dict[str, Any]: 매칭 검사 결과
    """
    if not media_files or len(media_files) == 0:
        return {
            "status": "SKIP",
            "reason": "업로드된 이미지가 없습니다.",
            "confidence": 1.0
        }
    
    try:
        import boto3
        import base64
        import os
        from pathlib import Path
        
        # Bedrock 클라이언트 초기화
        bedrock = boto3.client('bedrock-runtime', region_name='us-west-2')
        
        product_name = product_data.get("name", "")
        product_category = product_data.get("category", "")
        
        # 첫 번째 이미지만 검사 (여러 이미지가 있을 경우)
        first_media = media_files[0]
        
        # 이미지 파일 경로 구성
        # URL에서 실제 파일 경로 추출
        image_url = first_media.get("url", "")
        if image_url.startswith("/uploads/media/"):
            # agents/review_moderator/tools.py -> backend/uploads/media/
            current_file = Path(__file__).resolve()
            project_root = current_file.parent.parent.parent
            image_path = project_root / "backend" / "uploads" / "media" / image_url.split("/")[-1]
        else:
            return {
                "status": "FAIL",
                "reason": f"지원하지 않는 이미지 URL 형식입니다: {image_url}",
                "confidence": 0.0
            }
        
        # 이미지 파일이 존재하는지 확인
        if not image_path.exists():
            return {
                "status": "FAIL",
                "reason": f"이미지 파일이 존재하지 않습니다: {image_path}",
                "confidence": 0.0
            }
        
        # 이미지를 base64로 인코딩
        with open(image_path, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
        
        # Claude Vision API 호출
        prompt = f"""
이 이미지가 다음 제품과 관련이 있는지 분석해주세요:

제품명: {product_name}
카테고리: {product_category}

다음 기준으로 판단해주세요:
1. 이미지에 해당 제품이나 관련 제품이 보이는가?
2. 이미지가 제품 카테고리와 일치하는가?
3. 이미지가 제품 리뷰용으로 적절한가?

응답은 다음 JSON 형식으로만 제공해주세요:
{{
  "is_related": true/false,
  "confidence": 0.0-1.0,
  "reason": "판단 근거",
  "detected_objects": ["이미지에서 감지된 주요 객체들"]
}}
"""
        
        # Bedrock API 호출
        response = bedrock.invoke_model(
            modelId="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/png",
                                    "data": image_data
                                }
                            },
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ]
                    }
                ]
            })
        )
        
        # 응답 파싱
        response_body = json.loads(response['body'].read())
        claude_response = response_body['content'][0]['text']
        
        # JSON 응답 파싱
        try:
            if "```json" in claude_response:
                json_start = claude_response.find("```json") + 7
                json_end = claude_response.find("```", json_start)
                json_text = claude_response[json_start:json_end].strip()
            elif "{" in claude_response and "}" in claude_response:
                json_start = claude_response.find("{")
                json_end = claude_response.rfind("}") + 1
                json_text = claude_response[json_start:json_end]
            else:
                raise ValueError("JSON 형태를 찾을 수 없습니다.")
            
            vision_result = json.loads(json_text)
            
            # 결과 반환
            if vision_result.get("is_related", False):
                return {
                    "status": "PASS",
                    "reason": vision_result.get("reason", "이미지가 제품과 관련이 있습니다."),
                    "confidence": vision_result.get("confidence", 0.8),
                    "detected_objects": vision_result.get("detected_objects", []),
                    "image_count": len(media_files),
                    "product_category": product_category
                }
            else:
                return {
                    "status": "FAIL",
                    "reason": vision_result.get("reason", "이미지가 제품과 관련이 없습니다."),
                    "confidence": vision_result.get("confidence", 0.8),
                    "detected_objects": vision_result.get("detected_objects", []),
                    "image_count": len(media_files),
                    "product_category": product_category
                }
                
        except (json.JSONDecodeError, ValueError) as e:
            return {
                "status": "FAIL",
                "reason": f"Claude Vision 응답 파싱 실패: {str(e)}",
                "confidence": 0.0
            }
            
    except Exception as e:
        # Vision API 실패 시 폴백 로직
        print(f"Claude Vision API 오류: {e}")
        
        # 파일명 기반 간단한 매칭으로 폴백
        product_name_lower = product_data.get("name", "").lower()
        product_category_lower = product_data.get("category", "").lower()
        
        # 첫 번째 이미지 파일명 확인
        first_filename = media_files[0].get("filename", "").lower()
        
        # 간단한 키워드 매칭
        category_keywords = {
            "전자제품": ["watch", "phone", "earphone", "headphone", "electronic", "device"],
            "패션": ["shirt", "jacket", "clothes", "fashion", "wear"],
            "화장품": ["serum", "cosmetic", "beauty", "skincare"]
        }
        
        relevant_keywords = category_keywords.get(product_category, [])
        
        # 제품명이나 카테고리 키워드가 파일명에 포함되어 있는지 확인
        is_related = False
        for keyword in relevant_keywords:
            if keyword in first_filename or keyword in product_name_lower:
                is_related = True
                break
        
        if is_related:
            return {
                "status": "PASS",
                "reason": f"파일명 '{first_filename}'이 제품과 관련이 있는 것으로 판단됩니다. (Vision API 폴백)",
                "confidence": 0.6,
                "image_count": len(media_files),
                "product_category": product_category
            }
        else:
            return {
                "status": "FAIL",
                "reason": f"파일명 '{first_filename}'이 제품 '{product_name}'과 관련이 없는 것으로 판단됩니다. (Vision API 폴백)",
                "confidence": 0.7,
                "image_count": len(media_files),
                "product_category": product_category
            }

@tool
def check_rating_consistency(rating: int, content: str) -> Dict[str, Any]:
    """
    Claude LLM을 사용하여 별점과 리뷰 내용의 일치성을 분석합니다.
    
    Args:
        rating (int): 별점 (1-5)
        content (str): 리뷰 내용
        
    Returns:
        Dict[str, Any]: 일치성 검사 결과
    """
    try:
        import boto3
        import json
        
        # Bedrock 클라이언트 초기화
        bedrock = boto3.client('bedrock-runtime', region_name='us-west-2')
        
        # Claude에게 보낼 프롬프트
        prompt = f"""
다음 리뷰의 별점과 내용이 일치하는지 분석해주세요:

별점: {rating}점 (1-5점 척도)
리뷰 내용: "{content}"

다음 기준으로 판단해주세요:
1. 리뷰 내용의 전반적인 감정 (긍정/부정/중립)
2. 별점과 감정의 일치성
3. 반어법, 아이러니, 복합 감정 고려
4. 한국어 맥락과 뉘앙스 이해

판단 기준:
- 별점 4-5점: 긍정적 내용 기대
- 별점 1-2점: 부정적 내용 기대  
- 별점 3점: 중립적 내용 기대

응답은 다음 JSON 형식으로만 제공해주세요:
{{
  "content_sentiment": "positive/negative/neutral",
  "sentiment_confidence": 0.0-1.0,
  "is_consistent": true/false,
  "reason": "판단 근거",
  "detected_emotions": ["감지된 감정이나 표현들"]
}}
"""
        
        # Bedrock API 호출 (이미지 검수와 동일한 모델)
        response = bedrock.invoke_model(
            modelId="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
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
        
        # JSON 응답 파싱
        try:
            if "```json" in claude_response:
                json_start = claude_response.find("```json") + 7
                json_end = claude_response.find("```", json_start)
                json_text = claude_response[json_start:json_end].strip()
            elif "{" in claude_response and "}" in claude_response:
                json_start = claude_response.find("{")
                json_end = claude_response.rfind("}") + 1
                json_text = claude_response[json_start:json_end]
            else:
                raise ValueError("JSON 형태를 찾을 수 없습니다.")
            
            sentiment_result = json.loads(json_text)
            
            # 결과 반환
            status = "PASS" if sentiment_result.get("is_consistent", True) else "FAIL"
            reason = sentiment_result.get("reason", "별점과 리뷰 내용이 일치합니다.")
            
            return {
                "status": status,
                "reason": reason,
                "rating": rating,
                "content_sentiment": sentiment_result.get("content_sentiment", "neutral"),
                "sentiment_confidence": sentiment_result.get("sentiment_confidence", 0.8),
                "detected_emotions": sentiment_result.get("detected_emotions", []),
                "confidence": sentiment_result.get("sentiment_confidence", 0.8)
            }
            
        except (json.JSONDecodeError, ValueError) as e:
            # JSON 파싱 실패 시 폴백
            return {
                "status": "FAIL",
                "reason": f"감정 분석 응답 파싱 실패: {str(e)}",
                "rating": rating,
                "confidence": 0.0
            }
            
    except Exception as e:
        # Claude API 실패 시 기존 정규식 방식으로 폴백
        print(f"Claude 감정 분석 오류, 정규식 폴백: {e}")
        
        # 간단한 폴백 로직
        positive_words = ['좋', '만족', '훌륭', '완벽', '최고', '추천']
        negative_words = ['나쁘', '싫', '별로', '실망', '후회', '최악']
        
        content_lower = content.lower()
        positive_count = sum(1 for word in positive_words if word in content_lower)
        negative_count = sum(1 for word in negative_words if word in content_lower)
        
        # 간단한 일치성 검사
        inconsistent = False
        if rating >= 4 and negative_count > positive_count:
            inconsistent = True
            reason = f"별점 {rating}점에 비해 부정적인 표현이 많습니다. (폴백 분석)"
        elif rating <= 2 and positive_count > negative_count:
            inconsistent = True
            reason = f"별점 {rating}점에 비해 긍정적인 표현이 많습니다. (폴백 분석)"
        else:
            reason = "별점과 리뷰 내용이 일치합니다. (폴백 분석)"
        
        return {
            "status": "FAIL" if inconsistent else "PASS",
            "reason": reason,
            "rating": rating,
            "confidence": 0.6  # 폴백이므로 낮은 신뢰도
        }