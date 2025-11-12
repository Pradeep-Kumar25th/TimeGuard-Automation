# GitHub Repository Setup Guide

Complete step-by-step guide to set up TimeGuard AI project on GitHub for handover to Qatar AI team.

---

## 🎯 Overview

This guide will help you:
1. Create a GitHub repository
2. Initialize and push your code
3. Set up proper structure
4. Share with Qatar AI team
5. Configure branch protection (optional)

---

## 📋 Prerequisites

- GitHub account (personal or organization)
- Git installed on your computer
- Code ready to commit

---

## 🚀 Step-by-Step Setup

### Step 1: Create GitHub Repository

#### Option A: Using GitHub Website

1. **Go to GitHub**
   - Navigate to [github.com](https://github.com)
   - Sign in to your account

2. **Create New Repository**
   - Click the **"+"** icon in top right
   - Select **"New repository"**

3. **Repository Settings**
   ```
   Repository name: TimeGuard-AI-Automation
   Description: Enterprise Excel timesheet processing and PDF generation system
   Visibility: Private (recommended) or Public
   ✅ Add a README file (optional - we'll add our own)
   ✅ Add .gitignore (select Python or Node)
   ✅ Choose a license (optional)
   ```

4. **Click "Create repository"**

#### Option B: Using GitHub CLI

```bash
# Install GitHub CLI first (if not installed)
# Then authenticate
gh auth login

# Create repository
gh repo create TimeGuard-AI-Automation \
  --private \
  --description "Enterprise Excel timesheet processing and PDF generation system" \
  --clone
```

---

### Step 2: Prepare Local Repository

#### 2.1 Check Git Status

```bash
# Navigate to your project directory
cd "C:\Latets BKP TimeSecure AI\TimeSecure AI"

# Check if git is already initialized
git status
```

**If you see "not a git repository":**
- Proceed to Step 2.2 (Initialize Git)

**If you see git files:**
- Check for existing remote: `git remote -v`
- If remote exists, you may need to change it (see Step 2.4)

#### 2.2 Initialize Git (if not already done)

```bash
# Initialize git repository
git init

# Check status
git status
```

#### 2.3 Create/Update .gitignore

Ensure `.gitignore` includes:

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/
.venv
*.egg-info/
dist/
build/

# Node.js
node_modules/
.next/
out/
build/
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Project specific
data/
generated_pdfs/
output/
*.xlsx
*.xls
Consolidated.xlsx
logs/
*.pdf

# Temporary files
*.tmp
*.temp
```

#### 2.4 Add All Files

```bash
# Add all files to staging
git add .

# Check what will be committed
git status
```

**Important:** Verify that sensitive files are NOT included:
- `.env` files
- `node_modules/`
- `__pycache__/`
- `data/` directory
- Generated PDFs

---

### Step 3: Initial Commit

```bash
# Create initial commit
git commit -m "Initial commit: TimeGuard AI Automation Module

- Backend: FastAPI with service layer architecture
- Frontend: Next.js with TypeScript
- Features: Excel processing, dynamic column detection, PDF generation
- Documentation: Complete deployment and handover guides"

# Verify commit
git log --oneline
```

---

### Step 4: Connect to GitHub Repository

#### 4.1 Add Remote Repository

```bash
# Add GitHub repository as remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/TimeGuard-AI-Automation.git

# Verify remote
git remote -v
```

**If you need to change existing remote:**
```bash
# Remove existing remote
git remote remove origin

# Add new remote
git remote add origin https://github.com/YOUR_USERNAME/TimeGuard-AI-Automation.git
```

#### 4.2 Push to GitHub

```bash
# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

**If you get authentication error:**
- Use Personal Access Token (see Step 5)
- Or use SSH instead of HTTPS

---

### Step 5: GitHub Authentication

#### Option A: Personal Access Token (Recommended)

1. **Create Token:**
   - Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Click "Generate new token (classic)"
   - Name: `TimeGuard-AI-Deployment`
   - Select scopes: `repo` (full control)
   - Click "Generate token"
   - **Copy the token** (you won't see it again!)

2. **Use Token:**
   ```bash
   # When prompted for password, use the token
   git push -u origin main
   # Username: your-github-username
   # Password: your-personal-access-token
   ```

#### Option B: SSH Key

1. **Generate SSH Key:**
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   # Press Enter to accept default location
   # Enter passphrase (optional)
   ```

2. **Add to GitHub:**
   ```bash
   # Copy public key
   cat ~/.ssh/id_ed25519.pub
   # On Windows: type C:\Users\YourName\.ssh\id_ed25519.pub
   ```
   - Go to GitHub → Settings → SSH and GPG keys
   - Click "New SSH key"
   - Paste the key and save

3. **Update Remote URL:**
   ```bash
   git remote set-url origin git@github.com:YOUR_USERNAME/TimeGuard-AI-Automation.git
   git push -u origin main
   ```

---

### Step 6: Verify Upload

1. **Check GitHub Repository:**
   - Go to your repository on GitHub
   - Verify all files are present
   - Check that `.env` files are NOT included

2. **Verify Structure:**
   ```
   ✅ backend/
   ✅ app/
   ✅ components/
   ✅ lib/
   ✅ Documentation files (.md)
   ✅ Configuration files
   ❌ .env (should NOT be present)
   ❌ node_modules/ (should NOT be present)
   ```

---

## 👥 Sharing with Qatar AI Team

### Step 7: Add Collaborators

#### Option A: Add Individual Users

1. **Go to Repository Settings:**
   - Click "Settings" tab in your repository
   - Click "Collaborators" in left sidebar
   - Click "Add people"

2. **Add Team Members:**
   - Enter GitHub usernames or emails
   - Select permission level:
     - **Read**: Can view and clone
     - **Write**: Can push changes
     - **Admin**: Full access
   - Click "Add [username] to this repository"

#### Option B: Add Organization Team

1. **If using GitHub Organization:**
   - Go to repository → Settings → Manage access
   - Click "Add teams"
   - Select team (e.g., "Qatar-AI-Team")
   - Set permission level
   - Click "Add team to this repository"

### Step 8: Share Repository Link

Send Qatar AI team:
```
Repository URL: https://github.com/YOUR_USERNAME/TimeGuard-AI-Automation

Access: You've been added as a collaborator with [Read/Write] access.

Next Steps:
1. Clone the repository: git clone https://github.com/YOUR_USERNAME/TimeGuard-AI-Automation.git
2. Follow DEPLOYMENT_HANDOVER_GUIDE.md for deployment instructions
```

---

## 🌿 Branch Strategy (Optional but Recommended)

### Step 9: Set Up Branches

```bash
# Create develop branch
git checkout -b develop
git push -u origin develop

# Create feature branch template
git checkout -b feature/template
git push -u origin feature/template

# Switch back to main
git checkout main
```

### Recommended Branch Structure:
```
main          → Production-ready code
develop       → Development branch
feature/*     → Feature branches
hotfix/*      → Hotfix branches
```

### Step 10: Branch Protection (Optional)

1. **Go to Repository Settings:**
   - Settings → Branches

2. **Add Branch Protection Rule:**
   - Branch name pattern: `main`
   - ✅ Require pull request reviews
   - ✅ Require status checks to pass
   - ✅ Require branches to be up to date
   - ✅ Include administrators

---

## 📝 Create Release/Tag (Optional)

### Step 11: Tag Initial Release

```bash
# Create tag for initial release
git tag -a v1.0.0 -m "Initial release: TimeGuard AI Automation Module

- Complete backend and frontend implementation
- Enterprise-level refactoring
- Full documentation
- Ready for deployment"

# Push tags to GitHub
git push origin v1.0.0
```

### Create GitHub Release:

1. Go to repository → Releases → "Create a new release"
2. Choose tag: `v1.0.0`
3. Release title: `v1.0.0 - Initial Release`
4. Description:
   ```
   ## Initial Release - TimeGuard AI Automation Module
   
   ### Features
   - Excel file upload and processing
   - Dynamic column detection
   - Custom filtering conditions
   - PDF generation (26-column format)
   - Employee-based PDF grouping
   
   ### Documentation
   - Complete deployment guide included
   - Code review guide available
   - Architecture documentation provided
   
   ### Deployment
   See DEPLOYMENT_HANDOVER_GUIDE.md for deployment instructions.
   ```
5. Click "Publish release"

---

## ✅ Verification Checklist

Before sharing with Qatar AI team:

- [ ] All code committed and pushed
- [ ] `.env` files excluded (check `.gitignore`)
- [ ] `node_modules/` excluded
- [ ] `__pycache__/` excluded
- [ ] Sensitive data removed
- [ ] Documentation files included
- [ ] README.md is clear
- [ ] Repository is accessible to team
- [ ] Branch protection configured (optional)
- [ ] Release/tag created (optional)

---

## 🔧 Common Issues & Solutions

### Issue: "Permission denied" when pushing

**Solution:**
- Use Personal Access Token instead of password
- Or set up SSH keys
- Check repository permissions

### Issue: Large file upload fails

**Solution:**
```bash
# Use Git LFS for large files (if needed)
git lfs install
git lfs track "*.pdf"
git add .gitattributes
git commit -m "Add Git LFS tracking"
```

### Issue: Want to remove sensitive file from history

**Solution:**
```bash
# Remove file from git history (use with caution)
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all

# Force push (coordinate with team first!)
git push origin --force --all
```

### Issue: Need to update remote URL

**Solution:**
```bash
# Check current remote
git remote -v

# Update remote URL
git remote set-url origin https://github.com/NEW_USERNAME/REPO_NAME.git

# Verify
git remote -v
```

---

## 📋 Quick Reference Commands

```bash
# Initialize repository
git init
git add .
git commit -m "Initial commit"

# Connect to GitHub
git remote add origin https://github.com/USERNAME/REPO.git
git branch -M main
git push -u origin main

# Create and switch branch
git checkout -b develop
git push -u origin develop

# Create tag
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0

# Check status
git status
git remote -v
git log --oneline
```

---

## 🎯 Next Steps for Qatar AI Team

Once repository is shared, Qatar AI team should:

1. **Clone Repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/TimeGuard-AI-Automation.git
   cd TimeGuard-AI-Automation
   ```

2. **Set Up Environment:**
   ```bash
   # Backend
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   
   # Frontend
   cd ..
   npm install
   ```

3. **Configure Environment Variables:**
   - Copy `.env.example` to `.env`
   - Update values as needed

4. **Follow Deployment Guide:**
   - Read `DEPLOYMENT_HANDOVER_GUIDE.md`
   - Deploy to Azure
   - Test thoroughly

---

## 📞 Support

If you encounter issues:
1. Check GitHub documentation: [docs.github.com](https://docs.github.com)
2. Verify repository permissions
3. Check Git configuration: `git config --list`
4. Contact GitHub support if needed

---

**Repository Setup Complete!** ✅

Your code is now on GitHub and ready to share with Qatar AI team! 🚀

