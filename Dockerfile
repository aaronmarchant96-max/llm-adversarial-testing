FROM python:3.10-slim

WORKDIR /app

COPY schema_drift_optimized.py .
COPY schema_conflict_test.py .

RUN pip install requests

ENV OLLAMA_HOST=http://host-gateway:11434

CMD ["python3", "schema_conflict_test.py"]
