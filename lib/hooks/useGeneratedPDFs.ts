/**
 * Custom Hook for Generated PDFs
 * Enterprise-level React hook for PDF list management
 */

import { useQuery } from '@tanstack/react-query'
import logger from '../logger'

interface GeneratedPDF {
  filename: string
  file_size: number
  created: number
  file_path: string
}

interface PDFListResponse {
  files: GeneratedPDF[]
  count: number
  output_directory: string
  format?: string
}

export function useGeneratedPDFs() {
  return useQuery<PDFListResponse>({
    queryKey: ['generated-pdfs'],
    queryFn: async () => {
      try {
        const response = await fetch('/api/backend/expected-format-pdf/list-generated-pdfs')
        if (!response.ok) {
          logger.warn('Failed to fetch PDFs', { status: response.status })
          return { files: [], count: 0, output_directory: '' }
        }
        const data = await response.json()
        logger.debug('Fetched PDFs data', { count: data.count || data.files?.length })
        return {
          files: data.files || [],
          count: data.count || (data.files ? data.files.length : 0),
          output_directory: data.output_directory || '',
          format: data.format,
        }
      } catch (error) {
        logger.error('Error fetching PDFs', error as Error)
        return { files: [], count: 0, output_directory: '' }
      }
    },
    refetchInterval: 10000, // Refresh every 10 seconds
    staleTime: 5000, // Consider data stale after 5 seconds
  })
}

