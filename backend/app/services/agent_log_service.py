import json
import os
import uuid
from typing import Optional, List
from datetime import datetime
from ..models.product import AgentLog, AgentLogStep

# 로그 데이터 저장 경로
LOGS_DIR = "../data/agent_logs"

def ensure_logs_directory():
    """로그 디렉토리가 존재하는지 확인하고 없으면 생성"""
    if not os.path.exists(LOGS_DIR):
        os.makedirs(LOGS_DIR)

def save_agent_log(log: AgentLog) -> bool:
    """에이전트 로그를 파일에 저장"""
    try:
        ensure_logs_directory()
        
        log_file_path = os.path.join(LOGS_DIR, f"{log.id}.json")
        
        with open(log_file_path, 'w', encoding='utf-8') as f:
            json.dump(log.dict(), f, ensure_ascii=False, indent=2)
        
        return True
    except Exception as e:
        print(f"로그 저장 실패: {e}")
        return False

def load_agent_log_by_id(log_id: str) -> Optional[AgentLog]:
    """로그 ID로 에이전트 로그 조회"""
    try:
        log_file_path = os.path.join(LOGS_DIR, f"{log_id}.json")
        
        if not os.path.exists(log_file_path):
            return None
        
        with open(log_file_path, 'r', encoding='utf-8') as f:
            log_data = json.load(f)
        
        return AgentLog(**log_data)
    except Exception as e:
        print(f"로그 로딩 실패: {e}")
        return None

def load_agent_log_by_review_id(review_id: str) -> Optional[AgentLog]:
    """리뷰 ID로 에이전트 로그 조회"""
    try:
        ensure_logs_directory()
        
        # 모든 로그 파일을 검색하여 해당 리뷰 ID를 찾음
        for filename in os.listdir(LOGS_DIR):
            if filename.endswith('.json'):
                log_file_path = os.path.join(LOGS_DIR, filename)
                
                with open(log_file_path, 'r', encoding='utf-8') as f:
                    log_data = json.load(f)
                
                if log_data.get('review_id') == review_id:
                    return AgentLog(**log_data)
        
        return None
    except Exception as e:
        print(f"리뷰 ID로 로그 검색 실패: {e}")
        return None

def get_all_agent_logs() -> List[AgentLog]:
    """모든 에이전트 로그 조회"""
    try:
        ensure_logs_directory()
        logs = []
        
        for filename in os.listdir(LOGS_DIR):
            if filename.endswith('.json'):
                log_file_path = os.path.join(LOGS_DIR, filename)
                
                with open(log_file_path, 'r', encoding='utf-8') as f:
                    log_data = json.load(f)
                
                logs.append(AgentLog(**log_data))
        
        return logs
    except Exception as e:
        print(f"전체 로그 조회 실패: {e}")
        return []

def delete_agent_log(log_id: str) -> bool:
    """에이전트 로그 삭제"""
    try:
        log_file_path = os.path.join(LOGS_DIR, f"{log_id}.json")
        
        if os.path.exists(log_file_path):
            os.remove(log_file_path)
            return True
        
        return False
    except Exception as e:
        print(f"로그 삭제 실패: {e}")
        return False