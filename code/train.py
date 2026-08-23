import os

import mlflow
import pandas as pd
import yaml
from prefect import flow, task
from prefect.deployments import Deployment
from prefect.orion.schemas.schedules import CronSchedule
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics import accuracy_score, f1_score, roc_curve
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

from constants import EXPERIMENT_NAME
from features import bucket_age, bucket_duration
from helper import DataFrameToArrayTransformer

S3_BUCKET = os.getenv("S3_BUCKET_DATA", "mlop-data")
MLFLOW_URI = os.getenv("MLFLOW_URI")

mlflow.set_tracking_uri(MLFLOW_URI)


@task(retries=3)
def getdata():
    path = f"s3://{S3_BUCKET}/bank-additional-full.csv"
    reference_df = pd.read_csv(path, sep=";")
    return reference_df


@task
def clean_data(df_main):
    df_main["y_int"] = (df_main["y"] == "yes").astype("int")
    df_main["age"] = df_main["age"].apply(bucket_age)
    df_main["duration"] = df_main["duration"].apply(bucket_duration)
    df_main = df_main.drop(["y", "id", "day_of_week", "month"], axis=1)
    return df_main


@task(log_prints=True)
def score(y_test, y_pred):
    score = accuracy_score(y_test, y_pred.round())
    f1 = f1_score(y_test, y_pred.round())
    fpr, tpr, _ = roc_curve(y_test, y_pred)
    print(f"Accuracy {score}")
    print(f"F1 Score {f1}")
    print(f"FP {fpr.mean()}")
    print(f"TP {tpr.mean()}")
    return score, f1, fpr.mean(), tpr.mean()


def load_grid():
    with open("config/train_params.yaml") as params_file:
        return yaml.safe_load(params_file)


@flow(log_prints=True)
def main():
    print("Script Executing...")
    df_main = getdata()
    df_main = clean_data(df_main)

    print("Splitting data...")
    train_df, test_df = train_test_split(df_main, test_size=0.3, random_state=1)

    # Split data
    x_train = train_df.drop(["y_int"], axis=1).to_dict(orient="records")
    y_train = train_df["y_int"]
    x_test = test_df.drop(["y_int"], axis=1).to_dict(orient="records")
    y_test = test_df["y_int"]

    print("Training model...")
    grid = load_grid()
    mlflow.set_experiment(EXPERIMENT_NAME)
    # One parent run groups the grid search; each trial is a nested run
    # so params, metrics and the model live together in the MLflow UI.
    with mlflow.start_run(run_name="xgb-grid-search"):
        for lr in grid["learning_rate"]:
            for depth in grid["max_depth"]:
                for gamma in grid["gamma"]:
                    for n in grid["n_estimators"]:
                        params = dict(
                            learning_rate=lr,
                            n_estimators=n,
                            gamma=gamma,
                            max_depth=depth,
                        )
                        print(params)
                        with mlflow.start_run(nested=True, run_name=f"lr-{lr}-depth-{depth}"):
                            mlflow.log_params(params)

                            # Create pipeline
                            pipeline = make_pipeline(
                                DictVectorizer(sparse=True),
                                DataFrameToArrayTransformer(),
                                StandardScaler(),
                                XGBClassifier(**params, random_state=42),
                            )
                            pipeline.fit(x_train, y_train)
                            pred = pipeline.predict_proba(x_test)[:, 1]
                            sco, f1, fpr, tpr = score(y_test, pred)
                            print("Logging params...")
                            mlflow.log_metrics(
                                {"score": sco, "f1": f1, "fp": fpr, "tp": tpr}
                            )
                            mlflow.sklearn.log_model(
                                pipeline,
                                artifact_path="model",
                                code_paths=["helper.py"],
                            )
    print("Script done executing...")


if __name__ == "__main__":
    deployment = Deployment.build_from_flow(
        flow=main,
        name="MLOP-TrainML",
        schedule=(CronSchedule(cron="0 6 5 * *")),
    )
    deployment.apply()
