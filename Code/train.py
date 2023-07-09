from prefect import flow,task
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_curve,accuracy_score,f1_score,auc
from sklearn.feature_extraction import DictVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import xgboost 
import mlflow
import pandas as pd
import matplotlib.pyplot as plt
import pickle

mlflow.set_tracking_uri('http://127.0.0.1:5000')
mlflow.autolog()

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
    return df_main


def preparedata(data,dv,sc,mode=None):
    if mode =='init':
        dv = DictVectorizer(sparse=True)
        data_tran = dv.fit_transform(data.to_dict(orient='records'))        
        sc = StandardScaler()
        data_tran = sc.fit_transform(data_tran.toarray())
        return data_tran,dv,sc
    else:
        # Tranform data with DV    
        data_tran = dv.transform(data.to_dict(orient='records'))
        data_tran = sc.transform(data_tran.toarray())
        return data_tran
    
@task
def score(y_test,y_pred):
    score = accuracy_score(y_test,y_pred.round())
    f1 = f1_score(y_test,y_pred.round())
    print(f'Accuary {score}')
    print(f'F1 Score {f1}')
    fpr, tpr, _ = roc_curve(y_test,  y_pred)
    # print(f'auc = {auc(fpr,tpr)}')
    # plt.style.use('classic')
    # plt.figure(figsize=(6,6))
    # plt.plot(fpr,tpr)
    # plt.ylabel('True Positive Rate')
    # plt.xlabel('False Positive Rate')
    # plt.show()
    return score,f1

@task
def splitdata(df_drop):
    train_df,test_df = train_test_split(df_drop,test_size=0.3,random_state=1)

    # Peapare data
    x_train = train_df.drop([ 'y_int'],axis=1)
    x_train,dv,sc = preparedata(x_train,None,None,'init')
    y_train = train_df['y_int']
    
    x_test = test_df.drop([ 'y_int'],axis=1)
    x_test = preparedata(x_test,dv,sc,None)
    y_test = test_df['y_int']

    return x_train,x_test,y_train,y_test

@task
def trainmodel_xgb(x_train,y_train):
    xgb = xgboost.XGBClassifier(learning_rate=0.01,n_estimators=500,gamma=10,max_depth=20)
    xgb.fit(x_train,y_train)

    return xgb

@task
def trainmodel_tree(x_train,y_train):
    tree = DecisionTreeClassifier(min_samples_split=5, min_samples_leaf=25, max_depth=8, criterion='gini')
    tree.fit(x_train,y_train)

    return tree

@task
def trainmodel_logis(x_train,y_train):
    logis = LogisticRegression(max_iter=1000)
    logis.fit(x_train,y_train)

    return logis


@flow
def main():
    df_main = getdata()
    df_main = clendata(df_main)

    df_drop = df_main.drop(['y'],axis=1)
    # int_col = df_drop.dtypes[df_drop.dtypes!='object'].index.to_list()[:-1]
    # cat_col = df_drop.dtypes[df_drop.dtypes=='object'].index.to_list()

    x_train,x_test,y_train,y_test = splitdata(df_drop)

    # Tranin model
    mlflow.set_experiment('ML-xgb')
    model_xg = trainmodel_xgb(x_train,y_train)
    pred  = model_xg.predict_proba(x_test)[::,1]
    score(y_test,pred)
    pickle.dump(model_xg, open('model/model_xg.pkl', 'wb'))

    mlflow.set_experiment('ML-tree')
    model_xg = trainmodel_tree(x_train,y_train)
    pred  = model_xg.predict_proba(x_test)[::,1]
    score(y_test,pred)
    pickle.dump(model_xg, open('model/model_tree.pkl', 'wb'))

    mlflow.set_experiment('ML-logis')
    model_xg = trainmodel_logis(x_train,y_train)
    pred  = model_xg.predict_proba(x_test)[::,1]
    score(y_test,pred)
    pickle.dump(model_xg, open('model/model_logis.pkl', 'wb'))

if __name__ == '__main__':
    main()