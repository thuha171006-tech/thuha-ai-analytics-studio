"""
Data Loader Module for Thu Hà AI Analytics Studio - Multi-Project Sales Evaluation Agent
Supports:
1. Multi-sheet Excel files (.xlsx, .xls)
2. Individual CSV files
3. Google Sheets Link (XLSX export or CSV gviz export)
4. Flexible column alias mapping (English / Vietnamese)
"""

import os
import re
import urllib.request
import urllib.parse
import pandas as pd
import numpy as np

# Column Aliases Mapping for robust ingestion
COLUMN_MAPPINGS = {
    # Transactions table
    "order_id": [
        "order_id", "mã đơn hàng", "ma don hang", "mã hóa đơn", "ma hoa don", 
        "số hóa đơn", "so hoa don", "mã giao dịch", "ma giao dich", "giao dịch", "giao dich",
        "mã đh", "ma dh", "madon", "order id", "ma_don", "mã đơn", "ma don", 
        "order", "invoice", "id_don_hang", "id_don", "id", "code"
    ],
    "date": [
        "date", "ngày", "ngay giao dich", "ngay", "created_date", "order_date", 
        "ngày đặt", "ngay dat", "ngày lập", "ngay lap", "thời gian", "thoi gian", 
        "ngay_tao", "thời điểm", "thoi diem"
    ],
    "channel": [
        "channel", "kênh", "kenh", "kênh bán", "kenh ban", "sàn", "san", 
        "nền tảng", "nen tang", "chi nhánh", "chi nhanh", "cửa hàng", "cua hang", "platform", "store"
    ],
    "region": [
        "region", "khu vực", "khu vuc", "vùng", "vung", "miền", "mien", 
        "địa bàn", "dia ban", "khu_vuc", "tỉnh", "tinh", "thành phố", "thanh pho", "location", "area"
    ],
    "product_id": [
        "product_id", "mã sản phẩm", "ma san pham", "masp", "item_code", "sku", 
        "mã hàng", "ma hang", "product id", "mặt hàng", "mat hang", "hàng hóa", "hang hoa", 
        "tên sản phẩm", "ten san pham", "tên sp", "ten sp", "tên hàng", "ten hang", 
        "sản phẩm", "san pham", "item", "product"
    ],
    "quantity": [
        "quantity", "số lượng", "so luong", "qty", "soluong", "sl", "số lượng mua", "so luong mua"
    ],
    "unit_price": [
        "unit_price", "đơn giá", "don gia", "giá bán", "price", "giá", "gia", 
        "gia_ban", "unit price", "đơn giá bán", "don gia ban"
    ],
    "gross_amount": [
        "gross_amount", "thành tiền", "thanh tien", "thành_tiền", "thanh_tien", 
        "doanh thu", "doanh_thu", "doanh số", "doanh_so", "tổng tiền", "tong tien", 
        "tổng_tiền", "tong_tien", "tổng cộng", "tong cong", "tổng_cộng", "tong_cong", 
        "tiền hàng", "tien hang", "thanh toán", "thanh toan", "thanh_toán", 
        "giá trị", "gia tri", "giá trị đơn", "gia tri don", "thực thu", "thuc thu", 
        "revenue", "gross revenue", "total amount", "total", "amount", "sales"
    ],
    "status": [
        "status", "trạng thái", "trang thai", "tình trạng", "tinh trang", "kết quả", "ket qua"
    ],
    "return_date": [
        "return_date", "ngày trả", "ngay tra", "ngay_doi_tra", "ngày đổi trả", "ngày hoàn", "ngay hoan"
    ],
    "return_amount": [
        "return_amount", "tiền hoàn trả", "tien tra", "giá trị hoàn", "refund_amount", 
        "tiền hoàn", "hoàn tiền", "hoan tien", "hàng trả", "hang tra", "tiền trả lại", "tien tra lai"
    ],

    # Promotions table
    "promo_code": [
        "promo_code", "mã ưu đãi", "ma uu dai", "mã giảm giá", "voucher", "coupon", 
        "mã voucher", "ma voucher", "khuyến mãi", "khuyen mai"
    ],
    "campaign_id": [
        "campaign_id", "mã chương trình", "ma chuong trinh", "chiến dịch", "chien dich", 
        "campaign", "chương trình", "chuong trinh", "ct", "ctkm"
    ],
    "discount_amount": [
        "discount_amount", "tiền giảm", "mức giảm", "chiet khau", "chiết khấu", 
        "discount", "tiền voucher", "tien giam", "giảm giá", "giam gia", "giảm", "giam"
    ],

    # Products & COGS table
    "product_name": [
        "product_name", "tên sản phẩm", "ten san pham", "tên hàng", "tên sp", "ten sp", 
        "san pham", "sản phẩm", "tên mặt hàng", "ten mat hang"
    ],
    "category": [
        "category", "ngành hàng", "nganh hang", "danh mục", "danh muc", "nhóm hàng", "nhom hang"
    ],
    "list_price": ["list_price", "giá niêm yết", "gia niem yet", "giá bán gốc", "giá gốc"],
    "cogs": [
        "cogs", "giá vốn", "gia von", "tiền vốn", "tien von", "chi phí vốn", 
        "cost_of_goods", "vốn", "von", "giá nhập", "gia nhap", "chi phí giá vốn", "cost"
    ],

    # Campaign Costs table
    "cost_id": ["cost_id", "mã chi phí", "ma chi phi", "id_chi_phi"],
    "cost_type": ["cost_type", "loại chi phí", "loai chi phi", "phân loại chi phí"],
    "description": ["description", "mô tả", "mo ta", "nội dung chi"],
    "amount": ["amount", "số tiền", "so tien", "chi phí", "cost_amount", "tiền chi"],
    "allocation_rule": ["allocation_rule", "tiêu thức phân bổ", "tieu thuc", "quy tắc phân bổ"]
}

def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize DataFrame columns based on aliases dictionary, guaranteeing 100% unique column names."""
    if df is None or df.empty:
        return df
    
    # 1. Clean raw column names
    raw_cols = [str(c).strip() for c in df.columns]
    assigned_std = set()
    col_rename = {}
    
    # Pass 1: Exact matches to standard names (e.g. col_lower == "order_id")
    for col in raw_cols:
        col_lower = col.lower()
        if col_lower in COLUMN_MAPPINGS and col_lower not in assigned_std:
            col_rename[col] = col_lower
            assigned_std.add(col_lower)
            
    # Pass 2: Specific aliases matching (longest phrase first to avoid STT overriding Mã đơn hàng)
    for std_col, aliases in COLUMN_MAPPINGS.items():
        if std_col in assigned_std:
            continue
        sorted_aliases = sorted(aliases, key=len, reverse=True)
        matched_col = None
        for alias in sorted_aliases:
            for col in raw_cols:
                if col in col_rename:
                    continue
                if col.lower() == alias:
                    matched_col = col
                    break
            if matched_col:
                break
        if matched_col:
            col_rename[matched_col] = std_col
            assigned_std.add(std_col)

    # Pass 3: Fallback substring matching for standard fields that are still missing
    for std_col, aliases in COLUMN_MAPPINGS.items():
        if std_col in assigned_std:
            continue
        for col in raw_cols:
            if col in col_rename:
                continue
            col_lower = col.lower()
            if any(alias in col_lower for alias in aliases if len(alias) >= 4):
                col_rename[col] = std_col
                assigned_std.add(std_col)
                break
            
    # Pass 4: Clean remaining columns
    for col in raw_cols:
        if col not in col_rename:
            clean_name = re.sub(r"[^\w\s]", "", col.lower()).strip().replace(" ", "_")
            col_rename[col] = clean_name if clean_name else "col"
            
    df_renamed = df.rename(columns=col_rename).copy()
    
    # Pass 5: Force unique column names so Series ambiguity never happens
    final_cols = []
    seen = {}
    for c in df_renamed.columns:
        c_str = str(c)
        if c_str in seen:
            seen[c_str] += 1
            final_cols.append(f"{c_str}_{seen[c_str]}")
        else:
            seen[c_str] = 0
            final_cols.append(c_str)
    df_renamed.columns = final_cols
    return df_renamed

class DataLoader:
    @staticmethod
    def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
        """Normalize DataFrame columns based on aliases dictionary."""
        return standardize_columns(df)

    @staticmethod
    def load_from_csv(file_path_or_buffer) -> dict:
        """Load single CSV file into transactions dataframe with robust encoding and separator detection."""
        try:
            df = pd.read_csv(file_path_or_buffer, encoding="utf-8-sig", sep=None, engine="python")
        except Exception:
            if hasattr(file_path_or_buffer, "seek"):
                file_path_or_buffer.seek(0)
            try:
                df = pd.read_csv(file_path_or_buffer, encoding="cp1258", sep=None, engine="python")
            except Exception:
                if hasattr(file_path_or_buffer, "seek"):
                    file_path_or_buffer.seek(0)
                df = pd.read_csv(file_path_or_buffer, encoding="latin1")
        df_std = standardize_columns(df)
        return {"transactions": df_std}

    @staticmethod
    def load_from_excel(file_path_or_buffer) -> dict:
        """
        Load datasets from an Excel file containing multiple sheets.
        Returns dictionary with keys: 'transactions', 'promotions', 'products', 'costs'
        """
        xl = pd.ExcelFile(file_path_or_buffer)
        sheet_names = xl.sheet_names
        
        # Match sheets by keywords
        sheets_map = {
            "transactions": None,
            "promotions": None,
            "products": None,
            "costs": None
        }
        
        for s in sheet_names:
            s_lower = s.lower()
            if any(k in s_lower for k in ["trans", "giao dịch", "don hang", "đơn"]):
                sheets_map["transactions"] = s
            elif any(k in s_lower for k in ["promo", "ưu đãi", "khuyen mai", "voucher"]):
                sheets_map["promotions"] = s
            elif any(k in s_lower for k in ["prod", "giá vốn", "cogs", "sản phẩm"]):
                sheets_map["products"] = s
            elif any(k in s_lower for k in ["cost", "chi phí", "ngân sách"]):
                sheets_map["costs"] = s
                
        # Default fallback by index if sheet names are generic
        if sheets_map["transactions"] is None and len(sheet_names) > 0:
            sheets_map["transactions"] = sheet_names[0]
        if sheets_map["promotions"] is None and len(sheet_names) > 1:
            sheets_map["promotions"] = sheet_names[1]
        if sheets_map["products"] is None and len(sheet_names) > 2:
            sheets_map["products"] = sheet_names[2]
        if sheets_map["costs"] is None and len(sheet_names) > 3:
            sheets_map["costs"] = sheet_names[3]

        result = {}
        for key, s_name in sheets_map.items():
            if s_name:
                df = xl.parse(s_name)
                result[key] = standardize_columns(df)
            else:
                result[key] = pd.DataFrame()
        return result

    @staticmethod
    def load_from_csv_files(tx_path, promo_path, prod_path, cost_path) -> dict:
        """Load datasets from 4 separate CSV files."""
        result = {}
        try:
            result["transactions"] = standardize_columns(pd.read_csv(tx_path))
        except Exception:
            result["transactions"] = pd.DataFrame()
            
        try:
            result["promotions"] = standardize_columns(pd.read_csv(promo_path))
        except Exception:
            result["promotions"] = pd.DataFrame()
            
        try:
            result["products"] = standardize_columns(pd.read_csv(prod_path))
        except Exception:
            result["products"] = pd.DataFrame()
            
        try:
            result["costs"] = standardize_columns(pd.read_csv(cost_path))
        except Exception:
            result["costs"] = pd.DataFrame()
            
        return result

    @staticmethod
    def parse_google_sheet_url(url: str) -> str:
        """Extract Google Sheet ID and format the export URL for direct xlsx download."""
        # Examples:
        # https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit?usp=sharing
        match = re.search(r"/spreadsheets/d/([a-zA-Z0-9-_]+)", url)
        if match:
            sheet_id = match.group(1)
            # Direct export link as XLSX
            export_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx"
            return export_url
        raise ValueError("URL Google Sheet không hợp lệ. Vui lòng cung cấp link dạng https://docs.google.com/spreadsheets/d/.../edit")

    @staticmethod
    def load_from_google_sheet(url: str, cache_file: str = "data/gsheet_download.xlsx") -> dict:
        """Download public Google Sheet as XLSX and load into dataframes."""
        export_url = DataLoader.parse_google_sheet_url(url)
        # Attempt download
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            req = urllib.request.Request(export_url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as response, open(cache_file, "wb") as out_file:
                out_file.write(response.read())
            return DataLoader.load_from_excel(cache_file)
        except Exception as e:
            # If network error or blocked, try fallback or raise clear informative message
            raise RuntimeError(f"Không thể tải Google Sheet trực tiếp (Lỗi: {e}). Đảm bảo Sheet đã bật quyền 'Bất kỳ ai có liên kết đều có thể xem' (Anyone with link can view).")

    @staticmethod
    def load_scenario(scenario_name: str = "normal") -> dict:
        """Convenience function to load one of the built-in test scenarios (normal, missing, boundary)."""
        if scenario_name in ["standard", "default", "normal"]:
            scenario_name = "normal"
        file_path = f"data/giahoa_dataset_{scenario_name}.xlsx"
        if not os.path.exists(file_path):
            from data.generate_sample_data import generate_all_datasets
            generate_all_datasets()
        return DataLoader.load_from_excel(file_path)

