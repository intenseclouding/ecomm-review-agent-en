"""
API 응답 캐싱 시스템
"""
import json
import time
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

class SimpleCache:
    """간단한 메모리 기반 캐시"""
    
    def __init__(self, default_ttl: int = 300):  # 5분 기본 TTL
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.default_ttl = default_ttl
    
    def get(self, key: str) -> Optional[Any]:
        """캐시에서 값 조회"""
        if key not in self.cache:
            return None
        
        entry = self.cache[key]
        
        # TTL 확인
        if time.time() > entry['expires_at']:
            del self.cache[key]
            return None
        
        entry['access_count'] += 1
        entry['last_accessed'] = time.time()
        
        return entry['value']
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """캐시에 값 저장"""
        if ttl is None:
            ttl = self.default_ttl
        
        self.cache[key] = {
            'value': value,
            'created_at': time.time(),
            'expires_at': time.time() + ttl,
            'last_accessed': time.time(),
            'access_count': 0,
            'ttl': ttl
        }
    
    def delete(self, key: str) -> bool:
        """캐시에서 값 삭제"""
        if key in self.cache:
            del self.cache[key]
            return True
        return False
    
    def clear(self) -> None:
        """전체 캐시 클리어"""
        self.cache.clear()
    
    def cleanup_expired(self) -> int:
        """만료된 캐시 항목 정리"""
        current_time = time.time()
        expired_keys = []
        
        for key, entry in self.cache.items():
            if current_time > entry['expires_at']:
                expired_keys.append(key)
        
        for key in expired_keys:
            del self.cache[key]
        
        return len(expired_keys)
    
    def get_stats(self) -> Dict[str, Any]:
        """캐시 통계 조회"""
        current_time = time.time()
        total_entries = len(self.cache)
        expired_entries = 0
        total_access_count = 0
        
        for entry in self.cache.values():
            if current_time > entry['expires_at']:
                expired_entries += 1
            total_access_count += entry['access_count']
        
        return {
            'total_entries': total_entries,
            'active_entries': total_entries - expired_entries,
            'expired_entries': expired_entries,
            'total_access_count': total_access_count,
            'cache_hit_ratio': 0 if total_entries == 0 else total_access_count / total_entries
        }

# 전역 캐시 인스턴스
agent_log_cache = SimpleCache(default_ttl=600)  # 10분 TTL

def get_cached_log(cache_key: str) -> Optional[Any]:
    """캐시된 로그 조회"""
    return agent_log_cache.get(cache_key)

def cache_log(cache_key: str, log_data: Any, ttl: int = 600) -> None:
    """로그 데이터 캐싱"""
    agent_log_cache.set(cache_key, log_data, ttl)

def invalidate_log_cache(review_id: str) -> None:
    """특정 리뷰의 로그 캐시 무효화"""
    cache_keys_to_delete = []
    
    for key in agent_log_cache.cache.keys():
        if review_id in key:
            cache_keys_to_delete.append(key)
    
    for key in cache_keys_to_delete:
        agent_log_cache.delete(key)

def get_cache_stats() -> Dict[str, Any]:
    """캐시 통계 조회"""
    return agent_log_cache.get_stats()

def cleanup_cache() -> int:
    """만료된 캐시 정리"""
    return agent_log_cache.cleanup_expired()