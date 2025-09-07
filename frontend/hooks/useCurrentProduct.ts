import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';

export const useCurrentProduct = () => {
  const router = useRouter();
  const [currentProductId, setCurrentProductId] = useState<string | undefined>();

  useEffect(() => {
    try {
      // URL에서 제품 ID 추출
      const { id } = router.query;
      
      if (typeof id === 'string' && id.trim()) {
        setCurrentProductId(id);
      } else {
        setCurrentProductId(undefined);
      }
    } catch (error) {
      console.warn('제품 ID 추출 중 오류:', error);
      setCurrentProductId(undefined);
    }
  }, [router.query]);

  return currentProductId;
};