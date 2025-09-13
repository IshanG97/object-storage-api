import os
import pytest
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from minio import Minio

from config import config
from service import app
from s3_api import S3API


@pytest.fixture
def mock_config():
    """Mock configuration for testing"""
    with patch.dict(os.environ, {
        'OBJECT_STORAGE_SERVICE': 'minio',
        'OBJECT_STORAGE_ENDPOINT': 'localhost:9000',
        'OBJECT_STORAGE_ACCESS_KEY': 'test_access_key',
        'OBJECT_STORAGE_SECRET_KEY': 'test_secret_key',
        'OBJECT_STORAGE_SECURE': 'false',
        'OBJECT_STORAGE_REGION': 'us-east-1'
    }):
        yield


@pytest.fixture
def mock_minio_client():
    """Mock Minio client for testing"""
    return Mock(spec=Minio)


@pytest.fixture
def s3_api_with_mock(mock_config, mock_minio_client):
    """S3API instance with mocked Minio client"""
    with patch('s3_api.Minio', return_value=mock_minio_client):
        api = S3API()
        api.client = mock_minio_client
        return api


@pytest.fixture
def test_client():
    """FastAPI test client"""
    return TestClient(app)


@pytest.fixture
def sample_file_content():
    """Sample file content for testing uploads"""
    return b"This is test file content"


@pytest.fixture
def mock_upload_file():
    """Mock UploadFile for testing"""
    mock_file = Mock()
    mock_file.filename = "test.txt"
    mock_file.content_type = "text/plain"

    async def async_read():
        return b"test content"

    mock_file.read = async_read
    return mock_file