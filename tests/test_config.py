import pytest
import os
from unittest.mock import patch

from config import StorageConfig


class TestConfig:

    def test_config_loads_environment_variables(self):
        """Test that config loads environment variables correctly"""
        with patch.dict(os.environ, {
            'OBJECT_STORAGE_SERVICE': 'minio',
            'OBJECT_STORAGE_ENDPOINT': 'localhost:9000',
            'OBJECT_STORAGE_ACCESS_KEY': 'test_access',
            'OBJECT_STORAGE_SECRET_KEY': 'test_secret',
            'OBJECT_STORAGE_SECURE': 'false',
            'OBJECT_STORAGE_REGION': 'us-east-1'
        }):
            config = StorageConfig()
            assert config.OBJECT_STORAGE_SERVICE == 'minio'
            assert config.OBJECT_STORAGE_ENDPOINT == 'localhost:9000'
            assert config.OBJECT_STORAGE_ACCESS_KEY == 'test_access'
            assert config.OBJECT_STORAGE_SECRET_KEY == 'test_secret'
            assert config.OBJECT_STORAGE_SECURE is False
            assert config.OBJECT_STORAGE_REGION == 'us-east-1'

    def test_config_secure_boolean_conversion(self):
        """Test that SECURE setting is properly converted to boolean"""
        # Test 'true' string
        with patch.dict(os.environ, {'OBJECT_STORAGE_SERVICE': 'minio', 'OBJECT_STORAGE_SECURE': 'true'}):
            config = StorageConfig()
            assert config.OBJECT_STORAGE_SECURE is True

        # Test 'True' string (case insensitive - .lower() is applied)
        with patch.dict(os.environ, {'OBJECT_STORAGE_SERVICE': 'minio', 'OBJECT_STORAGE_SECURE': 'True'}):
            config = StorageConfig()
            assert config.OBJECT_STORAGE_SECURE is True  # .lower() makes this 'true'

        # Test 'false' string
        with patch.dict(os.environ, {'OBJECT_STORAGE_SERVICE': 'minio', 'OBJECT_STORAGE_SECURE': 'false'}):
            config = StorageConfig()
            assert config.OBJECT_STORAGE_SECURE is False

        # Test '1' string
        with patch.dict(os.environ, {'OBJECT_STORAGE_SERVICE': 'minio', 'OBJECT_STORAGE_SECURE': '1'}):
            config = StorageConfig()
            assert config.OBJECT_STORAGE_SECURE is False  # Only 'true' should be True

        # Test '0' string
        with patch.dict(os.environ, {'OBJECT_STORAGE_SERVICE': 'minio', 'OBJECT_STORAGE_SECURE': '0'}):
            config = StorageConfig()
            assert config.OBJECT_STORAGE_SECURE is False

    def test_config_default_values(self):
        """Test config default values when environment variables are not set"""
        # Clear relevant environment variables
        env_vars_to_clear = [
            'OBJECT_STORAGE_SERVICE',
            'OBJECT_STORAGE_ENDPOINT',
            'OBJECT_STORAGE_ACCESS_KEY',
            'OBJECT_STORAGE_SECRET_KEY',
            'OBJECT_STORAGE_SECURE',
            'OBJECT_STORAGE_REGION'
        ]

        with patch.dict(os.environ, {}, clear=False):
            # Remove the variables we want to test defaults for
            for var in env_vars_to_clear:
                if var in os.environ:
                    del os.environ[var]

            config = StorageConfig()

            # Test that attributes exist with defaults for minio service
            assert hasattr(config, 'OBJECT_STORAGE_SERVICE')
            assert hasattr(config, 'OBJECT_STORAGE_ENDPOINT')
            assert hasattr(config, 'OBJECT_STORAGE_ACCESS_KEY')
            assert hasattr(config, 'OBJECT_STORAGE_SECRET_KEY')
            assert hasattr(config, 'OBJECT_STORAGE_SECURE')
            assert hasattr(config, 'OBJECT_STORAGE_REGION')
            # Check minio defaults
            assert config.OBJECT_STORAGE_SERVICE == 'minio'
            assert config.OBJECT_STORAGE_ENDPOINT == '127.0.0.1:9000'
            assert config.OBJECT_STORAGE_ACCESS_KEY == 'minioadmin'
            assert config.OBJECT_STORAGE_SECRET_KEY == 'minioadmin'
            assert config.OBJECT_STORAGE_SECURE is False
            assert config.OBJECT_STORAGE_REGION == 'yo-momma'