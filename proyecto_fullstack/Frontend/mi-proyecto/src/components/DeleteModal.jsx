export function DeleteModal({ isOpen, onClose, onConfirm, userName }) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm animate-fade-in">
      <div className="bg-slate-900 border border-slate-700/60 p-6 rounded-2xl shadow-2xl max-w-md w-full text-center space-y-4">
        
        {/* Icono de advertencia */}
        <div className="mx-auto flex items-center justify-center w-12 h-12 rounded-full bg-red-500/10 border border-red-500/20 text-red-400">
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        </div>

        {/* Títulos y mensaje */}
        <div>
          <h3 className="text-lg font-bold text-slate-100">¿Eliminar usuario?</h3>
          <p className="text-sm text-slate-400 mt-1">
            Estás a punto de eliminar a <span className="text-slate-200 font-semibold">{userName}</span>. Esta acción no se puede deshacer.
          </p>
        </div>

        {/* Botones de acción */}
        <div className="flex space-x-3 pt-2">
          <button
            type="button"
            onClick={onClose}
            className="flex-1 px-4 py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-300 text-sm font-semibold rounded-xl border border-slate-700 transition"
          >
            Cancelar
          </button>
          <button
            type="button"
            onClick={onConfirm}
            className="flex-1 px-4 py-2.5 bg-red-600 hover:bg-red-500 text-white text-sm font-semibold rounded-xl transition shadow-lg shadow-red-600/20"
          >
            Sí, eliminar
          </button>
        </div>

      </div>
    </div>
  );
}