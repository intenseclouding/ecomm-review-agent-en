import React, { useState } from 'react';
import axios from 'axios';

interface ReviewFormProps {
  productId: string;
  onSubmitted: () => void;
  onCancel: () => void;
}

const ReviewForm: React.FC<ReviewFormProps> = ({ productId, onSubmitted, onCancel }) => {
  const [formData, setFormData] = useState({
    user_name: '',
    rating: 5,
    content: '',
    verified_purchase: true
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitStatus, setSubmitStatus] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.user_name.trim() || !formData.content.trim()) {
      alert('이름과 리뷰 내용을 모두 입력해주세요.');
      return;
    }

    setIsSubmitting(true);
    setSubmitStatus(null);

    try {
      const response = await axios.post(
        `http://localhost:8000/api/products/${productId}/reviews`,
        formData
      );
      
      setSubmitStatus('✅ 리뷰가 성공적으로 등록되었습니다! 검수를 통과하여 자동 응답을 생성 중입니다...');
      
      // 3초 후 폼 닫기
      setTimeout(() => {
        onSubmitted();
      }, 3000);
      
    } catch (error: any) {
      console.error('리뷰 등록 실패:', error);
      
      // 검수 실패 시 상세한 에러 메시지 표시
      if (error.response?.status === 400 && error.response?.data?.error === "리뷰 검수 실패") {
        const errorData = error.response.data;
        setSubmitStatus(
          `❌ 리뷰 검수 실패: ${errorData.reason}\n` +
          `심각도: ${errorData.severity_score}점\n` +
          `문제점: ${errorData.issues?.join(', ') || '부적절한 내용 포함'}\n\n` +
          `리뷰 내용을 수정한 후 다시 시도해주세요.`
        );
      } else {
        setSubmitStatus('❌ 리뷰 등록에 실패했습니다. 다시 시도해주세요.');
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? (e.target as HTMLInputElement).checked : value
    }));
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h2 className="text-2xl font-bold mb-6">리뷰 작성</h2>
      
      {submitStatus && (
        <div className={`p-4 rounded-lg mb-6 ${
          submitStatus.includes('✅') ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
        }`}>
          <pre className="whitespace-pre-wrap text-sm">{submitStatus}</pre>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label htmlFor="user_name" className="block text-sm font-medium text-gray-700 mb-2">
            이름 *
          </label>
          <input
            type="text"
            id="user_name"
            name="user_name"
            value={formData.user_name}
            onChange={handleInputChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="리뷰어 이름을 입력하세요"
            disabled={isSubmitting}
            required
          />
        </div>

        <div>
          <label htmlFor="rating" className="block text-sm font-medium text-gray-700 mb-2">
            평점 *
          </label>
          <select
            id="rating"
            name="rating"
            value={formData.rating}
            onChange={handleInputChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isSubmitting}
          >
            <option value={5}>⭐⭐⭐⭐⭐ (5점) - 매우 만족</option>
            <option value={4}>⭐⭐⭐⭐ (4점) - 만족</option>
            <option value={3}>⭐⭐⭐ (3점) - 보통</option>
            <option value={2}>⭐⭐ (2점) - 불만족</option>
            <option value={1}>⭐ (1점) - 매우 불만족</option>
          </select>
        </div>

        <div>
          <label htmlFor="content" className="block text-sm font-medium text-gray-700 mb-2">
            리뷰 내용 *
          </label>
          <textarea
            id="content"
            name="content"
            value={formData.content}
            onChange={handleInputChange}
            rows={5}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="제품에 대한 솔직한 후기를 작성해주세요. Strands Agent가 자동으로 분석하여 셀러가 적절한 댓글을 달 수 있도록 도와드립니다."
            disabled={isSubmitting}
            required
          />
          <p className="text-sm text-gray-500 mt-1">
            최소 10자 이상 작성해주세요. 작성하신 리뷰는 AI가 자동으로 분석됩니다.
          </p>
        </div>

        <div className="flex items-center">
          <input
            type="checkbox"
            id="verified_purchase"
            name="verified_purchase"
            checked={formData.verified_purchase}
            onChange={handleInputChange}
            className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            disabled={isSubmitting}
          />
          <label htmlFor="verified_purchase" className="ml-2 block text-sm text-gray-700">
            구매 확인된 리뷰입니다
          </label>
        </div>

        <div className="flex gap-4">
          <button
            type="submit"
            disabled={isSubmitting}
            className="flex-1 bg-blue-500 text-white py-3 px-6 rounded-lg hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
          >
            {isSubmitting ? (
              <span className="flex items-center justify-center">
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                등록 중...
              </span>
            ) : (
              '리뷰 등록'
            )}
          </button>
          <button
            type="button"
            onClick={onCancel}
            disabled={isSubmitting}
            className="px-6 py-3 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:bg-gray-100 disabled:cursor-not-allowed transition-colors"
          >
            취소
          </button>
        </div>
      </form>

      <div className="mt-6 p-4 bg-blue-50 rounded-lg">
        <h3 className="font-semibold text-blue-800 mb-2">🛡️ AI 검수 및 자동화 기능</h3>
        <p className="text-sm text-blue-700">
          리뷰 작성 후 Strands Agent가 자동으로:
        </p>
        <ul className="text-sm text-blue-700 mt-2 list-disc list-inside">
          <li><strong>1단계:</strong> 내용 검수 (공격적/선정적 언어 탐지)</li>
          <li><strong>2단계:</strong> 검수 통과 시 감정 분석 및 키워드 추출</li>
          <li><strong>3단계:</strong> 셀러 맞춤 자동 댓글 생성</li>
          <li><strong>4단계:</strong> 댓글 품질 검증 및 승인</li>
        </ul>
        <div className="mt-3 p-2 bg-yellow-100 rounded text-xs text-yellow-800">
          ⚠️ 부적절한 내용이 포함된 리뷰는 검수 단계에서 자동으로 차단됩니다.
        </div>
      </div>
    </div>
  );
};

export default ReviewForm;