from prefect import flow,task
from prefect.orion.schemas.schedules import CronSchedule
from prefect.deployments import Deployment
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_curve,accuracy_score,f1_score,auc
from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
import xgboost 
import mlflow
import pandas as pd
from  helper import DataFrameToArrayTransformer
import os 

S3_BUCKET = os.getenv('S3_BUCKET_DATA','mlop-data')    
MLFLOW_URI = os.getenv('MLFLOW_URI')

mlflow.set_tracking_uri("127.0.0.1:5000")

@task(retries=3)
def getdata():
    path = f's3://{S3_BUCKET}/bank-additional-full.csv'
    reference_df = pd.read_csv(path,sep=';')
    return reference_df

@task
def clendata(df_main):
    df_main['y_int'] = (df_main['y'] == 'yes').astype('int')
    df_main['age'] = df_main['age'].apply(lambda x :  1 if x >=0 and x<32 else  \
                                            2 if x>=32 and x<38 else  \
                                            3 if x>=38 and x<47 else  \
                                            4 if x>=47 and x<60 else  \
                                            5 if x>=60 and x<90 else  \
                                            6)
    df_main['duration'] = df_main['duration'].apply(lambda x :  1 if x >=0 and x<30 else  \
                                        2 if x>=30 and x<60 else  \
                                        3 if x>=60 and x<120 else  \
                                        4 if x>=120 and x<180 else  \
                                        5 if x>=180 and x<240 else  \
                                        6 if x>=240 and x<300 else  \
                                        7 if x>=300 and x<360 else  \
                                        8 if x>=360 and x<420 else  \
                                        9 if x>=420 and x<480 else  \
                                        10)  
    df_main = df_main.drop(['y','id','day_of_week','month'],axis=1)

    return df_main


@task(log_prints=True)
def score(y_test,y_pred):
    score = accuracy_score(y_test,y_pred.round())
    f1 = f1_score(y_test,y_pred.round())
    fp,tp,_ =roc_curve(y_test,y_pred)
    print(f'Accuary {score}')
    print(f'F1 Score {f1}')
    print(f'FP {fp.mean()}')
    print(f'TP {tp.mean()}')
    return score,f1,fp.mean(),tp.mean()

@task
def trainmodel_xgb(x_train,y_train):
    xgb = xgboost.XGBClassifier(learning_rate=0.01,n_estimators=500,gamma=10,max_depth=20)
    xgb.fit(x_train,y_train)

    return xgb

@flow(log_prints=True)
def main():
    print('Script Executing...')
    df_main = getdata()
    df_main = clendata(df_main)

    print('Spliting data...')
    train_df,test_df = train_test_split(df_main,test_size=0.3,random_state=1)

    # Split data
    x_train = train_df.drop([ 'y_int'],axis=1).to_dict(orient='records')
    y_train = train_df['y_int']
    x_test = test_df.drop([ 'y_int'],axis=1).to_dict(orient='records')
    y_test = test_df['y_int']

    print('Traning model...')
    # Train model
    mlflow.set_experiment('ML-xgb')
    para_lr = [0.1,0.01]
    para_depth = [5,15,25]
    para_gamma = [1,10,20]
    para_n= [100,300,600]
    for lr in para_lr:
        for depth in para_depth:
            for gamma in para_gamma:
                for n in para_n: 
                    with mlflow.start_run():                                   
                        params = dict(learning_rate=lr,n_estimators=n,gamma=gamma,max_depth=depth)
                        print(params)
                        mlflow.log_params(params)

                        # Create pipeline
                        pipeline = make_pipeline(
                            DictVectorizer(sparse=True),
                            DataFrameToArrayTransformer(),
                            StandardScaler(),
                            xgboost.XGBClassifier(**params)
                        )
                        pipeline.fit(x_train,y_train)
                        pred =pipeline.predict_proba(x_test)[::,1]
                        sco,f1,fp,tp=  score(y_test,pred)
                        print('Logging para...')
                        mlflow.log_metrics({'score':sco,'f1':f1,'fp':fp,'tp':tp})
                        mlflow.sklearn.log_model(pipeline,artifact_path='model',code_paths=['code/helper.py'])
    print('Script done executing...')
if __name__ == '__main__':
    main()