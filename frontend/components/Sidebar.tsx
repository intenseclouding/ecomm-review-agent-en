import React, { useState, useEffect, useMemo } from 'react';
import CategorySection from './CategorySection';
import ViewModeToggle, { ViewMode } from './ViewModeToggle';
import AllProductsList from './AllProductsList';
import { CategoryGroup, SidebarProduct } from '../types/product';
import { convertToSidebarProducts, groupProductsByCategory } from '../utils/productUtils';

interface SidebarProps {
  currentProductId?: string;
}

export default function Sidebar({ currentProductId }: SidebarProps) {
  const [categories, setCategories] = useState<CategoryGroup[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [viewMode, setViewMode] = useState<ViewMode>('category');
  const [allProducts, setAllProducts] = useState<SidebarProduct[]>([]);
  const [savedCategoryStates, setSavedCategoryStates] = useState<{ [key: string]: boolean }>({});

  // 컴포넌트 마운트 시 제품 데이터 로드
  useEffect(() => {
    const loadProducts = async () => {
      try {
        const products = await convertToSidebarProducts();
        const groupedCategories = groupProductsByCategory(products);
        setCategories(groupedCategories);
        setAllProducts(products);
      } catch (error) {
        console.error('제품 데이터 로딩 실패:', error);
      } finally {
        setIsLoading(false);
      }
    };

    loadProducts();
  }, []);

  // 전체 제품 목록을 이름순으로 정렬
  const sortedAllProducts = useMemo(() => {
    return [...allProducts].sort((a, b) => a.name.localeCompare(b.name, 'ko'));
  }, [allProducts]);

  // 보기 모드 변경 핸들러
  const handleModeChange = (mode: ViewMode) => {
    if (mode === 'all' && viewMode === 'category') {
      // 카테고리별 보기에서 전체 보기로 전환 시 현재 상태 저장
      const currentStates: { [key: string]: boolean } = {};
      categories.forEach(cat => {
        currentStates[cat.category] = cat.isExpanded;
      });
      setSavedCategoryStates(currentStates);
    } else if (mode === 'category' && viewMode === 'all') {
      // 전체 보기에서 카테고리별 보기로 전환 시 이전 상태 복원
      setCategories(prev =>
        prev.map(cat => ({
          ...cat,
          isExpanded: savedCategoryStates[cat.category] ?? cat.isExpanded
        }))
      );
    }
    setViewMode(mode);
  };

  const toggleCategory = (categoryName: string) => {
    setCategories(prev =>
      prev.map(cat =>
        cat.category === categoryName
          ? { ...cat, isExpanded: !cat.isExpanded }
          : cat
      )
    );
  };

  return (
    <div className="sidebar-container">
      {/* 사이드바 헤더 */}
      <div className="sidebar-header">
        <h2 className="sidebar-title">
          {viewMode === 'all' ? '전체 제품' : '제품 카테고리'}
        </h2>
      </div>

      {/* 보기 모드 토글 */}
      <ViewModeToggle 
        currentMode={viewMode} 
        onModeChange={handleModeChange} 
      />

      {/* 제품 목록 */}
      <div className="py-2">
        {isLoading ? (
          <div className="p-4 text-center text-gray-500">
            <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-gray-900 mx-auto"></div>
            <p className="mt-2 text-sm">로딩 중...</p>
          </div>
        ) : viewMode === 'all' ? (
          <AllProductsList 
            products={sortedAllProducts} 
            currentProductId={currentProductId} 
          />
        ) : categories.length === 0 ? (
          <div className="p-4 text-center text-gray-500">
            <p className="text-sm">제품이 없습니다.</p>
          </div>
        ) : (
          categories.map((category) => (
            <CategorySection
              key={category.category}
              category={category.category}
              products={category.products}
              isExpanded={category.isExpanded}
              currentProductId={currentProductId}
              onToggle={() => toggleCategory(category.category)}
            />
          ))
        )}
      </div>
    </div>
  );
}