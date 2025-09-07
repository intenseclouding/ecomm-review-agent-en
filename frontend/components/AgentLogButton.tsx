import React, { useState } from 'react';
import AgentLogModal from './AgentLogModal';

interface AgentLogButtonProps {
  reviewId: string;
  hasLog: boolean;
  className?: string;
}

const AgentLogButton: React.FC<AgentLogButtonProps> = ({ 
  reviewId, 
  hasLog, 
  className = "" 
}) => {
  const [showModal, setShowModal] = useState(false);

  // 로그가 없으면 버튼을 표시하지 않음
  if (!hasLog) {
    return null;
  }

  return (
    <>
      <button
        onClick={() => setShowModal(true)}
        className={`flex items-center space-x-1 text-blue-600 hover:text-blue-800 text-sm transition-colors duration-200 ${className}`}
        title="에이전트 처리 로그 확인"
      >
        <svg 
          className="w-4 h-4" 
          fill="currentColor" 
          viewBox="0 0 20 20"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path 
            fillRule="evenodd" 
            d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" 
            clipRule="evenodd" 
          />
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

export default AgentLogButton;