import { Link } from 'react-router-dom';

export const UnauthorizedPage = () => {
  return (
    <section className="message-page">
      <h1>Acceso denegado</h1>
      <p>No tienes permisos suficientes para ver esta sección.</p>
      <Link to="/" className="primary-btn inline-link">
        Volver al inicio
      </Link>
    </section>
  );
};
