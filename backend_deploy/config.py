"""
BiasLens — config.py (Debugged)
Central settings. All API keys loaded from .env file.
"""
from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    APP_NAME: str = "BiasLens API"
    VERSION: str = "2.6.0"
    DEBUG: bool = True

    # CORS — allow HTML opened directly in browser (file://) and localhost
    # Note: "null" is required for local file:// access in some browsers
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "null",
        "*", 
    ]

    # File upload settings
    MAX_FILE_SIZE_MB: int = 100
    UPLOAD_DIR: str = "uploads"

    # ── AI API Keys (Loaded from .env if present) ──────────────────────────
    NVIDIA_API_KEY: str = ""
    GEMINI_API_KEY: str = ""

    # ── Fairness Thresholds (Standard Industry Defaults) ───────────────────
    # Based on the 80% rule for Disparate Impact
    DISPARATE_IMPACT_THRESHOLD: float = 0.80
    STATISTICAL_PARITY_THRESHOLD: float = 0.10
    EQUAL_OPPORTUNITY_THRESHOLD: float = 0.10
    CALIBRATION_THRESHOLD: float = 0.70

    # ── Auto-detection Keywords ───────────────────────────────────────────────
    # Expanded list for better detection in raw CSVs
    SENSITIVE_ATTR_KEYWORDS: List[str] = [
        "gender", "sex", "race", "ethnicity", "age", "disability",
        "religion", "nationality", "marital", "pregnant", "color",
        "origin", "veteran", "sexual_orientation", "caste",
        "income", "education", "language", "tribe",
    ]

    LABEL_KEYWORDS: List[str] = [
        "label", "target", "outcome", "result", "decision",
        "approved", "hired", "accepted", "granted", "prediction",
        "class", "y", "output", "status", "default", "churn",
        "fraud", "loan", "admit", "pass", "fail",
    ]

    # ── Database & Auth ──────────────────────────────────────────────────────
    DATABASE_URL: str = "sqlite:///./biaslens.db"
    DATABASE_PATH: str = "users.db"
    SECRET_KEY: str = ""  # Set via environment in production; keep empty in repo
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 # 24 hours

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8' # Ensure no Unicode errors here
        extra = "ignore"


# Create settings instance
settings = Settings()

# Ensure upload directory exists with proper permissions
if not os.path.exists(settings.UPLOAD_DIR):
    try:
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    except Exception as e:
        print(f"Warning: Could not create upload directory: {e}")