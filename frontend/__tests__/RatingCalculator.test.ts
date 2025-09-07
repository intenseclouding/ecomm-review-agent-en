import { RatingCalculator } from '../utils/ratingCalculator';
import { Review } from '../services/productApiService';

// 테스트용 리뷰 데이터
const createMockReview = (rating: number, id: string = 'test'): Review => ({
  id,
  user_name: 'Test User',
  rating,
  content: 'Test review',
  date: '2024-01-01',
  verified_purchase: true
});

describe('RatingCalculator', () => {
  describe('calculateAverageRating', () => {
    test('calculates correct average for multiple reviews', () => {
      const reviews = [
        createMockReview(5, 'r1'),
        createMockReview(4, 'r2'),
        createMockReview(3, 'r3'),
        createMockReview(2, 'r4'),
        createMockReview(1, 'r5')
      ];

      const average = RatingCalculator.calculateAverageRating(reviews);
      expect(average).toBe(3.0);
    });

    test('returns 0 for empty review array', () => {
      const average = RatingCalculator.calculateAverageRating([]);
      expect(average).toBe(0);
    });

    test('handles single review correctly', () => {
      const reviews = [createMockReview(4.5)];
      const average = RatingCalculator.calculateAverageRating(reviews);
      expect(average).toBe(4.5);
    });

    test('filters out invalid ratings', () => {
      const reviews = [
        createMockReview(5, 'r1'),
        createMockReview(0, 'r2'), // Invalid
        createMockReview(4, 'r3'),
        createMockReview(6, 'r4'), // Invalid
        createMockReview(3, 'r5')
      ];

      const average = RatingCalculator.calculateAverageRating(reviews);
      expect(average).toBe(4.0); // (5 + 4 + 3) / 3
    });

    test('rounds to one decimal place', () => {
      const reviews = [
        createMockReview(4, 'r1'),
        createMockReview(4, 'r2'),
        createMockReview(5, 'r3')
      ];

      const average = RatingCalculator.calculateAverageRating(reviews);
      expect(average).toBe(4.3); // (4 + 4 + 5) / 3 = 4.333... -> 4.3
    });
  });

  describe('roundToHalfStar', () => {
    test('rounds 3.2 to 3.0', () => {
      expect(RatingCalculator.roundToHalfStar(3.2)).toBe(3.0);
    });

    test('rounds 3.3 to 3.5', () => {
      expect(RatingCalculator.roundToHalfStar(3.3)).toBe(3.5);
    });

    test('rounds 3.7 to 3.5', () => {
      expect(RatingCalculator.roundToHalfStar(3.7)).toBe(3.5);
    });

    test('rounds 3.8 to 4.0', () => {
      expect(RatingCalculator.roundToHalfStar(3.8)).toBe(4.0);
    });

    test('handles exact half values', () => {
      expect(RatingCalculator.roundToHalfStar(3.5)).toBe(3.5);
      expect(RatingCalculator.roundToHalfStar(4.5)).toBe(4.5);
    });

    test('handles edge cases', () => {
      expect(RatingCalculator.roundToHalfStar(0)).toBe(0);
      expect(RatingCalculator.roundToHalfStar(5)).toBe(5);
      expect(RatingCalculator.roundToHalfStar(0.1)).toBe(0);
      expect(RatingCalculator.roundToHalfStar(4.9)).toBe(5);
    });
  });

  describe('calculateRatingDistribution', () => {
    test('calculates correct distribution', () => {
      const reviews = [
        createMockReview(5, 'r1'),
        createMockReview(5, 'r2'),
        createMockReview(4, 'r3'),
        createMockReview(3, 'r4'),
        createMockReview(1, 'r5')
      ];

      const distribution = RatingCalculator.calculateRatingDistribution(reviews);
      expect(distribution).toEqual({
        1: 1,
        2: 0,
        3: 1,
        4: 1,
        5: 2
      });
    });

    test('returns zero distribution for empty reviews', () => {
      const distribution = RatingCalculator.calculateRatingDistribution([]);
      expect(distribution).toEqual({
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0
      });
    });

    test('ignores invalid ratings', () => {
      const reviews = [
        createMockReview(5, 'r1'),
        createMockReview(0, 'r2'), // Invalid
        createMockReview(6, 'r3'), // Invalid
        createMockReview(4, 'r4')
      ];

      const distribution = RatingCalculator.calculateRatingDistribution(reviews);
      expect(distribution).toEqual({
        1: 0,
        2: 0,
        3: 0,
        4: 1,
        5: 1
      });
    });
  });

  describe('calculateRatingPercentages', () => {
    test('calculates correct percentages', () => {
      const reviews = [
        createMockReview(5, 'r1'),
        createMockReview(5, 'r2'),
        createMockReview(4, 'r3'),
        createMockReview(3, 'r4')
      ];

      const percentages = RatingCalculator.calculateRatingPercentages(reviews);
      expect(percentages).toEqual({
        1: 0,
        2: 0,
        3: 25, // 1/4 = 25%
        4: 25, // 1/4 = 25%
        5: 50  // 2/4 = 50%
      });
    });

    test('returns zero percentages for empty reviews', () => {
      const percentages = RatingCalculator.calculateRatingPercentages([]);
      expect(percentages).toEqual({
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0
      });
    });
  });

  describe('calculateRatingStats', () => {
    test('calculates comprehensive rating statistics', () => {
      const reviews = [
        createMockReview(5, 'r1'),
        createMockReview(4, 'r2'),
        createMockReview(3, 'r3')
      ];

      const stats = RatingCalculator.calculateRatingStats(reviews);
      
      expect(stats.averageRating).toBe(4.0);
      expect(stats.roundedRating).toBe(4.0);
      expect(stats.totalReviews).toBe(3);
      expect(stats.ratingDistribution).toEqual({
        1: 0,
        2: 0,
        3: 1,
        4: 1,
        5: 1
      });
    });
  });

  describe('isValidRating', () => {
    test('validates correct ratings', () => {
      expect(RatingCalculator.isValidRating(1)).toBe(true);
      expect(RatingCalculator.isValidRating(3)).toBe(true);
      expect(RatingCalculator.isValidRating(5)).toBe(true);
      expect(RatingCalculator.isValidRating(4.5)).toBe(true);
    });

    test('rejects invalid ratings', () => {
      expect(RatingCalculator.isValidRating(0)).toBe(false);
      expect(RatingCalculator.isValidRating(6)).toBe(false);
      expect(RatingCalculator.isValidRating(-1)).toBe(false);
      expect(RatingCalculator.isValidRating('4')).toBe(false);
      expect(RatingCalculator.isValidRating(null)).toBe(false);
      expect(RatingCalculator.isValidRating(undefined)).toBe(false);
    });
  });

  describe('getRatingText', () => {
    test('generates correct rating text', () => {
      expect(RatingCalculator.getRatingText(4.2)).toBe('5점 만점에 4.0점');
      expect(RatingCalculator.getRatingText(4.2, 10)).toBe('5점 만점에 4.0점 (10개 리뷰)');
      expect(RatingCalculator.getRatingText(3.7, 0)).toBe('5점 만점에 3.5점');
    });
  });

  describe('getRatingQuality', () => {
    test('returns correct quality levels', () => {
      expect(RatingCalculator.getRatingQuality(0)).toEqual({
        level: 'none',
        text: '평점 없음',
        color: 'text-gray-400'
      });

      expect(RatingCalculator.getRatingQuality(4.8)).toEqual({
        level: 'excellent',
        text: '우수',
        color: 'text-green-600'
      });

      expect(RatingCalculator.getRatingQuality(4.0)).toEqual({
        level: 'good',
        text: '좋음',
        color: 'text-blue-600'
      });

      expect(RatingCalculator.getRatingQuality(3.0)).toEqual({
        level: 'average',
        text: '보통',
        color: 'text-yellow-600'
      });

      expect(RatingCalculator.getRatingQuality(2.0)).toEqual({
        level: 'poor',
        text: '나쁨',
        color: 'text-red-600'
      });
    });
  });

  describe('getStarCounts', () => {
    test('calculates correct star counts for various ratings', () => {
      expect(RatingCalculator.getStarCounts(3.5)).toEqual({
        fullStars: 3,
        hasHalfStar: true,
        emptyStars: 1
      });

      expect(RatingCalculator.getStarCounts(4.0)).toEqual({
        fullStars: 4,
        hasHalfStar: false,
        emptyStars: 1
      });

      expect(RatingCalculator.getStarCounts(4.7)).toEqual({
        fullStars: 4,
        hasHalfStar: true,
        emptyStars: 0
      });

      expect(RatingCalculator.getStarCounts(0)).toEqual({
        fullStars: 0,
        hasHalfStar: false,
        emptyStars: 5
      });

      expect(RatingCalculator.getStarCounts(5.0)).toEqual({
        fullStars: 5,
        hasHalfStar: false,
        emptyStars: 0
      });
    });
  });
});