FROM python:3.11

WORKDIR /app

COPY ./app/* ./
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY ./aerich.ini ./aerich.ini
COPY ./pyproject.toml ./pyproject.toml

COPY ./entrypoint.sh ./entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]