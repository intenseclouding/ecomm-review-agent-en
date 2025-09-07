# Design Document

## Overview

기존 카테고리별 제품 사이드바에 "전체 목록 보기" 기능을 추가하여 사용자가 모든 제품을 한 번에 탐색할 수 있도록 합니다. 이 기능은 기존 아마존 스타일 디자인을 유지하면서 새로운 보기 모드를 제공합니다.

## Architecture

### Component Structure (Updated)
```
Sidebar
├── SidebarHeader
├── ViewModeToggle (NEW)
├── AllProductsList (NEW - conditional)
└── CategorySections (existing - conditional)
    ├── CategorySection
    │   └── ProductItem[]
```

### State Management
```typescript
interface SidebarState {
  viewMode: 'category' | 'all';
  categories: CategoryGroup[];
  allProducts: SidebarProduct[];
  currentProductId?: string;
}
```

### Data Flow
1. 사이드바 컴포넌트에서 보기 모드 상태 관리
2. 보기 모드에 따라 조건부 렌더링
3. 전체 목록 보기 시 모든 제품을 평면 배열로 표시
4. 카테고리별 보기 시 기존 그룹화된 구조 사용

## Components and Interfaces

### 1. Sidebar Component (Updated)
**파일**: `frontend/components/Sidebar.tsx`

기존 사이드바 컴포넌트에 보기 모드 상태를 추가합니다.

```typescript
interface SidebarProps {
  currentProductId?: string;
}

interface SidebarState {
  viewMode: 'category' | 'all';
  categories: CategoryGroup[];
  allProducts: SidebarProduct[];
}

type ViewMode = 'category' | 'all';
```

**주요 기능 추가**:
- 보기 모드 상태 관리 (`useState`)
- 전체 제품 목록 생성 및 정렬
- 조건부 렌더링 로직

### 2. ViewModeToggle Component (NEW)
**파일**: `frontend/components/ViewModeToggle.tsx`

보기 모드를 전환하는 새로운 컴포넌트입니다.

```typescript
interface ViewModeToggleProps {
  currentMode: ViewMode;
  onModeChange: (mode: ViewMode) => void;
}
```

**주요 기능**:
- "전체 목록 보기" 버튼
- 현재 활성 모드 표시
- 아마존 스타일 버튼 디자인

### 3. AllProductsList Component (NEW)
**파일**: `frontend/components/AllProductsList.tsx`

전체 제품 목록을 표시하는 새로운 컴포넌트입니다.

```typescript
interface AllProductsListProps {
  products: SidebarProduct[];
  currentProductId?: string;
}
```

**주요 기능**:
- 모든 제품을 평면 목록으로 표시
- 각 제품에 카테고리 태그 표시
- 현재 제품 하이라이트

### 4. ProductItemWithCategory Component (NEW)
**파일**: `frontend/components/ProductItemWithCategory.tsx`

카테고리 태그가 포함된 제품 항목 컴포넌트입니다.

```typescript
interface ProductItemWithCategoryProps {
  product: SidebarProduct;
  isActive: boolean;
  showCategory?: boolean;
}
```

**주요 기능**:
- 기존 ProductItem 기능 + 카테고리 태그
- 카테고리 태그 표시/숨김 옵션
- 일관된 스타일링

## Data Models

### ViewMode Type
```typescript
type ViewMode = 'category' | 'all';
```

### Enhanced SidebarProduct Interface
```typescript
interface SidebarProduct {
  id: string;
  name: string;
  category: string;
  price: number;
  emoji: string;
  categoryColor?: string; // 카테고리별 색상 구분용
}
```

### ViewModeState Interface
```typescript
interface ViewModeState {
  current: ViewMode;
  previousCategoryStates: { [key: string]: boolean }; // 카테고리 펼침 상태 저장
}
```

## Design System Updates

### ViewModeToggle Styling
아마존 스타일을 따르는 토글 버튼 디자인:

```css
.view-mode-toggle {
  @apply mb-4 px-3 py-2 border-b border-gray-200;
}

.view-mode-button {
  @apply w-full text-left px-3 py-2 text-sm font-medium rounded-md transition-colors;
  @apply hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-orange-500;
}

.view-mode-button-active {
  @apply bg-orange-50 text-orange-700 border-l-2 border-orange-400;
}

.view-mode-button-inactive {
  @apply text-gray-700 hover:text-gray-900;
}
```

### Category Tag Styling
전체 목록에서 카테고리를 표시하는 작은 태그:

```css
.category-tag {
  @apply inline-block px-2 py-1 text-xs font-medium rounded-full;
  @apply bg-gray-100 text-gray-600 ml-2;
}

.category-tag-electronics {
  @apply bg-blue-100 text-blue-700;
}

.category-tag-fashion {
  @apply bg-pink-100 text-pink-700;
}

.category-tag-cosmetics {
  @apply bg-yellow-100 text-yellow-700;
}
```

### All Products List Styling
```css
.all-products-list {
  @apply space-y-1;
}

.all-products-item {
  @apply flex items-center justify-between px-3 py-2 text-sm;
  @apply hover:bg-gray-50 cursor-pointer rounded-md transition-colors;
}

.all-products-item-active {
  @apply bg-orange-50 border-l-2 border-orange-400 text-orange-700;
}
```

## User Experience Flow

### 1. Default State (Category View)
- 사이드바는 기존과 동일하게 카테고리별로 표시
- 상단에 "전체 목록 보기" 버튼이 비활성 상태로 표시

### 2. Switching to All View
1. 사용자가 "전체 목록 보기" 클릭
2. 현재 카테고리 펼침 상태를 저장
3. 부드러운 전환 애니메이션과 함께 전체 목록 표시
4. "전체 목록 보기" 버튼이 활성 상태로 변경

### 3. All Products View
- 모든 제품이 이름순으로 정렬되어 표시
- 각 제품 옆에 작은 카테고리 태그 표시
- 현재 제품이 있다면 하이라이트 표시

### 4. Switching Back to Category View
1. 사용자가 특정 카테고리 클릭 또는 다른 방식으로 전환
2. 이전에 저장된 카테고리 펼침 상태 복원
3. 부드러운 전환 애니메이션과 함께 카테고리별 보기로 변경

## Implementation Strategy

### Phase 1: Core Functionality
1. ViewModeToggle 컴포넌트 생성
2. Sidebar 컴포넌트에 상태 관리 추가
3. 기본적인 전체 목록 표시 기능

### Phase 2: Enhanced UX
1. AllProductsList 컴포넌트 생성
2. 카테고리 태그 기능 추가
3. 전환 애니메이션 구현

### Phase 3: Polish & Optimization
1. 상태 저장/복원 기능
2. 접근성 개선
3. 성능 최적화

## Error Handling

### 빈 제품 목록
- 전체 목록이 비어있을 경우 적절한 메시지 표시
- 로딩 상태 처리

### 상태 전환 오류
- 보기 모드 전환 실패 시 이전 상태로 복원
- 사용자에게 오류 상황 알림

### 데이터 불일치
- 카테고리별 보기와 전체 보기 간 데이터 동기화
- 제품 데이터 변경 시 두 보기 모두 업데이트

## Testing Strategy

### Unit Tests
- ViewModeToggle 컴포넌트 렌더링 및 클릭 이벤트
- AllProductsList 컴포넌트 제품 목록 표시
- 보기 모드 상태 전환 로직

### Integration Tests
- 전체 사이드바에서 보기 모드 전환
- 현재 제품 하이라이트 기능
- 카테고리 상태 저장/복원

### User Experience Tests
- 보기 모드 전환의 직관성
- 전환 애니메이션의 자연스러움
- 다양한 화면 크기에서의 동작

## Performance Considerations

### 메모리 최적화
- 불필요한 리렌더링 방지를 위한 `useMemo` 활용
- 제품 목록 정렬 결과 캐싱

### 애니메이션 성능
- CSS 트랜지션 사용으로 부드러운 전환
- 레이아웃 변경 최소화

### 상태 관리 최적화
- 카테고리 상태를 로컬 스토리지에 저장 (선택사항)
- 불필요한 상태 업데이트 방지