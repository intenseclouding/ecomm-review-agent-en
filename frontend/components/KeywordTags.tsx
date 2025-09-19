import React from 'react';

interface KeywordTagsProps {
  keywords: string[];
  selectedKeyword?: string | null;
  onKeywordClick?: (keyword: string) => void;
  className?: string;
}

const KeywordTags: React.FC<KeywordTagsProps> = ({ 
  keywords, 
  selectedKeyword,
  onKeywordClick, 
  className = "" 
}) => {
  if (!keywords || keywords.length === 0) {
    return null;
  }

  return (
    <div className={`flex flex-wrap gap-2 mt-2 ${className}`}>
      {keywords.map((keyword, index) => {
        const isSelected = selectedKeyword === keyword;
        return (
          <span
            key={index}
            onClick={() => onKeywordClick?.(keyword)}
            className={`
              inline-flex items-center px-2 py-1 rounded-full text-xs font-medium
              border transition-all duration-200 ease-in-out
              ${isSelected 
                ? 'bg-blue-500 text-white border-blue-600 shadow-md' 
                : 'bg-blue-100 text-blue-800 border-blue-200'
              }
              ${onKeywordClick ? 'cursor-pointer hover:shadow-sm' : ''}
              ${onKeywordClick && !isSelected ? 'hover:bg-blue-200 hover:border-blue-300' : ''}
            `}
            title={onKeywordClick ? `"${keyword}" 키워드로 필터링` : keyword}
          >
            <span className="mr-1">#</span>
            {keyword}
          </span>
        );
      })}
    </div>
  );
};

export default KeywordTags;