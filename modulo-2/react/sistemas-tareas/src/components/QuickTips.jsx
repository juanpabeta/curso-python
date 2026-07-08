const TIPS = [
  {
    id: 1,
    title: 'Prioriza lo urgente',
    description: 'Empieza por las tareas con fecha de entrega más cercana.',
  },
  {
    id: 2,
    title: 'Divide proyectos grandes',
    description: 'Convierte un proyecto extenso en pasos pequeños y manejables.',
  },
  {
    id: 3,
    title: 'Revisa al final del día',
    description: 'Dedica 5 minutos a actualizar tu lista antes de cerrar sesión.',
  },
  {
    id: 4,
    title: 'Evita la multitarea',
    description: 'Enfócate en una tarea a la vez para avanzar con mayor claridad.',
  },
];

function QuickTips() {
  return (
    <aside className="rounded-xl border border-slate-800 bg-slate-900/60 p-6 shadow-lg">
      <h3 className="mb-1 text-lg font-semibold text-slate-100">
        Consejos rápidos
      </h3>
      <p className="mb-5 text-sm text-slate-500">
        Pequeños hábitos que mejoran tu productividad.
      </p>

      <ul className="space-y-4">
        {TIPS.map((tip) => (
          <li
            key={tip.id}
            className="rounded-lg border border-slate-800/80 bg-slate-950/50 p-4 transition-colors hover:border-slate-700"
          >
            <p className="font-medium text-green-300">{tip.title}</p>
            <p className="mt-1 text-sm leading-relaxed text-stone-300">
              {tip.description}
            </p>
          </li>
        ))}
      </ul>
    </aside>
  );
}

export default QuickTips;
