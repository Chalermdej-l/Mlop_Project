FROM python:3.7-slim-buster

COPY requirement/Requirement-ml.txt .

RUN pip install -r  Requirement-ml.txt
