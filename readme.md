# MLOP Bank Deposit Prediction

This project leverages concepts learned from the[MLOps Zoomcamp](https://github.com/DataTalksClub/mlops-zoomcamp) course to implement a robust Machine Learning pipeline. By effectively training, evaluating, and selecting the optimal Machine Learning model, this project aims to deploy it to a production environment while continuously monitoring its performance.

Utilizing the [Bank Marketing](https://www.kaggle.com/datasets/henriqueyamahata/bank-marketing?select=bank-additional-full.csv) dataset sourced from [Kaggle](https://www.kaggle.com/), our objective is to predict the likelihood of customers subscribing to a bank term deposit.

## Table of Contents
- [Problem Statement](#problem-statement)
- [Tools Used](#tools-used)
- [Project Flow](#project-flow)
  - [1. Data Retrieval](#1-data-retrieval)
  - [2. Train and Track the Machine Learning Experiment](#2-train-and-track-the-machine-learning-experiment)
  - [3. Model Selection and Deployment](#3-model-selection-and-deployment)
  - [4. Front-End API Service](#4-front-end-api-service)
  - [5. Performance Monitoring](#5-performance-monitoring)
- [Reproducibility](#reproducibility)
- [Usage](#usage)
- [Further Improvements](#further-improvements)
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

![Project Flow](/image/projectflow.png)

## Project Flow

### 1. Data Retrieval

In this step, the project starts by fetching data from Kaggle using the Kaggle API. The retrieved data is then modified and add an "id" column to simulate customer IDs in production this should be present in the data then the data is stored in an AWS S3 bucket. To manage the data processing pipeline, Prefect is utilized as a data orchestrator and scheduler. In production, the data should be sourced directly from the database.

### 2. Train and Track the Machine Learning Experiment

With the acquired data, the project proceeds to train a machine-learning model in this project XGBoost model is used as this performs the best from experimenting with the data. MLflow is employed for tracking and managing training experiments. Experiment logs are stored in an AWS RDS PostgreSQL database.
The trained model artifacts are then saved in an AWS S3 bucket.

### 3. Model Selection and Deployment

Python script is implemented to connect to the MLflow. The script selects the most optimal model based on accuracy and F1 score metrics. This model is then deployed to a front-end API endpoint. 
In production, the data science team should monitor the model and evaluate whether the new model is suited to deploy to production or not. All production models are tracked in MLflow for version control.

### 4. Front-End API Service

The front-end API service is established using Flask and Waitress. This API interacts with the AWS S3 bucket to retrieve the model corresponding to the provided model ID. By accepting API requests from users, the front end performs predictions on incoming data. The API request is logged in an AWS RDS PostgreSQL database for model monitoring and service request traffic.

### 5. Performance Monitoring

To assess the performance of the deployed model Evidently is used for the calculation of metrics based on API prediction results. By comparing these metrics with the data stored in AWS S3 from Step 1, the model's performance is evaluated. The calculated metrics are then stored in a database. Grafana is used to fetch these metrics and user logs, presenting them in an accessible performance dashboard.


## Reproducibility



## Usage

## Further Improvements
