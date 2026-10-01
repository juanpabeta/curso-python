import { api } from '@/api/client';
import { endpoints } from '@/api/endpoints';
import type { RoleRecord, UserInput, UserRecord, UserUpdateInput } from '@/types';
import { parseRoleList, parseUser, parseUserList } from '@/services/parsers';

export const fetchUsers = async (): Promise<UserRecord[]> => {
  const response = await api.get<unknown>(endpoints.users);
  return parseUserList(response.data);
};

export const fetchRoles = async (): Promise<RoleRecord[]> => {
  const response = await api.get<unknown>(endpoints.roles);
  return parseRoleList(response.data);
};

export const createUser = async (payload: UserInput): Promise<UserRecord> => {
  const response = await api.post<unknown>(endpoints.users, payload);
  return parseUser(response.data);
};

export const updateUser = async (id: number, payload: UserUpdateInput): Promise<UserRecord> => {
  const response = await api.put<unknown>(endpoints.user(id), payload);
  return parseUser(response.data);
};

export const deleteUser = async (id: number): Promise<void> => {
  await api.delete(endpoints.user(id));
};

export const assignUserRole = async (userId: number, roleId: number): Promise<void> => {
  await api.post(endpoints.userRole(userId, roleId));
};
