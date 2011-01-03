@echo off
REM echo %~dp0
cd /d %~dp0
pause
for /f "tokens=4 delims= " %%i in ('findstr "$Revision:" lzuauto3\main.py') do set j=%%i
REM echo %j%
7z a -xr!*.svn* -xr!*.pyc lzuauto-1.1.3.%j%-py3-src.7z lzuauto3