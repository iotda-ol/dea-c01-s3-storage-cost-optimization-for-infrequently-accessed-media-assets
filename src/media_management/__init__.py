"""
Media Management Module

Provides specialized functionality for managing media assets in S3.
"""

from src.media_management.media_processor import MediaProcessor
from src.media_management.metadata_manager import MetadataManager

__all__ = [
    "MediaProcessor",
    "MetadataManager",
]
