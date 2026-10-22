@echo off
title Generate Offline GeoJSON Dataset
echo ======================================================================
echo   Generating nirankari_geojson.js for offline file:// browser access
echo ======================================================================
cd /d "%~dp0"

echo Compiling master GeoJSON into window.NIRANKARI_GEOJSON ...
(
  echo window.NIRANKARI_GEOJSON = 
  type nirankari_samalkha_ebandobast.geojson
  echo ;
) > nirankari_geojson.js

echo.
echo [SUCCESS] nirankari_geojson.js generated!
echo You can now double-click index.html or map_2d.html directly in Windows Explorer
echo with ZERO web server required and ZERO CORS errors.
echo.
pause
