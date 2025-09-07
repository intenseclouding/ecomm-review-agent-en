export interface SidebarProduct {
  id: string;
  name: string;
  category: string;
  price: number;
  emoji: string;
  averageRating?: number;
  reviewCount?: number;
}

export interface CategoryGroup {
  category: string;
  products: SidebarProduct[];
  isExpanded: boolean;
}

export interface CategoryState {
  [categoryName: string]: {
    isExpanded: boolean;
    productCount: number;
  };
}

// 평점 관련 타입 정의
export interface RatingDistribution {
  1: number;
  2: number;
  3: number;
  4: number;
  5: number;
}

export interface RatingStats {
  averageRating: number;
  totalReviews: number;
  ratingDistribution: RatingDistribution;
  roundedRating: number;
}

export interface RatingQuality {
  level: 'excellent' | 'good' | 'average' | 'poor' | 'none';
  text: string;
  color: string;
}

// 감정 분석 타입
export interface SentimentAnalysis {
  label: string;
  confidence: number;
  polarity: number;
}

// 셀러 응답 타입
export interface SellerResponse {
  content: string;
  date: string;
}

// 리뷰 타입 (확장된 버전)
export interface Review {
  id: string;
  user_name: string;
  rating: number;
  content: string;
  date: string;
  verified_purchase: boolean;
  auto_response?: string;
  response_approved?: boolean;
  keywords?: string[];
  sentiment?: SentimentAnalysis;
  analysis_completed?: boolean;
  analysis_timestamp?: string;
  seller_response?: SellerResponse;
  agent_log_id?: string;
}

// 제품 기본 정보 타입
export interface ProductBase {
  id: string;
  name: string;
  category: string;
  price: number;
  description: string;
  image_url: string;
  emoji: string;
}

// 제품 요약 정보 타입 (홈페이지, 사이드바용)
export interface ProductSummary extends ProductBase {
  average_rating: number;
  review_count: number;
}

// 제품 상세 정보 타입
export interface ProductDetail extends ProductSummary {
  seller_id: string;
  features: string[];
  reviews: Review[];
  rating_distribution: RatingDistribution;
}

// API 응답 타입
export interface ProductListResponse {
  products: ProductSummary[];
  total: number;
  page?: number;
  limit?: number;
}

export interface ProductDetailResponse extends ProductDetail {}

// 에러 응답 타입
export interface ApiError {
  detail: string;
  code?: string;
  timestamp?: string;
}

// 로딩 상태 타입
export interface LoadingState {
  isLoading: boolean;
  error: string | null;
}

// 캐시 엔트리 타입
export interface CacheEntry<T> {
  data: T;
  timestamp: number;
  ttl?: number;
}