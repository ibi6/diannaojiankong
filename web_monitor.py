#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
电脑状态监控工具 - Web 服务器
提供 REST API 和 Web 前端界面
"""

from flask import Flask, jsonify, render_template, send_from_directory
from flask_cors import CORS
import psutil
import time
from datetime import datetime
from collections import deque
import threading
import os

app = Flask(__name__)
CORS(app)

# 全局变量存储历史数据
history_data = {
    'cpu': deque(maxlen=60),
    'memory': deque(maxlen=60),
    'network': deque(maxlen=60),
    'disk_io': deque(maxlen=60),
    'timestamps': deque(maxlen=60)
}

last_network_io = None
last_disk_io = None


def bytes_to_human_readable(bytes_value):
    """将字节转换为可读格式"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} PB"


def get_system_info():
    """获取系统信息"""
    global last_network_io, last_disk_io

    # CPU 信息
    cpu_percent = psutil.cpu_percent(interval=0.1)
    cpu_per_core = psutil.cpu_percent(interval=0.1, percpu=True)
    cpu_freq = psutil.cpu_freq()

    # 内存信息
    memory = psutil.virtual_memory()
    swap = psutil.swap_memory()

    # 磁盘信息
    disk_partitions = []
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disk_partitions.append({
                'device': partition.device,
                'mountpoint': partition.mountpoint,
                'fstype': partition.fstype,
                'total': usage.total,
                'used': usage.used,
                'free': usage.free,
                'percent': usage.percent,
                'total_readable': bytes_to_human_readable(usage.total),
                'used_readable': bytes_to_human_readable(usage.used),
                'free_readable': bytes_to_human_readable(usage.free)
            })
        except PermissionError:
            continue

    # 磁盘 I/O
    disk_io = psutil.disk_io_counters()
    if disk_io and last_disk_io:
        disk_read_speed = disk_io.read_bytes - last_disk_io.read_bytes
        disk_write_speed = disk_io.write_bytes - last_disk_io.write_bytes
    else:
        disk_read_speed = 0
        disk_write_speed = 0
    last_disk_io = disk_io

    # 网络信息
    net_io = psutil.net_io_counters()
    if last_network_io:
        upload_speed = net_io.bytes_sent - last_network_io.bytes_sent
        download_speed = net_io.bytes_recv - last_network_io.bytes_recv
    else:
        upload_speed = 0
        download_speed = 0
    last_network_io = net_io

    # 进程信息
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
        try:
            info = proc.info
            if info['cpu_percent'] is not None and info['cpu_percent'] > 0:
                processes.append(info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    processes.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)
    top_processes = processes[:10]

    return {
        'timestamp': datetime.now().isoformat(),
        'cpu': {
            'percent': cpu_percent,
            'per_core': cpu_per_core,
            'count': psutil.cpu_count(),
            'frequency': cpu_freq.current if cpu_freq else 0
        },
        'memory': {
            'total': memory.total,
            'available': memory.available,
            'used': memory.used,
            'percent': memory.percent,
            'swap_total': swap.total,
            'swap_used': swap.used,
            'swap_percent': swap.percent,
            'total_readable': bytes_to_human_readable(memory.total),
            'used_readable': bytes_to_human_readable(memory.used),
            'available_readable': bytes_to_human_readable(memory.available)
        },
        'disk': {
            'partitions': disk_partitions,
            'read_speed': disk_read_speed,
            'write_speed': disk_write_speed,
            'read_speed_readable': bytes_to_human_readable(disk_read_speed) + '/s',
            'write_speed_readable': bytes_to_human_readable(disk_write_speed) + '/s'
        },
        'network': {
            'bytes_sent': net_io.bytes_sent,
            'bytes_recv': net_io.bytes_recv,
            'upload_speed': upload_speed,
            'download_speed': download_speed,
            'connections': len(psutil.net_connections()),
            'upload_speed_readable': bytes_to_human_readable(upload_speed) + '/s',
            'download_speed_readable': bytes_to_human_readable(download_speed) + '/s',
            'bytes_sent_readable': bytes_to_human_readable(net_io.bytes_sent),
            'bytes_recv_readable': bytes_to_human_readable(net_io.bytes_recv)
        },
        'processes': top_processes
    }


def collect_history_data():
    """后台线程收集历史数据"""
    while True:
        try:
            data = get_system_info()
            history_data['cpu'].append(data['cpu']['percent'])
            history_data['memory'].append(data['memory']['percent'])
            history_data['network'].append({
                'upload': data['network']['upload_speed'],
                'download': data['network']['download_speed']
            })
            history_data['disk_io'].append({
                'read': data['disk']['read_speed'],
                'write': data['disk']['write_speed']
            })
            history_data['timestamps'].append(data['timestamp'])
            time.sleep(1)
        except Exception as e:
            print(f"Error collecting history: {e}")
            time.sleep(1)


@app.route('/')
def index():
    """主页"""
    return render_template('index.html')


@app.route('/api/system')
def api_system():
    """获取当前系统状态"""
    return jsonify(get_system_info())


@app.route('/api/history')
def api_history():
    """获取历史数据"""
    return jsonify({
        'cpu': list(history_data['cpu']),
        'memory': list(history_data['memory']),
        'network': list(history_data['network']),
        'disk_io': list(history_data['disk_io']),
        'timestamps': list(history_data['timestamps'])
    })


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='电脑状态监控工具 - Web 服务器')
    parser.add_argument('-p', '--port', type=int, default=5000,
                        help='Web 服务器端口，默认 5000')
    parser.add_argument('--host', type=str, default='127.0.0.1',
                        help='Web 服务器地址，默认 127.0.0.1')

    args = parser.parse_args()

    # 启动后台数据收集线程
    thread = threading.Thread(target=collect_history_data, daemon=True)
    thread.start()

    print(f"Web 监控服务器启动中...")
    print(f"访问地址: http://{args.host}:{args.port}")
    print(f"按 Ctrl+C 停止服务器")

    app.run(host=args.host, port=args.port, debug=False)
