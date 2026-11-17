import sys
import os

# Thêm đường dẫn thư mục gốc để Vercel serverless function tìm thấy app.py và core/
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from app import RequestHandler

# Vercel Python runtime yêu cầu class handler kế thừa BaseHTTPRequestHandler
class handler(RequestHandler):
    pass
