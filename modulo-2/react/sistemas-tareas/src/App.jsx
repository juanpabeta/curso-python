import { useRef, useState } from 'react';
import Navbar from './components/Navbar';
import HeroBanner from './components/HeroBanner';
import StatsPanel from './components/StatsPanel';
import TaskForm from './components/TaskForm';
import TaskList from './components/TaskList';
import QuickTips from './components/QuickTips';
import Footer from './components/Footer';

const INITIAL_TASKS = [
  { id: 1, title: 'Configurar gemelo digital del sensor de temperatura' },
  { id: 2, title: 'Documentar arquitectura del sistema IoT' },
  { id: 3, title: 'Validar dashboard de monitoreo en tiempo real' },
  { id: 4, title: 'Revisar alertas automáticas del panel' },
  { id: 5, title: 'Preparar demo de Digital Twins Lab' },
];

const App = () => {
  const pageRef = useRef(null);
  const [tasks, setTasks] = useState(INITIAL_TASKS);

  const handleAddTask = (newTaskTitle) => {
    const newTask = {
      id: crypto.randomUUID(),
      title: newTaskTitle,
    };

    setTasks((prevTasks) => [...prevTasks, newTask]);
  };

  return (
    <div className="min-h-screen bg-slate-950 font-sans selection:bg-cyan-500 selection:text-slate-900">
      <div ref={pageRef}>
        <Navbar />

        <main className="container mx-auto px-4 pb-12 pt-10">
          <HeroBanner />
          <StatsPanel taskCount={tasks.length} />

          <div className="mx-auto grid max-w-5xl grid-cols-1 gap-8 lg:grid-cols-3">
            <section className="rounded-xl border border-slate-800 bg-slate-900/40 p-6 shadow-xl lg:col-span-2">
              <header className="mb-6">
                <h3 className="text-xl font-semibold text-slate-100">
                  Gestión de tareas
                </h3>
                <p className="mt-1 text-sm text-slate-500">
                  Escribe una tarea y presiona Agregar para incluirla en tu lista.
                </p>
              </header>

              <TaskForm onAddTask={handleAddTask} />
              <TaskList tasks={tasks} />
            </section>

            <QuickTips />
          </div>
        </main>

        <Footer />
      </div>

     
    </div>
  );
};

export default App;
