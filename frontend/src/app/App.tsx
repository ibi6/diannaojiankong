import { ConfigProvider } from 'antd'
import { RouterProvider } from 'react-router-dom'
import { router } from './router'

export function App() {
  return (
    <ConfigProvider>
      <RouterProvider router={router} />
    </ConfigProvider>
  )
}
