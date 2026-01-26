import apiClient from './client'
import type {
  UserRegister,
  UserLogin,
  UserRegisterResponse,
  TokenPayload,
} from '../types/api'

const AUTH_BASE = '/api/v1/auth'

export const authApi = {
  register: async (data: UserRegister): Promise<UserRegisterResponse> => {
    const response = await apiClient.post(`${AUTH_BASE}/users`, data)
    return response.data
  },

  login: async (data: UserLogin): Promise<{ message: string }> => {
    const response = await apiClient.post(`${AUTH_BASE}/sessions`, data)
    return response.data
  },

  logout: async (): Promise<void> => {
    await apiClient.delete(`${AUTH_BASE}/sessions/`)
  },

  getCurrentUser: async (): Promise<TokenPayload> => {
    const response = await apiClient.get(`${AUTH_BASE}/users/me`)
    return response.data
  },
}
