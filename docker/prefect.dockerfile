FROM prefecthq/prefect:2.8.7-python3.11

WORKDIR /app

# Install dependencies first so code changes don't bust the pip layer.
# Prefect Cloud auth comes from PREFECT_API_URL/PREFECT_API_KEY at
# runtime (docker-compose), never baked into an image layer.
COPY requirements/requirements-prefect.txt .
RUN pip install --no-cache-dir -r requirements-prefect.txt

COPY code/train.py .
COPY code/helper.py .
COPY code/monitor.py .
COPY code/features.py .
COPY code/constants.py .
COPY config/train_params.yaml config/
