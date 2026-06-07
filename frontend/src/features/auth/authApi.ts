import { request } from '../../lib/apiClient'

interface LoginResult {
  accessToken: string
  tokenType: string
  user: {
    id: number
    username: string
    isAdmin: boolean
  }
}

export function login(username: string, password: string) {
  return request<LoginResult>('/api/auth/login', {
    method: 'POST',
    body: { username, password },
  })
}
