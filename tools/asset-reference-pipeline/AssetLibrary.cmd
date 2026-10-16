@echo off
setlocal
if not defined MGSV_ASSET_PYTHON set "MGSV_ASSET_PYTHON=python"
if not defined MGSV_ASSET_CONFIG set "MGSV_ASSET_CONFIG=%~dp0config.local.json"
if not exist "%MGSV_ASSET_CONFIG%" goto missing_config
if "%~1"=="" goto default_click
"%MGSV_ASSET_PYTHON%" "%~dp0pipeline.py" --config "%MGSV_ASSET_CONFIG%" library %*
exit /b %errorlevel%
:default_click
"%MGSV_ASSET_PYTHON%" "%~dp0pipeline.py" --config "%MGSV_ASSET_CONFIG%" library
set "PIPELINE_EXIT=%errorlevel%"
echo.
echo Finished with exit code %PIPELINE_EXIT%. Counts and the aggregate catalogue path are shown above.
pause
exit /b %PIPELINE_EXIT%
:missing_config
echo Set up config.local.json with existing retained index/source paths first. See README.md.
if "%~1"=="" pause
exit /b 2
