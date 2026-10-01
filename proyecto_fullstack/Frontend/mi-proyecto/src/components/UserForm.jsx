import { useState } from 'react';

export function UserForm({ onUserCreated }) {
  const [nombreCompleto, setNombreCompleto] = useState('');
  const [email, setEmail] = useState('');
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    if (nombreCompleto.trim().length < 3) {
      setError('El nombre es demasiado corto (mínimo 3 caracteres)');
      return;
    }

    setLoading(true);

    try {
      const response = await fetch('http://localhost:8000/api/usuarios', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          nombre_completo: nombreCompleto,
          email: email,
        }),
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || 'Error al registrar el usuario');
      }

      const nuevoUsuario = await response.json();
      
      
      setNombreCompleto('');
      setEmail('');
      

      if (onUserCreated) onUserCreated(nuevoUsuario);
      
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-slate-900/60 border border-slate-700/50 backdrop-blur-lg p-8 rounded-2xl shadow-2xl max-w-md w-full">
      
      <div className="mb-6">
        <h2 className="text-xl font-bold text-slate-100">
         Registrar Nuevo Usuario
        </h2>
      </div>
      
    
      {error && (
        <div className="mb-5 p-4 bg-red-500/20 border border-red-500/20 text-red-400 rounded-xl text-xs flex items-center gap-2 ">
          <span>⚠️</span> {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-5">
        <div>
          <label className="block text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">
            Nombre Completo
          </label>
          <input
            type="text"
            value={nombreCompleto}
            onChange={(e) => setNombreCompleto(e.target.value)}
            required
            className="w-full px-4 py-3 bg-slate-950/60 border border-slate-700/60 rounded-xl text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:border-transparent text-sm transition-all"
            placeholder="Ej. Juan Pablo Medina"
          />
        </div>

        <div>
          <label className="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-2">
            Correo Electrónico
          </label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="w-full px-4 py-3 bg-slate-950/60 border border-slate-700/60 rounded-xl text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:border-transparent text-sm transition-all"
            placeholder="Ej. ejemplo@gmail.com"
          />
        </div>

        
        <button
          type="submit"
          disabled={loading}
          className="w-full mt-2 bg-linear-to-r from-blue-600 to-indigo-600 hover:from-pink-500 hover:to-yellow-500 text-white py-3 rounded-xl transition-all duration-200 font-semibold text-sm shadow-lg shadow-indigo-600/30 cursor-pointer"
        >
          {loading ? 'Guardando registro...' : 'Crear Usuario'}
        </button>
      </form>
    </div>
  );
}