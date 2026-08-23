FROM python:3.11-slim-bookworm

WORKDIR /app

RUN useradd --create-home app
USER app

COPY --chown=app:app requirements/requirements-ml.txt .
RUN pip install --no-cache-dir -r requirements-ml.txt

CMD ["mlflow", "server", "--host", "0.0.0.0"]
