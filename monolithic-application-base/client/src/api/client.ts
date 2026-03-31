/**
 * Axios instance and API helper functions.
 * All calls go through the Vite proxy (/api → localhost:8000).
 */

import axios from 'axios'
import type { Token, UserResponse, RolePermissionsMap, PermissionSet } from '@/types'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '',
  headers: { 'Content-Type': 'application/json' },
})

// Attach JWT to every request if present
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Redirect to login on 401
api.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(err)
  }
)

/* -------------------- Auth -------------------- */

export const loginUser = async (username: string, password: string): Promise<Token> => {
  const { data } = await api.post<Token>('/auth/login', { username, password })
  return data
}

/* -------------------- User Management -------------------- */

export const listUsers = async (): Promise<UserResponse[]> => {
  const { data } = await api.get<UserResponse[]>('/users')
  return data
}

export const createUser = async (payload: { username: string; password: string; role: string }): Promise<UserResponse> => {
  const { data } = await api.post<UserResponse>('/users', payload)
  return data
}

export const updateUser = async (id: number, payload: { role?: string; password?: string }): Promise<UserResponse> => {
  const { data } = await api.patch<UserResponse>(`/users/${id}`, payload)
  return data
}

export const deleteUser = async (id: number): Promise<void> => {
  await api.delete(`/users/${id}`)
}

/* -------------------- Role Permissions -------------------- */

export const getRolePermissions = async (): Promise<RolePermissionsMap> => {
  const { data } = await api.get<RolePermissionsMap>('/permissions')
  return data
}

export const updateRolePermissions = async (role: string, permissions: PermissionSet): Promise<PermissionSet> => {
  const { data } = await api.put<PermissionSet>(`/permissions/${role}`, { permissions })
  return data
}

// ─── Add Your Custom API Functions Below ─────────────────────────────────────
// Add your application-specific API functions here
// Example:
//
// export const listYourModels = async (): Promise<YourModel[]> => {
//   const { data } = await api.get<YourModel[]>('/your-endpoint')
//   return data
// }
//
// export const createYourModel = async (payload: YourModelCreate): Promise<YourModel> => {
//   const { data } = await api.post<YourModel>('/your-endpoint', payload)
//   return data
// }

