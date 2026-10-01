import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { api } from "../api/client.js";
import TaskForm from "../components/TaskForm.jsx";

export default function TaskPage({ mode }) {
  const { id } = useParams();
  const navigate = useNavigate();
  const [initialData, setInitialData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [fetching, setFetching] = useState(mode === "edit");

  useEffect(() => {
    if (mode === "edit" && id) {
      api.get(`/tasks/${id}`)
        .then(res => {
          setInitialData(res.data);
          setFetching(false);
        })
        .catch(() => {
          alert("No se pudo cargar la tarea.");
          navigate("/tasks");
        });
    }
  }, [mode, id, navigate]);

  const handleSubmit = async (payload) => {
    setLoading(true);
    try {
      if (mode === "create") {
        await api.post("/tasks", payload);
      } else {
        await api.put(`/tasks/${id}`, payload);
      }
      navigate("/tasks");
    } catch (err) {
      alert("Ocurrió un error al guardar la tarea.");
    } finally {
      setLoading(false);
    }
  };

  if (fetching) return <div className="p-8 text-center text-lg text-slate-600">Cargando...</div>;

  return (
    <div className="min-h-screen bg-slate-950 p-4 md:p-8">
      <div className="max-w-2xl mx-auto">
        <button 
          onClick={() => navigate("/tasks")} 
          className="mb-6 text-blue-600 font-medium hover:underline flex items-center"
        >
          &larr; Volver a la lista
        </button>
        
        <h1 className="text-2xl font-bold mb-6 text-purple-800">
          {mode === "create" ? "Nueva tarea" : "Editar tarea"}
        </h1>
        
        <TaskForm 
          key={initialData?.id || "new"} 
          initialData={initialData} 
          onSubmit={handleSubmit} 
          loading={loading} 
        />
      </div>
    </div>
  );
}