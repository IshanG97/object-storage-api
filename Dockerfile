FROM python:3.11-slim-bookworm

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1

# Install uv in a single layer
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    curl -LsSf https://astral.sh/uv/0.5.21/install.sh | sh && \
    rm -rf /var/lib/apt/lists/* && \
    rm -f /uv-installer.sh

ENV PATH="/root/.local/bin/:$PATH"

# copy environment files
COPY .python-version pyproject.toml uv.lock /app/

RUN uv sync

# copy app files
COPY config.py s3_api.py service.py storage_base.py storage_factory.py /app/

ENTRYPOINT ["uv", "run", "uvicorn", "service:app", "--host", "0.0.0.0", "--port", "59090"]
