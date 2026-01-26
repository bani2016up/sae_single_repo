import apiClient from './client'
import type {
  Document,
  DocumentExtended,
  CreateDocumentRequest,
  DocumentUpdateRequest,
} from '../types/api'

const DOCS_BASE = '/api/v1/documents'

export const documentsApi = {
  getAll: async (): Promise<Document[]> => {
    const response = await apiClient.get(DOCS_BASE)
    return response.data
  },

  getById: async (id: number): Promise<DocumentExtended> => {
    const response = await apiClient.get(`${DOCS_BASE}/${id}`)
    return response.data
  },

  create: async (data: CreateDocumentRequest): Promise<Document> => {
    const response = await apiClient.post(DOCS_BASE, data)
    return response.data
  },

  createFromFile: async (file: File): Promise<Document> => {
    const formData = new FormData()
    formData.append('file', file)
    const response = await apiClient.post(`${DOCS_BASE}/from-file`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  update: async (id: number, data: DocumentUpdateRequest): Promise<Document> => {
    const response = await apiClient.put(`${DOCS_BASE}/${id}`, data)
    return response.data
  },

  delete: async (id: number): Promise<void> => {
    await apiClient.delete(`${DOCS_BASE}/${id}`)
  },
}
