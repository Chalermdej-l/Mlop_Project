import psycopg
import argparse

def main(db_host,db_name,port,db_username,db_password):
    query ='''
    -- Creation of product table
    CREATE TABLE IF NOT EXISTS user_log (
    age INT,
    job varchar(100),
    marital varchar(100),
    education varchar(100),
    default_bool varchar(100),
    housing varchar(100),
    loan varchar(100),
    contact varchar(100),
    duration INT,
    campaign INT,
    pdays INT,
    previous INT,
    poutcome varchar(100),
    emprate INT,
    priceidx INT,
    confidx INT,
    euribor3m INT,
    employed INT,
    id varchar(100),
    datestamp TIMESTAMP,
    prediction INT
    );

    CREATE TABLE IF NOT EXISTS monitor_log (
    time_stamp TIMESTAMP,
    drift_score NUMERIC ,
    drift_col INT ,
    missing_val NUMERIC ,
    share_drift NUMERIC 
    );
    '''
    print(f'Connecting to {db_name} database.')
    with psycopg.connect(f"host={db_host} dbname={db_name} port={port} user={db_username} password={db_password}", autocommit=True) as con:
        print('Creating table')
        con.execute(query)

    print('Finish running script.')
if __name__ =="__main__":
    arg = argparse.ArgumentParser()
    db_name     = arg.add_argument('db_name')
    db_user     = arg.add_argument('db_user')
    db_password = arg.add_argument('db_password')
    db_host     = arg.add_argument('db_host')
    db_port     = arg.add_argument('db_port')
    args = arg.parse_args()
    main(args.db_host,args.db_name,args.db_port,args.db_user,args.db_password)
