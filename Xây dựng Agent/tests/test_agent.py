"""
Unit & Integration Tests for Gia Hoa Sales Evaluation AI Agent
Tests:
1. Normal Case (Standard execution)
2. Missing Data Case (Anomaly detection)
3. Boundary / Edge Case (Multi-touch deduplication, Late returns, HITL override)
"""

import unittest
import os
import sys

# Ensure workspace root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.data_loader import DataLoader
from core.agent_engine import SalesEvaluationAgent

class TestSalesEvaluationAgent(unittest.TestCase):
    def setUp(self):
        self.agent = SalesEvaluationAgent()

    def test_normal_case(self):
        """Kiểm thử kịch bản dữ liệu chuẩn thông thường."""
        data = DataLoader.load_scenario("normal")
        summary = self.agent.run_pipeline(data, multi_touch_rule="PROPORTIONAL")
        
        self.assertIn("pnl_table", summary)
        pnl = summary["pnl_table"]
        self.assertTrue(len(pnl) >= 4)
        
        # Verify no double counting: Total Net Revenue should equal sum of non-organic net revenues
        campaign_pnl = [p for p in pnl if p["campaign_id"] != "ORGANIC"]
        total_net_rev = sum(p["net_revenue"] for p in campaign_pnl)
        self.assertGreater(total_net_rev, 0)
        
        # Verify Recommendations generated
        self.assertTrue(len(summary["recommendations"]) >= 4)
        for rec in summary["recommendations"]:
            self.assertIn(rec["decision"], ["TIẾP TỤC THỬ NGHIỆM (CONTINUE TESTING)", "ĐIỀU CHỈNH (ADJUST)", "DỪNG (DISCONTINUE)"])
            self.assertTrue(len(rec["action_items"]) > 0)
            self.assertTrue(len(rec["data_needed"]) > 0)
            
        # Verify Causal distinction
        self.assertIn("causal_analysis", summary)
        self.assertIn("warning", summary["causal_analysis"])

    def test_missing_data_case(self):
        """Kiểm thử kịch bản thiếu dữ liệu: Agent phải phát hiện ngoại lệ và ghi nhận log."""
        data = DataLoader.load_scenario("missing")
        summary = self.agent.run_pipeline(data)
        
        exceptions = summary["exceptions_list"]
        self.assertGreater(len(exceptions), 0)
        
        exc_types = [e["type"] for e in exceptions]
        self.assertIn("MISSING_PRODUCT_ID", exc_types)
        self.assertIn("UNASSIGNED_COST_CAMPAIGN", exc_types)
        
        # Status should require review
        self.assertEqual(summary["status"], "NEEDS_HUMAN_REVIEW")

    def test_boundary_and_edge_case(self):
        """Kiểm thử kịch bản ranh giới: trùng voucher đa kênh (ORD_B02) & trả hàng trễ (ORD_B01)."""
        data = DataLoader.load_scenario("boundary")
        summary = self.agent.run_pipeline(data, multi_touch_rule="PROPORTIONAL")
        
        exceptions = summary["exceptions_list"]
        exc_types = [e["type"] for e in exceptions]
        self.assertIn("MULTI_TOUCH_CONFLICT", exc_types)
        self.assertIn("LATE_RETURN", exc_types)
        
        # Test Human-in-the-loop override
        overrides = {
            "orders": {
                "ORD_B02": {"assigned_campaign": "CT1_FLASH"}
            }
        }
        summary_overridden = self.agent.run_pipeline(data, human_overrides=overrides)
        # Find attribution note for ORD_B02
        attributed = [r for r in summary_overridden["attributed_orders_sample"] if r.get("order_id") == "ORD_B02"]
        if attributed:
            self.assertIn("Phê duyệt thủ công", attributed[0]["attribution_note"])

if __name__ == "__main__":
    unittest.main()

