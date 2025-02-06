# Object Storage REST API service

standalone FastAPI service for object storage


## 1. set up and run the MinIO object storage service

create `.env.minio` file from template, then manually update environment variables
```bash
cp .env.minio.example .env.minio
```

start [MinIO](https://github.com/minio/minio) object storage Docker container:
```bash
DATA_DIRECTORY=<local data directory path>

docker run -p 9000:9000 -p 9001:9001 -v $DATA_DIRECTORY:/data --env-file .env.minio quay.io/minio/minio server /data --console-address ":9001"
```


## 2a. preferred method: run service in a Docker container

create `.env.docker` file from template; update environment variable values if needed
```bash
cp .env.docker.example .env.docker
```

build the Docker image
```bash
docker build -t object-storage-api .
```

run the Docker container service
```bash
docker compose up
```


## 2b. alternative method: set up and run the service locally

create `.env` file from template; update environment variable values if needed
```bash
cp .env.example .env
```

set up a dedicated virtual environment to run the service
```bash
# (install uv)
# curl -LsSf https://astral.sh/uv/install.sh | sh
# https://docs.astral.sh/uv/getting-started/installation/

uv python install 3.11

uv sync
```

install `pre-commit` git hook scripts
```bash
uv run pre-commit install
```

start the service
```bash
# development
uv run fastapi dev --host 127.0.0.1 --port 59090 service.py

# production
uv run uvicorn service:app --host 127.0.0.1 --port 59090
```


## 3. test the service

manually request classification for an image
```bash
# e.g. local
IMAGE_PATH="data/{bucket_name}/{image_filename}"
# e.g. docker
IMAGE_PATH="local/{image_filename}"

# curl command once IMAGE_PATH has been set
curl -X GET "http://127.0.0.1:59090/process/${IMAGE_PATH}" -H "accept: application/json"
```

service documentation:
http://127.0.0.1:59090/docs

NOTE: The service is designed to run locally and currently doesn't incorporate authentication or other security features.
