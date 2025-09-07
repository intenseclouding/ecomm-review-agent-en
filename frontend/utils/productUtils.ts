import { SidebarProduct, CategoryGroup, ProductSummary } from '../types/product';
import { productApiService } from '../services/productApiService';

// API에서 제품 데이터를 가져와 사이드바용으로 변환
export const convertToSidebarProducts = async (): Promise<SidebarProduct[]> => {
  try {
    const productSummaries = await productApiService.getProductSummaries();
    
    return productSummaries.map((product: ProductSummary): SidebarProduct => ({
      id: product.id,
      name: product.name,
      category: product.category,
      price: product.price,
      emoji: product.emoji,
      averageRating: product.average_rating,
      reviewCount: product.review_count
    }));
  } catch (error) {
    console.error('Error fetching products for sidebar:', error);
    // 에러 발생 시 빈 배열 반환
    return [];
  }
};

// 동기 버전 (기존 호환성을 위해 유지, 하지만 빈 배열 반환)
export const convertToSidebarProductsSync = (): SidebarProduct[] => {
  console.warn('convertToSidebarProductsSync is deprecated. Use convertToSidebarProducts instead.');
  return [];
};

// 제품을 카테고리별로 그룹화
export const groupProductsByCategory = (products: SidebarProduct[]): CategoryGroup[] => {
  const categoryMap = new Map<string, SidebarProduct[]>();

  // 카테고리별로 제품 분류
  products.forEach(product => {
    if (!categoryMap.has(product.category)) {
      categoryMap.set(product.category, []);
    }
    categoryMap.get(product.category)!.push(product);
  });

  // CategoryGroup 배열로 변환
  const categoryGroups: CategoryGroup[] = [];
  categoryMap.forEach((products, category) => {
    categoryGroups.push({
      category,
      products: products.sort((a, b) => a.name.localeCompare(b.name)), // 이름순 정렬
      isExpanded: true, // 기본적으로 모든 카테고리 펼침
    });
  });

  // 카테고리명으로 정렬
  return categoryGroups.sort((a, b) => a.category.localeCompare(b.category));
};

// 제품 가격 포맷팅 (한국 원화)
export const formatPrice = (price: number): string => {
  return `₩${price.toLocaleString()}`;
};

// 카테고리별 제품 개수 계산
export const getCategoryProductCount = (categoryGroups: CategoryGroup[]): { [key: string]: number } => {
  const countMap: { [key: string]: number } = {};
  
  categoryGroups.forEach(group => {
    countMap[group.category] = group.products.length;
  });
  
  return countMap;
};