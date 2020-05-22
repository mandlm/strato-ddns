FROM python:3-alpine
RUN pip install --no-cache-dir --upgrade pip

WORKDIR /app
COPY src/ ./
CMD [ "python", "ddns_update.py" ]
