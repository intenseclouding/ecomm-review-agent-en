from strands import tool
from typing import List, Dict

# 키워드 저장 파일 경로
import os
KEYWORDS_FILE = os.path.join(os.path.dirname(__file__), "registered_keywords.json")


def _load_keywords() -> Dict[str, List[str]]:
    """등록된 키워드 목록 로드"""
    import os, json
    if os.path.exists(KEYWORDS_FILE):
        with open(KEYWORDS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

@tool
def get_all_keywords() -> Dict[str, List[str]]:
    """모든 등록된 키워드 반환 (Agent 도구)"""
    keywords = _load_keywords()
    return {
        "status": "success",
        "keywords": keywords,
        "total_keywords": len(keywords)
    }

def get_all_keywords_direct() -> Dict[str, List[str]]:
    """모든 등록된 키워드 반환 (직접 호출용)"""
    return _load_keywords()

