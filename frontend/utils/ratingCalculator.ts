/**
 * Rating Calculator - 평점 계산 및 처리 유틸리티
 */

import { Review, RatingStats, RatingDistribution, RatingQuality } from '../types/product';

export class RatingCalculator {
  /**
   * 리뷰 배열에서 평균 평점 계산
   */
  static calculateAverageRating(reviews: Review[]): number {
    if (!reviews || reviews.length === 0) {
      return 0;
    }

    const validRatings = reviews
      .map(review => review.rating)
      .filter(rating => rating !== null && rating !== undefined && rating >= 1 && rating <= 5);

    if (validRatings.length === 0) {
      return 0;
    }

    const sum = validRatings.reduce((acc, rating) => acc + rating, 0);
    const average = sum / validRatings.length;
    
    // 소수점 첫째 자리까지 반올림
    return Math.round(average * 10) / 10;
  }

  /**
   * 평점을 0.5 단위로 반올림 (별 표시용)
   */
  static roundToHalfStar(rating: number): number {
    return Math.round(rating * 2) / 2;
  }

  /**
   * 평점 분포 계산 (1-5점 각각의 개수)
   */
  static calculateRatingDistribution(reviews: Review[]): RatingDistribution {
    const distribution = { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 };

    if (!reviews || reviews.length === 0) {
      return distribution;
    }

    reviews.forEach(review => {
      const rating = review.rating;
      if (rating && rating >= 1 && rating <= 5) {
        distribution[rating]++;
      }
    });

    return distribution;
  }

  /**
   * 평점 분포를 퍼센트로 계산
   */
  static calculateRatingPercentages(reviews: Review[]): RatingDistribution {
    const distribution = this.calculateRatingDistribution(reviews);
    const totalReviews = reviews.length;

    if (totalReviews === 0) {
      return { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 };
    }

    const percentages: RatingDistribution = { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 };
    for (let rating = 1; rating <= 5; rating++) {
      percentages[rating as keyof RatingDistribution] = Math.round((distribution[rating as keyof RatingDistribution] / totalReviews) * 100);
    }

    return percentages;
  }

  /**
   * 종합 평점 통계 계산
   */
  static calculateRatingStats(reviews: Review[]): RatingStats {
    const averageRating = this.calculateAverageRating(reviews);
    const roundedRating = this.roundToHalfStar(averageRating);
    const ratingDistribution = this.calculateRatingDistribution(reviews);

    return {
      averageRating,
      totalReviews: reviews.length,
      ratingDistribution,
      roundedRating
    };
  }

  /**
   * 평점이 유효한지 검증
   */
  static isValidRating(rating: any): boolean {
    return typeof rating === 'number' && rating >= 1 && rating <= 5;
  }

  /**
   * 평점 텍스트 생성 (접근성용)
   */
  static getRatingText(rating: number, reviewCount: number = 0): string {
    const roundedRating = this.roundToHalfStar(rating);
    
    if (reviewCount > 0) {
      return `5점 만점에 ${roundedRating}점 (${reviewCount}개 리뷰)`;
    } else {
      return `5점 만점에 ${roundedRating}점`;
    }
  }

  /**
   * 평점 품질 레벨 계산 (우수/좋음/보통/나쁨)
   */
  static getRatingQuality(rating: number): RatingQuality {
    if (rating === 0) {
      return { level: 'none', text: '평점 없음', color: 'text-gray-400' };
    } else if (rating >= 4.5) {
      return { level: 'excellent', text: '우수', color: 'text-green-600' };
    } else if (rating >= 3.5) {
      return { level: 'good', text: '좋음', color: 'text-blue-600' };
    } else if (rating >= 2.5) {
      return { level: 'average', text: '보통', color: 'text-yellow-600' };
    } else {
      return { level: 'poor', text: '나쁨', color: 'text-red-600' };
    }
  }

  /**
   * 별 개수 계산 (전체별, 반별, 빈별)
   */
  static getStarCounts(rating: number): {
    fullStars: number;
    hasHalfStar: boolean;
    emptyStars: number;
  } {
    const roundedRating = this.roundToHalfStar(rating);
    const fullStars = Math.floor(roundedRating);
    const hasHalfStar = roundedRating % 1 !== 0;
    const emptyStars = 5 - Math.ceil(roundedRating);

    return {
      fullStars,
      hasHalfStar,
      emptyStars
    };
  }
}

export default RatingCalculator;