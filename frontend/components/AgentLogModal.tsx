import React, { useState, useEffect } from 'react';
import axios from 'axios';

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
  session_id: string;
  start_time: string;
  end_time?: string;
  total_duration_ms?: number;
  status: string;
  steps: AgentLogStep[];
  metadata: Record<string, any>;
  is_sample: boolean;
}

interface AgentLogModalProps {
  reviewId: string;
  onClose: () => void;
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
      setLoading(true);
      setError(null);
      
      const response = await axios.get(`http://localhost:8000/api/reviews/${reviewId}/agent-log`);
      setLog(response.data);
    } catch (err: any) {
      console.error('로그 조회 실패:', err);
      
      if (err.response?.status === 404) {
        setError('이 리뷰에 대한 에이전트 로그를 찾을 수 없습니다.');
      } else {
        setError('로그를 불러오는데 실패했습니다. 다시 시도해주세요.');
      }
    } finally {
      setLoading(false);
    }
  };

  const formatDuration = (ms: number) => {
    if (ms < 1000) return `${ms}ms`;
    if (ms < 60000) return `${(ms / 1000).toFixed(1)}s`;
    return `${Math.floor(ms / 60000)}m ${Math.floor((ms % 60000) / 1000)}s`;
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <span className="text-green-500 text-lg">✓</span>;
      case 'failed':
        return <span className="text-red-500 text-lg">✗</span>;
      case 'in_progress':
        return <span className="text-blue-500 text-lg animate-spin">⟳</span>;
      default:
        return <span className="text-gray-500 text-lg">○</span>;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'text-green-600 bg-green-50 border-green-200';
      case 'failed':
        return 'text-red-600 bg-red-50 border-red-200';
      case 'in_progress':
        return 'text-blue-600 bg-blue-50 border-blue-200';
      default:
        return 'text-gray-600 bg-gray-50 border-gray-200';
    }
  };

  const formatTimestamp = (timestamp: string) => {
    const date = new Date(timestamp);
    return date.toLocaleString('ko-KR', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  };

  const renderDetailValue = (value: any): string => {
    if (typeof value === 'object' && value !== null) {
      return JSON.stringify(value, null, 2);
    }
    return String(value);
  };

  // 모달 배경 클릭 시 닫기
  const handleBackdropClick = (e: React.MouseEvent) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  return (
    <div 
      className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
      onClick={handleBackdropClick}
    >
      <div className="bg-white rounded-lg max-w-6xl w-full max-h-[90vh] overflow-hidden shadow-2xl">
        {/* 헤더 */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200 bg-gray-50">
          <div>
            <h2 className="text-xl font-bold text-gray-900">Agent 처리 로그</h2>
            <p className="text-sm text-gray-600 mt-1">리뷰 ID: {reviewId}</p>
          </div>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700 text-2xl font-bold w-8 h-8 flex items-center justify-center rounded-full hover:bg-gray-200 transition-colors"
            title="닫기"
          >
            ×
          </button>
        </div>

        {/* 내용 */}
        <div className="p-6 overflow-y-auto max-h-[calc(90vh-120px)]">
          {loading && (
            <div className="text-center py-12">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
              <p className="mt-4 text-gray-600">로그를 불러오는 중...</p>
            </div>
          )}

          {error && (
            <div className="text-center py-12">
              <div className="text-red-500 text-6xl mb-4">⚠️</div>
              <p className="text-red-600 text-lg font-medium">{error}</p>
              <button
                onClick={fetchAgentLog}
                className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
              >
                다시 시도
              </button>
            </div>
          )}

          {log && (
            <div className="space-y-6">
              {/* 로그 요약 */}
              <div className="bg-gray-50 rounded-lg p-6 border">
                <h3 className="text-lg font-semibold mb-4 text-gray-900">처리 요약</h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                  <div>
                    <span className="text-gray-600 block">세션 ID</span>
                    <p className="font-mono text-gray-900 break-all">{log.id}</p>
                  </div>
                  <div>
                    <span className="text-gray-600 block">전체 소요시간</span>
                    <p className="font-semibold text-gray-900">
                      {log.total_duration_ms ? formatDuration(log.total_duration_ms) : '진행중'}
                    </p>
                  </div>
                  <div>
                    <span className="text-gray-600 block">상태</span>
                    <div className="flex items-center space-x-2">
                      {getStatusIcon(log.status)}
                      <span className={`px-2 py-1 rounded-full text-xs font-medium border ${getStatusColor(log.status)}`}>
                        {log.status}
                      </span>
                    </div>
                  </div>
                  <div>
                    <span className="text-gray-600 block">데이터 타입</span>
                    <p className={`font-medium ${log.is_sample ? 'text-orange-600' : 'text-green-600'}`}>
                      {log.is_sample ? '샘플 데이터' : '실제 데이터'}
                    </p>
                  </div>
                </div>
                
                {/* 메타데이터 */}
                {Object.keys(log.metadata).length > 0 && (
                  <div className="mt-4 pt-4 border-t border-gray-200">
                    <h4 className="font-medium text-gray-900 mb-2">메타데이터</h4>
                    <div className="grid grid-cols-2 md:grid-cols-3 gap-2 text-xs">
                      {Object.entries(log.metadata).map(([key, value]) => (
                        <div key={key}>
                          <span className="text-gray-600">{key}:</span>
                          <span className="ml-1 text-gray-900">{String(value)}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              {/* 단계별 로그 */}
              <div className="space-y-4">
                <h3 className="text-lg font-semibold text-gray-900">처리 단계</h3>
                
                {log.steps.length === 0 ? (
                  <div className="text-center py-8 text-gray-500">
                    처리 단계 정보가 없습니다.
                  </div>
                ) : (
                  <div className="space-y-4">
                    {log.steps.map((step, index) => (
                      <div key={index} className="border rounded-lg overflow-hidden">
                        {/* 단계 헤더 */}
                        <div className={`p-4 border-b ${getStatusColor(step.status)}`}>
                          <div className="flex items-center justify-between">
                            <div className="flex items-center space-x-3">
                              {getStatusIcon(step.status)}
                              <div>
                                <h4 className="font-semibold text-gray-900">{step.step_name}</h4>
                                <p className="text-sm text-gray-600">
                                  단계 {index + 1} / {log.steps.length}
                                </p>
                              </div>
                            </div>
                            <div className="text-right text-sm">
                              <div className="font-medium text-gray-900">
                                {step.duration_ms ? formatDuration(step.duration_ms) : '진행중'}
                              </div>
                              <div className="text-gray-600">
                                {formatTimestamp(step.start_time)}
                              </div>
                            </div>
                          </div>
                        </div>

                        {/* 단계 내용 */}
                        <div className="p-4 bg-white">
                          {/* 시간 정보 */}
                          <div className="mb-4 text-sm text-gray-600">
                            <div>시작: {formatTimestamp(step.start_time)}</div>
                            {step.end_time && (
                              <div>완료: {formatTimestamp(step.end_time)}</div>
                            )}
                          </div>

                          {/* 오류 메시지 */}
                          {step.error_message && (
                            <div className="mb-4 bg-red-50 border border-red-200 rounded p-3">
                              <h5 className="font-medium text-red-800 mb-1">오류 발생</h5>
                              <p className="text-red-700 text-sm">{step.error_message}</p>
                            </div>
                          )}

                          {/* 상세 정보 */}
                          {Object.keys(step.details).length > 0 && (
                            <div className="bg-blue-50 rounded p-4">
                              <h5 className="font-medium text-blue-800 mb-3">상세 정보</h5>
                              <div className="space-y-2">
                                {Object.entries(step.details).map(([key, value]) => (
                                  <div key={key} className="text-sm">
                                    <span className="font-medium text-blue-900">{key}:</span>
                                    <div className="mt-1 ml-4">
                                      <pre className="text-blue-700 whitespace-pre-wrap break-words text-xs bg-white p-2 rounded border">
                                        {renderDetailValue(value)}
                                      </pre>
                                    </div>
                                  </div>
                                ))}
                              </div>
                            </div>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default AgentLogModal;