from s3_api import S3API


def get_storage_api(storage_service="minio"):
    if storage_service in ["minio", "nebius"]:
        return S3API()
    else:
        raise ValueError(f"Unsupported storage type: {storage_service}")
