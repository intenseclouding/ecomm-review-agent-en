import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import SentimentIndicator from '../components/SentimentIndicator';

describe('SentimentIndicator Component', () => {
  const mockPositiveSentiment = {
    label: '긍정',
    confidence: 0.85,
    polarity: 0.7
  };
  
  const mockNegativeSentiment = {
    label: '부정',
    confidence: 0.92,
    polarity: -0.6
  };
  
  const mockNeutralSentiment = {
    label: '중립',
    confidence: 0.65,
    polarity: 0.1
  };
  
  test('감정 데이터가 없을 때 아무것도 렌더링하지 않음', () => {
    const { container } = render(<SentimentIndicator sentiment={null as any} />);
    expect(container.firstChild).toBeNull();
  });
  
  test('긍정적 감정이 올바르게 렌더링됨', () => {
    render(<SentimentIndicator sentiment={mockPositiveSentiment} />);
    
    expect(screen.getByText('긍정')).toBeInTheDocument();
    expect(screen.getByText('😊')).toBeInTheDocument();
    expect(screen.getByText('(85%)')).toBeInTheDocument();
  });
  
  test('부정적 감정이 올바르게 렌더링됨', () => {
    render(<SentimentIndicator sentiment={mockNegativeSentiment} />);
    
    expect(screen.getByText('부정')).toBeInTheDocument();
    expect(screen.getByText('😞')).toBeInTheDocument();
    expect(screen.getByText('(92%)')).toBeInTheDocument();
  });
  
  test('중립적 감정이 올바르게 렌더링됨', () => {
    render(<SentimentIndicator sentiment={mockNeutralSentiment} />);
    
    expect(screen.getByText('중립')).toBeInTheDocument();
    expect(screen.getByText('😐')).toBeInTheDocument();
    expect(screen.getByText('(65%)')).toBeInTheDocument();
  });
  
  test('신뢰도 표시를 숨길 수 있음', () => {
    render(
      <SentimentIndicator 
        sentiment={mockPositiveSentiment} 
        showConfidence={false} 
      />
    );
    
    expect(screen.getByText('긍정')).toBeInTheDocument();
    expect(screen.queryByText('(85%)')).not.toBeInTheDocument();
  });
  
  test('다양한 크기가 적용됨', () => {
    const { rerender } = render(
      <SentimentIndicator sentiment={mockPositiveSentiment} size="sm" />
    );
    
    let container = screen.getByText('긍정').closest('div');
    expect(container).toHaveClass('text-xs', 'px-2', 'py-1');
    
    rerender(<SentimentIndicator sentiment={mockPositiveSentiment} size="lg" />);
    
    container = screen.getByText('긍정').closest('div');
    expect(container).toHaveClass('text-sm', 'px-3', 'py-2');
  });
  
  test('긍정적 감정에 올바른 색상 클래스가 적용됨', () => {
    render(<SentimentIndicator sentiment={mockPositiveSentiment} />);
    
    const container = screen.getByText('긍정').closest('div');
    expect(container).toHaveClass('bg-green-100', 'text-green-800', 'border-green-200');
  });
  
  test('부정적 감정에 올바른 색상 클래스가 적용됨', () => {
    render(<SentimentIndicator sentiment={mockNegativeSentiment} />);
    
    const container = screen.getByText('부정').closest('div');
    expect(container).toHaveClass('bg-red-100', 'text-red-800', 'border-red-200');
  });
  
  test('중립적 감정에 올바른 색상 클래스가 적용됨', () => {
    render(<SentimentIndicator sentiment={mockNeutralSentiment} />);
    
    const container = screen.getByText('중립').closest('div');
    expect(container).toHaveClass('bg-gray-100', 'text-gray-800', 'border-gray-200');
  });
  
  test('커스텀 className이 적용됨', () => {
    const customClass = 'custom-sentiment-class';
    render(
      <SentimentIndicator 
        sentiment={mockPositiveSentiment} 
        className={customClass} 
      />
    );
    
    const container = screen.getByText('긍정').closest('div');
    expect(container).toHaveClass(customClass);
  });
  
  test('신뢰도가 올바르게 퍼센트로 변환됨', () => {
    const lowConfidenceSentiment = {
      label: '긍정',
      confidence: 0.123,
      polarity: 0.5
    };
    
    render(<SentimentIndicator sentiment={lowConfidenceSentiment} />);
    
    expect(screen.getByText('(12%)')).toBeInTheDocument();
  });
});