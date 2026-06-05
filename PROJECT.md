# 项目文件说明

## 📁 文件结构

```
电脑状态监控工具/
├── system_monitor.py          # 命令行版本监控程序
├── web_monitor.py             # Web 版本监控服务器
├── requirements.txt           # Python 依赖列表
├── README.md                  # 项目文档
├── 启动监控.bat               # Windows 快速启动脚本（命令行版）
├── 启动Web监控.bat            # Windows 快速启动脚本（Web版）
├── 保存快照.bat               # Windows 快速保存快照脚本
└── templates/
    └── index.html             # Web 界面 HTML 页面
```

## 🚀 快速开始

1. 安装依赖：`pip install -r requirements.txt`
2. 启动 Web 版本：`python web_monitor.py`
3. 浏览器访问：http://127.0.0.1:5000

## 技术栈

- **后端**：Python + Flask + psutil
- **前端**：HTML5 + CSS3 + JavaScript + Chart.js
- **监控指标**：CPU、内存、磁盘、网络、进程
