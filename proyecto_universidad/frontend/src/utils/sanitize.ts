export const sanitizeText = (value: string): string => {
  return value
    .replace(/<[^>]*>/g, '')
    .replace(/\s+/g, ' ')
    .trim();
};

export const sanitizeForm = <T extends Record<string, unknown>>(values: T): T => {
  const cleaned = { ...values } as Record<string, unknown>;

  Object.keys(cleaned).forEach((key) => {
    const value = cleaned[key];
    if (typeof value === 'string') {
      cleaned[key] = sanitizeText(value);
    }
  });

  return cleaned as T;
};
