"""
로그 관련 유틸리티 함수들
"""
import json
import os
import traceback
from typing import Optional, Dict, Any, Callable
from datetime import datetime
from ..models.product import AgentLog

def safe_execute_with_logging(
    collector,
    step_name: str,
    func: Callable,
    *args,
    **kwargs
) -> Any:
    """
    함수를 안전하게 실행하고 로그를 기록하는 래퍼
    
    Args:
        collector: LogCollector 인스턴스
        step_name: 단계 이름
        func: 실행할 함수
        *args, **kwargs: 함수에 전달할 인자들
    
    Returns:
        함수 실행 결과 또는 None (오류 시)
    """
    collector.start_step(step_name, {
        "function_name": func.__name__,
        "args_count": len(args),
        "kwargs_keys": list(kwargs.keys())
    })
    
    try:
        result = func(*args, **kwargs)
        
        collector.end_step("completed", {
            "result_type": type(result).__name__,
            "success": True
        })
        
        return result
        
    except Exception as e:
        error_details = {
            "error_type": type(e).__name__,
            "error_message": str(e),
            "traceback": traceback.format_exc()
        }
        
        collector.end_step("failed", error_details, str(e))
        
        print(f"함수 실행 실패 ({step_name}): {e}")
        return None

def create_minimal_log(review_id: str, error_message: str) -> AgentLog:
    """
    오류 발생 시 최소한의 로그 생성
    
    Args:
        review_id: 리뷰 ID
        error_message: 오류 메시지
    
    Returns:
        최소한의 정보를 담은 AgentLog
    """
    import uuid
    
    log_id = f"LOG-{uuid.uuid4().hex[:8].upper()}"
    current_time = datetime.now().isoformat()
    
    return AgentLog(
        id=log_id,
        review_id=review_id,
        session_id=log_id,
        start_time=current_time,
        end_time=current_time,
        total_duration_ms=0,
        status="failed",
        steps=[],
        metadata={
            "error": error_message,
            "minimal_log": True,
            "created_at": current_time
        },
        is_sample=False
    )

def validate_log_data(log_data: Dict[str, Any]) -> bool:
    """
    로그 데이터의 유효성 검증
    
    Args:
        log_data: 검증할 로그 데이터
    
    Returns:
        유효성 여부
    """
    required_fields = ['id', 'review_id', 'session_id', 'start_time', 'status']
    
    try:
        # 필수 필드 확인
        for field in required_fields:
            if field not in log_data:
                print(f"필수 필드 누락: {field}")
                return False
        
        # 상태 값 확인
        valid_statuses = ['in_progress', 'completed', 'failed']
        if log_data['status'] not in valid_statuses:
            print(f"잘못된 상태 값: {log_data['status']}")
            return False
        
        # 단계 데이터 확인
        if 'steps' in log_data:
            for i, step in enumerate(log_data['steps']):
                if not isinstance(step, dict):
                    print(f"잘못된 단계 데이터 형식: {i}")
                    return False
                
                if 'step_name' not in step or 'start_time' not in step:
                    print(f"단계 필수 필드 누락: {i}")
                    return False
        
        return True
        
    except Exception as e:
        print(f"로그 데이터 검증 중 오류: {e}")
        return False

def backup_log_to_memory(log: AgentLog) -> Dict[str, Any]:
    """
    로그를 메모리에 백업
    
    Args:
        log: 백업할 로그
    
    Returns:
        백업된 로그 데이터
    """
    return {
        'timestamp': datetime.now().isoformat(),
        'log_id': log.id,
        'review_id': log.review_id,
        'log_data': log.dict(),
        'backup_reason': 'storage_failure'
    }

def restore_log_from_backup(backup_data: Dict[str, Any]) -> Optional[AgentLog]:
    """
    백업에서 로그 복원
    
    Args:
        backup_data: 백업된 로그 데이터
    
    Returns:
        복원된 AgentLog 또는 None
    """
    try:
        if 'log_data' in backup_data:
            return AgentLog(**backup_data['log_data'])
        return None
    except Exception as e:
        print(f"백업에서 로그 복원 실패: {e}")
        return None

def cleanup_old_logs(days_to_keep: int = 30) -> int:
    """
    오래된 로그 파일 정리
    
    Args:
        days_to_keep: 보관할 일수
    
    Returns:
        삭제된 파일 수
    """
    from .agent_log_service import LOGS_DIR
    
    if not os.path.exists(LOGS_DIR):
        return 0
    
    deleted_count = 0
    cutoff_time = datetime.now().timestamp() - (days_to_keep * 24 * 60 * 60)
    
    try:
        for filename in os.listdir(LOGS_DIR):
            if filename.endswith('.json'):
                file_path = os.path.join(LOGS_DIR, filename)
                file_time = os.path.getmtime(file_path)
                
                if file_time < cutoff_time:
                    os.remove(file_path)
                    deleted_count += 1
                    print(f"오래된 로그 파일 삭제: {filename}")
    
    except Exception as e:
        print(f"로그 정리 중 오류: {e}")
    
    return deleted_count

def get_log_statistics() -> Dict[str, Any]:
    """
    로그 통계 정보 조회
    
    Returns:
        로그 통계 정보
    """
    from .agent_log_service import get_all_agent_logs
    
    logs = get_all_agent_logs()
    
    if not logs:
        return {
            'total_logs': 0,
            'sample_logs': 0,
            'real_logs': 0,
            'completed_logs': 0,
            'failed_logs': 0,
            'average_duration_ms': 0
        }
    
    sample_count = sum(1 for log in logs if log.is_sample)
    completed_count = sum(1 for log in logs if log.status == 'completed')
    failed_count = sum(1 for log in logs if log.status == 'failed')
    
    # 평균 처리 시간 계산 (완료된 로그만)
    completed_logs = [log for log in logs if log.status == 'completed' and log.total_duration_ms]
    avg_duration = 0
    if completed_logs:
        avg_duration = sum(log.total_duration_ms for log in completed_logs) / len(completed_logs)
    
    return {
        'total_logs': len(logs),
        'sample_logs': sample_count,
        'real_logs': len(logs) - sample_count,
        'completed_logs': completed_count,
        'failed_logs': failed_count,
        'average_duration_ms': int(avg_duration)
    }