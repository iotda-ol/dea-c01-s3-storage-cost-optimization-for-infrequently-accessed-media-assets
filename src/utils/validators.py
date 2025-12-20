"""
Validators Utility Module

Provides reusable validation functions for S3 operations.
"""

import re
from typing import Dict, List, Optional, Tuple


def validate_bucket_name(bucket_name: str) -> bool:
    """
    Validate S3 bucket name according to AWS rules.
    
    Args:
        bucket_name: S3 bucket name to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    # Bucket name rules:
    # - Between 3 and 63 characters
    # - Only lowercase letters, numbers, dots, and hyphens
    # - Must begin and end with letter or number
    # - Must not be formatted as IP address
    # - Must not start with 'xn--'
    # - Must not end with '-s3alias'
    
    if not bucket_name or len(bucket_name) < 3 or len(bucket_name) > 63:
        return False
    
    if not re.match(r'^[a-z0-9][a-z0-9.-]*[a-z0-9]$', bucket_name):
        return False
    
    if bucket_name.startswith('xn--') or bucket_name.endswith('-s3alias'):
        return False
    
    # Check if formatted as IP address
    if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', bucket_name):
        return False
    
    # Check for consecutive periods
    if '..' in bucket_name:
        return False
    
    return True


def validate_lifecycle_config(lifecycle_config: Dict) -> Tuple[bool, Optional[str]]:
    """
    Validate S3 lifecycle configuration.
    
    Args:
        lifecycle_config: Lifecycle configuration dictionary
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not isinstance(lifecycle_config, dict):
        return False, "Lifecycle config must be a dictionary"
    
    if 'Rules' not in lifecycle_config:
        return False, "Lifecycle config must contain 'Rules' key"
    
    rules = lifecycle_config['Rules']
    if not isinstance(rules, list):
        return False, "'Rules' must be a list"
    
    if not rules:
        return False, "At least one rule is required"
    
    for i, rule in enumerate(rules):
        if 'Status' not in rule:
            return False, f"Rule {i}: 'Status' is required"
        
        if rule['Status'] not in ['Enabled', 'Disabled']:
            return False, f"Rule {i}: Status must be 'Enabled' or 'Disabled'"
        
        if 'ID' not in rule:
            return False, f"Rule {i}: 'ID' is required"
        
        # Must have at least one action
        has_action = any(key in rule for key in [
            'Transitions', 'Expiration', 'NoncurrentVersionTransitions',
            'NoncurrentVersionExpiration', 'AbortIncompleteMultipartUpload'
        ])
        
        if not has_action:
            return False, f"Rule {i}: At least one action is required"
    
    return True, None


def validate_days_config(
    standard_ia_days: int,
    glacier_days: int,
    expiration_days: Optional[int] = None
) -> Tuple[bool, Optional[str]]:
    """
    Validate lifecycle transition days configuration.
    
    Args:
        standard_ia_days: Days before transition to Standard-IA
        glacier_days: Days before transition to Glacier
        expiration_days: Days before expiration
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if standard_ia_days < 30:
        return False, "Standard-IA transition must be at least 30 days"
    
    if glacier_days <= standard_ia_days:
        return False, "Glacier transition must be after Standard-IA transition"
    
    if expiration_days and expiration_days <= glacier_days:
        return False, "Expiration must be after Glacier transition"
    
    return True, None


def validate_storage_class(storage_class: str) -> bool:
    """
    Validate S3 storage class name.
    
    Args:
        storage_class: Storage class name
        
    Returns:
        bool: True if valid, False otherwise
    """
    valid_classes = [
        'STANDARD',
        'REDUCED_REDUNDANCY',
        'STANDARD_IA',
        'ONEZONE_IA',
        'INTELLIGENT_TIERING',
        'GLACIER',
        'DEEP_ARCHIVE',
        'GLACIER_IR'
    ]
    
    return storage_class in valid_classes
