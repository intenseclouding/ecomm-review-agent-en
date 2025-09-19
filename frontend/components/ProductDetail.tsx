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
  const [selectedKeyword, setSelectedKeyword] = useState<string | null>(null);

  const [showFeaturesModal, setShowFeaturesModal] = useState(false);

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
    setSelectedKeyword(null); // 제품 변경 시 키워드 필터 초기화
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
          
          <div className="h-96 flex flex-col justify-between">
            <div>
              <div className="mb-1">
                <span className={`inline-block px-2 py-1 rounded-full text-xs font-medium bg-gradient-to-r ${productVisuals.gradient} text-white`}>
                  {product.category}
                </span>
              </div>
              
              <h1 className="text-2xl font-bold mb-2 text-gray-900">{product.name}</h1>
              
              <div className="flex items-center justify-between mb-3 p-2 bg-gradient-to-r from-blue-50 to-yellow-50 rounded-lg">
                <div className="flex items-center">
                  <p className="text-xl font-bold text-blue-600 mr-2">
                    ₩{product.price.toLocaleString()}
                  </p>
                  <span className="bg-red-100 text-red-800 text-xs px-2 py-1 rounded-full font-medium">
                    무료배송
                  </span>
                </div>
                <div className="flex items-center">
                  <StarRating 
                    rating={product.average_rating}
                    size="small"
                    showCount={true}
                    reviewCount={product.review_count}
                  />
                </div>
              </div>
              
              <p className="text-gray-700 mb-3 text-sm leading-relaxed">{product.description}</p>
              
              <div className="mb-3 p-3 bg-gray-50 rounded-lg">
                <h3 className="font-bold mb-1 text-sm text-gray-800">✨ 주요 특징</h3>
                <div className="grid grid-cols-2 gap-x-2 gap-y-0.5">
                  {product.features.slice(0, 4).map((feature, index) => (
                    <div key={`feature-${index}`} className="flex items-center text-gray-700 text-xs">
                      <span className="w-1 h-1 bg-blue-500 rounded-full mr-1.5 flex-shrink-0"></span>
                      <span className="truncate">{feature}</span>
                    </div>
                  ))}
                  {product.features.length > 4 && (
                    <div className="col-span-2 text-center mt-0.5">
                      <button
                        onClick={() => setShowFeaturesModal(true)}
                        className="text-blue-600 hover:text-blue-800 text-xs font-medium hover:underline transition-colors duration-200"
                      >
                        +{product.features.length - 4}개 더 보기
                      </button>
                    </div>
                  )}
                </div>
              </div>
            </div>
            
            {/* 구매 버튼들 */}
            <div className="space-y-2">
              <div className="flex space-x-2">
                <button 
                  onClick={() => alert('구매 기능은 데모용입니다.')}
                  className="flex-1 px-4 py-2 bg-gradient-to-r from-orange-500 to-orange-600 text-white rounded-lg hover:from-orange-600 hover:to-orange-700 transition-all duration-300 font-semibold text-sm shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 flex items-center justify-center"
                >
                  🛒 구매하기
                </button>
                <button 
                  onClick={() => alert('장바구니 기능은 데모용입니다.')}
                  className="flex-1 px-4 py-2 bg-gradient-to-r from-gray-500 to-gray-600 text-white rounded-lg hover:from-gray-600 hover:to-gray-700 transition-all duration-300 font-semibold text-sm shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 flex items-center justify-center"
                >
                  🛍️ 장바구니
                </button>
              </div>
              
              {/* 배송 정보 */}
              <div className="text-center text-xs text-gray-600 bg-gray-50 rounded-lg p-1.5">
                <span className="font-medium">🚚 오늘 주문 시 내일 도착</span>
                <span className="mx-1">•</span>
                <span>무료배송</span>
              </div>
            </div>

          </div>
        </div>
      </div>

      {/* 리뷰 작성 폼 (토글 방식) */}
      {showReviewForm && (
        <div className="mb-8 animate-in slide-in-from-top duration-300">
          <div className="bg-white rounded-lg shadow-lg border border-blue-200">
            <div className="flex items-center justify-between p-4 border-b border-gray-200 bg-blue-50">
              <h3 className="text-lg font-semibold text-blue-800 flex items-center">
                ✍️ 리뷰 작성
              </h3>
              <button
                onClick={() => {
                  console.log('리뷰 작성 폼 닫기');
                  setShowReviewForm(false);
                }}
                className="text-gray-400 hover:text-gray-600 text-2xl font-bold transition-colors duration-200"
              >
                ×
              </button>
            </div>
            <div className="p-4">
              <ReviewForm 
                productId={product.id}
                onSubmitted={handleReviewSubmitted}
                onCancel={() => setShowReviewForm(false)}
              />
            </div>
          </div>
        </div>
      )}

      {/* 리뷰 분석 통계 */}
      {product.reviews.length > 0 && (
        <div className="mb-8">
          <ReviewAnalytics 
            reviews={product.reviews} 
            onKeywordClick={setSelectedKeyword}
          />
        </div>
      )}

      {/* 리뷰 목록 */}
      <ReviewList 
        reviews={selectedKeyword 
          ? product.reviews.filter(review => 
              review.keywords?.includes(selectedKeyword)
            )
          : product.reviews
        } 
        productFeatures={product.features}
        selectedKeyword={selectedKeyword}
        onKeywordClick={(keyword) => {
          setSelectedKeyword(selectedKeyword === keyword ? null : keyword);
        }}
        onWriteReview={() => {
          console.log('ProductDetail: 리뷰 작성 폼 표시');
          setShowReviewForm(true);
        }}
      />

      {/* 전체 특징 모달 */}
      {showFeaturesModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl shadow-2xl max-w-2xl w-full max-h-96 overflow-hidden">
            <div className="p-6 border-b border-gray-200">
              <div className="flex items-center justify-between">
                <h3 className="text-xl font-bold text-gray-900 flex items-center">
                  ✨ {product.name} - 전체 특징
                </h3>
                <button
                  onClick={() => setShowFeaturesModal(false)}
                  className="text-gray-400 hover:text-gray-600 text-2xl font-bold transition-colors duration-200"
                >
                  ×
                </button>
              </div>
            </div>
            <div className="p-6 overflow-y-auto max-h-80">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {product.features.map((feature, index) => (
                  <div key={`modal-feature-${index}`} className="flex items-start p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors duration-200">
                    <span className="w-2 h-2 bg-blue-500 rounded-full mr-3 mt-1.5 flex-shrink-0"></span>
                    <span className="text-gray-700 text-sm leading-relaxed">{feature}</span>
                  </div>
                ))}
              </div>
            </div>
            <div className="p-4 border-t border-gray-200 bg-gray-50">
              <div className="flex justify-center">
                <button
                  onClick={() => setShowFeaturesModal(false)}
                  className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors duration-200 font-medium"
                >
                  닫기
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ProductDetail;