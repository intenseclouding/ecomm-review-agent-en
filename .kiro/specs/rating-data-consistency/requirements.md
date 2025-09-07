# Requirements Document

## Introduction

This feature addresses inconsistencies in star rating display and data synchronization between different views in the product review system. Currently, the home/list view and product detail pages show different star ratings and review counts, and the star display doesn't properly handle half-star ratings. The solution will centralize data management through JSON files as a stepping stone toward future DynamoDB integration.

## Requirements

### Requirement 1

**User Story:** As a user browsing products, I want to see consistent star ratings and review counts across all views, so that I can trust the information displayed.

#### Acceptance Criteria

1. WHEN a user views a product on the home page THEN the system SHALL display the same star rating as shown on the product detail page
2. WHEN a user views a product on the home page THEN the system SHALL display the same review count as shown on the product detail page
3. WHEN product data is updated THEN all views SHALL reflect the updated information consistently
4. WHEN the system calculates ratings THEN it SHALL use a single source of truth from JSON data files

### Requirement 2

**User Story:** As a user viewing product ratings, I want to see accurate visual representation of star ratings including half stars, so that I can quickly assess product quality.

#### Acceptance Criteria

1. WHEN a product has a rating of 3.5 stars THEN the system SHALL display 3 full stars and 1 half star
2. WHEN a product has a rating of 4.5 stars THEN the system SHALL display 4 full stars and 1 half star
3. WHEN a product has a rating of 4.0 stars THEN the system SHALL display 4 full stars and 0 half stars
4. WHEN a product has a rating with decimal values THEN the system SHALL round to the nearest 0.5 for display purposes
5. WHEN displaying star ratings THEN the system SHALL never show more filled stars than the actual rating value

### Requirement 3

**User Story:** As a developer preparing for DynamoDB integration, I want a centralized data access layer that uses JSON files as mock data, so that future database migration will be seamless.

#### Acceptance Criteria

1. WHEN the frontend requests product data THEN the system SHALL retrieve it from a centralized data service
2. WHEN the backend serves product data THEN it SHALL read from JSON files that simulate database structure
3. WHEN product data is accessed THEN the system SHALL use consistent data models across all components
4. WHEN implementing data access THEN the system SHALL use an abstraction layer that can be easily replaced with DynamoDB calls
5. WHEN JSON data structure is defined THEN it SHALL include all necessary fields for ratings, reviews, and product information

### Requirement 4

**User Story:** As a user viewing product reviews, I want to see the same reviews and review analytics on both the home page preview and detail page, so that the information is consistent and reliable.

#### Acceptance Criteria

1. WHEN a user views review previews on the home page THEN the system SHALL show reviews from the same dataset as the detail page
2. WHEN review analytics are displayed THEN they SHALL be calculated from the same review data across all views
3. WHEN new reviews are added THEN they SHALL appear consistently across all views that display reviews
4. WHEN review sentiment analysis is shown THEN it SHALL be based on the same review dataset regardless of the view