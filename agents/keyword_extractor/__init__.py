"""
키워드 추출기 에이전트

이 모듈은 리뷰 텍스트에 대한 키워드 추출 및 검색 기능을 제공합니다.
Claude 3.7을 사용하여 한국어 리뷰 텍스트에서 1-5개의 관련 키워드를 추출하고
키워드 기반 검색 기능을 제공합니다.
"""

from .agent import keyword_extractor_agent, get_product_terms
from .tools import extract_keywords, upsert_review, search_reviews_by_keyword

__all__ = ['keyword_extractor_agent', 'get_product_terms', 'extract_keywords', 'upsert_review', 'search_reviews_by_keyword']