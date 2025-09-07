# Design Document

## Overview

아마존 스타일의 제품 사이드바 메뉴를 구현하여 사용자가 친숙한 인터페이스로 제품들을 탐색할 수 있도록 합니다. 기존 Next.js + Tailwind CSS 스택을 활용하여 아마존의 디자인 패턴을 모방한 사이드바를 구현합니다.

## Architecture

### Component Structure
```
Layout
├── Sidebar
│   ├── SidebarHeader
│   ├── CategorySection
│   │   └── ProductItem[]
│   └── SidebarFooter (optional)
└── MainContent
```

### Data Flow
1. 제품 데이터는 기존 `sample_products.json`에서 가져옴
2. 카테고리별로 제품을 그룹화하여 사이드바에 표시
3. 현재 페이지 정보를 기반으로 활성 제품 하이라이트

## Components and Interfaces

### 1. Layout Component
**파일**: `frontend/components/Layout.tsx`

전체 페이지 레이아웃을 관리하는 컨테이너 컴포넌트입니다.

```typescript
interface LayoutProps {
  children: React.ReactNode;
  currentProductId?: string;
}
```

**주요 기능**:
- 사이드바와 메인 콘텐츠 영역 배치
- 반응형 레이아웃 관리
- 현재 제품 ID를 사이드바에 전달

### 2. Sidebar Component
**파일**: `frontend/components/Sidebar.tsx`

아마존 스타일의 사이드바 메뉴 컴포넌트입니다.

```typescript
interface SidebarProps {
  currentProductId?: string;
}

interface Product {
  id: string;
  name: string;
  category: string;
  price: number;
  emoji: string;
}

interface CategoryGroup {
  category: string;
  products: Product[];
  isExpanded: boolean;
}
```

**주요 기능**:
- 제품 데이터를 카테고리별로 그룹화
- 카테고리 접기/펼치기 상태 관리
- 현재 제품 하이라이트 표시

### 3. CategorySection Component
**파일**: `frontend/components/CategorySection.tsx`

카테고리별 제품 목록을 표시하는 컴포넌트입니다.

```typescript
interface CategorySectionProps {
  category: string;
  products: Product[];
  isExpanded: boolean;
  currentProductId?: string;
  onToggle: () => void;
}
```

**주요 기능**:
- 카테고리 헤더 표시 (아마존 스타일)
- 제품 목록 접기/펼치기 애니메이션
- 제품 개수 표시

### 4. ProductItem Component
**파일**: `frontend/components/ProductItem.tsx`

개별 제품 항목을 표시하는 컴포넌트입니다.

```typescript
interface ProductItemProps {
  product: Product;
  isActive: boolean;
}
```

**주요 기능**:
- 제품명과 가격 표시
- 활성 상태 스타일링
- 호버 효과

## Data Models

### Product Interface (확장)
기존 제품 모델을 사이드바용으로 확장합니다.

```typescript
interface SidebarProduct {
  id: string;
  name: string;
  category: string;
  price: number;
  emoji: string;
}
```

### Category Interface
카테고리 그룹 관리를 위한 인터페이스입니다.

```typescript
interface CategoryState {
  [categoryName: string]: {
    isExpanded: boolean;
    productCount: number;
  };
}
```

## Design System (Amazon Style)

### Color Palette
아마존의 색상 체계를 모방합니다.

```css
:root {
  --amazon-orange: #ff9900;
  --amazon-blue: #232f3e;
  --amazon-light-blue: #37475a;
  --amazon-gray: #eaeded;
  --amazon-dark-gray: #565959;
  --amazon-white: #ffffff;
  --amazon-hover: #f3f3f3;
}
```

### Typography
아마존과 유사한 폰트 스타일을 적용합니다.

```css
.sidebar-title {
  font-size: 14px;
  font-weight: 700;
  color: var(--amazon-blue);
  line-height: 20px;
}

.category-header {
  font-size: 16px;
  font-weight: 700;
  color: var(--amazon-blue);
  line-height: 24px;
}

.product-name {
  font-size: 13px;
  font-weight: 400;
  color: var(--amazon-blue);
  line-height: 19px;
}

.product-price {
  font-size: 12px;
  font-weight: 700;
  color: #b12704;
}
```

### Layout Specifications
- 사이드바 너비: 280px (데스크톱)
- 사이드바 배경: #ffffff
- 테두리: 1px solid #ddd
- 패딩: 16px
- 카테고리 간격: 24px
- 제품 항목 높이: 40px

## Error Handling

### 데이터 로딩 실패
- 제품 데이터 로딩 실패 시 기본 메시지 표시
- 네트워크 오류 시 재시도 버튼 제공

### 빈 카테고리 처리
- 제품이 없는 카테고리는 숨김 처리
- 모든 카테고리가 비어있을 경우 안내 메시지 표시

### 잘못된 제품 ID
- 존재하지 않는 제품 ID의 경우 활성 상태 표시하지 않음
- 콘솔에 경고 메시지 출력

## Testing Strategy

### Unit Tests
- 각 컴포넌트의 렌더링 테스트
- 카테고리 접기/펼치기 기능 테스트
- 제품 클릭 네비게이션 테스트

### Integration Tests
- 전체 레이아웃 렌더링 테스트
- 제품 데이터와 사이드바 연동 테스트
- 반응형 레이아웃 테스트

### Visual Tests
- 아마존 스타일 일치성 확인
- 다양한 화면 크기에서의 표시 확인
- 호버 및 활성 상태 스타일 확인

## Implementation Notes

### Tailwind CSS Classes
아마존 스타일을 구현하기 위한 주요 Tailwind 클래스들:

```css
/* 사이드바 컨테이너 */
.sidebar-container {
  @apply w-70 bg-white border-r border-gray-200 h-screen overflow-y-auto;
}

/* 카테고리 헤더 */
.category-header {
  @apply text-sm font-bold text-gray-900 py-2 px-3 hover:bg-gray-50 cursor-pointer;
}

/* 제품 항목 */
.product-item {
  @apply text-xs text-gray-900 py-2 px-6 hover:bg-gray-50 cursor-pointer border-l-2 border-transparent;
}

/* 활성 제품 */
.product-item-active {
  @apply border-l-orange-400 bg-orange-50 text-orange-900;
}
```

### State Management
- React의 `useState`를 사용하여 카테고리 접기/펼치기 상태 관리
- 로컬 스토리지를 활용하여 사용자의 카테고리 선호도 저장 (선택사항)

### Performance Considerations
- 제품 목록이 많을 경우를 대비한 가상화 고려 (현재는 샘플 데이터로 불필요)
- 카테고리 접기/펼치기 애니메이션 최적화