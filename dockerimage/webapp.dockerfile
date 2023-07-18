FROM python:3.7-slim-buster

RUN pip install flask mlflow waitress boto3 botocore scikit-learn 

RUN pip install xgboost

WORKDIR /webapp

COPY code/predict.py .


# ENTRYPOINT [ "waitress-serve", "--host" ,"127.0.0.1" ,"--port" ,"9696", "predict:app" ]
