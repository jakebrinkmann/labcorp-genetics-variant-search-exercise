import {test, vi, expect} from 'vitest'
import {render, screen} from '@testing-library/react'
import VariantList from './VariantList'

const mockResponse = {
  count: 0,
  results: [],
}

global.fetch = vi.fn(async () => ({
  json: async () => mockResponse,
}))

test('renders VariantList', () => {
  render(<VariantList />)
  expect(screen.getByText('Search by gene')).toBeInTheDocument()
})
