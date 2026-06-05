#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
电脑状态监控工具
实时监控 CPU、内存、磁盘、网络等系统状态
"""

import psutil
import time
import os
import sys
from datetime import datetime
from collections import deque
import json


class SystemMonitor:
    """系统监控类"""

    def __init__(self, history_size=60):
        """
        初始化监控器
        :param history_size: 历史记录保存的数据点数量
        """
        self.history_size = history_size
        self.cpu_history = deque(maxlen=history_size)
        self.memory_history = deque(maxlen=history_size)
        self.network_history = deque(maxlen=history_size)
        self.last_network_io = psutil.net_io_counters()
        self.last_disk_io = psutil.disk_io_counters()
        self.start_time = time.time()

    def clear_screen(self):
        """清屏"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def get_cpu_info(self):
        """获取 CPU 信息"""
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        cpu_freq = psutil.cpu_freq()
        per_cpu = psutil.cpu_percent(interval=1, percpu=True)

        return {
            'percent': cpu_percent,
            'count': cpu_count,
            'frequency': cpu_freq.current if cpu_freq else 0,
            'per_cpu': per_cpu
        }

    def get_memory_info(self):
        """获取内存信息"""
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()

        return {
            'total': memory.total,
            'available': memory.available,
            'used': memory.used,
            'percent': memory.percent,
            'swap_total': swap.total,
            'swap_used': swap.used,
            'swap_percent': swap.percent
        }

    def get_disk_info(self):
        """获取磁盘信息"""
        partitions = psutil.disk_partitions()
        disk_info = []

        for partition in partitions:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disk_info.append({
                    'device': partition.device,
                    'mountpoint': partition.mountpoint,
                    'fstype': partition.fstype,
                    'total': usage.total,
                    'used': usage.used,
                    'free': usage.free,
                    'percent': usage.percent
                })
            except PermissionError:
                continue

        # 磁盘 I/O
        disk_io = psutil.disk_io_counters()
        if disk_io and self.last_disk_io:
            read_speed = (disk_io.read_bytes - self.last_disk_io.read_bytes)
            write_speed = (disk_io.write_bytes - self.last_disk_io.write_bytes)
            self.last_disk_io = disk_io
        else:
            read_speed = 0
            write_speed = 0

        return {
            'partitions': disk_info,
            'read_speed': read_speed,
            'write_speed': write_speed
        }

    def get_network_info(self):
        """获取网络信息"""
        net_io = psutil.net_io_counters()

        # 计算网络速度
        if self.last_network_io:
            upload_speed = net_io.bytes_sent - self.last_network_io.bytes_sent
            download_speed = net_io.bytes_recv - self.last_network_io.bytes_recv
        else:
            upload_speed = 0
            download_speed = 0

        self.last_network_io = net_io

        # 获取网络连接
        connections = len(psutil.net_connections())

        return {
            'bytes_sent': net_io.bytes_sent,
            'bytes_recv': net_io.bytes_recv,
            'upload_speed': upload_speed,
            'download_speed': download_speed,
            'connections': connections
        }

    def get_process_info(self, top_n=5):
        """获取进程信息"""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        # 按 CPU 使用率排序
        processes.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)

        return processes[:top_n]

    def bytes_to_human_readable(self, bytes_value):
        """将字节转换为可读格式"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.2f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.2f} PB"

    def draw_progress_bar(self, percent, width=50):
        """绘制进度条"""
        filled = int(width * percent / 100)
        bar = '█' * filled + '░' * (width - filled)
        return f"[{bar}] {percent:.1f}%"

    def display_system_info(self):
        """显示系统信息"""
        self.clear_screen()

        # 标题
        print("=" * 80)
        print(" " * 25 + "电脑状态监控工具")
        print("=" * 80)
        print(f"监控时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"运行时长: {int(time.time() - self.start_time)} 秒")
        print("=" * 80)

        # CPU 信息
        cpu_info = self.get_cpu_info()
        self.cpu_history.append(cpu_info['percent'])
        print(f"\n【CPU 信息】")
        print(f"核心数: {cpu_info['count']} 核")
        print(f"频率: {cpu_info['frequency']:.2f} MHz")
        print(f"总体使用率: {self.draw_progress_bar(cpu_info['percent'])}")
        print(f"各核心使用率:")
        for i, usage in enumerate(cpu_info['per_cpu']):
            print(f"  核心 {i}: {self.draw_progress_bar(usage, 30)}")

        # 内存信息
        mem_info = self.get_memory_info()
        self.memory_history.append(mem_info['percent'])
        print(f"\n【内存信息】")
        print(f"总内存: {self.bytes_to_human_readable(mem_info['total'])}")
        print(f"已使用: {self.bytes_to_human_readable(mem_info['used'])}")
        print(f"可用: {self.bytes_to_human_readable(mem_info['available'])}")
        print(f"使用率: {self.draw_progress_bar(mem_info['percent'])}")
        if mem_info['swap_total'] > 0:
            print(f"\n虚拟内存:")
            print(f"  总量: {self.bytes_to_human_readable(mem_info['swap_total'])}")
            print(f"  已使用: {self.bytes_to_human_readable(mem_info['swap_used'])}")
            print(f"  使用率: {self.draw_progress_bar(mem_info['swap_percent'], 30)}")

        # 磁盘信息
        disk_info = self.get_disk_info()
        print(f"\n【磁盘信息】")
        for partition in disk_info['partitions']:
            print(f"\n设备: {partition['device']}")
            print(f"  挂载点: {partition['mountpoint']}")
            print(f"  文件系统: {partition['fstype']}")
            print(f"  总容量: {self.bytes_to_human_readable(partition['total'])}")
            print(f"  已使用: {self.bytes_to_human_readable(partition['used'])}")
            print(f"  剩余: {self.bytes_to_human_readable(partition['free'])}")
            print(f"  使用率: {self.draw_progress_bar(partition['percent'], 30)}")

        print(f"\n磁盘 I/O:")
        print(f"  读取速度: {self.bytes_to_human_readable(disk_info['read_speed'])}/s")
        print(f"  写入速度: {self.bytes_to_human_readable(disk_info['write_speed'])}/s")

        # 网络信息
        net_info = self.get_network_info()
        self.network_history.append((net_info['upload_speed'], net_info['download_speed']))
        print(f"\n【网络信息】")
        print(f"总上传: {self.bytes_to_human_readable(net_info['bytes_sent'])}")
        print(f"总下载: {self.bytes_to_human_readable(net_info['bytes_recv'])}")
        print(f"上传速度: {self.bytes_to_human_readable(net_info['upload_speed'])}/s")
        print(f"下载速度: {self.bytes_to_human_readable(net_info['download_speed'])}/s")
        print(f"活动连接: {net_info['connections']}")

        # 进程信息
        processes = self.get_process_info(5)
        print(f"\n【Top 5 进程 (按 CPU 使用率)】")
        print(f"{'PID':<10} {'进程名':<30} {'CPU %':<10} {'内存 %':<10}")
        print("-" * 60)
        for proc in processes:
            print(f"{proc['pid']:<10} {proc['name'][:28]:<30} {proc['cpu_percent'] or 0:<10.1f} {proc['memory_percent'] or 0:<10.1f}")

        # 提示
        print("\n" + "=" * 80)
        print("按 Ctrl+C 退出监控")
        print("=" * 80)

    def save_snapshot(self, filename='system_snapshot.json'):
        """保存当前系统状态快照"""
        snapshot = {
            'timestamp': datetime.now().isoformat(),
            'cpu': self.get_cpu_info(),
            'memory': self.get_memory_info(),
            'disk': self.get_disk_info(),
            'network': self.get_network_info(),
            'processes': self.get_process_info(10)
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(snapshot, f, indent=2, ensure_ascii=False)

        print(f"\n快照已保存到: {filename}")

    def run(self, interval=2):
        """
        运行监控器
        :param interval: 刷新间隔（秒）
        """
        print("正在启动系统监控...")
        print("按 Ctrl+C 退出")
        time.sleep(2)

        try:
            while True:
                self.display_system_info()
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n\n正在退出监控...")
            # 保存退出时的快照
            self.save_snapshot(f"snapshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
            print("监控已停止")
            sys.exit(0)


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='电脑状态监控工具')
    parser.add_argument('-i', '--interval', type=int, default=2,
                        help='刷新间隔（秒），默认 2 秒')
    parser.add_argument('-s', '--snapshot', action='store_true',
                        help='只保存当前快照，不进入监控模式')
    parser.add_argument('-o', '--output', type=str, default='system_snapshot.json',
                        help='快照输出文件名')

    args = parser.parse_args()

    monitor = SystemMonitor()

    if args.snapshot:
        # 只保存快照
        print("正在获取系统状态...")
        time.sleep(1)  # 等待获取准确的 CPU 数据
        monitor.save_snapshot(args.output)
    else:
        # 运行监控
        monitor.run(interval=args.interval)


if __name__ == '__main__':
    main()


    def save_snapshot(self, filename='system_snapshot.json'):
        """保存当前系统状态快照"""
        snapshot = {
            'timestamp': datetime.now().isoformat(),
            'cpu': self.get_cpu_info(),
            'memory': self.get_memory_info(),
            'disk': self.get_disk_info(),
            'network': self.get_network_info(),
            'processes': self.get_process_info(10)
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(snapshot, f, indent=2, ensure_ascii=False)

        print(f"\n快照已保存到: {filename}")

    def run(self, interval=2):
        """
        运行监控器
        :param interval: 刷新间隔（秒）
        """
        print("正在启动系统监控...")
        print("按 Ctrl+C 退出")
        time.sleep(2)

        try:
            while True:
                self.display_system_info()
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n\n正在退出监控...")
            # 保存退出时的快照
            self.save_snapshot(f"snapshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
            print("监控已停止")
            sys.exit(0)
