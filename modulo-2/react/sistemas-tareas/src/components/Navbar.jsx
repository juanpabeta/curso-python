function Navbar() {
  return (
    <<header className="relative overflow-hidden bg-gradient-to-r from-indigo-600 via-violet-600 to-indigo-600 shadow-lg shadow-blue-500/20">
      <div
        className="pointer-events-none absolute inset-0 opacity-20"
        aria-hidden="true"
        style={{
          backgroundImage:
            'radial-gradient(circle at 10% 60%, white 2px, transparent 2px), radial-gradient(circle at 80% 20%, white 2px, transparent 2px)',
          backgroundSize: '60px 60px',
        }}
      />

      <nav
        className="relative mx-auto flex max-w-5xl flex-col items-center gap-2 px-4 py-6 sm:flex-row sm:justify-between sm:px-6 sm:py-7"
        aria-label="Navegación principal"
      >
        <div className="flex items-center gap-3">
          <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-white/20 text-white backdrop-blur-sm">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              className="h-5 w-5"
              aria-hidden="true"
            >
              <path d="M9 11l3 3L22 4" />
              <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11" />
            </svg>
          </span>
          <div>
            <h1 className="text-2xl font-bold tracking-tight text-white sm:text-3xl">
              Sistema de Tareas
            </h1>
            <p className="hidden text-sm text-indigo-200/80 sm:block">
              Tu espacio de productividad diaria
            </p>
          </div>
        </div>

        <p className="text-sm text-indigo-100/90 sm:text-right">
          {new Date().toLocaleDateString('es-ES', {
            weekday: 'long',
            day: 'numeric',
            month: 'long',
          })}
        </p>
      </nav>
    </header>
  );
}

export default Navbar;