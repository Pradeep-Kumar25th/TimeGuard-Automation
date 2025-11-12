import { NextRequest, NextResponse } from 'next/server'

const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url)
    const filename = searchParams.get('filename')
    if (!filename) {
      return NextResponse.json({ error: 'Missing filename' }, { status: 400 })
    }

    const backendResponse = await fetch(
      `${BACKEND_URL}/api/expected-format-pdf/download-pdf/${filename}`,
      { method: 'GET' }
    )

    if (!backendResponse.ok) {
      return new NextResponse(backendResponse.body, {
        status: backendResponse.status,
        headers: backendResponse.headers,
      })
    }

    const headers = new Headers(backendResponse.headers)
    headers.set('Content-Disposition', `attachment; filename="${filename}"`)

    return new NextResponse(backendResponse.body, {
      status: 200,
      headers,
    })
  } catch (error: any) {
    console.error('Error downloading PDF:', error)
    return NextResponse.json(
      { error: error.message || 'Failed to download PDF' },
      { status: 500 }
    )
  }
}


