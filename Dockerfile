FROM python:3.11

WORKDIR /app

COPY ./app ./app
COPY ./migrations ./migrations
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY ./aerich.ini ./aerich.ini
COPY ./pyproject.toml ./pyproject.toml

COPY ./entrypoint.sh ./entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENV PYTHONPATH=/app

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
