// User and Authentication Types
export interface UserRegister {
  email: string
  password: string
}

export interface UserLogin {
  email: string
  password: string
}

export interface UserRegisterResponse {
  message: string
  user_id: string
}

export interface TokenPayload {
  iss: string
  sub: string
  aud: string
  exp: number
  iat: number
  email: string
  phone?: string
  role: string
  session_id: string
  is_anonymous: boolean
}

// Document Types
export interface Document {
  id: number
  title: string
  was_created: string
}

export interface DocumentExtended extends Document {
  content: string
}

export interface CreateDocumentRequest {
  title: string
  content: string
}

export interface DocumentUpdateRequest {
  title: string
  content: string
}

// Validation Types
export interface ValidationError {
  suggestion: string
  explanation: string
  wrong_fragment: string
  loc_index_ch_start: number
  loc_index_ch_end: number
}

export interface ValidationErrorResponse {
  id: number
  is_resolved: boolean
  error: ValidationError | null
}

export interface DocumentValidation {
  id: number
  validated: boolean
  is_valid: boolean
}

export interface DocumentValidationErrorsResponse {
  errors: ValidationErrorResponse[]
}

export interface CreateValidationRequest {
  document_id: number
}

// API Error Types
export interface ApiError {
  detail: string | { msg: string; type: string }[]
}
