@echo off
REM Script to create handover package (ZIP file) for Windows
REM Usage: create_handover_package.bat

echo 📦 Creating TimeGuard AI Handover Package...

REM Create package name with date
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
set PACKAGE_NAME=TimeGuard-AI-Handover-%datetime:~0,8%

echo 📁 Creating directory...
mkdir "%PACKAGE_NAME%" 2>nul

echo 📁 Copying files...

REM Copy backend
echo   - Backend files...
xcopy /E /I /Y backend "%PACKAGE_NAME%\backend" >nul

REM Copy frontend
echo   - Frontend files...
xcopy /E /I /Y app "%PACKAGE_NAME%\app" >nul
xcopy /E /I /Y components "%PACKAGE_NAME%\components" >nul
xcopy /E /I /Y lib "%PACKAGE_NAME%\lib" >nul
if exist public xcopy /E /I /Y public "%PACKAGE_NAME%\public" >nul
if exist styles xcopy /E /I /Y styles "%PACKAGE_NAME%\styles" >nul

REM Copy configuration files
echo   - Configuration files...
if exist package.json copy /Y package.json "%PACKAGE_NAME%\" >nul
if exist package-lock.json copy /Y package-lock.json "%PACKAGE_NAME%\" >nul
if exist requirements.txt copy /Y requirements.txt "%PACKAGE_NAME%\" >nul
if exist next.config.js copy /Y next.config.js "%PACKAGE_NAME%\" >nul
if exist tailwind.config.js copy /Y tailwind.config.js "%PACKAGE_NAME%\" >nul
if exist tsconfig.json copy /Y tsconfig.json "%PACKAGE_NAME%\" >nul
if exist postcss.config.js copy /Y postcss.config.js "%PACKAGE_NAME%\" >nul
if exist .env.example copy /Y .env.example "%PACKAGE_NAME%\" >nul
if exist .gitignore copy /Y .gitignore "%PACKAGE_NAME%\" >nul

REM Copy documentation
echo   - Documentation...
if exist README.md copy /Y README.md "%PACKAGE_NAME%\" >nul
if exist DEPLOYMENT_HANDOVER_GUIDE.md copy /Y DEPLOYMENT_HANDOVER_GUIDE.md "%PACKAGE_NAME%\" >nul
if exist CODE_REVIEW_QUICK_REFERENCE.md copy /Y CODE_REVIEW_QUICK_REFERENCE.md "%PACKAGE_NAME%\" >nul
if exist ENTERPRISE_REFACTORING_SUMMARY.md copy /Y ENTERPRISE_REFACTORING_SUMMARY.md "%PACKAGE_NAME%\" >nul
if exist HANDOVER_CHECKLIST.md copy /Y HANDOVER_CHECKLIST.md "%PACKAGE_NAME%\" >nul
if exist FINAL_CODE_REVIEW_SUMMARY.md copy /Y FINAL_CODE_REVIEW_SUMMARY.md "%PACKAGE_NAME%\" >nul

REM Copy logo if exists
if exist logo.png (
    echo   - Logo...
    copy /Y logo.png "%PACKAGE_NAME%\" >nul
)

REM Remove sensitive files
echo   - Removing sensitive files...
del /S /Q "%PACKAGE_NAME%\*.env" 2>nul
del /S /Q "%PACKAGE_NAME%\*.env.local" 2>nul
del /S /Q "%PACKAGE_NAME%\*.pyc" 2>nul
for /d /r "%PACKAGE_NAME%" %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul
for /d /r "%PACKAGE_NAME%" %%d in (node_modules) do @if exist "%%d" rd /s /q "%%d" 2>nul
for /d /r "%PACKAGE_NAME%" %%d in (.next) do @if exist "%%d" rd /s /q "%%d" 2>nul

echo 📦 Creating ZIP file...
powershell -Command "Compress-Archive -Path '%PACKAGE_NAME%' -DestinationPath '%PACKAGE_NAME%.zip' -Force"

REM Clean up
rmdir /S /Q "%PACKAGE_NAME%" 2>nul

echo ✅ Package created: %PACKAGE_NAME%.zip
echo.
echo 📝 Next steps:
echo   1. Review HANDOVER_CHECKLIST.md
echo   2. Test the ZIP file contents
echo   3. Upload to Teams or share via DevOps repository
echo.

pause

