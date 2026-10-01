import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    setError("");

    if (!email.includes("@")) {
      setError("El email no es válido.");
      return;
    }
    
    if (password.length < 4) {
      setError("La contraseña debe tener al menos 4 caracteres.");
      return;
    }

    localStorage.setItem("token", "TOKEN_JWT_FICTICIO_123");
    navigate("/tasks");
  };

  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center ">
      <div className="dark:bg-gray-900/40 p-8 rounded-lg  shadow-md w-md max-w-md">
        <h1 className="text-3xl font-bold mb-6 text-center text-indigo-800">INICIAR SESIÓN</h1>
        
        {error && (
          <p className="text-slate-900 bg-red-500/40 border border-red-400 p-2 rounded mb-4 text-sm font-bold text-center">
            {error}
          </p>
        )}
        
        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="block mb-0.5 text-sm font-medium text-white">Email</label>
            <input
              type="text"
              className="w-full border border-slate-300 p-3 rounded focus:ring-2 focus:ring-blue-600 outline-none text-md text-white bg-slate-900 placeholder:text-slate-400"
              placeholder="usuario@empresa.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>
          
          <div>
            <label className="block mb-1 text-sm font-medium text-white">Contraseña</label>
            <input
              type="password"
              className="w-full border border-slate-300 p-3 rounded focus:ring-2 focus:ring-blue-600 outline-none text-md text-white bg-slate-900 placeholder:text-slate-400"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
          
          <button
            type="submit"
            className="w-full bg-violet-600 text-white font-medium p-3 rounded hover:bg-violet-700 transition"
          >
            Entrar
          </button>
        </form>
      </div>
    </div>
  );
}