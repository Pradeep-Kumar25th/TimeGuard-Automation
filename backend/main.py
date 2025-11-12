"""
TimeGuard AI API - Automation Module Only
This is a minimal FastAPI application supporting only the Automation tab functionality.
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import uvicorn
import traceback
import os
import tempfile
import uuid
from datetime import datetime
import pandas as pd
import logging

from expected_format_endpoints import router as expected_format_router
from settings import settings
from services.excel_service import ExcelService
from services.filter_service import FilterService
from services.pdf_service import PDFService

# Configure enterprise-level logging
from utils.logging_utils import setup_logging, get_logger

setup_logging(
    log_level=settings.log_level,
    log_file=settings.log_file if settings.log_file else None
)
logger = get_logger(__name__)

app = FastAPI(title="TimeGuard AI API - Automation Module", version="1.0.0")

# Global exception handler to ALWAYS return JSON
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler that ALWAYS returns JSON, even on errors"""
    # Generate correlation ID for error tracking
    correlation_id = str(uuid.uuid4())
    
    # Log error with correlation ID and context
    logger.error(
        f"Error [Correlation ID: {correlation_id}] while handling {request.url}: {exc}",
        exc_info=True,
        extra={
            "correlation_id": correlation_id,
            "url": str(request.url),
            "method": request.method,
            "timestamp": datetime.utcnow().isoformat(),
            "environment": settings.environment
        }
    )
    
    # In production, don't expose internal error details
    if settings.environment == "production":
        error_message = "An internal server error occurred. Please contact support."
    else:
        error_message = str(exc)
    
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": error_message,
            "message": "An internal server error occurred",
            "correlation_id": correlation_id,
            "type": "server_error"
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors with JSON response"""
    logger.error(f"❌ Validation error on {request.url}: {exc}")
    
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": "Validation error",
            "message": "Invalid request data",
            "details": exc.errors(),
            "type": "validation_error"
        }
    )

# CORS middleware - Use settings for Azure deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
excel_service = ExcelService()
filter_service = FilterService()
pdf_service = PDFService()

# Basic endpoints
@app.get("/")
async def root():
    return {"message": "TimeGuard AI API - Automation Module is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# PDF Generation Endpoint - Core Automation functionality
@app.post("/api/timesheets/upload-excel")
async def upload_excel_timesheet(
    file: UploadFile = File(None),
    filter_letter: str = Form(""),
    filter_emp_id: str = Form(""),
    filter_billability: str = Form("all"),
    custom_condition: str = Form("")
):
    """
    Upload Excel timesheet and generate PDFs.
    
    File is optional - if not provided, uses existing Consolidated.xlsx.
    Supports standard filters and custom conditions.
    """
    try:
        # Step 1: Load or process Excel file
        if file is not None and file.filename:
            df = await excel_service.process_uploaded_file(file)
        else:
            df = excel_service.load_consolidated_file()
        
        # Step 2: Store initial row count for tracking
        initial_rows = len(df)
        
        # Step 3: Apply custom condition if provided
        if custom_condition.strip():
            df = filter_service.apply_custom_condition(df, custom_condition)
        
        # Step 4: Prepare standard filters
        filters = filter_service.prepare_standard_filters(
            filter_letter, filter_emp_id, filter_billability
        )
        
        # Step 5: Generate PDFs
        result = pdf_service.generate_pdfs(
            df=df,
            name_filter=filters['name_filter'],
            emp_id_filter=filters['emp_id_filter'],
            billability_filter=filters['billability_filter'],
            custom_condition=custom_condition if custom_condition.strip() else None
        )
        
        # Step 6: Add filter information to response
        result.update({
            "filter_letter": filter_letter.upper().strip() if filter_letter and filter_letter.strip() else "",
            "filter_emp_id": filter_emp_id.upper().strip() if filter_emp_id and filter_emp_id.strip() else "",
            "filter_billability": filter_billability.strip() if filter_billability and filter_billability.strip() != "all" else "",
        })
        
        return JSONResponse(content=result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error processing Excel file: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing Excel file: {str(e)}")

@app.delete("/api/timesheets/clear-excel")
async def clear_uploaded_excel():
    """Clear the uploaded Consolidated.xlsx file"""
    try:
        result = excel_service.clear_consolidated_file()
        return JSONResponse(content=result)
    except Exception as e:
        logger.error(f"❌ Error clearing Excel file: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error clearing Excel file: {str(e)}")

@app.get("/api/timesheets/excel-status")
async def get_excel_status():
    """Check if Consolidated.xlsx exists and return its status including all column names"""
    try:
        result = excel_service.get_excel_status()
        return JSONResponse(content=result)
    except Exception as e:
        logger.error(f"❌ Error checking Excel status: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error checking Excel status: {str(e)}")

# Add Expected Format PDF endpoints router
app.include_router(expected_format_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

