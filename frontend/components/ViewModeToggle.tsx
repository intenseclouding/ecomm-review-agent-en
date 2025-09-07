import React from 'react';

export type ViewMode = 'category' | 'all';

interface ViewModeToggleProps {
  currentMode: ViewMode;
  onModeChange: (mode: ViewMode) => void;
}

export default function ViewModeToggle({ currentMode, onModeChange }: ViewModeToggleProps) {
  return (
    <div className="view-mode-toggle mb-4 px-3 py-2 border-b border-gray-200">
      <button
        onClick={() => onModeChange('all')}
        className={`view-mode-button w-full text-left px-3 py-2 text-sm font-medium rounded-md transition-colors hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-orange-500 ${
          currentMode === 'all'
            ? 'view-mode-button-active bg-orange-50 text-orange-700 border-l-2 border-orange-400'
            : 'view-mode-button-inactive text-gray-700 hover:text-gray-900'
        }`}
      >
        📋 전체 목록 보기
      </button>
      
      {currentMode === 'all' && (
        <button
          onClick={() => onModeChange('category')}
          className="view-mode-button w-full text-left px-3 py-2 text-sm font-medium rounded-md transition-colors hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-orange-500 view-mode-button-inactive text-gray-700 hover:text-gray-900 mt-1"
        >
          📁 카테고리별 보기
        </button>
      )}
    </div>
  );
}