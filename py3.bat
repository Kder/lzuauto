@echo off
REM echo %~dp0
cd /d %~dp0
for /f "tokens=2 delims='" %%i in ('findstr /r "'[0-9]\.[0-9]\.[0-9]'" lzuauto3\main.py') do set ver=%%i
for /f "tokens=4 delims= " %%i in ('findstr "$Revision:" lzuauto3\main.py') do set rev=%%i
echo %ver%.%rev%
7z a -xr!*.svn* -xr!*.pyc -xr!*__pycache__* lzuauto-%ver%.%rev%-py3-src.7z lzuauto3