import psycopg
import os
import pandas as pd
from evidently.report import Report
from evidently import ColumnMapping
from evidently.metrics import ColumnDriftMetric, DatasetDriftMetric, DatasetMissingValuesMetric,ColumnQuantileMetric

def getrefdata():
    None

def getlogdata():
    EXPERIMENT_ID = os.getenv('EXPERIMENT_ID','1')
    query= """
    select age, job, marital, education, default_bool, housing, loan, contact, duration, campaign, pdays, previous, poutcome, emprate, priceidx, confidx, euribor3m, employed,id, datestamp from user_log 
    """
    with psycopg.connect(f"host='localhost' dbname={EXPERIMENT_ID} port=5432 user=root password=root", autocommit=True) as con:
        data = con.execute(query).fetchall()
    con.close()
    return data