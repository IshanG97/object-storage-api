import pytest
from unittest.mock import Mock, patch, AsyncMock
from fastapi.testclient import TestClient
import io

from service import app


class TestService:

    def test_health_check(self, test_client):
        """Test health check endpoint"""
        response = test_client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "storage_service" in data
        assert "endpoint" in data
        assert data["status"] == "healthy"

    @patch('service.storage_api')
    def test_create_bucket_success(self, mock_storage_api, test_client):
        """Test successful bucket creation"""
        mock_storage_api.create_bucket = AsyncMock(return_value={"message": "Bucket created successfully"})

        response = test_client.post("/bucket/create/test-bucket")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "created successfully" in data["message"]

    @patch('service.storage_api')
    def test_create_bucket_error(self, mock_storage_api, test_client):
        """Test bucket creation with error"""
        mock_storage_api.create_bucket = AsyncMock(return_value={"error": "Bucket creation failed"})

        response = test_client.post("/bucket/create/test-bucket")
        assert response.status_code == 400
        assert "Bucket creation failed" in response.json()["detail"]

    @patch('service.storage_api')
    def test_upload_file_success(self, mock_storage_api, test_client):
        """Test successful file upload"""
        mock_storage_api.upload_file = AsyncMock(return_value={"message": "File uploaded successfully"})

        # Create test file
        test_file = ("test.txt", b"test content", "text/plain")

        response = test_client.post(
            "/bucket/test-bucket/upload",
            files={"file": test_file}
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "uploaded successfully" in data["message"]

    @patch('service.storage_api')
    def test_upload_file_error(self, mock_storage_api, test_client):
        """Test file upload with error"""
        mock_storage_api.upload_file = AsyncMock(return_value={"error": "Upload failed"})

        test_file = ("test.txt", b"test content", "text/plain")

        response = test_client.post(
            "/bucket/test-bucket/upload",
            files={"file": test_file}
        )
        assert response.status_code == 400
        assert "Upload failed" in response.json()["detail"]

    @patch('service.storage_api')
    def test_list_files_success(self, mock_storage_api, test_client):
        """Test successful file listing"""
        mock_storage_api.list_files = AsyncMock(return_value={
            "bucket": "test-bucket",
            "files": [{"name": "test.txt", "size": 1024, "last_modified": "2023-01-01T00:00:00"}]
        })

        response = test_client.get("/bucket/test-bucket/files")
        assert response.status_code == 200
        data = response.json()
        assert "bucket" in data
        assert "files" in data
        assert len(data["files"]) == 1

    @patch('service.storage_api')
    def test_list_files_error(self, mock_storage_api, test_client):
        """Test file listing with error"""
        mock_storage_api.list_files = AsyncMock(return_value={"error": "Bucket not found"})

        response = test_client.get("/bucket/nonexistent-bucket/files")
        assert response.status_code == 400
        assert "Bucket not found" in response.json()["detail"]

    @patch('service.storage_api')
    def test_download_file_success(self, mock_storage_api, test_client):
        """Test successful file download"""
        mock_storage_api.download_file = AsyncMock(return_value=b"file content")

        response = test_client.get("/bucket/test-bucket/download/test.txt")
        assert response.status_code == 200
        assert response.content == b"file content"

    @patch('service.storage_api')
    def test_download_file_error(self, mock_storage_api, test_client):
        """Test file download with error"""
        mock_storage_api.download_file = AsyncMock(return_value={"error": "File not found"})

        response = test_client.get("/bucket/test-bucket/download/nonexistent.txt")
        assert response.status_code == 400
        assert "File not found" in response.json()["detail"]

    @patch('service.storage_api')
    def test_delete_file_success(self, mock_storage_api, test_client):
        """Test successful file deletion"""
        mock_storage_api.delete_file = AsyncMock(return_value={"message": "File deleted successfully"})

        response = test_client.delete("/bucket/test-bucket/file/test.txt")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "deleted successfully" in data["message"]

    @patch('service.storage_api')
    def test_delete_file_error(self, mock_storage_api, test_client):
        """Test file deletion with error"""
        mock_storage_api.delete_file = AsyncMock(return_value={"error": "File not found"})

        response = test_client.delete("/bucket/test-bucket/file/nonexistent.txt")
        assert response.status_code == 400
        assert "File not found" in response.json()["detail"]