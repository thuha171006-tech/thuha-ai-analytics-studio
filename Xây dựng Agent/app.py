"""
Web Server Application for Thu Hà Sales Campaign & Financial P&L Evaluation Agent
Provides:
- Web Dashboard interface
- REST APIs for Pipeline execution, Google Sheet ingestion, and HITL overrides
"""

import os
import sys
import json
import webbrowser
from http.server import HTTPServer, ThreadingHTTPServer, BaseHTTPRequestHandler
import urllib.parse

import pandas as pd
from core.data_loader import DataLoader
from core.agent_engine import SalesEvaluationAgent, sanitize_for_json

PORT = 8050
agent_instance = SalesEvaluationAgent()

def safe_json_dumps(obj, **kwargs) -> str:
    """Serialize object to strictly valid JSON string without NaN, inf, NaT."""
    clean_obj = sanitize_for_json(obj)
    return json.dumps(clean_obj, ensure_ascii=False, allow_nan=False, **kwargs)

def safe_decode(post_data: bytes) -> str:
    if not post_data:
        return ""
    for enc in ["utf-8", "utf-8-sig", "windows-1258", "cp1252"]:
        try:
            return post_data.decode(enc)
        except UnicodeDecodeError:
            continue
    return post_data.decode("utf-8", errors="replace")

class RequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200, content_type="application/json"):
        self.send_response(status)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers(200)

    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path

        if path == "/" or path == "/index.html":
            html_path = os.path.join(os.path.dirname(__file__), "ui", "index.html")
            if os.path.exists(html_path):
                self._set_headers(200, "text/html")
                with open(html_path, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self._set_headers(404, "text/plain")
                self.wfile.write(b"404 Not Found")
        
        elif os.path.exists(os.path.join(os.path.dirname(__file__), "ui", path.lstrip("/"))):
            file_path = os.path.join(os.path.dirname(__file__), "ui", path.lstrip("/"))
            if os.path.isfile(file_path):
                ext = os.path.splitext(file_path)[1].lower()
                mime_map = {
                    ".jpg": "image/jpeg",
                    ".jpeg": "image/jpeg",
                    ".png": "image/png",
                    ".svg": "image/svg+xml",
                    ".gif": "image/gif",
                    ".webp": "image/webp",
                    ".ico": "image/x-icon",
                    ".css": "text/css",
                    ".js": "application/javascript"
                }
                mime = mime_map.get(ext, "application/octet-stream")
                self._set_headers(200, mime)
                with open(file_path, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self._set_headers(404, "text/plain")
                self.wfile.write(b"404 Not Found")
        
        elif path == "/api/status":
            self._set_headers(200)
            self.wfile.write(safe_json_dumps({"status": "RUNNING", "port": PORT}).encode("utf-8"))

        elif path == "/api/export_json":
            self._set_headers(200, "application/json")
            self.send_header("Content-Disposition", "attachment; filename=Bao_Cao_Danh_Gia_Hieu_Qua_ThuHa.json")
            summary = agent_instance.get_summary()
            self.wfile.write(safe_json_dumps(summary, indent=2).encode("utf-8"))

        elif path == "/api/export_excel":
            from core.excel_exporter import ExcelReportExporter
            summary = agent_instance.get_summary()
            excel_path = ExcelReportExporter.export(summary, "exports/Bao_Cao_Hieu_Qua_Ban_Hang_ThuHa.xlsx")
            with open(excel_path, "rb") as f:
                data = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            self.send_header("Content-Disposition", "attachment; filename=Bao_Cao_Hieu_Qua_Ban_Hang_ThuHa.xlsx")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        elif path == "/api/export_html_pnl":
            from core.html_exporter import StandaloneHtmlExporter
            summary = agent_instance.get_summary()
            html_content = StandaloneHtmlExporter.generate_pnl_report(summary)
            data = html_content.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Disposition", "attachment; filename=Bao_Cao_Chi_Tiet_PnL_ThuHa.html")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        elif path == "/api/export_html_dashboard":
            from core.html_exporter import StandaloneHtmlExporter
            summary = agent_instance.get_summary()
            html_content = StandaloneHtmlExporter.generate_dashboard_overview(summary)
            data = html_content.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Disposition", "attachment; filename=Dashboard_Tong_Quan_ThuHa.html")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        else:
            self._set_headers(404, "text/plain")
            self.wfile.write(b"404 Not Found")

    def do_POST(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path

        if path == "/api/run_pipeline":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)
            
            try:
                params = json.loads(safe_decode(post_data))
            except Exception:
                params = {}

            scenario = params.get("scenario")
            multi_touch_rule = params.get("multi_touch_rule", "PROPORTIONAL")
            overhead_method = params.get("overhead_method", "REVENUE_SHARE")
            gsheet_url = params.get("gsheet_url")
            file_base64 = params.get("file_base64")
            file_name = params.get("file_name", "")
            human_overrides = params.get("human_overrides", {})
            business_context = params.get("business_context")

            from datetime import datetime
            if not (file_base64 and file_base64.strip()) and not (gsheet_url and gsheet_url.strip()) and not scenario:
                self._set_headers(200)
                empty_res = {
                    "status": "AWAITING_INPUT",
                    "message": "Chưa có dữ liệu. Vui lòng tải tệp Excel hoặc CSV lên.",
                    "summary_kpis": {
                        "total_campaigns": 0,
                        "total_net_revenue": 0,
                        "total_contribution_margin": 0,
                        "total_campaign_costs": 0,
                        "total_exceptions_detected": 0
                    },
                    "financial_kpis": {
                        "total_gross_revenue": 0,
                        "total_discount_amount": 0,
                        "total_return_amount": 0,
                        "total_net_revenue": 0,
                        "total_cogs": 0,
                        "total_gross_profit": 0,
                        "total_campaign_costs": 0,
                        "total_contribution_margin": 0,
                        "gross_margin_pct": 0,
                        "cm_pct": 0,
                        "aov": 0,
                        "return_rate": 0,
                        "roas": 0,
                        "roi": 0
                    },
                    "dataset_meta": {
                        "dataset_name": "-- Chưa tải dữ liệu --",
                        "total_rows": 0,
                        "total_cols": 0,
                        "numeric_cols_count": 0
                    },
                    "column_profiling": [],
                    "contextual_qa": [],
                    "channel_breakdown": [],
                    "product_breakdown": [],
                    "timeline_breakdown": [],
                    "pnl_table": [],
                    "cleaned_orders_table": [],
                    "exceptions_list": [],
                    "recommendations": [],
                    "audit_trail": [
                        {
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "step": "INITIALIZATION",
                            "action": "AWAIT_DATA",
                            "tool_name": "AGENT_CORE",
                            "message": "Thu Hà AI Analytics Studio sẵn sàng. Đang chờ người dùng tải tệp dữ liệu lên để bắt đầu phân tích.",
                            "level": "INFO"
                        }
                    ],
                    "ai_executive_insights": "Hệ thống đang ở trạng thái chờ. Vui lòng tải tệp dữ liệu lên ở Bước 1 để AI Agent bắt đầu phân tích và tính toán P&L."
                }
                self.wfile.write(safe_json_dumps(empty_res).encode("utf-8"))
                return

            if business_context is None:
                business_context = {}
            if file_name:
                business_context["file_name"] = file_name
                if not business_context.get("project_name"):
                    business_context["project_name"] = file_name

            try:
                if file_base64 and file_base64.strip():
                    import base64
                    import io
                    decoded = base64.b64decode(file_base64)
                    file_buffer = io.BytesIO(decoded)
                    print(f"[PIPELINE] Nhận file tải lên: {file_name} (Bytes: {len(decoded)})")
                    if file_name.lower().endswith(".csv"):
                        raw_data = DataLoader.load_from_csv(file_buffer)
                    else:
                        raw_data = DataLoader.load_from_excel(file_buffer)
                    print(f"[PIPELINE] Nạp dữ liệu file thành công: {list(raw_data.keys())}, số dòng đơn: {len(raw_data.get('transactions', []))}")
                elif gsheet_url and gsheet_url.strip():
                    print(f"[PIPELINE] Nạp dữ liệu từ Google Sheet: {gsheet_url}")
                    raw_data = DataLoader.load_from_google_sheet(gsheet_url)
                else:
                    print(f"[PIPELINE] Chạy kịch bản mẫu: {scenario}")
                    raw_data = DataLoader.load_scenario(scenario)

                summary = agent_instance.run_pipeline(
                    raw_data=raw_data,
                    multi_touch_rule=multi_touch_rule,
                    overhead_method=overhead_method,
                    human_overrides=human_overrides,
                    business_context=business_context
                )
                self._set_headers(200)
                self.wfile.write(safe_json_dumps(summary).encode("utf-8"))
            except Exception as e:
                import traceback
                traceback.print_exc()
                self._set_headers(500)
                self.wfile.write(safe_json_dumps({"error": str(e)}).encode("utf-8"))

        elif path == "/api/save_context":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)
            try:
                payload = json.loads(safe_decode(post_data)) if post_data else {}
                agent_instance.business_context.update(payload)
                self._set_headers(200)
                self.wfile.write(safe_json_dumps({"success": True, "business_context": agent_instance.business_context}).encode("utf-8"))
            except Exception as e:
                import traceback
                traceback.print_exc()
                self._set_headers(500)
                self.wfile.write(safe_json_dumps({"error": str(e)}).encode("utf-8"))

        elif path == "/api/save_custom_charts":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)
            try:
                payload = json.loads(safe_decode(post_data)) if post_data else {}
                agent_instance.custom_charts = payload.get("custom_charts", [])
                self._set_headers(200)
                self.wfile.write(safe_json_dumps({"success": True, "count": len(agent_instance.custom_charts)}).encode("utf-8"))
            except Exception as e:
                import traceback
                traceback.print_exc()
                self._set_headers(500)
                self.wfile.write(safe_json_dumps({"error": str(e)}).encode("utf-8"))

        elif path == "/api/chat":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)
            query = ""
            try:
                payload = json.loads(safe_decode(post_data)) if post_data else {}
                query = payload.get("query", "").strip()
                if not query:
                    self._set_headers(200)
                    self.wfile.write(safe_json_dumps({"answer": "Vui lòng nhập câu hỏi để tôi hỗ trợ phân tích."}).encode("utf-8"))
                    return

                summary = agent_instance.get_summary()
                print(f"[COPILOT] Nhận câu hỏi: '{query}'", flush=True)
                answer = agent_instance.gemini_service.chat_with_copilot(query, summary)
                print(f"[COPILOT] Phản hồi thành công ({len(answer)} ký tự)", flush=True)
                self._set_headers(200)
                self.wfile.write(safe_json_dumps({"answer": answer}).encode("utf-8"))
            except Exception as e:
                import traceback
                traceback.print_exc()
                self._set_headers(200)
                fallback_ans = f"Trợ lý AI đã ghi nhận câu hỏi: '{query}'. Hệ thống đang phân tích lại dữ liệu P&L và ngoại lệ."
                self.wfile.write(safe_json_dumps({"answer": fallback_ans}).encode("utf-8"))

        else:
            self._set_headers(404, "text/plain")
            self.wfile.write(b"404 Not Found")

def run_server():
    server_address = ("0.0.0.0", PORT)
    httpd = ThreadingHTTPServer(server_address, RequestHandler)
    print(f"==================================================================", flush=True)
    print(f" Thu Hà • AI Data Analyst & Business Intelligence Studio", flush=True)
    print(f" Server đang chạy tại: http://127.0.0.1:{PORT}", flush=True)
    print(f"==================================================================", flush=True)
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()

