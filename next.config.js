/** @type {import('next').NextConfig} */
// Get backend URL from environment variable (Azure-friendly)
const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL || process.env.BACKEND_URL || 'http://localhost:8000'

const nextConfig = {
  images: {
    domains: ['localhost'],
  },
  async rewrites() {
    return [
      {
        source: '/api/backend/:path*',
        destination: `${BACKEND_URL}/:path*`,
      },
      {
        source: '/api/jarvis/:path*',
        destination: `${BACKEND_URL}/api/jarvis/:path*`,
      },
    ]
  },
}

module.exports = nextConfig
