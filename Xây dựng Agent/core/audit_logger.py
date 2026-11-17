"""
Audit Logger for Thu Hà AI Analytics Studio - Multi-Project Sales Evaluation Agent
Provides verifiable execution trail, tool call logs, rule tracking, and exception events.
"""

import json
import time
from datetime import datetime
from typing import List, Dict, Any

class AuditLogger:
    def __init__(self):
        self.logs: List[Dict[str, Any]] = []

    def log(self, step: str, action: str, tool_name: str, message: str, details: Any = None, level: str = "INFO"):
        entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
            "step": step,
            "action": action,
            "tool_name": tool_name,
            "message": message,
            "details": details if details is not None else {},
            "level": level
        }
        self.logs.append(entry)

    def log_tool_call(self, tool_name: str, inputs: Dict[str, Any], output_summary: str):
        self.log(
            step="TOOL_EXECUTION",
            action="TOOL_CALL",
            tool_name=tool_name,
            message=f"Đã gọi công cụ [{tool_name}]",
            details={"inputs": inputs, "output_summary": output_summary},
            level="INFO"
        )

    def log_rule(self, rule_id: str, rule_name: str, condition: str, impact_count: int, note: str = ""):
        self.log(
            step="RULE_EVALUATION",
            action="RULE_APPLIED",
            tool_name=rule_id,
            message=f"Áp dụng quy tắc [{rule_id}] - {rule_name}: {impact_count} bản ghi bị ảnh hưởng",
            details={"rule_id": rule_id, "rule_name": rule_name, "condition": condition, "impact_count": impact_count, "note": note},
            level="INFO"
        )

    def log_anomaly(self, anomaly_type: str, item_id: str, reason: str, suggested_action: str):
        self.log(
            step="ANOMALY_DETECTION",
            action="ANOMALY_DETECTED",
            tool_name="AnomalyDetector",
            message=f"Phát hiện ngoại lệ [{anomaly_type}] trên [{item_id}]: {reason}",
            details={"anomaly_type": anomaly_type, "item_id": item_id, "reason": reason, "suggested_action": suggested_action},
            level="WARNING"
        )

    def log_human_intervention(self, checkpoint: str, decision: str, applied_by: str = "Trưởng phòng Kinh doanh"):
        self.log(
            step="HUMAN_IN_THE_LOOP",
            action="HUMAN_DECISION",
            tool_name=checkpoint,
            message=f"Con người can thiệp tại [{checkpoint}]: {decision} (Bởi: {applied_by})",
            details={"checkpoint": checkpoint, "decision": decision, "applied_by": applied_by},
            level="ACTION_REQUIRED"
        )

    def get_logs(self) -> List[Dict[str, Any]]:
        return self.logs

    def to_json(self) -> str:
        return json.dumps(self.logs, ensure_ascii=False, indent=2)

    def clear(self):
        self.logs = []

