"""Shared configuration for the MLop services."""

DB_PORT = 5432
MLFLOW_PORT = 5000
API_PORT = 9696

# MLflow experiment that train.py writes to.
EXPERIMENT_NAME = "ML-xgb"

# Raw /predict request fields, in user_log column order (see
# save_request in predict.py).
REQUEST_COLUMNS = [
    "age",
    "job",
    "marital",
    "education",
    "default",
    "housing",
    "loan",
    "contact",
    "duration",
    "campaign",
    "pdays",
    "previous",
    "poutcome",
    "emp.var.rate",
    "cons.price.idx",
    "cons.conf.idx",
    "euribor3m",
    "nr.employed",
    "id",
]
