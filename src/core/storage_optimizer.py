"""
Storage Optimizer Module

Analyzes storage usage patterns and provides optimization recommendations
for S3 storage classes and lifecycle policies.
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class StorageOptimizer:
    """
    Analyzes S3 storage patterns and provides cost optimization recommendations.
    
    This class provides reusable methods to analyze object access patterns,
    calculate potential cost savings, and recommend optimal lifecycle policies.
    """
    
    # Storage class pricing (example prices per GB/month in USD)
    STORAGE_PRICING = {
        'STANDARD': 0.023,
        'STANDARD_IA': 0.0125,
        'GLACIER': 0.004,
        'DEEP_ARCHIVE': 0.00099
    }
    
    def __init__(self, s3_client):
        """
        Initialize the StorageOptimizer.
        
        Args:
            s3_client: Boto3 S3 client or S3ClientWrapper instance
        """
        self.s3_client = s3_client
        self.logger = logger
    
    def analyze_bucket_storage(
        self,
        bucket_name: str,
        prefix: str = ""
    ) -> Dict:
        """
        Analyze storage distribution across storage classes.
        
        Args:
            bucket_name: Name of the S3 bucket
            prefix: Object prefix filter
            
        Returns:
            Dict containing storage analysis results
        """
        client = getattr(self.s3_client, 'client', self.s3_client)
        
        storage_distribution = {
            'STANDARD': {'count': 0, 'size': 0},
            'STANDARD_IA': {'count': 0, 'size': 0},
            'GLACIER': {'count': 0, 'size': 0},
            'DEEP_ARCHIVE': {'count': 0, 'size': 0},
            'OTHER': {'count': 0, 'size': 0}
        }
        
        try:
            paginator = client.get_paginator('list_objects_v2')
            pages = paginator.paginate(Bucket=bucket_name, Prefix=prefix)
            
            for page in pages:
                for obj in page.get('Contents', []):
                    storage_class = obj.get('StorageClass', 'STANDARD')
                    size = obj.get('Size', 0)
                    
                    if storage_class in storage_distribution:
                        storage_distribution[storage_class]['count'] += 1
                        storage_distribution[storage_class]['size'] += size
                    else:
                        storage_distribution['OTHER']['count'] += 1
                        storage_distribution['OTHER']['size'] += size
            
            self.logger.info(f"Completed storage analysis for {bucket_name}")
            return storage_distribution
            
        except Exception as e:
            self.logger.error(f"Error analyzing bucket storage: {str(e)}")
            return storage_distribution
    
    def calculate_cost_savings(
        self,
        current_storage_gb: float,
        current_class: str,
        target_class: str
    ) -> Dict:
        """
        Calculate potential cost savings from storage class transition.
        
        Args:
            current_storage_gb: Current storage size in GB
            current_class: Current storage class
            target_class: Target storage class
            
        Returns:
            Dict containing cost savings calculation
        """
        current_cost = current_storage_gb * self.STORAGE_PRICING.get(current_class, 0)
        target_cost = current_storage_gb * self.STORAGE_PRICING.get(target_class, 0)
        monthly_savings = current_cost - target_cost
        annual_savings = monthly_savings * 12
        
        return {
            'current_monthly_cost': round(current_cost, 2),
            'target_monthly_cost': round(target_cost, 2),
            'monthly_savings': round(monthly_savings, 2),
            'annual_savings': round(annual_savings, 2),
            'savings_percentage': round((monthly_savings / current_cost * 100), 2) if current_cost > 0 else 0
        }
    
    def recommend_lifecycle_policy(
        self,
        bucket_name: str,
        access_pattern: str = "media"
    ) -> Dict:
        """
        Generate lifecycle policy recommendations based on usage patterns.
        
        Args:
            bucket_name: Name of the S3 bucket
            access_pattern: Type of access pattern (media, archive, backup)
            
        Returns:
            Dict containing recommended lifecycle policy
        """
        recommendations = {
            'media': {
                'standard_ia_days': 30,
                'glacier_days': 90,
                'expiration_days': 365,
                'description': 'Optimized for media assets with initial high access, declining over time'
            },
            'archive': {
                'standard_ia_days': 7,
                'glacier_days': 30,
                'expiration_days': None,
                'description': 'Optimized for archival data with rare access'
            },
            'backup': {
                'standard_ia_days': 1,
                'glacier_days': 30,
                'expiration_days': 90,
                'description': 'Optimized for backup data with retention policy'
            }
        }
        
        pattern = access_pattern.lower()
        if pattern not in recommendations:
            pattern = 'media'  # Default to media pattern
        
        return recommendations[pattern]
    
    def get_optimization_report(
        self,
        bucket_name: str,
        prefix: str = ""
    ) -> Dict:
        """
        Generate a comprehensive optimization report for a bucket.
        
        Args:
            bucket_name: Name of the S3 bucket
            prefix: Object prefix filter
            
        Returns:
            Dict containing comprehensive optimization report
        """
        storage_analysis = self.analyze_bucket_storage(bucket_name, prefix)
        
        # Calculate total storage
        total_size_bytes = sum(
            class_data['size'] for class_data in storage_analysis.values()
        )
        total_size_gb = total_size_bytes / (1024 ** 3)
        
        # Calculate potential savings if all STANDARD moved to STANDARD_IA
        standard_size_gb = storage_analysis['STANDARD']['size'] / (1024 ** 3)
        cost_savings = self.calculate_cost_savings(
            standard_size_gb,
            'STANDARD',
            'STANDARD_IA'
        )
        
        recommendation = self.recommend_lifecycle_policy(bucket_name)
        
        return {
            'bucket_name': bucket_name,
            'total_size_gb': round(total_size_gb, 2),
            'storage_distribution': storage_analysis,
            'potential_savings': cost_savings,
            'recommended_policy': recommendation,
            'analysis_date': datetime.now().isoformat()
        }
