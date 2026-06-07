import { Card, Col, Row, Typography } from 'antd'
import { Link } from 'react-router-dom'

export function WorkspacePage() {
  return (
    <div className="page">
      <Typography.Title>Smart Resume Workspace</Typography.Title>
      <Row gutter={[16, 16]}>
        <Col xs={24} md={8}>
          <Link to="/resumes">
            <Card title="My Resumes" hoverable>
              Create, edit, preview, and version resumes.
            </Card>
          </Link>
        </Col>
        <Col xs={24} md={8}>
          <Card title="AI Configuration">Configure AI providers in a follow-up plan.</Card>
        </Col>
        <Col xs={24} md={8}>
          <Card title="Interviews">Interview practice will be implemented later.</Card>
        </Col>
      </Row>
    </div>
  )
}
