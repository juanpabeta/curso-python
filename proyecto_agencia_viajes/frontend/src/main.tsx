import { BrowserRouter } from 'react-router-dom';
import { AuthProvider } from './auth';
import { AppRoutes } from './routes';
import './styles.css';
export default function App() { return <AuthProvider><AppRoutes /></AuthProvider>; }
import { createRoot } from 'react-dom/client';
createRoot(document.getElementById('root')!).render(<BrowserRouter><App /></BrowserRouter>);
