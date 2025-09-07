#!/bin/bash

echo "🚀 제품 리뷰 자동화 시스템 데모 시작"
echo "=================================="

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 함수 정의
check_command() {
    if command -v $1 &> /dev/null; then
        echo -e "${GREEN}✓${NC} $1 설치됨"
        return 0
    else
        echo -e "${RED}✗${NC} $1 설치되지 않음"
        return 1
    fi
}

# 필수 도구 확인
echo -e "${BLUE}1. 필수 도구 확인${NC}"
echo "-------------------"

MISSING_TOOLS=0

if ! check_command python3; then
    echo "  Python 3를 설치해주세요: https://python.org"
    MISSING_TOOLS=1
fi

if ! check_command node; then
    echo "  Node.js를 설치해주세요: https://nodejs.org"
    MISSING_TOOLS=1
fi

if ! check_command npm; then
    echo "  npm이 Node.js와 함께 설치되어야 합니다"
    MISSING_TOOLS=1
fi

if [ $MISSING_TOOLS -eq 1 ]; then
    echo -e "${RED}필수 도구가 누락되었습니다. 설치 후 다시 실행해주세요.${NC}"
    exit 1
fi

echo ""

# Python 가상환경 설정
echo -e "${BLUE}2. Python 가상환경 설정${NC}"
echo "------------------------"

if [ ! -d "venv" ]; then
    echo "가상환경 생성 중..."
    python3 -m venv venv
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓${NC} 가상환경 생성 완료"
    else
        echo -e "${RED}✗${NC} 가상환경 생성 실패"
        exit 1
    fi
else
    echo -e "${GREEN}✓${NC} 가상환경이 이미 존재합니다"
fi

# 가상환경 활성화
echo "가상환경 활성화 중..."
source venv/bin/activate
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} 가상환경 활성화 완료"
else
    echo -e "${RED}✗${NC} 가상환경 활성화 실패"
    exit 1
fi

echo ""

# 백엔드 의존성 설치
echo -e "${BLUE}3. 백엔드 의존성 설치${NC}"
echo "----------------------"

cd backend
if [ -f "requirements.txt" ]; then
    echo "Python 패키지 설치 중..."
    pip install -r requirements.txt
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓${NC} 백엔드 의존성 설치 완료"
    else
        echo -e "${RED}✗${NC} 백엔드 의존성 설치 실패"
        exit 1
    fi
else
    echo -e "${RED}✗${NC} requirements.txt 파일을 찾을 수 없습니다"
    exit 1
fi

cd ..

# Agents 의존성 설치
echo "Agents 의존성 설치 중..."
cd agents
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓${NC} Agents 의존성 설치 완료"
    else
        echo -e "${RED}✗${NC} Agents 의존성 설치 실패"
        exit 1
    fi
else
    echo -e "${RED}✗${NC} agents/requirements.txt 파일을 찾을 수 없습니다"
    exit 1
fi

cd ..
echo ""

# 프론트엔드 의존성 설치
echo -e "${BLUE}4. 프론트엔드 의존성 설치${NC}"
echo "-------------------------"

cd frontend
if [ -f "package.json" ]; then
    echo "Node.js 패키지 설치 중..."
    npm install
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓${NC} 프론트엔드 의존성 설치 완료"
    else
        echo -e "${RED}✗${NC} 프론트엔드 의존성 설치 실패"
        exit 1
    fi
else
    echo -e "${RED}✗${NC} package.json 파일을 찾을 수 없습니다"
    exit 1
fi

cd ..
echo ""

# 기존 프로세스 정리
echo -e "${BLUE}5. 기존 프로세스 정리${NC}"
echo "---------------------"

echo "기존 서버 프로세스 확인 및 정리 중..."

# 8000번 포트 정리
if lsof -ti:8000 > /dev/null 2>&1; then
    echo "8000번 포트 사용 중인 프로세스 종료 중..."
    kill -9 $(lsof -ti:8000) 2>/dev/null || true
    echo -e "${GREEN}✓${NC} 8000번 포트 정리 완료"
else
    echo -e "${GREEN}✓${NC} 8000번 포트 사용 가능"
fi

# 3000번 포트 정리
if lsof -ti:3000 > /dev/null 2>&1; then
    echo "3000번 포트 사용 중인 프로세스 종료 중..."
    kill -9 $(lsof -ti:3000) 2>/dev/null || true
    echo -e "${GREEN}✓${NC} 3000번 포트 정리 완료"
else
    echo -e "${GREEN}✓${NC} 3000번 포트 사용 가능"
fi

echo ""

# 서버 실행
echo -e "${BLUE}6. 서버 실행${NC}"
echo "-------------"

echo -e "${YELLOW}백엔드 서버를 백그라운드에서 시작합니다...${NC}"
echo "포트: 8000"
echo "URL: http://localhost:8000"

# 백그라운드에서 백엔드 서버 실행 (로그 파일로 리다이렉트)
cd backend
nohup python -m app.main > ../backend.log 2>&1 &
BACKEND_PID=$!

# 서버 시작 대기
echo "백엔드 서버 시작 대기 중..."
sleep 3

# 백엔드 서버 상태 확인
BACKEND_READY=false
for i in {1..10}; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} 백엔드 서버 실행 중 (PID: $BACKEND_PID)"
        BACKEND_READY=true
        break
    else
        echo "백엔드 서버 시작 중... ($i/10)"
        sleep 2
    fi
done

if [ "$BACKEND_READY" = false ]; then
    echo -e "${RED}✗${NC} 백엔드 서버 시작 실패"
    echo "로그 확인: tail -f backend.log"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

cd ..

echo ""
echo -e "${YELLOW}프론트엔드 서버를 백그라운드에서 시작합니다...${NC}"
echo "포트: 3000"
echo "URL: http://localhost:3000"

# 프론트엔드 서버 백그라운드 실행 (로그 파일로 리다이렉트)
cd frontend
nohup npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!

# 프론트엔드 서버 시작 대기
echo "프론트엔드 서버 시작 대기 중..."
sleep 5

# 프론트엔드 서버 상태 확인
FRONTEND_READY=false
for i in {1..15}; do
    if curl -s http://localhost:3000 > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} 프론트엔드 서버 실행 중 (PID: $FRONTEND_PID)"
        FRONTEND_READY=true
        break
    else
        echo "프론트엔드 서버 시작 중... ($i/15)"
        sleep 2
    fi
done

if [ "$FRONTEND_READY" = false ]; then
    echo -e "${YELLOW}⚠${NC} 프론트엔드 서버 상태 확인 실패 (계속 시작 중일 수 있음)"
    echo "로그 확인: tail -f frontend.log"
fi

cd ..

echo ""
if [ "$BACKEND_READY" = true ] && [ "$FRONTEND_READY" = true ]; then
    echo -e "${GREEN}🎉 데모 시스템이 성공적으로 시작되었습니다!${NC}"
    echo "============================================="
elif [ "$BACKEND_READY" = true ]; then
    echo -e "${YELLOW}⚠️  백엔드는 실행 중, 프론트엔드는 시작 중입니다${NC}"
    echo "============================================="
else
    echo -e "${RED}❌ 시스템 시작에 문제가 있습니다${NC}"
    echo "============================================="
fi

echo ""
echo -e "${BLUE}📊 서버 상태:${NC}"
echo "• 백엔드 (포트 8000): $([ "$BACKEND_READY" = true ] && echo -e "${GREEN}실행 중${NC}" || echo -e "${RED}실행 실패${NC}")"
echo "• 프론트엔드 (포트 3000): $([ "$FRONTEND_READY" = true ] && echo -e "${GREEN}실행 중${NC}" || echo -e "${YELLOW}시작 중${NC}")"
echo ""
echo -e "${BLUE}🌐 접속 정보:${NC}"
echo "• 프론트엔드: http://localhost:3000"
echo "• 백엔드 API: http://localhost:8000"
echo "• API 문서: http://localhost:8000/docs"
echo ""
echo -e "${BLUE}🛍️ 샘플 제품 페이지:${NC}"
echo "• 무선 이어폰: http://localhost:3000/product/PROD-001"
echo "• 크롭 니트: http://localhost:3000/product/PROD-002"
echo "• 비타민 세럼: http://localhost:3000/product/PROD-003"
echo "• 스마트 워치: http://localhost:3000/product/PROD-004"
echo "• 데님 자켓: http://localhost:3000/product/PROD-005"
echo ""
echo -e "${BLUE}🛡️ 새로운 검수 시스템 테스트:${NC}"
echo "1. 위 URL 중 하나로 접속"
echo "2. '리뷰 작성' 버튼 클릭"
echo "3. 부적절한 내용(욕설, 스팸 등) 입력해보기"
echo "4. 검수 시스템이 자동으로 차단하는지 확인"
echo "5. 정상적인 리뷰 작성 후 자동 분석 및 댓글 생성 확인"
echo ""
echo -e "${BLUE}📋 로그 확인:${NC}"
echo "• 백엔드 로그: tail -f backend.log"
echo "• 프론트엔드 로그: tail -f frontend.log"
echo ""
echo -e "${RED}🛑 종료하려면 Ctrl+C를 누르세요${NC}"

# 종료 시그널 처리
cleanup() {
    echo ""
    echo -e "${YELLOW}서버를 종료합니다...${NC}"
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo -e "${GREEN}✓${NC} 모든 서버가 종료되었습니다"
    exit 0
}

trap cleanup SIGINT SIGTERM

# 서버들이 실행 중인 동안 대기
wait