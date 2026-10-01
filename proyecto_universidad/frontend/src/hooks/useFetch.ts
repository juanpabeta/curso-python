import { useCallback, useEffect, useRef, useState } from 'react';
import { toUserMessage } from '@/utils/errors';

interface UseFetchResult<T> {
  data: T | null;
  error: string;
  isLoading: boolean;
  reload: () => Promise<void>;
}

export const useFetch = <T>(loader: () => Promise<T>): UseFetchResult<T> => {
  const [data, setData] = useState<T | null>(null);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const loaderRef = useRef(loader);
  const requestId = useRef(0);

  loaderRef.current = loader;

  const reload = useCallback(async () => {
    const current = requestId.current + 1;
    requestId.current = current;
    setIsLoading(true);

    try {
      const result = await loaderRef.current();
      if (requestId.current !== current) {
        return;
      }
      setData(result);
      setError('');
    } catch (caught) {
      if (requestId.current !== current) {
        return;
      }
      setError(toUserMessage(caught));
    } finally {
      if (requestId.current === current) {
        setIsLoading(false);
      }
    }
  }, []);

  useEffect(() => {
    void reload();
  }, [reload]);

  return { data, error, isLoading: isLoading && data === null, reload };
};
