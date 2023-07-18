FROM python:3.7-slim-buster

RUN pip install mlflow psycopg2-binary SQLAlchemy
