import pytest
from unittest.mock import Mock, patch, MagicMock
from minio.error import S3Error
import io

from s3_api import S3API


class TestS3API:

    def test_init(self, mock_config):
        """Test S3API initialization"""
        with patch('s3_api.Minio') as mock_minio:
            api = S3API()
            mock_minio.assert_called_once()
            assert api.region is not None

    @pytest.mark.asyncio
    async def test_list_files_success(self, s3_api_with_mock):
        """Test successful file listing"""
        # Mock bucket exists
        s3_api_with_mock.client.bucket_exists.return_value = True

        # Mock list_objects
        mock_obj = Mock()
        mock_obj.object_name = "test.txt"
        mock_obj.size = 1024
        mock_obj.last_modified = Mock()
        mock_obj.last_modified.isoformat.return_value = "2023-01-01T00:00:00"

        s3_api_with_mock.client.list_objects.return_value = [mock_obj]

        result = await s3_api_with_mock.list_files("test-bucket")

        assert "bucket" in result
        assert "files" in result
        assert result["bucket"] == "test-bucket"
        assert len(result["files"]) == 1
        assert result["files"][0]["name"] == "test.txt"
        assert result["files"][0]["size"] == 1024

    @pytest.mark.asyncio
    async def test_list_files_bucket_not_exists(self, s3_api_with_mock):
        """Test listing files when bucket doesn't exist"""
        s3_api_with_mock.client.bucket_exists.return_value = False

        result = await s3_api_with_mock.list_files("nonexistent-bucket")

        assert "error" in result
        assert "does not exist" in result["error"]

    @pytest.mark.asyncio
    async def test_list_files_s3_error(self, s3_api_with_mock):
        """Test listing files with S3 error"""
        s3_api_with_mock.client.bucket_exists.side_effect = S3Error("Test error", "", "", "", "", "")

        result = await s3_api_with_mock.list_files("test-bucket")

        assert "error" in result
        assert "Error listing files" in result["error"]

    @pytest.mark.asyncio
    async def test_upload_file_success(self, s3_api_with_mock, mock_upload_file):
        """Test successful file upload"""
        s3_api_with_mock.client.put_object.return_value = None

        result = await s3_api_with_mock.upload_file("test-bucket", mock_upload_file)

        assert "message" in result
        assert "uploaded successfully" in result["message"]
        s3_api_with_mock.client.put_object.assert_called_once()

    @pytest.mark.asyncio
    async def test_upload_file_s3_error(self, s3_api_with_mock, mock_upload_file):
        """Test file upload with S3 error"""
        s3_api_with_mock.client.put_object.side_effect = S3Error("Upload error", "", "", "", "", "")

        result = await s3_api_with_mock.upload_file("test-bucket", mock_upload_file)

        assert "error" in result
        assert "Error uploading file" in result["error"]

    @pytest.mark.asyncio
    async def test_download_file_success(self, s3_api_with_mock):
        """Test successful file download"""
        mock_data = Mock()
        mock_data.read.return_value = b"file content"
        s3_api_with_mock.client.get_object.return_value = mock_data

        result = await s3_api_with_mock.download_file("test-bucket", "test.txt")

        assert result == b"file content"

    @pytest.mark.asyncio
    async def test_download_file_s3_error(self, s3_api_with_mock):
        """Test file download with S3 error"""
        s3_api_with_mock.client.get_object.side_effect = S3Error("Download error", "", "", "", "", "")

        result = await s3_api_with_mock.download_file("test-bucket", "test.txt")

        assert isinstance(result, dict)
        assert "error" in result
        assert "Error downloading file" in result["error"]

    @pytest.mark.asyncio
    async def test_delete_file_success(self, s3_api_with_mock):
        """Test successful file deletion"""
        s3_api_with_mock.client.remove_object.return_value = None

        result = await s3_api_with_mock.delete_file("test-bucket", "test.txt")

        assert "message" in result
        assert "deleted successfully" in result["message"]

    @pytest.mark.asyncio
    async def test_delete_file_s3_error(self, s3_api_with_mock):
        """Test file deletion with S3 error"""
        s3_api_with_mock.client.remove_object.side_effect = S3Error("Delete error", "", "", "", "", "")

        result = await s3_api_with_mock.delete_file("test-bucket", "test.txt")

        assert "error" in result
        assert "Error deleting file" in result["error"]

    @pytest.mark.asyncio
    async def test_create_bucket_success(self, s3_api_with_mock):
        """Test successful bucket creation"""
        s3_api_with_mock.client.bucket_exists.return_value = False
        s3_api_with_mock.client.make_bucket.return_value = None

        result = await s3_api_with_mock.create_bucket("new-bucket")

        assert "message" in result
        assert "created successfully" in result["message"]

    @pytest.mark.asyncio
    async def test_create_bucket_already_exists(self, s3_api_with_mock):
        """Test creating bucket that already exists"""
        s3_api_with_mock.client.bucket_exists.return_value = True

        result = await s3_api_with_mock.create_bucket("existing-bucket")

        assert "message" in result
        assert "already exists" in result["message"]

    @pytest.mark.asyncio
    async def test_create_bucket_s3_error(self, s3_api_with_mock):
        """Test bucket creation with S3 error"""
        s3_api_with_mock.client.bucket_exists.side_effect = S3Error("Bucket error", "", "", "", "", "")

        result = await s3_api_with_mock.create_bucket("test-bucket")

        assert "error" in result
        assert "Error creating bucket" in result["error"]