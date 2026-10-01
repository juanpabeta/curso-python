export class ContractError extends Error {
  constructor() {
    super('La respuesta del servidor no cumple el contrato esperado.');
    this.name = 'ContractError';
  }
}

export const asRecord = (value: unknown): Record<string, unknown> => {
  if (typeof value !== 'object' || value === null) {
    throw new ContractError();
  }
  return value as Record<string, unknown>;
};

export const asArray = (value: unknown): unknown[] => {
  if (!Array.isArray(value)) {
    throw new ContractError();
  }
  return value;
};

export const asString = (record: Record<string, unknown>, key: string): string => {
  const value = record[key];
  if (typeof value !== 'string') {
    throw new ContractError();
  }
  return value;
};

export const asNumber = (record: Record<string, unknown>, key: string): number => {
  const value = record[key];
  if (typeof value !== 'number' || Number.isNaN(value)) {
    throw new ContractError();
  }
  return value;
};

export const asBoolean = (record: Record<string, unknown>, key: string): boolean => {
  const value = record[key];
  if (typeof value !== 'boolean') {
    throw new ContractError();
  }
  return value;
};

export const asOptionalString = (record: Record<string, unknown>, key: string): string | null => {
  if (!(key in record) || record[key] === null || record[key] === undefined) {
    return null;
  }
  if (typeof record[key] !== 'string') {
    throw new ContractError();
  }
  return record[key];
};
