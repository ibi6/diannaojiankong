@echo off
chcp 65001 >nul
echo ========================================
echo     电脑状态监控工具
echo ========================================
echo.
python system_monitor.py %*
