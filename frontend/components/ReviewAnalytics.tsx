import React, { useMemo } from 'react';
import KeywordTags from './KeywordTags';
import SentimentIndicator from './SentimentIndicator';

interface Review {
  id: string;
  rating: number;
  keywords?: string[];
  sentiment?: {
    label: string;
    confidence: number;
    polarity: number;
  };
  analysis_completed?: boolean;
}

interface ReviewAnalyticsProps {
  reviews: Review[];
  className?: string;
}

interface KeywordFrequency {
  keyword: string;
  count: number;
  percentage: number;
}

interface SentimentStats {
  긍정: number;
  부정: number;
  중립: number;
  total: number;
}

const ReviewAnalytics: React.FC<ReviewAnalyticsProps> = ({ reviews, className = "" }) => {
  const analytics = useMemo(() => {
    const analyzedReviews = reviews.filter(r => r.analysis_completed);
    
    // 키워드 빈도 계산
    const keywordMap = new Map<string, number>();
    analyzedReviews.forEach(review => {
      if (review.keywords) {
        review.keywords.forEach(keyword => {
          keywordMap.set(keyword, (keywordMap.get(keyword) || 0) + 1);
        });
      }
    });

    const keywordFrequencies: KeywordFrequency[] = Array.from(keywordMap.entries())
      .map(([keyword, count]) => ({
        keyword,
        count,
        percentage: Math.round((count / analyzedReviews.length) * 100)
      }))
      .sort((a, b) => b.count - a.count)
      .slice(0, 10); // 상위 10개만

    // 감정 분포 계산
    const sentimentStats: SentimentStats = {
      긍정: 0,
      부정: 0,
      중립: 0,
      total: analyzedReviews.length
    };

    analyzedReviews.forEach(review => {
      if (review.sentiment) {
        const label = review.sentiment.label as keyof Omit<SentimentStats, 'total'>;
        if (label in sentimentStats) {
          sentimentStats[label]++;
        }
      }
    });

    // 평균 감정 점수 계산
    const avgSentimentScore = analyzedReviews.length > 0 
      ? analyzedReviews.reduce((sum, review) => {
          return sum + (review.sentiment?.polarity || 0);
        }, 0) / analyzedReviews.length
      : 0;

    return {
      keywordFrequencies,
      sentimentStats,
      avgSentimentScore,
      analyzedCount: analyzedReviews.length,
      totalCount: reviews.length
    };
  }, [reviews]);

  if (reviews.length === 0) {
    return (
      <div className={`bg-white rounded-lg shadow-lg p-6 ${className}`}>
        <h3 className="text-lg font-semibold mb-4">📊 리뷰 분석 통계</h3>
        <p className="text-gray-500 text-center py-8">분석할 리뷰가 없습니다.</p>
      </div>
    );
  }

  return (
    <div className={`bg-white rounded-lg shadow-lg p-6 ${className}`}>
      <h3 className="text-lg font-semibold mb-6 flex items-center">
        📊 리뷰 분석 통계
        <span className="ml-2 text-sm text-gray-500">
          (총 {analytics.totalCount}개)
        </span>
      </h3>

      <div className="grid grid-cols-3 gap-6">
        {/* 감정 분포 */}
        <div className="space-y-4">
          <h4 className="font-medium text-gray-800 flex items-center">
            😊 감정 분포
          </h4>
          
          {analytics.sentimentStats.total > 0 ? (
            <div className="flex flex-wrap gap-2">
              {Object.entries(analytics.sentimentStats).map(([label, count]) => {
                if (label === 'total') return null;
                
                const percentage = analytics.sentimentStats.total > 0 
                  ? Math.round((count / analytics.sentimentStats.total) * 100) 
                  : 0;
                
                return (
                  <div key={label} className="flex items-center gap-1">
                    <SentimentIndicator 
                      sentiment={{ label, confidence: 1, polarity: 0 }}
                      showConfidence={false}
                      size="sm"
                    />
                    <span className="text-sm font-medium">{count}</span>
                    <span className="text-xs text-gray-500">({percentage}%)</span>
                  </div>
                );
              })}
            </div>
          ) : (
            <p className="text-gray-500 text-sm">분석된 리뷰가 없습니다.</p>
          )}
        </div>

        {/* 키워드 빈도 */}
        <div className="space-y-4 col-span-2">
          <h4 className="font-medium text-gray-800 flex items-center">
            🏷️ 인기 키워드
          </h4>

          
          {analytics.keywordFrequencies.length > 0 ? (
            <div className="flex flex-wrap gap-2">
              {analytics.keywordFrequencies.map((item) => (
                <KeywordTags 
                  key={item.keyword}
                  keywords={[item.keyword]}
                  className="flex-shrink-0"
                />
              ))}
            </div>
          ) : (
            <p className="text-gray-500 text-sm">추출된 키워드가 없습니다.</p>
          )}
        </div>
      </div>

      {/* 분석 진행률 */}
      {analytics.analyzedCount < analytics.totalCount && (
        <div className="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-blue-800">
              AI 분석 진행률
            </span>
            <span className="text-sm text-blue-600">
              {analytics.analyzedCount}/{analytics.totalCount} 
              ({Math.round((analytics.analyzedCount / analytics.totalCount) * 100)}%)
            </span>
          </div>
          <div className="w-full bg-blue-200 rounded-full h-2">
            <div 
              className="h-2 rounded-full bg-blue-500 transition-all duration-300"
              style={{ 
                width: `${(analytics.analyzedCount / analytics.totalCount) * 100}%` 
              }}
            />
          </div>
          <p className="text-xs text-blue-600 mt-2">
            🤖 Strands Agent가 리뷰를 분석하고 있습니다...
          </p>
        </div>
      )}
    </div>
  );
};

export default ReviewAnalytics;