"""
Expected Format PDF Generator
Generates PDFs exactly matching the Expected.pdf format
"""

import pandas as pd
import os
import logging
from datetime import datetime
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import io
import re

# Import settings if available, otherwise use defaults
try:
    from settings import settings
    USE_SETTINGS = True
except ImportError:
    USE_SETTINGS = False
    logger = logging.getLogger(__name__)
    logger.warning("Settings module not found, using default paths")

logger = logging.getLogger(__name__)

def normalize_column_name(name):
    """Normalize column name for comparison (remove spaces, underscores, lowercase)"""
    return str(name).strip().lower().replace(' ', '').replace('_', '').replace('-', '')

def find_column_dynamic(column_name: str, df_columns, exact_match_preferred=True):
    """
    Dynamically find column by name with fuzzy matching
    
    Args:
        column_name: The column name to search for
        df_columns: List of actual column names in DataFrame
        exact_match_preferred: If True, prefers exact matches over fuzzy
    
    Returns:
        Actual column name if found, None otherwise
    """
    col_name_clean = str(column_name).strip()
    df_columns_list = list(df_columns)
    
    # Strategy 1: Exact match (case-sensitive)
    if col_name_clean in df_columns_list:
        return col_name_clean
    
    # Strategy 2: Case-insensitive exact match
    df_columns_lower = {str(col).lower().strip(): str(col) for col in df_columns_list}
    col_name_lower = col_name_clean.lower().strip()
    
    if col_name_lower in df_columns_lower:
        return df_columns_lower[col_name_lower]
    
    # Strategy 3: Normalized match (handles spaces, underscores, case)
    col_name_normalized = normalize_column_name(col_name_clean)
    for df_col in df_columns_list:
        df_col_normalized = normalize_column_name(df_col)
        if df_col_normalized == col_name_normalized:
            return str(df_col).strip()
    
    # Strategy 4: Partial match (if column name contains the search term or vice versa)
    for df_col in df_columns_list:
        df_col_str = str(df_col).strip()
        if col_name_lower in df_col_str.lower() or df_col_str.lower() in col_name_lower:
            return df_col_str
    
    # Strategy 5: Keyword-based fuzzy match (80% threshold)
    col_keywords = set(col_name_lower.split())
    if len(col_keywords) > 0:
        for df_col in df_columns_list:
            df_col_str = str(df_col).strip().lower()
            df_col_keywords = set(df_col_str.split())
            match_ratio = len(col_keywords & df_col_keywords) / len(col_keywords) if len(col_keywords) > 0 else 0
            if match_ratio >= 0.8:
                return str(df_col).strip()
    
    return None

def detect_employee_identifier_columns(df):
    """
    Dynamically detect employee identifier columns (name and ID columns)
    
    Returns:
        dict with keys: 'name_column', 'id_column', 'name_found', 'id_found'
    """
    df_columns = list(df.columns)
    result = {
        'name_column': None,
        'id_column': None,
        'name_found': False,
        'id_found': False
    }
    
    # Common patterns for name columns
    name_patterns = [
        r'user\s*name', r'employee\s*name', r'full\s*name', r'name', 
        r'resource\s*name', r'staff\s*name', r'person\s*name'
    ]
    
    # Common patterns for ID columns
    id_patterns = [
        r'emp\s*id', r'employee\s*id', r'emp\s*number', r'staff\s*id',
        r'resource\s*id', r'person\s*id', r'employee\s*number'
    ]
    
    # Try to find name column
    for pattern in name_patterns:
        for col in df_columns:
            col_lower = str(col).lower().strip()
            if re.search(pattern, col_lower, re.IGNORECASE):
                result['name_column'] = str(col).strip()
                result['name_found'] = True
                break
        if result['name_found']:
            break
    
    # Try to find ID column
    for pattern in id_patterns:
        for col in df_columns:
            col_lower = str(col).lower().strip()
            if re.search(pattern, col_lower, re.IGNORECASE):
                result['id_column'] = str(col).strip()
                result['id_found'] = True
                break
        if result['id_found']:
            break
    
    # If not found by pattern, try direct lookup with common names
    if not result['name_found']:
        common_names = ['User Name', 'Employee Name', 'Full Name', 'Name']
        for name in common_names:
            found = find_column_dynamic(name, df_columns)
            if found:
                result['name_column'] = found
                result['name_found'] = True
                break
    
    if not result['id_found']:
        common_ids = ['EMP ID', 'Employee ID', 'Emp ID', 'Employee Number']
        for id_col in common_ids:
            found = find_column_dynamic(id_col, df_columns)
            if found:
                result['id_column'] = found
                result['id_found'] = True
                break
    
    return result

def detect_billability_column(df):
    """
    Dynamically detect billability column from DataFrame
    
    Returns:
        Column name if found, None otherwise
    """
    df_columns = list(df.columns)
    
    # Common patterns for billability columns
    billability_patterns = [
        r'billability', r'billing\s*type', r'billable', r'chargeable'
    ]
    
    # Try pattern matching first
    for pattern in billability_patterns:
        for col in df_columns:
            col_lower = str(col).lower().strip()
            if re.search(pattern, col_lower, re.IGNORECASE):
                return str(col).strip()
    
    # Try direct lookup with common names
    common_names = [
        'Project Billability Type', 'Project Billability', 'Billability',
        'Task Billability', 'Billability Type', 'Billable'
    ]
    
    for name in common_names:
        found = find_column_dynamic(name, df_columns)
        if found:
            return found
    
    return None

class ExpectedFormatPDFGenerator:
    """
    PDF Generator that creates PDFs exactly matching the Expected.pdf format
    """
    
    def __init__(self):
        # Use settings for output directory (Azure-friendly)
        if USE_SETTINGS:
            # Use configured output directory, fallback to 'output' subdirectory of data_dir
            base_dir = settings.data_dir
            self.output_dir = os.path.join(base_dir, "output")
        else:
            # Fallback to default location
            self.output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
        
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Page setup for landscape A4 (exactly like Expected.pdf)
        self.page_width, self.page_height = landscape(A4)
        self.margin = 10 * mm  # Even smaller margins to fit 26 columns
        
        # Exact column widths as specified (in pixels converted to points)
        # 1 pixel = 0.75 points, but we need to scale to fit A4 landscape
        # A4 landscape width: 841.89pt, margins: 20mm = 56.7pt, available: ~785pt
        # Total specified width: 44+44+54+44+50+50+50+54+44+62+44+50+61+50+50+48+50+37+62+56+48+50+50+50+48+50 = 1307px
        # Scale factor: 785 / 1307 ≈ 0.6
        scale_factor = 0.6
        
        self.column_widths = [
            44 * scale_factor,  # A: Date (44 px)
            44 * scale_factor,  # B: Month (44 px)
            54 * scale_factor,  # C: User Name (54 px)
            44 * scale_factor,  # D: EMP ID (44 px)
            50 * scale_factor,  # E: Email (50 px)
            50 * scale_factor,  # F: Resource Category (50 px)
            50 * scale_factor,  # G: User Resource Type (50 px)
            54 * scale_factor,  # H: DU Head (54 px)
            44 * scale_factor,  # I: DU (44 px)
            62 * scale_factor,  # J: PU (62 px)
            44 * scale_factor,  # K: BU (44 px)
            50 * scale_factor,  # L: SBU (50 px)
            61 * scale_factor,  # M: Project (61 px)
            50 * scale_factor,  # N: Project Code (50 px)
            50 * scale_factor,  # O: Project Manager (50 px)
            48 * scale_factor,  # P: Project Practice Owner (48 px)
            50 * scale_factor,  # Q: Project Contract Type (50 px)
            37 * scale_factor,  # R: Project Type (37 px)
            62 * scale_factor,  # S: Project Billability Type (62 px)
            56 * scale_factor,  # T: Task (56 px)
            48 * scale_factor,  # U: Task Category (48 px)
            50 * scale_factor,  # V: Task Billability (50 px)
            50 * scale_factor,  # W: Tasks Payability (50 px)
            50 * scale_factor,  # X: Regular Time (Hours) (50 px)
            48 * scale_factor,  # Y: Timesheet Status (48 px)
            50 * scale_factor   # Z: Input Type Code (50 px)
        ]
        
        # Colors matching Expected.pdf
        # Dark Blue, Text 2, lighter 40% - RGB(68, 114, 196) converted to decimal
        self.header_color = colors.Color(68/255, 114/255, 196/255)  # Dark Blue, Text 2, lighter 40%
        self.white = colors.white
        self.black = colors.black
        self.light_gray = colors.Color(0.98, 0.98, 0.98)  # Very light gray for alternating rows
        
        logger.info("✅ Expected Format PDF Generator initialized")
        logger.info(f"📄 Page size: {self.page_width:.1f} x {self.page_height:.1f} points (Landscape A4)")
        logger.info(f"📏 Total column width: {sum(self.column_widths):.1f} points")
    
    def create_header_and_logo(self, canvas, doc, employee_name="", emp_id=""):
        """
        Create header with title, timestamp, and logo in top-left corner
        """
        try:
            # Logo in top-left corner - use logo.png from root directory
            logo_x = self.margin - 10  # Move further left
            logo_y = self.page_height - 70  # Move down slightly to avoid overlap
            
            # Try to load and display the logo.png file
            # Try multiple locations for logo (root, public, current directory)
            logo_paths = [
                os.path.join(os.path.dirname(os.path.dirname(__file__)), "logo.png"),  # Root directory
                os.path.join(os.path.dirname(os.path.dirname(__file__)), "public", "logo.png"),  # Public directory
                "logo.png",  # Current directory
            ]
            
            logo_path = None
            for path in logo_paths:
                if os.path.exists(path):
                    logo_path = path
                    break
            
            if logo_path and os.path.exists(logo_path):
                try:
                    # Load and display the logo image
                    from reportlab.lib.utils import ImageReader
                    logo = ImageReader(logo_path)
                    # Smaller logo dimensions to avoid overlap
                    logo_width = 120  # Reduced from 169
                    logo_height = 55  # Reduced from 75
                    canvas.drawImage(logo, logo_x, logo_y, width=logo_width, height=logo_height)
                    logger.info("✅ Logo loaded successfully from logo.png")
                except Exception as logo_error:
                    logger.warning(f"⚠️ Could not load logo.png: {logo_error}")
            else:
                logger.warning("⚠️ logo.png not found in root directory")
            
            # Report title (centered) - Black Bold Arial 9.5
            title_y = self.page_height - 35
            canvas.setFillColor(self.black)
            canvas.setFont("Helvetica-Bold", 9.5)  # Black Bold Arial 9.5
            
            title = "Admin Timesheet Report"
            
            title_width = canvas.stringWidth(title, "Helvetica-Bold", 9.5)
            title_x = (self.page_width - title_width) / 2
            canvas.drawString(title_x, title_y, title)
            
            # Generation timestamp (centered below title) - Black Arial MT 3.5 (no bold)
            timestamp = f"Generated on {datetime.now().strftime('%a %b %d %H:%M:%S AST %Y')}"
            canvas.setFont("Helvetica", 3.5)  # Black Arial MT 3.5 (no bold)
            canvas.setFillColor(self.black)
            timestamp_width = canvas.stringWidth(timestamp, "Helvetica", 3.5)
            timestamp_x = (self.page_width - timestamp_width) / 2
            canvas.drawString(timestamp_x, title_y - 8, timestamp)
            
        except Exception as e:
            logger.error(f"❌ Error creating header: {e}")
    
    
    def get_table_headers(self):
        """
        Return the 26 column headers exactly as in Expected.pdf with text wrapping
        """
        headers = [
            "Date", "Month", "User Name", "EMP ID", "Email", "Resource Category",
            "User Resource Type", "DU Head", "DU", "PU", "BU", "SBU",
            "Project", "Project Code", "Project Manager", "Project Practice Owner",
            "Project Contract Type", "Project Type", "Project Billability Type",
            "Task", "Task Category", "Task Billability", "Tasks Payability", "Regular Time (Hours)",
            "Timesheet Status", "Input Type Code"
        ]
        
        # Convert headers to Paragraphs for text wrapping
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import Paragraph
        from reportlab.lib import colors
        styles = getSampleStyleSheet()
        header_style = styles['Normal']
        header_style.fontSize = 3.5
        header_style.fontName = 'Helvetica-Bold'
        header_style.leading = 4
        header_style.alignment = 1  # Center alignment
        header_style.textColor = colors.white  # Set header text color to white
        
        return [Paragraph(header, header_style) for header in headers]
    
    def create_table_data(self, employee_data):
        """
        Convert employee DataFrame to table data format
        """
        try:
            logger.info(f"📊 Creating table data for {len(employee_data)} rows")
            logger.info(f"📊 Available columns: {list(employee_data.columns)}")
            
            # Get string headers for mapping (not Paragraph objects)
            string_headers = [
                "Date", "Month", "User Name", "EMP ID", "Email", "Resource Category",
                "User Resource Type", "DU Head", "DU", "PU", "BU", "SBU",
                "Project", "Project Code", "Project Manager", "Project Practice Owner",
                "Project Contract Type", "Project Type", "Project Billability Type",
                "Task", "Task Category", "Task Billability", "Tasks Payability", "Regular Time (Hours)",
                "Timesheet Status", "Input Type Code"
            ]
            
            # Get Paragraph headers for table data
            headers = self.get_table_headers()
            table_data = [headers]
            
            # Create column mapping dictionary - enhanced dynamic approach
            col_mapping = {}
            df_columns = list(employee_data.columns)
            
            # Helper function for fuzzy column matching
            def normalize_column_name(name):
                """Normalize column name for comparison (remove spaces, underscores, lowercase)"""
                return str(name).strip().lower().replace(' ', '').replace('_', '').replace('-', '')
            
            # Build mapping with multiple matching strategies
            for header in string_headers:
                found = False
                header_normalized = normalize_column_name(header)
                
                # Strategy 1: Exact match
                if header in df_columns:
                    col_mapping[header] = header
                    found = True
                # Strategy 2: Case-insensitive exact match
                elif not found:
                    for df_col in df_columns:
                        if str(df_col).strip() == header:
                            col_mapping[header] = df_col
                            found = True
                            break
                # Strategy 3: Case-insensitive match
                elif not found:
                    for df_col in df_columns:
                        df_col_str = str(df_col).strip()
                        if df_col_str.lower() == header.lower():
                            col_mapping[header] = df_col
                            found = True
                            break
                # Strategy 4: Normalized match (handles spaces, underscores, case variations)
                # e.g., "User Name" matches "User_Name", "USER NAME", "UserName", etc.
                if not found:
                    for df_col in df_columns:
                        df_col_normalized = normalize_column_name(df_col)
                        if df_col_normalized == header_normalized:
                            col_mapping[header] = df_col
                            found = True
                            break
                # Strategy 5: Partial match (if column contains header keywords)
                # e.g., "Project Billability Type" matches "Billability", "Project_Billability", etc.
                if not found:
                    header_keywords = set(header.lower().split())
                    for df_col in df_columns:
                        df_col_str = str(df_col).strip()
                        df_col_keywords = set(df_col_str.lower().split())
                        # If 80% of keywords match, consider it a match
                        if len(header_keywords) > 0:
                            match_ratio = len(header_keywords & df_col_keywords) / len(header_keywords)
                            if match_ratio >= 0.8:
                                col_mapping[header] = df_col
                                found = True
                                logger.info(f"✅ Fuzzy match found: '{header}' -> '{df_col}' (match ratio: {match_ratio:.0%})")
                                break
                
                # Log if column not found (will use empty string in PDF)
                if not found:
                    logger.warning(f"⚠️ No column mapping found for header: '{header}' - will use empty value in PDF")
            
            logger.info(f"📊 Column mapping: {col_mapping}")
            
            # Data rows
            for _, row in employee_data.iterrows():
                row_data = []
                for header in string_headers:  # Use string headers for mapping
                    if header in col_mapping:
                        actual_col = col_mapping[header]
                        value = row.get(actual_col, "")
                        
                        # Handle different data types
                        if pd.isna(value):
                            value = ""
                        elif isinstance(value, (int, float)):
                            if header == "Regular Time (Hours)":
                                value = str(int(value)) if not pd.isna(value) else ""
                            else:
                                value = str(value)
                        else:
                            value = str(value)
                        
                        # Enable text wrapping by using Paragraph for long text
                        if len(str(value)) > 15:  # Use Paragraph for longer text
                            from reportlab.lib.styles import getSampleStyleSheet
                            from reportlab.platypus import Paragraph
                            styles = getSampleStyleSheet()
                            normal_style = styles['Normal']
                            normal_style.fontSize = 3.5
                            normal_style.fontName = 'Helvetica'
                            normal_style.leading = 4
                            value = Paragraph(str(value), normal_style)
                        
                        row_data.append(value)
                    else:
                        # Column not found - use empty string (graceful handling)
                        # This allows PDF generation to continue even if some columns are missing
                        row_data.append("")
                
                table_data.append(row_data)
            
            # Log column mapping summary
            mapped_count = len(col_mapping)
            total_headers = len(string_headers)
            unmapped_count = total_headers - mapped_count
            logger.info(f"📊 Column mapping summary: {mapped_count}/{total_headers} columns mapped successfully")
            if unmapped_count > 0:
                unmapped_headers = [h for h in string_headers if h not in col_mapping]
                logger.info(f"⚠️ Unmapped columns ({unmapped_count}) - will appear empty in PDF: {', '.join(unmapped_headers[:5])}{'...' if unmapped_count > 5 else ''}")
            
            logger.info(f"✅ Created table data with {len(table_data)} rows (including header)")
            return table_data
            
        except Exception as e:
            logger.error(f"❌ Error creating table data: {e}")
            return []
    
    def create_table_style(self):
        """
        Create table style exactly matching Expected.pdf
        """
        return TableStyle([
            # Header row styling - Excel-like header with blue background
            ('BACKGROUND', (0, 0), (-1, 0), self.header_color),
            ('TEXTCOLOR', (0, 0), (-1, 0), self.white),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 3.5),  # Small font to fit 26 columns
            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
            
            # Data rows styling - Excel-like data cells
            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),  # Center align all data
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 3.5),  # Small font to fit 26 columns
            ('TEXTCOLOR', (0, 1), (-1, -1), self.black),
            ('VALIGN', (0, 1), (-1, -1), 'TOP'),  # Top align for better text wrapping
            
            # Special alignment for numeric columns
            ('ALIGN', (23, 1), (23, -1), 'CENTER'),  # Regular Time (Hours) - center aligned
            
            # Excel-like grid borders - all cells have borders
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),  # Thicker line below header
            ('LINEABOVE', (0, 0), (-1, 0), 1, colors.black),  # Thicker line above header
            ('LINEBEFORE', (0, 0), (0, -1), 1, colors.black),  # Thicker line before first column
            ('LINEAFTER', (-1, 0), (-1, -1), 1, colors.black),  # Thicker line after last column
            
            # Row striping for better readability (like Excel)
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.Color(0.95, 0.95, 0.95)]),
            
            # Cell padding for better appearance
            ('LEFTPADDING', (0, 0), (-1, -1), 3),
            ('RIGHTPADDING', (0, 0), (-1, -1), 3),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            
            # Text wrapping for all cells - critical for Excel-like behavior
            ('WORDWRAP', (0, 0), (-1, -1), 'CJK'),  # Enable text wrapping for all cells
        ])
    
    def generate_single_pdf(self, employee_data, user_name, emp_id):
        """
        Generate PDF for a single employee exactly matching Expected.pdf format
        """
        try:
            logger.info(f"🎯 Generating Expected Format PDF for {user_name} ({emp_id})")
            
            # Create filename using just the User Name exactly as it appears
            filename = f"{user_name}.pdf"
            output_path = os.path.join(self.output_dir, filename)
            
            # Create PDF document with exact margins
            doc = SimpleDocTemplate(
                output_path,
                pagesize=landscape(A4),
                leftMargin=self.margin,
                rightMargin=self.margin,
                topMargin=self.margin + 50,  # Increased space to avoid logo overlap
                bottomMargin=self.margin
            )
            
            # Create table data
            table_data = self.create_table_data(employee_data)
            if not table_data:
                logger.error(f"❌ No table data created for {user_name}")
                return {
                    "success": False,
                    "error": "No table data created",
                    "message": f"Failed to create table data for {user_name}"
                }
            
            # Create table with exact column widths
            table = Table(table_data, colWidths=self.column_widths, repeatRows=1)
            table.setStyle(self.create_table_style())
            
            # Build PDF with custom header
            def on_first_page(canvas, doc):
                self.create_header_and_logo(canvas, doc, user_name, emp_id)
            
            def on_later_pages(canvas, doc):
                self.create_header_and_logo(canvas, doc, user_name, emp_id)
            
            # Build the document
            doc.build([table], onFirstPage=on_first_page, onLaterPages=on_later_pages)
            
            # Verify file was created
            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path)
                logger.info(f"✅ PDF created successfully: {output_path} ({file_size:,} bytes)")
                return {
                    "success": True,
                    "file_path": output_path,
                    "filename": filename,
                    "user_name": user_name,
                    "emp_id": emp_id,
                    "file_size": file_size,
                    "message": f"Expected Format PDF generated successfully for {user_name}"
                }
            else:
                logger.error(f"❌ PDF file not found after creation: {output_path}")
                return {"success": False, "error": "PDF file not created"}
                
        except Exception as e:
            logger.error(f"❌ Error generating Expected Format PDF for {user_name}: {e}")
            return {"success": False, "error": str(e)}
    
    def generate_all_pdfs(self, df, name_filter=None, emp_id_filter=None, billability_filter=None):
        """
        Generate PDFs for all employees using Expected.pdf format
        Supports filtering by name starting with specific letter, EMP ID starting with specific text, and billability type
        """
        try:
            logger.info("🎯 Generating Expected Format PDFs for all employees")
            logger.info(f"🔍 Received filters - name_filter: {name_filter}, emp_id_filter: {emp_id_filter}, billability_filter: {billability_filter}")
            logger.info(f"📊 Received DataFrame with {len(df)} rows")
            
            # Use provided DataFrame if it's not empty (custom condition was already applied)
            # Only load from Consolidated.xlsx if DataFrame is empty or not provided
            if df is None or df.empty:
                consolidated_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Consolidated.xlsx")
                if os.path.exists(consolidated_path):
                    logger.info("📊 DataFrame empty, loading real data from Consolidated.xlsx")
                    df = pd.read_excel(consolidated_path)
                    logger.info(f"📊 Loaded {len(df)} rows from Consolidated.xlsx")
                else:
                    logger.warning("⚠️ Consolidated.xlsx not found, using provided DataFrame")
                    return {
                        "success": False,
                        "error": "No data provided and Consolidated.xlsx not found",
                        "message": "DataFrame is empty and no consolidated data available"
                    }
            else:
                logger.info(f"📊 Using provided DataFrame with {len(df)} rows (custom condition already applied)")
            
            # Dynamically detect employee identifier columns
            employee_cols = detect_employee_identifier_columns(df)
            name_col = employee_cols['name_column']
            id_col = employee_cols['id_column']
            
            if not employee_cols['name_found'] or not employee_cols['id_found']:
                logger.error(f"❌ Could not detect required employee identifier columns")
                logger.error(f"❌ Name column found: {employee_cols['name_found']} ({name_col})")
                logger.error(f"❌ ID column found: {employee_cols['id_found']} ({id_col})")
                logger.error(f"❌ Available columns: {list(df.columns)}")
                return {
                    "success": False,
                    "error": "Could not detect employee identifier columns (name and ID)",
                    "message": f"Excel file must contain employee name and ID columns. Found columns: {', '.join(list(df.columns)[:10])}"
                }
            
            logger.info(f"✅ Detected employee columns - Name: '{name_col}', ID: '{id_col}'")
            
            # Apply name filter if provided
            if name_filter:
                logger.info(f"🔍 Filtering employees by first letter after comma starting with '{name_filter}'")
                # Filter data where the first letter after comma in name column starts with the specified letter
                def extract_first_letter_after_comma(name):
                    if pd.isna(name):
                        return ''
                    name_str = str(name).strip()
                    if ',' in name_str:
                        # Get part after comma, strip spaces, get first letter
                        after_comma = name_str.split(',', 1)[1].strip()
                        return after_comma[0].upper() if after_comma else ''
                    return name_str[0].upper() if name_str else ''

                mask_after_comma = df[name_col].apply(extract_first_letter_after_comma) == name_filter.upper()
                filtered_df = df[mask_after_comma]
                logger.info(f"🔍 After 'after comma' name filtering: {len(filtered_df)} rows")

                # Fallback: if no rows, try first letter of whole name (previous behavior)
                if filtered_df.empty:
                    logger.info("ℹ️ No matches using 'after comma' rule. Falling back to first letter of full name (legacy behavior).")
                    mask_first_letter = df[name_col].astype(str).str.strip().str.upper().str[0] == name_filter.upper()
                    filtered_df = df[mask_first_letter]
                    logger.info(f"🔍 After legacy first-letter filtering: {len(filtered_df)} rows")

                # If still empty, return helpful message
                if filtered_df.empty:
                    return {
                        "success": False,
                        "error": f"No employees found starting with '{name_filter}'",
                        "message": f"No data available for employees starting with '{name_filter}' (after-comma and legacy modes)",
                    }

                df = filtered_df
            
            # Apply EMP ID filter if provided
            if emp_id_filter:
                logger.info(f"🔍 Filtering employees by ID starting with '{emp_id_filter}'")
                logger.info(f"🔍 Available columns: {list(df.columns)}")
                logger.info(f"🔍 Sample ID values: {df[id_col].head(10).tolist()}")
                
                # Filter data where ID starts with the specified text
                mask = df[id_col].astype(str).str.upper().str.startswith(emp_id_filter.upper())
                df = df[mask]
                logger.info(f"🔍 After ID filtering: {len(df)} rows for IDs starting with '{emp_id_filter}'")
                
                if df.empty:
                    return {
                        "success": False,
                        "error": f"No employees found with ID starting with '{emp_id_filter}'",
                        "message": f"No data available for employees whose ID starts with '{emp_id_filter}'"
                    }
            
            # Apply billability filter if provided
            if billability_filter:
                logger.info(f"🔍 Filtering employees by billability type: '{billability_filter}'")
                logger.info(f"🔍 Available columns: {list(df.columns)}")
                
                # Dynamically detect billability column
                billability_column = detect_billability_column(df)
                
                if billability_column:
                    logger.info(f"🔍 Using billability column: '{billability_column}'")
                    logger.info(f"🔍 Sample {billability_column} values: {df[billability_column].head(10).tolist()}")
                    
                    # Filter data based on billability type
                    if billability_filter.lower() == 'billable':
                        mask = df[billability_column].astype(str).str.lower().str.contains('billable', na=False)
                    elif billability_filter.lower() == 'non-billable':
                        mask = df[billability_column].astype(str).str.lower().str.contains('non-billable', na=False)
                    else:
                        logger.warning(f"⚠️ Unknown billability filter: {billability_filter}")
                        mask = pd.Series([True] * len(df), index=df.index)
                    
                    df = df[mask]
                    logger.info(f"🔍 After billability filtering: {len(df)} rows for '{billability_filter}' billability type")
                    
                    if df.empty:
                        return {
                            "success": False,
                            "error": f"No employees found with '{billability_filter}' billability type",
                            "message": f"No data available for employees with '{billability_filter}' billability type"
                        }
                else:
                    logger.warning("⚠️ No billability column found in data. Available columns: " + ", ".join(df.columns))
                    # If no billability column exists, continue without filtering
            
            # Group by employee using dynamically detected columns
            employee_groups = df.groupby([name_col, id_col])
            results = []
            generated_files = []
            successful_generations = 0
            
            logger.info(f"📊 Found {len(employee_groups)} unique employees to process")
            logger.info(f"📊 Sample employee data: {list(employee_groups.groups.keys())[:5]}")
            
            for (user_name, emp_id), group in employee_groups:
                logger.info(f"📊 Processing {user_name} ({emp_id}) - {len(group)} rows")
                
                # Ensure name_col and id_col are in the group DataFrame for PDF generation
                # They should already be there from groupby, but ensure consistency
                result = self.generate_single_pdf(group, str(user_name), str(emp_id))
                results.append(result)
                
                if result.get("success"):
                    successful_generations += 1
                    generated_files.append({
                        "filename": result.get("filename", ""),
                        "file_path": result.get("file_path", ""),
                        "user_name": result.get("user_name", ""),
                        "emp_id": result.get("emp_id", ""),
                        "file_size": result.get("file_size", 0)
                    })
            
            # Build filter message
            filter_parts = []
            if name_filter:
                filter_parts.append(f"name starting with '{name_filter}'")
            if emp_id_filter:
                filter_parts.append(f"EMP ID starting with '{emp_id_filter}'")
            if billability_filter:
                filter_parts.append(f"billability type '{billability_filter}'")
            
            # Check if this was a pre-filtered DataFrame (custom condition)
            # If all standard filters are None but DataFrame is not empty and wasn't loaded from file,
            # it means custom condition was applied
            initial_row_count = getattr(df, '_initial_row_count', None)
            if not name_filter and not emp_id_filter and not billability_filter:
                # Likely custom condition was applied (standard filters are None)
                # The filter message will be handled by main.py response
                filter_message = " (custom condition applied)"
            elif filter_parts:
                filter_message = f" (filtered by {', '.join(filter_parts)})"
            else:
                filter_message = " (no filters applied - all employees included)"
            
            return {
                "success": successful_generations > 0,
                "total_employees": len(employee_groups),
                "successful_generations": successful_generations,
                "failed_generations": len(employee_groups) - successful_generations,
                "generated_files": generated_files,
                "results": results,
                "filter_applied": {
                    "name_filter": name_filter,
                    "emp_id_filter": emp_id_filter
                },
                "message": f"Generated {successful_generations}/{len(employee_groups)} Expected Format PDFs successfully{filter_message}"
            }
            
        except Exception as e:
            logger.error(f"❌ Error generating all Expected Format PDFs: {e}")
            import traceback
            logger.error(f"❌ Full traceback: {traceback.format_exc()}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to generate Expected Format PDFs: {e}",
                "traceback": traceback.format_exc()
            }
