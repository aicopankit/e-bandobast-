@echo off
title e-Bandobast 3D Digital Twin - Server and Offline Engine
echo ======================================================================
echo   e-Bandobast 3D Digital Twin Local Server & Offline Engine
echo   Site: Sant Nirankari Sant Samagam Ground, Samalkha, Haryana
echo ======================================================================
cd /d "%~dp0"

echo.
echo [1/3] Generating / synchronizing offline dataset (nirankari_geojson.js)...
(
  echo window.NIRANKARI_GEOJSON = 
  type nirankari_samalkha_ebandobast.geojson
  echo ;
) > nirankari_geojson.js
echo       [OK] Standalone dataset ready.

echo.
echo [2/3] Opening browser at http://localhost:8000/index.html ...
start "" "http://localhost:8000/index.html"

echo.
echo [3/3] Starting local HTTP server on port 8000...
echo       Keep this command window OPEN while interacting with the 3D map.
echo       Press Ctrl+C to stop the server.
echo.

python -m http.server 8000
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [NOTE] python returned error. Trying py launcher or python3...
    py -m http.server 8000 || python3 -m http.server 8000
    if %ERRORLEVEL% NEQ 0 (
        echo.
        echo [INFO] Python command-line runtime is not found in PATH.
        echo Opening standalone offline index.html directly in browser...
        start "" "index.html"
    )
)
pause
