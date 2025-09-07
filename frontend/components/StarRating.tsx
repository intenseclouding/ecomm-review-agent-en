import React from 'react';

interface StarRatingProps {
  rating: number;
  size?: 'small' | 'medium' | 'large';
  showCount?: boolean;
  reviewCount?: number;
  className?: string;
}

const StarRating: React.FC<StarRatingProps> = ({
  rating,
  size = 'medium',
  showCount = false,
  reviewCount = 0,
  className = ''
}) => {
  // 0.5 단위로 반올림하여 정확한 반별 표시
  const roundedRating = Math.round(rating * 2) / 2;
  
  // 크기별 스타일 정의
  const sizeClasses = {
    small: 'text-sm',
    medium: 'text-lg',
    large: 'text-2xl'
  };
  
  const textSizeClasses = {
    small: 'text-xs',
    medium: 'text-sm',
    large: 'text-base'
  };
  
  // 별 렌더링 함수
  const renderStars = () => {
    const stars = [];
    const fullStars = Math.floor(roundedRating);
    const hasHalfStar = roundedRating % 1 !== 0;
    const emptyStars = 5 - Math.ceil(roundedRating);
    
    // 꽉 찬 별들
    for (let i = 0; i < fullStars; i++) {
      stars.push(
        <span
          key={`full-${i}`}
          className="text-yellow-400"
          aria-hidden="true"
        >
          ★
        </span>
      );
    }
    
    // 반별 (있는 경우)
    if (hasHalfStar) {
      stars.push(
        <span
          key="half"
          className="relative inline-block text-gray-300"
          aria-hidden="true"
        >
          <span className="absolute inset-0 overflow-hidden w-1/2 text-yellow-400">
            ★
          </span>
          ★
        </span>
      );
    }
    
    // 빈 별들
    for (let i = 0; i < emptyStars; i++) {
      stars.push(
        <span
          key={`empty-${i}`}
          className="text-gray-300"
          aria-hidden="true"
        >
          ★
        </span>
      );
    }
    
    return stars;
  };
  
  return (
    <div className={`flex items-center ${className}`}>
      {/* 별점 표시 */}
      <div 
        className={`flex ${sizeClasses[size]}`}
        role="img"
        aria-label={`${rating}점 만점에 ${roundedRating}점`}
      >
        {renderStars()}
      </div>
      
      {/* 숫자 평점 및 리뷰 개수 */}
      <div className={`ml-2 ${textSizeClasses[size]} text-gray-600 flex items-center gap-1`}>
        <span className="font-medium">
          {roundedRating.toFixed(1)}
        </span>
        {showCount && reviewCount > 0 && (
          <span className="text-gray-500">
            ({reviewCount}개 리뷰)
          </span>
        )}
      </div>
    </div>
  );
};

export default StarRating;