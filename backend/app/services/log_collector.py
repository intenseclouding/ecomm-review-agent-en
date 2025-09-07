import uuid
from datetime import datetime
from typing import Optional, Dict, Any
from ..models.product import AgentLog, AgentLogStep
from .agent_log_service import save_agent_log

class LogCollector:
    """에이전트 처리 과정의 로그를 수집하는 클래스"""
    
    def __init__(self, review_id: str):
        self.review_id = review_id
        self.session_id = f"LOG-{uuid.uuid4().hex[:8].upper()}"
        self.log = AgentLog(
            id=self.session_id,
            review_id=review_id,
            session_id=self.session_id,
            start_time=datetime.now().isoformat(),
            status="in_progress"
        )
        self.current_step: Optional[AgentLogStep] = None
    
    def start_step(self, step_name: str, details: Dict[str, Any] = None):
        """새로운 처리 단계 시작"""
        # 이전 단계가 완료되지 않았다면 완료 처리
        if self.current_step and not self.current_step.end_time:
            self.end_step()
        
        self.current_step = AgentLogStep(
            step_name=step_name,
            start_time=datetime.now().isoformat(),
            status="in_progress",
            details=details or {}
        )
        self.log.steps.append(self.current_step)
        
        # 실시간으로 로그 저장 (백업용)
        self._save_log_safely()
    
    def end_step(self, status: str = "completed", details: Dict[str, Any] = None, error: str = None):
        """현재 단계 완료"""
        if self.current_step:
            end_time = datetime.now()
            start_time = datetime.fromisoformat(self.current_step.start_time)
            
            self.current_step.end_time = end_time.isoformat()
            self.current_step.duration_ms = int((end_time - start_time).total_seconds() * 1000)
            self.current_step.status = status
            
            if details:
                self.current_step.details.update(details)
            if error:
                self.current_step.error_message = error
            
            # 실시간으로 로그 저장
            self._save_log_safely()
    
    def add_step_detail(self, key: str, value: Any):
        """현재 단계에 상세 정보 추가"""
        if self.current_step:
            self.current_step.details[key] = value
            self._save_log_safely()
    
    def complete_session(self, status: str = "completed", metadata: Dict[str, Any] = None):
        """전체 세션 완료"""
        # 마지막 단계가 완료되지 않았다면 완료 처리
        if self.current_step and not self.current_step.end_time:
            self.end_step()
        
        end_time = datetime.now()
        start_time = datetime.fromisoformat(self.log.start_time)
        
        self.log.end_time = end_time.isoformat()
        self.log.total_duration_ms = int((end_time - start_time).total_seconds() * 1000)
        self.log.status = status
        
        if metadata:
            self.log.metadata.update(metadata)
        
        # 최종 로그 저장
        success = save_agent_log(self.log)
        
        if success:
            print(f"에이전트 로그 저장 완료: {self.log.id}")
        else:
            print(f"에이전트 로그 저장 실패: {self.log.id}")
        
        return self.log
    
    def _save_log_safely(self):
        """안전한 로그 저장 (오류가 발생해도 프로세스 중단하지 않음)"""
        try:
            save_agent_log(self.log)
        except Exception as e:
            print(f"로그 저장 중 오류 (계속 진행): {e}")

class RobustLogCollector(LogCollector):
    """오류에 강한 로그 수집기"""
    
    def __init__(self, review_id: str):
        super().__init__(review_id)
        self.fallback_logs = []  # 메모리 백업
        self.error_count = 0
    
    def _save_log_safely(self):
        """향상된 안전 저장 (메모리 백업 포함)"""
        try:
            save_agent_log(self.log)
            # 성공 시 백업 로그 클리어
            self.fallback_logs.clear()
        except Exception as e:
            self.error_count += 1
            # 실패 시 메모리에 백업
            self.fallback_logs.append({
                'timestamp': datetime.now().isoformat(),
                'log_data': self.log.dict(),
                'error': str(e)
            })
            print(f"로그 저장 실패 #{self.error_count}, 메모리에 백업: {e}")
    
    def complete_session(self, status: str = "completed", metadata: Dict[str, Any] = None):
        """향상된 세션 완료 (백업 복구 시도)"""
        result = super().complete_session(status, metadata)
        
        # 백업된 로그가 있다면 복구 시도
        if self.fallback_logs:
            print(f"백업된 로그 {len(self.fallback_logs)}개 복구 시도 중...")
            for backup in self.fallback_logs:
                try:
                    backup_log = AgentLog(**backup['log_data'])
                    save_agent_log(backup_log)
                    print(f"백업 로그 복구 성공: {backup['timestamp']}")
                except Exception as e:
                    print(f"백업 로그 복구 실패: {e}")
        
        return result