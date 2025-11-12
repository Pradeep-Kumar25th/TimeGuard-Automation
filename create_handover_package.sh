#!/bin/bash
# Script to create handover package (ZIP file)
# Usage: ./create_handover_package.sh

echo "📦 Creating TimeGuard AI Handover Package..."

# Create temporary directory
PACKAGE_NAME="TimeGuard-AI-Handover-$(date +%Y%m%d)"
mkdir -p "$PACKAGE_NAME"

echo "📁 Copying files..."

# Copy backend
echo "  - Backend files..."
cp -r backend "$PACKAGE_NAME/"

# Copy frontend
echo "  - Frontend files..."
cp -r app "$PACKAGE_NAME/"
cp -r components "$PACKAGE_NAME/"
cp -r lib "$PACKAGE_NAME/"
cp -r public "$PACKAGE_NAME/"
cp -r styles "$PACKAGE_NAME/"

# Copy configuration files
echo "  - Configuration files..."
cp package.json "$PACKAGE_NAME/"
cp package-lock.json "$PACKAGE_NAME/" 2>/dev/null || true
cp requirements.txt "$PACKAGE_NAME/"
cp next.config.js "$PACKAGE_NAME/"
cp tailwind.config.js "$PACKAGE_NAME/"
cp tsconfig.json "$PACKAGE_NAME/"
cp postcss.config.js "$PACKAGE_NAME/" 2>/dev/null || true
cp .env.example "$PACKAGE_NAME/" 2>/dev/null || true
cp .gitignore "$PACKAGE_NAME/"

# Copy documentation
echo "  - Documentation..."
cp README.md "$PACKAGE_NAME/" 2>/dev/null || true
cp DEPLOYMENT_HANDOVER_GUIDE.md "$PACKAGE_NAME/"
cp CODE_REVIEW_QUICK_REFERENCE.md "$PACKAGE_NAME/"
cp ENTERPRISE_REFACTORING_SUMMARY.md "$PACKAGE_NAME/"
cp HANDOVER_CHECKLIST.md "$PACKAGE_NAME/"
cp FINAL_CODE_REVIEW_SUMMARY.md "$PACKAGE_NAME/" 2>/dev/null || true

# Copy logo if exists
if [ -f "logo.png" ]; then
    echo "  - Logo..."
    cp logo.png "$PACKAGE_NAME/"
fi

# Remove sensitive files
echo "  - Removing sensitive files..."
find "$PACKAGE_NAME" -name ".env" -delete
find "$PACKAGE_NAME" -name ".env.local" -delete
find "$PACKAGE_NAME" -name "*.pyc" -delete
find "$PACKAGE_NAME" -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find "$PACKAGE_NAME" -name "node_modules" -type d -exec rm -rf {} + 2>/dev/null || true
find "$PACKAGE_NAME" -name ".next" -type d -exec rm -rf {} + 2>/dev/null || true

# Create ZIP file
echo "📦 Creating ZIP file..."
zip -r "${PACKAGE_NAME}.zip" "$PACKAGE_NAME" -x "*.git*" "*.DS_Store" "*node_modules*" "*.next*" "*__pycache__*"

# Clean up
rm -rf "$PACKAGE_NAME"

echo "✅ Package created: ${PACKAGE_NAME}.zip"
echo "📋 File size: $(du -h ${PACKAGE_NAME}.zip | cut -f1)"
echo ""
echo "📝 Next steps:"
echo "  1. Review HANDOVER_CHECKLIST.md"
echo "  2. Test the ZIP file contents"
echo "  3. Upload to Teams or share via DevOps repository"
echo ""

