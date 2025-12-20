"""
S3 Storage Cost Optimization for Infrequently Accessed Media Assets

This package provides reusable modules for optimizing S3 storage costs
through lifecycle policies and intelligent tiering strategies.
"""

__version__ = "1.0.0"
__author__ = "AWS Solutions Team"

from src.core.lifecycle_manager import LifecycleManager
from src.core.s3_client import S3ClientWrapper
from src.config.settings import Settings

__all__ = [
    "LifecycleManager",
    "S3ClientWrapper",
    "Settings",
]
