import React, { useState } from 'react';
import axios from 'axios';
import AgentLogButton from './AgentLogButton';
import KeywordTags from './KeywordTags';
import SentimentIndicator from './SentimentIndicator';
import HighlightedText from './HighlightedText';
import MediaGallery from './MediaGallery';
import { Review } from '../types/product';

interface ReviewListProps {
  reviews: Review[];
  productFeatures?: string[];
  onWriteReview?: () => void;
}

const ReviewList: React.FC<ReviewListProps> = ({ reviews, productFeatures = [], onWriteReview }) => {
  const [processingReviews, setProcessingReviews] = useState<Set<string>>(new Set());

  const handleApproveResponse = async (reviewId: string) => {
    setProcessingReviews(prev => new Set(prev).add(reviewId));

    try {
      await axios.post(`http://localhost:8000/api/reviews/${reviewId}/approve-response`);
      // 성공 시 페이지 새로고침 또는 상태 업데이트
      window.location.reload();
    } catch (error) {
      console.error('댓글 승인 실패:', error);
      alert('댓글 승인에 실패했습니다.');
    } finally {
      setProcessingReviews(prev => {
        const newSet = new Set(prev);
        newSet.delete(reviewId);
        return newSet;
      });
    }
  };

  const handleRejectResponse = async (reviewId: string) => {
    setProcessingReviews(prev => new Set(prev).add(reviewId));

    try {
      await axios.delete(`http://localhost:8000/api/reviews/${reviewId}/response`);
      // 성공 시 페이지 새로고침 또는 상태 업데이트
      window.location.reload();
    } catch (error) {
      console.error('댓글 거부 실패:', error);
      alert('댓글 거부에 실패했습니다.');
    } finally {
      setProcessingReviews(prev => {
        const newSet = new Set(prev);
        newSet.delete(reviewId);
        return newSet;
      });
    }
  };

  const renderStars = (rating: number) => {
    return [...Array(5)].map((_, i) => (
      <span key={i} className={i < rating ? 'text-yellow-400' : 'text-gray-300'}>
        ★
      </span>
    ));
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('ko-KR', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  if (reviews.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-lg p-8 text-center">
        <p className="text-gray-500">아직 작성된 리뷰가 없습니다.</p>
        <p className="text-sm text-gray-400 mt-2">첫 번째 리뷰를 작성해보세요!</p>
        {onWriteReview && (
          <button
            onClick={onWriteReview}
            className="mt-4 px-6 py-3 bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-lg hover:from-blue-600 hover:to-blue-700 transition-all duration-300 font-semibold shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
          >
            ✍️ 리뷰 작성
          </button>
        )}
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold">
          고객 리뷰 ({reviews.length})
        </h2>
        {onWriteReview && (
          <button
            onClick={onWriteReview}
            className="px-6 py-3 bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-lg hover:from-blue-600 hover:to-blue-700 transition-all duration-300 font-semibold shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
          >
            ✍️ 리뷰 작성
          </button>
        )}
      </div>

      <div className="space-y-6">
        {reviews.map((review) => (
          <div key={review.id} className="border-b border-gray-200 pb-6 last:border-b-0">
            {/* 리뷰 헤더 */}
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center space-x-3">
                <span className="font-semibold">{review.user_name || '익명 사용자'}</span>
                {review.verified_purchase && (
                  <span className="bg-green-100 text-green-800 text-xs px-2 py-1 rounded-full">
                    구매확인
                  </span>
                )}
              </div>
              <span className="text-sm text-gray-500">
                {formatDate(review.date)}
              </span>
            </div>

            {/* 평점 */}
            <div className="flex items-center mb-3">
              <div className="flex">
                {renderStars(review.rating)}
              </div>
              <span className="ml-2 text-sm text-gray-600">
                ({review.rating}/5)
              </span>
            </div>

            {/* 리뷰 내용 (키워드 하이라이팅 적용) */}
            <div className="text-gray-800 mb-4 leading-relaxed">
              <HighlightedText
                text={review.content}
                keywords={review.keywords || []}
                productFeatures={productFeatures}
              />
            </div>

            {/* 미디어 파일 표시 */}
            {review.media_files && review.media_files.length > 0 && (
              <MediaGallery mediaFiles={review.media_files} />
            )}

            {/* 키워드 및 감정 분석 결과 */}
            {(review.keywords || review.sentiment) && (
              <div className="mb-4 p-3 bg-gray-50 rounded-lg border">
                <div className="flex flex-wrap items-center gap-3">
                  {/* 감정 분석 결과 */}
                  {review.sentiment && (
                    <div className="flex items-center">
                      <span className="text-xs text-gray-600 mr-2">감정:</span>
                      <SentimentIndicator
                        sentiment={review.sentiment}
                        showConfidence={true}
                        size="sm"
                      />
                    </div>
                  )}

                  {/* 키워드 태그 */}
                  {review.keywords && review.keywords.length > 0 && (
                    <div className="flex items-start flex-1">
                      <span className="text-xs text-gray-600 mr-2 mt-1">키워드:</span>
                      <KeywordTags
                        keywords={review.keywords}
                        onKeywordClick={(keyword) => {
                          console.log(`키워드 클릭: ${keyword}`);
                          // 향후 키워드 필터링 기능 구현 예정
                        }}
                      />
                    </div>
                  )}
                </div>

                {/* 분석 상태 표시 */}
                {review.analysis_completed === false && (
                  <div className="mt-2 text-xs text-gray-500 flex items-center">
                    <div className="animate-spin rounded-full h-3 w-3 border-b-2 border-blue-500 mr-2"></div>
                    AI 분석 중...
                  </div>
                )}

                {review.analysis_completed && review.analysis_timestamp && (
                  <div className="mt-2 text-xs text-gray-400">
                    분석 완료: {new Date(review.analysis_timestamp).toLocaleString('ko-KR')}
                  </div>
                )}
              </div>
            )}

            {/* AI 자동 응답 섹션 */}
            {review.auto_response && (
              <div className="bg-blue-50 rounded-lg p-4 mt-4">
                <div className="flex items-center justify-between mb-2">
                  <h4 className="font-semibold text-blue-800 flex items-center">
                    🤖 AI 자동 생성 댓글
                    {review.response_approved && (
                      <span className="ml-2 bg-green-100 text-green-800 text-xs px-2 py-1 rounded-full">
                        승인됨
                      </span>
                    )}
                  </h4>

                  {!review.response_approved && (
                    <div className="flex space-x-2">
                      <button
                        onClick={() => handleApproveResponse(review.id)}
                        disabled={processingReviews.has(review.id)}
                        className="bg-green-500 text-white px-3 py-1 rounded text-sm hover:bg-green-600 disabled:bg-gray-400 disabled:cursor-not-allowed"
                      >
                        {processingReviews.has(review.id) ? '처리중...' : '승인'}
                      </button>
                      <button
                        onClick={() => handleRejectResponse(review.id)}
                        disabled={processingReviews.has(review.id)}
                        className="bg-red-500 text-white px-3 py-1 rounded text-sm hover:bg-red-600 disabled:bg-gray-400 disabled:cursor-not-allowed"
                      >
                        {processingReviews.has(review.id) ? '처리중...' : '거부'}
                      </button>
                    </div>
                  )}
                </div>

                <p className="text-blue-700 text-sm mb-3">
                  {review.auto_response}
                </p>

                {/* Agent 로그 버튼 */}
                <div className="flex items-center justify-between">
                  <div>
                    {!review.response_approved && (
                      <p className="text-xs text-blue-600">
                        💡 Strands Agent가 리뷰를 분석하여 자동으로 생성한 댓글입니다. 승인하시면 고객에게 표시됩니다.
                      </p>
                    )}
                  </div>
                  <AgentLogButton
                    reviewId={review.id}
                    hasLog={!!review.agent_log_id}
                    className="ml-auto"
                  />
                </div>
              </div>
            )}

            {/* 승인된 댓글 표시 */}
            {review.response_approved && review.auto_response && (
              <div className="bg-gray-50 rounded-lg p-4 mt-4">
                <div className="flex items-center justify-between mb-2">
                  <h4 className="font-semibold text-gray-800 flex items-center">
                    💬 셀러 댓글
                    <span className="ml-2 bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full">
                      AI 생성
                    </span>
                  </h4>
                  <AgentLogButton
                    reviewId={review.id}
                    hasLog={!!review.agent_log_id}
                  />
                </div>
                <p className="text-gray-700 text-sm">
                  {review.auto_response}
                </p>
              </div>
            )}

            {/* 샘플 데이터의 seller_response 표시 */}
            {review.seller_response && (
              <div className="bg-gray-50 rounded-lg p-4 mt-4">
                <div className="flex items-center justify-between mb-2">
                  <h4 className="font-semibold text-gray-800 flex items-center">
                    💬 셀러 댓글
                  </h4>
                </div>
                <p className="text-gray-700 text-sm mb-2">
                  {review.seller_response.content}
                </p>
                <p className="text-xs text-gray-500">
                  작성일: {review.seller_response.date}
                </p>
              </div>
            )}
          </div>
        ))}
      </div>


    </div>
  );
};

export default ReviewList;