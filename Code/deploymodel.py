from mlflow.tracking import MlflowClient


def registermodel(client,name_model):       
    runs = client.search_runs(experiment_ids=1
                            ,filter_string="attribute.status = 'FINISHED'"
                            ,order_by=["metrics.f1 DESC","metrics.score DESC","attributes.end_time DESC","params.n_estimators ASC","params.max_depth ASC","params.gamma ASC"]
                            ,max_results=1)[0]
    id   =  runs.info.run_id
    rud_id=f"runs:/{id}/model"

    # Create a model if not exist
    try:
        client.create_registered_model(name_model)
    except:
        None
    result = client.create_model_version(
        name=name_model,
        source=rud_id,
        run_id=id
    )

def getlastestmodel_version(client,name_model):
        latest_model = client.get_latest_versions(name=name_model,stages=['None'])    
        version = latest_model[0].version
        return version

def deploy_model_prod(version,client,name_model):
    client.transition_model_version_stage(
        name=name_model, version=version, stage="Production",archive_existing_versions=True
    )

def logmodelid(prod_model):
    with open('../.env','r')as f:
        con =f.read()

    with open('../.env','w')as f:
        for i in con.split('\n'):
            para = i[:i.find('=')-1]
            if para == 'RUN_ID':
                f.write(f"RUN_ID = '{prod_model}'")
                print(i)
            else:
                f.write(i)
            f.write('\n')
def main():
    client = MlflowClient(tracking_uri='http://127.0.0.1:5000')
    name_model = 'ML_xgb'   

    print('Register best model ...')
    registermodel(client,name_model)
    version = getlastestmodel_version(client,name_model)

    print(f'Move model to production current version {version}...')
    deploy_model_prod(version,client,name_model)

# local deploy
    print('Getting prod model id...')
    prod_model = client.get_latest_versions(name=name_model,stages=['Production'])[0].run_id

    print('logging model id ...')
    logmodelid(prod_model)
if __name__ =='__main__':
    main()