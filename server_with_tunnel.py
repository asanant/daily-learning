#!/usr/bin/env python3
"""
学习系统本地网页服务器 + 公网穿透
使用 localhost.run 免费隧道（无需注册）
"""

import http.server
import socketserver
import os
import json
import threading
import subprocess
import sys
from datetime import datetime
import socket

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class LearningHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.path = '/index.html'
        return super().do_GET()
    
    def log_message(self, format, *args):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {args[0]}")

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        return s.getsockname()[0]
    finally:
        s.close()

def start_server():
    with socketserver.TCPServer(("", PORT), LearningHandler) as httpd:
        print(f"学习系统服务器启动")
        print(f"本地访问: http://localhost:{PORT}")
        print(f"局域网访问: http://{get_local_ip()}:{PORT}")
        httpd.serve_forever()

def start_tunnel():
    """使用 localhost.run 免费隧道"""
    import urllib.request
    import json
    
    print("\n正在连接公网隧道...")
    
    # 使用 SSH 隧道方式
    try:
        # 检查 ssh 是否可用
        result = subprocess.run(['ssh', '-V'], capture_output=True, text=True)
        if result.returncode != 0:
            print("SSH 不可用，跳过公网隧道")
            return
        
        # 启动 SSH 隧道
        cmd = [
            'ssh', '-o', 'StrictHostKeyChecking=no',
            '-R', f'80:localhost:{PORT}',
            'localhost.run'
        ]
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        print("等待公网链接生成...")
        
        for line in process.stdout:
            line = line.strip()
            if 'https://' in line:
                print(f"\n{'='*50}")
                print(f"公网访问链接: {line}")
                print(f"{'='*50}")
                break
            
    except Exception as e:
        print(f"隧道启动失败: {e}")
        print("请使用局域网访问")

if __name__ == "__main__":
    # 启动服务器
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    # 启动隧道
    start_tunnel()
    
    try:
        while True:
            import time
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n服务器已停止")
        sys.exit(0)
