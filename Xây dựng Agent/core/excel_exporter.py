"""
Excel Report Exporter for Sales Campaign Evaluation Agent • Thu Hà Studio
Generates an executive-ready, multi-sheet, beautifully formatted Excel workbook:
- Sheet 1: Bảng Tổng Hợp P&L và Hiệu Quả (with KPI headers, currency & percentage formatting)
- Sheet 2: Chi Tiết Gán Đơn & Khử Trùng (Order attribution & return adjustments)
- Sheet 3: Danh Sách Ngoại Lệ & HITL (Exceptions requiring human intervention)
- Sheet 4: Nhật Ký Truy Vết Thực Thi (Audit Trail of all agent actions)
"""

import os
import pandas as pd
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

class ExcelReportExporter:
    @staticmethod
    def export(summary: dict, output_path: str = "exports/Bao_Cao_Hieu_Qua_Ban_Hang_ThuHa.xlsx") -> str:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # 1. Prepare DataFrames
        df_pnl = pd.DataFrame(summary.get("pnl_table", []))
        df_orders = pd.DataFrame(summary.get("attributed_orders_sample", []))
        df_exceptions = pd.DataFrame(summary.get("exceptions_list", []))
        df_audit = pd.DataFrame(summary.get("audit_trail", []))

        # Reorder / Select clean columns for PnL
        pnl_cols = [
            "campaign_id", "campaign_name", "orders_count", "gross_revenue", 
            "returns_value", "net_revenue", "cogs", "discount_cost", 
            "direct_cost", "allocated_overhead", "contribution_margin", 
            "contribution_margin_pct", "roi_pct"
        ]
        df_pnl_clean = df_pnl[[c for c in pnl_cols if c in df_pnl.columns]].copy()
        df_pnl_clean.rename(columns={
            "campaign_id": "Mã CT",
            "campaign_name": "Tên Chương Trình",
            "orders_count": "Số Đơn",
            "gross_revenue": "Doanh Thu Gộp",
            "returns_value": "Hàng Trả Lại",
            "net_revenue": "Doanh Thu Thuần",
            "cogs": "Giá Vốn (COGS)",
            "discount_cost": "Tiền Voucher",
            "direct_cost": "Chi Phí Trực Tiếp",
            "allocated_overhead": "Chi Phí Phân Bổ",
            "contribution_margin": "Biên Đóng Góp (CM)",
            "contribution_margin_pct": "Biên Đóng Góp %",
            "roi_pct": "ROI %"
        }, inplace=True)

        # 2. Write to Excel
        with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
            df_pnl_clean.to_excel(writer, sheet_name="Tong_Hop_PnL", index=False)
            if not df_orders.empty:
                df_orders.to_excel(writer, sheet_name="Phan_Bo_Don_Hang", index=False)
            if not df_exceptions.empty:
                df_exceptions.to_excel(writer, sheet_name="Danh_Sach_Ngoai_Le", index=False)
            if not df_audit.empty:
                df_audit.to_excel(writer, sheet_name="Nhat_Ky_Audit_Trail", index=False)
            
            # Sheet 5: Báo cáo Vấn đề - Giải pháp thực thi chi tiết
            matrix = summary.get("problem_solution_matrix", [])
            if matrix:
                df_matrix = pd.DataFrame([{
                    "Mã Vấn Đề": m.get("id"),
                    "Mức Độ": m.get("severity"),
                    "Tiêu Đề Vấn Đề": m.get("title"),
                    "Thực Trạng & Bằng Chứng Số Liệu": f"{m.get('problem')} ({m.get('evidence')})",
                    "Nguyên Nhân Cốt Lõi": m.get("root_cause"),
                    "Giải Pháp Khẩn Cấp (24h)": m.get("urgent_solution"),
                    "Giải Pháp Tối Ưu (1-2 Tuần)": m.get("medium_solution"),
                    "Giải Pháp Chiến Lược (A/B)": m.get("strategic_solution"),
                    "Kỳ Vọng Tác Động": m.get("expected_impact")
                } for m in matrix])
                df_matrix.to_excel(writer, sheet_name="Van_De_Giai_Phap", index=False)

        # 3. Apply Professional Styling with openpyxl
        import openpyxl
        wb = openpyxl.load_workbook(output_path)
        
        # Style Sheet 1: Tong_Hop_PnL
        ws_pnl = wb["Tong_Hop_PnL"]
        
        # Colors
        header_fill = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid") # Navy
        header_font = Font(name="Arial", size=10, bold=True, color="FFFFFF")
        regular_font = Font(name="Arial", size=10)
        bold_font = Font(name="Arial", size=10, bold=True)
        green_font = Font(name="Arial", size=10, bold=True, color="047857") # Emerald
        red_font = Font(name="Arial", size=10, bold=True, color="B91C1C")   # Red
        
        thin_border = Border(
            left=Side(style="thin", color="E2E8F0"),
            right=Side(style="thin", color="E2E8F0"),
            top=Side(style="thin", color="E2E8F0"),
            bottom=Side(style="thin", color="E2E8F0")
        )

        # Style header row
        for cell in ws_pnl[1]:
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

        # Style data rows
        for row in ws_pnl.iter_rows(min_row=2, max_row=ws_pnl.max_row):
            for cell in row:
                cell.font = regular_font
                cell.border = thin_border
                col_name = ws_pnl.cell(1, cell.column).value
                
                # Format numbers
                if col_name in ["Doanh Thu Gộp", "Hàng Trả Lại", "Doanh Thu Thuần", "Giá Vốn (COGS)", "Tiền Voucher", "Chi Phí Trực Tiếp", "Chi Phí Phân Bổ", "Biên Đóng Góp (CM)"]:
                    cell.number_format = '#,##0" đ"'
                    cell.alignment = Alignment(horizontal="right")
                elif col_name in ["Biên Đóng Góp %", "ROI %"]:
                    cell.number_format = '0.00"%"'
                    cell.alignment = Alignment(horizontal="right")
                elif col_name == "Số Đơn":
                    cell.alignment = Alignment(horizontal="center")
                else:
                    cell.alignment = Alignment(horizontal="left")

                # Highlight Contribution Margin
                if col_name == "Biên Đóng Góp (CM)":
                    try:
                        val = float(cell.value)
                        cell.font = green_font if val >= 0 else red_font
                    except (ValueError, TypeError):
                        pass

        # Auto-adjust column width
        for ws in wb.worksheets:
            for col in ws.columns:
                max_len = max(len(str(cell.value or '')) for cell in col)
                col_letter = get_column_letter(col[0].column)
                ws.column_dimensions[col_letter].width = max(max_len + 3, 12)

        wb.save(output_path)
        return output_path

