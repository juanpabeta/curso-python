import type { RoleName } from '@/types';

export interface NavItem {
  to: string;
  label: string;
  roles: RoleName[];
  end?: boolean;
}

export const NAV_ITEMS: NavItem[] = [
  { to: '/student', label: 'Inicio', roles: ['Estudiante'], end: true },
  { to: '/teacher', label: 'Inicio', roles: ['Docente'], end: true },
  { to: '/teacher/calificaciones', label: 'Calificaciones', roles: ['Docente'] },
  { to: '/admin', label: 'Inicio', roles: ['Administrador'], end: true },
  { to: '/admin/materias', label: 'Materias', roles: ['Administrador'] },
  { to: '/admin/usuarios', label: 'Usuarios', roles: ['Administrador'] },
  { to: '/admin/periodos', label: 'Períodos', roles: ['Administrador'] },
  { to: '/admin/inscripciones', label: 'Inscripciones', roles: ['Administrador'] },
  { to: '/admin/calificaciones', label: 'Calificaciones', roles: ['Administrador'] },
];
