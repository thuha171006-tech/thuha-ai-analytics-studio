"""
Sample Data Generator for Công ty Gia Hòa (Đề án 08 - AI301)
Generates 4 tables across 3 test scenarios:
1. Normal Case (Dữ liệu hợp lệ chuẩn)
2. Missing Data Case (Thiếu dữ liệu: thiếu mã SP, thiếu tag chi phí, v.v.)
3. Boundary / Edge Case (Ranh giới quy tắc: trùng nhiều voucher, hoàn hàng trễ, chi phí chung)
"""

import os
import pandas as pd
import numpy as np

def generate_all_datasets(output_dir="data"):
    os.makedirs(output_dir, exist_ok=True)
    
    # 4 Chương trình bán hàng trong tháng:
    # CT1: FLASH_SALE - Flash Sale Mùa Hè (Giảm giá sốc đồ làm mát/gia dụng)
    # CT2: LOYAL_VIP  - Tri Ân Khách Quen (Voucher tích điểm/giảm giá cho khách cũ)
    # CT3: KITCHEN_COMBO - Combo Nhà Bếp Tiện Lợi (Mua kèm nồi chiên + chảo)
    # CT4: SMART_HOME - Đồ Gia Dụng Thông Minh Online (Kênh trực tuyến)

    # =========================================================================
    # 1. DANH MỤC SẢN PHẨM & GIÁ VỐN (Products & COGS)
    # =========================================================================
    products_data = [
        {"product_id": "SP01", "product_name": "Quạt điều hòa hơi nước", "category": "Thiết bị làm mát", "list_price": 1850000, "cogs": 1150000},
        {"product_id": "SP02", "product_name": "Nồi chiên không dầu 6L", "category": "Đồ dùng nhà bếp", "list_price": 1450000, "cogs": 850000},
        {"product_id": "SP03", "product_name": "Bộ chảo chống dính 3 đáy", "category": "Đồ dùng nhà bếp", "list_price": 450000, "cogs": 230000},
        {"product_id": "SP04", "product_name": "Robot hút bụi thông minh", "category": "Gia dụng thông minh", "list_price": 4200000, "cogs": 2700000},
        {"product_id": "SP05", "product_name": "Máy lọc không khí gia đình", "category": "Gia dụng thông minh", "list_price": 2800000, "cogs": 1750000},
        {"product_id": "SP06", "product_name": "Bộ hộp thủy tinh bảo quản", "category": "Đồ dùng gia đình", "list_price": 250000, "cogs": 110000},
        {"product_id": "SP07", "product_name": "Ấm siêu tốc giữ nhiệt 1.8L", "category": "Đồ dùng gia đình", "list_price": 320000, "cogs": 160000},
        {"product_id": "SP08", "product_name": "Máy xay sinh tố đa năng", "category": "Đồ dùng nhà bếp", "list_price": 650000, "cogs": 380000},
    ]
    df_products = pd.DataFrame(products_data)
    
    # =========================================================================
    # KỊCH BẢN 1: NORMAL CASE (Dữ liệu chuẩn, đối chiếu khớp quy tắc)
    # =========================================================================
    normal_tx = [
        # CT1: Flash Sale (Offline + Online)
        {"order_id": "ORD_001", "date": "2026-10-02", "channel": "Online", "product_id": "SP01", "quantity": 1, "unit_price": 1850000, "status": "COMPLETED", "return_date": None, "return_amount": 0},
        {"order_id": "ORD_002", "date": "2026-10-02", "channel": "Offline", "product_id": "SP02", "quantity": 1, "unit_price": 1450000, "status": "COMPLETED", "return_date": None, "return_amount": 0},
        {"order_id": "ORD_003", "date": "2026-10-03", "channel": "Online", "product_id": "SP07", "quantity": 2, "unit_price": 320000, "status": "COMPLETED", "return_date": None, "return_amount": 0},
        {"order_id": "ORD_004", "date": "2026-10-04", "channel": "Online", "product_id": "SP01", "quantity": 1, "unit_price": 1850000, "status": "RETURNED", "return_date": "2026-10-06", "return_amount": 1850000},
        {"order_id": "ORD_005", "date": "2026-10-05", "channel": "Offline", "product_id": "SP03", "quantity": 2, "unit_price": 450000, "status": "COMPLETED", "return_date": None, "return_amount": 0},
        
        # CT2: Tri Ân Khách Quen (Offline)
        {"order_id": "ORD_006", "date": "2026-10-07", "channel": "Offline", "product_id": "SP04", "quantity": 1, "unit_price": 4200000, "status": "COMPLETED", "return_date": None, "return_amount": 0},
        {"order_id": "ORD_007", "date": "2026-10-08", "channel": "Offline", "product_id": "SP05", "quantity": 1, "unit_price": 2800000, "status": "COMPLETED", "return_date": None, "return_amount": 0},
        {"order_id": "ORD_008", "date": "2026-10-09", "channel": "Offline", "product_id": "SP06", "quantity": 4, "unit_price": 250000, "status": "COMPLETED", "return_date": None, "return_amount": 0},
        {"order_id": "ORD_009", "date": "2026-10-10", "channel": "Offline", "product_id": "SP02", "quantity": 1, "unit_price": 1450000, "status": "COMPLETED", "return_date": None, "return_amount": 0},

        # CT3: Combo Nhà Bếp (Mua SP02 + SP03)
        {"order_id": "ORD_010", "date": "2026-10-12", "channel": "Online", "product_id": "SP02", "quantity": 1, "unit_price": 1450000, "status": "COMPLETED", "return_date": None, "return_amount": 0},
        {"order_id": "ORD_011", "date": "2026-10-13", "channel": "Online", "product_id": "SP03", "quantity": 1, "unit_price": 450000, "status": "COMPLETED", "return_date": None, "return_amount": 0},
        {"order_id": "ORD_012", "date": "2026-10-14", "channel": "Offline", "product_id": "SP08", "quantity": 2, "unit_price": 650000, "status": "COMPLETED", "return_date": None, "return_amount": 0},
        {"order_id": "ORD_013", "date": "2026-10-15", "channel": "Online", "product_id": "SP02", "quantity": 1, "unit_price": 1450000, "status": "RETURNED", "return_date": "2026-10-18", "return_amount": 1450000},

        # CT4: Gia Dụng Thông Minh Online (SP04, SP05 trên kênh Online)
        {"order_id": "ORD_014", "date": "2026-10-18", "channel": "Online", "product_id": "SP04", "quantity": 1, "unit_price": 4200000, "status": "COMPLETED", "return_date": None, "return_amount": 0},
        {"order_id": "ORD_015", "date": "2026-10-19", "channel": "Online", "product_id": "SP05", "quantity": 1, "unit_price": 2800000, "status": "COMPLETED", "return_date": None, "return_amount": 0},
        {"order_id": "ORD_016", "date": "2026-10-20", "channel": "Online", "product_id": "SP04", "quantity": 1, "unit_price": 4200000, "status": "COMPLETED", "return_date": None, "return_amount": 0},
        {"order_id": "ORD_017", "date": "2026-10-22", "channel": "Online", "product_id": "SP05", "quantity": 1, "unit_price": 2800000, "status": "RETURNED", "return_date": "2026-10-25", "return_amount": 2800000},
        
        # Đơn hữu cơ (Không qua chương trình nào)
        {"order_id": "ORD_018", "date": "2026-10-25", "channel": "Offline", "product_id": "SP07", "quantity": 1, "unit_price": 320000, "status": "COMPLETED", "return_date": None, "return_amount": 0},
    ]
    df_normal_tx = pd.DataFrame(normal_tx)

    normal_promo = [
        {"order_id": "ORD_001", "promo_code": "FLASH15", "campaign_id": "CT1_FLASH", "discount_amount": 277500},
        {"order_id": "ORD_002", "promo_code": "FLASH15", "campaign_id": "CT1_FLASH", "discount_amount": 217500},
        {"order_id": "ORD_003", "promo_code": "FLASH15", "campaign_id": "CT1_FLASH", "discount_amount": 96000},
        {"order_id": "ORD_004", "promo_code": "FLASH15", "campaign_id": "CT1_FLASH", "discount_amount": 277500},
        {"order_id": "ORD_005", "promo_code": "FLASH15", "campaign_id": "CT1_FLASH", "discount_amount": 135000},
        
        {"order_id": "ORD_006", "promo_code": "VIP10", "campaign_id": "CT2_LOYAL", "discount_amount": 420000},
        {"order_id": "ORD_007", "promo_code": "VIP10", "campaign_id": "CT2_LOYAL", "discount_amount": 280000},
        {"order_id": "ORD_008", "promo_code": "VIP10", "campaign_id": "CT2_LOYAL", "discount_amount": 100000},
        {"order_id": "ORD_009", "promo_code": "VIP10", "campaign_id": "CT2_LOYAL", "discount_amount": 145000},

        {"order_id": "ORD_010", "promo_code": "COMBO20", "campaign_id": "CT3_COMBO", "discount_amount": 290000},
        {"order_id": "ORD_011", "promo_code": "COMBO20", "campaign_id": "CT3_COMBO", "discount_amount": 90000},
        {"order_id": "ORD_012", "promo_code": "COMBO20", "campaign_id": "CT3_COMBO", "discount_amount": 260000},
        {"order_id": "ORD_013", "promo_code": "COMBO20", "campaign_id": "CT3_COMBO", "discount_amount": 290000},

        {"order_id": "ORD_014", "promo_code": "SMART12", "campaign_id": "CT4_SMART", "discount_amount": 504000},
        {"order_id": "ORD_015", "promo_code": "SMART12", "campaign_id": "CT4_SMART", "discount_amount": 336000},
        {"order_id": "ORD_016", "promo_code": "SMART12", "campaign_id": "CT4_SMART", "discount_amount": 504000},
        {"order_id": "ORD_017", "promo_code": "SMART12", "campaign_id": "CT4_SMART", "discount_amount": 336000},
    ]
    df_normal_promo = pd.DataFrame(normal_promo)

    normal_costs = [
        {"cost_id": "CST_01", "campaign_id": "CT1_FLASH", "cost_type": "DIRECT", "description": "Facebook Ads & Banner Flash Sale", "amount": 1200000, "allocation_rule": "Direct to CT1"},
        {"cost_id": "CST_02", "campaign_id": "CT2_LOYAL", "cost_type": "DIRECT", "description": "SMS Brandname & Thiệp quà tặng khách VIP", "amount": 600000, "allocation_rule": "Direct to CT2"},
        {"cost_id": "CST_03", "campaign_id": "CT3_COMBO", "cost_type": "DIRECT", "description": "Tờ rơi & POSM tại quầy Combo Bếp", "amount": 800000, "allocation_rule": "Direct to CT3"},
        {"cost_id": "CST_04", "campaign_id": "CT4_SMART", "cost_type": "DIRECT", "description": "KOL Tiktok Review Robot & Máy lọc", "amount": 2500000, "allocation_rule": "Direct to CT4"},
        {"cost_id": "CST_05", "campaign_id": "ALL", "cost_type": "OVERHEAD", "description": "Chi phí nền tảng vận hành e-commerce & kho bãi", "amount": 2000000, "allocation_rule": "Revenue-share"},
    ]
    df_normal_costs = pd.DataFrame(normal_costs)

    # =========================================================================
    # KỊCH BẢN 2: MISSING DATA CASE (Thiếu dữ liệu)
    # =========================================================================
    missing_tx = normal_tx.copy()
    # Giả lập: ORD_002 thiếu product_id, ORD_007 có unit_price = None, ORD_012 trạng thái trống
    missing_tx[1] = {"order_id": "ORD_002", "date": "2026-10-02", "channel": "Offline", "product_id": None, "quantity": 1, "unit_price": 1450000, "status": "COMPLETED", "return_date": None, "return_amount": 0}
    missing_tx[6] = {"order_id": "ORD_007", "date": "2026-10-08", "channel": "Offline", "product_id": "SP05", "quantity": 1, "unit_price": np.nan, "status": "COMPLETED", "return_date": None, "return_amount": 0}
    df_missing_tx = pd.DataFrame(missing_tx)

    missing_costs = normal_costs.copy()
    # Chi phí CST_06 không có campaign_id và không có allocation_rule
    missing_costs.append({"cost_id": "CST_06", "campaign_id": None, "cost_type": "DIRECT", "description": "Chi phí in ấn tờ rơi chưa rõ chiến dịch", "amount": 500000, "allocation_rule": None})
    df_missing_costs = pd.DataFrame(missing_costs)

    # =========================================================================
    # KỊCH BẢN 3: BOUNDARY & EDGE CASE (Ranh giới quy tắc, trùng lặp, trả hàng trễ)
    # =========================================================================
    boundary_tx = [
        # Trả hàng trễ: Chương trình kết thúc 31/10, đơn hàng trả vào ngày 15/11 (ngoài kỳ kế toán thường)
        {"order_id": "ORD_B01", "date": "2026-10-28", "channel": "Online", "product_id": "SP04", "quantity": 1, "unit_price": 4200000, "status": "RETURNED", "return_date": "2026-11-15", "return_amount": 4200000},
        
        # Đơn hàng tiếp xúc 2 chương trình cùng lúc (Double Coupon Stacking)
        {"order_id": "ORD_B02", "date": "2026-10-15", "channel": "Online", "product_id": "SP01", "quantity": 1, "unit_price": 1850000, "status": "COMPLETED", "return_date": None, "return_amount": 0},
        
        # Đơn hàng trả một phần (Partial Return)
        {"order_id": "ORD_B03", "date": "2026-10-16", "channel": "Offline", "product_id": "SP06", "quantity": 10, "unit_price": 250000, "status": "PARTIAL_RETURN", "return_date": "2026-10-20", "return_amount": 1000000},
        
        # Đơn hàng ranh giới doanh số 0 đồng (Tặng kèm / Voucher 100%)
        {"order_id": "ORD_B04", "date": "2026-10-20", "channel": "Online", "product_id": "SP07", "quantity": 1, "unit_price": 320000, "status": "COMPLETED", "return_date": None, "return_amount": 0},

        # Thêm các đơn chuẩn để có kết quả tổng thể
        {"order_id": "ORD_B05", "date": "2026-10-05", "channel": "Offline", "product_id": "SP02", "quantity": 2, "unit_price": 1450000, "status": "COMPLETED", "return_date": None, "return_amount": 0},
        {"order_id": "ORD_B06", "date": "2026-10-10", "channel": "Online", "product_id": "SP05", "quantity": 2, "unit_price": 2800000, "status": "COMPLETED", "return_date": None, "return_amount": 0},
    ]
    df_boundary_tx = pd.DataFrame(boundary_tx)

    boundary_promo = [
        # ORD_B01 thuộc CT4
        {"order_id": "ORD_B01", "promo_code": "SMART12", "campaign_id": "CT4_SMART", "discount_amount": 504000},
        # ORD_B02 áp dụng CẢ 2 VOUCHER: FLASH15 (CT1) và VIP10 (CT2) -> Xung đột tiếp xúc đa kênh!
        {"order_id": "ORD_B02", "promo_code": "FLASH15", "campaign_id": "CT1_FLASH", "discount_amount": 277500},
        {"order_id": "ORD_B02", "promo_code": "VIP10", "campaign_id": "CT2_LOYAL", "discount_amount": 185000},
        # ORD_B03 thuộc CT2
        {"order_id": "ORD_B03", "promo_code": "VIP10", "campaign_id": "CT2_LOYAL", "discount_amount": 250000},
        # ORD_B04 miễn phí 100% bằng voucher tri ân đặc biệt
        {"order_id": "ORD_B04", "promo_code": "FREE100", "campaign_id": "CT2_LOYAL", "discount_amount": 320000},
        {"order_id": "ORD_B05", "promo_code": "FLASH15", "campaign_id": "CT1_FLASH", "discount_amount": 435000},
        {"order_id": "ORD_B06", "promo_code": "SMART12", "campaign_id": "CT4_SMART", "discount_amount": 672000},
    ]
    df_boundary_promo = pd.DataFrame(boundary_promo)

    boundary_costs = [
        {"cost_id": "CST_B1", "campaign_id": "CT1_FLASH", "cost_type": "DIRECT", "description": "Flash sale Ads", "amount": 1500000, "allocation_rule": "Direct to CT1"},
        {"cost_id": "CST_B2", "campaign_id": "CT2_LOYAL", "cost_type": "DIRECT", "description": "Quà tặng VIP", "amount": 800000, "allocation_rule": "Direct to CT2"},
        {"cost_id": "CST_B3", "campaign_id": "CT3_COMBO", "cost_type": "DIRECT", "description": "Thiết kế POSM", "amount": 500000, "allocation_rule": "Direct to CT3"},
        {"cost_id": "CST_B4", "campaign_id": "CT4_SMART", "cost_type": "DIRECT", "description": "Livestream KOL", "amount": 3500000, "allocation_rule": "Direct to CT4"},
        # Chi phí chung mập mờ, tỷ lệ không đồng đều
        {"cost_id": "CST_B5", "campaign_id": "ALL", "cost_type": "OVERHEAD", "description": "Phí thuê server và quản trị chung", "amount": 3000000, "allocation_rule": "Pending Approval"},
    ]
    df_boundary_costs = pd.DataFrame(boundary_costs)

    # Save to Excel files (multi-sheet) and CSV files for ease of testing
    scenarios = {
        "normal": (df_normal_tx, df_normal_promo, df_products, df_normal_costs),
        "missing": (df_missing_tx, df_normal_promo, df_products, df_missing_costs),
        "boundary": (df_boundary_tx, df_boundary_promo, df_products, df_boundary_costs)
    }

    for name, (tx, promo, prod, cost) in scenarios.items():
        # Excel multi-sheet
        xlsx_path = os.path.join(output_dir, f"giahoa_dataset_{name}.xlsx")
        with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
            tx.to_excel(writer, sheet_name="Transactions", index=False)
            promo.to_excel(writer, sheet_name="Promotions", index=False)
            prod.to_excel(writer, sheet_name="Products_COGS", index=False)
            cost.to_excel(writer, sheet_name="Campaign_Costs", index=False)
        print(f"Generated: {xlsx_path}")

        # CSV separate files
        prefix_dir = os.path.join(output_dir, name)
        os.makedirs(prefix_dir, exist_ok=True)
        tx.to_csv(os.path.join(prefix_dir, "transactions_returns.csv"), index=False, encoding="utf-8-sig")
        promo.to_csv(os.path.join(prefix_dir, "promotion_usage.csv"), index=False, encoding="utf-8-sig")
        prod.to_csv(os.path.join(prefix_dir, "products_cogs.csv"), index=False, encoding="utf-8-sig")
        cost.to_csv(os.path.join(prefix_dir, "campaign_costs.csv"), index=False, encoding="utf-8-sig")
        print(f"Generated CSVs in: {prefix_dir}")

if __name__ == "__main__":
    generate_all_datasets()

