from minio_api import MinioAPI


def get_storage_api(storage_service):
    if storage_service == "minio":
        return MinioAPI()
    elif storage_service == "aws":
        raise NotImplementedError("AWS S3 storage is not yet implemented")
    else:
        raise ValueError(f"Unsupported storage type: {storage_service}")
