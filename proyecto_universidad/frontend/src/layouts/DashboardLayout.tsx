import { NavLink, Outlet } from 'react-router-dom';
import { useAuth } from '@/hooks/useAuth';
import { NAV_ITEMS } from '@/routes/navigation';

export const DashboardLayout = () => {
  const { user, logout } = useAuth();
  const navItems = NAV_ITEMS.filter((item) => item.roles.some((role) => user?.roles.includes(role)));

  return (
    <div className="dashboard-shell">
      <a className="skip-link" href="#contenido-principal">
        Saltar al contenido
      </a>
      <aside className="sidebar" aria-label="Menú principal">
        <div className="brand-block">
          <h1>Universidad Digital</h1>
        </div>
        <nav aria-label="Secciones">
          <ul className="nav-list">
            {navItems.map((item) => (
              <li key={item.to}>
                <NavLink to={item.to} end={item.end} className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')}>
                  {item.label}
                </NavLink>
              </li>
            ))}
          </ul>
        </nav>
        <div className="user-card">
          <strong>{user?.full_name ?? 'Usuario'}</strong>
          <span>{user?.roles.join(', ') ?? 'Sin rol'}</span>
          <button type="button" onClick={() => void logout()} className="secondary-btn">
            Cerrar sesión
          </button>
        </div>
      </aside>

      <main id="contenido-principal" className="content-area" tabIndex={-1}>
        <Outlet />
      </main>
    </div>
  );
};
