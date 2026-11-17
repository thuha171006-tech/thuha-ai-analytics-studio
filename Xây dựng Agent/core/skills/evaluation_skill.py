"""
Skill 2: Business Decision & Causal Evaluation Skill (Thu Hà Studio)
Handles:
1. Strategy Categorization: Continue Testing, Adjust, or Discontinue
2. Action Items & Data Requirements per Campaign
3. Critical Distinction: Rule-based Accounting Attribution vs. Causal Uplift (Counterfactual analysis)
4. Comprehensive Executive Summary Report
"""

import pandas as pd
from typing import Dict, Any, List
from core.audit_logger import AuditLogger

class EvaluationSkill:
    def __init__(self, audit_logger: AuditLogger):
        self.logger = audit_logger

    def evaluate_campaigns(
        self, 
        df_pnl: pd.DataFrame, 
        target_cm_pct: float = 15.0, 
        max_return_rate_pct: float = 12.0
    ) -> Dict[str, Any]:
        """
        Step 4 in Workflow: Đánh giá đạt tiêu chí & Phân loại quyết định chiến lược
        - Categorizes each campaign: TIẾP TỤC THỬ NGHIỆM / ĐIỀU CHỈNH / DỪNG
        - Identifies actionable tasks and missing data requirements
        """
        self.logger.log_tool_call(
            tool_name="evaluate_campaign_strategy",
            inputs={"target_cm_pct": target_cm_pct, "max_return_rate_pct": max_return_rate_pct},
            output_summary="Đánh giá tiêu chí biên đóng góp, tỷ lệ hoàn trả và ROI"
        )

        recommendations = []
        
        for idx, row in df_pnl.iterrows():
            cid = row["campaign_id"]
            if cid == "ORGANIC":
                continue
                
            cname = row["campaign_name"]
            net_rev = row["net_revenue"]
            cm = row["contribution_margin"]
            cm_pct = row["contribution_margin_pct"]
            ret_rate = row["return_rate_pct"]
            roi = row["roi_pct"]
            total_cost = row["total_cost"]
            discount = row["discount_cost"]
            direct_cost = row["direct_cost"]

            # Decision Logic
            if cm < 0 or ret_rate >= 25.0:
                decision = "DỪNG (DISCONTINUE)"
                decision_badge = "danger"
                primary_reason = f"Lợi nhuận đóng góp âm ({cm:,.0f} đ) hoặc tỷ lệ hoàn hàng vượt ngưỡng báo động ({ret_rate:.1f}%)."
                action_items = [
                    "Dừng ngay việc cấp ngân sách và đóng mã khuyến mãi trên tất cả các kênh.",
                    "Thu hồi tồn kho và điều tra nguyên nhân tỷ lệ trả hàng cao (do lỗi mô tả sản phẩm, chất lượng kỹ thuật hay giao vận chậm).",
                    "Rà soát lại toàn bộ hợp đồng KOL/quảng cáo để cắt giảm chi phí phát sinh."
                ]
                data_needed = [
                    "Báo cáo chi tiết lý do đổi trả hàng (Return Reason Codes) phân theo SKU.",
                    "Dữ liệu phản hồi & đánh giá của khách hàng (CSAT/Reviews) sau khi nhận sản phẩm.",
                    "Chi phí hoàn tất đơn hàng thực tế (reverse logistics & kho bãi) phát sinh ngoài dự kiến."
                ]

            elif cm >= 0 and (cm_pct < target_cm_pct or ret_rate > max_return_rate_pct or direct_cost > net_rev * 0.25):
                decision = "ĐIỀU CHỈNH (ADJUST)"
                decision_badge = "warning"
                primary_reason = f"Chương trình có đóng góp dương ({cm:,.0f} đ) nhưng biên lợi nhuận mỏng ({cm_pct:.1f}% < {target_cm_pct}%) hoặc tỷ lệ hoàn trả ({ret_rate:.1f}%) ăn mòn lợi nhuận."
                action_items = [
                    f"Giảm mức chiết khấu voucher (hiện tại tổng giảm giá {discount:,.0f} đ) hoặc áp dụng giá trị đơn hàng tối thiểu (AOV threshold).",
                    "Đàm phán lại chi phí quảng cáo/KOL để tối ưu chi phí thu hút khách hàng (CAC).",
                    "Chỉ áp dụng ưu đãi cho các dòng sản phẩm có biên lợi nhuận gộp cao (>40%), hạn chế áp dụng cho các SKU biên mỏng."
                ]
                data_needed = [
                    "Độ co giãn của cầu theo giá (Price Elasticity) để thử nghiệm mức voucher thấp hơn.",
                    "Báo cáo phân tích hành vi khách hàng xem họ có mua kèm thêm sản phẩm giá trị cao không.",
                    "Số liệu đối soát chi phí quảng cáo chi tiết theo từng ngày (Ad spend daily breakdown)."
                ]

            else:
                decision = "TIẾP TỤC THỬ NGHIỆM (CONTINUE TESTING)"
                decision_badge = "success"
                primary_reason = f"Chương trình đạt hiệu quả tài chính vững chắc: Biên đóng góp {cm_pct:.1f}% (đạt {cm:,.0f} đ), ROI {roi:.1f}%, tỷ lệ trả hàng thấp ({ret_rate:.1f}%)."
                action_items = [
                    "Tăng ngân sách thử nghiệm thêm 15% - 20% trong tháng kế tiếp để kiểm tra khả năng mở rộng quy mô (Scalability).",
                    "Mở rộng tập khách hàng mục tiêu tương tự (Lookalike audience) trên kênh số.",
                    "Tiếp tục theo dõi tỷ lệ khách hàng quay lại mua lần 2 (Repeat purchase rate)."
                ]
                data_needed = [
                    "Tỷ lệ chuyển đổi chi tiết theo từng kênh bán (Conversion rate by placement).",
                    "Số liệu theo dõi tỷ lệ giữ chân khách hàng (Cohort Retention Rate) sau 30-60 ngày.",
                    "Dữ liệu năng lực đáp ứng của kho bãi nếu tăng quy mô đơn hàng lên gấp đôi."
                ]

            rec = {
                "campaign_id": cid,
                "campaign_name": cname,
                "decision": decision,
                "decision_badge": decision_badge,
                "primary_reason": primary_reason,
                "financial_snapshot": {
                    "net_revenue": net_rev,
                    "contribution_margin": cm,
                    "contribution_margin_pct": cm_pct,
                    "return_rate_pct": ret_rate,
                    "roi_pct": roi,
                    "total_cost": total_cost
                },
                "action_items": action_items,
                "data_needed": data_needed
            }
            recommendations.append(rec)
            self.logger.log_rule("RULE_DECISION_01", f"Phân loại quyết định {cid}", f"Kết luận: {decision}", 1, primary_reason)

        # Methodology distinction: Accounting attribution vs Causal Uplift
        causal_analysis = {
            "title": "Phân biệt Bản chất: Ghi nhận Kế toán (Rule-based Attribution) vs Bằng chứng Tác động Gia tăng Thực tế (Causal Uplift)",
            "warning": "CẢNH BÁO PHƯƠNG PHÁP LUẬN: Tuyệt đối không đánh đồng 'Doanh thu ghi nhận theo mã khuyến mãi' với 'Chương trình làm doanh thu công ty tăng trưởng'!",
            "explanation": (
                "Các con số trong bảng P&L ở trên được tính toán dựa trên Quy tắc Kế toán Gán đơn (Rule-based Accounting Attribution), "
                "nghĩa là mọi đơn hàng có gắn mã voucher được ghi nhận doanh số cho chương trình đó. "
                "Tuy nhiên, điều này CHƯA PHẢI LÀ BẰNG CHỨNG NHÂN QUẢ (Causal Impact). "
                "Một lượng lớn khách hàng (đặc biệt là khách quen trong chương trình Tri Ân Khách Quen) vốn dĩ ĐÃ CÓ Ý ĐỊNH MUA HÀNG từ trước, "
                "và họ chỉ vô tình áp thêm mã voucher giảm giá (hiện tượng Tự ăn lấn doanh thu - Cannibalization / Deadweight Loss). "
                "Nếu không có nhóm đối chứng (Control Group), doanh nghiệp có thể đang 'đốt tiền' tặng voucher cho những đơn hàng vốn dĩ vẫn phát sinh!"
            ),
            "requirements_for_causal_proof": [
                "1. Thiết kế Thử nghiệm Ngẫu nhiên có Đối chứng (A/B Testing / Randomized Controlled Trial - RCT): Chia ngẫu nhiên khách hàng thành Nhóm thử nghiệm (nhận voucher) và Nhóm đối chứng (không nhận voucher hoặc nhận thông điệp thường).",
                "2. Tính toán Doanh thu Tăng thêm Thuần (Incremental Revenue Lift): Lift = Doanh thu Nhóm thử nghiệm - Doanh thu Nhóm đối chứng.",
                "3. So sánh với Doanh số Cơ sở (Baseline Sales): Đối chiếu xu hướng bán hàng của cùng kỳ các tháng trước để loại bỏ yếu tố mùa vụ (Seasonality) hoặc xu hướng thị trường chung.",
                "4. Đánh giá Tác động Ăn lấn (Cannibalization Check): Đánh giá xem doanh số tăng ở nhóm sản phẩm khuyến mãi có làm tụt giảm doanh số của các sản phẩm nguyên giá cùng ngành hàng hay không."
            ]
        }

        return {
            "recommendations": recommendations,
            "causal_analysis": causal_analysis
        }

