import unittest
import sys
import os

# agents 모듈을 import하기 위한 경로 추가
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from review_analyzer.agent import analyze_review_for_storage
from review_analyzer.tools import sentiment_analysis, extract_keywords, detect_spam_or_fake, categorize_review_topic

class TestReviewAnalyzer(unittest.TestCase):
    
    def setUp(self):
        """테스트 데이터 설정"""
        self.positive_review = "음질이 정말 좋아요! 노이즈 캔슬링 기능도 훌륭하고 배터리도 오래 갑니다. 강력 추천합니다!"
        self.negative_review = "제 피부에는 맞지 않는 것 같아요. 사용 후 트러블이 생겼습니다. 개인차가 있는 것 같네요."
        self.neutral_review = "디자인은 좋은데 사이즈가 좀 작은 것 같아요. 한 사이즈 크게 주문하시는 걸 추천합니다."
        self.spam_review = "할인코드 SAVE50으로 50% 할인받으세요!!! 링크: http://fake-site.com"
    
    def test_sentiment_analysis_positive(self):
        """긍정적 리뷰 감정 분석 테스트"""
        result = sentiment_analysis(self.positive_review)
        
        self.assertIn("sentiment_label", result)
        self.assertIn("polarity", result)
        self.assertIn("confidence", result)
        self.assertEqual(result["sentiment_label"], "긍정")
        self.assertGreater(result["polarity"], 0)
    
    def test_sentiment_analysis_negative(self):
        """부정적 리뷰 감정 분석 테스트"""
        result = sentiment_analysis(self.negative_review)
        
        self.assertIn("sentiment_label", result)
        self.assertIn("polarity", result)
        self.assertIn("confidence", result)
        # 부정적이거나 중립적이어야 함
        self.assertIn(result["sentiment_label"], ["부정", "중립"])
    
    def test_extract_keywords(self):
        """키워드 추출 테스트"""
        result = extract_keywords(self.positive_review, max_keywords=5)
        
        self.assertIsInstance(result, list)
        self.assertLessEqual(len(result), 5)
        
        # 예상되는 키워드들이 포함되어 있는지 확인
        expected_keywords = ["음질", "노이즈", "캔슬링", "배터리", "추천"]
        found_keywords = [kw for kw in expected_keywords if any(kw in r for r in result)]
        self.assertGreater(len(found_keywords), 0)
    
    def test_detect_spam_normal_review(self):
        """정상 리뷰 스팸 검사 테스트"""
        result = detect_spam_or_fake(self.positive_review)
        
        self.assertIn("is_suspicious", result)
        self.assertIn("risk_score", result)
        self.assertIn("indicators", result)
        self.assertFalse(result["is_suspicious"])
        self.assertLess(result["risk_score"], 0.5)
    
    def test_detect_spam_suspicious_review(self):
        """의심스러운 리뷰 스팸 검사 테스트"""
        result = detect_spam_or_fake(self.spam_review)
        
        self.assertIn("is_suspicious", result)
        self.assertIn("risk_score", result)
        self.assertIn("indicators", result)
        self.assertTrue(result["is_suspicious"])
        self.assertGreater(result["risk_score"], 0.5)
    
    def test_categorize_review_topic(self):
        """리뷰 주제 분류 테스트"""
        keywords = ["음질", "배터리", "기능"]
        result = categorize_review_topic(self.positive_review, keywords)
        
        self.assertIn("primary_topic", result)
        self.assertIn("topic_scores", result)
        self.assertIn("all_topics", result)
        
        # 품질이나 사용성 관련 주제가 나와야 함
        expected_topics = ["품질", "사용성", "기타"]
        self.assertIn(result["primary_topic"], expected_topics)
    
    def test_analyze_review_for_storage_success(self):
        """구조화된 리뷰 분석 성공 테스트"""
        result = analyze_review_for_storage(self.positive_review, "PROD-001")
        
        self.assertTrue(result["success"])
        self.assertIn("structured_data", result)
        
        structured_data = result["structured_data"]
        self.assertIn("keywords", structured_data)
        self.assertIn("sentiment", structured_data)
        self.assertIn("analysis_completed", structured_data)
        
        # 키워드가 리스트인지 확인
        self.assertIsInstance(structured_data["keywords"], list)
        
        # 감정 데이터 구조 확인
        sentiment = structured_data["sentiment"]
        self.assertIn("label", sentiment)
        self.assertIn("confidence", sentiment)
        self.assertIn("polarity", sentiment)
    
    def test_analyze_review_for_storage_empty_text(self):
        """빈 텍스트 분석 테스트"""
        result = analyze_review_for_storage("", "PROD-001")
        
        # 빈 텍스트도 기본값으로 처리되어야 함
        self.assertIn("structured_data", result)
        structured_data = result["structured_data"]
        self.assertIsInstance(structured_data["keywords"], list)
        self.assertIn("sentiment", structured_data)

class TestReviewAnalyzerIntegration(unittest.TestCase):
    """통합 테스트"""
    
    def test_full_analysis_pipeline(self):
        """전체 분석 파이프라인 테스트"""
        test_reviews = [
            "정말 만족스러운 제품입니다! 품질도 좋고 가격도 합리적이에요.",
            "배송이 늦었지만 제품 자체는 괜찮네요.",
            "완전 실망이에요. 돈 아까워요. 환불하고 싶습니다."
        ]
        
        for review in test_reviews:
            result = analyze_review_for_storage(review)
            
            # 모든 리뷰가 성공적으로 분석되어야 함
            self.assertIn("structured_data", result)
            
            structured_data = result["structured_data"]
            
            # 필수 필드들이 모두 있는지 확인
            self.assertIn("keywords", structured_data)
            self.assertIn("sentiment", structured_data)
            self.assertIn("analysis_completed", structured_data)
            
            # 감정 라벨이 유효한지 확인
            sentiment_label = structured_data["sentiment"]["label"]
            self.assertIn(sentiment_label, ["긍정", "부정", "중립"])

if __name__ == "__main__":
    unittest.main()