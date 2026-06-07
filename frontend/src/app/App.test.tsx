import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import { App } from './App'

describe('App', () => {
  it('renders the workspace route by default', async () => {
    render(<App />)
    const heading = await screen.findByText('Smart Resume Workspace')
    expect(heading).toBeTruthy()
  })
})
