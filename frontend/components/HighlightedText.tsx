import React from 'react';

interface HighlightedTextProps {
  text: string;
  keywords: string[];
  productFeatures?: string[];
  className?: string;
}

const HighlightedText: React.FC<HighlightedTextProps> = ({ 
  text, 
  keywords = [], 
  productFeatures = [],
  className = "" 
}) => {
  if (!text || (keywords.length === 0 && productFeatures.length === 0)) {
    return <span className={className}>{text}</span>;
  }

  // 모든 하이라이트할 단어들을 수집
  const allHighlightWords = [...keywords, ...productFeatures];
  
  if (allHighlightWords.length === 0) {
    return <span className={className}>{text}</span>;
  }

  // 정규식 생성 (대소문자 구분 없이, 단어 경계 고려)
  const regex = new RegExp(
    `(${allHighlightWords.map(word => 
      word.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') // 특수문자 이스케이프
    ).join('|')})`,
    'gi'
  );

  const parts = text.split(regex);

  return (
    <span className={className}>
      {parts.map((part, index) => {
        if (!part) return null;
        
        const isKeyword = keywords.some(keyword => 
          keyword.toLowerCase() === part.toLowerCase()
        );
        const isProductFeature = productFeatures.some(feature => 
          feature.toLowerCase() === part.toLowerCase()
        );

        if (isKeyword || isProductFeature) {
          return (
            <span
              key={index}
              className={`
                px-1 py-0.5 rounded text-sm font-medium
                ${isProductFeature 
                  ? 'bg-orange-100 text-orange-800 border border-orange-200' 
                  : 'bg-yellow-100 text-yellow-800 border border-yellow-200'
                }
              `}
              title={
                isProductFeature 
                  ? `제품 기능: ${part}` 
                  : `키워드: ${part}`
              }
            >
              {part}
            </span>
          );
        }

        return <span key={index}>{part}</span>;
      })}
    </span>
  );
};

export default HighlightedText;