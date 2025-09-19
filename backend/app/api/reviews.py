from fastapi import APIRouter, HTTPException, BackgroundTasks, File, UploadFile, Form
from typing import List, Optional
import json
import uuid
from datetime import datetime
import sys
import os
import shutil
from pathlib import Path
import boto3
from botocore.exceptions import ClientError
# agents 모듈을 import하기 위한 경로 추가
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../agents'))

# 검수 Agent import
try:
    from review_moderator.agent import moderate_review, generate_error_messages
except ImportError as e:
    print(f"검수 Agent import 실패: {e}")
    moderate_review = None
    generate_error_messages = None

# sentiment_analyzer import
try:
    from sentiment_analyzer.agent import analyze_review
    print("✅ sentiment_analyzer 시스템 로드 성공")
except ImportError as e:
    print(f"❌ sentiment_analyzer import 실패: {e}")
    analyze_review = None

# keyword_extractor import
try:
    from keyword_extractor.agent import keyword_extractor_agent
    from keyword_extractor.tools import extract_keywords, upsert_review, search_reviews_by_keyword, KeywordExtractorTools, set_db_path
    
    # 키워드 추출기 데이터베이스 초기화
    import os
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    db_path = os.path.join(project_root, 'ecommerce_reviews.db')
    set_db_path(db_path)
    
    # 데이터베이스 스키마 초기화
    tools = KeywordExtractorTools(db_path)
    tools.init_database()
    
    print("✅ keyword_extractor 시스템 로드 성공")
except ImportError as e:
    print(f"❌ keyword_extractor import 실패: {e}")
    keyword_extractor_agent = None
    extract_keywords = None
    upsert_review = None
    search_reviews_by_keyword = None

from ..models.product import Product, Review, ReviewCreate, ReviewAnalysisResult, AutoResponseResult, AgentLog, MediaFile
from ..services.database_service import database_service
from ..services.agent_log_service import load_agent_log_by_id, load_agent_log_by_review_id
from ..services.log_utils import get_log_statistics
from ..services.api_cache import get_cached_log, cache_log, get_cache_stats

router = APIRouter()

def generate_review_id():
    """리뷰 ID 생성"""
    return f"REV-{uuid.uuid4().hex[:8].upper()}"


async def run_analysis_agents(review_id: str, content: str):
    """백그라운드에서 키워드 추출 및 감정분석 실행"""
    print(f"🤖 리뷰 {review_id} 분석 시작...")
    
    analysis_results = {}
    
    # 키워드 추출 실행
    if extract_keywords:
        try:
            keywords_result = extract_keywords(content)
            analysis_results["keywords"] = keywords_result.get("keywords", [])
            print(f"✅ 키워드 추출 완료: {keywords_result}")
            
            # 키워드 데이터베이스에 저장
            if upsert_review and keywords_result.get("keywords"):
                try:
                    upsert_review(int(review_id.split('-')[1], 16), content, keywords_result["keywords"])
                    print(f"✅ 키워드 DB 저장 완료: {keywords_result['keywords']}")
                except Exception as e:
                    print(f"❌ 키워드 DB 저장 실패: {e}")
                    
        except Exception as e:
            print(f"❌ 키워드 추출 실패: {e}")
            analysis_results["keywords"] = []
    
    # 감정분석 실행
    if analyze_review:
        try:
            sentiment_analysis = analyze_review(content)
            if sentiment_analysis["success"]:
                sentiment_data = sentiment_analysis["sentiment_result"]
                analysis_results["sentiment"] = {
                    "label": sentiment_data["label"],
                    "confidence": sentiment_data["score"],
                    "polarity": 1.0 if sentiment_data["label"] == "긍정" else (-1.0 if sentiment_data["label"] == "부정" else 0.0)
                }
                print(f"✅ 감정분석 완료: {analysis_results['sentiment']}")
            else:
                analysis_results["sentiment"] = {"label": "NEU", "confidence": 0.5, "polarity": 0.0}
                print("⚠️ 감정분석 실패, 기본값 사용")
        except Exception as e:
            print(f"❌ 감정분석 실패: {e}")
            analysis_results["sentiment"] = {"label": "NEU", "confidence": 0.5, "polarity": 0.0}
    
    # 분석 결과를 리뷰에 업데이트
    try:
        update_data = {
            "keywords": analysis_results.get("keywords", []),
            "sentiment": analysis_results.get("sentiment", {"label": "중립", "confidence": 0.5, "polarity": 0.0}),
            "analysis_completed": True
        }
        
        # 리뷰 업데이트
        review = database_service.get_review_by_id(review_id)
        if review:
            for field, value in update_data.items():
                setattr(review, field, value)
            review.analysis_timestamp = datetime.now().isoformat()
            database_service.update_review(review)
            print(f"✅ 리뷰 {review_id} 분석 결과 저장 완료")
        else:
            print(f"❌ 리뷰 {review_id}를 찾을 수 없음")
            
    except Exception as e:
        print(f"❌ 분석 결과 저장 실패: {e}")
    
    print(f"🎉 리뷰 {review_id} 분석 완료!")

@router.post("/products/{product_id}/reviews")
async def create_review(
    product_id: str,
    rating: int = Form(...),
    content: str = Form(...),
    verified_purchase: bool = Form(True),
    user_name: Optional[str] = Form(None),
    media_files: List[UploadFile] = File(default=[]),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """새 리뷰 작성 - 검수 후 승인된 경우에만 저장"""
    product = database_service.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # 미디어 파일 처리
    saved_media_files = []
    if media_files:
        # backend/uploads 디렉토리 사용 (정적 파일 서빙과 동일)
        # backend/app/api/reviews.py -> backend/
        backend_root = Path(__file__).parent.parent.parent
        upload_dir = backend_root / "uploads" / "media"
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        for file in media_files:
            if file.filename:
                # 파일 확장자 검증
                allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.mp4', '.mov', '.avi'}
                file_ext = Path(file.filename).suffix.lower()
                if file_ext not in allowed_extensions:
                    continue
                
                # 고유 파일명 생성
                file_id = uuid.uuid4().hex[:8]
                new_filename = f"{file_id}_{file.filename}"
                file_path = upload_dir / new_filename
                
                # 파일 저장
                with open(file_path, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)
                
                # MediaFile 객체 생성
                media_file = MediaFile(
                    id=file_id,
                    type="image" if file_ext in {'.jpg', '.jpeg', '.png', '.gif'} else "video",
                    url=f"/uploads/media/{new_filename}",
                    filename=file.filename,
                    size=file_path.stat().st_size
                )
                saved_media_files.append(media_file)

    # 1. 검수 Agent 실행
    moderation_result = None
    if moderate_review:
        try:
            # 미디어 파일 정보를 딕셔너리 형태로 변환
            media_files_dict = []
            if saved_media_files:
                for media in saved_media_files:
                    media_files_dict.append({
                        "id": media.id,
                        "type": media.type,
                        "url": media.url,
                        "filename": media.filename,
                        "size": media.size
                    })
            
            moderation_result = moderate_review(
                review_content=content,
                rating=rating,
                product_data={
                    "id": product.id,
                    "name": product.name,
                    "category": product.category
                },
                media_files=media_files_dict if media_files_dict else None
            )
            
        except Exception as e:
            print(f"검수 Agent 실행 중 오류: {e}")
            moderation_result = {
                "success": False,
                "error": str(e),
                "moderation_result": {
                    "overall_status": "FAIL",
                    "failed_checks": ["system_error"],
                    "summary": "검수 시스템 오류"
                }
            }
    
    # 2. 리뷰 저장 (검수 결과와 관계없이 저장)
    try:
        # user_name이 제공되지 않은 경우 기본값 생성
        final_user_name = user_name or f"사용자{uuid.uuid4().hex[:6].upper()}"
        
        new_review = Review(
            id=generate_review_id(),
            user_name=final_user_name,
            rating=rating,
            content=content,
            date=datetime.now().strftime("%Y-%m-%d"),
            verified_purchase=verified_purchase,
            media_files=saved_media_files if saved_media_files else None,
            analysis_completed=False,  # 초기값을 False로 설정
            # 검수 결과 저장
            moderation_status=moderation_result["moderation_result"]["overall_status"] if moderation_result else "PENDING",
            moderation_results=json.dumps(moderation_result["moderation_result"]) if moderation_result else None,
            moderation_timestamp=datetime.now().isoformat(),
            is_approved=(moderation_result["moderation_result"]["overall_status"] == "PASS") if moderation_result else False
        )
        
        # 분석 결과가 있으면 함께 저장 (주석 처리)
        # if moderation_result["success"] and moderation_result.get("structured_data"):
        #     structured_data = moderation_result["structured_data"]
        #     structured_data["analysis_timestamp"] = datetime.now().isoformat()
        #     
        #     new_review.keywords = structured_data["keywords"]
        #     new_review.sentiment = structured_data["sentiment"]
        #     new_review.analysis_completed = structured_data["analysis_completed"]
        #     new_review.analysis_timestamp = structured_data["analysis_timestamp"]
        
        # 데이터베이스에 리뷰 추가
        database_service.add_review(product_id, new_review)
        
        # 검수 통과 시 키워드 추출 및 감정분석 자동 실행
        if moderation_result and moderation_result["moderation_result"]["overall_status"] == "PASS":
            background_tasks.add_task(run_analysis_agents, new_review.id, content)
        
    except Exception as e:
        print(f"리뷰 저장 중 오류 발생: {e}")
        raise HTTPException(
            status_code=500, 
            detail={
                "error": "리뷰 저장 중 오류가 발생했습니다.",
                "reason": "시스템 오류",
                "message": str(e)
            }
        )
    
    # 3. 검수 결과에 따른 응답 (try-catch 블록 밖에서 처리)
    if moderation_result and moderation_result["moderation_result"]["overall_status"] == "FAIL":
        # 검수 실패 시 에러 메시지와 함께 400 응답
        error_messages = []
        if generate_error_messages:
            error_messages = generate_error_messages(moderation_result["moderation_result"])
        else:
            error_messages = ["리뷰 검수에 실패했습니다."]
        
        raise HTTPException(
            status_code=400,
            detail={
                "message": "리뷰 검수에 실패했습니다.",
                "errors": error_messages,
                "failed_checks": moderation_result["moderation_result"].get("failed_checks", []),
                "review_id": new_review.id,  # 실패해도 리뷰는 저장됨
                "moderation_summary": moderation_result["moderation_result"].get("summary", "")
            }
        )
    
    # 검수 통과 시 성공 응답
    return {
        "message": "리뷰가 성공적으로 등록되었습니다.",
        "review_id": new_review.id,
        "status": "검수 통과 - 등록 완료",
        "moderation_status": moderation_result["moderation_result"]["overall_status"] if moderation_result else "PENDING",
        "analysis_completed": False
    }

@router.get("/products/{product_id}/reviews", response_model=List[Review])
async def get_product_reviews(product_id: str):
    """제품의 모든 리뷰 조회"""
    product = database_service.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product.reviews

@router.get("/reviews/{review_id}", response_model=Review)
async def get_review(review_id: str):
    """특정 리뷰 조회"""
    review = database_service.get_review_by_id(review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

@router.post("/reviews/{review_id}/approve-response")
async def approve_auto_response(review_id: str):
    """자동 생성된 댓글 승인"""
    products = database_service.load_all_products()
    
    for product in products:
        for review in product.reviews:
            if review.id == review_id:
                if review.auto_response:
                    return await update_review(review_id, {"response_approved": True})
                else:
                    raise HTTPException(status_code=400, detail="승인할 자동 댓글이 없습니다.")
    
    raise HTTPException(status_code=404, detail="Review not found")

@router.delete("/reviews/{review_id}/response")
async def reject_auto_response(review_id: str):
    """자동 생성된 댓글 거부"""
    return await update_review(review_id, {"auto_response": None, "response_approved": False})

@router.get("/reviews/{review_id}/agent-log")
async def get_agent_log_by_review(review_id: str):
    """특정 리뷰의 에이전트 로그 조회 (캐싱 적용)"""
    try:
        # 캐시 확인
        cache_key = f"review_log_{review_id}"
        cached_log = get_cached_log(cache_key)
        
        if cached_log:
            return cached_log
        
        # 먼저 리뷰가 존재하는지 확인
        products = database_service.load_all_products()
        review_found = False
        
        for product in products:
            for review in product.reviews:
                if review.id == review_id:
                    review_found = True
                    break
            if review_found:
                break
        
        if not review_found:
            raise HTTPException(status_code=404, detail="Review not found")
        
        # 로그 조회
        log = load_agent_log_by_review_id(review_id)
        if not log:
            raise HTTPException(status_code=404, detail="Agent log not found for this review")
        
        # 캐시에 저장
        cache_log(cache_key, log, ttl=600)  # 10분 캐싱
        
        return log
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"로그 조회 중 오류: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/agent-logs/{log_id}")
async def get_agent_log_by_id(log_id: str):
    """로그 ID로 에이전트 로그 조회 (캐싱 적용)"""
    try:
        # 캐시 확인
        cache_key = f"log_{log_id}"
        cached_log = get_cached_log(cache_key)
        
        if cached_log:
            return cached_log
        
        log = load_agent_log_by_id(log_id)
        if not log:
            raise HTTPException(status_code=404, detail="Agent log not found")
        
        # 캐시에 저장
        cache_log(cache_key, log, ttl=600)  # 10분 캐싱
        
        return log
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"로그 조회 중 오류: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put("/reviews/{review_id}")
async def update_review(review_id: str, update_data: dict):
    """리뷰 업데이트"""
    review = database_service.get_review_by_id(review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    updatable_fields = {
        "auto_response", "response_approved", "keywords", 
        "sentiment", "analysis_completed", "seller_response", "agent_log_id"
    }
    
    # 업데이트 가능한 필드만 업데이트
    for field, value in update_data.items():
        if field in updatable_fields:
            setattr(review, field, value)
    
    # analysis_timestamp 자동 설정
    if "analysis_completed" in update_data and update_data["analysis_completed"]:
        review.analysis_timestamp = datetime.now().isoformat()
    
    database_service.update_review(review)
    return {"message": "리뷰가 업데이트되었습니다."}

# 자동 응답 생성 함수 (주석 처리)
# async def process_auto_response_only(product_id: str, review_id: str, analysis_data: dict, seller_id: str):
#     """자동 응답만 생성하는 함수 (분석은 이미 완료된 상태)"""
#     try:
#         from auto_responder.agent import create_auto_response
#         
#         # 자동 응답 생성을 위한 구조화된 분석 데이터 준비
#         enhanced_analysis = {
#             "review_text": analysis_data.get("review_text", ""),
#             "sentiment": analysis_data.get("sentiment", {}),
#             "keywords": analysis_data.get("keywords", []),
#             "topic_analysis": analysis_data.get("topic_analysis", {}),
#             "spam_check": analysis_data.get("spam_check", {})
#         }
#         
#         response_result = create_auto_response(
#             review_analysis=enhanced_analysis,
#             seller_id=seller_id,
#             personalization_level="medium"
#         )
#         
#         if response_result["success"]:
#             # 생성된 응답을 데이터베이스에 저장
#             products = product_data_service.load_all_products()
#             for i, product in enumerate(products):
#                 for j, review in enumerate(product.reviews):
#                     if review.id == review_id:
#                         products[i].reviews[j].auto_response = "소중한 리뷰 감사합니다! 더 나은 서비스로 보답하겠습니다."
#                         product_data_service.save_products(products)
#                         break
#         
#     except Exception as e:
#         print(f"자동 응답 생성 중 오류 발생: {e}")

# 리뷰 자동화 처리 함수 (주석 처리)
# async def process_review_automation(product_id: str, review_id: str, review_content: str, seller_id: str):
#     """리뷰 자동화 처리 (분석 + 자동 응답 생성) - 기존 호환성 유지"""
#     try:
#         # 새로운 구조화된 리뷰 분석 함수 사용
#         from review_analyzer.agent import analyze_review_for_storage
#         analysis_result = analyze_review_for_storage(review_content, product_id)
#         
#         # 분석 결과를 리뷰 데이터에 저장
#         products = product_data_service.load_all_products()
#         for i, product in enumerate(products):
#             for j, review in enumerate(product.reviews):
#                 if review.id == review_id:
#                     if analysis_result["success"]:
#                         # 분석 성공 시 구조화된 데이터 저장
#                         structured_data = analysis_result["structured_data"]
#                         structured_data["analysis_timestamp"] = datetime.now().isoformat()
#                         
#                         products[i].reviews[j].keywords = structured_data["keywords"]
#                         products[i].reviews[j].sentiment = structured_data["sentiment"]
#                         products[i].reviews[j].analysis_completed = structured_data["analysis_completed"]
#                         products[i].reviews[j].analysis_timestamp = structured_data["analysis_timestamp"]
#                     else:
#                         # 분석 실패 시 기본값 설정
#                         products[i].reviews[j].keywords = []
#                         products[i].reviews[j].sentiment = {
#                             "label": "중립",
#                             "confidence": 0.5,
#                             "polarity": 0.0
#                         }
#                         products[i].reviews[j].analysis_completed = False
#                         products[i].reviews[j].analysis_timestamp = datetime.now().isoformat()
#                     
#                     product_data_service.save_products(products)
#                     break
#         
#         # 자동 응답 생성 (분석 성공 시에만)
#         if analysis_result["success"]:
#             from auto_responder.agent import create_auto_response
#             
#             # 분석된 데이터를 자동 응답 생성에 활용
#             raw_analysis = analysis_result["raw_analysis"]
#             
#             # 자동 응답 생성을 위한 구조화된 분석 데이터 준비
#             enhanced_analysis = {
#                 "review_text": review_content,
#                 "sentiment": raw_analysis["sentiment"],
#                 "keywords": raw_analysis["keywords"],
#                 "topic_analysis": raw_analysis["topic_analysis"],
#                 "spam_check": raw_analysis["spam_check"]
#             }
#             
#             response_result = create_auto_response(
#                 review_analysis=enhanced_analysis,
#                 seller_id=seller_id,
#                 personalization_level="medium"
#             )
#             
#             if response_result["success"]:
#                 # 생성된 응답을 데이터베이스에 저장
#                 products = product_data_service.load_all_products()
#                 for i, product in enumerate(products):
#                     for j, review in enumerate(product.reviews):
#                         if review.id == review_id:
#                             products[i].reviews[j].auto_response = "소중한 리뷰 감사합니다! 더 나은 서비스로 보답하겠습니다."
#                             product_data_service.save_products(products)
#                             break
#         
#     except Exception as e:
#         print(f"리뷰 자동화 처리 중 오류 발생: {e}")
#         # 분석 실패 시에도 기본 데이터는 저장
#         try:
#             products = product_data_service.load_all_products()
#             for i, product in enumerate(products):
#                 for j, review in enumerate(product.reviews):
#                     if review.id == review_id:
#                         products[i].reviews[j].keywords = []
#                         products[i].reviews[j].sentiment = {
#                             "label": "중립",
#                             "confidence": 0.5,
#                             "polarity": 0.0
#                         }
#                         products[i].reviews[j].analysis_completed = False
#                         products[i].reviews[j].analysis_timestamp = datetime.now().isoformat()
#                         product_data_service.save_products(products)
#                         break
#         except Exception as save_error:
#             print(f"기본 데이터 저장 중 오류: {save_error}")

@router.get("/keywords/{keyword}/reviews")
async def search_reviews_by_keyword_api(keyword: str):
    """키워드로 리뷰 검색"""
    try:
        # URL 디코딩
        import urllib.parse
        decoded_keyword = urllib.parse.unquote(keyword)
        print(f"키워드 검색 요청: {keyword} -> {decoded_keyword}")
        
        # 키워드 검색 함수가 없으면 직접 import 시도
        global search_reviews_by_keyword
        if not search_reviews_by_keyword:
            try:
                from keyword_extractor.tools import search_reviews_by_keyword as search_func, KeywordExtractorTools, set_db_path
                
                # 데이터베이스 초기화
                import os
                project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
                db_path = os.path.join(project_root, 'ecommerce_reviews.db')
                set_db_path(db_path)
                
                # 데이터베이스 스키마 초기화
                tools = KeywordExtractorTools(db_path)
                tools.init_database()
                
                search_reviews_by_keyword = search_func
                print("✅ 키워드 검색 시스템 동적 로드 성공")
            except Exception as init_error:
                print(f"❌ 키워드 검색 시스템 동적 로드 실패: {init_error}")
                raise HTTPException(status_code=503, detail="키워드 검색 서비스를 사용할 수 없습니다.")
        
        results = search_reviews_by_keyword(decoded_keyword)
        return {
            "keyword": decoded_keyword,
            "results": results,
            "count": len(results)
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"키워드 검색 중 오류: {e}")
        raise HTTPException(status_code=500, detail="키워드 검색 중 오류가 발생했습니다.")

@router.get("/agent-logs/stats")
async def get_agent_log_statistics():
    """에이전트 로그 통계 조회"""
    try:
        stats = get_log_statistics()
        cache_stats = get_cache_stats()
        
        return {
            "success": True,
            "statistics": stats,
            "cache_stats": cache_stats
        }
    except Exception as e:
        print(f"로그 통계 조회 중 오류: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")