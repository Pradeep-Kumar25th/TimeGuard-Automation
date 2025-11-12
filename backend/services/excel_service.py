"""
Excel Processing Service
Handles Excel file operations, validation, and data loading
"""

import os
import tempfile
import logging
from typing import Dict, Optional, Tuple
import pandas as pd
from fastapi import HTTPException, UploadFile

from settings import settings
from expected_format_pdf_generator import detect_employee_identifier_columns

logger = logging.getLogger(__name__)


class ExcelService:
    """Service for Excel file operations and validation"""
    
    # Standard column names for consistency
    STANDARD_NAME_COL = 'User Name'
    STANDARD_ID_COL = 'EMP ID'
    
    def __init__(self):
        self.data_dir = settings.data_dir
        os.makedirs(self.data_dir, exist_ok=True)
        self.consolidated_path = os.path.join(self.data_dir, "Consolidated.xlsx")
    
    async def validate_file(self, file: UploadFile) -> Tuple[bytes, int]:
        """
        Validate uploaded Excel file.
        
        Args:
            file: Uploaded file object
            
        Returns:
            Tuple of (file_content, file_size)
            
        Raises:
            HTTPException: If file validation fails
        """
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        # Validate file extension
        if not file.filename.endswith(('.xlsx', '.xls')):
            raise HTTPException(
                status_code=400, 
                detail="Only Excel files (.xlsx, .xls) are allowed"
            )
        
        # Read and validate file size (await async read)
        content = await file.read()
        file_size = len(content)
        
        if file_size > settings.max_file_size_bytes:
            raise HTTPException(
                status_code=400,
                detail=f"File size must be less than {settings.max_file_size_mb}MB"
            )
        
        if file_size == 0:
            raise HTTPException(status_code=400, detail="File is empty")
        
        return content, file_size
    
    def read_excel_file(self, file_path: str) -> Optional[pd.DataFrame]:
        """
        Read Excel file with multiple header row attempts.
        
        Args:
            file_path: Path to Excel file
            
        Returns:
            DataFrame if successful, None otherwise
        """
        for header_row in [0, 1, 2]:  # Try rows 1, 2, 3 as headers
            try:
                df = pd.read_excel(file_path, header=header_row)
                df = df.dropna(how='all').reset_index(drop=True)
                
                if not df.empty:
                    # Validate that required columns exist
                    employee_cols = detect_employee_identifier_columns(df)
                    if employee_cols['name_found'] and employee_cols['id_found']:
                        return df
            except Exception as e:
                logger.debug(f"Failed to read with header row {header_row}: {e}")
                continue
        
        return None
    
    async def process_uploaded_file(self, file: UploadFile) -> pd.DataFrame:
        """
        Process and save uploaded Excel file.
        
        Args:
            file: Uploaded file object
            
        Returns:
            Processed DataFrame
            
        Raises:
            HTTPException: If processing fails
        """
        # Validate file
        content, file_size = await self.validate_file(file)
        
        # Create temporary file
        temp_file_path = None
        try:
            with tempfile.NamedTemporaryFile(
                delete=False, 
                suffix=f".{file.filename.split('.')[-1]}"
            ) as temp_file:
                temp_file.write(content)
                temp_file_path = temp_file.name
            
            # Read Excel file
            df = self.read_excel_file(temp_file_path)
            
            if df is None or df.empty:
                raise HTTPException(
                    status_code=400,
                    detail="Could not read Excel file or no valid data found"
                )
            
            # Validate required columns
            self._validate_employee_columns(df)
            
            # Standardize column names
            df = self._standardize_column_names(df)
            
            # Save to consolidated path
            df.to_excel(self.consolidated_path, index=False)
            logger.info(f"✅ Saved Excel as Consolidated.xlsx at {self.consolidated_path}")
            
            return df
            
        finally:
            # Clean up temporary file
            if temp_file_path and os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
    
    def load_consolidated_file(self) -> pd.DataFrame:
        """
        Load existing Consolidated.xlsx file.
        
        Returns:
            DataFrame with loaded data
            
        Raises:
            HTTPException: If file doesn't exist or is invalid
        """
        if not os.path.exists(self.consolidated_path):
            raise HTTPException(
                status_code=400,
                detail="No Excel file available. Please upload an Excel file first."
            )
        
        logger.info(f"📂 Loading data from Consolidated.xlsx")
        df = pd.read_excel(self.consolidated_path)
        df = df.dropna(how='all').reset_index(drop=True)
        
        if df.empty:
            raise HTTPException(
                status_code=400,
                detail="Consolidated.xlsx is empty or no valid data found"
            )
        
        # Validate required columns
        self._validate_employee_columns(df)
        
        # Standardize column names
        df = self._standardize_column_names(df)
        
        logger.info(f"📊 Loaded {len(df)} rows from Consolidated.xlsx")
        return df
    
    def _validate_employee_columns(self, df: pd.DataFrame) -> None:
        """
        Validate that DataFrame contains required employee identifier columns.
        
        Args:
            df: DataFrame to validate
            
        Raises:
            HTTPException: If required columns are missing
        """
        employee_cols = detect_employee_identifier_columns(df)
        
        if not employee_cols['name_found'] or not employee_cols['id_found']:
            available_cols = ', '.join(list(df.columns)[:20])
            available_similar_name = [
                col for col in df.columns 
                if 'name' in str(col).lower()
            ][:5]
            available_similar_id = [
                col for col in df.columns 
                if 'id' in str(col).lower() or 'number' in str(col).lower()
            ][:5]
            
            error_msg = "Excel must contain employee name and ID columns. "
            if available_similar_name:
                error_msg += f"Similar name columns found: {', '.join(available_similar_name)}. "
            if available_similar_id:
                error_msg += f"Similar ID columns found: {', '.join(available_similar_id)}. "
            error_msg += f"Available columns: {available_cols}"
            
            raise HTTPException(status_code=400, detail=error_msg)
    
    def _standardize_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Standardize employee identifier column names.
        
        Args:
            df: DataFrame to standardize
            
        Returns:
            DataFrame with standardized column names
        """
        employee_cols = detect_employee_identifier_columns(df)
        name_col_actual = employee_cols['name_column']
        id_col_actual = employee_cols['id_column']
        
        rename_map = {}
        if name_col_actual != self.STANDARD_NAME_COL:
            rename_map[name_col_actual] = self.STANDARD_NAME_COL
            logger.info(
                f"🔄 Renaming column '{name_col_actual}' to '{self.STANDARD_NAME_COL}'"
            )
        
        if id_col_actual != self.STANDARD_ID_COL:
            rename_map[id_col_actual] = self.STANDARD_ID_COL
            logger.info(
                f"🔄 Renaming column '{id_col_actual}' to '{self.STANDARD_ID_COL}'"
            )
        
        if rename_map:
            df = df.rename(columns=rename_map)
            logger.info(f"✅ Standardized column names: {rename_map}")
        
        return df
    
    def get_excel_status(self) -> Dict:
        """
        Get status of Consolidated.xlsx file.
        
        Returns:
            Dictionary with file status information
        """
        if not os.path.exists(self.consolidated_path):
            return {
                "success": True,
                "exists": False,
                "message": "No Excel file uploaded"
            }
        
        try:
            df = pd.read_excel(self.consolidated_path)
            columns_list = [str(col) for col in df.columns]
            employee_cols = detect_employee_identifier_columns(df)
            
            return {
                "success": True,
                "exists": True,
                "rows": len(df),
                "columns": columns_list,
                "columns_count": len(columns_list),
                "has_user_name": employee_cols['name_found'],
                "has_emp_id": employee_cols['id_found']
            }
        except Exception as e:
            return {
                "success": False,
                "exists": True,
                "error": f"Error reading file: {str(e)}"
            }
    
    def clear_consolidated_file(self) -> Dict:
        """
        Clear the Consolidated.xlsx file.
        
        Returns:
            Dictionary with operation result
        """
        if os.path.exists(self.consolidated_path):
            os.remove(self.consolidated_path)
            logger.info(f"✅ Deleted Consolidated.xlsx at {self.consolidated_path}")
            return {"success": True, "message": "Excel file cleared successfully"}
        else:
            return {"success": True, "message": "No Excel file to clear"}


