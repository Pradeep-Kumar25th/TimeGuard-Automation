# Code Review Quick Reference Cheat Sheet

## 🎯 System Flow (30-Second Overview)

```
User Uploads Excel
    ↓
ExcelService: Validate → Read → Standardize Columns → Save to Consolidated.xlsx
    ↓
FilterService: Apply Custom Condition (if provided) OR Standard Filters
    ↓
PDFService: Orchestrate PDF Generation
    ↓
ExpectedFormatPDFGenerator: Group by Employee → Generate PDF per Employee
    ↓
Save PDFs to data/output/{User Name}.pdf
```

## 📁 Key Files & Their Purpose

| File | Purpose | Key Function |
|------|---------|--------------|
| `backend/main.py` | API endpoint | `upload_excel_timesheet()` |
| `backend/services/excel_service.py` | Excel operations | `process_uploaded_file()` |
| `backend/services/filter_service.py` | Data filtering | `apply_custom_condition()` |
| `backend/services/pdf_service.py` | PDF orchestration | `generate_pdfs()` |
| `backend/expected_format_pdf_generator.py` | Core PDF generation | `generate_all_pdfs()`, `generate_single_pdf()` |

## 🔍 Key Functions to Know

### Excel Processing
- **`ExcelService.process_uploaded_file()`**: Validates, reads, standardizes, saves Excel
- **`detect_employee_identifier_columns()`**: Finds name/ID columns using regex + fuzzy matching
- **`_standardize_column_names()`**: Renames to "User Name" and "EMP ID"

### Filtering
- **`FilterService.apply_custom_condition()`**: Parses and applies custom filters
  - Supports: `contains`, `starts with`, `==`, pandas query
- **`find_column_dynamic()`**: 5-strategy fuzzy column matching

### PDF Generation
- **`ExpectedFormatPDFGenerator.generate_all_pdfs()`**: Groups by employee, generates PDFs
- **`ExpectedFormatPDFGenerator.generate_single_pdf()`**: Creates one PDF
- **`create_table_data()`**: Maps Excel columns to 26 PDF columns
- **`create_table_style()`**: Defines PDF styling (colors, borders, fonts)

## 🎨 PDF Format Details

- **Page Size**: Landscape A4 (841.89 x 595.28 points)
- **Columns**: 26 fixed columns
- **Column Widths**: Scaled by 0.6 to fit page
- **Header**: Blue background (RGB 68, 114, 196), white text
- **Font Size**: 3.5pt (small to fit 26 columns)
- **Borders**: All cells have borders
- **Row Striping**: Alternating white/light gray

## 🔄 Data Flow Details

### 1. Excel Upload
```
File → Validate (type, size) → Read (try headers 0,1,2) → 
Detect Columns → Standardize → Save to Consolidated.xlsx
```

### 2. Filtering
```
Custom Condition? 
  YES → Parse condition → Apply filter → Return filtered DataFrame
  NO → Apply standard filters (name, ID, billability)
```

### 3. PDF Generation
```
Group by (User Name, EMP ID) → 
For each employee:
  - Extract their rows
  - Create table data (map 26 columns)
  - Create PDF document
  - Add header/logo
  - Save to {User Name}.pdf
```

## 💡 Key Design Decisions

1. **Service Layer**: Separates business logic from API endpoints
2. **Dynamic Column Detection**: Works with different Excel formats
3. **Fuzzy Matching**: 5 strategies to find columns (exact → keyword-based)
4. **Column Standardization**: Renames to standard names internally
5. **Persistent Excel**: Saves to Consolidated.xlsx for multiple operations
6. **Graceful Degradation**: Missing columns = empty cells (doesn't break)

## ❓ Common Questions & Quick Answers

**Q: What if Excel has different column names?**  
A: Fuzzy matching finds them (5 strategies: exact → keyword-based)

**Q: What if a column is missing?**  
A: Appears as empty cell in PDF, generation continues

**Q: How are PDFs named?**  
A: `{User Name}.pdf` (exactly as appears in Excel)

**Q: Can I filter by custom conditions?**  
A: Yes! Supports: `contains`, `starts with`, `==`, pandas query

**Q: What if PDF generation fails for one employee?**  
A: Others continue, system tracks success/failure counts

**Q: Why 26 fixed columns?**  
A: Matches Expected.pdf template (business requirement)

**Q: How does it handle large files?**  
A: 50MB limit, processes in chunks (grouped by employee)

## 🛠️ Technical Stack

- **Backend**: FastAPI, Pandas, ReportLab
- **Frontend**: Next.js, TypeScript, TanStack Query
- **PDF Library**: ReportLab (industry-standard Python library)

## 📊 Column Mapping Process

1. Define 26 expected headers
2. For each header, try to find matching Excel column:
   - Exact match
   - Case-insensitive
   - Normalized (remove spaces/underscores)
   - Partial match
   - Keyword-based (80% threshold)
3. Map found columns, use empty string for missing

## 🎯 Key Metrics

- **Reduced main.py**: 439 → 190 lines (57% reduction)
- **Service Layer**: 3 services (Excel, Filter, PDF)
- **Column Detection**: 5-strategy fuzzy matching
- **PDF Format**: 26 columns, landscape A4
- **Max File Size**: 50MB (configurable)

## 🚨 Error Handling

- **File Validation**: Type, size, empty checks
- **Column Validation**: Required columns (name, ID) must exist
- **Filter Validation**: Clear error if condition invalid
- **PDF Generation**: Individual failures don't stop others
- **Logging**: Comprehensive logging with correlation IDs

## 📝 Code Quality Features

✅ Type hints throughout  
✅ Comprehensive error handling  
✅ Structured logging  
✅ Service layer architecture  
✅ Dynamic column detection  
✅ Graceful degradation  
✅ Security (path traversal prevention)

---

**Remember**: The system is designed to be **flexible** (handles different Excel formats) and **robust** (graceful error handling, doesn't break on missing columns).

