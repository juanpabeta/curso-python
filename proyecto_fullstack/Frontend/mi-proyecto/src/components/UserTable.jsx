import { useState } from 'react';
import { DeleteModal } from './DeleteModal'; 

export function UserTable({ usuarios, onUserDeleted }) {
  const [userToDelete, setUserToDelete] = useState(null); 
  const handleConfirmDelete = async () => {
    if (!userToDelete) return;

    try {
      const response = await fetch(`http://localhost:8000/api/usuarios/${userToDelete.id}`, {
        method: 'DELETE',
      });

      if (!response.ok) throw new Error('Error al eliminar el usuario');

      
      if (onUserDeleted) onUserDeleted();
      
    } catch (err) {
      alert(err.message);
    } finally {
      setUserToDelete(null); 
    }
  };

  return (
    <>
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-indigo-950/40 text-indigo-300 border-b border-indigo-500/20 uppercase text-xs tracking-wider font-bold">
              <th className="px-6 py-4">ID</th>
              <th className="px-6 py-4">Nombre Completo</th>
              <th className="px-6 py-4">Correo Electrónico</th>
              <th className="px-6 py-4 text-center">Fecha de Registro</th>
              <th className="px-6 py-4 text-center">Acciones</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60">
            {usuarios.map((usuario) => (
              <tr key={usuario.id} className="hover:bg-indigo-950/20 transition-colors">
                <td className="px-6 py-4 text-sm font-semibold text-green-400">#{usuario.id}</td>
                <td className="px-6 py-4 text-sm font-medium text-slate-200">{usuario.nombre_completo}</td>
                <td className="px-6 py-4 text-sm text-slate-400">{usuario.email}</td>
                <td className="px-6 py-4 text-sm text-center">{new Date(usuario.fecha_registro).toLocaleDateString()}</td>
                <td className="px-6 py-4 text-sm text-center">
           
                  <button 
                    onClick={() => setUserToDelete(usuario)}
                    className="text-xs bg-red-500/10 text-red-400 hover:bg-red-500/20 px-3 py-1.5 rounded-lg border border-red-500/20 transition"
                  >
                     Eliminar
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <DeleteModal 
        isOpen={!!userToDelete}
        userName={userToDelete?.nombre_completo}
        onClose={() => setUserToDelete(null)}
        onConfirm={handleConfirmDelete}
      />
    </>
  );
}