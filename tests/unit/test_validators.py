"""
Unit tests for validators module.
"""

import unittest
from src.utils.validators import (
    validate_bucket_name,
    validate_lifecycle_config,
    validate_days_config,
    validate_storage_class
)


class TestValidators(unittest.TestCase):
    """Test cases for validator functions."""
    
    def test_validate_bucket_name_valid(self):
        """Test valid bucket names."""
        valid_names = [
            'my-bucket',
            'my.bucket',
            'mybucket123',
            'my-bucket-123'
        ]
        
        for name in valid_names:
            with self.subTest(name=name):
                self.assertTrue(validate_bucket_name(name))
    
    def test_validate_bucket_name_invalid(self):
        """Test invalid bucket names."""
        invalid_names = [
            'My-Bucket',  # uppercase
            'ab',  # too short
            'my..bucket',  # consecutive periods
            'xn--bucket',  # starts with xn--
            '192.168.1.1',  # IP address format
            'my_bucket',  # underscore not allowed
        ]
        
        for name in invalid_names:
            with self.subTest(name=name):
                self.assertFalse(validate_bucket_name(name))
    
    def test_validate_lifecycle_config_valid(self):
        """Test valid lifecycle configuration."""
        config = {
            'Rules': [
                {
                    'ID': 'rule1',
                    'Status': 'Enabled',
                    'Transitions': [
                        {'Days': 30, 'StorageClass': 'STANDARD_IA'}
                    ]
                }
            ]
        }
        
        is_valid, error = validate_lifecycle_config(config)
        self.assertTrue(is_valid)
        self.assertIsNone(error)
    
    def test_validate_lifecycle_config_invalid(self):
        """Test invalid lifecycle configuration."""
        # Missing Rules key
        config = {'Invalid': 'config'}
        is_valid, error = validate_lifecycle_config(config)
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)
        
        # Empty rules
        config = {'Rules': []}
        is_valid, error = validate_lifecycle_config(config)
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)
        
        # Missing Status
        config = {'Rules': [{'ID': 'rule1'}]}
        is_valid, error = validate_lifecycle_config(config)
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)
    
    def test_validate_days_config_valid(self):
        """Test valid days configuration."""
        is_valid, error = validate_days_config(30, 90, 365)
        self.assertTrue(is_valid)
        self.assertIsNone(error)
    
    def test_validate_days_config_invalid(self):
        """Test invalid days configuration."""
        # Standard-IA less than 30 days
        is_valid, error = validate_days_config(20, 90)
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)
        
        # Glacier before Standard-IA
        is_valid, error = validate_days_config(30, 20)
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)
        
        # Expiration before Glacier
        is_valid, error = validate_days_config(30, 90, 60)
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)
    
    def test_validate_storage_class(self):
        """Test storage class validation."""
        valid_classes = ['STANDARD', 'STANDARD_IA', 'GLACIER', 'DEEP_ARCHIVE']
        for storage_class in valid_classes:
            with self.subTest(storage_class=storage_class):
                self.assertTrue(validate_storage_class(storage_class))
        
        self.assertFalse(validate_storage_class('INVALID_CLASS'))


if __name__ == '__main__':
    unittest.main()
