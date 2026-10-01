import axios from 'axios';

const UNSAFE_DETAIL = /traceback|sqlalchemy|password_hash|exception|stack/i;

const isRecord = (value: unknown): value is Record<string, unknown> =>
  typeof value === 'object' && value !== null;

const readDetail = (data: unknown): string | null => {
  if (!isRecord(data)) {
    return null;
  }

  const detail = data.detail;

  if (typeof detail === 'string') {
    if (detail.length > 300 || UNSAFE_DETAIL.test(detail)) {
      return null;
    }
    return detail;
  }

  if (!Array.isArray(detail)) {
    return null;
  }

  const messages = detail
    .map((issue) => {
      if (!isRecord(issue) || typeof issue.msg !== 'string') {
        return '';
      }
      return issue.msg.replace(/^Value error,\s*/i, '').trim();
    })
    .filter((message) => message.length > 0 && message.length <= 240 && !UNSAFE_DETAIL.test(message));

  return messages.length > 0 ? messages.join('. ') : null;
};

export const toUserMessage = (error: unknown, fallback = 'No se pudo completar la operación.'): string => {
  if (error instanceof Error && error.name === 'ContractError') {
    return 'La respuesta del servidor no se pudo interpretar.';
  }

  if (!axios.isAxiosError(error)) {
    return fallback;
  }

  if (!error.response) {
    return 'No hay conexión con el servidor.';
  }

  const status = error.response.status;
  const detail = readDetail(error.response.data);

  if (status >= 500) {
    return 'El servicio no está disponible en este momento. Inténtalo de nuevo más tarde.';
  }

  if (detail) {
    return detail;
  }

  if (status === 401) {
    return 'Tu sesión no es válida. Vuelve a iniciar sesión.';
  }

  if (status === 404) {
    return 'No se encontró el registro solicitado.';
  }

  if (status === 409) {
    return 'El registro entra en conflicto con uno existente.';
  }

  return fallback;
};
