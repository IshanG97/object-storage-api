import pytest
from unittest.mock import patch

from storage_factory import get_storage_api
from s3_api import S3API


class TestStorageFactory:

    def test_get_storage_api_minio(self):
        """Test getting storage API for minio service"""
        with patch('storage_factory.S3API') as mock_s3_api:
            get_storage_api('minio')
            mock_s3_api.assert_called_once()

    def test_get_storage_api_nebius(self):
        """Test getting storage API for nebius service"""
        with patch('storage_factory.S3API') as mock_s3_api:
            get_storage_api('nebius')
            mock_s3_api.assert_called_once()

    def test_get_storage_api_invalid_service(self):
        """Test getting storage API for invalid service"""
        with pytest.raises(ValueError) as exc_info:
            get_storage_api('invalid_service')
        assert "Unsupported storage type" in str(exc_info.value)

    def test_get_storage_api_none_service(self):
        """Test getting storage API with None service"""
        with pytest.raises(ValueError) as exc_info:
            get_storage_api(None)
        assert "Unsupported storage type" in str(exc_info.value)

    def test_get_storage_api_empty_string(self):
        """Test getting storage API with empty string service"""
        with pytest.raises(ValueError) as exc_info:
            get_storage_api('')
        assert "Unsupported storage type" in str(exc_info.value)