# Implementation Plan

- [x] 1. Create backend data service layer
  - Implement ProductDataService class that loads and processes JSON product data
  - Add rating calculation logic that computes average ratings from review arrays
  - Create data validation and error handling for JSON file operations
  - _Requirements: 1.4, 3.1, 3.2, 3.4_

- [x] 2. Update backend API endpoints to use centralized data service
  - Modify existing product API endpoints to use ProductDataService
  - Ensure all endpoints return consistent product data with calculated ratings
  - Add proper error handling and logging for data service failures
  - _Requirements: 1.1, 1.2, 1.3, 3.1_

- [x] 3. Create reusable StarRating component
  - Implement StarRating React component with accurate half-star display logic
  - Add props for rating value, size, and review count display
  - Implement proper rounding to nearest 0.5 for visual representation
  - Add accessibility attributes and keyboard navigation support
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_

- [x] 4. Create frontend data service layer
  - Implement ProductApiService for centralized API communication
  - Add RatingCalculator utility for consistent rating calculations
  - Implement data caching mechanism for improved performance
  - Add error handling for API failures with user-friendly messages
  - _Requirements: 3.1, 3.3, 1.4_

- [x] 5. Update home page to use centralized data and StarRating component
  - Modify index.tsx to fetch product data from API instead of hardcoded data
  - Replace hardcoded star ratings with StarRating component
  - Ensure rating and review count data comes from actual product reviews
  - Add loading states and error handling for data fetching
  - _Requirements: 1.1, 1.2, 2.1, 2.2, 2.3, 4.1_

- [x] 6. Update ProductDetail component to use StarRating component
  - Replace existing star rating display with new StarRating component
  - Ensure rating calculation uses the same logic as other components
  - Verify that rating and review count are consistent with home page display
  - _Requirements: 1.1, 1.2, 2.1, 2.2, 2.3_

- [x] 7. Update sidebar components to use centralized data
  - Modify productUtils.ts to fetch data from API instead of hardcoded arrays
  - Update Sidebar and ProductItem components to display consistent ratings
  - Add StarRating component to sidebar product items if ratings should be shown
  - Ensure all sidebar data comes from the same source as other components
  - _Requirements: 1.1, 1.2, 3.1, 4.1_

- [x] 8. Add comprehensive unit tests for rating functionality
  - Create tests for StarRating component with various rating values (3.5, 4.0, 4.7, etc.)
  - Test RatingCalculator utility for accurate average calculations
  - Test ProductDataService for proper JSON data loading and processing
  - Add tests for edge cases like products with no reviews
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_

- [x] 9. Add integration tests for data consistency
  - Create tests that verify same product shows identical data across all views
  - Test API endpoints return consistent data structure
  - Verify rating calculations are identical between frontend and backend
  - Test error handling scenarios for missing or corrupted data
  - _Requirements: 1.1, 1.2, 1.3, 4.1, 4.2, 4.3, 4.4_

- [x] 10. Update product data models and types
  - Enhance TypeScript interfaces to include calculated rating fields
  - Add RatingDistribution interface for rating breakdown statistics
  - Update existing components to use enhanced product models
  - Ensure type safety across all data transformations
  - _Requirements: 3.3, 3.5_