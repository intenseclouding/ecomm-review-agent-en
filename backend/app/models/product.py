from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime

class MediaFile(BaseModel):
    id: str
    type: str  # 'image' or 'video'
    url: str
    filename: str
    size: int
    thumbnail_url: Optional[str] = None

class SellerResponse(BaseModel):
    content: str
    date: str

class Review(BaseModel):
    id: str
    user_name: str
    rating: int
    content: str
    date: str
    verified_purchase: bool = True
    auto_response: Optional[str] = None
    response_approved: bool = False
    
    # 새로 추가되는 분석 데이터
    keywords: Optional[List[str]] = None
    sentiment: Optional[dict] = None
    analysis_completed: bool = False
    analysis_timestamp: Optional[str] = None
    
    # 셀러 응답
    seller_response: Optional[SellerResponse] = None
    
    # Agent 로그 연결
    agent_log_id: Optional[str] = None
    
    # 미디어 파일
    media_files: Optional[List[MediaFile]] = None

class Product(BaseModel):
    id: str
    name: str
    category: str
    seller_id: str
    price: int
    description: str
    image_url: str
    features: List[str]
    reviews: List[Review] = []
    
    # 계산된 필드들
    average_rating: float = 0.0
    review_count: int = 0
    rating_distribution: Dict[int, int] = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}

class ReviewCreate(BaseModel):
    user_name: Optional[str] = None
    rating: int
    content: str
    verified_purchase: bool = True

class ReviewAnalysisResult(BaseModel):
    review_id: str
    sentiment: dict
    keywords: List[str]
    spam_check: dict
    topic_analysis: dict
    overall_assessment: str
    seller_insights: str

class AutoResponseResult(BaseModel):
    review_id: str
    generated_response: str
    validation_result: dict
    final_decision: str
    confidence_score: int
    reasoning: str

class AgentLogStep(BaseModel):
    step_name: str
    start_time: str
    end_time: Optional[str] = None
    duration_ms: Optional[int] = None
    status: str  # "in_progress", "completed", "failed"
    details: dict = {}
    error_message: Optional[str] = None

class AgentLog(BaseModel):
    id: str
    review_id: str
    session_id: str
    start_time: str
    end_time: Optional[str] = None
    total_duration_ms: Optional[int] = None
    status: str  # "in_progress", "completed", "failed"
    steps: List[AgentLogStep] = []
    metadata: dict = {}
    is_sample: bool = False  # 샘플 데이터 여부