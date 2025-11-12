/**
 * Custom Hook for PDF Operations
 * Enterprise-level React hook for PDF download/delete operations
 */

import { useMutation, useQueryClient } from '@tanstack/react-query'
import logger from '../logger'

interface DeleteResponse {
  success: boolean
  message: string
}

export function usePDFOperations() {
  const queryClient = useQueryClient()

  const deletePDF = useMutation<DeleteResponse, Error, string>({
    mutationFn: async (filename: string) => {
      const response = await fetch(
        `/api/backend/expected-format-pdf/delete-pdf?filename=${encodeURIComponent(filename)}`,
        { method: 'DELETE' }
      )
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || errorData.error || 'Failed to delete PDF')
      }
      return response.json()
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['generated-pdfs'] })
      logger.info('PDF deleted successfully')
    },
    onError: (error) => {
      logger.error('Error deleting PDF', error)
    },
  })

  const deleteAllPDFs = useMutation<DeleteResponse, Error, void>({
    mutationFn: async () => {
      const response = await fetch('/api/backend/expected-format-pdf/delete-all-pdfs', {
        method: 'DELETE',
      })
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || errorData.error || 'Failed to delete all PDFs')
      }
      return response.json()
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['generated-pdfs'] })
      logger.info('All PDFs deleted successfully')
    },
    onError: (error) => {
      logger.error('Error deleting all PDFs', error)
    },
  })

  const downloadPDF = async (filename: string): Promise<void> => {
    try {
      const response = await fetch(
        `/api/backend/expected-format-pdf/download-pdf?filename=${encodeURIComponent(filename)}`
      )
      if (!response.ok) {
        throw new Error('Failed to download PDF')
      }

      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = filename
      document.body.appendChild(link)
      link.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(link)
      
      logger.info('PDF downloaded successfully', { filename })
    } catch (error) {
      logger.error('Download error', error as Error, { filename })
      throw error
    }
  }

  return {
    deletePDF: deletePDF.mutateAsync,
    deleteAllPDFs: deleteAllPDFs.mutateAsync,
    downloadPDF,
    isDeleting: deletePDF.isPending,
    isDeletingAll: deleteAllPDFs.isPending,
  }
}

