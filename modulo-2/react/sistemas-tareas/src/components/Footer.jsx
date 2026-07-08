function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="mt-16 border-t border-slate-800 bg-slate-900/50">
      <div className="container mx-auto flex flex-col items-center gap-4 px-4 py-8 text-center sm:flex-row sm:justify-between sm:text-left">
        <div>
          <p className="font-semibold text-slate-200">Sistema de Tareas</p>
          <p className="mt-1 text-sm text-slate-500">
            Pagina web para la gestion de tareas
          </p>
        </div>

        <div className="flex flex-wrap justify-center gap-4 text-sm text-slate-500">
          <span>Tareas</span>
          <span aria-hidden="true">·</span>
          <span>Gestion de tareas</span>
          <span aria-hidden="true">·</span>
          <span>Consejos</span>
        </div>

        <p className="text-sm text-slate-600">
          © {currentYear} Todos los derechos reservados
        </p>
      </div>
    </footer>
  );
}

export default Footer;
