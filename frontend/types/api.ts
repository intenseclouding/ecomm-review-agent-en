/**
 * API 관련 타입 정의
 */

// HTTP 메서드 타입
export type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH';

// API 응답 상태 타입
export type ApiStatus = 'idle' | 'loading' | 'success' | 'error';

// 페이지네이션 타입
export interface Pagination {
  page: number;
  limit: number;
  total: number;
  totalPages: number;
}

// 정렬 옵션 타입
export interface SortOption {
  field: string;
  direction: 'asc' | 'desc';
}

// 필터 옵션 타입
export interface FilterOption {
  field: string;
  value: any;
  operator?: 'eq' | 'ne' | 'gt' | 'gte' | 'lt' | 'lte' | 'in' | 'like';
}

// API 요청 옵션 타입
export interface ApiRequestOptions {
  method?: HttpMethod;
  headers?: Record<string, string>;
  params?: Record<string, any>;
  timeout?: number;
  retries?: number;
}

// API 응답 래퍼 타입
export interface ApiResponse<T> {
  data: T;
  status: number;
  message?: string;
  timestamp: string;
}

// 에러 응답 타입
export interface ApiErrorResponse {
  error: {
    code: string;
    message: string;
    details?: any;
  };
  status: number;
  timestamp: string;
}

// 캐시 설정 타입
export interface CacheConfig {
  ttl: number; // Time to live in milliseconds
  maxSize?: number; // Maximum number of entries
  strategy?: 'lru' | 'fifo'; // Cache eviction strategy
}

// API 엔드포인트 타입
export interface ApiEndpoint {
  path: string;
  method: HttpMethod;
  cache?: CacheConfig;
}

// 요청 상태 타입
export interface RequestState<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
  lastFetch?: number;
}

export default {};