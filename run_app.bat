@echo off
setlocal

REM Activate the virtual environment
call venv\Scripts\activate.bat

REM Start the Flask app
python app.py

endlocal
pause 