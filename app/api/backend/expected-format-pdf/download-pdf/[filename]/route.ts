import { NextRequest, NextResponse } from 'next/server'

const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export async function GET(
  request: NextRequest,
  { params }: { params: { filename: string } }
) {
  try {
    const { filename } = params
    // Forward the filename exactly as received to avoid double-encoding issues
    const backendResponse = await fetch(
      `${BACKEND_URL}/api/expected-format-pdf/download-pdf/${filename}`,
      { method: 'GET' }
    )

    if (!backendResponse.ok) {
      // Proxy backend status and body as-is for clarity
      return new NextResponse(backendResponse.body, {
        status: backendResponse.status,
        headers: backendResponse.headers,
      })
    }

    const headers = new Headers(backendResponse.headers)
    const contentType = headers.get('content-type') || 'application/pdf'
    headers.set('Content-Type', contentType)
    // Best-effort: if filename is percent-encoded, leave as-is
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



