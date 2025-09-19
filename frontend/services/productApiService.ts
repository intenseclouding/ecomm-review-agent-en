/**
 * Product API Service - 제품 데이터 API 통신 및 캐싱 관리
 */

import axios, { AxiosResponse } from 'axios';
import {
  ProductSummary,
  ProductDetail,
  Review,
  CacheEntry,
  ApiError,
  LoadingState
} from '../types/product';

// API 기본 설정
const API_BASE_URL = 'http://localhost:8000/api';
const CACHE_DURATION = 5 * 60 * 1000; // 5분

// 캐시 인터페이스는 이제 types에서 import

// 캐시 저장소
class DataCache {
  private cache = new Map<string, CacheEntry<any>>();

  set<T>(key: string, data: T): void {
    this.cache.set(key, {
      data,
      timestamp: Date.now()
    });
  }

  get<T>(key: string): T | null {
    const entry = this.cache.get(key);
    if (!entry) return null;

    // 캐시 만료 확인
    if (Date.now() - entry.timestamp > CACHE_DURATION) {
      this.cache.delete(key);
      return null;
    }

    return entry.data;
  }

  clear(): void {
    this.cache.clear();
  }

  delete(key: string): void {
    this.cache.delete(key);
  }
}

class ProductApiService {
  private cache = new DataCache();
  private axiosInstance;

  constructor() {
    this.axiosInstance = axios.create({
      baseURL: API_BASE_URL,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // 응답 인터셉터 - 에러 처리
    this.axiosInstance.interceptors.response.use(
      (response) => response,
      (error) => {
        console.error('API Error:', error.response?.data || error.message);
        return Promise.reject(error);
      }
    );
  }

  /**
   * 모든 제품 요약 정보 조회
   */
  async getProductSummaries(useCache: boolean = true): Promise<ProductSummary[]> {
    const cacheKey = 'product-summaries';

    if (useCache) {
      const cached = this.cache.get<ProductSummary[]>(cacheKey);
      if (cached) {
        console.log('Using cached product summaries');
        return cached;
      }
    }

    try {
      const response: AxiosResponse<ProductSummary[]> = await this.axiosInstance.get('/products/summaries');
      const summaries = response.data;

      this.cache.set(cacheKey, summaries);
      console.log(`Fetched ${summaries.length} product summaries from API`);

      return summaries;
    } catch (error) {
      console.error('Error fetching product summaries:', error);
      throw new Error('제품 목록을 불러오는데 실패했습니다.');
    }
  }

  /**
   * 특정 제품 상세 정보 조회
   */
  async getProductDetail(productId: string, useCache: boolean = true): Promise<ProductDetail> {
    const cacheKey = `product-detail-${productId}`;

    if (useCache) {
      const cached = this.cache.get<ProductDetail>(cacheKey);
      if (cached) {
        console.log(`Using cached product detail for ${productId}`);
        return cached;
      }
    }

    try {
      const response: AxiosResponse<ProductDetail> = await this.axiosInstance.get(`/products/${productId}`);
      const product = response.data;

      this.cache.set(cacheKey, product);
      console.log(`Fetched product detail for ${productId} from API`);

      return product;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.status === 404) {
        throw new Error('제품을 찾을 수 없습니다.');
      }
      console.error(`Error fetching product detail for ${productId}:`, error);
      throw new Error('제품 정보를 불러오는데 실패했습니다.');
    }
  }

  /**
   * 특정 제품 요약 정보 조회
   */
  async getProductSummary(productId: string, useCache: boolean = true): Promise<ProductSummary> {
    const cacheKey = `product-summary-${productId}`;

    if (useCache) {
      const cached = this.cache.get<ProductSummary>(cacheKey);
      if (cached) {
        console.log(`Using cached product summary for ${productId}`);
        return cached;
      }
    }

    try {
      const response: AxiosResponse<ProductSummary> = await this.axiosInstance.get(`/products/${productId}/summary`);
      const summary = response.data;

      this.cache.set(cacheKey, summary);
      console.log(`Fetched product summary for ${productId} from API`);

      return summary;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.status === 404) {
        throw new Error('제품을 찾을 수 없습니다.');
      }
      console.error(`Error fetching product summary for ${productId}:`, error);
      throw new Error('제품 요약 정보를 불러오는데 실패했습니다.');
    }
  }

  /**
   * 카테고리별 제품 조회
   */
  async getProductsByCategory(category: string, useCache: boolean = true): Promise<ProductDetail[]> {
    const cacheKey = `products-category-${category}`;

    if (useCache) {
      const cached = this.cache.get<ProductDetail[]>(cacheKey);
      if (cached) {
        console.log(`Using cached products for category ${category}`);
        return cached;
      }
    }

    try {
      const response: AxiosResponse<ProductDetail[]> = await this.axiosInstance.get(`/products/category/${category}`);
      const products = response.data;

      this.cache.set(cacheKey, products);
      console.log(`Fetched ${products.length} products for category ${category} from API`);

      return products;
    } catch (error) {
      console.error(`Error fetching products for category ${category}:`, error);
      throw new Error(`${category} 카테고리 제품을 불러오는데 실패했습니다.`);
    }
  }

  /**
   * 키워드로 리뷰 검색
   */
  async searchReviewsByKeyword(keyword: string): Promise<any> {
    try {
      const response = await this.axiosInstance.get(`/keywords/${encodeURIComponent(keyword)}/reviews`);
      console.log(`Searched reviews for keyword: ${keyword}`);
      return response.data;
    } catch (error) {
      console.error(`Error searching reviews for keyword ${keyword}:`, error);
      throw new Error(`"${keyword}" 키워드 검색에 실패했습니다.`);
    }
  }

  /**
   * 캐시 관리 메서드들
   */
  clearCache(): void {
    this.cache.clear();
    console.log('Product cache cleared');
  }

  invalidateProduct(productId: string): void {
    this.cache.delete(`product-detail-${productId}`);
    this.cache.delete(`product-summary-${productId}`);
    console.log(`Cache invalidated for product ${productId}`);
  }

  invalidateProductSummaries(): void {
    this.cache.delete('product-summaries');
    console.log('Product summaries cache invalidated');
  }
}

// 싱글톤 인스턴스 생성
export const productApiService = new ProductApiService();
export default productApiService;