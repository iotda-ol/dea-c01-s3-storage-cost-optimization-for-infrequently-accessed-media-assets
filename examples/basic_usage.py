#!/usr/bin/env python3
"""
Basic Usage Example

Demonstrates basic usage of the S3 cost optimization modules.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.s3_client import S3ClientWrapper
from src.core.lifecycle_manager import LifecycleManager
from src.core.storage_optimizer import StorageOptimizer
from src.config.settings import Settings
from src.utils.logger import setup_logger


def main():
    """Demonstrate basic usage of the cost optimization tools."""
    
    # Setup logging
    logger = setup_logger('example', level='INFO')
    logger.info("Starting S3 cost optimization example...")
    
    # Load settings
    settings = Settings()
    
    # Initialize S3 client
    s3_client = S3ClientWrapper(
        region_name=settings.get('aws.region')
    )
    
    # Example bucket name (replace with your bucket)
    bucket_name = "my-media-assets-bucket"
    
    # Initialize managers
    lifecycle_mgr = LifecycleManager(s3_client)
    optimizer = StorageOptimizer(s3_client)
    
    # Create a lifecycle policy for media assets
    logger.info("Creating lifecycle policy...")
    lifecycle_config = lifecycle_mgr.create_media_lifecycle_policy(
        bucket_name=bucket_name,
        standard_ia_days=30,  # Move to Standard-IA after 30 days
        glacier_days=90,      # Move to Glacier after 90 days
        expiration_days=365,  # Delete after 1 year
        prefix="media/"
    )
    
    logger.info(f"Lifecycle policy created: {lifecycle_config}")
    
    # Get optimization recommendations
    logger.info("Analyzing bucket for optimization opportunities...")
    recommendation = optimizer.recommend_lifecycle_policy(bucket_name, "media")
    logger.info(f"Recommendation: {recommendation}")
    
    # Calculate potential savings
    logger.info("Calculating potential cost savings...")
    savings = optimizer.calculate_cost_savings(
        current_storage_gb=100,  # Example: 100 GB
        current_class='STANDARD',
        target_class='STANDARD_IA'
    )
    
    logger.info(f"Monthly savings: ${savings['monthly_savings']}")
    logger.info(f"Annual savings: ${savings['annual_savings']}")
    logger.info(f"Savings percentage: {savings['savings_percentage']}%")
    
    logger.info("Example completed successfully!")


if __name__ == "__main__":
    main()
