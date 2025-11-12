# Quick Start Guide - 5 Minutes Setup

## Prerequisites Check
```bash
python --version  # Should be 3.8+
node --version    # Should be 18+
npm --version     # Should be 9+
```

## Setup (5 Steps)

### 1. Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### 2. Frontend Setup
```bash
# From project root
npm install
```

### 3. Environment Setup
```bash
# Windows
copy env.example .env

# Linux/Mac
cp env.example .env
```

### 4. Start Backend
```bash
cd backend
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

### 5. Start Frontend (New Terminal)
```bash
npm run dev
```

## Verify

- Backend: http://127.0.0.1:8000/health
- Frontend: http://localhost:3000
- API Docs: http://127.0.0.1:8000/docs

## Test

1. Go to http://localhost:3000
2. Upload an Excel file
3. Click "Upload & Generate PDFs"
4. Download generated PDFs

**Done!** ✅

For detailed instructions, see `SETUP_INSTRUCTIONS.md`

