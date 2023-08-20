FROM python:3.7-slim-buster

COPY requirement/Requirement-web.txt .

RUN pip install -r  Requirement-web.txt

RUN pip install xgboost

WORKDIR /webapp

COPY code/predict.py .


# ENTRYPOINT [ "waitress-serve", "--host" ,"127.0.0.1" ,"--port" ,"9696", "predict:app" ]
