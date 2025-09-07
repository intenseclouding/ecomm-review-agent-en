---
inclusion: always
---

# 포트 관리 가이드라인

## 기본 원칙

- 항상 고정된 포트를 사용하여 일관성 유지
- 새로운 서버를 띄우기 전에 기존 프로세스를 정리
- 포트 충돌 방지를 위한 체계적인 관리

## 표준 포트 할당

### 백엔드 서버

- **포트**: 8000
- **용도**: FastAPI 백엔드 서버
- **URL**: http://localhost:8000

### 프론트엔드 서버

- **포트**: 3000
- **용도**: Next.js 개발 서버
- **URL**: http://localhost:3000

## 서버 시작 전 필수 작업

### 1. 기존 프로세스 확인 및 정리

```bash
# 포트 사용 중인 프로세스 확인
lsof -ti:8000  # 백엔드
lsof -ti:3000  # 프론트엔드

# 프로세스 종료
kill -9 $(lsof -ti:8000)  # 백엔드 프로세스 종료
kill -9 $(lsof -ti:3000)  # 프론트엔드 프로세스 종료
```

### 2. 서버 시작 명령어 (백그라운드 실행 권장)

#### 백그라운드 실행 원칙

- **AI 어시스턴트 사용 시 필수**: 포그라운드 실행 시 터미널이 블록되어 응답을 받을 수 없음
- **백그라운드 실행으로 서버 상태 즉시 확인 가능**
- **로그 파일을 통한 실시간 모니터링**

#### 백엔드 서버 시작 (백그라운드)

```bash
# 1. 기존 프로세스 정리
kill -9 $(lsof -ti:8000) 2>/dev/null || true

# 2. 가상환경 활성화 및 백그라운드 서버 시작
source venv/bin/activate
cd backend
nohup uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 > ../backend.log 2>&1 &

# 3. 서버 시작 확인
sleep 2
curl -s http://localhost:8000/health || echo "Backend server starting..."
```

#### 프론트엔드 서버 시작 (백그라운드)

```bash
# 1. 기존 프로세스 정리
kill -9 $(lsof -ti:3000) 2>/dev/null || true

# 2. 백그라운드 개발 서버 시작
cd frontend
nohup npm run dev > ../frontend.log 2>&1 &

# 3. 서버 시작 확인
sleep 3
curl -s http://localhost:3000 > /dev/null && echo "Frontend server started" || echo "Frontend server starting..."
```

#### 포그라운드 실행 (로컬 개발용)

```bash
# 백엔드 포그라운드 실행
source venv/bin/activate
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 프론트엔드 포그라운드 실행
cd frontend
npm run dev
```

## 포트 충돌 해결 방법

### 문제 상황

- "Address already in use" 에러 발생
- 포트가 이미 사용 중인 경우

### 해결 단계

1. **프로세스 확인**: `lsof -ti:포트번호`
2. **프로세스 종료**: `kill -9 프로세스ID`
3. **서버 재시작**: 해당 서버 시작 명령어 실행

### 예시

```bash
# 8000번 포트 문제 해결
lsof -ti:8000
kill -9 46421 53459  # 출력된 프로세스 ID들
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 3000번 포트 문제 해결
lsof -ti:3000
kill -9 12345  # 출력된 프로세스 ID
npm run dev
```

## 자동화 스크립트 활용

### run_demo.sh 사용

```bash
# 전체 시스템 시작 (포트 정리 포함)
./run_demo.sh
```

### 개별 서버 관리

```bash
# 백엔드만 재시작
./scripts/restart-backend.sh

# 프론트엔드만 재시작
./scripts/restart-frontend.sh
```

## 주의사항

- 포트 번호를 임의로 변경하지 않기
- 서버 종료 시 graceful shutdown 사용 권장
- 개발 중 포트 변경이 필요한 경우 팀과 사전 협의
- 프로덕션 환경에서는 다른 포트 정책 적용 가능

## 트러블슈팅

### 자주 발생하는 문제들

1. **포트 이미 사용 중**: 위의 프로세스 정리 방법 사용
2. **권한 문제**: sudo 없이 1024 이상 포트 사용
3. **방화벽 문제**: 로컬 개발 시 방화벽 설정 확인
4. **프로세스 좀비화**: 강제 종료 후에도 포트 점유 시 시스템 재시작

### 백그라운드 서버 관리

#### 서버 상태 확인

```bash
# 포트 사용 상태 확인
lsof -i:8000,3000

# 프로세스 확인
ps aux | grep -E "(uvicorn|npm)" | grep -v grep

# 서버 응답 테스트
curl -s http://localhost:8000/health
curl -s http://localhost:3000 > /dev/null && echo "Frontend OK"
```

#### 백그라운드 서버 종료

```bash
# 개별 서버 종료
kill -9 $(lsof -ti:8000)  # 백엔드
kill -9 $(lsof -ti:3000)  # 프론트엔드

# 모든 관련 프로세스 종료
pkill -f "uvicorn.*8000"
pkill -f "npm.*dev"
```

### 로그 확인 방법

```bash
# 서버 로그 실시간 확인
tail -f backend.log
tail -f frontend.log

# 포트 상태 모니터링
watch "lsof -i:8000,3000"

# 로그 파일 위치
# - backend.log: 프로젝트 루트/backend.log
# - frontend.log: 프로젝트 루트/frontend.log
```
