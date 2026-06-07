import { Navigate, useLocation } from 'react-router-dom'
import { getAuthToken } from '../../lib/authToken'

export function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const token = getAuthToken()
  const location = useLocation()

  if (!token) {
    return <Navigate to="/auth/login" state={{ from: location }} replace />
  }

  return <>{children}</>
}
