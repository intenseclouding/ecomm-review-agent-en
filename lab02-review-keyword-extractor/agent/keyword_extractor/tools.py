"""
키워드 추출기 도구

키워드 추출 및 데이터베이스 작업을 위한 핵심 도구 구현.
"""

from strands import tool
import sqlite3
import json
import os
import boto3
from typing import Dict, List, Any, Optional
from datetime import datetime


# 전역 데이터베이스 경로 - 에이전트에 의해 설정됨
_db_path = None

def set_db_path(db_path: str):
    """도구용 전역 데이터베이스 경로를 설정합니다."""
    global _db_path
    _db_path = db_path

def get_db_path() -> str:
    """데이터베이스 경로를 가져옵니다. 설정되지 않은 경우 기본값을 사용합니다."""
    global _db_path
    if _db_path is None:
        # 프로젝트 루트의 데이터베이스를 기본값으로 사용
        current_dir = os.path.dirname(__file__)
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
        _db_path = os.path.join(project_root, 'ecommerce_reviews.db')
    return _db_path


@tool
def extract_keywords(review: str) -> Dict[str, List[str]]:
    """
    리뷰 텍스트에서 1-3개의 제품 특성 관련 키워드만 추출합니다.
    
    이 도구는 한국어 리뷰 텍스트에서 제품의 구체적 특성만을 추출하며,
    감정 표현이나 일반적인 단어는 제외합니다.
    
    Args:
        review: 키워드를 추출할 리뷰 텍스트
        
    Returns:
        추출된 키워드 목록을 포함하는 'keywords' 키가 있는 딕셔너리
    """
    
    if not review or not review.strip():
        return {"keywords": []}
    
    # 제품 특성 관련 핵심 키워드만 정의
    product_keywords = {
        # 의류/패션
        "핏": ["핏", "사이즈", "크기"],
        "소재": ["소재", "재질", "원단"],
        "디자인": ["디자인", "스타일"],
        "색상": ["색상", "컬러", "색깔"],
        
        # 화장품/뷰티
        "발림성": ["발림성", "발림"],
        "커버력": ["커버력", "커버"],
        "지속력": ["지속력", "지속"],
        "질감": ["질감", "텍스처"],
        "향": ["향", "냄새", "향기"],
        
        # 전자제품
        "음질": ["음질", "소리"],
        "배터리": ["배터리", "충전"],
        "화질": ["화질", "화면"],
        "성능": ["성능", "속도"],
        "착용감": ["착용감", "착용"],
        "노이즈캔슬링": ["노이즈캔슬링", "노이즈 캔슬링", "소음차단"],
        
        # 공통 특성
        "품질": ["품질", "퀄리티"],
        "가격": ["가격", "가성비"],
        "용량": ["용량", "분량"]
    }
    
    # 제외할 의미 없는 단어들
    exclude_words = [
        "좋다", "나쁘다", "만족", "추천", "예쁘다", "아쉽다", "사용", "구매",
        "주문", "배송", "테스트", "리뷰", "완전", "정말", "너무", "대박",
        "최고", "별로", "괜찮다", "좋아요", "싫어요", "만족해요"
    ]
    
    found_keywords = []
    review_lower = review.lower()
    
    # 제품 특성 키워드 검색
    for main_keyword, variations in product_keywords.items():
        for variation in variations:
            if variation in review_lower:
                # 이미 추가된 키워드가 아니고, 제외 단어가 아닌 경우만 추가
                if main_keyword not in found_keywords and \
                   not any(exclude in variation for exclude in exclude_words):
                    found_keywords.append(main_keyword)
                    break
    
    # 최대 3개까지만 반환
    return {"keywords": found_keywords[:3]}


@tool
def upsert_review(review_id: int, text: str, keywords: List[str]) -> None:
    """
    리뷰와 키워드를 데이터베이스에 저장하거나 업데이트합니다.
    
    리뷰에는 INSERT OR REPLACE를, 키워드에는 INSERT OR IGNORE를 사용하여
    데이터 일관성을 유지하면서 중복을 방지합니다.
    
    Args:
        review_id: 리뷰의 고유 식별자
        text: 리뷰 텍스트 내용
        keywords: 리뷰와 연관된 키워드 목록
    """
    db_path = get_db_path()
    
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        try:
            # 트랜잭션 시작
            cursor.execute('BEGIN TRANSACTION')
            
            # 리뷰 테이블이 예상 스키마를 가지고 있는지 확인
            cursor.execute("PRAGMA table_info(reviews)")
            columns = [col[1] for col in cursor.fetchall()]
            
            if 'text' in columns:
                # 우리 스키마 - 리뷰 삽입 또는 교체
                cursor.execute('''
                    INSERT OR REPLACE INTO reviews (id, text, created_at)
                    VALUES (?, ?, ?)
                ''', (str(review_id), text, datetime.now()))
            else:
                # 기존 스키마 - 리뷰가 존재하는지 확인하고, 없으면 최소 항목 생성
                cursor.execute('SELECT id FROM reviews WHERE id = ?', (str(review_id),))
                if not cursor.fetchone():
                    # 기존 스키마용 최소 리뷰 항목 생성
                    cursor.execute('''
                        INSERT INTO reviews (id, product_id, user_name, rating, content, date)
                        VALUES (?, 'unknown', 'system', 5, ?, datetime('now'))
                    ''', (str(review_id), text))
                else:
                    # 기존 리뷰 내용 업데이트
                    cursor.execute('''
                        UPDATE reviews SET content = ? WHERE id = ?
                    ''', (text, str(review_id)))
            
            # 이 리뷰의 기존 키워드 관계 삭제
            cursor.execute('''
                DELETE FROM review_keywords WHERE review_id = ?
            ''', (str(review_id),))
            
            # 키워드 삽입 및 관계 생성
            for keyword in keywords:
                if keyword.strip():  # 비어있지 않은 키워드만 처리
                    # 키워드가 존재하지 않으면 삽입 (INSERT OR IGNORE)
                    cursor.execute('''
                        INSERT OR IGNORE INTO keywords (keyword) VALUES (?)
                    ''', (keyword.strip(),))
                    
                    # keyword_id 가져오기
                    cursor.execute('''
                        SELECT id FROM keywords WHERE keyword = ?
                    ''', (keyword.strip(),))
                    result = cursor.fetchone()
                    if result:
                        keyword_id = result[0]
                        
                        # 리뷰-키워드 관계 생성
                        cursor.execute('''
                            INSERT INTO review_keywords (review_id, keyword_id)
                            VALUES (?, ?)
                        ''', (str(review_id), keyword_id))
            
            # 트랜잭션 커밋
            cursor.execute('COMMIT')
            
        except Exception as e:
            # 오류 시 롤백
            cursor.execute('ROLLBACK')
            raise e


@tool
def search_reviews_by_keyword(keyword: str) -> List[Dict[str, Any]]:
    """
    키워드로 리뷰를 검색합니다.
    
    지정된 키워드를 포함하는 리뷰를 생성일 기준으로 정렬하여 반환합니다 (최신순).
    
    Args:
        keyword: 검색할 키워드
        
    Returns:
        review_id와 text 필드를 포함하는 딕셔너리 목록
    """
    db_path = get_db_path()
    
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        # 리뷰 테이블이 예상 스키마를 가지고 있는지 확인
        cursor.execute("PRAGMA table_info(reviews)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'text' in columns:
            # 우리 스키마 - text 필드와 created_at 사용
            cursor.execute('''
                SELECT DISTINCT r.id, r.text
                FROM reviews r
                JOIN review_keywords rk ON CAST(r.id AS TEXT) = CAST(rk.review_id AS TEXT)
                JOIN keywords k ON rk.keyword_id = k.id
                WHERE k.keyword = ?
                ORDER BY r.created_at DESC
            ''', (keyword,))
        else:
            # 기존 스키마 - content 필드와 date 사용
            cursor.execute('''
                SELECT DISTINCT r.id, r.content
                FROM reviews r
                JOIN review_keywords rk ON CAST(r.id AS TEXT) = CAST(rk.review_id AS TEXT)
                JOIN keywords k ON rk.keyword_id = k.id
                WHERE k.keyword = ?
                ORDER BY r.date DESC
            ''', (keyword,))
        
        results = cursor.fetchall()
        
        # 딕셔너리 목록으로 변환
        return [
            {
                'review_id': row[0],
                'text': row[1]
            }
            for row in results
        ]


class KeywordExtractorTools:
    """하위 호환성을 위한 레거시 도구 클래스."""
    
    def __init__(self, db_path: str):
        """
        데이터베이스 경로로 도구를 초기화합니다.
        
        Args:
            db_path: SQLite 데이터베이스 파일 경로
        """
        self.db_path = db_path
        set_db_path(db_path)
    
    def init_database(self):
        """필요한 테이블로 데이터베이스 스키마를 초기화합니다."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 리뷰 테이블이 존재하고 예상 구조를 가지고 있는지 확인
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='reviews'
            """)
            reviews_exists = cursor.fetchone() is not None
            
            if not reviews_exists:
                # 존재하지 않으면 우리 스키마로 리뷰 테이블 생성
                cursor.execute('''
                    CREATE TABLE reviews (
                        id INTEGER PRIMARY KEY,
                        text TEXT NOT NULL,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
            
            # 고유 제약 조건이 있는 키워드 테이블 생성
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS keywords (
                    id INTEGER PRIMARY KEY,
                    keyword TEXT UNIQUE NOT NULL
                )
            ''')
            
            # review_keywords 연결 테이블 생성
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS review_keywords (
                    review_id TEXT,
                    keyword_id INTEGER,
                    PRIMARY KEY (review_id, keyword_id),
                    FOREIGN KEY (review_id) REFERENCES reviews(id),
                    FOREIGN KEY (keyword_id) REFERENCES keywords(id)
                )
            ''')
            
            # 더 나은 검색 성능을 위한 인덱스 생성
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_keywords_keyword 
                ON keywords(keyword)
            ''')
            
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_review_keywords_keyword_id 
                ON review_keywords(keyword_id)
            ''')
            
            conn.commit()
    
    def extract_keywords(self, review: str) -> Dict[str, List[str]]:
        """레거시 메서드 - 전역 함수에 위임합니다."""
        return extract_keywords(review)
    
    def upsert_review(self, review_id: int, text: str, keywords: List[str]) -> None:
        """레거시 메서드 - 전역 함수에 위임합니다."""
        return upsert_review(review_id, text, keywords)
    
    def search_reviews_by_keyword(self, keyword: str) -> List[Dict[str, Any]]:
        """레거시 메서드 - 전역 함수에 위임합니다."""
        return search_reviews_by_keyword(keyword)