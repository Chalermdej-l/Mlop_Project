import warnings
warnings.filterwarnings("ignore", message=".*The 'nopython' keyword.*")
import pandas as pd
import psycopg
import os
import datetime
from evidently.report import Report
from evidently import ColumnMapping
from evidently.metrics import ColumnDriftMetric, DatasetDriftMetric, DatasetMissingValuesMetric,DataDriftTable

DB_NAME_GRAFANA = os.getenv('DB_NAME_GRAFANA','Monitor_DB')
S3_BUCKET = os.getenv('S3_BUCKET_DATA','mlop-data')    

def getrefdata():
    path = f's3://{S3_BUCKET}/bank-additional-full.csv'
    reference_df = pd.read_csv(path,sep=';')
    reference_df['y'] = (reference_df['y'] == 'yes').astype('int')
    reference_df.drop([ 'month', 'day_of_week', 'id'],axis=1,inplace=True)
    reference_df.columns = ['age', 'job', 'marital', 'education', 'default_bool', 'housing', 'loan','contact', 'duration', 'campaign', 'pdays', 'previous', 'poutcome','emprate', 'priceidx', 'confidx', 'euribor3m', 'employed','prediction']
    return reference_df

def getlogdata():

    query= """
    select * from user_log;
    """
    with psycopg.connect(f"host='localhost' dbname={DB_NAME_GRAFANA} port=5432 user=root password=root", autocommit=True) as con:
        receive_df = pd.read_sql_query(query, con)
    con.close()
    receive_df.drop(['id','datestamp'],inplace=True,axis=1)
    return receive_df

def genmetric(reference_df,receive_df):
    num_features = ['pdays' ,'emprate', 'priceidx', 'confidx', 'euribor3m', 'employed']
    cat_features =  ['age', 'job', 'marital', 'education', 'default_bool', 'housing', 'loan','contact', 'duration', 'campaign', 'previous', 'poutcome']
    column_mapping = ColumnMapping(
        prediction='prediction',
        numerical_features=num_features,
        categorical_features=cat_features,
        target=None
                )
    report = Report(metrics = [
        ColumnDriftMetric(column_name='prediction'),
        DatasetDriftMetric(),
        DatasetMissingValuesMetric(),
        DataDriftTable()
    ])
    report.run(reference_data = reference_df, current_data = receive_df,column_mapping=column_mapping)    
    result = report.as_dict()
    timestamp = datetime.datetime.now()
    rediction_drift = result['metrics'][0]['result']['drift_score']
    num_drifted_columns = result['metrics'][1]['result']['number_of_drifted_columns']
    share_missing_values = result['metrics'][2]['result']['current']['share_of_missing_values']
    share_of_drifted_columns = result['metrics'][3]['result']['share_of_drifted_columns']
    return (timestamp,rediction_drift,num_drifted_columns,share_missing_values,share_of_drifted_columns)

def writedata(record):   
    query= '''
    insert into monitor_log(time_stamp, drift_score, drift_col, missing_val,share_drift) values (%s, %s, %s, %s, %s)
    '''
    with psycopg.connect(f"host='localhost' dbname={DB_NAME_GRAFANA} port=5432 user=root password=root", autocommit=True) as con:
        sql = con.execute(query,record)
    return None

def getmonitor():
    print('Getting reference data...')
    reference_df = getrefdata()
    print('Getting log data...')
    receive_df = getlogdata()
    print('Generating metric...')
    metric = genmetric(reference_df,receive_df)
    print('Writing data to database...')
    writedata(metric)
    print('Finish running script.')

if __name__ == '__main__':
    getmonitor()