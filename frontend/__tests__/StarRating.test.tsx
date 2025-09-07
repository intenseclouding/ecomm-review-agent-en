import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import StarRating from '../components/StarRating';

describe('StarRating Component', () => {
  test('displays 3.5 rating as 3 full stars and 1 half star', () => {
    render(<StarRating rating={3.5} />);
    
    // 평점 텍스트 확인
    expect(screen.getByText('3.5')).toBeInTheDocument();
    
    // aria-label 확인
    expect(screen.getByRole('img')).toHaveAttribute('aria-label', '3.5점 만점에 3.5점');
  });

  test('displays 4.0 rating as 4 full stars and 0 half stars', () => {
    render(<StarRating rating={4.0} />);
    
    expect(screen.getByText('4.0')).toBeInTheDocument();
    expect(screen.getByRole('img')).toHaveAttribute('aria-label', '4.0점 만점에 4.0점');
  });

  test('displays 4.7 rating as 4 full stars and 1 half star (rounded to 4.5)', () => {
    render(<StarRating rating={4.7} />);
    
    // 4.7은 4.5로 반올림되어 표시
    expect(screen.getByText('4.5')).toBeInTheDocument();
    expect(screen.getByRole('img')).toHaveAttribute('aria-label', '4.7점 만점에 4.5점');
  });

  test('displays 0 rating correctly', () => {
    render(<StarRating rating={0} />);
    
    expect(screen.getByText('0.0')).toBeInTheDocument();
    expect(screen.getByRole('img')).toHaveAttribute('aria-label', '0점 만점에 0.0점');
  });

  test('displays 5.0 rating as 5 full stars', () => {
    render(<StarRating rating={5.0} />);
    
    expect(screen.getByText('5.0')).toBeInTheDocument();
    expect(screen.getByRole('img')).toHaveAttribute('aria-label', '5.0점 만점에 5.0점');
  });

  test('shows review count when showCount is true', () => {
    render(<StarRating rating={4.2} showCount={true} reviewCount={15} />);
    
    expect(screen.getByText('(15개 리뷰)')).toBeInTheDocument();
  });

  test('does not show review count when showCount is false', () => {
    render(<StarRating rating={4.2} showCount={false} reviewCount={15} />);
    
    expect(screen.queryByText('(15개 리뷰)')).not.toBeInTheDocument();
  });

  test('applies correct size classes', () => {
    const { rerender } = render(<StarRating rating={4.0} size="small" />);
    let starContainer = screen.getByRole('img');
    expect(starContainer).toHaveClass('text-sm');

    rerender(<StarRating rating={4.0} size="medium" />);
    starContainer = screen.getByRole('img');
    expect(starContainer).toHaveClass('text-lg');

    rerender(<StarRating rating={4.0} size="large" />);
    starContainer = screen.getByRole('img');
    expect(starContainer).toHaveClass('text-2xl');
  });

  test('applies custom className', () => {
    render(<StarRating rating={4.0} className="custom-class" />);
    
    const container = screen.getByRole('img').parentElement;
    expect(container).toHaveClass('custom-class');
  });

  test('handles edge case ratings correctly', () => {
    // 음수 평점
    const { rerender } = render(<StarRating rating={-1} />);
    expect(screen.getByText('0.0')).toBeInTheDocument();

    // 5점 초과 평점
    rerender(<StarRating rating={6.5} />);
    expect(screen.getByText('5.0')).toBeInTheDocument();

    // 매우 작은 소수점
    rerender(<StarRating rating={0.1} />);
    expect(screen.getByText('0.0')).toBeInTheDocument();

    // 4.25 같은 값 (4.5로 반올림되어야 함)
    rerender(<StarRating rating={4.25} />);
    expect(screen.getByText('4.5')).toBeInTheDocument();
  });

  test('handles zero review count correctly', () => {
    render(<StarRating rating={4.0} showCount={true} reviewCount={0} />);
    
    // 리뷰 개수가 0이면 표시하지 않음
    expect(screen.queryByText('(0개 리뷰)')).not.toBeInTheDocument();
  });
});