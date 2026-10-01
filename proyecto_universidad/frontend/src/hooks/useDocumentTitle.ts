import { useEffect } from 'react';

export const useDocumentTitle = (title: string): void => {
  useEffect(() => {
    const previous = document.title;
    document.title = `${title} · Universidad Digital`;
    return () => {
      document.title = previous;
    };
  }, [title]);
};
