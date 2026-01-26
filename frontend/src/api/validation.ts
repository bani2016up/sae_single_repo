import apiClient from './client'
import type {
  CreateValidationRequest,
  DocumentValidation,
  DocumentValidationErrorsResponse,
} from '../types/api'

const VALIDATION_BASE = '/api/v1/validation'

export const validationApi = {
  create: async (data: CreateValidationRequest): Promise<DocumentValidation> => {
    const response = await apiClient.post(VALIDATION_BASE, data)
    return response.data
  },

  start: async (id: number): Promise<DocumentValidation> => {
    const response = await apiClient.post(`${VALIDATION_BASE}/${id}/start`)
    return response.data
  },

  reset: async (id: number): Promise<void> => {
    await apiClient.put(`${VALIDATION_BASE}/${id}/reset`)
  },

  getById: async (id: number): Promise<DocumentValidation> => {
    const response = await apiClient.get(`${VALIDATION_BASE}/${id}`)
    return response.data
  },

  getErrors: async (id: number): Promise<DocumentValidationErrorsResponse> => {
    const response = await apiClient.get(`${VALIDATION_BASE}/${id}/errors`)
    return response.data
  },
}
