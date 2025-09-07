import React from 'react';

interface KeywordTagsProps {
  keywords: string[];
  onKeywordClick?: (keyword: string) => void;
  className?: string;
}

const KeywordTags: React.FC<KeywordTagsProps> = ({ 
  keywords, 
  onKeywordClick, 
  className = "" 
}) => {
  if (!keywords || keywords.length === 0) {
    return null;
  }

  return (
    <div className={`flex flex-wrap gap-2 mt-2 ${className}`}>
      {keywords.map((keyword, index) => (
        <span
          key={index}
          onClick={() => onKeywordClick?.(keyword)}
          className={`
            inline-flex items-center px-2 py-1 rounded-full text-xs font-medium
            bg-blue-100 text-blue-800 border border-blue-200
            transition-all duration-200 ease-in-out
            ${onKeywordClick ? 'cursor-pointer hover:bg-blue-200 hover:border-blue-300 hover:shadow-sm' : ''}
          `}
          title={onKeywordClick ? `"${keyword}" 키워드로 필터링` : keyword}
        >
          <span className="mr-1">#</span>
          {keyword}
        </span>
      ))}
    </div>
  );
};

export default KeywordTags;