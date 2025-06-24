@echo off
setlocal

REM Check for Python 3.9.13
where python >nul 2>nul
if %errorlevel%==0 (
    for /f "delims=" %%i in ('python --version 2^>^&1') do set PY_VER=%%i
    echo Detected %PY_VER%
    echo %PY_VER% | findstr /C:"3.9.13" >nul
    if %errorlevel%==0 (
        echo Python 3.9.13 is already installed.
        set PYTHON_EXE=python
    ) else (
        echo Python 3.9.13 not found. Installing...
        goto install_python
    )
) else (
    echo Python not found. Installing Python 3.9.13...
    goto install_python
)

goto create_venv

:install_python
REM Download and install Python 3.9.13 (Windows x64)
set PYTHON_INSTALLER=python-3.9.13-amd64.exe
if not exist %PYTHON_INSTALLER% (
    powershell -Command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.9.13/python-3.9.13-amd64.exe -OutFile %PYTHON_INSTALLER%"
)
start /wait %PYTHON_INSTALLER% /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
set PYTHON_EXE=python

:create_venv
REM Create virtual environment
%PYTHON_EXE% -m venv venv
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo Failed to create virtual environment.
    exit /b 1
)

REM Upgrade pip
python -m pip install --upgrade pip

REM Install requirements
pip install -r requirements.txt

echo Environment setup complete.
endlocal
pause 