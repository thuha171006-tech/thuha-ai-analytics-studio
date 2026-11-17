"""
Configuration Module for Thu Hà AI Analytics Studio - Multi-Project Sales Evaluation Agent
Stores API keys, model selections, and business benchmark parameters.
"""

import os

def load_env():
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ[key.strip()] = val.strip()

load_env()

# Google Gemini AI Studio API Configuration
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AQ.Ab8RN6I62QIBTsipWCkLI-79El8GUlz2xKq_jZ145OR859dmGg")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash-lite")

# Benchmark business thresholds
TARGET_CM_PCT = 15.0         # Kỳ vọng biên lợi nhuận đóng góp tối thiểu 15%
MAX_RETURN_RATE_PCT = 12.0   # Tỷ lệ hoàn hàng tối đa cho phép 12%

