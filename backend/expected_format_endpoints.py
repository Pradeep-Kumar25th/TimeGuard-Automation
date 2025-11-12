"""
FastAPI endpoints for Expected Format PDF Generator
"""

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse
import pandas as pd
import os
import logging
from pathlib import Path
from expected_format_pdf_generator import ExpectedFormatPDFGenerator, detect_employee_identifier_columns
from settings import settings
from utils.file_utils import validate_filename, sanitize_path

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/expected-format-pdf", tags=["Expected Format PDF Generation"])

# Initialize generator
expected_format_generator = ExpectedFormatPDFGenerator()

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "Expected Format PDF Generator is ready",
        "output_dir_exists": os.path.exists(expected_format_generator.output_dir),
        "method": "Expected Format ReportLab",
        "page_size": f"{expected_format_generator.page_width:.1f} x {expected_format_generator.page_height:.1f} points",
        "total_columns": len(expected_format_generator.column_widths)
    }

@router.post("/generate-single-timesheet")
async def generate_single_timesheet(
    user_name: str = Query(..., min_length=1, max_length=200, description="Employee name"),
    emp_id: str = Query(..., min_length=1, max_length=50, description="Employee ID")
):
    """Generate Expected Format PDF for a single employee"""
    try:
        # Load data from Consolidated.xlsx using settings
        consolidated_path = os.path.join(settings.data_dir, "Consolidated.xlsx")
        if not os.path.exists(consolidated_path):
            raise HTTPException(status_code=404, detail="Consolidated.xlsx not found")
        
        # Read data
        df = pd.read_excel(consolidated_path)
        
        # Dynamically detect employee identifier columns
        employee_cols = detect_employee_identifier_columns(df)
        if not employee_cols['name_found'] or not employee_cols['id_found']:
            raise HTTPException(status_code=400, detail="Could not detect employee identifier columns in Excel file")
        
        # Filter for specific employee using dynamically detected columns
        name_col = employee_cols['name_column']
        id_col = employee_cols['id_column']
        employee_data = df[(df[name_col] == user_name) & (df[id_col] == emp_id)]
        
        if employee_data.empty:
            raise HTTPException(status_code=404, detail=f"No data found for {user_name} ({emp_id})")
        
        # Generate PDF
        result = expected_format_generator.generate_single_pdf(employee_data, user_name, emp_id)
        
        if result["success"]:
            return result
        else:
            raise HTTPException(status_code=500, detail=result.get("error", "PDF generation failed"))
            
    except Exception as e:
        logger.error(f"❌ Error in generate_single_timesheet: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-all-timesheets")
async def generate_all_timesheets(
    name_filter: str = Query(None, description="Filter by names starting with this letter (e.g., 'A')")
):
    """Generate Expected Format PDFs for all employees, optionally filtered by name"""
    try:
        # Load data from Consolidated.xlsx using settings
        consolidated_path = os.path.join(settings.data_dir, "Consolidated.xlsx")
        if not os.path.exists(consolidated_path):
            raise HTTPException(status_code=404, detail="Consolidated.xlsx not found")
        
        # Read data
        df = pd.read_excel(consolidated_path)
        
        # Generate all PDFs with optional filter
        result = expected_format_generator.generate_all_pdfs(df, name_filter=name_filter)
        
        return result
            
    except Exception as e:
        logger.error(f"❌ Error in generate_all_timesheets: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list-generated-pdfs")
async def list_generated_pdfs():
    """List all generated Expected Format PDF files"""
    try:
        output_dir = expected_format_generator.output_dir
        
        if not os.path.exists(output_dir):
            return {"files": [], "count": 0}
        
        files = []
        for filename in os.listdir(output_dir):
            if filename.endswith('.pdf'):
                file_path = os.path.join(output_dir, filename)
                file_size = os.path.getsize(file_path)
                files.append({
                    "filename": filename,
                    "file_path": file_path,
                    "file_size": file_size,
                    "created": os.path.getctime(file_path)
                })
        
        # Sort by creation time (newest first)
        files.sort(key=lambda x: x["created"], reverse=True)
        
        return {
            "files": files,
            "count": len(files),
            "output_directory": output_dir,
            "format": "Expected Format (matching Expected.pdf)"
        }
        
    except Exception as e:
        logger.error(f"❌ Error listing PDFs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/download-pdf/{filename}")
async def download_pdf(filename: str):
    """Download a specific Expected Format PDF file"""
    try:
        # Validate and sanitize filename
        safe_filename = validate_filename(filename, allowed_extensions=['.pdf'])
        
        # Build and sanitize file path
        output_dir = expected_format_generator.output_dir
        file_path = os.path.join(output_dir, safe_filename)
        file_path_resolved = sanitize_path(file_path, output_dir)
        
        if not file_path_resolved.exists():
            raise HTTPException(status_code=404, detail="PDF file not found")
        
        return FileResponse(
            path=str(file_path_resolved),
            filename=safe_filename,
            media_type='application/pdf'
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error downloading PDF: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/delete-pdf/{filename}")
async def delete_pdf(filename: str):
    """Delete a specific Expected Format PDF file"""
    try:
        # Validate and sanitize filename
        safe_filename = validate_filename(filename, allowed_extensions=['.pdf'])
        
        # Build and sanitize file path
        output_dir = expected_format_generator.output_dir
        file_path = os.path.join(output_dir, safe_filename)
        file_path_resolved = sanitize_path(file_path, output_dir)
        
        if not file_path_resolved.exists():
            raise HTTPException(status_code=404, detail="PDF file not found")
        
        # Delete file
        file_path_resolved.unlink()
        logger.info(f"✅ Deleted PDF: {safe_filename}")
        
        return {
            "success": True,
            "message": f"Expected Format PDF {safe_filename} deleted successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error deleting PDF: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/delete-all-pdfs")
async def delete_all_pdfs():
    """Delete all Expected Format PDF files"""
    try:
        output_dir = expected_format_generator.output_dir
        
        if not os.path.exists(output_dir):
            return {
                "success": True,
                "message": "No PDF files to delete",
                "deleted_count": 0
            }
        
        deleted_count = 0
        deleted_files = []
        
        # Get all PDF files in the output directory
        for filename in os.listdir(output_dir):
            if filename.endswith('.pdf'):
                file_path = os.path.join(output_dir, filename)
                try:
                    os.remove(file_path)
                    deleted_count += 1
                    deleted_files.append(filename)
                    logger.info(f"✅ Deleted PDF: {filename}")
                except Exception as e:
                    logger.error(f"❌ Error deleting {filename}: {e}")
        
        return {
            "success": True,
            "message": f"Successfully deleted {deleted_count} PDF files",
            "deleted_count": deleted_count,
            "deleted_files": deleted_files
        }
        
    except Exception as e:
        logger.error(f"❌ Error deleting all PDFs: {e}")
        raise HTTPException(status_code=500, detail=str(e))
