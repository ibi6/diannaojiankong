import { Button, Card, List, Space, Typography, message } from 'antd'
import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { createResume, listResumes } from './resumeApi'
import type { Resume } from './types'

export function ResumeListPage() {
  const [resumes, setResumes] = useState<Resume[]>([])
  const navigate = useNavigate()

  async function load() {
    const result = await listResumes()
    setResumes(result.items)
  }

  async function handleCreate() {
    try {
      const resume = await createResume('Untitled Resume')
      navigate(`/resumes/${resume.id}/edit`)
    } catch (error) {
      message.error(error instanceof Error ? error.message : 'Create failed')
    }
  }

  useEffect(() => {
    load().catch((error) => message.error(error instanceof Error ? error.message : 'Load failed'))
  }, [])

  return (
    <div className="page">
      <Space direction="vertical" size="large" style={{ width: '100%' }}>
        <Space style={{ justifyContent: 'space-between', width: '100%' }}>
          <Typography.Title>My Resumes</Typography.Title>
          <Button type="primary" onClick={handleCreate}>New Resume</Button>
        </Space>
        <List
          grid={{ gutter: 16, xs: 1, md: 2, lg: 3 }}
          dataSource={resumes}
          renderItem={(resume) => (
            <List.Item>
              <Card title={resume.title} actions={[<Link to={`/resumes/${resume.id}/edit`}>Edit</Link>]}>
                Template: {resume.templateKey}
              </Card>
            </List.Item>
          )}
        />
      </Space>
    </div>
  )
}
