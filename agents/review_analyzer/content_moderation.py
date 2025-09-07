"""
리뷰 내용 검수 및 모더레이션 도구
공격적이고 선정적인 언어를 탐지하여 부적절한 리뷰를 필터링합니다.
"""

from strands import tool
import re
from typing import Dict, List, Any

# 공격적 언어 패턴
AGGRESSIVE_PATTERNS = [
    # 욕설 및 비속어
    r'(바보|멍청|병신|미친|개새끼|씨발|좆|존나|개같|쓰레기)',
    # 공격적 표현
    r'(죽어|뒤져|꺼져|닥쳐|엿먹어|개판|최악|쓰레기같|더러워)',
    # 차별적 표현
    r'(장애인|정신병|미개|후진국|열등)',
    # 협박성 표현
    r'(고발|신고|고소|죽이|때리|박살|망하|파산)'
]

# 선정적 언어 패턴
SEXUAL_PATTERNS = [
    r'(섹스|성관계|야동|포르노|AV|19금|성인|야한|음란|변태)',
    r'(가슴|엉덩이|성기|자위|오르가즘|섹시|야해|꼴려|발정)',
    r'(원나잇|불륜|바람|외도|성매매|조건만남)'
]

# 스팸성 패턴
SPAM_PATTERNS = [
    r'(http[s]?://|www\.|\.com|\.kr|\.net)',  # URL
    r'(\d{2,3}-\d{3,4}-\d{4})',  # 전화번호
    r'(카톡|카카오톡|텔레그램|라인|위챗)',  # 메신저
    r'(대출|투자|수익|돈벌기|부업|알바)',  # 금융 스팸
    r'(광고|홍보|마케팅|프로모션|이벤트|할인쿠폰)'  # 광고성
]

@tool
def moderate_review_content(review_text: str) -> Dict[str, Any]:
    """
    리뷰 내용을 검수하여 부적절한 내용을 탐지합니다.
    
    Args:
        review_text (str): 검수할 리뷰 텍스트
        
    Returns:
        Dict[str, Any]: 검수 결과
    """
    
    issues = []
    severity_score = 0
    detected_patterns = []
    
    # 공격적 언어 검사
    for pattern in AGGRESSIVE_PATTERNS:
        matches = re.findall(pattern, review_text, re.IGNORECASE)
        if matches:
            issues.append(f"공격적 언어 감지: {', '.join(set(matches))}")
            severity_score += 30
            detected_patterns.extend(matches)
    
    # 선정적 언어 검사
    for pattern in SEXUAL_PATTERNS:
        matches = re.findall(pattern, review_text, re.IGNORECASE)
        if matches:
            issues.append(f"선정적 언어 감지: {', '.join(set(matches))}")
            severity_score += 25
            detected_patterns.extend(matches)
    
    # 스팸성 내용 검사
    for pattern in SPAM_PATTERNS:
        matches = re.findall(pattern, review_text, re.IGNORECASE)
        if matches:
            issues.append(f"스팸성 내용 감지: {', '.join(set(matches))}")
            severity_score += 20
            detected_patterns.extend(matches)
    
    # 추가 검사 항목들
    
    # 과도한 반복 문자 검사
    repeated_chars = re.findall(r'(.)\1{4,}', review_text)
    if repeated_chars:
        issues.append("과도한 반복 문자 사용")
        severity_score += 10
    
    # 과도한 특수문자 검사
    special_char_ratio = len(re.findall(r'[!@#$%^&*()_+=\[\]{}|;:,.<>?]', review_text)) / len(review_text) if review_text else 0
    if special_char_ratio > 0.3:
        issues.append("과도한 특수문자 사용")
        severity_score += 15
    
    # 길이 검사
    if len(review_text.strip()) < 5:
        issues.append("리뷰 내용이 너무 짧음")
        severity_score += 20
    elif len(review_text) > 1000:
        issues.append("리뷰 내용이 너무 김")
        severity_score += 10
    
    # 전체 대문자 검사 (한글 제외)
    english_text = re.sub(r'[^a-zA-Z]', '', review_text)
    if len(english_text) > 10 and english_text.isupper():
        issues.append("과도한 대문자 사용")
        severity_score += 10
    
    # 검수 결과 판정 (더 엄격한 기준 적용)
    if severity_score >= 25:
        decision = "거부"
        reason = "부적절한 내용 포함"
    elif severity_score >= 15:
        decision = "경고"
        reason = "일부 부적절한 내용 포함, 수정 필요"
    elif severity_score >= 10:
        decision = "주의"
        reason = "주의가 필요한 내용"
    else:
        decision = "승인"
        reason = "적절한 내용"
    
    return {
        "is_approved": decision == "승인",
        "decision": decision,
        "reason": reason,
        "severity_score": severity_score,
        "issues": issues,
        "detected_patterns": list(set(detected_patterns)),
        "review_length": len(review_text),
        "clean_text": review_text  # 필요시 정제된 텍스트 반환
    }

@tool
def get_moderation_statistics(reviews: List[str]) -> Dict[str, Any]:
    """
    여러 리뷰에 대한 검수 통계를 제공합니다.
    
    Args:
        reviews (List[str]): 검수할 리뷰 목록
        
    Returns:
        Dict[str, Any]: 검수 통계
    """
    
    total_reviews = len(reviews)
    approved = 0
    rejected = 0
    warnings = 0
    
    common_issues = {}
    
    for review in reviews:
        result = moderate_review_content(review)
        
        if result["decision"] == "승인":
            approved += 1
        elif result["decision"] == "거부":
            rejected += 1
        else:
            warnings += 1
        
        # 이슈 통계 수집
        for issue in result["issues"]:
            issue_type = issue.split(":")[0] if ":" in issue else issue
            common_issues[issue_type] = common_issues.get(issue_type, 0) + 1
    
    return {
        "total_reviews": total_reviews,
        "approved": approved,
        "rejected": rejected,
        "warnings": warnings,
        "approval_rate": (approved / total_reviews * 100) if total_reviews > 0 else 0,
        "common_issues": common_issues
    }

# 테스트용 함수
if __name__ == "__main__":
    # 테스트 케이스들
    test_reviews = [
        "이 제품 정말 좋아요! 품질도 만족스럽고 배송도 빨라서 만족합니다.",  # 정상
        "이 제품 완전 쓰레기네요. 돈 아까워 죽겠어요.",  # 공격적
        "섹시한 디자인이 마음에 들어요 ㅎㅎ",  # 선정적
        "www.spam-site.com에서 더 싸게 팔아요!",  # 스팸
        "ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ",  # 반복문자
        "좋음"  # 너무 짧음
    ]
    
    print("=== 리뷰 검수 테스트 ===")
    for i, review in enumerate(test_reviews, 1):
        result = moderate_review_content(review)
        print(f"\n{i}. 리뷰: {review}")
        print(f"   결과: {result['decision']} ({result['reason']})")
        print(f"   점수: {result['severity_score']}")
        if result['issues']:
            print(f"   이슈: {', '.join(result['issues'])}")