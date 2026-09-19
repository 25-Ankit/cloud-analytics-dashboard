FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    ANALYTICS_DB_PATH=/app/data/events.db

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY stream ./stream
COPY processor ./processor
COPY dashboard ./dashboard
COPY data-generator ./data-generator
COPY runtime ./runtime
COPY sdk ./sdk
COPY apps ./apps
COPY benchmarks ./benchmarks

RUN mkdir -p /app/data /app/benchmarks/results
EXPOSE 5000
CMD ["gunicorn","--bind","0.0.0.0:5000","--workers","1","dashboard.app:app"]
