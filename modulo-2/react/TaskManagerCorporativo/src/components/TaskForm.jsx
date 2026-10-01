import { useState, useEffect } from "react";

const EMPTY_TASK = {
  title: "",
  description: "",
  priority: "Media",
  status: "Pendiente",
  dueDate: "",
  assignedTo: "",
  tags: ""
};

export default function TaskForm({ initialData, onSubmit, loading }) {
  const [form, setForm] = useState(EMPTY_TASK);
  const [error, setError] = useState("");

  useEffect(() => {
    if (initialData) {
      setForm({
        ...initialData,
        tags: initialData.tags && Array.isArray(initialData.tags) ? initialData.tags.join(", ") : ""
      });
    }
  }, [initialData]);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setError("");

    if (!form.title.trim()) {
      setError("El título es obligatorio.");
      return;
    }
    if (!form.description.trim() || form.description.trim().length < 10) {
      setError("La descripción debe tener al menos 10 caracteres.");
      return;
    }
    if (!form.dueDate) {
      setError("La fecha de vencimiento es obligatoria.");
      return;
    }
    if (!form.assignedTo.trim()) {
      setError("Debe asignarse un responsable.");
      return;
    }

    const payload = {
      ...form,
      tags: form.tags
        ? form.tags.split(",").map((t) => t.trim()).filter(Boolean)
        : []
    };

    onSubmit(payload);
  };

  return (
    <div className="bg-slate-950 p-6 rounded-lg shadow-md border border-gray-100">
      {error && (
        <p className="text-red-600 border border-red-300 bg-red-200 p-3 rounded mb-4 text-sm font-medium">
          {error}
        </p>
      )}
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-semibold text-white mb-1">Título</label>
          <input
            type="text"
            name="title"
            value={form.title}
            onChange={handleChange}
            className={`w-full border p-2 rounded focus:ring-2 focus:ring-slate-800 
              text-white bg-slate-950 outline-none ${error === "El título es obligatorio." ? 'border-red-800' : 'border-gray-300'}`}
          />
        </div>

        <div>
          <label className="block text-sm font-semibold text-white mb-1">Descripción</label>
          <textarea
            name="description"
            value={form.description}
            onChange={handleChange}
            rows="4"
            className={`w-full border p-2 rounded focus:ring-2 focus:ring-slate-800 
              text-white bg-slate-950 outline-none ${error === "La descripción debe tener al menos 10 caracteres." ? 'border-red-800' : 'border-gray-300'}`}
          ></textarea>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-semibold text-white mb-1">Prioridad</label>
            <select
              name="priority"
              value={form.priority}
              onChange={handleChange}
              className="w-full border border-gray-200 p-2 rounded focus:ring-2 focus:ring-slate-800 outline-none text-sm text-white bg-slate-950"
            >
              <option value="Baja">Baja</option>
              <option value="Media">Media</option>
              <option value="Alta">Alta</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-semibold text-white mb-1">Estado</label>
            <select
              name="status"
              value={form.status}
              onChange={handleChange}
              className="w-full border border-gray-300 p-2 rounded focus:ring-2 focus:ring-slate-800 outline-none text-white bg-slate-950 "
            >
              <option value="Pendiente">Pendiente</option>
              <option value="En progreso">En progreso</option>
              <option value="Completada">Completada</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-semibold text-white mb-1">Fecha de vencimiento</label>
            <input
              type="date"
              name="dueDate"
              value={form.dueDate}
              onChange={handleChange}
              className={`w-full border p-2 rounded focus:ring-2 focus:ring-slate-800 
                text-white bg-slate-950 outline-none ${error === "La fecha de vencimiento es obligatoria." ? 'border-red-800' : 'border-gray-300'}`}
            />
          </div>
          <div>
            <label className="block text-sm font-semibold text-white mb-1">Responsable</label>
            <input
              type="text"
              name="assignedTo"
              value={form.assignedTo}
              onChange={handleChange}
              className={`w-full border p-2 rounded focus:ring-2 focus:ring-blue-500 
                text-white bg-slate-950 outline-none ${error === "Debe asignarse un responsable." ? 'border-red-800' : 'border-gray-300'}`}
            />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Tags (opcional, separar por comas)</label>
          <input
            type="text"
            name="tags"
            value={form.tags}
            onChange={handleChange}
            className="w-full border border-white p-2 rounded focus:ring-2 focus:ring-blue-500 outline-none text-white bg-slate-950"
            placeholder="ej: legal, cliente X"
          />
        </div>

        <div className="pt-4">
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-indigo-600 text-white font-medium p-3 rounded hover:bg-indigo-800 transition disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? "Guardando..." : "Guardar tarea"}
          </button>
        </div>
      </form>
    </div>
  );
}