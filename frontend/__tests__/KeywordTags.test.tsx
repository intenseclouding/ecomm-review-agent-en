import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import KeywordTags from '../components/KeywordTags';

describe('KeywordTags Component', () => {
  const mockKeywords = ['음질', '배터리', '디자인', '가격'];
  
  test('키워드가 없을 때 아무것도 렌더링하지 않음', () => {
    const { container } = render(<KeywordTags keywords={[]} />);
    expect(container.firstChild).toBeNull();
  });
  
  test('키워드들이 올바르게 렌더링됨', () => {
    render(<KeywordTags keywords={mockKeywords} />);
    
    mockKeywords.forEach(keyword => {
      expect(screen.getByText(keyword)).toBeInTheDocument();
    });
  });
  
  test('키워드 클릭 시 onKeywordClick 콜백이 호출됨', () => {
    const mockOnClick = jest.fn();
    render(<KeywordTags keywords={mockKeywords} onKeywordClick={mockOnClick} />);
    
    const firstKeyword = screen.getByText(mockKeywords[0]);
    fireEvent.click(firstKeyword);
    
    expect(mockOnClick).toHaveBeenCalledWith(mockKeywords[0]);
  });
  
  test('onKeywordClick이 없을 때 클릭해도 에러가 발생하지 않음', () => {
    render(<KeywordTags keywords={mockKeywords} />);
    
    const firstKeyword = screen.getByText(mockKeywords[0]);
    expect(() => fireEvent.click(firstKeyword)).not.toThrow();
  });
  
  test('커스텀 className이 적용됨', () => {
    const customClass = 'custom-test-class';
    const { container } = render(
      <KeywordTags keywords={mockKeywords} className={customClass} />
    );
    
    expect(container.firstChild).toHaveClass(customClass);
  });
  
  test('각 키워드에 # 접두사가 표시됨', () => {
    render(<KeywordTags keywords={['테스트']} />);
    
    expect(screen.getByText('#')).toBeInTheDocument();
    expect(screen.getByText('테스트')).toBeInTheDocument();
  });
  
  test('호버 스타일이 onKeywordClick이 있을 때만 적용됨', () => {
    const mockOnClick = jest.fn();
    const { rerender } = render(<KeywordTags keywords={['테스트']} />);
    
    let keywordElement = screen.getByText('테스트').closest('span');
    expect(keywordElement).not.toHaveClass('cursor-pointer');
    
    rerender(<KeywordTags keywords={['테스트']} onKeywordClick={mockOnClick} />);
    
    keywordElement = screen.getByText('테스트').closest('span');
    expect(keywordElement).toHaveClass('cursor-pointer');
  });
});