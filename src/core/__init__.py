"""
Core module for S3 lifecycle and storage management.

This module contains the core business logic for managing S3 lifecycle
policies, bucket operations, and storage class transitions.
"""

from src.core.lifecycle_manager import LifecycleManager
from src.core.s3_client import S3ClientWrapper
from src.core.storage_optimizer import StorageOptimizer

__all__ = [
    "LifecycleManager",
    "S3ClientWrapper",
    "StorageOptimizer",
]
