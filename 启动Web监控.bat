@echo off
chcp 65001 >nul
echo ========================================
echo     电脑状态监控工具 - Web 版
echo ========================================
echo.
echo 正在启动 Web 服务器...
echo.
python web_monitor.py
pause
