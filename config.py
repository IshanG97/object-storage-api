# config.py
import os

from dotenv import load_dotenv


class StorageConfig:  # docker practically skips all the logic below since it loads the env vars from the .env.docker file at the beginning
    def __init__(self):
        if os.path.exists(".env"):
            load_dotenv(".env", override=True)

        self.OBJECT_STORAGE_SERVICE = os.getenv(
            "OBJECT_STORAGE_SERVICE", "minio"
        ).lower()

        if self.OBJECT_STORAGE_SERVICE == "minio":
            self._load_minio_config()
        elif self.OBJECT_STORAGE_SERVICE == "nebius":
            self._load_nebius_config()
        elif self.OBJECT_STORAGE_SERVICE == "aws":
            self._load_aws_config()
        else:
            raise ValueError(
                f"Unsupported storage service: {self.OBJECT_STORAGE_SERVICE}"
            )

    def _load_minio_config(self):
        if os.path.exists(".env.minio"):
            load_dotenv(".env.minio", override=True)
        self.OBJECT_STORAGE_ENDPOINT = os.getenv(
            "OBJECT_STORAGE_ENDPOINT", "127.0.0.1:9000"
        ).replace("http://", "")
        self.OBJECT_STORAGE_ACCESS_KEY = os.getenv(
            "OBJECT_STORAGE_ACCESS_KEY", "minioadmin"
        )
        self.OBJECT_STORAGE_SECRET_KEY = os.getenv(
            "OBJECT_STORAGE_SECRET_KEY", "minioadmin"
        )
        self.OBJECT_STORAGE_REGION = os.getenv("OBJECT_STORAGE_REGION", "yo-momma")
        self.OBJECT_STORAGE_SECURE = (
            os.getenv("OBJECT_STORAGE_SECURE", "false").lower() == "true"
        )
        self.MINIO_ROOT_USER = (
            self.OBJECT_STORAGE_ACCESS_KEY
        )  # Minio uses this to set the root user
        self.MINIO_ROOT_PASSWORD = (
            self.OBJECT_STORAGE_SECRET_KEY
        )  # Minio uses this to set the root password

    def _load_nebius_config(self):
        if os.path.exists(".env.nebius"):
            load_dotenv(".env.nebius", override=True)
        endpoint = os.getenv("OBJECT_STORAGE_ENDPOINT", "storage.eu-west1.nebius.cloud")
        self.OBJECT_STORAGE_ENDPOINT = (
            endpoint.replace("https://", "").replace("http://", "").replace(":443", "")
        )
        self.OBJECT_STORAGE_ACCESS_KEY = os.getenv("OBJECT_STORAGE_ACCESS_KEY")
        self.OBJECT_STORAGE_SECRET_KEY = os.getenv("OBJECT_STORAGE_SECRET_KEY")
        self.OBJECT_STORAGE_REGION = os.getenv("OBJECT_STORAGE_REGION", "eu-west1")
        self.OBJECT_STORAGE_SECURE = (
            os.getenv("OBJECT_STORAGE_SECURE", "false").lower() == "true"
        )

    def _load_aws_config(self):
        if os.path.exists(".env.aws"):
            load_dotenv(".env.aws", override=True)
        endpoint = os.getenv("OBJECT_STORAGE_ENDPOINT", "s3.amazonaws.com")
        self.OBJECT_STORAGE_ENDPOINT = (
            endpoint.replace("https://", "").replace("http://", "").replace(":443", "")
        )
        self.OBJECT_STORAGE_ACCESS_KEY = os.getenv("OBJECT_STORAGE_ACCESS_KEY")
        self.OBJECT_STORAGE_SECRET_KEY = os.getenv("OBJECT_STORAGE_SECRET_KEY")
        self.OBJECT_STORAGE_REGION = os.getenv("OBJECT_STORAGE_REGION", "us-east-1")
        self.OBJECT_STORAGE_SECURE = (
            os.getenv("OBJECT_STORAGE_SECURE", "true").lower() == "true"
        )


config = StorageConfig()
