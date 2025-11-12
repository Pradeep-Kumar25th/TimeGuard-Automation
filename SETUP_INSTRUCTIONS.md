# Complete Setup Instructions for TimeGuard AI Automation Module

## 🎯 Purpose
This guide will help the Qatar AI team set up and run the complete Automation functionality on their local PCs before deploying to Azure.

---

## 📋 Prerequisites

### Required Software
1. **Python 3.8 or higher**
   - Download from: https://www.python.org/downloads/
   - During installation, check "Add Python to PATH"
   - Verify: `python --version` (should show 3.8+)

2. **Node.js 18 or higher**
   - Download from: https://nodejs.org/
   - Verify: `node --version` (should show 18+)
   - Verify: `npm --version` (should show 9+)

3. **Git** (for cloning the repository)
   - Download from: https://git-scm.com/downloads
   - Verify: `git --version`

### Optional but Recommended
- **Visual Studio Code** (or any code editor)
- **Postman** (for API testing)

---

## 🚀 Step-by-Step Setup

### Step 1: Clone the Repository

```bash
# Clone from GitHub
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

### Step 2: Backend Setup

#### 2.1 Create Python Virtual Environment

**Windows:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

#### 2.2 Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will install:
- FastAPI (web framework)
- Uvicorn (ASGI server)
- Pandas (data processing)
- ReportLab (PDF generation)
- OpenPyXL (Excel file handling)
- And other required packages

#### 2.3 Verify Backend Installation

```bash
python -c "import fastapi, pandas, reportlab; print('✅ All packages installed')"
```

### Step 3: Frontend Setup

#### 3.1 Install Node.js Dependencies

Open a **new terminal** (keep backend terminal open) and navigate to project root:

```bash
# From project root directory
npm install
```

This will install all React/Next.js dependencies (may take 2-5 minutes).

#### 3.2 Verify Frontend Installation

```bash
npm list --depth=0
```

You should see all packages listed without errors.

### Step 4: Environment Configuration

#### 4.1 Create Environment File

**Windows:**
```bash
copy env.example .env
```

**Linux/Mac:**
```bash
cp env.example .env
```

#### 4.2 Configure Environment Variables

Open `.env` file and set these values (minimum required):

```env
# Backend URL (for local development)
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000

# Application Settings
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=INFO

# Data Directories (will be created automatically)
DATA_DIR=./data
PDF_OUTPUT_DIR=./generated_pdfs

# CORS Configuration (for local development)
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

**Note:** For local development, you can use the default values. The `.env` file is already in `.gitignore`, so it won't be committed.

### Step 5: Create Required Directories

The application will create these automatically, but you can create them manually:

```bash
# Windows
mkdir data
mkdir generated_pdfs

# Linux/Mac
mkdir -p data generated_pdfs
```

### Step 6: Start the Application

#### 6.1 Start Backend Server

In the **backend terminal** (with venv activated):

```bash
cd backend
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Keep this terminal open!**

#### 6.2 Start Frontend Server

In a **new terminal** (from project root):

```bash
npm run dev
```

You should see:
```
▲ Next.js 15.4.0
- Local:        http://localhost:3000
- Ready in 2.5s
```

**Keep this terminal open too!**

### Step 7: Verify Installation

#### 7.1 Test Backend

Open browser and visit:
- **Health Check**: http://127.0.0.1:8000/health
- **API Docs**: http://127.0.0.1:8000/docs

You should see:
- Health check returns: `{"status":"healthy","timestamp":"..."}`
- Swagger UI shows all available endpoints

#### 7.2 Test Frontend

Open browser and visit:
- **Application**: http://localhost:3000

You should see:
- TimeGuard AI header
- Automation navigation tab
- PDF Generation Dashboard

---

## ✅ Testing the Complete Functionality

### Test 1: Excel Upload

1. Go to http://localhost:3000
2. Click "Choose File" in the "Upload Excel File" section
3. Select an Excel file (.xlsx or .xls) with columns:
   - User Name (or similar)
   - EMP ID (or similar)
   - Date, Month, and other timesheet data
4. Click "Upload & Generate PDFs"
5. Wait for processing (may take 30 seconds to 2 minutes depending on file size)
6. You should see: "Processing Complete! Generated X/X PDFs successfully"

### Test 2: Filtering

1. With Excel file already uploaded
2. Enter a filter (e.g., Name starts with "A")
3. Click "Upload & Generate PDFs" (without selecting a new file)
4. Should generate PDFs only for filtered employees

### Test 3: PDF Download

1. After PDFs are generated, scroll to "Generated PDFs" section
2. Click "Download" button next to any PDF
3. PDF should download to your Downloads folder

### Test 4: PDF Delete

1. Click "Delete" button next to a PDF
2. PDF should be removed from the list
3. Or click "Delete All PDFs" to remove all

### Test 5: Clear Excel

1. Click "Clear Excel" button
2. Excel file should be cleared
3. Status should show "No Excel file uploaded"

---

## 🐛 Troubleshooting

### Backend Issues

**Problem: "Module not found" errors**
```bash
# Solution: Make sure venv is activated and dependencies are installed
cd backend
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

**Problem: Port 8000 already in use**
```bash
# Solution: Use a different port
python -m uvicorn main:app --host 127.0.0.1 --port 8001
# Then update .env: NEXT_PUBLIC_API_URL=http://127.0.0.1:8001
```

**Problem: "No module named 'pandas'"**
```bash
# Solution: Reinstall dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Frontend Issues

**Problem: "Cannot find module" errors**
```bash
# Solution: Delete node_modules and reinstall
rm -rf node_modules package-lock.json  # Linux/Mac
rmdir /s /q node_modules && del package-lock.json  # Windows
npm install
```

**Problem: Port 3000 already in use**
```bash
# Solution: Use a different port
npm run dev -- -p 3001
```

**Problem: "Failed to fetch" errors**
```bash
# Solution: Check backend is running and .env has correct API URL
# Verify: http://127.0.0.1:8000/health works in browser
```

### Excel Upload Issues

**Problem: "No Excel file available"**
- Make sure you uploaded an Excel file first
- Check that the file has "User Name" and "EMP ID" columns (or similar)

**Problem: "Could not read Excel file"**
- Verify file is .xlsx or .xls format
- Check file is not corrupted
- Ensure file has data (not empty)

**Problem: PDFs not generating**
- Check backend terminal for error messages
- Verify Excel file has required columns
- Check `generated_pdfs/` directory exists and is writable

---

## 📁 Project Structure

```
TimeGuard-AI-Automation/
├── backend/                    # Python FastAPI backend
│   ├── main.py                # Main application entry
│   ├── settings.py            # Configuration
│   ├── expected_format_*.py  # PDF generation
│   ├── services/              # Business logic
│   ├── utils/                 # Utilities
│   └── requirements.txt       # Python dependencies
│
├── app/                       # Next.js frontend
│   ├── page.tsx              # Main page
│   ├── layout.tsx            # Root layout
│   └── api/backend/          # API route proxies
│
├── components/                # React components
│   ├── enhanced-automation-dashboard.tsx  # Main UI
│   └── ui/                    # UI components
│
├── lib/                       # Utilities and hooks
│   ├── hooks/                 # Custom React hooks
│   └── logger.ts             # Logging utility
│
├── public/                    # Static assets
│   └── logo.png              # Company logo
│
├── .env                       # Environment variables (create from env.example)
├── package.json              # Node.js dependencies
├── requirements.txt          # Python dependencies (root level)
└── README.md                 # Project overview
```

---

## 🔧 Development Commands

### Backend Commands

```bash
# Start backend (with auto-reload)
cd backend
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload

# Start backend (production mode, no reload)
python -m uvicorn main:app --host 0.0.0.0 --port 8000

# Check backend health
curl http://127.0.0.1:8000/health
```

### Frontend Commands

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run linter
npm run lint
```

---

## 📝 Important Notes

1. **Both servers must run simultaneously:**
   - Backend on port 8000
   - Frontend on port 3000

2. **Data Persistence:**
   - Uploaded Excel files are saved as `data/Consolidated.xlsx`
   - Generated PDFs are saved in `generated_pdfs/`
   - These directories are in `.gitignore` (not committed)

3. **Environment Variables:**
   - `.env` file is required for frontend to connect to backend
   - Never commit `.env` file (it's in `.gitignore`)

4. **First Run:**
   - Backend will create `data/` directory automatically
   - Frontend will create `.next/` directory on first build
   - Generated PDFs directory will be created automatically

5. **Stopping Servers:**
   - Press `Ctrl+C` in each terminal to stop servers
   - Close terminals when done

---

## 🚀 Next Steps After Setup

1. ✅ Verify all functionality works (see Testing section above)
2. ✅ Review code structure and documentation
3. ✅ Test with different Excel file formats
4. ✅ Prepare for Azure deployment (see `DEPLOYMENT_HANDOVER_GUIDE.md`)

---

## 📞 Support

If you encounter issues:
1. Check the Troubleshooting section above
2. Review error messages in terminal output
3. Check backend logs for detailed error information
4. Verify all prerequisites are installed correctly
5. Refer to `CODE_REVIEW_QUICK_REFERENCE.md` for code structure

---

## ✅ Setup Verification Checklist

- [ ] Python 3.8+ installed and verified
- [ ] Node.js 18+ installed and verified
- [ ] Backend dependencies installed (`pip install -r requirements.txt`)
- [ ] Frontend dependencies installed (`npm install`)
- [ ] `.env` file created from `env.example`
- [ ] Backend server starts without errors
- [ ] Frontend server starts without errors
- [ ] Backend health check works (http://127.0.0.1:8000/health)
- [ ] Frontend loads (http://localhost:3000)
- [ ] Excel upload works
- [ ] PDF generation works
- [ ] PDF download works
- [ ] PDF delete works

**Once all checkboxes are checked, the setup is complete!** ✅

