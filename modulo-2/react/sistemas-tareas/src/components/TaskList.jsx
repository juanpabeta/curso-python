import PropTypes from 'prop-types';

const TaskList = ({ tasks }) => {
  if (!tasks || tasks.length === 0) {
    return (
      <div className="rounded-xl border border-dashed border-slate-700 bg-slate-900/40 px-6 py-10 text-center">
        <p className="font-medium text-slate-300">No hay tareas pendientes</p>
        <p className="mt-2 text-sm text-slate-500">
          Usa el formulario de arriba para agregar tu primera tarea.
        </p>
      </div>
    );
  }

  return (
    <section aria-label="Lista de tareas">
      <header className="mb-4 flex items-center justify-between">
        <h3 className="text-lg font-semibold text-slate-100">
          Tareas pendientes
        </h3>
        <span className="rounded-full bg-slate-800 px-3 py-1 text-xs font-medium text-cyan-400">
          {tasks.length} {tasks.length === 1 ? 'tarea' : 'tareas'}
        </span>
      </header>

      <ul className="space-y-3">
        {tasks.map((task, index) => (
          <li
            key={task.id}
            className="flex items-center gap-4 rounded-md border border-slate-800 bg-slate-800 p-4 shadow-md transition-colors hover:border-slate-700 hover:bg-slate-800/80"
          >
            <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-md bg-cyan-500/20 text-sm font-bold text-cyan-400">
              {index + 1}
            </span>
            <span className="flex-1 border-l-4 border-cyan-500 pl-4 font-medium tracking-wide text-slate-200">
              {task.title}
            </span>
          </li>
        ))}
      </ul>
    </section>
  );
};

TaskList.propTypes = {
  tasks: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.oneOfType([PropTypes.number, PropTypes.string]).isRequired,
      title: PropTypes.string.isRequired,
    }),
  ).isRequired,
};

export default TaskList;
