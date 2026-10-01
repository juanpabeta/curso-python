import { FormEvent, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/Button';
import { TextField } from '@/components/ui/TextField';
import { useAuth } from '@/hooks/useAuth';
import { isValidEmail, validatePassword } from '@/utils/validators';

export const LoginPage = () => {
  const navigate = useNavigate();
  const { login, isLoading, sessionNotice, clearSessionNotice } = useAuth();
  const [email, setEmail] = useState('admin@universidad.test');
  const [password, setPassword] = useState('Secret123!');
  const [error, setError] = useState('');

  const visibleError = error || sessionNotice;

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError('');
    clearSessionNotice();

    if (!isValidEmail(email)) {
      setError('Ingresa un correo válido.');
      return;
    }

    const passwordError = validatePassword(password);
    if (passwordError) {
      setError(passwordError);
      return;
    }

    try {
      await login(email, password);
      navigate('/', { replace: true });
    } catch (loginError) {
      setError(loginError instanceof Error ? loginError.message : 'No se pudo iniciar sesión.');
    }
  };

  return (
    <section aria-labelledby="login-title" className="login-card">
      <h1 id="login-title">Iniciar sesión</h1>
      <p>Accede al panel académico de la Universidad Digital</p>

      <form onSubmit={(event) => void handleSubmit(event)} noValidate>
        <TextField
          id="email"
          label="Correo electrónico"
          type="email"
          value={email}
          onChange={setEmail}
          autoComplete="email"
          invalid={Boolean(visibleError)}
          required
        />
        <TextField
          id="password"
          label="Contraseña"
          type="password"
          value={password}
          onChange={setPassword}
          autoComplete="current-password"
          invalid={Boolean(visibleError)}
          required
        />

        {visibleError ? (
          <p className="error-message" role="alert">
            {visibleError}
          </p>
        ) : null}

        <Button type="submit" isLoading={isLoading} loadingLabel="Ingresando...">
          Ingresar
        </Button>
      </form>
    </section>
  );
};
