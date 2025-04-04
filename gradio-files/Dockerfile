FROM python:3.10-slim

WORKDIR /workspace

# Dependências mínimas para compilar websockets
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

COPY . /workspace/

RUN pip install --no-cache-dir -r /workspace/requirements.txt

EXPOSE 7861
CMD ["python", "/workspace/app-gradio.py"]
