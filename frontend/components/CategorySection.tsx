import React from 'react';
import ProductItem from './ProductItem';
import { SidebarProduct } from '../types/product';

interface CategorySectionProps {
  category: string;
  products: SidebarProduct[];
  isExpanded: boolean;
  currentProductId?: string;
  onToggle: () => void;
}

export default function CategorySection({
  category,
  products,
  isExpanded,
  currentProductId,
  onToggle,
}: CategorySectionProps) {
  // 제품이 없는 카테고리는 렌더링하지 않음
  if (products.length === 0) {
    return null;
  }

  return (
    <div className="mb-1">
      {/* 카테고리 헤더 */}
      <div
        className="category-header flex items-center justify-between"
        onClick={onToggle}
      >
        <span className="font-bold">{category}</span>
        <div className="flex items-center space-x-2">
          <span className="text-xs text-gray-500">({products.length})</span>
          <span className={`category-toggle text-xs ${isExpanded ? 'expanded' : ''}`}>
            ▶
          </span>
        </div>
      </div>

      {/* 제품 목록 */}
      <div className={`overflow-hidden transition-all duration-300 ${isExpanded ? 'max-h-96 opacity-100' : 'max-h-0 opacity-0'}`}>
        <div className="ml-2">
          {products.map((product) => (
            <ProductItem
              key={product.id}
              product={product}
              isActive={currentProductId === product.id}
            />
          ))}
        </div>
      </div>
    </div>
  );
}