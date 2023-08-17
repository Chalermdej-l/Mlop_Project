# MLOP Bank Deposit Prediction

This project leverages concepts learned from the[MLOps Zoomcamp](https://github.com/DataTalksClub/mlops-zoomcamp) course to implement a robust Machine Learning pipeline. By effectively training, evaluating, and selecting the optimal Machine Learning model, we aim to deploy it to a production environment while continuously monitoring its performance.

Utilizing the [Bank Marketing](https://www.kaggle.com/datasets/henriqueyamahata/bank-marketing?select=bank-additional-full.csv) dataset sourced from [Kaggle](https://www.kaggle.com/), our objective is to predict the likelihood of customers subscribing to a bank term deposit.

## Table of Contents
- [Problem Statement](#problem-statement)
- [Tools Used](#tools-used)
- [Project Flow](#project-flow)
  - [(1) Train and Track the Machine Learning Experiment](#1-train-and-track-the-machine-learning-experiment)
  - [(2) Deploy the Best Model](#2-deploy-the-best-model)
  - [(3) Monitor the Model](#3-monitor-the-model)
- [Reproducibility](#reproducibility)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Problem Statement
Traditionally, reaching out to customers to gauge their interest in a bank term deposit involves resource-intensive methods such as individual phone calls. With the vast number of customer accounts, this approach proves time-consuming and inefficient. To address this challenge and optimize the allocation of resources and time, we propose a Machine Learning solution. By training the model on historical customer data, including information gathered during the account creation process, and leveraging insights from previous marketing campaigns, we aim to predict whether a customer is likely to respond positively or negatively to a term deposit offer. This predictive capability empowers stakeholders to strategically target the most receptive audience, enhancing the efficacy of marketing campaigns.

The proposed model is designed to be integrated into the bank's internal systems, accessible via an API endpoint. The marketing department can input customer information lists, and in return, receive predictions indicating whether each client is likely to subscribe to the term deposit or not. This streamlined approach ensures informed decision-making and enables the optimization of marketing efforts for higher success rates.

Ultimately, this project showcases the application of MLOps principles in addressing real-world business challenges, illustrating the power of Machine Learning in enhancing marketing strategies and resource allocation within the banking industry.


## Tools Used

This project used the tool below.

- Data Orchestration: Perfect (as a data orchestration platform)
- Infrastructure Setup: Terraform (for provisioning and managing infrastructure)
- Containerization: Docker (for containerized deployment)
- Cloud Storage: AWS S3 (for data storage)
- Container Registry: Amazon ECR (for Docker image registry)
- Container Orchestration: Amazon ECS (for container deployment and scaling)
- Serverless Function: AWS Lambda (for front-end API)
- Reproducibility: Makefile (for ease of project reproducibility)
- Experiment Tracking: MLFlow (for tracking and managing machine learning experiments)
- Model Monitoring: Evidently + Grafana (for monitoring model performance)

## Project Flow

### (1) Train and Track the Machine Learning Experiment

Begin by fetching data using the Kaggle API. For the sake of this example, an "id" column is manually added to simulate customer IDs. In production, the data would ideally be sourced from a data warehouse or storage repository.
Train a model using the data. In this project, an XGBoost model is employed since it yielded the best results during experimentation.
A Python script is employed to train the model, iterating through various parameters to identify the best-performing configuration. This training script is logged by Prefect and scheduled to run monthly, utilizing the most current data available.
Experiment data is tracked and recorded by the MLflow server, storing model artifacts within AWS S3 storage, while also saving the experiment details within a PostgreSQL database.

### (2) Deploy the Best Model

Identify the best-performing model from step 1 based on accuracy and F1 score.
Data scientists make a judgment call, evaluating whether the new model surpasses the performance of the existing production model.
If the new model is deemed superior, it's pushed to GitHub. The model undergoes unit tests and integration tests, and the CI/CD pipeline is triggered using GitHub Actions to automate deployment.

### (3) Monitor the Model

Once the chosen model is finalized for deployment, it's integrated into a Lambda function. This function receives requests via an API endpoint and returns prediction results.
Incoming requests are logged into a PostgreSQL database.
On a daily basis, monitor metrics are calculated, using Evidently to assess model performance.
The calculated metrics are stored in the database and are linked with a Grafana dashboard for continuous monitoring and analysis of the model's behavior and efficacy.
This enhanced project flow captures the steps involved in data handling, model training, deployment decision-making, and ongoing monitoring to ensure the model's effectiveness over time.


## Reproducibility



## Usage

