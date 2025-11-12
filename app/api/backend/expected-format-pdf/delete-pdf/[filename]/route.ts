import { NextRequest, NextResponse } from 'next/server'

const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export async function DELETE(
  request: NextRequest,
  { params }: { params: { filename: string } }
) {
  try {
    const { filename } = params
    // Forward the filename exactly as received to avoid double-encoding issues
    const response = await fetch(
      `${BACKEND_URL}/api/expected-format-pdf/delete-pdf/${filename}`,
      {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
      }
    )

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: 'Failed to delete PDF' }))
      throw new Error(errorData.detail || `Backend responded with status: ${response.status}`)
    }

    const data = await response.json()
    return NextResponse.json(data)
  } catch (error: any) {
    console.error('Error deleting PDF:', error)
    return NextResponse.json(
      { error: error.message || 'Failed to delete PDF' },
      { status: 500 }
    )
  }
}



