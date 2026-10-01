export const endpoints = {
  subjects: '/subjects/',
  subject: (id: number) => `/subjects/${id}`,
  users: '/users/',
  user: (id: number) => `/users/${id}`,
  userRole: (userId: number, roleId: number) => `/users/${userId}/roles/${roleId}`,
  roles: '/roles/',
  enrollments: '/enrollments/',
  enrollment: (id: number) => `/enrollments/${id}`,
  periods: '/periods/',
  period: (id: number) => `/periods/${id}`,
  grades: '/grades/',
  grade: (id: number) => `/grades/${id}`,
} as const;
