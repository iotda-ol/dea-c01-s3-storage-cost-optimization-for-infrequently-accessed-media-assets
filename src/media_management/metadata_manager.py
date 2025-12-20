"""
Metadata Manager Module

Manages metadata and tagging for media assets in S3.
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class MetadataManager:
    """
    Manages metadata and tags for S3 objects.
    
    Provides reusable methods for adding, updating, and querying
    object metadata and tags for improved organization and lifecycle management.
    """
    
    def __init__(self, s3_client):
        """
        Initialize the MetadataManager.
        
        Args:
            s3_client: S3ClientWrapper instance
        """
        self.s3_client = s3_client
        self.logger = logger
    
    def tag_object(
        self,
        bucket_name: str,
        object_key: str,
        tags: Dict[str, str]
    ) -> bool:
        """
        Add tags to an S3 object.
        
        Args:
            bucket_name: S3 bucket name
            object_key: S3 object key
            tags: Dictionary of tag key-value pairs
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            client = getattr(self.s3_client, 'client', self.s3_client)
            
            tag_set = [{'Key': k, 'Value': v} for k, v in tags.items()]
            
            client.put_object_tagging(
                Bucket=bucket_name,
                Key=object_key,
                Tagging={'TagSet': tag_set}
            )
            
            self.logger.info(f"Tagged object: {object_key}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to tag object: {str(e)}")
            return False
    
    def get_object_tags(
        self,
        bucket_name: str,
        object_key: str
    ) -> Optional[Dict[str, str]]:
        """
        Get tags from an S3 object.
        
        Args:
            bucket_name: S3 bucket name
            object_key: S3 object key
            
        Returns:
            Dict of tags or None
        """
        try:
            client = getattr(self.s3_client, 'client', self.s3_client)
            
            response = client.get_object_tagging(
                Bucket=bucket_name,
                Key=object_key
            )
            
            tags = {tag['Key']: tag['Value'] for tag in response.get('TagSet', [])}
            return tags
            
        except Exception as e:
            self.logger.error(f"Failed to get object tags: {str(e)}")
            return None
    
    def update_object_metadata(
        self,
        bucket_name: str,
        object_key: str,
        metadata: Dict[str, str]
    ) -> bool:
        """
        Update metadata for an S3 object.
        
        Note: This requires copying the object to itself with new metadata.
        
        Args:
            bucket_name: S3 bucket name
            object_key: S3 object key
            metadata: New metadata dictionary
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            client = getattr(self.s3_client, 'client', self.s3_client)
            
            # Copy object to itself with new metadata
            copy_source = {'Bucket': bucket_name, 'Key': object_key}
            
            client.copy_object(
                Bucket=bucket_name,
                Key=object_key,
                CopySource=copy_source,
                Metadata=metadata,
                MetadataDirective='REPLACE'
            )
            
            self.logger.info(f"Updated metadata for: {object_key}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to update metadata: {str(e)}")
            return False
    
    def batch_tag_objects(
        self,
        bucket_name: str,
        prefix: str,
        tags: Dict[str, str]
    ) -> Dict:
        """
        Batch tag objects with a specific prefix.
        
        Args:
            bucket_name: S3 bucket name
            prefix: Object key prefix
            tags: Tags to apply
            
        Returns:
            Dict with operation statistics
        """
        results = {
            'total': 0,
            'successful': 0,
            'failed': 0
        }
        
        try:
            objects = self.s3_client.list_objects(bucket_name, prefix)
            results['total'] = len(objects)
            
            for obj in objects:
                object_key = obj['Key']
                success = self.tag_object(bucket_name, object_key, tags)
                
                if success:
                    results['successful'] += 1
                else:
                    results['failed'] += 1
            
            self.logger.info(
                f"Batch tagging completed: {results['successful']}/{results['total']} successful"
            )
            
        except Exception as e:
            self.logger.error(f"Batch tagging failed: {str(e)}")
        
        return results
    
    def create_lifecycle_tags(
        self,
        access_pattern: str = "media",
        retention_years: int = 1
    ) -> Dict[str, str]:
        """
        Create recommended tags for lifecycle management.
        
        Args:
            access_pattern: Type of access pattern
            retention_years: Retention period in years
            
        Returns:
            Dict of recommended tags
        """
        return {
            'AccessPattern': access_pattern,
            'RetentionYears': str(retention_years),
            'LifecycleManaged': 'true',
            'CreatedDate': datetime.now().strftime('%Y-%m-%d')
        }
