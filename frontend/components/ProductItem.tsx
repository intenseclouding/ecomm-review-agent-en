import React from 'react';
import Link from 'next/link';
import { SidebarProduct } from '../types/product';
import { formatPrice } from '../utils/productUtils';
import StarRating from './StarRating';

interface ProductItemProps {
  product: SidebarProduct;
  isActive: boolean;
}

export default function ProductItem({ product, isActive }: ProductItemProps) {
  return (
    <Link href={`/product/${product.id}`}>
      <div
        className={`product-item flex items-center ${
          isActive ? 'product-item-active' : ''
        }`}
      >
        {/* 제품 이모지 */}
        <span className="product-emoji">{product.emoji}</span>
        
        {/* 제품 정보 */}
        <div className="product-info">
          <div className="product-name" title={product.name}>
            {product.name}
          </div>
          <div className="product-price">
            {formatPrice(product.price)}
          </div>
          {/* 평점 표시 (있는 경우) */}
          {product.averageRating !== undefined && product.reviewCount !== undefined && (
            <div className="mt-1">
              <StarRating 
                rating={product.averageRating}
                size="small"
                showCount={false}
                reviewCount={product.reviewCount}
              />
            </div>
          )}
        </div>
      </div>
    </Link>
  );
}