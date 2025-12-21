"""
S3 Client Wrapper Module

Provides a reusable wrapper around boto3 S3 client with enhanced
error handling, logging, and convenience methods.
"""

import logging
from typing import Optional, Dict, List
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


class S3ClientWrapper:
    """
    A wrapper class for boto3 S3 client with enhanced functionality.
    
    Provides reusable methods for common S3 operations with built-in
    error handling and logging.
    """
    
    def __init__(
        self,
        region_name: Optional[str] = None,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        profile_name: Optional[str] = None
    ):
        """
        Initialize the S3 client wrapper.
        
        Args:
            region_name: AWS region name
            aws_access_key_id: AWS access key ID
            aws_secret_access_key: AWS secret access key
            profile_name: AWS profile name from credentials file
        """
        session_params = {}
        
        if profile_name:
            session_params['profile_name'] = profile_name
        if region_name:
            session_params['region_name'] = region_name
        if aws_access_key_id and aws_secret_access_key:
            session_params['aws_access_key_id'] = aws_access_key_id
            session_params['aws_secret_access_key'] = aws_secret_access_key
        
        self.session = boto3.Session(**session_params) if session_params else boto3.Session()
        self.client = self.session.client('s3')
        self.logger = logger
    
    def bucket_exists(self, bucket_name: str) -> bool:
        """
        Check if an S3 bucket exists and is accessible.
        
        Args:
            bucket_name: Name of the S3 bucket
            
        Returns:
            bool: True if bucket exists, False otherwise
        """
        try:
            self.client.head_bucket(Bucket=bucket_name)
            return True
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == '404':
                return False
            self.logger.error(f"Error checking bucket existence: {str(e)}")
            return False
    
    def create_bucket(
        self,
        bucket_name: str,
        region: Optional[str] = None
    ) -> bool:
        """
        Create an S3 bucket.
        
        Args:
            bucket_name: Name of the S3 bucket
            region: AWS region for bucket creation
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if region and region != 'us-east-1':
                self.client.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={'LocationConstraint': region}
                )
            else:
                self.client.create_bucket(Bucket=bucket_name)
            
            self.logger.info(f"Successfully created bucket: {bucket_name}")
            return True
        except ClientError as e:
            self.logger.error(f"Failed to create bucket: {str(e)}")
            return False
    
    def upload_file(
        self,
        file_path: str,
        bucket_name: str,
        object_key: str,
        metadata: Optional[Dict[str, str]] = None,
        storage_class: str = 'STANDARD'
    ) -> bool:
        """
        Upload a file to S3.
        
        Args:
            file_path: Local file path
            bucket_name: S3 bucket name
            object_key: S3 object key
            metadata: Custom metadata
            storage_class: S3 storage class
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            extra_args = {'StorageClass': storage_class}
            if metadata:
                extra_args['Metadata'] = metadata
            
            self.client.upload_file(
                file_path,
                bucket_name,
                object_key,
                ExtraArgs=extra_args
            )
            self.logger.info(f"Successfully uploaded {file_path} to {bucket_name}/{object_key}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to upload file: {str(e)}")
            return False
    
    def get_object_storage_class(
        self,
        bucket_name: str,
        object_key: str
    ) -> Optional[str]:
        """
        Get the storage class of an S3 object.
        
        Args:
            bucket_name: S3 bucket name
            object_key: S3 object key
            
        Returns:
            str: Storage class name or None
        """
        try:
            response = self.client.head_object(
                Bucket=bucket_name,
                Key=object_key
            )
            return response.get('StorageClass', 'STANDARD')
        except Exception as e:
            self.logger.error(f"Failed to get object storage class: {str(e)}")
            return None
    
    def list_objects(
        self,
        bucket_name: str,
        prefix: str = "",
        max_keys: int = 1000
    ) -> List[Dict]:
        """
        List objects in an S3 bucket.
        
        Args:
            bucket_name: S3 bucket name
            prefix: Object key prefix filter
            max_keys: Maximum number of keys to return
            
        Returns:
            List of object dictionaries
        """
        try:
            response = self.client.list_objects_v2(
                Bucket=bucket_name,
                Prefix=prefix,
                MaxKeys=max_keys
            )
            return response.get('Contents', [])
        except Exception as e:
            self.logger.error(f"Failed to list objects: {str(e)}")
            return []
