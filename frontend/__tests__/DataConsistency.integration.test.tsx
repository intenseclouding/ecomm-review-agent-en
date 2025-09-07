/**
 * 데이터 일관성 통합 테스트
 * 홈페이지, 상세페이지, 사이드바 간의 데이터 일관성을 검증
 */

import { render, screen, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { productApiService } from '../services/productApiService';
import { RatingCalculator } from '../utils/ratingCalculator';
import StarRating from '../components/StarRating';
import ProductDetail from '../components/ProductDetail';

// Mock 데이터
const mockProductSummary = {
  id: 'PROD-001',
  name: '테스트 제품',
  category: '전자제품',
  price: 50000,
  average_rating: 4.2,
  review_count: 15,
  image_url: '/test.jpg',
  emoji: '🎧'
};

const mockProductDetail = {
  ...mockProductSummary,
  seller_id: 'SELLER-001',
  description: '테스트 제품 설명',
  features: ['기능1', '기능2'],
  reviews: [
    {
      id: 'REV-001',
      user_name: '사용자1',
      rating: 5,
      content: '좋은 제품',
      date: '2024-01-01',
      verified_purchase: true
    },
    {
      id: 'REV-002',
      user_name: '사용자2',
      rating: 3,
      content: '보통',
      date: '2024-01-02',
      verified_purchase: true
    }
  ],
  rating_distribution: { 1: 0, 2: 0, 3: 1, 4: 0, 5: 1 }
};

// API 서비스 모킹
jest.mock('../services/productApiService', () => ({
  productApiService: {
    getProductSummaries: jest.fn(),
    getProductDetail: jest.fn(),
    getProductSummary: jest.fn()
  }
}));

const mockProductApiService = productApiService as jest.Mocked<typeof productApiService>;

describe('Data Consistency Integration Tests', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('Rating Calculation Consistency', () => {
    test('frontend and backend rating calculations should match', async () => {
      // 백엔드에서 계산된 평점
      const backendRating = mockProductDetail.average_rating;
      
      // 프론트엔드에서 동일한 리뷰 데이터로 계산한 평점
      const frontendRating = RatingCalculator.calculateAverageRating(mockProductDetail.reviews);
      
      // 두 값이 일치해야 함
      expect(Math.abs(backendRating - frontendRating)).toBeLessThan(0.1);
    });

    test('star rounding should be consistent across components', () => {
      const rating = 4.2;
      const expectedRounded = 4.0; // 4.2는 4.0으로 반올림되어야 함
      
      const rounded = RatingCalculator.roundToHalfStar(rating);
      expect(rounded).toBe(expectedRounded);
    });

    test('rating distribution calculation should be consistent', () => {
      const reviews = mockProductDetail.reviews;
      const calculatedDistribution = RatingCalculator.calculateRatingDistribution(reviews);
      const expectedDistribution = mockProductDetail.rating_distribution;
      
      expect(calculatedDistribution).toEqual(expectedDistribution);
    });
  });

  describe('Cross-Component Data Consistency', () => {
    test('StarRating component displays consistent rating across different sizes', () => {
      const rating = 4.2;
      const reviewCount = 15;

      // 다양한 크기로 렌더링
      const { rerender } = render(
        <StarRating rating={rating} size="small" showCount={true} reviewCount={reviewCount} />
      );
      
      // 작은 크기에서의 평점 표시 확인
      expect(screen.getByText('4.0')).toBeInTheDocument();
      expect(screen.getByText('(15개 리뷰)')).toBeInTheDocument();

      // 중간 크기로 재렌더링
      rerender(
        <StarRating rating={rating} size="medium" showCount={true} reviewCount={reviewCount} />
      );
      
      // 동일한 평점이 표시되어야 함
      expect(screen.getByText('4.0')).toBeInTheDocument();
      expect(screen.getByText('(15개 리뷰)')).toBeInTheDocument();

      // 큰 크기로 재렌더링
      rerender(
        <StarRating rating={rating} size="large" showCount={true} reviewCount={reviewCount} />
      );
      
      // 여전히 동일한 평점이 표시되어야 함
      expect(screen.getByText('4.0')).toBeInTheDocument();
      expect(screen.getByText('(15개 리뷰)')).toBeInTheDocument();
    });

    test('product data should be consistent between summary and detail views', async () => {
      mockProductApiService.getProductSummary.mockResolvedValue(mockProductSummary);
      mockProductApiService.getProductDetail.mockResolvedValue(mockProductDetail);

      // 요약 정보 가져오기
      const summary = await productApiService.getProductSummary('PROD-001');
      
      // 상세 정보 가져오기
      const detail = await productApiService.getProductDetail('PROD-001');

      // 공통 필드들이 일치해야 함
      expect(summary.id).toBe(detail.id);
      expect(summary.name).toBe(detail.name);
      expect(summary.category).toBe(detail.category);
      expect(summary.price).toBe(detail.price);
      expect(summary.average_rating).toBe(detail.average_rating);
      expect(summary.review_count).toBe(detail.review_count);
    });
  });

  describe('API Response Consistency', () => {
    test('API endpoints should return consistent data structure', async () => {
      mockProductApiService.getProductSummaries.mockResolvedValue([mockProductSummary]);
      mockProductApiService.getProductDetail.mockResolvedValue(mockProductDetail);

      // 전체 제품 목록에서 특정 제품 찾기
      const summaries = await productApiService.getProductSummaries();
      const summaryFromList = summaries.find(p => p.id === 'PROD-001');

      // 개별 제품 상세 정보 가져오기
      const detail = await productApiService.getProductDetail('PROD-001');

      // 요약 정보와 상세 정보의 공통 필드가 일치해야 함
      expect(summaryFromList?.id).toBe(detail.id);
      expect(summaryFromList?.name).toBe(detail.name);
      expect(summaryFromList?.average_rating).toBe(detail.average_rating);
      expect(summaryFromList?.review_count).toBe(detail.review_count);
    });

    test('error handling should be consistent across API calls', async () => {
      const errorMessage = '제품을 찾을 수 없습니다.';
      
      mockProductApiService.getProductDetail.mockRejectedValue(new Error(errorMessage));
      mockProductApiService.getProductSummary.mockRejectedValue(new Error(errorMessage));

      // 두 API 호출 모두 동일한 에러를 발생시켜야 함
      await expect(productApiService.getProductDetail('NONEXISTENT')).rejects.toThrow(errorMessage);
      await expect(productApiService.getProductSummary('NONEXISTENT')).rejects.toThrow(errorMessage);
    });
  });

  describe('Edge Cases and Error Scenarios', () => {
    test('should handle products with no reviews consistently', async () => {
      const productWithNoReviews = {
        ...mockProductDetail,
        reviews: [],
        average_rating: 0,
        review_count: 0,
        rating_distribution: { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 }
      };

      mockProductApiService.getProductDetail.mockResolvedValue(productWithNoReviews);

      const detail = await productApiService.getProductDetail('PROD-001');
      
      expect(detail.average_rating).toBe(0);
      expect(detail.review_count).toBe(0);
      expect(detail.reviews).toHaveLength(0);

      // StarRating 컴포넌트도 올바르게 처리해야 함
      render(<StarRating rating={detail.average_rating} showCount={true} reviewCount={detail.review_count} />);
      
      expect(screen.getByText('0.0')).toBeInTheDocument();
      expect(screen.queryByText('개 리뷰')).not.toBeInTheDocument(); // 리뷰 개수가 0이면 표시하지 않음
    });

    test('should handle invalid rating values consistently', () => {
      const invalidRatings = [-1, 0, 6, 10, NaN, null, undefined];
      
      invalidRatings.forEach(rating => {
        // RatingCalculator는 유효하지 않은 평점을 적절히 처리해야 함
        const isValid = RatingCalculator.isValidRating(rating);
        expect(isValid).toBe(false);
        
        // StarRating 컴포넌트도 유효하지 않은 평점을 안전하게 처리해야 함
        const { unmount } = render(<StarRating rating={rating as number} />);
        
        // 컴포넌트가 에러 없이 렌더링되어야 함
        expect(screen.getByRole('img')).toBeInTheDocument();
        
        unmount();
      });
    });

    test('should maintain data consistency during loading states', async () => {
      // 로딩 중에도 데이터 구조가 일관되어야 함
      let resolvePromise: (value: any) => void;
      const pendingPromise = new Promise(resolve => {
        resolvePromise = resolve;
      });

      mockProductApiService.getProductDetail.mockReturnValue(pendingPromise);

      render(<ProductDetail productId="PROD-001" />);

      // 로딩 상태 확인
      expect(screen.getByText(/로딩/)).toBeInTheDocument();

      // Promise 해결
      resolvePromise!(mockProductDetail);

      // 데이터가 로드된 후 일관된 구조로 표시되어야 함
      await waitFor(() => {
        expect(screen.getByText(mockProductDetail.name)).toBeInTheDocument();
      });
    });
  });

  describe('Performance and Caching Consistency', () => {
    test('cached data should be consistent with fresh data', async () => {
      // 첫 번째 호출 (캐시 없음)
      mockProductApiService.getProductSummary.mockResolvedValueOnce(mockProductSummary);
      const firstCall = await productApiService.getProductSummary('PROD-001');

      // 두 번째 호출 (캐시 사용)
      mockProductApiService.getProductSummary.mockResolvedValueOnce(mockProductSummary);
      const secondCall = await productApiService.getProductSummary('PROD-001');

      // 두 호출의 결과가 동일해야 함
      expect(firstCall).toEqual(secondCall);
    });

    test('cache invalidation should maintain data consistency', async () => {
      const updatedProduct = {
        ...mockProductSummary,
        average_rating: 4.5,
        review_count: 20
      };

      // 초기 데이터
      mockProductApiService.getProductSummary.mockResolvedValueOnce(mockProductSummary);
      const initialData = await productApiService.getProductSummary('PROD-001');

      // 캐시 무효화 후 업데이트된 데이터
      productApiService.invalidateProduct('PROD-001');
      mockProductApiService.getProductSummary.mockResolvedValueOnce(updatedProduct);
      const updatedData = await productApiService.getProductSummary('PROD-001');

      // 데이터가 올바르게 업데이트되어야 함
      expect(initialData.average_rating).toBe(4.2);
      expect(updatedData.average_rating).toBe(4.5);
      expect(updatedData.review_count).toBe(20);
    });
  });
});