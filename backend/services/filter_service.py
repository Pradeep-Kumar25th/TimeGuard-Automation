"""
Filter Service
Handles data filtering logic for Excel data
"""

import logging
from typing import Optional, Dict, Any
import pandas as pd
from fastapi import HTTPException

from expected_format_pdf_generator import find_column_dynamic

logger = logging.getLogger(__name__)


class FilterService:
    """Service for filtering Excel data"""
    
    def __init__(self):
        self.initial_rows = 0
    
    def apply_custom_condition(
        self, 
        df: pd.DataFrame, 
        custom_condition: str
    ) -> pd.DataFrame:
        """
        Apply custom filter condition to DataFrame.
        
        Args:
            df: DataFrame to filter
            custom_condition: Custom condition string
            
        Returns:
            Filtered DataFrame
            
        Raises:
            HTTPException: If condition is invalid or results in empty DataFrame
        """
        if not custom_condition.strip():
            return df
        
        # Store initial row count
        self.initial_rows = len(df)
        
        logger.info(f"🔍 Applying custom condition: {custom_condition}")
        logger.info(f"📋 Available columns in Excel: {list(df.columns)}")
        
        try:
            condition_lower = custom_condition.lower()
            
            # Handle "contains" condition
            if " contains " in condition_lower:
                df = self._apply_contains_filter(df, custom_condition)
            
            # Handle "starts with" condition
            elif " starts with " in condition_lower:
                df = self._apply_starts_with_filter(df, custom_condition)
            
            # Handle "==" condition
            elif " == " in custom_condition:
                df = self._apply_equals_filter(df, custom_condition)
            
            # Try pandas query syntax
            else:
                df = self._apply_pandas_query(df, custom_condition)
            
            if df.empty:
                raise HTTPException(
                    status_code=400,
                    detail=f"Custom condition '{custom_condition}' resulted in 0 rows. "
                           f"No PDFs will be generated."
                )
            
            return df
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"❌ Error applying custom condition: {e}")
            raise HTTPException(
                status_code=400,
                detail=f"Failed to apply custom condition: {e}"
            )
    
    def _apply_contains_filter(
        self, 
        df: pd.DataFrame, 
        condition: str
    ) -> pd.DataFrame:
        """Apply 'contains' filter condition"""
        parts = condition.split(" contains ", 1)
        if len(parts) != 2:
            raise HTTPException(
                status_code=400,
                detail="Invalid 'contains' condition format. Use: 'Column Name contains value'"
            )
        
        col_name = parts[0].strip()
        value = parts[1].strip().strip('"\'').strip()
        actual_col = find_column_dynamic(col_name, df.columns)
        
        if not actual_col:
            raise HTTPException(
                status_code=400,
                detail=f"Column '{col_name}' not found. Available columns: {', '.join(list(df.columns))}"
            )
        
        rows_before = len(df)
        df = df[df[actual_col].astype(str).str.contains(value, case=False, na=False)]
        logger.info(
            f"✅ Applied 'contains' filter: {actual_col} contains '{value}' - "
            f"{rows_before} → {len(df)} rows (custom condition)"
        )
        return df
    
    def _apply_starts_with_filter(
        self, 
        df: pd.DataFrame, 
        condition: str
    ) -> pd.DataFrame:
        """Apply 'starts with' filter condition"""
        parts = condition.split(" starts with ", 1)
        if len(parts) != 2:
            raise HTTPException(
                status_code=400,
                detail="Invalid 'starts with' condition format. Use: 'Column Name starts with value'"
            )
        
        col_name = parts[0].strip()
        value = parts[1].strip().strip('"\'').strip()
        actual_col = find_column_dynamic(col_name, df.columns)
        
        if not actual_col:
            raise HTTPException(
                status_code=400,
                detail=f"Column '{col_name}' not found. Available columns: {', '.join(list(df.columns))}"
            )
        
        rows_before = len(df)
        df = df[df[actual_col].astype(str).str.startswith(value, na=False)]
        logger.info(
            f"✅ Applied 'starts with' filter: {actual_col} starts with '{value}' - "
            f"{rows_before} → {len(df)} rows (custom condition)"
        )
        return df
    
    def _apply_equals_filter(
        self, 
        df: pd.DataFrame, 
        condition: str
    ) -> pd.DataFrame:
        """Apply 'equals' filter condition"""
        parts = condition.split(" == ", 1)
        if len(parts) != 2:
            raise HTTPException(
                status_code=400,
                detail="Invalid 'equals' condition format. Use: 'Column Name == value'"
            )
        
        col_name = parts[0].strip()
        value = parts[1].strip().strip('"\'').strip()
        actual_col = find_column_dynamic(col_name, df.columns)
        
        if not actual_col:
            raise HTTPException(
                status_code=400,
                detail=f"Column '{col_name}' not found. Available columns: {', '.join(list(df.columns))}"
            )
        
        rows_before = len(df)
        df = df[df[actual_col].astype(str) == value]
        logger.info(
            f"✅ Applied 'equals' filter: {actual_col} == '{value}' - "
            f"{rows_before} → {len(df)} rows (custom condition)"
        )
        return df
    
    def _apply_pandas_query(
        self, 
        df: pd.DataFrame, 
        condition: str
    ) -> pd.DataFrame:
        """Apply pandas query syntax"""
        try:
            rows_before = len(df)
            df = df.query(condition)
            logger.info(
                f"✅ Applied pandas query: {condition} - "
                f"{rows_before} → {len(df)} rows (custom condition)"
            )
            return df
        except Exception as query_error:
            raise HTTPException(
                status_code=400,
                detail=f"Could not parse custom condition '{condition}'. "
                       f"Try formats like: 'User Name contains John' or "
                       f"'EMP ID starts with E' or 'Project == IT Project'. "
                       f"Error: {query_error}"
            )
    
    def prepare_standard_filters(
        self,
        filter_letter: str,
        filter_emp_id: str,
        filter_billability: str
    ) -> Dict[str, Optional[str]]:
        """
        Prepare standard filter parameters.
        
        Args:
            filter_letter: Filter by name starting with letter
            filter_emp_id: Filter by EMP ID starting with text
            filter_billability: Filter by billability type
            
        Returns:
            Dictionary with normalized filter values
        """
        return {
            'name_filter': (
                filter_letter.strip().upper() 
                if filter_letter and filter_letter.strip() 
                else None
            ),
            'emp_id_filter': (
                filter_emp_id.strip().upper() 
                if filter_emp_id and filter_emp_id.strip() 
                else None
            ),
            'billability_filter': (
                filter_billability.strip().lower() 
                if filter_billability and filter_billability.strip() != "all" 
                else None
            )
        }

