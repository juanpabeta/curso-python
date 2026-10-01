import { Outlet } from 'react-router-dom';

export const AuthLayout = () => {
  return (
    <main className="auth-shell">
      <div className="auth-panel">
        <Outlet />
      </div>
    </main>
  );
};
