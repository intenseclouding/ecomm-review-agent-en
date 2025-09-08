from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .api import products, reviews
import os

app = FastAPI(
    title="제품 리뷰 자동화 API",
    description="Strands Agent를 활용한 제품 리뷰 분석 및 자동 댓글 생성 시스템",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # React 개발 서버
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 정적 파일 서빙 (업로드된 미디어 파일)
if os.path.exists("uploads"):
    app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# API 라우터 등록
app.include_router(products.router, prefix="/api", tags=["products"])
app.include_router(reviews.router, prefix="/api", tags=["reviews"])

@app.get("/")
async def root():
    return {
        "message": "제품 리뷰 자동화 API에 오신 것을 환영합니다!",
        "docs": "/docs",
        "features": [
            "제품 관리",
            "리뷰 작성 및 조회", 
            "Strands Agent 기반 리뷰 분석",
            "자동 댓글 생성 및 승인"
        ]
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "product-review-automation"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)