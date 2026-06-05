#!/usr/bin/env python3
"""
学习系统本地网页服务器
访问地址: http://192.168.31.61:8080
"""

import http.server
import socketserver
import os
import json
from datetime import datetime

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

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), LearningHandler) as httpd:
        print(f"学习系统服务器启动")
        print(f"访问地址: http://192.168.31.61:{PORT}")
        print(f"本地访问: http://localhost:{PORT}")
        print(f"按 Ctrl+C 停止")
        httpd.serve_forever()
