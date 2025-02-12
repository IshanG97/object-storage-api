# storage_base.py
from abc import ABC, abstractmethod

from fastapi import UploadFile

from config import config


class StorageAPI(ABC):
    def __init__(self):
        self.endpoint = config.OBJECT_STORAGE_ENDPOINT
        self.access_key = config.OBJECT_STORAGE_ACCESS_KEY
        self.secret_key = config.OBJECT_STORAGE_SECRET_KEY
        self.secure = config.OBJECT_STORAGE_SECURE

    @abstractmethod
    async def list_files(self, bucket_name: str):
        pass

    @abstractmethod
    async def upload_file(self, bucket_name: str, file: UploadFile):
        pass

    @abstractmethod
    async def download_file(self, bucket_name: str, filename: str):
        pass

    @abstractmethod
    async def delete_file(self, bucket_name: str, filename: str):
        pass

    @abstractmethod
    async def create_bucket(self, bucket_name: str):
        pass
