import { createBrowserRouter, Navigate } from 'react-router-dom'
import { LoginPage } from '../features/auth/LoginPage'
import { ResumeEditPage } from '../features/resume/ResumeEditPage'
import { ResumeListPage } from '../features/resume/ResumeListPage'
import { WorkspacePage } from '../features/workspace/WorkspacePage'
import { ProtectedRoute } from './ProtectedRoute'

export const router = createBrowserRouter([
  { path: '/', element: <Navigate to="/workspace" replace /> },
  { path: '/auth/login', element: <LoginPage /> },
  {
    path: '/workspace',
    element: (
      <ProtectedRoute>
        <WorkspacePage />
      </ProtectedRoute>
    ),
  },
  {
    path: '/resumes',
    element: (
      <ProtectedRoute>
        <ResumeListPage />
      </ProtectedRoute>
    ),
  },
  {
    path: '/resumes/:resumeId/edit',
    element: (
      <ProtectedRoute>
        <ResumeEditPage />
      </ProtectedRoute>
    ),
  },
])
