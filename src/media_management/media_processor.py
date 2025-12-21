"""
Media Processor Module

Handles media asset processing, classification, and upload operations.
"""

import logging
import os
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

from src.config.constants import MediaType, MEDIA_EXTENSIONS

logger = logging.getLogger(__name__)


class MediaProcessor:
    """
    Processes and manages media assets for S3 storage.
    
    Provides reusable methods for media file classification,
    metadata extraction, and batch upload operations.
    """
    
    def __init__(self, s3_client):
        """
        Initialize the MediaProcessor.
        
        Args:
            s3_client: S3ClientWrapper instance
        """
        self.s3_client = s3_client
        self.logger = logger
    
    def classify_media_type(self, file_path: str) -> MediaType:
        """
        Classify media file based on extension.
        
        Args:
            file_path: Path to media file
            
        Returns:
            MediaType enum value
        """
        ext = Path(file_path).suffix.lower()
        
        for media_type, extensions in MEDIA_EXTENSIONS.items():
            if ext in extensions:
                return media_type
        
        return MediaType.OTHER
    
    def get_file_metadata(self, file_path: str) -> Dict:
        """
        Extract metadata from a file.
        
        Args:
            file_path: Path to file
            
        Returns:
            Dict containing file metadata
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        stat = path.stat()
        
        return {
            'filename': path.name,
            'size': stat.st_size,
            'extension': path.suffix.lower(),
            'media_type': self.classify_media_type(file_path).value,
            'modified_time': datetime.fromtimestamp(stat.st_mtime).isoformat(),
            'created_time': datetime.fromtimestamp(stat.st_ctime).isoformat()
        }
    
    def upload_media_asset(
        self,
        file_path: str,
        bucket_name: str,
        prefix: str = "",
        storage_class: str = "STANDARD",
        add_metadata: bool = True
    ) -> bool:
        """
        Upload a media asset to S3 with appropriate metadata.
        
        Args:
            file_path: Local file path
            bucket_name: S3 bucket name
            prefix: S3 key prefix
            storage_class: Initial storage class
            add_metadata: Whether to add file metadata
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            file_metadata = self.get_file_metadata(file_path)
            
            # Create object key
            filename = Path(file_path).name
            object_key = f"{prefix}/{filename}".lstrip('/')
            
            # Prepare S3 metadata
            s3_metadata = None
            if add_metadata:
                s3_metadata = {
                    'media-type': file_metadata['media_type'],
                    'original-size': str(file_metadata['size']),
                    'upload-date': datetime.now().isoformat()
                }
            
            # Upload file
            success = self.s3_client.upload_file(
                file_path=file_path,
                bucket_name=bucket_name,
                object_key=object_key,
                metadata=s3_metadata,
                storage_class=storage_class
            )
            
            if success:
                self.logger.info(f"Uploaded media asset: {object_key}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Failed to upload media asset: {str(e)}")
            return False
    
    def batch_upload_media(
        self,
        directory: str,
        bucket_name: str,
        prefix: str = "",
        storage_class: str = "STANDARD",
        media_types: Optional[List[MediaType]] = None
    ) -> Dict:
        """
        Batch upload media files from a directory.
        
        Args:
            directory: Local directory path
            bucket_name: S3 bucket name
            prefix: S3 key prefix
            storage_class: Initial storage class
            media_types: Filter by media types (None = all types)
            
        Returns:
            Dict with upload statistics
        """
        dir_path = Path(directory)
        
        if not dir_path.is_dir():
            raise NotADirectoryError(f"Not a directory: {directory}")
        
        results = {
            'total': 0,
            'successful': 0,
            'failed': 0,
            'skipped': 0,
            'files': []
        }
        
        # Get all files
        for file_path in dir_path.rglob('*'):
            if file_path.is_file():
                results['total'] += 1
                
                # Check media type filter
                file_type = self.classify_media_type(str(file_path))
                if media_types and file_type not in media_types:
                    results['skipped'] += 1
                    continue
                
                # Calculate relative path for S3 key
                relative_path = file_path.relative_to(dir_path)
                file_prefix = f"{prefix}/{relative_path.parent}".strip('/')
                
                # Upload file
                success = self.upload_media_asset(
                    file_path=str(file_path),
                    bucket_name=bucket_name,
                    prefix=file_prefix,
                    storage_class=storage_class
                )
                
                if success:
                    results['successful'] += 1
                else:
                    results['failed'] += 1
                
                results['files'].append({
                    'path': str(relative_path),
                    'type': file_type.value,
                    'success': success
                })
        
        self.logger.info(
            f"Batch upload completed: {results['successful']}/{results['total']} successful"
        )
        
        return results
    
    def recommend_storage_class(
        self,
        file_path: str,
        access_frequency: str = "high"
    ) -> str:
        """
        Recommend storage class based on file characteristics and access pattern.
        
        Args:
            file_path: Path to file
            access_frequency: Expected access frequency (high, medium, low)
            
        Returns:
            Recommended storage class
        """
        metadata = self.get_file_metadata(file_path)
        file_size = metadata['size']
        
        # Small files (< 128KB) should use STANDARD
        if file_size < 128 * 1024:
            return "STANDARD"
        
        # Recommend based on access frequency
        if access_frequency == "high":
            return "STANDARD"
        elif access_frequency == "medium":
            return "STANDARD_IA"
        else:  # low
            return "GLACIER"
