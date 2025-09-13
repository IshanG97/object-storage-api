# Object Storage REST API Service

FastAPI service for S3-compatible object storage with support for multiple backends and deployment methods.

## Setup

This service uses a **two-tier environment configuration system**:
1. **Main config (`.env`)** - sets `OBJECT_STORAGE_SERVICE` to choose backend (`minio`, `aws`, or `nebius`)
2. **Backend-specific config** - credentials and endpoint configuration for the chosen backend

### Step 1: setup your backend
```bash
cp env_examples/.env.example .env
# Edit OBJECT_STORAGE_SERVICE to: minio, aws, or nebius
```

### Step 2: configure your chosen backend

**MinIO (local/self-hosted)** - best for local dev and testing
```bash
# For local development
cp env_examples/.env.minio.local.example .env.minio

# For Docker deployment
cp env_examples/.env.minio.docker.example .env.minio
```
***Launch MinIO service***
```bash
DATA_DIRECTORY=<local data directory path>
docker run -p 9000:9000 -p 9001:9001 \
  -v $DATA_DIRECTORY:/data \
  --env-file .env.minio \
  quay.io/minio/minio server /data --console-address ":9001"
```

**AWS S3** - For production deployments
```bash
cp env_examples/.env.aws.example .env.aws
# Edit with your AWS credentials and region
```

**Nebius Cloud Storage** - For production deployments
```bash
cp env_examples/.env.nebius.example .env.nebius
# Edit with your Nebius credentials and region
```

## Deployment

After completing the [Setup](#setup) steps above

### 1. Docker (recommended)

```bash
docker build -t object-storage-api .
docker compose up
```

### 2. Local

**Set up Python environment:**
```bash
# Install uv if not already installed
# curl -LsSf https://astral.sh/uv/install.sh | sh

uv python install 3.11
uv sync
uv run pre-commit install
```

**Start the service:**
```bash
# Development mode with auto-reload
fastapi dev --host 127.0.0.1 --port 59090 service.py

# Production mode
uvicorn service:app --host 127.0.0.1 --port 59090
```

## Testing the Service

**Available API endpoints:**

```bash
# Health check
curl -X GET "http://127.0.0.1:59090/health"

# Create bucket
curl -X POST "http://127.0.0.1:59090/create/my-bucket"

# Upload file
curl -X POST "http://127.0.0.1:59090/upload/my-bucket" \
     -F "file=@/path/to/your/file.jpg"

# List files in bucket
curl -X GET "http://127.0.0.1:59090/list/my-bucket"

# Download file
curl -X GET "http://127.0.0.1:59090/download/my-bucket/file.jpg" \
     --output downloaded-file.jpg

# Delete file
curl -X DELETE "http://127.0.0.1:59090/delete/my-bucket/file.jpg"
```

## Security Notes

- The service currently doesn't incorporate authentication or other security features
- Ensure proper firewall and network security when deploying to production
- Store credentials securely and never commit them to version control
