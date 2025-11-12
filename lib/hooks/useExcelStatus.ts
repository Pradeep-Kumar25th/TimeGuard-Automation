/**
 * Custom Hook for Excel Status
 * Enterprise-level React hook for Excel file status management
 */

import { useQuery } from '@tanstack/react-query'
import logger from '../logger'

interface ExcelStatus {
  success: boolean
  exists: boolean
  rows?: number
  columns?: string[]
  columns_count?: number
  has_user_name?: boolean
  has_emp_id?: boolean
  message?: string
  error?: string
}

export function useExcelStatus() {
  return useQuery<ExcelStatus>({
    queryKey: ['excel-status'],
    queryFn: async () => {
      try {
        const response = await fetch('/api/backend/timesheets/excel-status')
        if (!response.ok) {
          logger.warn('Excel status check failed', { status: response.status })
          return { success: false, exists: false }
        }
        const data = await response.json()
        logger.info('Excel status retrieved', { exists: data.exists, rows: data.rows })
        return data
      } catch (error) {
        logger.error('Error checking Excel status', error as Error)
        return { success: false, exists: false }
      }
    },
    refetchInterval: 5000, // Check every 5 seconds
    staleTime: 3000, // Consider data stale after 3 seconds
  })
}

