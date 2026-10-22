@echo off
title Push e-Bandobast 3D Digital Twin to GitHub
echo ======================================================================
echo   Pushing e-Bandobast 3D Digital Twin to GitHub
echo   Repository: https://github.com/aicopankit/e-bandobast-
echo ======================================================================
cd /d "%~dp0"

echo.
echo [1/4] Checking current Git status...
git status

echo.
echo [2/4] Staging all files (models, KML, GeoJSON, HTML, batch scripts)...
git add -A

echo.
echo [3/4] Committing realigned dataset and 3D reconstruction updates...
git commit -m "Real-world geographic realignment of GT Road (NH-44), footbridge integration, and offline viewer support"

echo.
echo [4/4] Pushing to GitHub (origin main)...
git push -u origin main
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Retrying push to origin master...
    git push -u origin master
)

echo.
echo ======================================================================
echo   Done! Verify your repository at:
echo   https://github.com/aicopankit/e-bandobast-
echo ======================================================================
pause
