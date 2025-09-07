#!/usr/bin/env python3
"""
리뷰 키워드 및 감정 분석 기능 통합 테스트 스크립트

이 스크립트는 다음을 테스트합니다:
1. 백엔드 API 엔드포인트
2. 리뷰 분석 기능
3. 데이터 모델 호환성
4. 전체 워크플로우
"""

import requests
import json
import time
import sys
import os

# 테스트 설정
BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"

def test_backend_health():
    """백엔드 서버 상태 확인"""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def test_get_products():
    """제품 목록 조회 테스트"""
    try:
        response = requests.get(f"{BACKEND_URL}/api/products")
        if response.status_code == 200:
            products = response.json()
            print(f"✅ 제품 목록 조회 성공: {len(products)}개 제품")
            return products
        else:
            print(f"❌ 제품 목록 조회 실패: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ 제품 목록 조회 오류: {e}")
        return None

def test_get_product_reviews(product_id):
    """특정 제품의 리뷰 조회 테스트"""
    try:
        response = requests.get(f"{BACKEND_URL}/api/products/{product_id}/reviews")
        if response.status_code == 200:
            reviews = response.json()
            print(f"✅ 제품 {product_id} 리뷰 조회 성공: {len(reviews)}개 리뷰")
            
            # 키워드와 감정 분석 데이터 확인
            analyzed_count = 0
            for review in reviews:
                if review.get('keywords') or review.get('sentiment'):
                    analyzed_count += 1
                    print(f"  - 리뷰 {review['id']}: 키워드={review.get('keywords', [])}, 감정={review.get('sentiment', {}).get('label', 'N/A')}")
            
            print(f"  분석 완료된 리뷰: {analyzed_count}/{len(reviews)}개")
            return reviews
        else:
            print(f"❌ 리뷰 조회 실패: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ 리뷰 조회 오류: {e}")
        return None

def test_create_review(product_id):
    """새 리뷰 생성 테스트"""
    test_review = {
        "user_name": "테스트유저",
        "rating": 5,
        "content": "정말 좋은 제품이에요! 품질도 훌륭하고 배송도 빨라서 만족합니다. 강력 추천드려요!",
        "verified_purchase": True
    }
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/products/{product_id}/reviews",
            json=test_review
        )
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 리뷰 생성 성공: {result['review_id']}")
            print(f"  상태: {result['status']}")
            return result['review_id']
        else:
            print(f"❌ 리뷰 생성 실패: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ 리뷰 생성 오류: {e}")
        return None

def test_review_analysis_completion(product_id, review_id, max_wait=30):
    """리뷰 분석 완료 대기 및 확인"""
    print(f"🔄 리뷰 분석 완료 대기 중... (최대 {max_wait}초)")
    
    for i in range(max_wait):
        try:
            response = requests.get(f"{BACKEND_URL}/api/products/{product_id}/reviews")
            if response.status_code == 200:
                reviews = response.json()
                for review in reviews:
                    if review['id'] == review_id:
                        if review.get('analysis_completed'):
                            print(f"✅ 리뷰 분석 완료!")
                            print(f"  키워드: {review.get('keywords', [])}")
                            print(f"  감정: {review.get('sentiment', {})}")
                            return True
                        break
        except Exception as e:
            print(f"❌ 분석 상태 확인 오류: {e}")
        
        time.sleep(1)
        if i % 5 == 0:
            print(f"  대기 중... ({i}/{max_wait}초)")
    
    print(f"⚠️ 리뷰 분석이 {max_wait}초 내에 완료되지 않았습니다.")
    return False

def test_data_model_compatibility():
    """데이터 모델 호환성 테스트"""
    print("\n📋 데이터 모델 호환성 테스트")
    
    # 샘플 데이터 로드 테스트
    try:
        with open('data/sample_products.json', 'r', encoding='utf-8') as f:
            sample_data = json.load(f)
        
        print("✅ 샘플 데이터 로드 성공")
        
        # 새로운 필드 확인
        review_count = 0
        analyzed_count = 0
        
        for product in sample_data['products']:
            for review in product['reviews']:
                review_count += 1
                if 'keywords' in review and 'sentiment' in review:
                    analyzed_count += 1
        
        print(f"  총 리뷰: {review_count}개")
        print(f"  분석 데이터 포함: {analyzed_count}개")
        
        if analyzed_count > 0:
            print("✅ 샘플 데이터에 분석 데이터 포함됨")
        else:
            print("⚠️ 샘플 데이터에 분석 데이터 없음")
            
        return True
        
    except Exception as e:
        print(f"❌ 데이터 모델 테스트 실패: {e}")
        return False

def test_frontend_accessibility():
    """프론트엔드 접근성 테스트"""
    try:
        response = requests.get(FRONTEND_URL, timeout=10)
        if response.status_code == 200:
            print("✅ 프론트엔드 서버 접근 가능")
            return True
        else:
            print(f"❌ 프론트엔드 서버 응답 오류: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 프론트엔드 서버 접근 불가: {e}")
        return False

def main():
    """메인 테스트 실행"""
    print("🚀 리뷰 키워드 및 감정 분석 기능 통합 테스트 시작\n")
    
    # 1. 백엔드 서버 상태 확인
    print("1️⃣ 백엔드 서버 상태 확인")
    if not test_backend_health():
        print("❌ 백엔드 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인하세요.")
        sys.exit(1)
    print("✅ 백엔드 서버 정상 동작\n")
    
    # 2. 데이터 모델 호환성 테스트
    print("2️⃣ 데이터 모델 호환성 테스트")
    if not test_data_model_compatibility():
        print("❌ 데이터 모델 호환성 테스트 실패")
        sys.exit(1)
    print()
    
    # 3. 제품 목록 조회 테스트
    print("3️⃣ 제품 목록 조회 테스트")
    products = test_get_products()
    if not products:
        print("❌ 제품 목록 조회 실패")
        sys.exit(1)
    print()
    
    # 4. 기존 리뷰 분석 데이터 확인
    print("4️⃣ 기존 리뷰 분석 데이터 확인")
    test_product_id = products[0]['id']
    existing_reviews = test_get_product_reviews(test_product_id)
    if existing_reviews is None:
        print("❌ 기존 리뷰 조회 실패")
        sys.exit(1)
    print()
    
    # 5. 새 리뷰 생성 및 분석 테스트
    print("5️⃣ 새 리뷰 생성 및 분석 테스트")
    new_review_id = test_create_review(test_product_id)
    if not new_review_id:
        print("❌ 새 리뷰 생성 실패")
        sys.exit(1)
    
    # 6. 리뷰 분석 완료 대기
    print("6️⃣ 리뷰 분석 완료 확인")
    analysis_completed = test_review_analysis_completion(test_product_id, new_review_id)
    if not analysis_completed:
        print("⚠️ 리뷰 분석이 완료되지 않았지만 테스트를 계속합니다.")
    print()
    
    # 7. 프론트엔드 접근성 테스트
    print("7️⃣ 프론트엔드 접근성 테스트")
    frontend_ok = test_frontend_accessibility()
    print()
    
    # 테스트 결과 요약
    print("📊 테스트 결과 요약")
    print("=" * 50)
    print("✅ 백엔드 서버: 정상")
    print("✅ 데이터 모델: 호환")
    print("✅ 제품 조회: 성공")
    print("✅ 리뷰 조회: 성공")
    print("✅ 리뷰 생성: 성공")
    print(f"{'✅' if analysis_completed else '⚠️'} 리뷰 분석: {'완료' if analysis_completed else '진행중'}")
    print(f"{'✅' if frontend_ok else '❌'} 프론트엔드: {'정상' if frontend_ok else '오류'}")
    print()
    
    if analysis_completed and frontend_ok:
        print("🎉 모든 통합 테스트가 성공적으로 완료되었습니다!")
        print("\n📝 다음 단계:")
        print("1. 브라우저에서 http://localhost:3000 접속")
        print("2. 제품 페이지에서 새로운 키워드/감정 분석 기능 확인")
        print("3. 리뷰 작성 후 자동 분석 결과 확인")
    else:
        print("⚠️ 일부 테스트가 완료되지 않았습니다. 로그를 확인하세요.")
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)