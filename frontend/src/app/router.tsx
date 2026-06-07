import { createBrowserRouter, Navigate } from 'react-router-dom'
import { LoginPage } from '../features/auth/LoginPage'
import { ResumeEditPage } from '../features/resume/ResumeEditPage'
import { ResumeListPage } from '../features/resume/ResumeListPage'
import { WorkspacePage } from '../features/workspace/WorkspacePage'

export const router = createBrowserRouter([
  { path: '/', element: <Navigate to="/workspace" replace /> },
  { path: '/auth/login', element: <LoginPage /> },
  { path: '/workspace', element: <WorkspacePage /> },
  { path: '/resumes', element: <ResumeListPage /> },
  { path: '/resumes/:resumeId/edit', element: <ResumeEditPage /> },
])
