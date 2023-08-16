FROM  prefecthq/prefect:2.8.7-python3.11

COPY requirement/Requirement-prefect.txt .
COPY code/train.py .
COPY code/helper.py .

ARG Prefect_API_KEY
ARG Prefect_Workspace

RUN pip install -r  Requirement-prefect.txt
RUN prefect cloud login --key $Prefect_API_KEY --workspace $Prefect_Workspace

