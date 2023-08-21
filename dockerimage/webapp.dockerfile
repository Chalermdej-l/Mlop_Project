FROM python:3.7-slim-buster

COPY requirement/Requirement-web.txt .

RUN pip install -r  Requirement-web.txt

RUN pip install xgboost

WORKDIR /webapp

COPY code/predict.py .

