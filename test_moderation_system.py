#!/usr/bin/env python3
"""
리뷰 검수 시스템 테스트 스크립트
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents'))

from agents.review_analyzer.content_moderation import moderate_review_content

def test_moderation_system():
    """검수 시스템 테스트"""
    
    test_cases = [
        # 정상적인 리뷰들
        {
            "text": "이 제품 정말 좋아요! 품질도 만족스럽고 배송도 빨라서 만족합니다.",
            "expected": "승인"
        },
        {
            "text": "가격 대비 성능이 훌륭하네요. 디자인도 예쁘고 사용하기 편해요.",
            "expected": "승인"
        },
        
        # 공격적인 리뷰들
        {
            "text": "이 제품 완전 쓰레기네요. 돈 아까워 죽겠어요.",
            "expected": "거부"
        },
        {
            "text": "바보같은 디자인이네요. 멍청한 회사 같아요.",
            "expected": "거부"
        },
        
        # 선정적인 리뷰들
        {
            "text": "섹시한 디자인이 마음에 들어요 ㅎㅎ",
            "expected": "거부"
        },
        
        # 스팸성 리뷰들
        {
            "text": "www.spam-site.com에서 더 싸게 팔아요! 010-1234-5678로 연락주세요",
            "expected": "거부"
        },
        
        # 경계선 케이스들
        {
            "text": "좋음",  # 너무 짧음
            "expected": "경고"
        },
        {
            "text": "ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ",  # 반복문자
            "expected": "주의"
        }
    ]
    
    print("=== 리뷰 검수 시스템 테스트 ===\n")
    
    passed = 0
    total = len(test_cases)
    
    for i, case in enumerate(test_cases, 1):
        result = moderate_review_content(case["text"])
        
        print(f"{i}. 테스트 케이스:")
        print(f"   리뷰: {case['text']}")
        print(f"   예상: {case['expected']}")
        print(f"   결과: {result['decision']} ({result['reason']})")
        print(f"   점수: {result['severity_score']}")
        
        if result['issues']:
            print(f"   이슈: {', '.join(result['issues'])}")
        
        # 결과 검증
        if result['decision'] == case['expected']:
            print("   ✅ 통과")
            passed += 1
        else:
            print("   ❌ 실패")
        
        print()
    
    print(f"=== 테스트 결과: {passed}/{total} 통과 ({passed/total*100:.1f}%) ===")
    
    return passed == total

if __name__ == "__main__":
    success = test_moderation_system()
    sys.exit(0 if success else 1)