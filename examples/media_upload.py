#!/usr/bin/env python3
"""
Media Upload Example

Demonstrates uploading media assets with lifecycle management.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.s3_client import S3ClientWrapper
from src.media_management.media_processor import MediaProcessor
from src.media_management.metadata_manager import MetadataManager
from src.config.constants import MediaType
from src.utils.logger import setup_logger


def main():
    """Demonstrate media upload with metadata and tagging."""
    
    # Setup logging
    logger = setup_logger('media_example', level='INFO')
    logger.info("Starting media upload example...")
    
    # Initialize S3 client
    s3_client = S3ClientWrapper(region_name='us-east-1')
    
    # Example bucket name (replace with your bucket)
    bucket_name = "my-media-assets-bucket"
    
    # Initialize media processor and metadata manager
    media_processor = MediaProcessor(s3_client)
    metadata_mgr = MetadataManager(s3_client)
    
    # Example: Upload a single media file
    # file_path = "/path/to/video.mp4"
    # logger.info(f"Uploading media file: {file_path}")
    # 
    # success = media_processor.upload_media_asset(
    #     file_path=file_path,
    #     bucket_name=bucket_name,
    #     prefix="media/videos",
    #     storage_class="STANDARD",
    #     add_metadata=True
    # )
    # 
    # if success:
    #     logger.info("Upload successful!")
    #     
    #     # Add lifecycle tags
    #     object_key = f"media/videos/{os.path.basename(file_path)}"
    #     tags = metadata_mgr.create_lifecycle_tags(
    #         access_pattern="media",
    #         retention_years=1
    #     )
    #     
    #     metadata_mgr.tag_object(bucket_name, object_key, tags)
    #     logger.info(f"Tags added: {tags}")
    
    # Example: Batch upload from directory
    # media_dir = "/path/to/media/directory"
    # logger.info(f"Batch uploading from: {media_dir}")
    # 
    # results = media_processor.batch_upload_media(
    #     directory=media_dir,
    #     bucket_name=bucket_name,
    #     prefix="media",
    #     storage_class="STANDARD",
    #     media_types=[MediaType.VIDEO, MediaType.IMAGE]  # Upload only videos and images
    # )
    # 
    # logger.info(f"Upload results: {results['successful']}/{results['total']} successful")
    
    logger.info("Media upload example completed!")
    logger.info("Note: Uncomment the example code blocks and provide valid paths to test.")


if __name__ == "__main__":
    main()
