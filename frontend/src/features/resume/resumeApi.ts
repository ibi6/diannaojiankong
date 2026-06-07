import { request } from '../../lib/apiClient'
import type { Resume, ResumeList } from './types'

export function listResumes() {
  return request<ResumeList>('/api/resumes')
}

export function createResume(title: string) {
  return request<Resume>('/api/resumes', {
    method: 'POST',
    body: { title, templateKey: 'classic' },
  })
}

export function getResume(id: string) {
  return request<Resume>(`/api/resumes/${id}`)
}

export function updateResume(resume: Resume) {
  return request<Resume>(`/api/resumes/${resume.id}`, {
    method: 'PUT',
    body: {
      title: resume.title,
      templateKey: resume.templateKey,
      content: resume.content,
      layout: resume.layout,
    },
  })
}
