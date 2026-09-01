FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY dashboard ./dashboard
COPY stream ./stream

EXPOSE 5000

CMD ["python", "dashboard/app.py"]
