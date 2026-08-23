FROM python:3.11-slim-bookworm

WORKDIR /webapp

RUN useradd --create-home app
USER app

COPY --chown=app:app requirements/requirements-web.txt .
RUN pip install --no-cache-dir -r requirements-web.txt

COPY --chown=app:app code/predict.py .
COPY --chown=app:app code/features.py .
COPY --chown=app:app code/constants.py .
COPY --chown=app:app code/response.py .

CMD ["waitress-serve", "--host", "0.0.0.0", "--port", "9696", "predict:app"]
