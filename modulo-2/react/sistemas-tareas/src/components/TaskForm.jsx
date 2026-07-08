import { useState } from 'react';

// Desestructuramos la prop onAddTask directamente en la firma (Guía Airbnb)
const TaskForm = ({ onAddTask }) => {
  const [taskText, setTaskText] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Evitamos agregar tareas vacías
    if (taskText.trim() === '') return;

    // Llamamos a la función del padre y le pasamos el texto
    onAddTask(taskText.trim());
    
    // Limpiamos el input
    setTaskText('');
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="mb-8 flex w-full gap-3"
      aria-label="Formulario para agregar tareas"
    >
      <label htmlFor="task-input" className="sr-only">
        Nueva tarea
      </label>
      <input
        id="task-input"
        type="text"
        value={taskText}
        onChange={(e) => setTaskText(e.target.value)}
        placeholder="Ingresa una nueva tarea..."
        className="flex-1 px-4 py-3 bg-slate-800 text-cyan-50 border border-slate-700 rounded-md focus:outline-none focus:border-cyan-400 focus:ring-1 focus:ring-cyan-400 transition-all placeholder:text-slate-500"
        maxLength={120}
        required
      />
      <button
        type="submit"
        className="px-6 py-3 bg-fuchsia-600 text-white font-semibold rounded-md hover:bg-fuchsia-500 active:bg-fuchsia-700 transition-colors shadow-lg shadow-fuchsia-600/30 cursor-pointer"
      >
        Agregar
      </button>
    </form>
  );
};

export default TaskForm;