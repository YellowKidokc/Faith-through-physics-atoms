@echo off
setlocal
set "HERE=%~dp0"
set "PROJECT_ROOT=%~1"
if "%PROJECT_ROOT%"=="" set "PROJECT_ROOT=."
python "%HERE%canon_guard\canon_guard.py" "%PROJECT_ROOT%" -m "%HERE%canon_guard\canon-manifest.toml"
endlocal
