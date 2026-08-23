FROM python:3.7-slim-buster

COPY requirements/requirements-ml.txt .

RUN pip install -r  Requirement-ml.txt
