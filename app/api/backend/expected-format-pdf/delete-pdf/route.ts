import { NextRequest, NextResponse } from 'next/server'

const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export async function DELETE(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url)
    const filename = searchParams.get('filename')
    if (!filename) {
      return NextResponse.json({ error: 'Missing filename' }, { status: 400 })
    }

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
      return new NextResponse(response.body, {
        status: response.status,
        headers: response.headers,
      })
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
