import React, { useState, useEffect } from 'react';
import ReviewForm from './ReviewForm';
import ReviewList from './ReviewList';
import ReviewAnalytics from './ReviewAnalytics';
import StarRating from './StarRating';
import { productApiService } from '../services/productApiService';
import { ProductDetail as ProductDetailType } from '../types/product';

// 타입은 이제 productApiService에서 import

interface ProductDetailProps {
  productId: string;
}

const ProductDetail: React.FC<ProductDetailProps> = ({ productId }) => {
  const [product, setProduct] = useState<ProductDetailType | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showReviewForm, setShowReviewForm] = useState(false);

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

  useEffect(() => {
    fetchProduct();
  }, [productId]);

  const fetchProduct = async () => {
    try {
      setLoading(true);
      setError(null);
      const productData = await productApiService.getProductDetail(productId);
      setProduct(productData);
    } catch (err) {
      console.error('Error fetching product:', err);
      setError(err instanceof Error ? err.message : '제품을 불러오는데 실패했습니다.');
    } finally {
      setLoading(false);
    }
  };

  const handleReviewSubmitted = () => {
    setShowReviewForm(false);
    fetchProduct(); // 새 리뷰 반영을 위해 제품 정보 다시 로드
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center text-red-500 p-8">
        <p>{error}</p>
        <button 
          onClick={fetchProduct}
          className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          다시 시도
        </button>
      </div>
    );
  }

  if (!product) {
    return <div className="text-center p-8">제품을 찾을 수 없습니다.</div>;
  }

  // 제품별 시각적 요소 매핑
  const getProductVisuals = (productId: string, category: string) => {
    const visuals = {
      'PROD-001': { emoji: '🎧', gradient: 'from-blue-400 to-purple-500' },
      'PROD-002': { emoji: '👕', gradient: 'from-pink-400 to-rose-500' },
      'PROD-003': { emoji: '✨', gradient: 'from-yellow-400 to-orange-500' },
      'PROD-004': { emoji: '⌚', gradient: 'from-gray-400 to-gray-600' },
      'PROD-005': { emoji: '🧥', gradient: 'from-indigo-400 to-blue-600' },
    };
    return visuals[productId as keyof typeof visuals] || { emoji: '📦', gradient: 'from-gray-300 to-gray-500' };
  };

  const productVisuals = getProductVisuals(product.id, product.category);

  return (
    <div className="max-w-6xl mx-auto p-6">
      {/* 제품 정보 섹션 */}
      <div className="bg-white rounded-xl shadow-xl p-8 mb-8 border border-gray-100">
        <div className="grid md:grid-cols-2 gap-10">
          <div>
            <div className="w-full h-96 rounded-xl relative overflow-hidden shadow-lg bg-white">
              <img 
                src={`/images/output/${getImageName(product.id)}.png`}
                alt={product.name}
                className="w-full h-full object-cover rounded-xl"
                onError={(e) => {
                  // 이미지 로드 실패 시 그라데이션 배경으로 대체
                  e.currentTarget.style.display = 'none';
                  const fallback = e.currentTarget.nextElementSibling as HTMLElement;
                  if (fallback) fallback.style.display = 'flex';
                }}
              />
              <div className={`w-full h-96 bg-gradient-to-br ${productVisuals.gradient} rounded-xl hidden items-center justify-center relative overflow-hidden shadow-lg`}>
                <div className="text-center z-10">
                  <div className="text-9xl mb-4 filter drop-shadow-2xl animate-pulse">
                    {productVisuals.emoji}
                  </div>
                  <p className="text-white font-bold text-lg bg-black bg-opacity-30 px-4 py-2 rounded-full backdrop-blur-sm">
                    {product.category} 제품
                  </p>
                </div>
                {/* 장식적 요소들 */}
                <div className="absolute top-6 right-6 w-12 h-12 bg-white bg-opacity-20 rounded-full animate-bounce"></div>
                <div className="absolute bottom-6 left-6 w-8 h-8 bg-white bg-opacity-15 rounded-full"></div>
                <div className="absolute top-1/2 left-6 w-6 h-6 bg-white bg-opacity-10 rounded-full"></div>
                <div className="absolute bottom-1/3 right-8 w-10 h-10 bg-white bg-opacity-10 rounded-full"></div>
              </div>
            </div>
          </div>
          
          <div>
            <div className="mb-4">
              <span className={`inline-block px-3 py-1 rounded-full text-sm font-medium bg-gradient-to-r ${productVisuals.gradient} text-white`}>
                {product.category}
              </span>
            </div>
            
            <h1 className="text-4xl font-bold mb-4 text-gray-900">{product.name}</h1>
            
            <div className="flex items-center mb-6">
              <p className="text-3xl font-bold text-blue-600 mr-4">
                ₩{product.price.toLocaleString()}
              </p>
              <span className="bg-red-100 text-red-800 text-sm px-2 py-1 rounded-full font-medium">
                무료배송
              </span>
            </div>
            
            <div className="flex items-center mb-6 p-4 bg-yellow-50 rounded-lg">
              <StarRating 
                rating={product.average_rating}
                size="large"
                showCount={true}
                reviewCount={product.review_count}
              />
            </div>
            
            <p className="text-gray-700 mb-8 text-lg leading-relaxed">{product.description}</p>
            
            <div className="mb-8 p-6 bg-gray-50 rounded-lg">
              <h3 className="font-bold mb-4 text-lg text-gray-800">✨ 주요 특징</h3>
              <ul className="space-y-2">
                {product.features.map((feature, index) => (
                  <li key={`feature-${index}`} className="flex items-center text-gray-700">
                    <span className="w-2 h-2 bg-blue-500 rounded-full mr-3"></span>
                    {feature}
                  </li>
                ))}
              </ul>
            </div>
            
            <div className="flex justify-center">
              <button 
                onClick={() => setShowReviewForm(true)}
                className="px-8 py-4 bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-xl hover:from-blue-600 hover:to-blue-700 transition-all duration-300 font-semibold text-lg shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
              >
                ✍️ 리뷰 작성
              </button>
            </div>
            
            {/* AI 자동화 안내 */}
            <div className="mt-6 p-4 bg-green-50 rounded-lg border border-green-200">
              <div className="flex items-center mb-2">
                <span className="text-green-600 mr-2">🤖</span>
                <span className="font-semibold text-green-800">AI 자동화 기능</span>
              </div>
              <p className="text-green-700 text-sm">
                리뷰 작성 시 Strands Agent가 자동으로 감정 분석, 키워드 추출, 스팸 탐지를 수행하고 
                셀러 맞춤 댓글을 생성합니다.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* 리뷰 작성 폼 */}
      {showReviewForm && (
        <div className="mb-8">
          <ReviewForm 
            productId={product.id}
            onSubmitted={handleReviewSubmitted}
            onCancel={() => setShowReviewForm(false)}
          />
        </div>
      )}

      {/* 리뷰 분석 통계 */}
      {product.reviews.length > 0 && (
        <div className="mb-8">
          <ReviewAnalytics reviews={product.reviews} />
        </div>
      )}

      {/* 리뷰 목록 */}
      <ReviewList 
        reviews={product.reviews} 
        productFeatures={product.features}
      />
    </div>
  );
};

export default ProductDetail;