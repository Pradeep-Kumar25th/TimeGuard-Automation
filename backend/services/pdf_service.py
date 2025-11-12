"""
PDF Generation Service
Handles PDF generation business logic
"""

import logging
from typing import Dict, Any, Optional
import pandas as pd

from expected_format_pdf_generator import ExpectedFormatPDFGenerator

logger = logging.getLogger(__name__)


class PDFService:
    """Service for PDF generation operations"""
    
    def __init__(self):
        self.generator = ExpectedFormatPDFGenerator()
    
    def generate_pdfs(
        self,
        df: pd.DataFrame,
        name_filter: Optional[str] = None,
        emp_id_filter: Optional[str] = None,
        billability_filter: Optional[str] = None,
        custom_condition: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate PDFs from filtered DataFrame.
        
        Args:
            df: Filtered DataFrame
            name_filter: Filter by name starting with letter
            emp_id_filter: Filter by EMP ID starting with text
            billability_filter: Filter by billability type
            custom_condition: Custom condition string (if applied)
            
        Returns:
            Dictionary with generation results
        """
        logger.info("🎯 Generating PDFs using ExpectedFormatPDFGenerator")
        logger.info(
            f"🔍 Filters: name={name_filter}, emp_id={emp_id_filter}, "
            f"billability={billability_filter}, "
            f"custom_condition={custom_condition if custom_condition else 'None'}"
        )
        logger.info(f"📊 DataFrame shape after filtering: {df.shape} (rows, columns)")
        
        # If custom condition was applied, don't apply standard filters
        if custom_condition and custom_condition.strip():
            result = self.generator.generate_all_pdfs(
                df,
                name_filter=None,
                emp_id_filter=None,
                billability_filter=None
            )
        else:
            result = self.generator.generate_all_pdfs(
                df,
                name_filter=name_filter,
                emp_id_filter=emp_id_filter,
                billability_filter=billability_filter
            )
        
        return self._format_response(result, custom_condition)
    
    def _format_response(
        self, 
        result: Dict[str, Any], 
        custom_condition: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Format PDF generation response.
        
        Args:
            result: Raw generation result
            custom_condition: Custom condition string if applied
            
        Returns:
            Formatted response dictionary
        """
        if result.get("success"):
            message = result.get("message", "PDFs generated successfully")
            
            # Enhance message for custom conditions
            if custom_condition and custom_condition.strip():
                if "custom condition applied" not in message.lower():
                    message = (
                        f"Generated {result.get('successful_generations', 0)}/"
                        f"{result.get('total_employees', 0)} Expected Format PDFs "
                        f"successfully (custom condition: '{custom_condition}')"
                    )
            
            return {
                "success": True,
                "message": message,
                "generated_files": result.get("generated_files", []),
                "total_employees": result.get("total_employees", 0),
                "successful_generations": result.get("successful_generations", 0),
                "failed_generations": result.get("failed_generations", 0),
                "total_resources": len(result.get("generated_files", [])),
                "custom_condition_applied": (
                    custom_condition.strip() 
                    if custom_condition and custom_condition.strip() 
                    else ""
                ),
            }
        else:
            return {
                "success": False,
                "message": result.get("message", "Failed to generate PDFs"),
                "error": result.get("error", "Unknown error"),
                "generated_files": [],
                "total_employees": 0,
                "successful_generations": 0,
                "failed_generations": 0,
                "total_resources": 0,
                "custom_condition_applied": "",
            }

