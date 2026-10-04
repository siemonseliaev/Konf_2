@echo off
chcp 65001 >nul
cd /d "%~dp0.."

python src\main.py --vfs my_vfs.tar --script tests\startup.txt

pause
