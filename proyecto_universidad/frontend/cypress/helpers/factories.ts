export const buildTaskTitle = (suffix = ''): string => {
  const stamp = Date.now();
  return `e2e-tarea-${stamp}${suffix ? `-${suffix}` : ''}`.slice(0, 120);
};

export const buildTaskPayload = (overrides: Partial<{ id: string; title: string; completed: boolean }> = {}) => ({
  id: overrides.id ?? crypto.randomUUID(),
  title: overrides.title ?? buildTaskTitle('fixture'),
  completed: overrides.completed ?? false,
});
