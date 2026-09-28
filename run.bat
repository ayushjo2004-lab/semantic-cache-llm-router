@echo off
start cmd /k "uvicorn app.main:app --reload"
timeout /t 3 >nul
start cmd /k "streamlit run dashboard/app.py"
