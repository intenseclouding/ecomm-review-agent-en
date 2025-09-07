import React from 'react';

interface SentimentData {
  label: string;
  confidence: number;
  polarity?: number;
}

interface SentimentIndicatorProps {
  sentiment: SentimentData;
  showConfidence?: boolean;
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

const SentimentIndicator: React.FC<SentimentIndicatorProps> = ({ 
  sentiment, 
  showConfidence = true,
  size = 'md',
  className = "" 
}) => {
  if (!sentiment || !sentiment.label) {
    return null;
  }

  const getColorClass = (label: string) => {
    switch (label.toLowerCase()) {
      case '긍정':
        return 'bg-green-100 text-green-800 border-green-200';
      case '부정':
        return 'bg-red-100 text-red-800 border-red-200';
      case '중립':
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getEmoji = (label: string) => {
    switch (label.toLowerCase()) {
      case '긍정':
        return '😊';
      case '부정':
        return '😞';
      case '중립':
      default:
        return '😐';
    }
  };

  const getSizeClass = (size: string) => {
    switch (size) {
      case 'sm':
        return 'text-xs px-2 py-1';
      case 'lg':
        return 'text-sm px-3 py-2';
      case 'md':
      default:
        return 'text-xs px-2 py-1';
    }
  };

  const confidencePercentage = Math.round((sentiment.confidence || 0) * 100);

  return (
    <div className={`
      inline-flex items-center rounded-full font-medium border
      transition-all duration-200 ease-in-out
      ${getColorClass(sentiment.label)}
      ${getSizeClass(size)}
      ${className}
    `}>
      <span className="mr-1">
        {getEmoji(sentiment.label)}
      </span>
      <span>
        {sentiment.label}
        {showConfidence && (
          <span className="ml-1 opacity-75">
            ({confidencePercentage}%)
          </span>
        )}
      </span>
    </div>
  );
};

export default SentimentIndicator;