@echo off
setlocal
where py >nul 2>nul
if errorlevel 1 goto usepython
py -3 "%~dp0installer\install.py" install %*
goto finished
:usepython
where python >nul 2>nul
if errorlevel 1 goto missingpython
python "%~dp0installer\install.py" install %*
goto finished
:missingpython
echo Install Python 3.10 or later from https://www.python.org/downloads/windows/ first.
echo Then run this file again. No files were changed.
set IMB_EXIT=1
goto waitdone
:finished
set IMB_EXIT=%ERRORLEVEL%
:waitdone
if not "%~1"=="" goto exitnow
pause
:exitnow
exit /b %IMB_EXIT%
