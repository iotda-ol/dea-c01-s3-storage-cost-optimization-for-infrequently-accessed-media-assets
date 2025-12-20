#!/usr/bin/env python3
"""
Cost Analysis Example

Demonstrates storage cost analysis and optimization reporting.
"""

import sys
import os
import json

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.s3_client import S3ClientWrapper
from src.core.storage_optimizer import StorageOptimizer
from src.utils.logger import setup_logger
from src.utils.formatters import format_bytes, format_cost


def main():
    """Demonstrate storage cost analysis."""
    
    # Setup logging
    logger = setup_logger('cost_example', level='INFO')
    logger.info("Starting cost analysis example...")
    
    # Initialize S3 client
    s3_client = S3ClientWrapper(region_name='us-east-1')
    
    # Example bucket name (replace with your bucket)
    bucket_name = "my-media-assets-bucket"
    
    # Initialize storage optimizer
    optimizer = StorageOptimizer(s3_client)
    
    # Generate comprehensive optimization report
    logger.info(f"Analyzing bucket: {bucket_name}")
    # report = optimizer.get_optimization_report(bucket_name, prefix="media/")
    # 
    # logger.info("=" * 60)
    # logger.info("STORAGE OPTIMIZATION REPORT")
    # logger.info("=" * 60)
    # logger.info(f"Bucket: {report['bucket_name']}")
    # logger.info(f"Total Storage: {format_bytes(report['total_size_gb'] * 1024**3)}")
    # logger.info("")
    # 
    # logger.info("Storage Distribution:")
    # for storage_class, data in report['storage_distribution'].items():
    #     if data['count'] > 0:
    #         logger.info(f"  {storage_class}: {data['count']} objects, {format_bytes(data['size'])}")
    # 
    # logger.info("")
    # logger.info("Potential Savings (STANDARD → STANDARD_IA):")
    # savings = report['potential_savings']
    # logger.info(f"  Current Monthly Cost: {format_cost(savings['current_monthly_cost'])}")
    # logger.info(f"  Target Monthly Cost: {format_cost(savings['target_monthly_cost'])}")
    # logger.info(f"  Monthly Savings: {format_cost(savings['monthly_savings'])}")
    # logger.info(f"  Annual Savings: {format_cost(savings['annual_savings'])}")
    # logger.info(f"  Savings Percentage: {savings['savings_percentage']}%")
    # 
    # logger.info("")
    # logger.info("Recommended Lifecycle Policy:")
    # policy = report['recommended_policy']
    # logger.info(f"  Description: {policy['description']}")
    # logger.info(f"  Standard-IA Transition: {policy['standard_ia_days']} days")
    # logger.info(f"  Glacier Transition: {policy['glacier_days']} days")
    # if policy['expiration_days']:
    #     logger.info(f"  Expiration: {policy['expiration_days']} days")
    # 
    # logger.info("=" * 60)
    
    # Example: Compare different storage classes
    logger.info("\nComparing Storage Classes for 500 GB:")
    logger.info("-" * 60)
    
    storage_classes = ['STANDARD', 'STANDARD_IA', 'GLACIER', 'DEEP_ARCHIVE']
    storage_gb = 500
    
    for storage_class in storage_classes:
        savings = optimizer.calculate_cost_savings(
            current_storage_gb=storage_gb,
            current_class='STANDARD',
            target_class=storage_class
        )
        
        logger.info(f"{storage_class}:")
        logger.info(f"  Monthly Cost: {format_cost(savings['target_monthly_cost'])}")
        logger.info(f"  Monthly Savings: {format_cost(savings['monthly_savings'])}")
        logger.info(f"  Savings: {savings['savings_percentage']}%")
    
    logger.info("\nCost analysis example completed!")
    logger.info("Note: Uncomment the report generation code to analyze a real bucket.")


if __name__ == "__main__":
    main()
