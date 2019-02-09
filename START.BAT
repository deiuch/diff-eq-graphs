@echo off

REM This file is required to be run in order to get administrator privileges in Windows

set pth=%temp%\tmp_dir_path.txt
NET SESSION >nul 2>&1
if %ERRORLEVEL% equ 0 (
    if exist "%pth%" (
        goto :payload
    ) else (
        goto :script
    )
) else (
    cd > %pth%
)
:getadmin
    set vbs=%temp%\getadmin.vbs
    echo Set UAC = CreateObject^("Shell.Application"^) >> "%vbs%"
    echo UAC.ShellExecute "%~s0", "payload %~sdp0 %*", "", "runas", 1 >> "%vbs%"
    "%temp%\getadmin.vbs"
    del "%temp%\getadmin.vbs"
goto :eof
:payload
set /p npath=<%pth%
cd %npath%
del "%pth%"
:script
python __main__.py
echo.
set /p a=Press Enter to exit...
