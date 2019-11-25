@echo off
:install
set /P PYTHONINSTALL=Do you want to install Python [Y/N]?
if %PYTHONINSTALL%==Y goto Python
if %PYTHONINSTALL%==y goto Python
if %PYTHONINSTALL%==N goto Kivy
if %PYTHONINSTALL%==n goto Kivy
:Python
start /w python-install.bat
:Kivy
start /w kivy-install.bat
start kreat-launcher.bat