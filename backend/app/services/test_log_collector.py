"""
LogCollector 테스트 스크립트
"""
import time
from .log_collector import LogCollector, RobustLogCollector

def test_basic_log_collector():
    """기본 LogCollector 테스트"""
    print("=== 기본 LogCollector 테스트 ===")
    
    collector = LogCollector("REV-TEST-001")
    
    # 1단계: 셀러 프롬프트 로드
    collector.start_step("셀러 프롬프트 로드", {
        "seller_id": "TEST-SELLER",
        "prompts_found": 5
    })
    time.sleep(0.1)  # 실제 처리 시간 시뮬레이션
    collector.end_step("completed", {
        "selected_template": "positive_template_1",
        "template_count": 3
    })
    
    # 2단계: 리뷰 분석
    collector.start_step("리뷰 분석")
    collector.add_step_detail("analysis_type", "sentiment_and_keywords")
    time.sleep(0.2)
    collector.add_step_detail("sentiment_result", {
        "label": "긍정",
        "confidence": 0.85
    })
    collector.end_step("completed", {
        "keywords": ["좋다", "만족", "추천"],
        "processing_time": "200ms"
    })
    
    # 3단계: 응답 생성
    collector.start_step("응답 생성")
    time.sleep(0.15)
    collector.end_step("completed", {
        "generated_response": "소중한 리뷰 감사합니다!",
        "personalization_applied": True
    })
    
    # 세션 완료
    log = collector.complete_session("completed", {
        "agent_version": "1.0.0",
        "total_steps": 3
    })
    
    print(f"로그 ID: {log.id}")
    print(f"총 소요시간: {log.total_duration_ms}ms")
    print(f"단계 수: {len(log.steps)}")
    
    return log

def test_robust_log_collector():
    """RobustLogCollector 테스트"""
    print("\n=== RobustLogCollector 테스트 ===")
    
    collector = RobustLogCollector("REV-TEST-002")
    
    # 단계 실행
    collector.start_step("테스트 단계 1")
    time.sleep(0.05)
    collector.end_step("completed")
    
    collector.start_step("테스트 단계 2")
    time.sleep(0.05)
    collector.end_step("failed", error="테스트 오류")
    
    log = collector.complete_session("completed")
    
    print(f"로그 ID: {log.id}")
    print(f"오류 발생 횟수: {collector.error_count}")
    
    return log

if __name__ == "__main__":
    # 테스트 실행
    log1 = test_basic_log_collector()
    log2 = test_robust_log_collector()
    
    print(f"\n테스트 완료. 생성된 로그: {log1.id}, {log2.id}")