"""
Test configuration and fixtures.
"""

import pytest
from unittest.mock import Mock


@pytest.fixture
def mock_s3_client():
    """Create a mock S3 client for testing."""
    client = Mock()
    client.client = Mock()
    return client


@pytest.fixture
def sample_bucket_name():
    """Provide a sample bucket name for tests."""
    return "test-media-bucket"


@pytest.fixture
def sample_lifecycle_config():
    """Provide a sample lifecycle configuration."""
    return {
        'Rules': [
            {
                'ID': 'test-rule',
                'Status': 'Enabled',
                'Prefix': 'media/',
                'Transitions': [
                    {
                        'Days': 30,
                        'StorageClass': 'STANDARD_IA'
                    },
                    {
                        'Days': 90,
                        'StorageClass': 'GLACIER'
                    }
                ]
            }
        ]
    }
