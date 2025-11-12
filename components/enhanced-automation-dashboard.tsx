'use client'

import { useState, useRef, useCallback, useMemo } from 'react'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { 
  Bot, Upload, CheckCircle, XCircle, AlertTriangle, Clock,
  Mail, FileText, Users, BarChart3, RefreshCw, Download, Trash2
} from 'lucide-react'
import logger from '@/lib/logger'
import { useExcelStatus } from '@/lib/hooks/useExcelStatus'
import { useGeneratedPDFs } from '@/lib/hooks/useGeneratedPDFs'
import { usePDFOperations } from '@/lib/hooks/usePDFOperations'

interface GeneratedPDF {
  filename: string
  file_size: number
  created: number
  file_path: string
}

interface PDFGenerationResult {
  success: boolean
  message: string
  generated_files: Array<{
    filename: string
    file_path: string
    user_name?: string
    emp_id?: string
    file_size?: number
  }>
  total_resources: number
  total_employees: number
  successful_generations: number
  filter_letter: string
  filter_emp_id?: string
  filter_billability?: string
  custom_condition_applied?: string
}

export function EnhancedAutomationDashboard() {
  const [isProcessing, setIsProcessing] = useState(false)
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [filterLetter, setFilterLetter] = useState('')
  const [filterEmpId, setFilterEmpId] = useState('')
  const [filterBillability, setFilterBillability] = useState('all')
  const [customCondition, setCustomCondition] = useState('')
  const [processingResult, setProcessingResult] = useState<PDFGenerationResult | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)
  const queryClient = useQueryClient()

  // Use custom hooks for data fetching
  const { data: excelStatus, refetch: refetchExcelStatus } = useExcelStatus()
  const { data: pdfs, isLoading: pdfsLoading, refetch: refetchPdfs } = useGeneratedPDFs()
  const { deletePDF, deleteAllPDFs, downloadPDF, isDeleting, isDeletingAll } = usePDFOperations()

  // Derived state from hooks
  const excelFileExists = excelStatus?.exists || false
  const excelFileInfo = excelStatus

  // Upload and generate PDFs mutation
  const uploadMutation = useMutation({
    mutationFn: async (formData: FormData) => {
      const controller = new AbortController()
      const timeoutId = setTimeout(() => controller.abort(), 180000) // 3 minute timeout
      
      try {
        const response = await fetch('/api/backend/timesheets/upload-excel', {
          method: 'POST',
          body: formData,
          signal: controller.signal,
        })
        clearTimeout(timeoutId)
        
        if (!response.ok) {
          let errorData: any
          try {
            errorData = await response.json()
          } catch {
            errorData = { error: `Server responded with status: ${response.status}` }
          }
          throw new Error(errorData.detail || errorData.error || 'Failed to upload and generate PDFs')
        }
        return response.json()
      } catch (error: any) {
        clearTimeout(timeoutId)
        if (error.name === 'AbortError') {
          throw new Error('Request timed out after 3 minutes. The file might be too large or the server is slow.')
        }
        throw error
      }
    },
    onSuccess: (data) => {
      setProcessingResult(data)
      refetchPdfs()
      setIsProcessing(false)
      refetchExcelStatus()
      logger.info('PDFs generated successfully', { count: data.total_resources })
    },
    onError: (error: any) => {
      logger.error('Upload error', error as Error)
      setIsProcessing(false)
      setProcessingResult(null)
      const errorMessage = error?.message || error?.detail || 'Failed to upload and generate PDFs'
      alert(`Error: ${errorMessage}`)
    },
  })

  // Memoized handlers for performance
  const handleFileSelect = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      setSelectedFile(file)
      logger.debug('File selected', { filename: file.name, size: file.size })
    }
  }, [])

  const handleUpload = useCallback(async () => {
    if (!selectedFile && !excelFileExists) {
      alert('Please upload an Excel file first or wait for existing file to be detected.')
      return
    }

    setIsProcessing(true)
    const formData = new FormData()
    if (selectedFile) {
      formData.append('file', selectedFile)
    }
    formData.append('filter_letter', filterLetter)
    formData.append('filter_emp_id', filterEmpId)
    formData.append('filter_billability', filterBillability)
    formData.append('custom_condition', customCondition)

    try {
      const result = await uploadMutation.mutateAsync(formData)
      logger.info('PDF generation completed', { result })
      refetchExcelStatus()
    } catch (error) {
      logger.error('Error generating PDFs', error as Error)
    }
  }, [selectedFile, excelFileExists, filterLetter, filterEmpId, filterBillability, customCondition, uploadMutation, refetchExcelStatus])

  const handleClearExcel = useCallback(async () => {
    if (!window.confirm('Are you sure you want to clear the uploaded Excel file? This will allow you to upload a new file.')) {
      return
    }
    
    try {
      const response = await fetch('/api/backend/timesheets/clear-excel', {
        method: 'DELETE',
      })
      if (!response.ok) throw new Error('Failed to clear Excel file')
      setSelectedFile(null)
      if (fileInputRef.current) {
        fileInputRef.current.value = ''
      }
      alert('Excel file cleared. You can now upload a new file.')
      refetchExcelStatus()
      logger.info('Excel file cleared')
    } catch (error) {
      logger.error('Error clearing Excel file', error as Error)
      alert('Failed to clear Excel file. Please try again.')
    }
  }, [refetchExcelStatus])

  const handleRefresh = useCallback(() => {
    refetchPdfs()
    refetchExcelStatus()
    logger.debug('Refreshed data')
  }, [refetchPdfs, refetchExcelStatus])

  const handleDownload = useCallback(async (filename: string) => {
    try {
      await downloadPDF(filename)
    } catch (error) {
      logger.error('Download error', error as Error, { filename })
      alert('Failed to download PDF')
    }
  }, [downloadPDF])

  const handleDeleteAll = useCallback(async () => {
    if (window.confirm('Are you sure you want to delete all generated PDFs? This action cannot be undone.')) {
      try {
        await deleteAllPDFs()
      } catch (error) {
        logger.error('Error deleting all PDFs', error as Error)
      }
    }
  }, [deleteAllPDFs])

  const handleDelete = useCallback(async (filename: string) => {
    if (confirm(`Are you sure you want to delete ${filename}? This action cannot be undone.`)) {
      try {
        await deletePDF(filename)
      } catch (error) {
        logger.error('Error deleting PDF', error as Error, { filename })
        alert('Failed to delete PDF. Please try again.')
      }
    }
  }, [deletePDF])

  // Memoized utility function
  const formatFileSize = useCallback((bytes: number) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }, [])

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-dark-gray dark:text-white">PDF Generation Dashboard</h2>
          <p className="text-medium-gray dark:text-light-gray">Upload Excel timesheets and generate individual PDFs</p>
        </div>
        <div className="flex items-center gap-2">
          {excelFileExists && (
            <Button
              onClick={handleClearExcel}
              variant="outline"
              size="sm"
              className="text-red hover:text-red/80"
            >
              <Trash2 className="h-4 w-4 mr-2" />
              Clear Excel
            </Button>
          )}
          <Button
            onClick={handleRefresh}
            variant="outline"
            size="sm"
            disabled={pdfsLoading}
          >
            <RefreshCw className={`h-4 w-4 mr-2 ${pdfsLoading ? 'animate-spin' : ''}`} />
            Refresh
          </Button>
        </div>
      </div>

      {/* Upload Section */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Upload className="h-5 w-5" />
            Upload Consolidated Excel Timesheet
          </CardTitle>
          <CardDescription>
            Upload your monthly Consolidated Excel timesheet file from your local PC. The system will automatically process it and generate individual Expected Format PDFs for each employee based on your filter conditions.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div>
              <Label htmlFor="file-upload">Select Excel File</Label>
              <Input
                id="file-upload"
                type="file"
                accept=".xlsx,.xls"
                onChange={handleFileSelect}
                ref={fileInputRef}
                className="mt-1"
              />
              {selectedFile && (
                <p className="text-sm text-medium-gray dark:text-light-gray mt-1">
                  Selected: {selectedFile.name} ({formatFileSize(selectedFile.size)})
                </p>
              )}
            </div>
            <div>
              <Label htmlFor="filter-letter">Filter by Name Starting With</Label>
              <Input
                id="filter-letter"
                type="text"
                value={filterLetter}
                onChange={(e) => setFilterLetter(e.target.value.toUpperCase())}
                maxLength={1}
                className="mt-1"
              />
              <p className="text-sm text-medium-gray dark:text-light-gray mt-1">
                Generate PDFs for resources whose first letter after comma in name starts with this letter (leave empty for all)
              </p>
            </div>
            <div>
              <Label htmlFor="filter-emp-id">Filter by EMP ID Starting With</Label>
              <Input
                id="filter-emp-id"
                type="text"
                value={filterEmpId}
                onChange={(e) => setFilterEmpId(e.target.value.toUpperCase())}
                className="mt-1"
              />
              <p className="text-sm text-gray-600 mt-1">
                Generate PDFs for resources whose EMP ID starts with this text (leave empty for all)
              </p>
            </div>
            <div>
              <Label htmlFor="filter-billability">Filter by Project Billability Type</Label>
              <select
                id="filter-billability"
                value={filterBillability}
                onChange={(e) => setFilterBillability(e.target.value)}
                className="mt-1 w-full px-3 py-2 border border-light-gray dark:border-medium-gray rounded-md bg-white dark:bg-dark-gray text-dark-gray dark:text-white focus:outline-none focus:ring-2 focus:ring-teal"
              >
                <option value="all">All Billability Types</option>
                <option value="billable">Billable Only</option>
                <option value="non-billable">Non-Billable Only</option>
              </select>
              <p className="text-sm text-gray-600 mt-1">
                Generate PDFs for resources with specific billability type
              </p>
            </div>
          </div>
          
          {/* Custom Condition Input - Full Width */}
          <div className="mt-4">
            <Label htmlFor="custom-condition">Custom Filter Condition (Advanced - Optional)</Label>
            <Input
              id="custom-condition"
              type="text"
              value={customCondition}
              onChange={(e) => setCustomCondition(e.target.value)}
              placeholder="e.g., User Name contains 'John' or Project == 'IT Project' or EMP ID starts with 'E'"
              className="mt-1"
            />
            <div className="mt-2 p-3 bg-teal/10 dark:bg-teal/20 border border-teal/30 dark:border-teal/40 rounded-lg">
              <p className="text-sm font-bold text-teal dark:text-teal mb-2">
                💡 Custom Filtering
              </p>
              <p className="text-sm text-teal-dark dark:text-teal mb-2">
                Filter by ANY column in your Excel file using flexible conditions:
              </p>
              <ul className="text-xs text-teal-dark dark:text-teal space-y-1 ml-4 list-disc">
                <li><code>Column Name contains 'value'</code> - Text contains (case-insensitive)</li>
                <li><code>Column Name starts with 'value'</code> - Text starts with</li>
                <li><code>Column Name == 'value'</code> - Exact match</li>
                <li><code>df['Column Name'] == 'value'</code> - Advanced pandas expression</li>
              </ul>
              <p className="text-xs text-teal-dark dark:text-teal/80 mt-2">
                <strong>Note:</strong> Custom condition overrides standard filters above. Leave empty to use standard filters. Column names are matched case-insensitively.
              </p>
              {excelFileInfo && excelFileInfo.columns && excelFileInfo.columns.length > 0 && (
                <div className="mt-3 p-2 bg-white dark:bg-gray-800 rounded border border-teal/30 dark:border-teal/40">
                  <p className="text-xs font-bold text-teal dark:text-teal mb-1">
                    📋 Available Columns ({excelFileInfo.columns.length}):
                  </p>
                  <div className="text-xs text-teal-dark dark:text-teal max-h-32 overflow-y-auto">
                    <div className="flex flex-wrap gap-1">
                      {excelFileInfo.columns.map((col: string, idx: number) => (
                        <code key={idx} className="px-1 py-0.5 bg-teal/10 dark:bg-teal/20 rounded text-xs">
                          {col}
                        </code>
                      ))}
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>

          <div className="flex gap-2">
            <Button
              onClick={handleUpload}
              disabled={(!selectedFile && !excelFileExists) || isProcessing}
              className="flex-1"
            >
              {isProcessing ? (
                <>
                  <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
                  Processing Excel & Generating PDFs...
                </>
              ) : (
                <>
                  <FileText className="h-4 w-4 mr-2" />
                  {selectedFile ? 'Upload & Generate PDFs' : excelFileExists ? 'Generate PDFs (Using Existing Excel)' : 'Upload Excel First'}
                </>
              )}
            </Button>
          </div>
          
          {excelFileExists && !selectedFile && (
            <div className="mt-2 p-3 bg-teal/10 dark:bg-teal/20 border border-teal/30 dark:border-teal/40 rounded-lg">
              <p className="text-sm text-teal-dark dark:text-teal">
                ℹ️ <strong>No file selected</strong> - Using existing Excel file. You can change filters and generate PDFs multiple times, or upload a new file to replace it.
              </p>
            </div>
          )}

          {/* Processing Result */}
          {processingResult && (
            <div className="mt-4 p-4 bg-teal/10 dark:bg-teal/20 border border-teal/30 dark:border-teal/40 rounded-lg">
              <div className="flex items-center gap-2 mb-2">
                <CheckCircle className="h-5 w-5 text-teal" />
                <span className="font-bold text-teal dark:text-teal">
                  Processing Complete!
                </span>
              </div>
              <p className="text-sm text-teal-dark dark:text-teal">
                {processingResult.message}
              </p>
              <div className="mt-2 text-sm text-teal dark:text-teal/80">
                <p>• Generated {processingResult.total_resources} PDFs</p>
                {processingResult.filter_letter && (
                  <p>• Name Filter: Starting with "{processingResult.filter_letter}"</p>
                )}
                {processingResult.filter_emp_id && (
                  <p>• EMP ID Filter: Starting with "{processingResult.filter_emp_id}"</p>
                )}
                {filterBillability !== 'all' && (
                  <p>• Billability Filter: {filterBillability === 'billable' ? 'Billable Only' : 'Non-Billable Only'}</p>
                )}
                {!processingResult.filter_letter && !processingResult.filter_emp_id && filterBillability === 'all' && (
                  <p>• No filters applied - All employees included</p>
                )}
                <p>• Using exact Excel template formatting</p>
              </div>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Generated PDFs Section */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <FileText className="h-5 w-5" />
            Generated PDFs
          </CardTitle>
          <CardDescription>
            Download or delete generated PDF files
          </CardDescription>
        </CardHeader>
        <CardContent>
          {pdfsLoading ? (
            <div className="flex items-center justify-center py-8">
              <RefreshCw className="h-6 w-6 animate-spin" />
              <span className="ml-2">Loading PDFs...</span>
            </div>
          ) : !pdfs || !pdfs.files || pdfs.files.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              <FileText className="h-12 w-12 mx-auto mb-4 text-gray-300" />
              <p>No PDFs generated yet</p>
              <p className="text-sm">Upload an Excel file to get started</p>
            </div>
          ) : (
            <div className="space-y-3">
              {pdfs.files.map((pdf: GeneratedPDF) => (
                <div
                  key={pdf.filename}
                  className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50"
                >
                  <div className="flex items-center gap-3">
                    <FileText className="h-8 w-8 text-red" />
                    <div>
                      <p className="font-medium">{pdf.filename}</p>
                      <p className="text-sm text-gray-500">
                        {formatFileSize(pdf.file_size)} • Created {new Date(pdf.created * 1000).toLocaleString()}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <Button
                      onClick={() => handleDownload(pdf.filename)}
                      size="sm"
                      variant="outline"
                    >
                      <Download className="h-4 w-4 mr-1" />
                      Download
                    </Button>
                    <Button
                      onClick={() => handleDelete(pdf.filename)}
                      size="sm"
                      variant="outline"
                      className="text-red-600 hover:text-red-700"
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              ))}
              
              {/* Delete All Button */}
              {pdfs.files.length > 0 && (
                <div className="mt-4 pt-4 border-t">
                  <Button
                    onClick={handleDeleteAll}
                    variant="destructive"
                    disabled={isDeletingAll}
                    className="w-full"
                  >
                    {isDeletingAll ? (
                      <>
                        <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
                        Deleting All PDFs...
                      </>
                    ) : (
                      <>
                        <Trash2 className="h-4 w-4 mr-2" />
                        Delete All PDFs ({pdfs.files.length})
                      </>
                    )}
                  </Button>
                </div>
              )}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Excel Template Information */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <FileText className="h-5 w-5" />
            Excel Template Information
          </CardTitle>
          <CardDescription>
            How the system processes your consolidated Excel file
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="bg-teal/10 dark:bg-teal/20 border border-teal/30 dark:border-teal/40 rounded-lg p-4">
              <h4 className="font-bold text-teal dark:text-teal mb-2">
                📋 Template Processing
              </h4>
              <div className="text-sm text-teal-dark dark:text-teal space-y-2">
                <p>• <strong>Template Source:</strong> Uses "Excel Template.xlsx" from the root directory</p>
                <p>• <strong>Data Mapping:</strong> Maps consolidated data to template columns automatically</p>
                <p>• <strong>Formatting:</strong> Preserves exact Excel formatting, fonts, colors, and layout</p>
                <p>• <strong>Individual PDFs:</strong> Creates separate PDF for each resource</p>
              </div>
            </div>
            
            <div className="bg-teal/10 dark:bg-teal/20 border border-teal/30 dark:border-teal/40 rounded-lg p-4">
              <h4 className="font-bold text-teal dark:text-teal mb-2">
                ✅ Expected Columns in Your Consolidated Excel
              </h4>
              <div className="text-sm text-teal-dark dark:text-teal grid grid-cols-2 gap-1">
                <p>• Date</p>
                <p>• Month</p>
                <p>• User Name</p>
                <p>• EMP ID</p>
                <p>• Email</p>
                <p>• Resource Category</p>
                <p>• Project</p>
                <p>• Task</p>
                <p>• Regular Time (Hours)</p>
                <p>• Timesheet Status</p>
                <p>• Project Manager</p>
                <p>• And other standard fields...</p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Processing Features */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Bot className="h-5 w-5" />
            Processing Features
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="text-center p-4 border rounded-lg">
              <CheckCircle className="h-8 w-8 text-teal mx-auto mb-2" />
              <h3 className="font-bold">Smart Excel Processing</h3>
              <p className="text-sm text-medium-gray">Automatically detects headers and maps data columns</p>
            </div>
            <div className="text-center p-4 border rounded-lg">
              <FileText className="h-8 w-8 text-teal mx-auto mb-2" />
              <h3 className="font-semibold">Excel Template PDF Generation</h3>
              <p className="text-sm text-gray-600">Preserves exact Excel formatting in PDF output</p>
            </div>
            <div className="text-center p-4 border rounded-lg">
              <Download className="h-8 w-8 text-purple-500 mx-auto mb-2" />
              <h3 className="font-semibold">Batch Processing</h3>
              <p className="text-sm text-gray-600">Filter by name and generate multiple PDFs at once</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
