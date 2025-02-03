# config.py
import os
from typing import Any, Dict

from dotenv import load_dotenv


def load_minio_config() -> Dict[str, str]:
    return {
        "OBJECT_STORAGE_ENDPOINT": os.getenv(
            "OBJECT_STORAGE_ENDPOINT", "127.0.0.1:9000"
        ).replace("http://", ""),
        "OBJECT_STORAGE_ACCESS_KEY": os.getenv(
            "OBJECT_STORAGE_ACCESS_KEY", "minioadmin"
        ),
        "OBJECT_STORAGE_SECRET_KEY": os.getenv(
            "OBJECT_STORAGE_SECRET_KEY", "minioadmin"
        ),
        "MINIO_ROOT_USER": os.getenv("OBJECT_STORAGE_ACCESS_KEY", "minioadmin"),
        "MINIO_ROOT_PASSWORD": os.getenv("OBJECT_STORAGE_SECRET_KEY", "minioadmin"),
    }


def load_aws_config() -> Dict[str, str]:
    # Placeholder for AWS configuration
    raise NotImplementedError("AWS configuration not yet implemented")
    # return {
    #     "OBJECT_STORAGE_ENDPOINT": os.getenv("OBJECT_STORAGE_ENDPOINT", "s3.amazonaws.com"),
    #     "OBJECT_STORAGE_ACCESS_KEY": os.getenv("OBJECT_STORAGE_ACCESS_KEY"),
    #     "OBJECT_STORAGE_SECRET_KEY": os.getenv("OBJECT_STORAGE_SECRET_KEY"),
    #     "OBJECT_STORAGE_REGION": os.getenv("OBJECT_STORAGE_REGION", "us-east-1")
    # }


def load_config() -> Dict[str, Any]:
    if os.path.exists(
        ".env"
    ):  # this makes it so .env files override whatever other env vars have been loaded in
        load_dotenv(".env", override=True)

    # Get storage service from environment variable
    storage_service = os.getenv("OBJECT_STORAGE_SERVICE", "minio").lower()

    # Load the appropriate configuration
    if storage_service == "minio":
        config_dict = load_minio_config()
    elif storage_service == "aws":
        config_dict = load_aws_config()
    else:
        raise ValueError(f"Unsupported storage service: {storage_service}")

    # Add the storage service type to the config
    config_dict["OBJECT_STORAGE_SERVICE"] = storage_service

    return config_dict


config = load_config()
