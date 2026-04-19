FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir requests

COPY load_gen.py .

CMD ["python", "load_gen.py"]
