@echo off
SETLOCAL

: Code repositories
set M_GIT=git@github.com:MicronOxford/microscope.git
set C_GIT=git@github.com:MicronOxford/cockpit.git

: Query the registry to find python
set REG_PREFIXES=hklm hkcu
set PYTHON_VERSION=0
set PYTHON_KEY=''
for %%p in (%REG_PREFIXES%) do (call :regquery %%p)
if %PYTHON_VERSION% equ 0 (
    echo No python installation found. Exiting.
    exit /B )
echo %PYTHON_KEY%
for /f "tokens=3" %%p in ('reg query %PYTHON_KEY%\InstallPath') do (
    set PYTHON_PATH=%%p)
echo.  
echo Python path is %PYTHON_PATH%
set PYTHON_EXE=%PYTHON_PATH%\python.exe

: Fetch the source code for microscope and cockpit
if exist "microscope" (echo No need to fetch microscope.) else (git clone %M_GIT%)
if exist "cockpit" (echo No need to fetch cockpit.) else (git clone %C_GIT%)

echo. & echo.Installing microscope.
cd microscope
%PYTHON_EXE% setup.py develop

echo. & echo.Installing cockpit
cd ../cockpit
%PYTHON_EXE% setup.py develop
cd ..

ENDLOCAL

echo. & echo. "microscope and cockpit installed"
exit /b

: Determine available python versions user HKLM or HKCU
:regquery
 set REG_KEY=%1\software\python\pythoncore
 (for /f "tokens=5 delims=\" %%v in ('reg query "%REG_KEY%"') do (
   if %%v gtr %PYTHON_VERSION% (
      set PYTHON_VERSION=%%v
      set PYTHON_KEY=%REG_KEY%\%%v
 )))
 GOTO :eof