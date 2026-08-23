import datetime
import logging
import os

import mlflow
import psycopg
from flask import Flask, jsonify, request
from waitress import serve

from constants import API_PORT, DB_PORT, REQUEST_COLUMNS
from features import bucket_age, bucket_duration
from response import prepare_response

RUN_ID = os.getenv("RUN_ID")
S3_BUCKET = os.getenv("S3_BUCKET")
EXPERIMENT_ID = os.getenv("EXPERIMENT_ID", "1")
DB_NAME_GRAFANA = os.getenv("DB_NAME_GRAFANA", "Monitor_DB")
AWS_USER_DB = os.getenv("AWS_USER_DB")
AWS_PASS_DB = os.getenv("AWS_PASS_DB")
AWS_DB_MONITOR = os.getenv("AWS_DB_MONITOR")

app = Flask("bank-prediction")


def get_db_connection():
    return psycopg.connect(
        host=AWS_DB_MONITOR,
        dbname=DB_NAME_GRAFANA,
        port=DB_PORT,
        user=AWS_USER_DB,
        password=AWS_PASS_DB,
        autocommit=True,
    )


def getmodel():
    path = f"s3://{S3_BUCKET}/{EXPERIMENT_ID}/{RUN_ID}/artifacts/model"
    return mlflow.sklearn.load_model(path)


# Load once at startup instead of re-downloading and unpickling the
# whole pipeline from S3 on every request.
model = getmodel()


def save_request(datas, predict):
    current_time = datetime.datetime.today()
    query = """
    insert into user_log(
        age, job, marital, education, default_bool, housing, loan, contact,
        duration, campaign, pdays, previous, poutcome,
        emprate, priceidx, confidx, euribor3m, employed,
        id, datestamp, prediction
    ) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """
    with get_db_connection() as con:
        for i, data in enumerate(datas):
            data["timestamp"] = current_time
            data["prediction"] = int(predict[i])
            values = tuple(data[col] for col in REQUEST_COLUMNS)
            con.execute(query, values + (current_time, int(predict[i])))


def convertdata(data):
    for record in data:
        # Convert age variable
        record["age"] = bucket_age(record["age"])
        # Convert duration variable
        record["duration"] = bucket_duration(record["duration"])
    return data


def predict(model, data):
    return model.predict(data)


@app.route("/predict", methods=["POST"])
def main():
    logging.info("Receiving request...")
    request_data = request.get_json()
    data = convertdata(request_data)

    logging.info("Predicting...")
    pred_result = predict(model, data)

    result = prepare_response(pred_result, request_data, RUN_ID)

    logging.info("Logging data...")
    save_request(request_data, pred_result)

    logging.info("Done executing...")
    return jsonify(result)


if __name__ == "__main__":
    serve(app=app, host="0.0.0.0", port=API_PORT)
