function HeroBanner() {
  return (
    <section className="mx-auto mb-10 max-w-4xl text-center">
      <p className="mb-3 inline-block rounded-full border border-cyan-500/30 bg-cyan-500/10 px-4 py-1 text-xs font-semibold uppercase tracking-widest text-cyan-400">
        Organiza tu semana
      </p>
      <h2 className="text-3xl font-bold tracking-wide text-slate-100 sm:text-4xl">
        Panel de Control
      </h2>
      <p className="mx-auto mt-4 max-w-2xl text-base leading-relaxed text-slate-400 sm:text-lg">
        Centraliza tus pendientes académicos y personales en un solo lugar.
        Agrega tareas, revisa tu progreso y mantén el foco en lo importante.
      </p>
    </section>
  );
}

export default HeroBanner;
