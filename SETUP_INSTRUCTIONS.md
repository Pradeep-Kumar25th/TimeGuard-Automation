# TimeGuard AI - Setup Instructions

Complete setup guide for the TimeGuard AI Automation Module.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Environment Configuration](#environment-configuration)
4. [Running the Application](#running-the-application)
5. [Troubleshooting](#troubleshooting)
6. [Deployment](#deployment)

## Prerequisites

### Required Software

1. **Node.js** (v18 or higher)
   - Download from [nodejs.org](https://nodejs.org/)
   - Verify installation: `node --version`
   - Verify npm: `npm --version`

2. **Python** (v3.9 or higher)
   - Download from [python.org](https://www.python.org/downloads/)
   - Verify installation: `python --version` or `python3 --version`
   - Ensure pip is installed: `pip --version`

3. **Git** (for cloning the repository)
   - Download from [git-scm.com](https://git-scm.com/downloads)
   - Verify installation: `git --version`

### System Requirements

- **Operating System**: Windows 10+, macOS 10.15+, or Linux
- **RAM**: Minimum 4GB (8GB recommended)
- **Disk Space**: At least 500MB free space
- **Network**: Internet connection for initial package installation

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/Pradeep-Kumar25th/TimeGuard-Automation.git
cd TimeGuard-Automation
```

### Step 2: Install Python Dependencies

1. **Create a virtual environment** (recommended):
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   If you encounter issues, try:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

### Step 3: Install Node.js Dependencies

```bash
npm install
```

If you encounter issues, try:
```bash
npm cache clean --force
npm install
```

## Environment Configuration

### Frontend Environment Variables

1. **Create `.env.local` file** in the root directory:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

   For production:
   ```env
   NEXT_PUBLIC_API_URL=https://your-backend-url.com
   ```

### Backend Environment Variables

1. **Create `.env` file** in the root directory (optional, defaults are used if not set):
   ```env
   # Application Configuration
   APP_NAME=TimeGuard AI API
   ENVIRONMENT=development
   DEBUG=false

   # API Configuration
   API_TITLE=TimeGuard AI API - Automation Module
   API_VERSION=1.0.0

   # CORS Configuration (comma-separated)
   CORS_ORIGINS=http://localhost:3000,http://localhost:3001

   # Data Storage Configuration
   DATA_DIR=./data
   PDF_OUTPUT_DIR=./generated_pdfs

   # File Upload Configuration
   MAX_FILE_SIZE_MB=50
   ALLOWED_FILE_EXTENSIONS=.xlsx,.xls

   # Logging Configuration
   LOG_LEVEL=INFO
   LOG_FILE=
   ```

## Running the Application

### Development Mode

#### Start Backend Server

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Start the FastAPI server**:
   ```bash
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

3. **Verify backend is running**:
   - Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) in your browser
   - You should see the FastAPI Swagger documentation

#### Start Frontend Server

1. **Open a new terminal** (keep backend running)

2. **Navigate to project root**:
   ```bash
   cd TimeGuard-Automation
   ```

3. **Start the Next.js development server**:
   ```bash
   npm run dev
   ```

   You should see:
   ```
   ▲ Next.js 15.x.x
   - Local:        http://localhost:3000
   - Ready in X seconds
   ```

4. **Access the application**:
   - Open [http://localhost:3000](http://localhost:3000) in your browser

### Production Mode

#### Build Frontend

```bash
npm run build
npm start
```

#### Run Backend

```bash
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

## Troubleshooting

### Common Issues

#### 1. Port Already in Use

**Error**: `Address already in use` or `Port 8000/3000 is already in use`

**Solution**:
- **Windows**: Find and kill the process:
  ```bash
  netstat -ano | findstr :8000
  taskkill /PID <PID> /F
  ```
- **macOS/Linux**: Find and kill the process:
  ```bash
  lsof -ti:8000 | xargs kill -9
  ```

#### 2. Python Module Not Found

**Error**: `ModuleNotFoundError: No module named 'fastapi'`

**Solution**:
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`
- Verify Python version: `python --version` (should be 3.9+)

#### 3. Node Modules Issues

**Error**: `Cannot find module` or npm install fails

**Solution**:
- Delete `node_modules` and `package-lock.json`:
  ```bash
  rm -rf node_modules package-lock.json
  npm install
  ```
- Clear npm cache: `npm cache clean --force`

#### 4. Backend Not Connecting to Frontend

**Error**: CORS errors or connection refused

**Solution**:
- Verify `NEXT_PUBLIC_API_URL` in `.env.local` matches backend URL
- Check backend is running on correct port (8000)
- Verify CORS origins in backend `.env` include frontend URL

#### 5. Excel File Upload Fails

**Error**: File upload errors or validation failures

**Solution**:
- Verify file is `.xlsx` or `.xls` format
- Check file size is under 50MB (default limit)
- Ensure Excel file has proper headers (User Name, EMP ID columns)

#### 6. PDF Generation Fails

**Error**: PDF generation errors or missing logo

**Solution**:
- Ensure `logo.png` exists in root directory or `public/` directory
- Check `generated_pdfs/` directory has write permissions
- Verify Excel file is properly loaded before generating PDFs

### Logs and Debugging

#### Backend Logs

Backend logs are displayed in the terminal where uvicorn is running. For file logging, set `LOG_FILE` in `.env`:

```env
LOG_FILE=./logs/backend.log
```

#### Frontend Logs

Frontend logs are displayed in the browser console (F12 → Console tab) and terminal.

#### Enable Debug Mode

Backend:
```env
DEBUG=true
LOG_LEVEL=DEBUG
```

## Deployment

### Azure App Service Deployment

#### Prerequisites
- Azure account with App Service access
- Azure CLI installed
- Git configured

#### Backend Deployment

1. **Create Azure App Service**:
   ```bash
   az webapp create --resource-group <resource-group> --plan <app-plan> --name <app-name> --runtime "PYTHON:3.9"
   ```

2. **Configure environment variables** in Azure Portal:
   - `CORS_ORIGINS`: Your frontend URL
   - `DATA_DIR`: `/home/data`
   - `PDF_OUTPUT_DIR`: `/home/generated_pdfs`

3. **Deploy via Git**:
   ```bash
   az webapp deployment source config --name <app-name> --resource-group <resource-group> --repo-url <repo-url> --branch main --manual-integration
   ```

#### Frontend Deployment

1. **Build the application**:
   ```bash
   npm run build
   ```

2. **Deploy to Azure Static Web Apps** or **Azure App Service**:
   - Use Azure Static Web Apps for static hosting
   - Or use App Service with Node.js runtime

3. **Configure environment variables**:
   - `NEXT_PUBLIC_API_URL`: Your backend API URL

### Local Network Access

To access from other devices on the same network:

1. **Backend**: Change host from `127.0.0.1` to `0.0.0.0`:
   ```bash
   python -m uvicorn main:app --host 0.0.0.0 --port 8000
   ```

2. **Frontend**: Next.js automatically allows network access in dev mode

3. **Access**: Use your machine's IP address instead of `localhost`

## File Structure After Setup

```
TimeGuard-Automation/
├── .env                    # Backend environment variables (create this)
├── .env.local              # Frontend environment variables (create this)
├── node_modules/           # Node.js dependencies (generated)
├── venv/                   # Python virtual environment (optional)
├── data/                   # Data directory (auto-created)
│   └── Consolidated.xlsx  # Uploaded Excel files
├── generated_pdfs/         # Generated PDFs (auto-created)
├── logs/                   # Log files (if LOG_FILE is set)
└── ... (other project files)
```

## Next Steps

1. **Upload an Excel file** with timesheet data
2. **Test filtering** with standard and custom filters
3. **Generate PDFs** and verify output
4. **Review generated PDFs** in the `generated_pdfs/` directory

## Support

For additional support:
- Review the [README.md](./README.md) for feature documentation
- Check backend API documentation at `http://localhost:8000/docs` when running
- Contact the development team for enterprise support

---

**Last Updated**: 2025-01-27

