import React from 'react';
import Link from 'next/link';
import { SidebarProduct } from '../types/product';

interface AllProductsListProps {
  products: SidebarProduct[];
  currentProductId?: string;
}

// 카테고리별 색상 매핑
const getCategoryTagClass = (category: string): string => {
  const categoryMap: { [key: string]: string } = {
    '전자제품': 'bg-blue-100 text-blue-700',
    '패션': 'bg-pink-100 text-pink-700',
    '화장품': 'bg-yellow-100 text-yellow-700',
  };
  return categoryMap[category] || 'bg-gray-100 text-gray-600';
};

export default function AllProductsList({ products, currentProductId }: AllProductsListProps) {
  if (products.length === 0) {
    return (
      <div className="p-4 text-center text-gray-500">
        <p className="text-sm">제품이 없습니다.</p>
      </div>
    );
  }

  return (
    <div className="all-products-list space-y-1">
      {products.map((product) => {
        const isActive = currentProductId === product.id;
        
        return (
          <Link key={product.id} href={`/product/${product.id}`}>
            <div
              className={`all-products-item flex items-center justify-between px-3 py-2 text-sm hover:bg-gray-50 cursor-pointer rounded-md transition-colors ${
                isActive
                  ? 'all-products-item-active bg-orange-50 border-l-2 border-orange-400 text-orange-700'
                  : ''
              }`}
            >
              <div className="flex items-center flex-1 min-w-0">
                <span className="text-base mr-2">{product.emoji}</span>
                <div className="flex-1 min-w-0">
                  <div className="font-medium truncate">
                    {product.name}
                  </div>
                  <div className="text-xs text-gray-500 mt-1">
                    ₩{product.price.toLocaleString()}
                  </div>
                </div>
              </div>
              
              <span
                className={`category-tag inline-block px-2 py-1 text-xs font-medium rounded-full ml-2 ${getCategoryTagClass(
                  product.category
                )}`}
              >
                {product.category}
              </span>
            </div>
          </Link>
        );
      })}
    </div>
  );
}