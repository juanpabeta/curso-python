import { Link } from 'react-router-dom';

interface ServerErrorPageProps {
  onRetry?: () => void;
}

export const ServerErrorPage = ({ onRetry }: ServerErrorPageProps) => {
  return (
    <section className="message-page" aria-labelledby="server-error-title">
      <h1 id="server-error-title">Error del servidor</h1>
      <p>Ocurrió un problema inesperado. Los detalles internos no se muestran.</p>
      <div className="inline-actions">
        <button type="button" className="secondary-btn" onClick={onRetry ?? (() => window.location.reload())}>
          Reintentar
        </button>
        <Link to="/" className="primary-btn inline-link">
          Ir al inicio
        </Link>
      </div>
    </section>
  );
};
