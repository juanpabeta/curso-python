import { useNavigate, Link } from "react-router-dom";
import useTasks from "../hooks/useTasks.js";
import { api } from "../api/client.js";

export default function TasksList() {
  const { tasks, loading, error, reload } = useTasks();
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  const handleDelete = async (id) => {
    if (window.confirm("¿Seguro que deseas eliminar esta tarea?")) {
      try {
        await api.delete(`/tasks/${id}`);
        reload();
      } catch (err) {
        alert("Ocurrió un error al eliminar la tarea.");
      }
    }
  };

  const getStatusBadge = (status) => {
    switch(status) {
      case "Pendiente": return "bg-red-300 text-red-800";
      case "En progreso": return "bg-blue-300 text-blue-800";
      case "Completada": return "bg-green-300 text-green-800";
      default: return "bg-gray-300 text-gray-800";
    }
  };

  const getPriorityBadge = (priority) => {
    switch(priority) {
      case "Alta": return "bg-red-300 text-red-800";
      case "Media": return "bg-orange-400 text-orange-900";
      case "Baja": return "bg-gray-300 text-gray-800";
      default: return "bg-gray-300 text-gray-800";
    }
  };

  if (loading) return <div className="p-12 text-center text-lg text-red-600 font-medium bg-slate-950
  ">Cargando tareas...</div>;
  if (error) return <div className="p-8 text-center text-red-600 font-medium bg-slate-950">{error}</div>;

  return (
    <div className="min-h-screen bg-slate-950 p-4 md:p-8">
      <div className="max-w-6xl mx-auto">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-8 gap-4">
          <h1 className="text-3xl font-bold text-purple-800/95">Panel de tareas</h1>
          <div className="flex gap-5">
            <button 
              onClick={() => navigate("/tasks/new")} 
              className="bg-sky-600 
              border border-white text-white font-medium px-5 py-2.5 rounded hover:bg-sky-700 transition"
            >
              Nueva tarea
            </button>
            <button 
              onClick={handleLogout} 
              className="bg-fuchsia-600 border border-white text-white font-medium px-5 py-2.5 rounded hover:bg-fuchsia-700 transition"
            >
              Cerrar sesión
            </button>
          </div>
        </div>

        {tasks.length === 0 ? (
          <div className="text-center bg-slate-950 p-12 rounded-lg shadow-sm border  border-gray-200">
            <p className="text-gray-500 mb-2">No hay tareas actualmente.</p>
            <Link to="/tasks/new" className="text-green-600 font-medium hover:underline text-lg">
              Necesitas crear una nueva tarea
            </Link>
          </div>
        ) : (
          <div className="bg-slate-950 rounded-lg shadow-sm border border-gray-400 overflow-x-auto overflow-y-auto">
            <table className="w-full text-left border-collapse min-w-800px">
              <thead>
                <tr className="bg-slate-900 border-b border-white">
                  <th className="p-4 font-semibold text-white">Título</th>
                  <th className="p-4 font-semibold text-white">Estado</th>
                  <th className="p-4 font-semibold text-white">Prioridad</th>
                  <th className="p-4 font-semibold text-white">Responsable</th>
                  <th className="p-4 font-semibold text-white">Vence</th>
                  <th className="p-4 font-semibold text-white text-right">Acciones</th>
                </tr>
              </thead>
              <tbody className="bg-slate-950">
                {tasks.map((task) => (
                  <tr key={task.id} className="hover:bg-gray-950 transition:0.3s">
                    <td className="p-4 text-white font-medium">{task.title}</td>
                    <td className="p-4.5">
                      <span className={`px-3.5 py-2 rounded-full text-xs font-bold ${getStatusBadge(task.status)}`}>
                        {task.status}
                      </span>
                    </td>
                    <td className="p-4.5">
                      <span className={`px-3.5 py-2 rounded-full text-xs font-bold ${getPriorityBadge(task.priority)}`}>
                        {task.priority}
                      </span>
                    </td>
                    <td className="p-4.5 text-white">{task.assignedTo}</td>
                    <td className="p-4 text-white">{task.dueDate}</td>
                    <td className="p-4 text-right space-x-3">
                      <button 
                        onClick={() => navigate(`/tasks/${task.id}/edit`)} 
                        className="text-blue-600 font-medium hover:text-blue-800 hover:underline"
                      >
                        Editar
                      </button>
                      <button 
                        onClick={() => handleDelete(task.id)} 
                        className="text-red-600 font-medium hover:text-red-800 hover:underline"
                      >
                        Eliminar
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}