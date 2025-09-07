import { useRouter } from 'next/router';
import Layout from '../../components/Layout';
import ProductDetail from '../../components/ProductDetail';

export default function ProductPage() {
  const router = useRouter();
  const { id } = router.query;

  if (!id || typeof id !== 'string') {
    return (
      <Layout>
        <div className="text-center p-8">잘못된 제품 ID입니다.</div>
      </Layout>
    );
  }

  return (
    <Layout currentProductId={id}>
      <div className="min-h-screen bg-gray-50">
        <header className="bg-white shadow-sm">
          <div className="max-w-6xl mx-auto px-6 py-4">
            <h1 className="text-xl font-bold text-gray-800">
              🛍️ 제품 리뷰 자동화 데모
            </h1>
            <p className="text-sm text-gray-600 mt-1">
              Strands Agent 기반 리뷰 분석 및 자동 댓글 생성 시스템
            </p>
          </div>
        </header>
        
        <main className="py-8">
          <ProductDetail productId={id} />
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