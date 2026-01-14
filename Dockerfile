FROM python:3.10-slim

WORKDIR /app

ENV PYTHONPATH=/app
ENV RUNNING_IN_DOCKER=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/
COPY config.py .

CMD ["python", "src/main.py"]
