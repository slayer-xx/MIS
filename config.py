"""
Application Configuration
Centralized configuration for the Real Estate MIS application.
"""
import os
from pathlib import Path

# Application Information
APP_NAME = "Real Estate MIS"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Your Company"

# Directories
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# Database Configuration
DATABASE_PATH = DATA_DIR / "real_estate_mis.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# UI Configuration
WINDOW_MIN_WIDTH = 1024
WINDOW_MIN_HEIGHT = 600
WINDOW_DEFAULT_WIDTH = 1280
WINDOW_DEFAULT_HEIGHT = 720

# Deal Configuration
DEAL_TYPES = ["Builder", "Resale", "Rental"]
DEAL_STATUSES = ["Lead", "Site Visit", "Negotiation", "Booked", "Closed", "Lost"]

# Date Format
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
DISPLAY_DATE_FORMAT = "%d %b %Y, %I:%M %p"
