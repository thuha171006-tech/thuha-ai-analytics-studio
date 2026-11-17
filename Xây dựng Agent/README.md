# AI AGENT ĐÁNH GIÁ HIỆU QUẢ CHƯƠNG TRÌNH BÁN HÀNG - CÔNG TY GIA HÒA
## Học Phần: AI301 | Đề Dự Án 08

Hệ thống AI Agent hỗ trợ Trưởng phòng Kinh doanh Công ty Gia Hòa đánh giá hiệu quả 4 chương trình bán hàng trong tháng, tự động xử lý trùng lặp doanh thu, khấu trừ hàng trả sau chiến dịch, phân bổ chi phí chuẩn xác, và đưa ra đề xuất chiến lược: **Tiếp tục thử nghiệm / Điều chỉnh / Dừng**.

---

## 1. Cấu Trúc Dự Án
```
d:\Xây dựng Agent\
├── app.py                     # Máy chủ Web & REST API phục vụ Dashboard
├── cli.py                     # Giao diện dòng lệnh CLI chuẩn mực (Chấm thi trực tiếp)
├── BAO_CAO_DU_AN_08_GIA_HOA.md # Toàn văn Báo cáo Task 1 & Task 2 chi tiết
├── core/
│   ├── data_loader.py         # Nạp file Excel (.xlsx), CSV, hoặc link Google Sheet
│   ├── audit_logger.py        # Nhật ký truy vết (Audit Trail) minh chứng Agent thực thi
│   ├── agent_engine.py        # Controller Agent điều phối ReAct & Human-in-the-Loop
│   └── skills/
│       ├── reconciliation_skill.py  # Kỹ năng 1: Đối chiếu Kế toán, Khử trùng lặp & Xử lý Hoàn hàng
│       └── evaluation_skill.py      # Kỹ năng 2: Đánh giá Hiệu quả Chiến lược & Phân tích Nhân quả
├── ui/
│   └── index.html             # Giao diện Web Dashboard tương tác (Tailwind CSS, Chart.js)
├── data/
│   ├── generate_sample_data.py # Tự động tạo bộ dữ liệu mẫu theo 3 kịch bản
│   ├── giahoa_dataset_normal.xlsx
│   ├── giahoa_dataset_missing.xlsx
│   ├── giahoa_dataset_boundary.xlsx
│   └── (thư mục csv normal/, missing/, boundary/)
├── tests/
│   └── test_agent.py          # Bộ kiểm thử tự động (Unit & Integration Tests)
└── exports/                   # Thư mục xuất báo cáo JSON / Bảng kết quả
```

---

## 2. Hướng Dẫn Khởi Chạy

### 2.1. Khởi chạy Giao diện Web Dashboard (Interactive UI)
Chạy lệnh sau trong PowerShell hoặc Terminal:
```powershell
python app.py
```
Mở trình duyệt web truy cập: **`http://127.0.0.1:8050`**

**Tính năng trên giao diện Web:**
- **Nạp dữ liệu 1-click:** Nạp ngay 3 kịch bản kiểm thử (Chuẩn, Thiếu dữ liệu, Ranh giới quy tắc).
- **Nhập link Google Sheet hoặc tải file Excel (.xlsx) / CSV:** Tự động nhận diện cấu trúc cột tiếng Việt / tiếng Anh.
- **Tiến trình trực quan:** Minh họa từng bước theo đúng Sơ đồ Workflow người dùng cung cấp.
- **Bảng P&L & Biểu đồ:** Phân tích trực quan Doanh thu gộp, Hoàn hàng, Doanh thu thuần, COGS, Chiết khấu, Chi phí trực tiếp, Chi phí phân bổ, Biên đóng góp (Contribution Margin) và ROI.
- **Trung tâm Ngoại lệ & Human Control (HITL):** Cho phép Trưởng phòng phê duyệt thủ công các đơn trùng ưu đãi và duyệt chi phí chung.
- **Báo cáo Chiến lược & Phân tích Nhân quả:** Đề xuất Tiếp tục / Điều chỉnh / Dừng kèm Action Items, Data Needed và cảnh báo cạm bẫy Cannibalization.
- **Audit Trail:** Xem toàn bộ vết thực thi, công cụ gọi và quy tắc áp dụng theo thời gian thực.

---

### 2.2. Khởi chạy bằng Giao diện Dòng lệnh (CLI)
Dành cho việc chấm thi hoặc chạy tự động không cần mở trình duyệt:

```powershell
# Chạy kịch bản chuẩn:
python cli.py --scenario normal

# Chạy kịch bản thiếu dữ liệu (Agent tự phát hiện ngoại lệ):
python cli.py --scenario missing

# Chạy kịch bản ranh giới (trùng ưu đãi đa kênh, trả hàng trễ):
python cli.py --scenario boundary

# Nạp file Excel mới của Giảng viên tại buổi chấm thi:
python cli.py --file "C:/path/to/dataset_moi.xlsx"
```

---

### 2.3. Chạy Kiểm Thử Tự Động (Unit Tests)
```powershell
python tests/test_agent.py
```
Đảm bảo 100% test cases vượt qua (`OK`).

---

## 3. Đáp Ứng Trọn Vẹn Yêu Cầu Đề Án 08 (AI301)
- **Task 1:** Phân tích 3 vấn đề cốt lõi kèm ảnh hưởng định lượng; Quy trình To-Be có RACI; 3 bước AI Agent tự động; 2 điểm kiểm soát HITL; Bản thiết kế GIPO và kiến trúc Agent.
- **Task 2:** Giải pháp chạy được 100%; phối hợp 2 kỹ năng nghiệp vụ; có nhật ký truy vết Audit Trail minh chứng gọi công cụ; xử lý triệt để trùng lặp và hoàn hàng sau chương trình; phân biệt rạch ròi giữa Ghi nhận Kế toán (Attribution) và Tác động Nhân quả (Causality); sẵn sàng nhận bộ dữ liệu mới cùng cấu trúc để chấm thi trực tiếp.

