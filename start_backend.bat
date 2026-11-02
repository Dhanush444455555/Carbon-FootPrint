@echo off
echo Starting Tomato CarbonTrace FastAPI Backend on port 8000...
cd /d "%~dp0backend"
python main.py
pause
