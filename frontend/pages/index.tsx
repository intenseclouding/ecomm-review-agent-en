import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import Layout from '../components/Layout';
import StarRating from '../components/StarRating';
import { productApiService } from '../services/productApiService';
import { ProductSummary } from '../types/product';

export default function Home() {
  const [products, setProducts] = useState<ProductSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const getImageName = (productId: string) => {
    const imageMap: { [key: string]: string } = {
      'PROD-001': 'earphone',
      'PROD-002': 'crop-knit',
      'PROD-003': 'vitamin-serum',
      'PROD-004': 'smart-watch',
      'PROD-005': 'denim-jacket'
    };
    return imageMap[productId] || 'default';
  };

  const getProductGradient = (productId: string) => {
    const gradientMap: { [key: string]: string } = {
      'PROD-001': 'from-blue-400 to-purple-500',
      'PROD-002': 'from-pink-400 to-rose-500',
      'PROD-003': 'from-yellow-400 to-orange-500',
      'PROD-004': 'from-gray-400 to-gray-600',
      'PROD-005': 'from-indigo-400 to-blue-600'
    };
    return gradientMap[productId] || 'from-gray-300 to-gray-500';
  };

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      setLoading(true);
      setError(null);
      const productSummaries = await productApiService.getProductSummaries();
      setProducts(productSummaries);
    } catch (err) {
      console.error('Error fetching products:', err);
      setError(err instanceof Error ? err.message : '제품을 불러오는데 실패했습니다.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout>
      <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <h1 className="text-2xl font-bold text-gray-800">
            🛍️ 제품 리뷰 자동화 데모
          </h1>
          <p className="text-gray-600 mt-1">
            Strands Agent 기반 리뷰 분석 및 자동 댓글 생성 시스템
          </p>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-8">
        <div className="mb-8">
          <h2 className="text-xl font-semibold mb-4">샘플 제품 목록</h2>
          <p className="text-gray-600 mb-6">
            아래 제품들을 클릭하여 리뷰 작성 및 AI 자동화 기능을 체험해보세요.
          </p>
        </div>

        {loading ? (
          <div className="flex justify-center items-center py-16">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
            <span className="ml-4 text-gray-600">제품을 불러오는 중...</span>
          </div>
        ) : error ? (
          <div className="text-center py-16">
            <div className="text-red-500 mb-4">
              <p className="text-lg font-semibold">오류가 발생했습니다</p>
              <p className="text-sm">{error}</p>
            </div>
            <button 
              onClick={fetchProducts}
              className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
            >
              다시 시도
            </button>
          </div>
        ) : products.length === 0 ? (
          <div className="text-center py-16 text-gray-500">
            <p>표시할 제품이 없습니다.</p>
          </div>
        ) : (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {products.map((product) => (
              <Link key={product.id} href={`/product/${product.id}`}>
                <div className="bg-white rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 cursor-pointer transform hover:-translate-y-1">
                  <div className="h-48 rounded-t-xl relative overflow-hidden">
                    <img 
                      src={`/images/output/${getImageName(product.id)}.png`}
                      alt={product.name}
                      className="w-full h-full object-cover"
                      onError={(e) => {
                        // 이미지 로드 실패 시 그라데이션 배경으로 대체
                        e.currentTarget.style.display = 'none';
                        const fallback = e.currentTarget.nextElementSibling as HTMLElement;
                        if (fallback) fallback.style.display = 'flex';
                      }}
                    />
                    <div className={`h-48 bg-gradient-to-br ${getProductGradient(product.id)} rounded-t-xl hidden items-center justify-center relative overflow-hidden`}>
                      <div className="text-center z-10">
                        <div className="text-6xl mb-2 filter drop-shadow-lg">
                          {product.emoji}
                        </div>
                        <span className="text-white font-medium text-sm bg-black bg-opacity-20 px-3 py-1 rounded-full backdrop-blur-sm">
                          {product.category}
                        </span>
                      </div>
                      {/* 장식적 요소 */}
                      <div className="absolute top-4 right-4 w-8 h-8 bg-white bg-opacity-20 rounded-full"></div>
                      <div className="absolute bottom-4 left-4 w-6 h-6 bg-white bg-opacity-10 rounded-full"></div>
                    </div>
                    {/* 카테고리 오버레이 */}
                    <div className="absolute top-3 left-3">
                      <span className="text-white font-medium text-xs bg-black bg-opacity-50 px-2 py-1 rounded-full backdrop-blur-sm">
                        {product.category}
                      </span>
                    </div>
                  </div>
                  <div className="p-5">
                    <h3 className="font-bold text-lg mb-1 text-gray-800">{product.name}</h3>
                    <div className="flex items-center justify-between mb-3">
                      <p className="text-2xl font-bold text-blue-600">
                        ₩{product.price.toLocaleString()}
                      </p>
                      <StarRating 
                        rating={product.average_rating}
                        size="small"
                        showCount={true}
                        reviewCount={product.review_count}
                      />
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="inline-block bg-blue-100 text-blue-800 text-xs px-3 py-1 rounded-full font-medium">
                        {product.category}
                      </span>
                      <span className="inline-block bg-green-100 text-green-800 text-xs px-3 py-1 rounded-full font-medium">
                        🤖 AI 자동화
                      </span>
                    </div>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        )}

        <div className="mt-12 bg-blue-50 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-blue-800 mb-4">
            🤖 AI 자동화 기능
          </h3>
          <div className="grid md:grid-cols-2 gap-4 text-sm text-blue-700">
            <div>
              <h4 className="font-semibold mb-2">리뷰 분석</h4>
              <ul className="list-disc list-inside space-y-1">
                <li>감정 분석 (긍정/부정/중립)</li>
                <li>핵심 키워드 자동 추출</li>
                <li>스팸/가짜 리뷰 탐지</li>
                <li>주제별 카테고리 분류</li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-2">자동 댓글 생성</h4>
              <ul className="list-disc list-inside space-y-1">
                <li>브랜드 맞춤 톤앤매너</li>
                <li>감정에 적절한 응답</li>
                <li>댓글 품질 자동 검증</li>
                <li>셀러 승인 시스템</li>
              </ul>
            </div>
          </div>
        </div>
      </main>

      <footer className="bg-gradient-to-r from-gray-50 to-blue-50 border-t mt-16">
        <div className="max-w-6xl mx-auto px-6 py-8">
          <div className="text-center">
            <div className="mb-6">
              <p className="text-lg font-semibold text-gray-800 mb-2">🤖 Powered by Strands Agents</p>
              <p className="text-sm text-gray-600 mb-4">
                이 데모는 AI 기반 리뷰 분석 및 자동 댓글 생성 시스템을 보여줍니다.
              </p>
            </div>
            
            <div className="border-t border-gray-200 pt-6">
              <div className="flex flex-col md:flex-row items-center justify-center gap-4 text-sm text-gray-500">
                <div className="flex items-center gap-2">
                  <span className="text-purple-500">🎨</span>
                  <span>모든 이미지는 <strong className="text-purple-600">Amazon Nova Canvas</strong>로 생성</span>
                </div>
                <div className="hidden md:block text-gray-300">•</div>
                <div className="flex items-center gap-2">
                  <span className="text-blue-500">💻</span>
                  <span>개발은 <strong className="text-blue-600">Amazon Q Developer</strong>와 <strong className="text-green-600">Kiro</strong>로 100% 완성</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </footer>
      </div>
    </Layout>
  );
}