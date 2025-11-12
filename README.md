# TimeGuard AI - Automation Module

A comprehensive enterprise-grade automation system for generating timesheet PDFs from Excel files with advanced filtering capabilities.

## Overview

TimeGuard AI Automation Module is a full-stack web application that enables users to upload Excel timesheet files, apply custom filters, and generate professional PDF reports for individual employees or groups. The system features dynamic column detection, robust filtering, and enterprise-level code architecture.

## Features

- **Excel File Upload**: Upload and process Excel timesheet files with persistent storage
- **Dynamic Column Detection**: Automatically detects employee name, ID, and billability columns even with varying column names
- **Advanced Filtering**: 
  - Standard filters (Employee Name, EMP ID, Billability Status)
  - Custom filter conditions with support for:
    - Contains operations
    - Starts with operations
    - Equals operations
    - Pandas query expressions
- **PDF Generation**: Generate professional PDF reports matching expected format specifications
- **Batch Processing**: Generate PDFs for multiple employees simultaneously
- **PDF Management**: Download, delete individual PDFs, or delete all generated PDFs
- **Enterprise Architecture**: Service layer separation, centralized logging, and configuration management

## Technology Stack

### Frontend
- **Next.js 15** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling
- **TanStack Query** - Data fetching and state management
- **Radix UI** - Accessible component library

### Backend
- **FastAPI** - Modern Python web framework
- **Pandas** - Data manipulation and analysis
- **ReportLab** - PDF generation
- **Pydantic** - Data validation and settings management
- **Uvicorn** - ASGI server

## Project Structure

```
TimeGuard-Automation/
├── app/                          # Next.js app directory
│   ├── api/                      # API route handlers
│   │   └── backend/              # Backend API proxies
│   ├── globals.css               # Global styles
│   ├── layout.tsx                # Root layout
│   └── page.tsx                  # Home page
├── backend/                      # FastAPI backend
│   ├── services/                 # Business logic layer
│   │   ├── excel_service.py     # Excel file operations
│   │   ├── filter_service.py     # Filtering logic
│   │   └── pdf_service.py        # PDF generation orchestration
│   ├── utils/                    # Utility functions
│   │   ├── file_utils.py         # File operations
│   │   └── logging_utils.py      # Logging configuration
│   ├── expected_format_endpoints.py  # PDF endpoints
│   ├── expected_format_pdf_generator.py  # PDF generation core
│   ├── main.py                   # FastAPI application
│   └── settings.py               # Configuration management
├── components/                   # React components
│   ├── enhanced-automation-dashboard.tsx  # Main dashboard
│   ├── header.tsx                # Header component
│   ├── sidebar.tsx               # Sidebar navigation
│   └── ui/                       # UI component library
├── lib/                          # Frontend utilities
│   ├── hooks/                    # Custom React hooks
│   ├── logger.ts                 # Frontend logging
│   └── utils.ts                  # Utility functions
├── public/                       # Static assets
│   └── logo.png                  # Application logo
├── logo.png                      # Logo for PDF generation
├── package.json                  # Node.js dependencies
├── requirements.txt              # Python dependencies
├── next.config.js                # Next.js configuration
├── tailwind.config.js            # Tailwind CSS configuration
└── tsconfig.json                 # TypeScript configuration
```

## Quick Start

### Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.9+
- **Git**

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Pradeep-Kumar25th/TimeGuard-Automation.git
   cd TimeGuard-Automation
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Node.js dependencies**
   ```bash
   npm install
   ```

4. **Configure environment variables**
   - Copy `env.example` to `.env.local` (for frontend)
   - Copy `env.example` to `.env` (for backend)
   - Update the values as needed

5. **Start the backend server**
   ```bash
   cd backend
   python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
   ```

6. **Start the frontend server** (in a new terminal)
   ```bash
   npm run dev
   ```

7. **Access the application**
   - Open [http://localhost:3000](http://localhost:3000) in your browser

## Detailed Setup Instructions

For comprehensive setup instructions, including environment configuration, troubleshooting, and deployment guidance, see [SETUP_INSTRUCTIONS.md](./SETUP_INSTRUCTIONS.md).

## Usage

1. **Upload Excel File**: Click "Upload Excel" and select your timesheet Excel file
2. **Apply Filters** (Optional): Use standard filters or custom filter conditions
3. **Generate PDFs**: Click "Generate PDFs" to create reports
4. **Manage PDFs**: Download or delete generated PDFs from the list

### Custom Filter Examples

- `EMP ID starts with 'P'` - Filter employees whose ID starts with 'P'
- `User Name contains 'John'` - Filter employees with 'John' in their name
- `EMP ID == 'EMP001'` - Filter specific employee ID
- `Billability == 'Billable'` - Filter by billability status

## API Endpoints

### Excel Operations
- `POST /api/timesheets/upload-excel` - Upload Excel file
- `GET /api/timesheets/excel-status` - Check Excel file status
- `DELETE /api/timesheets/clear-excel` - Clear uploaded Excel file

### PDF Operations
- `POST /api/expected-format-pdf/generate-pdfs` - Generate PDFs
- `GET /api/expected-format-pdf/list-generated-pdfs` - List all generated PDFs
- `GET /api/expected-format-pdf/download-pdf/{filename}` - Download a PDF
- `DELETE /api/expected-format-pdf/delete-pdf/{filename}` - Delete a PDF
- `DELETE /api/expected-format-pdf/delete-all-pdfs` - Delete all PDFs

## Configuration

The application uses environment variables for configuration. Key settings include:

- `NEXT_PUBLIC_API_URL` - Backend API URL (default: `http://localhost:8000`)
- `LOG_LEVEL` - Logging level (default: `INFO`)
- `DATA_DIR` - Data storage directory (default: `./data`)
- `PDF_OUTPUT_DIR` - PDF output directory (default: `./generated_pdfs`)

## Development

### Running in Development Mode

Backend (with auto-reload):
```bash
cd backend
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

Frontend (with hot-reload):
```bash
npm run dev
```

### Building for Production

Frontend:
```bash
npm run build
npm start
```

Backend:
```bash
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

## Architecture

The application follows enterprise-level best practices:

- **Service Layer Architecture**: Business logic separated into service classes
- **Centralized Configuration**: Pydantic-based settings management
- **Enterprise Logging**: Structured logging with correlation IDs
- **Security**: Path traversal prevention, input validation
- **Type Safety**: TypeScript on frontend, type hints on backend
- **Modular Design**: Reusable components and hooks

## Contributing

This is a private enterprise project. For contributions or questions, please contact the project maintainers.

## License

Proprietary - All rights reserved

## Support

For setup assistance or technical support, refer to [SETUP_INSTRUCTIONS.md](./SETUP_INSTRUCTIONS.md) or contact the development team.

---

**Repository**: [https://github.com/Pradeep-Kumar25th/TimeGuard-Automation](https://github.com/Pradeep-Kumar25th/TimeGuard-Automation)

