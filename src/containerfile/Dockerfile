FROM python:3.12-slim

WORKDIR /app

RUN pip install --upgrade pip

COPY src/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY src /app

RUN chmod +x /app/containerfile/api-entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["bash", "/app/containerfile/api-entrypoint.sh"]
