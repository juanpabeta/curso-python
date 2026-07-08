import PropTypes from 'prop-types';

const STATS = [
  {
    id: 'total',
    label: 'Total de tareas',
    color: 'text-purple-400',
    bar: 'bg-purple-500',
    bg: 'bg-purple-500/10',
    getValue: (total) => total,
  },
  {
    id: 'pending',
    label: 'Pendientes',
    color: 'text-fuchsia-400',
    bar: 'bg-fuchsia-500',
    bg: 'bg-fuchsia-500/10',
    getValue: (total) => total,
  },
  {
    id: 'completed',
    label: 'Completadas',
    color: 'text-emerald-400',
    bar: 'bg-emerald-500',
    bg: 'bg-emerald-500/10',
    getValue: () => 0,
  },
];

function StatsPanel({ taskCount }) {
  return (
    <section
      aria-label="Resumen de tareas"
      className="mx-auto mb-10 grid w-full max-w-5xl grid-cols-1 gap-4 sm:grid-cols-3"
    >
      {STATS.map((stat) => (
        <article
          key={stat.id}
          className={`rounded-xl border border-slate-800 p-5 shadow-lg backdrop-blur-sm ${stat.bg}`}
        >
          <p className="text-sm font-medium text-slate-400">{stat.label}</p>
          <p className={`mt-2 text-3xl font-bold ${stat.color}`}>
            {stat.getValue(taskCount)}
          </p>
          <div className={`mt-3 h-1 w-12 rounded-full ${stat.bar}`} />
        </article>
      ))}
    </section>
  );
}

StatsPanel.propTypes = {
  taskCount: PropTypes.number.isRequired,
};

export default StatsPanel;
