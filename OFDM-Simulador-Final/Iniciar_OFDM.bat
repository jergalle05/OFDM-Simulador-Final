@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
 echo Creando entorno virtual...
 python -m venv .venv
 if errorlevel 1 goto error
)
.venv\Scripts\python.exe -c "import streamlit" >nul 2>&1
if errorlevel 1 (
 echo Instalando dependencias...
 .venv\Scripts\python.exe -m pip install -r requirements.txt
 if errorlevel 1 goto error
)
.venv\Scripts\python.exe -m streamlit run app.py
if errorlevel 1 goto error
exit /b 0
:error
echo Error. Comprueba Python e internet y revisa el mensaje anterior.
pause
exit /b 1
