@echo off
setlocal
if not defined MGSV_CATALOGUE_PYTHON set "MGSV_CATALOGUE_PYTHON=python"
"%MGSV_CATALOGUE_PYTHON%" "%~dp0catalogue.py" %*
set "CATALOGUE_EXIT=%ERRORLEVEL%"
if "%~1"=="" pause
exit /b %CATALOGUE_EXIT%