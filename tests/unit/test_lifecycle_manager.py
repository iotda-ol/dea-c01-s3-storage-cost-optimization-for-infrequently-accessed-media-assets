"""
Unit tests for LifecycleManager module.
"""

import unittest
from unittest.mock import Mock, MagicMock
from src.core.lifecycle_manager import LifecycleManager


class TestLifecycleManager(unittest.TestCase):
    """Test cases for LifecycleManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.lifecycle_mgr = LifecycleManager(self.mock_client)
    
    def test_create_media_lifecycle_policy(self):
        """Test creating a media lifecycle policy."""
        config = self.lifecycle_mgr.create_media_lifecycle_policy(
            bucket_name="test-bucket",
            standard_ia_days=30,
            glacier_days=90
        )
        
        self.assertIn('Rules', config)
        self.assertEqual(len(config['Rules']), 1)
        
        rule = config['Rules'][0]
        self.assertEqual(rule['Status'], 'Enabled')
        self.assertEqual(len(rule['Transitions']), 2)
        self.assertEqual(rule['Transitions'][0]['Days'], 30)
        self.assertEqual(rule['Transitions'][0]['StorageClass'], 'STANDARD_IA')
        self.assertEqual(rule['Transitions'][1]['Days'], 90)
        self.assertEqual(rule['Transitions'][1]['StorageClass'], 'GLACIER')
    
    def test_create_lifecycle_policy_with_expiration(self):
        """Test creating a lifecycle policy with expiration."""
        config = self.lifecycle_mgr.create_media_lifecycle_policy(
            bucket_name="test-bucket",
            standard_ia_days=30,
            glacier_days=90,
            expiration_days=365
        )
        
        rule = config['Rules'][0]
        self.assertIn('Expiration', rule)
        self.assertEqual(rule['Expiration']['Days'], 365)
    
    def test_create_lifecycle_policy_with_tags(self):
        """Test creating a lifecycle policy with tag filters."""
        tags = {'Environment': 'Production', 'Type': 'Media'}
        config = self.lifecycle_mgr.create_media_lifecycle_policy(
            bucket_name="test-bucket",
            standard_ia_days=30,
            glacier_days=90,
            tags=tags
        )
        
        rule = config['Rules'][0]
        self.assertIn('Filter', rule)
        self.assertIn('And', rule['Filter'])
        self.assertEqual(len(rule['Filter']['And']['Tags']), 2)


if __name__ == '__main__':
    unittest.main()
