@echo off
chcp 65001 >nul
echo 正在生成系统快照...
python system_monitor.py -s -o snapshot_%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%.json
echo.
pause
