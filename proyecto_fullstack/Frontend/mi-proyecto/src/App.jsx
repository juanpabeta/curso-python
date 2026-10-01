import { useState, useEffect } from 'react';
import { UserForm } from './components/UserForm';
import { UserTable } from './components/UserTable';

export default function App() {
  const [usuarios, setUsuarios] = useState([]);
  const [search, setSearch] = useState('');
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchUsuarios = async () => {
    setLoading(true);
    setError(null);
    try {
      let url = `http://localhost:8000/api/usuarios?page=${page}&limit=5`;
      if (search) {
        url += `&search=${encodeURIComponent(search)}`;
      }

      const response = await fetch(url);
      if (!response.ok) {
        throw new Error('No se pudieron cargar los usuarios');
      }

      const data = await response.json();
      setUsuarios(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUsuarios();
  }, [page, search]);

  const handleUserCreated = () => {
    fetchUsuarios();
  };

  return (
    <div className="min-h-screen bg-linear-to-br from-slate-900 via-indigo-950 to-slate-900 text-slate-100 p-8 px-2 sm:px-6 lg:px-8 ">
      <div className="max-w-7xl mx-auto mb-12 space-y-9" >
    
        <header className="flex flex-col md:flex-row justify-between items-center bg-slate-800/40 border border-slate-700/50 p-6 rounded-2xl backdrop-blur-xl shadow-2xl">
          <div className="flex flex-col md:flex-row items-center space-y-2 "> 
            <h1 className="text-2xl font-black bg-clip-text 
            text-transparent bg-linear-to-r from-blue-500 via-indigo-600 to-pink-500">
             Panel de Gestión de Usuarios
            </h1>
      
          </div>
          <div className="mt-4 md:mt-0 px-4 py-2 bg-green-500/10 border border-green-500/20 rounded-full text-green-400 text-sm font-semibold tracking-wide uppercase">
            {usuarios.length} Usuarios
          </div>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          <div className="lg:col-span-1">
            <div className="bg-slate-800/40 border border-slate-700/50 p-8 rounded-2xl shadow-2xl backdrop-blur-xl ">
              <UserForm onUserCreated={handleUserCreated} />
            </div>
          </div>

  <div className="lg:col-span-2 space-y-6">

<div className="bg-slate-800/40 border border-slate-700/50 p-5 rounded-2xl shadow-2xl backdrop-blur-xl">
  <div className="flex items-center space-x-2 mb-2">

    <svg className="w-4 h-4 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707v4.172a1 1 0 01-1.447.894l-4-2A1 1 0 017 18v-3.172a1 1 0 00-.293-.707L.293 7.293A1 1 0 010 6.586V4z" />
    </svg>
    <label className="block text-xs font-bold uppercase tracking-wider text-slate-400">
      Filtrar Registros
    </label>
  </div>
  
  <div className="relative">
    <span className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none text-slate-400">
      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
      </svg>
    </span>
    <input
      type="text"
      placeholder="Buscar por nombre o correo electrónico..."
      value={search}
      onChange={(e) => {
        setSearch(e.target.value);
        setPage(1);
      }}
      className="w-full pl-10 pr-4 py-2.5 bg-slate-900/60 border border-slate-700/60 rounded-xl text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all text-sm"
    />
  </div>
</div>

            {/* Mensaje de Error */}
            {error && (
              <div className="p-4 bg-red-500/10 border border-red-500/20 text-red-400 rounded-xl text-sm flex items-center space-x-2">
                <span>⚠️</span>
                <span>{error}</span>
              </div>
            )}

            
            <div className="bg-slate-800/40 border border-slate-700/50 rounded-2xl shadow-2xl backdrop-blur-xl overflow-hidden">
              {loading ? (
                <div className="flex flex-col items-center justify-center py-12 space-y-3">
                  <div className="w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
                  <p className="text-sm text-gray-400">Cargando registros...</p>
                </div>
              ) : (
                <UserTable usuarios={usuarios} />
              )}
            </div>

           
    <div className="flex justify-between items-center bg-slate-800/40 border border-slate-700/50 px-6 py-4 rounded-2xl shadow-2xl backdrop-blur-xl">
    <button
    onClick={() => 
      setPage((prev) => Math.max(prev - 1, 1))
    }
      
    disabled={page === 1}
    className="px-4 py-2 bg-linear-to-r from-blue-600 to-indigo-600 hover:from-pink-500 hover:to-yellow-500 text-slate-200 rounded-xl text-sm font-semibold transition disabled:opacity-40 disabled:cursor-not-allowed"
  >
    ← Anterior
    </button>
  
  <div className="text-sm font-medium text-slate-400">
    Página <span className="text-slate-200 font-bold">{page}</span>
  </div>

  <button
    onClick={(e) =>  setPage((prev) => prev + 1)
   
    }
    disabled={usuarios.length < 5}
    className="px-4 py-2 bg-linear-to-r from-blue-600 to-indigo-600 hover:from-pink-500 hover:to-yellow-500 text-white rounded-xl text-sm font-semibold transition disabled:opacity-40 disabled:cursor-not-allowed "
  >
    Siguiente →
  </button>
</div>

          </div>
        </div>

      </div>
    </div>
  );
}