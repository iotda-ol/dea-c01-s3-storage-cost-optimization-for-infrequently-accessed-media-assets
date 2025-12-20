"""
Lifecycle Manager Module

Handles creation, updating, and management of S3 lifecycle policies
for cost optimization through storage class transitions.
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class LifecycleManager:
    """
    Manages S3 bucket lifecycle policies for storage cost optimization.
    
    This class provides reusable methods to create and manage lifecycle
    rules that transition objects from S3 Standard to S3 Standard-IA
    and eventually to Glacier for long-term archival.
    """
    
    def __init__(self, s3_client):
        """
        Initialize the LifecycleManager.
        
        Args:
            s3_client: Boto3 S3 client or S3ClientWrapper instance
        """
        self.s3_client = s3_client
        self.logger = logger
    
    def create_media_lifecycle_policy(
        self,
        bucket_name: str,
        standard_ia_days: int = 30,
        glacier_days: int = 90,
        expiration_days: Optional[int] = None,
        prefix: str = "",
        tags: Optional[Dict[str, str]] = None
    ) -> Dict:
        """
        Create a lifecycle policy optimized for media assets.
        
        Args:
            bucket_name: Name of the S3 bucket
            standard_ia_days: Days before transition to Standard-IA
            glacier_days: Days before transition to Glacier
            expiration_days: Days before object expiration (optional)
            prefix: Object prefix filter
            tags: Tag filters for lifecycle rule
            
        Returns:
            Dict containing the created lifecycle configuration
        """
        rules = []
        
        # Rule for transitioning to Standard-IA
        rule = {
            'ID': f'MediaAssetOptimization-{datetime.now().strftime("%Y%m%d")}',
            'Status': 'Enabled',
            'Prefix': prefix,
            'Transitions': [
                {
                    'Days': standard_ia_days,
                    'StorageClass': 'STANDARD_IA'
                },
                {
                    'Days': glacier_days,
                    'StorageClass': 'GLACIER'
                }
            ]
        }
        
        # Add expiration if specified
        if expiration_days:
            rule['Expiration'] = {'Days': expiration_days}
        
        # Add tag filter if specified
        if tags:
            rule['Filter'] = {
                'And': {
                    'Prefix': prefix,
                    'Tags': [{'Key': k, 'Value': v} for k, v in tags.items()]
                }
            }
        
        rules.append(rule)
        
        lifecycle_config = {'Rules': rules}
        
        self.logger.info(f"Creating lifecycle policy for bucket: {bucket_name}")
        return lifecycle_config
    
    def apply_lifecycle_policy(
        self,
        bucket_name: str,
        lifecycle_config: Dict
    ) -> bool:
        """
        Apply a lifecycle policy to an S3 bucket.
        
        Args:
            bucket_name: Name of the S3 bucket
            lifecycle_config: Lifecycle configuration dictionary
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            client = getattr(self.s3_client, 'client', self.s3_client)
            client.put_bucket_lifecycle_configuration(
                Bucket=bucket_name,
                LifecycleConfiguration=lifecycle_config
            )
            self.logger.info(f"Successfully applied lifecycle policy to {bucket_name}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to apply lifecycle policy: {str(e)}")
            return False
    
    def get_lifecycle_policy(self, bucket_name: str) -> Optional[Dict]:
        """
        Retrieve the current lifecycle policy of a bucket.
        
        Args:
            bucket_name: Name of the S3 bucket
            
        Returns:
            Dict containing the lifecycle configuration or None
        """
        try:
            client = getattr(self.s3_client, 'client', self.s3_client)
            response = client.get_bucket_lifecycle_configuration(
                Bucket=bucket_name
            )
            return response
        except client.exceptions.NoSuchLifecycleConfiguration:
            self.logger.info(f"No lifecycle configuration found for {bucket_name}")
            return None
        except Exception as e:
            self.logger.error(f"Error retrieving lifecycle policy: {str(e)}")
            return None
    
    def delete_lifecycle_policy(self, bucket_name: str) -> bool:
        """
        Delete the lifecycle policy from a bucket.
        
        Args:
            bucket_name: Name of the S3 bucket
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            client = getattr(self.s3_client, 'client', self.s3_client)
            client.delete_bucket_lifecycle(Bucket=bucket_name)
            self.logger.info(f"Successfully deleted lifecycle policy from {bucket_name}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to delete lifecycle policy: {str(e)}")
            return False
