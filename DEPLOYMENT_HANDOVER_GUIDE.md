# Deployment Handover Guide - TimeGuard AI Automation Module

## Project Handover to Qatar AI Team

This document provides complete instructions for deploying and using the TimeGuard AI Automation Module.

---

## 📦 Delivery Methods

### Option 1: DevOps Repository (Recommended) ✅

**Why DevOps Repo is Better:**
- ✅ Version control and change tracking
- ✅ Collaboration and code review
- ✅ CI/CD pipeline integration
- ✅ Issue tracking
- ✅ Better for long-term maintenance

**Steps:**
1. Create a new repository in Azure DevOps (or your preferred DevOps platform)
2. Push all code to the repository
3. Share repository access with Qatar AI team
4. Provide deployment documentation (this guide)

### Option 2: ZIP File on Teams (Alternative)

**When to Use:**
- Quick handover
- One-time deployment
- Limited DevOps access

**Steps:**
1. Create ZIP file (see checklist below)
2. Upload to Teams
3. Share with Qatar AI team
4. Provide deployment instructions

---

## 📋 Pre-Deployment Checklist

### Required Files to Include

#### Backend Files
- [x] `backend/main.py` - Main FastAPI application
- [x] `backend/settings.py` - Configuration management
- [x] `backend/expected_format_pdf_generator.py` - PDF generation core
- [x] `backend/expected_format_endpoints.py` - PDF endpoints
- [x] `backend/services/` - Service layer (all files)
- [x] `backend/utils/` - Utility modules (all files)
- [x] `requirements.txt` - Python dependencies
- [x] `.env.example` - Environment variables template

#### Frontend Files
- [x] `app/` - Next.js application directory
- [x] `components/` - React components
- [x] `lib/` - Utility libraries and hooks
- [x] `public/` - Static assets
- [x] `package.json` - Node.js dependencies
- [x] `next.config.js` - Next.js configuration
- [x] `tailwind.config.js` - Tailwind CSS configuration
- [x] `tsconfig.json` - TypeScript configuration

#### Configuration Files
- [x] `.gitignore` - Git ignore rules
- [x] `README.md` - Project documentation
- [x] `logo.png` - Company logo (if exists)

#### Documentation Files
- [x] `DEPLOYMENT_HANDOVER_GUIDE.md` - This file
- [x] `CODE_REVIEW_QUICK_REFERENCE.md` - Code review guide
- [x] `ENTERPRISE_REFACTORING_SUMMARY.md` - Refactoring documentation
- [x] `FINAL_CODE_REVIEW_SUMMARY.md` - Code review summary

---

## 🚀 Deployment Instructions

### Prerequisites

**Backend Requirements:**
- Python 3.8+ installed
- pip package manager
- Azure App Service (or similar hosting)

**Frontend Requirements:**
- Node.js 18+ installed
- npm or yarn package manager
- Azure Static Web Apps (or similar hosting)

**Azure Resources Needed:**
- Azure App Service (for FastAPI backend)
- Azure Static Web Apps (for Next.js frontend)
- Azure Storage Account (optional, for file storage)

---

## 📝 Step-by-Step Deployment

### Step 1: Backend Deployment

#### 1.1 Environment Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### 1.2 Environment Variables

Create `.env` file in `backend/` directory:

```env
# Application Configuration
APP_NAME=TimeGuard AI API
ENVIRONMENT=production
DEBUG=false

# CORS Configuration (Update with your frontend URL)
CORS_ORIGINS=https://your-frontend-url.azurestaticapps.net,https://your-frontend-url.com

# Data Storage Configuration
DATA_DIR=./data
PDF_OUTPUT_DIR=./generated_pdfs

# File Upload Configuration
MAX_FILE_SIZE_MB=50

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=./logs/app.log
```

#### 1.3 Azure App Service Deployment

**Option A: Using Azure CLI**
```bash
# Login to Azure
az login

# Create resource group (if not exists)
az group create --name TimeGuardRG --location eastus

# Create App Service plan
az appservice plan create --name TimeGuardPlan --resource-group TimeGuardRG --sku B1 --is-linux

# Create Web App
az webapp create --resource-group TimeGuardRG --plan TimeGuardPlan --name timeguard-api --runtime "PYTHON:3.11"

# Deploy code
az webapp deployment source config-zip --resource-group TimeGuardRG --name timeguard-api --src backend.zip

# Set environment variables
az webapp config appsettings set --resource-group TimeGuardRG --name timeguard-api --settings \
  ENVIRONMENT=production \
  CORS_ORIGINS="https://your-frontend-url.azurestaticapps.net" \
  DATA_DIR="./data" \
  MAX_FILE_SIZE_MB=50
```

**Option B: Using Azure DevOps Pipeline**
```yaml
# azure-pipelines.yml
trigger:
  branches:
    include:
      - main

pool:
  vmImage: 'ubuntu-latest'

steps:
- task: UsePythonVersion@0
  inputs:
    versionSpec: '3.11'
  
- script: |
    cd backend
    pip install -r requirements.txt
  displayName: 'Install dependencies'
  
- task: AzureWebApp@1
  inputs:
    azureSubscription: 'YourSubscription'
    appName: 'timeguard-api'
    package: './backend'
```

#### 1.4 Verify Backend Deployment

```bash
# Test health endpoint
curl https://timeguard-api.azurewebsites.net/health

# Expected response:
# {"status":"healthy","timestamp":"2024-..."}
```

### Step 2: Frontend Deployment

#### 2.1 Environment Setup

```bash
# Navigate to project root
cd /path/to/project

# Install dependencies
npm install
# or
yarn install
```

#### 2.2 Environment Variables

Create `.env.local` file in project root:

```env
# Backend API URL
NEXT_PUBLIC_API_URL=https://timeguard-api.azurewebsites.net

# Optional: Debug mode
NEXT_PUBLIC_DEBUG=false
```

#### 2.3 Build Application

```bash
# Build for production
npm run build
# or
yarn build

# Test production build locally
npm run start
```

#### 2.4 Azure Static Web Apps Deployment

**Option A: Using Azure CLI**
```bash
# Create Static Web App
az staticwebapp create \
  --name timeguard-frontend \
  --resource-group TimeGuardRG \
  --location eastus2 \
  --sku Standard

# Deploy
az staticwebapp deploy \
  --name timeguard-frontend \
  --resource-group TimeGuardRG \
  --source-location . \
  --app-location . \
  --output-location .next
```

**Option B: Using GitHub Actions (Auto-deploy)**
```yaml
# .github/workflows/azure-static-web-apps.yml
name: Azure Static Web Apps CI/CD

on:
  push:
    branches:
      - main
  pull_request:
    types: [opened, synchronize, reopened, closed]
    branches:
      - main

jobs:
  build_and_deploy_job:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build And Deploy
        uses: Azure/static-web-apps-deploy@v1
        with:
          azure_static_web_apps_api_token: ${{ secrets.AZURE_STATIC_WEB_APPS_API_TOKEN }}
          repo_token: ${{ secrets.GITHUB_TOKEN }}
          action: "upload"
          app_location: "/"
          output_location: ".next"
```

**Option C: Manual Deployment**
```bash
# Build
npm run build

# Deploy using SWA CLI
npm install -g @azure/static-web-apps-cli
swa deploy .next --deployment-token YOUR_TOKEN
```

### Step 3: Post-Deployment Configuration

#### 3.1 Update CORS Settings

In Azure App Service, ensure CORS includes your frontend URL:
```
https://timeguard-frontend.azurestaticapps.net
```

#### 3.2 Configure Storage (Optional)

If using Azure Storage for file storage:
```bash
# Create storage account
az storage account create \
  --name timeguardstorage \
  --resource-group TimeGuardRG \
  --location eastus \
  --sku Standard_LRS

# Update DATA_DIR in backend settings to use Azure Storage
```

#### 3.3 Set Up Monitoring

- Enable Application Insights in Azure App Service
- Configure logging to Azure Log Analytics
- Set up alerts for errors

---

## 🔧 Configuration Details

### Backend Configuration (`backend/settings.py`)

**Key Settings:**
- `CORS_ORIGINS`: Frontend URLs (comma-separated)
- `DATA_DIR`: Directory for Excel files and PDFs
- `MAX_FILE_SIZE_MB`: Maximum upload size (default: 50MB)
- `LOG_LEVEL`: Logging level (INFO, DEBUG, WARNING, ERROR)

### Frontend Configuration (`next.config.js`)

**Key Settings:**
- `NEXT_PUBLIC_API_URL`: Backend API URL
- Rewrites configured for `/api/backend/*` routes

### Environment Variables Reference

**Backend (.env):**
```env
ENVIRONMENT=production
CORS_ORIGINS=https://your-frontend.azurestaticapps.net
DATA_DIR=./data
MAX_FILE_SIZE_MB=50
LOG_LEVEL=INFO
```

**Frontend (.env.local):**
```env
NEXT_PUBLIC_API_URL=https://your-backend.azurewebsites.net
```

---

## 🧪 Testing After Deployment

### 1. Backend Health Check
```bash
curl https://your-backend.azurewebsites.net/health
```

### 2. Frontend Access
- Navigate to: `https://your-frontend.azurestaticapps.net`
- Verify UI loads correctly

### 3. End-to-End Test
1. Upload Excel file
2. Apply filters (optional)
3. Generate PDFs
4. Download PDFs
5. Verify PDF format matches Expected.pdf

---

## 📊 Monitoring & Maintenance

### Application Insights

Enable Application Insights in Azure App Service:
```bash
az monitor app-insights component create \
  --app timeguard-insights \
  --location eastus \
  --resource-group TimeGuardRG

az webapp config appsettings set \
  --resource-group TimeGuardRG \
  --name timeguard-api \
  --settings APPLICATIONINSIGHTS_CONNECTION_STRING="InstrumentationKey=..."
```

### Logging

- Backend logs: Available in Azure App Service logs
- Frontend logs: Browser console + Application Insights
- Log levels: Configure via `LOG_LEVEL` environment variable

### Backup Strategy

- **Excel Files**: Stored in `data/Consolidated.xlsx` (consider Azure Storage)
- **Generated PDFs**: Stored in `data/output/` (consider Azure Storage)
- **Database**: Not applicable (stateless application)

---

## 🔒 Security Considerations

### 1. CORS Configuration
- Only allow trusted frontend URLs
- Don't use wildcard (`*`) in production

### 2. File Upload Security
- File size limits enforced
- File type validation (.xlsx, .xls only)
- Path traversal prevention implemented

### 3. Error Messages
- Production mode hides internal error details
- Correlation IDs for error tracking

### 4. Environment Variables
- Never commit `.env` files
- Use Azure App Service Configuration for secrets

---

## 🐛 Troubleshooting

### Common Issues

**Issue: Backend not accessible from frontend**
- Check CORS settings in `settings.py`
- Verify `CORS_ORIGINS` includes frontend URL
- Check Azure App Service CORS configuration

**Issue: PDFs not generating**
- Check `data/output/` directory exists and is writable
- Verify ReportLab is installed: `pip install reportlab`
- Check logs for specific errors

**Issue: Excel file upload fails**
- Verify file size < 50MB (or configured limit)
- Check file extension (.xlsx or .xls)
- Ensure `data/` directory exists and is writable

**Issue: Column detection fails**
- Verify Excel has "User Name" or similar name column
- Verify Excel has "EMP ID" or similar ID column
- Check logs for detected columns

### Debug Mode

Enable debug mode for troubleshooting:
```env
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=DEBUG
```

---

## 📞 Support & Contact

### Documentation
- Code Review Guide: `CODE_REVIEW_QUICK_REFERENCE.md`
- Architecture: `ENTERPRISE_REFACTORING_SUMMARY.md`

### Key Files to Review
- `backend/main.py` - Main API endpoint
- `backend/expected_format_pdf_generator.py` - PDF generation
- `components/enhanced-automation-dashboard.tsx` - Frontend UI

---

## ✅ Deployment Checklist

### Pre-Deployment
- [ ] All code committed to repository
- [ ] Environment variables documented
- [ ] Dependencies listed in requirements.txt and package.json
- [ ] Documentation complete

### Backend Deployment
- [ ] Azure App Service created
- [ ] Environment variables configured
- [ ] Dependencies installed
- [ ] Health endpoint responding
- [ ] CORS configured correctly

### Frontend Deployment
- [ ] Azure Static Web App created
- [ ] Environment variables configured
- [ ] Build successful
- [ ] Frontend accessible
- [ ] API connection working

### Post-Deployment
- [ ] End-to-end test successful
- [ ] Monitoring configured
- [ ] Logging working
- [ ] Error handling verified
- [ ] Security settings reviewed

---

## 🎯 Next Steps for Qatar AI Team

1. **Review Documentation**
   - Read `CODE_REVIEW_QUICK_REFERENCE.md`
   - Review `ENTERPRISE_REFACTORING_SUMMARY.md`

2. **Set Up Development Environment**
   - Clone repository
   - Install dependencies
   - Configure environment variables
   - Run locally

3. **Deploy to Azure**
   - Follow deployment instructions above
   - Configure monitoring
   - Set up backups

4. **Test Thoroughly**
   - Upload various Excel formats
   - Test all filtering options
   - Verify PDF generation
   - Test error scenarios

5. **Customize (if needed)**
   - Update logo (logo.png)
   - Modify colors/styling
   - Adjust column widths (if needed)

---

**Good luck with the deployment!** 🚀

For questions or issues, refer to the documentation files or contact the development team.

