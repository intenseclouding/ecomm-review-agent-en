import React from 'react';
import Sidebar from './Sidebar';
import { useCurrentProduct } from '../hooks/useCurrentProduct';

interface LayoutProps {
  children: React.ReactNode;
  currentProductId?: string; // 수동으로 전달할 수도 있음
}

export default function Layout({ children, currentProductId }: LayoutProps) {
  // 자동으로 현재 제품 ID 감지
  const autoDetectedProductId = useCurrentProduct();
  
  // 수동으로 전달된 ID가 있으면 우선 사용, 없으면 자동 감지된 ID 사용
  const activeProductId = currentProductId || autoDetectedProductId;

  return (
    <div className="flex min-h-screen bg-gray-50">
      {/* 사이드바 */}
      <Sidebar currentProductId={activeProductId} />
      
      {/* 메인 콘텐츠 영역 */}
      <main className="flex-1 ml-0 md:ml-240 lg:ml-256 xl:ml-280 transition-all duration-300">
        {children}
      </main>
    </div>
  );
}