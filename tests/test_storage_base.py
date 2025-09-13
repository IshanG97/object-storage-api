import pytest
from abc import ABC
from unittest.mock import patch, Mock

from storage_base import StorageAPI


class TestStorageAPI:

    def test_is_abstract_class(self):
        """Test that StorageAPI is an abstract class"""
        assert issubclass(StorageAPI, ABC)

    def test_cannot_instantiate_directly(self):
        """Test that StorageAPI cannot be instantiated directly"""
        with pytest.raises(TypeError):
            StorageAPI()

    def test_concrete_implementation_can_be_instantiated(self, mock_config):
        """Test that concrete implementations can be instantiated"""

        class ConcreteStorage(StorageAPI):
            async def list_files(self, bucket_name: str):
                return {"files": []}

            async def upload_file(self, bucket_name: str, file):
                return {"message": "uploaded"}

            async def download_file(self, bucket_name: str, filename: str):
                return b"content"

            async def delete_file(self, bucket_name: str, filename: str):
                return {"message": "deleted"}

            async def create_bucket(self, bucket_name: str):
                return {"message": "created"}

        storage = ConcreteStorage()
        assert storage.endpoint is not None
        assert storage.access_key is not None
        assert storage.secret_key is not None
        assert isinstance(storage.secure, bool)

    def test_abstract_methods_exist(self):
        """Test that all required abstract methods are defined"""
        abstract_methods = StorageAPI.__abstractmethods__
        expected_methods = {
            'list_files',
            'upload_file',
            'download_file',
            'delete_file',
            'create_bucket'
        }
        assert abstract_methods == expected_methods