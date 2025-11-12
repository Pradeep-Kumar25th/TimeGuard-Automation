import { NextRequest, NextResponse } from 'next/server'

const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000'

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData()
    
    const response = await fetch(`${BACKEND_URL}/api/timesheets/upload-excel`, {
      method: 'POST',
      body: formData,
    })

    if (!response.ok) {
      let errorData: any
      try {
        errorData = await response.json()
      } catch {
        errorData = { detail: `Backend responded with status: ${response.status}` }
      }
      console.error('Backend error:', errorData)
      return NextResponse.json(
        { error: errorData.detail || errorData.error || `Backend responded with status: ${response.status}` },
        { status: response.status }
      )
    }

    const data = await response.json()
    return NextResponse.json(data)
  } catch (error: any) {
    console.error('Error uploading Excel file:', error)
    // Check if it's a connection error
    if (error.message && (error.message.includes('ECONNREFUSED') || error.message.includes('fetch failed'))) {
      return NextResponse.json(
        { error: 'Backend server is not running. Please ensure the backend is running on port 8000.' },
        { status: 503 }
      )
    }
    return NextResponse.json(
      { error: error.message || 'Failed to upload Excel file' },
      { status: 500 }
    )
  }
}
