from prefect import flow,task
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_curve,accuracy_score,f1_score,auc
from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
import xgboost 
import mlflow
import pandas as pd
from  helper import DataFrameToArrayTransformer

mlflow.set_tracking_uri('http://127.0.0.1:5000')
# mlflow.autolog()

@task(retries=3)
def getdata():
    df_main = pd.read_csv('data/bank-additional-full.csv',sep=";")

    return df_main

@task
def clendata(df_main):
    df_main['y_int'] = (df_main['y'] == 'yes').astype('int')
    df_main['age'] = df_main['age'].apply(lambda x :  1 if x >=0 and x<32 else  \
                                            2 if x>=32 and x<38 else  \
                                            3 if x>=38 and x<47 else  \
                                            4 if x>=47 and x<60 else  \
                                            5 if x>=60 and x<90 else  \
                                            6)
    df_main = df_main.drop(['y'],axis=1)
    return df_main


@task
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

@flow
def main():
    df_main = getdata()
    df_main = clendata(df_main)

    train_df,test_df = train_test_split(df_main,test_size=0.3,random_state=1)

    # Split data
    x_train = train_df.drop([ 'y_int'],axis=1).to_dict(orient='records')
    y_train = train_df['y_int']
    x_test = test_df.drop([ 'y_int'],axis=1).to_dict(orient='records')
    y_test = test_df['y_int']

    # Train model
    mlflow.set_experiment('ML-xgb')

    params = dict(learning_rate=0.01,n_estimators=500,gamma=10,max_depth=20)
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

    mlflow.log_metrics({'score':sco,'f1':f1,'fp':fp,'tp':tp})
    mlflow.sklearn.log_model(pipeline,artifact_path='model' )

if __name__ == '__main__':
    main()