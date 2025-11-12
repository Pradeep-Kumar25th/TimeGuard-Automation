import { NextRequest, NextResponse } from 'next/server'

const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export async function GET(request: NextRequest) {
  try {
    // Try to fetch from backend
    const response = await fetch(`${BACKEND_URL}/api/expected-format-pdf/list-generated-pdfs`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      cache: 'no-store',
    })

    // If backend endpoint not found, return empty result instead of error
    if (response.status === 404) {
      console.warn('Backend endpoint not found, returning empty list')
      return NextResponse.json({
        files: [],
        count: 0,
        output_directory: '',
        format: 'Expected Format (matching Expected.pdf)'
      })
    }

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: 'Failed to fetch PDFs' }))
      throw new Error(errorData.detail || `Backend responded with status: ${response.status}`)
    }

    const data = await response.json()
    
    // Ensure the response has the expected structure
    return NextResponse.json({
      files: data.files || [],
      count: data.count || (data.files ? data.files.length : 0),
      output_directory: data.output_directory || '',
      format: data.format || 'Expected Format (matching Expected.pdf)'
    })
  } catch (error: any) {
    console.error('Error fetching generated PDFs:', error)
    // Return empty list instead of error to prevent UI breakage
    return NextResponse.json({
      files: [],
      count: 0,
      output_directory: '',
      format: 'Expected Format (matching Expected.pdf)',
      error: error.message || 'Failed to fetch generated PDFs'
    })
  }
}

