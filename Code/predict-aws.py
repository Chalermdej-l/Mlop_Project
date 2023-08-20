import logging
import mlflow
import psycopg
import datetime
import os
import json

RUN_ID = os.getenv('RUN_ID')
S3_BUCKET = os.getenv('S3_BUCKET')
EXPERIMENT_ID = os.getenv('EXPERIMENT_ID','1')
DB_NAME_GRAFANA = os.getenv('DB_NAME_GRAFANA','Monitor_DB')
AWS_USER_DB = os.getenv('AWS_USER_DB')
AWS_PASS_DB = os.getenv('AWS_PASS_DB')
AWS_DB_MONITOR = os.getenv('AWS_DB_MONITOR')

logging.basicConfig(level=logging.INFO)

def getmodel():    
    path = f's3://{S3_BUCKET}/{EXPERIMENT_ID}/{RUN_ID}/artifacts/model'
    model = mlflow.sklearn.load_model(path)
    return model

def save_request(datas,predict):
    current_time = datetime.datetime.today()
    query= """
    insert into user_log(age, job, marital, education, default_bool, housing, loan, contact, duration, campaign, pdays, previous, poutcome, emprate, priceidx, confidx, euribor3m, employed,id, datestamp, prediction) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """
    
    with psycopg.connect(f"host={AWS_DB_MONITOR} dbname={DB_NAME_GRAFANA} port=5432 user={AWS_USER_DB} password={AWS_PASS_DB}", autocommit=True) as con:
        for i,data in enumerate(datas):
            data['timestamp'] = current_time
            data['prediction'] = int(predict[i])
            con.execute(query,tuple(data.values()))            
    con.close()
    return None

def convertdata(data):
    for i in data:
        # Convert age variable
        x =  i['age']
        i['age']    = (1 if x >=0 and x<32 else  \
                            2 if x>=32 and x<38 else  \
                            3 if x>=38 and x<47 else  \
                            4 if x>=47 and x<60 else  \
                            5 if x>=60 and x<90 else  \
                            6)

        # Convert duration variable
        x = i['duration']
        i['duration'] = (1 if x >=0 and x<30 else  \
                            2 if x>=30 and x<60 else  \
                            3 if x>=60 and x<120 else  \
                            4 if x>=120 and x<180 else  \
                            5 if x>=180 and x<240 else  \
                            6 if x>=240 and x<300 else  \
                            7 if x>=300 and x<360 else  \
                            8 if x>=360 and x<420 else  \
                            9 if x>=420 and x<480 else  \
                        10)
    return data

def predict(model,data):

    result = model.predict(data)
    return result


def preparerespond(predict,data,version):
    _list = []
    dict_result = {}
    for i,o in enumerate(predict):
        id = str(data[i]['id'])
        _list.append((id,int(o)))
        # dict_result['data'][id] = o

    dict_result['model_version'] = version
    dict_result['date'] = datetime.datetime.today().strftime('%Y-%m-%d')    
    dict_result['result'] = _list
    return dict_result




def lambda_handler(event, context):
    logging.info('Receiving request...')
    # request_data = event['body']
    request_data = [
  {"age": 56, "job": "housemaid", "marital": "married", "education": "basic.4y", "default": "no", "housing": "no", "loan": "no", "contact": "telephone", "duration": 261, "campaign": 1, "pdays": 999, "previous": 0, "poutcome": "nonexistent", "emp.var.rate": 1.1, "cons.price.idx": 93.994, "cons.conf.idx": -36.4, "euribor3m": 4.857, "nr.employed": 5191.0, "id": "3ad93d85-2390-11ee-83b8-e7e9bcdc248d"}
, {"age": 57, "job": "services", "marital": "married", "education": "high.school", "default": "unknown", "housing": "no", "loan": "no", "contact": "telephone", "duration": 149, "campaign": 1, "pdays": 999, "previous": 0, "poutcome": "nonexistent", "emp.var.rate": 1.1, "cons.price.idx": 93.994, "cons.conf.idx": -36.4, "euribor3m": 4.857, "nr.employed": 5191.0, "id": "3ad93d86-2390-11ee-bd5e-e7e9bcdc248d"}
, {"age": 37, "job": "services", "marital": "married", "education": "high.school", "default": "no", "housing": "yes", "loan": "no", "contact": "telephone", "duration": 226, "campaign": 1, "pdays": 999, "previous": 0, "poutcome": "nonexistent", "emp.var.rate": 1.1, "cons.price.idx": 93.994, "cons.conf.idx": -36.4, "euribor3m": 4.857, "nr.employed": 5191.0, "id": "3ad93d87-2390-11ee-8a78-e7e9bcdc248d"}
, {"age": 40, "job": "admin.", "marital": "married", "education": "basic.6y", "default": "no", "housing": "no", "loan": "no", "contact": "telephone", "duration": 151, "campaign": 1, "pdays": 999, "previous": 0, "poutcome": "nonexistent", "emp.var.rate": 1.1, "cons.price.idx": 93.994, "cons.conf.idx": -36.4, "euribor3m": 4.857, "nr.employed": 5191.0, "id": "3ad93d88-2390-11ee-b81f-e7e9bcdc248d"}
, {"age": 56, "job": "services", "marital": "married", "education": "high.school", "default": "no", "housing": "no", "loan": "yes", "contact": "telephone", "duration": 307, "campaign": 1, "pdays": 999, "previous": 0, "poutcome": "nonexistent", "emp.var.rate": 1.1, "cons.price.idx": 93.994, "cons.conf.idx": -36.4, "euribor3m": 4.857, "nr.employed": 5191.0, "id": "3ad93d89-2390-11ee-a395-e7e9bcdc248d"}
]
    data = convertdata(request_data)

    logging.info('Getting model...')
    model = getmodel()
    version = model.__hash__()

    logging.info('Predicting...')
    pred_result = predict(model, data)

    result = preparerespond(pred_result, request_data, version)

    logging.info('Logging data...')
    save_request(request_data, pred_result)

    response = {
        "statusCode": 200,
        "body": json.dumps(result)
    }

    logging.info('Done executing...')
    return response


if __name__ == "__main__":
    lambda_handler()
