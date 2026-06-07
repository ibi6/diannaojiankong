import { Button, Card, Col, Form, Input, Row, Typography, message } from 'antd'
import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { getResume, updateResume } from './resumeApi'
import type { Resume } from './types'

export function ResumeEditPage() {
  const { resumeId } = useParams()
  const [resume, setResume] = useState<Resume | null>(null)

  useEffect(() => {
    if (!resumeId) return
    getResume(resumeId)
      .then(setResume)
      .catch((error) => message.error(error instanceof Error ? error.message : 'Load failed'))
  }, [resumeId])

  async function handleSave(values: { title: string; name: string }) {
    if (!resume) return
    const nextResume: Resume = {
      ...resume,
      title: values.title,
      content: { ...resume.content, basics: { name: values.name } },
    }
    const saved = await updateResume(nextResume)
    setResume(saved)
    message.success('Saved')
  }

  if (!resume) return <div className="page">Loading...</div>

  const basics = (resume.content.basics ?? {}) as { name?: string }

  return (
    <div className="page">
      <Typography.Title>Edit Resume</Typography.Title>
      <Row gutter={16}>
        <Col xs={24} lg={12}>
          <Card title="Editor">
            <Form layout="vertical" onFinish={handleSave} initialValues={{ title: resume.title, name: basics.name }}>
              <Form.Item name="title" label="Title" rules={[{ required: true }]}>
                <Input />
              </Form.Item>
              <Form.Item name="name" label="Name">
                <Input />
              </Form.Item>
              <Button type="primary" htmlType="submit">Save</Button>
            </Form>
          </Card>
        </Col>
        <Col xs={24} lg={12}>
          <Card title="Preview">
            <Typography.Title level={3}>{basics.name || resume.title}</Typography.Title>
            <pre>{JSON.stringify(resume.content, null, 2)}</pre>
          </Card>
        </Col>
      </Row>
    </div>
  )
}
