import { getAuthToken } from './authToken'

export interface ApiEnvelope<T> {
  success: boolean
  message: string
  data: T
}

export async function request<T>(path: string, options: RequestInit & { body?: unknown } = {}) {
  const token = getAuthToken()
  const headers = new Headers(options.headers)
  headers.set('Content-Type', 'application/json')
  if (token) headers.set('Authorization', `Bearer ${token}`)

  const response = await fetch(path, {
    ...options,
    headers,
    body: options.body === undefined ? undefined : JSON.stringify(options.body),
  })
  const envelope = (await response.json()) as ApiEnvelope<T>
  if (!response.ok || !envelope.success) {
    throw new Error(envelope.message || 'Request failed')
  }
  return envelope.data
}
