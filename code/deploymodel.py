import argparse

from mlflow.exceptions import MlflowException
from mlflow.tracking import MlflowClient

from constants import EXPERIMENT_NAME, MLFLOW_PORT
from envutil import update_env_file

MODEL_NAME = "ML_xgb"

# Which run wins the grid search.
ORDER_BY = [
    "metrics.f1 DESC",
    "metrics.score DESC",
    "attributes.end_time DESC",
    "params.n_estimators ASC",
    "params.max_depth ASC",
    "params.gamma ASC",
]


def get_experiment_id(client):
    experiment = client.get_experiment_by_name(EXPERIMENT_NAME)
    if experiment is None:
        raise SystemExit(f"MLflow experiment '{EXPERIMENT_NAME}' not found")
    return experiment.experiment_id


def registermodel(client, name_model):
    runs = client.search_runs(
        experiment_ids=[get_experiment_id(client)],
        filter_string="attributes.status = 'FINISHED'",
        order_by=ORDER_BY,
        max_results=1,
    )[0]
    run_id = runs.info.run_id
    model_source = f"runs:/{run_id}/model"

    # Create a model if not exist
    try:
        client.create_registered_model(name_model)
    except MlflowException:
        # The registered model already exists.
        pass
    client.create_model_version(
        name=name_model,
        source=model_source,
        run_id=run_id,
    )


def get_latest_model_version(client, name_model):
    latest_model = client.get_latest_versions(name=name_model, stages=["None"])
    return latest_model[0].version


def deploy_model_prod(version, client, name_model):
    client.transition_model_version_stage(
        name=name_model, version=version, stage="Production", archive_existing_versions=True
    )


def logmodelid(prod_model):
    update_env_file(".env.local", "RUN_ID", str(prod_model))


def main(mlflow_uri):
    client = MlflowClient(tracking_uri=f"http://{mlflow_uri}:{MLFLOW_PORT}")
    name_model = MODEL_NAME

    registermodel(client, name_model)
    version = get_latest_model_version(client, name_model)
    deploy_model_prod(version, client, name_model)

    prod_model = client.get_latest_versions(name=name_model, stages=["Production"])[0].run_id
    logmodelid(prod_model)
    print(prod_model)


if __name__ == "__main__":
    arg = argparse.ArgumentParser()
    arg.add_argument("mlflow_uri")
    arg = arg.parse_args()
    main(arg.mlflow_uri)
