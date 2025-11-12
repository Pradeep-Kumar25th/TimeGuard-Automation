import { NextRequest, NextResponse } from 'next/server'

const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export async function DELETE(request: NextRequest) {
  try {
    const response = await fetch(`${BACKEND_URL}/api/expected-format-pdf/delete-all-pdfs`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: 'Failed to delete all PDFs' }))
      throw new Error(errorData.detail || `Backend responded with status: ${response.status}`)
    }

    const data = await response.json()
    return NextResponse.json(data)
  } catch (error: any) {
    console.error('Error deleting all PDFs:', error)
    return NextResponse.json(
      { error: error.message || 'Failed to delete all PDFs' },
      { status: 500 }
    )
  }
}



