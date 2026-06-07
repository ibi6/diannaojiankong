export interface Resume {
  id: string
  title: string
  templateKey: string
  content: Record<string, unknown>
  layout: Record<string, unknown>
  createdAt: string
  updatedAt: string
}

export interface ResumeList {
  items: Resume[]
}
