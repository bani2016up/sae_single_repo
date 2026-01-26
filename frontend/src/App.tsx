import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { Toaster } from 'sonner'
import { AuthProvider } from './context/AuthContext'
import { ThemeProvider } from './context/ThemeContext'
import { ProtectedRoute } from './components/common/ProtectedRoute'
import { Navbar } from './components/common/Navbar'
import { LandingPage } from './pages/LandingPage'
import { LoginPage } from './pages/LoginPage'
import { RegisterPage } from './pages/RegisterPage'
import { DashboardPage } from './pages/DashboardPage'
import { DocumentsListPage } from './pages/DocumentsListPage'
import { CreateDocumentPage } from './pages/CreateDocumentPage'
import { DocumentDetailPage } from './pages/DocumentDetailPage'
import { AnalysisListPage } from './pages/AnalysisListPage'
import { AnalysisDetailPage } from './pages/AnalysisDetailPage'
import './styles/globals.css'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
})

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider>
        <AuthProvider>
          <BrowserRouter>
            <div className="min-h-screen bg-background">
              <Navbar />
              <Routes>
                <Route path="/" element={<LandingPage />} />
                <Route path="/login" element={<LoginPage />} />
                <Route path="/register" element={<RegisterPage />} />
                
                <Route
                  path="/dashboard"
                  element={
                    <ProtectedRoute>
                      <DashboardPage />
                    </ProtectedRoute>
                  }
                />
                
                <Route
                  path="/documents"
                  element={
                    <ProtectedRoute>
                      <DocumentsListPage />
                    </ProtectedRoute>
                  }
                />
                
                <Route
                  path="/documents/new"
                  element={
                    <ProtectedRoute>
                      <CreateDocumentPage />
                    </ProtectedRoute>
                  }
                />
                
                <Route
                  path="/documents/:id"
                  element={
                    <ProtectedRoute>
                      <DocumentDetailPage />
                    </ProtectedRoute>
                  }
                />
                
                <Route
                  path="/analysis"
                  element={
                    <ProtectedRoute>
                      <AnalysisListPage />
                    </ProtectedRoute>
                  }
                />
                
                <Route
                  path="/analysis/:id"
                  element={
                    <ProtectedRoute>
                      <AnalysisDetailPage />
                    </ProtectedRoute>
                  }
                />
                
                <Route path="*" element={<Navigate to="/" replace />} />
              </Routes>
            </div>
            <Toaster position="top-right" />
          </BrowserRouter>
        </AuthProvider>
      </ThemeProvider>
    </QueryClientProvider>
  )
}

export default App
