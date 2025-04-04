FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1
WORKDIR /app/api

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000"]
