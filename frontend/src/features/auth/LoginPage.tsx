import { Button, Card, Form, Input, Typography, message } from 'antd'
import { useNavigate } from 'react-router-dom'
import { setAuthToken } from '../../lib/authToken'
import { login } from './authApi'

export function LoginPage() {
  const navigate = useNavigate()

  async function handleFinish(values: { username: string; password: string }) {
    try {
      const result = await login(values.username, values.password)
      setAuthToken(result.accessToken)
      message.success('Login successful')
      navigate('/workspace')
    } catch (error) {
      message.error(error instanceof Error ? error.message : 'Login failed')
    }
  }

  return (
    <div className="page">
      <Card style={{ maxWidth: 420, margin: '80px auto' }}>
        <Typography.Title level={2}>Smart Resume</Typography.Title>
        <Typography.Paragraph>Default account: admin / admin123</Typography.Paragraph>
        <Form layout="vertical" onFinish={handleFinish} initialValues={{ username: 'admin' }}>
          <Form.Item name="username" label="Username" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="password" label="Password" rules={[{ required: true }]}>
            <Input.Password />
          </Form.Item>
          <Button htmlType="submit" type="primary" block>
            Login
          </Button>
        </Form>
      </Card>
    </div>
  )
}
