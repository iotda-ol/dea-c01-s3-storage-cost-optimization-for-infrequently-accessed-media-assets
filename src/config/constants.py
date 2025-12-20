"""
Constants Module

Defines reusable constants and enumerations for the application.
"""

from enum import Enum


class StorageClass(str, Enum):
    """S3 Storage Class enumeration."""
    STANDARD = "STANDARD"
    REDUCED_REDUNDANCY = "REDUCED_REDUNDANCY"
    STANDARD_IA = "STANDARD_IA"
    ONEZONE_IA = "ONEZONE_IA"
    INTELLIGENT_TIERING = "INTELLIGENT_TIERING"
    GLACIER = "GLACIER"
    DEEP_ARCHIVE = "DEEP_ARCHIVE"
    GLACIER_IR = "GLACIER_IR"


class LifecycleAction(str, Enum):
    """Lifecycle action types."""
    TRANSITION = "TRANSITION"
    EXPIRATION = "EXPIRATION"
    ABORT_INCOMPLETE_MULTIPART_UPLOAD = "ABORT_INCOMPLETE_MULTIPART_UPLOAD"
    NONCURRENT_VERSION_TRANSITION = "NONCURRENT_VERSION_TRANSITION"
    NONCURRENT_VERSION_EXPIRATION = "NONCURRENT_VERSION_EXPIRATION"


class MediaType(str, Enum):
    """Media asset types."""
    VIDEO = "VIDEO"
    IMAGE = "IMAGE"
    AUDIO = "AUDIO"
    DOCUMENT = "DOCUMENT"
    OTHER = "OTHER"


# Default lifecycle transition days
DEFAULT_STANDARD_IA_DAYS = 30
DEFAULT_GLACIER_DAYS = 90
DEFAULT_DEEP_ARCHIVE_DAYS = 180
DEFAULT_EXPIRATION_DAYS = 365

# Storage class minimum storage duration (days)
MIN_STORAGE_DURATION = {
    StorageClass.STANDARD: 0,
    StorageClass.STANDARD_IA: 30,
    StorageClass.ONEZONE_IA: 30,
    StorageClass.GLACIER: 90,
    StorageClass.DEEP_ARCHIVE: 180,
}

# Storage class minimum object size (bytes)
MIN_OBJECT_SIZE = {
    StorageClass.STANDARD: 0,
    StorageClass.STANDARD_IA: 128 * 1024,  # 128 KB
    StorageClass.ONEZONE_IA: 128 * 1024,   # 128 KB
    StorageClass.GLACIER: 0,
    StorageClass.DEEP_ARCHIVE: 0,
}

# Media file extensions by type
MEDIA_EXTENSIONS = {
    MediaType.VIDEO: ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.m4v'],
    MediaType.IMAGE: ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'],
    MediaType.AUDIO: ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a'],
    MediaType.DOCUMENT: ['.pdf', '.doc', '.docx', '.txt', '.md', '.rtf'],
}
