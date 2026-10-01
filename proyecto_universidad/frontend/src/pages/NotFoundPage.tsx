import { Link } from 'react-router-dom';

export const NotFoundPage = () => {
  return (
    <section className="message-page">
      <h1>404</h1>
      <p>La página solicitada no existe.</p>
      <Link to="/" className="primary-btn inline-link">
        Ir al inicio
      </Link>
    </section>
  );
};
