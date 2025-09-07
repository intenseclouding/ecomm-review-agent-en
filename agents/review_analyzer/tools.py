from strands import tool
from textblob import TextBlob
import json
import re
from typing import Dict, List, Any

@tool
def sentiment_analysis(review_text: str) -> Dict[str, Any]:
    """
    리뷰 텍스트의 감정을 분석합니다.
    
    Args:
        review_text (str): 분석할 리뷰 텍스트
        
    Returns:
        Dict[str, Any]: 감정 분석 결과 (polarity, subjectivity, sentiment_label)
    """
    blob = TextBlob(review_text)
    polarity = blob.sentiment.polarity  # -1 (부정) ~ 1 (긍정)
    subjectivity = blob.sentiment.subjectivity  # 0 (객관적) ~ 1 (주관적)
    
    # 감정 라벨 결정
    if polarity > 0.1:
        sentiment_label = "긍정"
    elif polarity < -0.1:
        sentiment_label = "부정"
    else:
        sentiment_label = "중립"
    
    return {
        "polarity": round(polarity, 3),
        "subjectivity": round(subjectivity, 3),
        "sentiment_label": sentiment_label,
        "confidence": abs(polarity)
    }

@tool
def extract_keywords(review_text: str, max_keywords: int = 10) -> List[str]:
    """
    리뷰 텍스트에서 주요 키워드를 추출합니다.
    
    Args:
        review_text (str): 키워드를 추출할 리뷰 텍스트
        max_keywords (int): 최대 키워드 개수
        
    Returns:
        List[str]: 추출된 키워드 리스트
    """
    # 한글, 영문, 숫자만 남기고 정리
    cleaned_text = re.sub(r'[^\w\s가-힣]', ' ', review_text)
    
    # 불용어 제거 (간단한 예시)
    stop_words = {'이', '그', '저', '것', '들', '는', '은', '을', '를', '에', '의', '가', '와', '과', '도', '만', '에서', '로', '으로', '부터', '까지', '하고', '하지만', '그런데', '그러나', '또한', '또', '및', '그리고'}
    
    words = cleaned_text.split()
    keywords = []
    
    for word in words:
        if len(word) > 1 and word not in stop_words:
            keywords.append(word)
    
    # 빈도수 기반으로 상위 키워드 반환
    from collections import Counter
    word_freq = Counter(keywords)
    top_keywords = [word for word, count in word_freq.most_common(max_keywords)]
    
    return top_keywords

@tool
def detect_spam_or_fake(review_text: str) -> Dict[str, Any]:
    """
    리뷰가 스팸이나 가짜 리뷰인지 검사합니다.
    
    Args:
        review_text (str): 검사할 리뷰 텍스트
        
    Returns:
        Dict[str, Any]: 스팸/가짜 리뷰 검사 결과
    """
    spam_indicators = []
    risk_score = 0
    
    # 길이 체크
    if len(review_text.strip()) < 10:
        spam_indicators.append("너무 짧은 리뷰")
        risk_score += 0.3
    
    # 반복 문자/단어 체크
    if re.search(r'(.)\1{4,}', review_text):
        spam_indicators.append("반복 문자 사용")
        risk_score += 0.2
    
    # 과도한 이모지 사용
    emoji_count = len(re.findall(r'[😀-🙏🌀-🗿🚀-🛿]', review_text))
    if emoji_count > len(review_text) * 0.1:
        spam_indicators.append("과도한 이모지 사용")
        risk_score += 0.2
    
    # 광고성 키워드
    ad_keywords = ['할인', '쿠폰', '링크', 'http', 'www', '추천코드', '할인코드']
    for keyword in ad_keywords:
        if keyword in review_text:
            spam_indicators.append(f"광고성 키워드 포함: {keyword}")
            risk_score += 0.3
            break
    
    is_suspicious = risk_score > 0.5
    
    return {
        "is_suspicious": is_suspicious,
        "risk_score": round(risk_score, 3),
        "indicators": spam_indicators,
        "recommendation": "승인 거부" if is_suspicious else "승인 가능"
    }

@tool
def categorize_review_topic(review_text: str, keywords: List[str]) -> Dict[str, Any]:
    """
    리뷰의 주제를 카테고리별로 분류합니다.
    
    Args:
        review_text (str): 분류할 리뷰 텍스트
        keywords (List[str]): 추출된 키워드 리스트
        
    Returns:
        Dict[str, Any]: 주제 분류 결과
    """
    categories = {
        "품질": ["품질", "질", "좋다", "나쁘다", "훌륭", "최고", "최악", "만족", "불만"],
        "배송": ["배송", "택배", "빠르다", "늦다", "포장", "박스", "배달"],
        "가격": ["가격", "비싸다", "싸다", "저렴", "비용", "돈", "가성비", "합리적"],
        "디자인": ["디자인", "예쁘다", "못생겼다", "색깔", "모양", "외관", "스타일"],
        "사용성": ["사용", "편하다", "불편", "쉽다", "어렵다", "기능", "성능"],
        "서비스": ["서비스", "친절", "불친절", "응답", "문의", "고객센터", "AS"]
    }
    
    topic_scores = {}
    text_lower = review_text.lower()
    keywords_lower = [k.lower() for k in keywords]
    
    for category, category_keywords in categories.items():
        score = 0
        matched_keywords = []
        
        for keyword in category_keywords:
            if keyword in text_lower:
                score += 2
                matched_keywords.append(keyword)
            
            # 추출된 키워드와 매칭
            for extracted_keyword in keywords_lower:
                if keyword in extracted_keyword or extracted_keyword in keyword:
                    score += 1
                    if extracted_keyword not in matched_keywords:
                        matched_keywords.append(extracted_keyword)
        
        if score > 0:
            topic_scores[category] = {
                "score": score,
                "matched_keywords": matched_keywords
            }
    
    # 가장 높은 점수의 카테고리 선택
    primary_topic = max(topic_scores.keys(), key=lambda k: topic_scores[k]["score"]) if topic_scores else "기타"
    
    return {
        "primary_topic": primary_topic,
        "topic_scores": topic_scores,
        "all_topics": list(topic_scores.keys())
    }