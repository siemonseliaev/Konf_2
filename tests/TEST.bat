@echo off
chcp 65001 >nul
cd /d "%~dp0.."

python src\Konf_2.py --vfs my_vfs.tar --script tests\startup.txt

pause
