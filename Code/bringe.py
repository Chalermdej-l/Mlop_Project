from mlflow.entities import ViewType
import mlflow
from mlflow.tracking import MlflowClient
import os

def main():
    client = MlflowClient(tracking_uri='http://127.0.0.1:5000')
    runs = client.search_runs(experiment_ids=1,order_by=["metrics.f1 ASC"],max_results=1)
    
    # RUN_ID = os.getenv('RUN_ID')
    # DB_NAME = os.getenv('DB_NAME')
    # path = f's3://{DB_NAME}/1/{RUN_ID}/artifacts/model'

    path = runs[0].info.artifact_uri + '/model'
    model = mlflow.pyfunc.load_model(path)


if __name__ == '__main__':
    main()