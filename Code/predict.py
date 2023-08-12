import logging
import mlflow
import os
import datetime
import psycopg
import datetime
from waitress import serve
from flask import Flask, request, jsonify


def getmodel():
    RUN_ID = os.getenv('RUN_ID')
    S3_BUCKET = os.getenv('S3_BUCKET')
    EXPERIMENT_ID = os.getenv('EXPERIMENT_ID','1')

    
    path = f's3://{S3_BUCKET}/{EXPERIMENT_ID}/{RUN_ID}/artifacts/model'
    model = mlflow.sklearn.load_model(path)
    return model

def save_request(datas,predict):
    DB_NAME_GRAFANA = os.getenv('DB_NAME_GRAFANA','Monitor_DB')
    IP_MONITOR = os.getenv('IP_WEB','172.21.0.2')
    current_time = datetime.datetime.today()
    query= """
    insert into user_log(age, job, marital, education, default_bool, housing, loan, contact, duration, campaign, pdays, previous, poutcome, emprate, priceidx, confidx, euribor3m, employed,id, datestamp, prediction) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """
    with psycopg.connect(f"host={IP_MONITOR} dbname={DB_NAME_GRAFANA} port=5432 user=root password=root", autocommit=True) as con:
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

app = Flask('bank-prediction')

@app.route('/predict', methods=['POST'])
def main():

    logging.info('Receving request...')
    request_data = request.get_json()
    data = convertdata(request_data)

    logging.info('Getting model...')
    model = getmodel()
    version = model.__hash__()

    logging.info('Predicting...')
    pred_result = predict(model,data)
    
    result = preparerespond(pred_result,request_data,version)

    logging.info('Logging data...')
    save_request(request_data,pred_result)


    logging.info('Done executing...')
    return jsonify(result)

if __name__ == "__main__":
    serve(app=app,host='0.0.0.0',port=9696)
    # app.run(debug=True, host='0.0.0.0', port=9696)