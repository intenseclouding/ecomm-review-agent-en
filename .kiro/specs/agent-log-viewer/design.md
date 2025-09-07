# 설계 문서

## 개요

리뷰 시스템에 Agent 로그 확인 기능을 추가하여, 각 자동 응답이 생성되는 과정을 투명하게 보여주는 시스템을 설계합니다. 에이전트의 단계별 처리 과정, 소요 시간, 셀러 프롬프트 활용 내역 등을 실시간으로 기록하고 사용자가 확인할 수 있도록 구현합니다.

## 아키텍처

### 전체 시스템 구조

```mermaid
graph TB
    A[사용자] --> B[프론트엔드 - ReviewList]
    B --> C[Agent 로그 버튼]
    C --> D[로그 뷰어 모달]
    D --> E[백엔드 API - /logs/{review_id}]
    E --> F[로그 데이터 저장소]
    
    G[자동 응답 생성 프로세스] --> H[로그 수집기]
    H --> I[실시간 로그 기록]
    I --> F
    
    J[샘플 데이터 생성기] --> K[가짜 로그 생성]
    K --> F
    
    subgraph "에이전트 처리 단계"
        L[1. 셀러 프롬프트 로드]
        M[2. 리뷰 분석]
        N[3. 응답 생성]
        O[4. 검증 및 개선]
        P[5. 최종 결정]
    end
    
    G --> L
    L --> M
    M --> N
    N --> O
    O --> P
```

### 데이터 흐름

1. **실시간 로그 기록**:
   - 자동 응답 생성 시작 → 로그 세션 생성
   - 각 처리 단계 완료 → 단계별 로그 추가
   - 전체 프로세스 완료 → 로그 세션 종료

2. **로그 조회**:
   - 사용자가 "Agent 로그확인하기" 클릭
   - API에서 해당 리뷰의 로그 데이터 조회
   - 모달에서 시간순 단계별 표시

## 컴포넌트 및 인터페이스

### 1. 데이터 모델 확장

**AgentLog 모델 추가:**

```python
class AgentLogStep(BaseModel):
    step_name: str
    start_time: str
    end_time: Optional[str] = None
    duration_ms: Optional[int] = None
    status: str  # "in_progress", "completed", "failed"
    details: Dict[str, Any] = {}
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
    metadata: Dict[str, Any] = {}
    is_sample: bool = False  # 샘플 데이터 여부

class Review(BaseModel):
    # 기존 필드들...
    id: str
    user_name: str
    rating: int
    content: str
    date: str
    verified_purchase: bool = True
    auto_response: Optional[str] = None
    response_approved: bool = False
    
    # 새로 추가되는 필드
    agent_log_id: Optional[str] = None
```

### 2. 로그 수집 시스템

**LogCollector 클래스:**

```python
class LogCollector:
    def __init__(self, review_id: str):
        self.review_id = review_id
        self.session_id = f"LOG-{uuid.uuid4().hex[:8].upper()}"
        self.log = AgentLog(
            id=self.session_id,
            review_id=review_id,
            session_id=self.session_id,
            start_time=datetime.now().isoformat(),
            status="in_progress"
        )
        self.current_step: Optional[AgentLogStep] = None
    
    def start_step(self, step_name: str, details: Dict[str, Any] = None):
        """새로운 처리 단계 시작"""
        if self.current_step and not self.current_step.end_time:
            self.end_step()
        
        self.current_step = AgentLogStep(
            step_name=step_name,
            start_time=datetime.now().isoformat(),
            status="in_progress",
            details=details or {}
        )
        self.log.steps.append(self.current_step)
    
    def end_step(self, status: str = "completed", details: Dict[str, Any] = None, error: str = None):
        """현재 단계 완료"""
        if self.current_step:
            end_time = datetime.now()
            start_time = datetime.fromisoformat(self.current_step.start_time)
            
            self.current_step.end_time = end_time.isoformat()
            self.current_step.duration_ms = int((end_time - start_time).total_seconds() * 1000)
            self.current_step.status = status
            
            if details:
                self.current_step.details.update(details)
            if error:
                self.current_step.error_message = error
    
    def complete_session(self, status: str = "completed"):
        """전체 세션 완료"""
        if self.current_step and not self.current_step.end_time:
            self.end_step()
        
        end_time = datetime.now()
        start_time = datetime.fromisoformat(self.log.start_time)
        
        self.log.end_time = end_time.isoformat()
        self.log.total_duration_ms = int((end_time - start_time).total_seconds() * 1000)
        self.log.status = status
        
        # 로그 저장
        save_agent_log(self.log)
        return self.log
```

### 3. API 엔드포인트

**새로운 엔드포인트 추가:**

```python
@router.get("/reviews/{review_id}/agent-log")
async def get_agent_log(review_id: str):
    """특정 리뷰의 에이전트 로그 조회"""
    log = load_agent_log_by_review_id(review_id)
    if not log:
        raise HTTPException(status_code=404, detail="Agent log not found")
    return log

@router.get("/agent-logs/{log_id}")
async def get_agent_log_by_id(log_id: str):
    """로그 ID로 에이전트 로그 조회"""
    log = load_agent_log_by_id(log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Agent log not found")
    return log
```

### 4. 프론트엔드 컴포넌트

#### AgentLogButton 컴포넌트

```tsx
interface AgentLogButtonProps {
  reviewId: string;
  hasLog: boolean;
}

const AgentLogButton: React.FC<AgentLogButtonProps> = ({ reviewId, hasLog }) => {
  const [showModal, setShowModal] = useState(false);

  if (!hasLog) return null;

  return (
    <>
      <button
        onClick={() => setShowModal(true)}
        className="flex items-center space-x-1 text-blue-600 hover:text-blue-800 text-sm"
      >
        <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
          <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
        </svg>
        <span>Agent 로그확인하기</span>
      </button>
      
      {showModal && (
        <AgentLogModal
          reviewId={reviewId}
          onClose={() => setShowModal(false)}
        />
      )}
    </>
  );
};
```

#### AgentLogModal 컴포넌트

```tsx
interface AgentLogModalProps {
  reviewId: string;
  onClose: () => void;
}

interface AgentLogStep {
  step_name: string;
  start_time: string;
  end_time?: string;
  duration_ms?: number;
  status: string;
  details: Record<string, any>;
  error_message?: string;
}

interface AgentLog {
  id: string;
  review_id: string;
  start_time: string;
  end_time?: string;
  total_duration_ms?: number;
  status: string;
  steps: AgentLogStep[];
  is_sample: boolean;
}

const AgentLogModal: React.FC<AgentLogModalProps> = ({ reviewId, onClose }) => {
  const [log, setLog] = useState<AgentLog | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchAgentLog();
  }, [reviewId]);

  const fetchAgentLog = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/api/reviews/${reviewId}/agent-log`);
      setLog(response.data);
    } catch (err) {
      setError('로그를 불러오는데 실패했습니다.');
    } finally {
      setLoading(false);
    }
  };

  const formatDuration = (ms: number) => {
    if (ms < 1000) return `${ms}ms`;
    return `${(ms / 1000).toFixed(1)}s`;
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <span className="text-green-500">✓</span>;
      case 'failed':
        return <span className="text-red-500">✗</span>;
      case 'in_progress':
        return <span className="text-blue-500">⟳</span>;
      default:
        return <span className="text-gray-500">○</span>;
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg max-w-4xl w-full mx-4 max-h-[90vh] overflow-hidden">
        <div className="flex items-center justify-between p-6 border-b">
          <h2 className="text-xl font-bold">Agent 처리 로그</h2>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700"
          >
            ✕
          </button>
        </div>

        <div className="p-6 overflow-y-auto max-h-[calc(90vh-120px)]">
          {loading && (
            <div className="text-center py-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto"></div>
              <p className="mt-2 text-gray-600">로그를 불러오는 중...</p>
            </div>
          )}

          {error && (
            <div className="text-center py-8">
              <p className="text-red-600">{error}</p>
            </div>
          )}

          {log && (
            <div className="space-y-6">
              {/* 로그 요약 */}
              <div className="bg-gray-50 rounded-lg p-4">
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                  <div>
                    <span className="text-gray-600">세션 ID:</span>
                    <p className="font-mono">{log.id}</p>
                  </div>
                  <div>
                    <span className="text-gray-600">전체 소요시간:</span>
                    <p className="font-semibold">
                      {log.total_duration_ms ? formatDuration(log.total_duration_ms) : '진행중'}
                    </p>
                  </div>
                  <div>
                    <span className="text-gray-600">상태:</span>
                    <p className="flex items-center space-x-1">
                      {getStatusIcon(log.status)}
                      <span>{log.status}</span>
                    </p>
                  </div>
                  <div>
                    <span className="text-gray-600">데이터 타입:</span>
                    <p className={log.is_sample ? 'text-orange-600' : 'text-green-600'}>
                      {log.is_sample ? '샘플 데이터' : '실제 데이터'}
                    </p>
                  </div>
                </div>
              </div>

              {/* 단계별 로그 */}
              <div className="space-y-4">
                <h3 className="text-lg font-semibold">처리 단계</h3>
                
                {log.steps.map((step, index) => (
                  <div key={index} className="border rounded-lg p-4">
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center space-x-2">
                        {getStatusIcon(step.status)}
                        <h4 className="font-semibold">{step.step_name}</h4>
                      </div>
                      <div className="text-sm text-gray-600">
                        {step.duration_ms ? formatDuration(step.duration_ms) : '진행중'}
                      </div>
                    </div>
                    
                    <div className="text-sm text-gray-600 mb-2">
                      시작: {new Date(step.start_time).toLocaleString()}
                      {step.end_time && (
                        <span className="ml-4">
                          완료: {new Date(step.end_time).toLocaleString()}
                        </span>
                      )}
                    </div>

                    {step.error_message && (
                      <div className="bg-red-50 border border-red-200 rounded p-2 mb-2">
                        <p className="text-red-700 text-sm">오류: {step.error_message}</p>
                      </div>
                    )}

                    {Object.keys(step.details).length > 0 && (
                      <div className="bg-blue-50 rounded p-3">
                        <h5 className="font-medium text-blue-800 mb-2">상세 정보</h5>
                        <pre className="text-xs text-blue-700 overflow-x-auto">
                          {JSON.stringify(step.details, null, 2)}
                        </pre>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
```

## 데이터 모델

### 로그 데이터 구조

```json
{
  "id": "LOG-A1B2C3D4",
  "review_id": "REV-001",
  "session_id": "LOG-A1B2C3D4",
  "start_time": "2024-01-15T10:30:00Z",
  "end_time": "2024-01-15T10:30:45Z",
  "total_duration_ms": 45230,
  "status": "completed",
  "is_sample": false,
  "steps": [
    {
      "step_name": "셀러 프롬프트 로드",
      "start_time": "2024-01-15T10:30:00Z",
      "end_time": "2024-01-15T10:30:02Z",
      "duration_ms": 2100,
      "status": "completed",
      "details": {
        "seller_id": "TECH-001",
        "prompts_loaded": {
          "positive_templates": 3,
          "negative_templates": 3,
          "neutral_templates": 2
        },
        "selected_template_type": "positive"
      }
    },
    {
      "step_name": "리뷰 분석",
      "start_time": "2024-01-15T10:30:02Z",
      "end_time": "2024-01-15T10:30:15Z",
      "duration_ms": 13200,
      "status": "completed",
      "details": {
        "sentiment_analysis": {
          "label": "긍정",
          "confidence": 0.92,
          "polarity": 0.8
        },
        "keywords_extracted": ["음질", "노이즈캔슬링", "배터리", "추천"],
        "topic_analysis": {
          "primary_topic": "품질",
          "confidence": 0.85
        },
        "spam_check": {
          "is_suspicious": false,
          "risk_score": 0.1
        }
      }
    },
    {
      "step_name": "개인화된 응답 생성",
      "start_time": "2024-01-15T10:30:15Z",
      "end_time": "2024-01-15T10:30:28Z",
      "duration_ms": 13500,
      "status": "completed",
      "details": {
        "base_template": "소중한 리뷰 감사합니다! 앞으로도 더 좋은 제품과 서비스로 보답하겠습니다.",
        "personalization_level": "medium",
        "topic_addressed": "품질",
        "keywords_mentioned": ["음질"],
        "generated_response": "음질에 대한 좋은 평가 감사합니다! 앞으로도 더 좋은 제품과 서비스로 보답하겠습니다."
      }
    },
    {
      "step_name": "응답 적절성 검증",
      "start_time": "2024-01-15T10:30:28Z",
      "end_time": "2024-01-15T10:30:35Z",
      "duration_ms": 7200,
      "status": "completed",
      "details": {
        "validation_score": 85,
        "issues_found": [],
        "sentiment_match": true,
        "length_appropriate": true,
        "recommendation": "승인"
      }
    },
    {
      "step_name": "최종 결정",
      "start_time": "2024-01-15T10:30:35Z",
      "end_time": "2024-01-15T10:30:45Z",
      "duration_ms": 10230,
      "status": "completed",
      "details": {
        "final_decision": "승인",
        "confidence_score": 85,
        "reasoning": "긍정적 리뷰에 적절한 감사 표현과 개인화된 멘트가 포함되어 있음",
        "auto_approved": false
      }
    }
  ],
  "metadata": {
    "agent_version": "1.0.0",
    "model_used": "claude-3-sonnet",
    "total_tokens": 1250,
    "processing_node": "agent-worker-01"
  }
}
```

### 샘플 로그 데이터 생성

```python
def generate_sample_log(review_id: str, review_content: str, sentiment: str) -> AgentLog:
    """샘플 리뷰를 위한 가짜 로그 데이터 생성"""
    
    base_time = datetime.now() - timedelta(minutes=random.randint(1, 60))
    
    steps = [
        {
            "step_name": "셀러 프롬프트 로드",
            "duration_range": (1500, 3000),
            "details": {
                "seller_id": "SAMPLE-SELLER",
                "prompts_loaded": {"positive_templates": 3, "negative_templates": 3},
                "selected_template_type": sentiment
            }
        },
        {
            "step_name": "리뷰 분석",
            "duration_range": (8000, 15000),
            "details": {
                "sentiment_analysis": {"label": sentiment, "confidence": random.uniform(0.7, 0.95)},
                "keywords_extracted": extract_sample_keywords(review_content),
                "topic_analysis": {"primary_topic": "품질", "confidence": random.uniform(0.8, 0.9)}
            }
        },
        {
            "step_name": "개인화된 응답 생성",
            "duration_range": (10000, 18000),
            "details": {
                "personalization_level": "medium",
                "generated_response": "샘플 자동 응답입니다."
            }
        },
        {
            "step_name": "응답 적절성 검증",
            "duration_range": (5000, 10000),
            "details": {
                "validation_score": random.randint(75, 95),
                "recommendation": "승인"
            }
        },
        {
            "step_name": "최종 결정",
            "duration_range": (3000, 8000),
            "details": {
                "final_decision": "승인",
                "confidence_score": random.randint(80, 95)
            }
        }
    ]
    
    # 단계별 시간 계산 및 로그 생성
    current_time = base_time
    log_steps = []
    
    for step_config in steps:
        duration = random.randint(*step_config["duration_range"])
        start_time = current_time
        end_time = current_time + timedelta(milliseconds=duration)
        
        log_steps.append(AgentLogStep(
            step_name=step_config["step_name"],
            start_time=start_time.isoformat(),
            end_time=end_time.isoformat(),
            duration_ms=duration,
            status="completed",
            details=step_config["details"]
        ))
        
        current_time = end_time + timedelta(milliseconds=random.randint(100, 500))
    
    total_duration = int((current_time - base_time).total_seconds() * 1000)
    
    return AgentLog(
        id=f"LOG-{uuid.uuid4().hex[:8].upper()}",
        review_id=review_id,
        session_id=f"LOG-{uuid.uuid4().hex[:8].upper()}",
        start_time=base_time.isoformat(),
        end_time=current_time.isoformat(),
        total_duration_ms=total_duration,
        status="completed",
        steps=log_steps,
        is_sample=True
    )
```

## 오류 처리

### 로그 기록 실패 시나리오

1. **저장소 오류**: 로그 저장 실패
2. **네트워크 오류**: 로그 전송 실패
3. **메모리 부족**: 대용량 로그 처리 실패

### 오류 처리 전략

```python
class RobustLogCollector(LogCollector):
    def __init__(self, review_id: str):
        super().__init__(review_id)
        self.fallback_logs = []  # 메모리 백업
        
    def save_step_safely(self, step: AgentLogStep):
        """안전한 단계 저장"""
        try:
            # 메인 저장소에 저장 시도
            save_log_step(step)
        except Exception as e:
            # 실패 시 메모리에 백업
            self.fallback_logs.append(step)
            logger.warning(f"로그 저장 실패, 메모리에 백업: {e}")
    
    def complete_session_safely(self):
        """안전한 세션 완료"""
        try:
            # 백업된 로그들을 다시 저장 시도
            for log in self.fallback_logs:
                save_log_step(log)
            
            # 전체 세션 저장
            return super().complete_session()
        except Exception as e:
            logger.error(f"로그 세션 완료 실패: {e}")
            # 최소한의 정보라도 저장
            return self.create_minimal_log()
```

## 테스트 전략

### 1. 단위 테스트

**로그 수집기 테스트:**
```python
def test_log_collector():
    collector = LogCollector("REV-001")
    
    # 단계 시작/종료 테스트
    collector.start_step("테스트 단계")
    time.sleep(0.1)
    collector.end_step("completed")
    
    # 세션 완료 테스트
    log = collector.complete_session()
    
    assert len(log.steps) == 1
    assert log.steps[0].duration_ms > 0
    assert log.status == "completed"
```

**프론트엔드 컴포넌트 테스트:**
```tsx
describe('AgentLogButton', () => {
  it('로그가 있을 때 버튼을 표시한다', () => {
    render(<AgentLogButton reviewId="REV-001" hasLog={true} />);
    expect(screen.getByText('Agent 로그확인하기')).toBeInTheDocument();
  });

  it('로그가 없을 때 버튼을 숨긴다', () => {
    render(<AgentLogButton reviewId="REV-001" hasLog={false} />);
    expect(screen.queryByText('Agent 로그확인하기')).not.toBeInTheDocument();
  });
});
```

### 2. 통합 테스트

- 자동 응답 생성 → 로그 기록 → 로그 조회 전체 플로우 테스트
- 샘플 데이터와 실제 데이터 로그 호환성 테스트
- 로그 저장 실패 시 폴백 동작 테스트

### 3. 성능 테스트

- 대량 로그 데이터 조회 성능
- 실시간 로그 기록이 응답 생성 성능에 미치는 영향
- 모달 렌더링 성능 (대용량 로그)

## 보안 고려사항

1. **로그 데이터 보호**: 민감한 정보 마스킹
2. **접근 권한**: 로그 조회 권한 제어
3. **데이터 무결성**: 로그 조작 방지

## 성능 최적화

1. **지연 로딩**: 로그 상세 정보 필요 시에만 로드
2. **캐싱**: 자주 조회되는 로그 캐싱
3. **압축**: 대용량 로그 데이터 압축 저장
4. **배치 처리**: 로그 저장 배치 처리로 성능 향상

## 구현 우선순위

### Phase 1: 기본 구조
1. 로그 데이터 모델 정의
2. 기본 로그 수집기 구현
3. 샘플 로그 데이터 생성

### Phase 2: UI 구현
1. Agent 로그 버튼 추가
2. 로그 뷰어 모달 구현
3. API 엔드포인트 추가

### Phase 3: 실시간 로깅
1. 자동 응답 생성 과정에 로그 수집기 통합
2. 실시간 로그 기록 구현
3. 오류 처리 및 폴백 메커니즘

### Phase 4: 고급 기능
1. 로그 검색 및 필터링
2. 성능 모니터링
3. 로그 분석 대시보드