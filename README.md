# Object Storage REST API service

standalone FastAPI service for object storage

## set up and run the service

for minio:
start minio docker container: 

```bash
docker run -p 9000:9000 -p 9001:9001 -e-v <local_data_folder>:/data  quay.io/minio/minio server /data --console-address ":9001"
```

## 1. setup environment variables

for `.env` files with `.example` at then, remove the `.example` from the filename
- e.g. `.env.docker.example` ---> `.env.docker`

## 2a. preferred method: run in a Docker container

uses variables stored in `.env.docker`

build the Docker image
```bash
docker build -t object-storage-api .
```

run the Docker container service
```bash
docker compose up
```

## 2b. alternative method: set up and run the service locally

uses variables stored in `.env` 

set up a dedicated virtual environment to run the service
```bash
# (install uv)
# curl -LsSf https://astral.sh/uv/install.sh | sh
# https://docs.astral.sh/uv/getting-started/installation/

uv python install 3.11

uv sync
```

start the service
```bash
# development
uv run fastapi dev --host 127.0.0.1 --port 9090 service.py

# production
uv run uvicorn service:app --host 127.0.0.1 --port 9090
# OR
uv run fastapi run --host 127.0.0.1 --port 9090 service.py
```

## 3. test the service

manually request classification for an image
```bash
# e.g. local
IMAGE_PATH="data/{bucket_name}/{image_filename}"
# e.g. docker
IMAGE_PATH="local/{image_filename}"

# curl command once IMAGE_PATH has been set
curl -X GET "http://127.0.0.1:9090/process/${IMAGE_PATH}" -H "accept: application/json"

```

service documentation:
http://127.0.0.1:9090/docs

NOTE: The service is designed to run locally and currently doesn't incorporate authentication or other security features.
