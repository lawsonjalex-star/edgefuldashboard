@echo off
title Push Dashboard Update
cd /d "C:\Users\xkayl\OneDrive\Documents\EDGEFUL API"
echo Pushing dashboard update to GitHub...
echo.
git add dashboard.html
git commit -m "Update dashboard"
git push
echo.
if %errorlevel% == 0 (
    echo Done! Replit will serve the latest version.
) else (
    echo Something went wrong. See output above.
)
echo.
pause
