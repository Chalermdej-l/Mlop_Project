FROM public.ecr.aws/lambda/python:3.9

COPY requirement/Requirement-web.txt .

RUN pip install -r  Requirement-web.txt

RUN pip install xgboost

COPY code/predict-aws.py .

CMD [ "predict-aws.lambda_handler" ]