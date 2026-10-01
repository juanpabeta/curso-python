const toBase64Url = (value: object): string =>
  btoa(JSON.stringify(value)).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');

export const buildJwt = (claims: Record<string, unknown> = {}): string => {
  const header = toBase64Url({ alg: 'HS256', typ: 'JWT' });
  const payload = toBase64Url({
    sub: 2,
    email: 'student@universidad.test',
    full_name: 'Estudiante E2E',
    roles: ['Estudiante'],
    exp: Math.floor(Date.now() / 1000) + 3600,
    ...claims,
  });

  return `${header}.${payload}.e2e-signature`;
};

export const buildExpiredJwt = (): string =>
  buildJwt({
    exp: Math.floor(Date.now() / 1000) - 30,
  });
