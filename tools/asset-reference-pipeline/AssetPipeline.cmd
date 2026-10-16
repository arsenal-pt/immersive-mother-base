@echo off
setlocal
if not defined MGSV_ASSET_PYTHON set "MGSV_ASSET_PYTHON=python"
if not defined MGSV_ASSET_CONFIG set "MGSV_ASSET_CONFIG=%~dp0config.local.json"
if not exist "%MGSV_ASSET_CONFIG%" goto missing_config
if "%~1"=="" goto default_click
"%MGSV_ASSET_PYTHON%" "%~dp0pipeline.py" --config "%MGSV_ASSET_CONFIG%" %*
exit /b %errorlevel%
:default_click
"%MGSV_ASSET_PYTHON%" "%~dp0pipeline.py" --config "%MGSV_ASSET_CONFIG%" run --export-default
set "PIPELINE_EXIT=%errorlevel%"
echo.
echo Finished with exit code %PIPELINE_EXIT%. The catalogue path or error is shown above.
pause
exit /b %PIPELINE_EXIT%
:missing_config
echo First copy config.example.json to a private config.local.json and configure tool/source paths.
echo See README.md. No tools or game files are bundled.
if "%~1"=="" pause
exit /b 2
