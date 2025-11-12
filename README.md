# TimeGuard AI - Automation Module

Enterprise-level Excel timesheet processing and PDF generation system.

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+** - [Download](https://www.python.org/downloads/)
- **Node.js 18+** - [Download](https://nodejs.org/)
- **Git** - [Download](https://git-scm.com/downloads)

### Complete Setup Instructions

**👉 For detailed setup instructions, see: [`SETUP_INSTRUCTIONS.md`](SETUP_INSTRUCTIONS.md)**

This guide includes:
- Step-by-step installation
- Environment configuration
- Troubleshooting
- Testing procedures
- Verification checklist

### Quick Setup (TL;DR)

**1. Backend Setup:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

**2. Frontend Setup (new terminal):**
```bash
npm install
npm run dev
```

**3. Access Application:**
- Frontend: http://localhost:3000
- Backend API: http://127.0.0.1:8000
- API Docs: http://127.0.0.1:8000/docs

## 📚 Documentation

- **Setup Instructions**: `SETUP_INSTRUCTIONS.md` ⭐ **START HERE**

## 🏗️ Architecture

- **Backend**: FastAPI with service layer architecture
- **Frontend**: Next.js 15 with TypeScript
- **PDF Generation**: ReportLab
- **Data Processing**: Pandas
- **State Management**: TanStack Query (React Query)

## ✨ Features

- ✅ Dynamic Excel column detection (handles column name variations)
- ✅ Custom filtering conditions (advanced query support)
- ✅ PDF generation (26-column landscape format)
- ✅ Employee-based PDF grouping
- ✅ Persistent Excel file storage
- ✅ Real-time status updates
- ✅ Download/Delete PDF operations
- ✅ Responsive UI with dark mode support

## 🧪 Testing the Application

After setup, test these features:

1. **Excel Upload**: Upload a timesheet Excel file
2. **PDF Generation**: Generate PDFs for all employees
3. **Filtering**: Test name, EMP ID, and billability filters
4. **Custom Conditions**: Try "EMP ID starts with 'P'" or similar
5. **PDF Download**: Download generated PDFs
6. **PDF Delete**: Delete individual or all PDFs
7. **Excel Clear**: Clear uploaded Excel file

## 📦 Project Structure

```
├── backend/              # FastAPI backend
│   ├── main.py          # Application entry point
│   ├── services/        # Business logic layer
│   └── utils/           # Utilities
├── app/                 # Next.js frontend
│   ├── page.tsx        # Main page
│   └── api/backend/    # API route proxies
├── components/          # React components
└── lib/                 # Shared utilities and hooks
```

## 🔧 Development

### Backend Commands
```bash
# Start with auto-reload
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload

# Production mode
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### Frontend Commands
```bash
# Development
npm run dev

# Production build
npm run build
npm start

# Linting
npm run lint
```

## 📦 Deployment

For Azure deployment, refer to Azure App Service documentation or contact your DevOps team.

## 🐛 Troubleshooting

Common issues and solutions are documented in `SETUP_INSTRUCTIONS.md` under the Troubleshooting section.

## 📞 Support

For setup or deployment questions:
1. Check `SETUP_INSTRUCTIONS.md` first
2. Review error messages in terminal output
3. Check backend logs for detailed errors
4. Refer to documentation files listed above
