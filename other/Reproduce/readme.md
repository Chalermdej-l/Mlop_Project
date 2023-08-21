
## Setup and Configuration Guide

# Table of Contents


  - [Clone the Project and Configuration Setup](#1-clone-the-project-and-configuration-setup)
  - [Data Retrieval and Infrastructure Initialization](#2-data-retrieval-and-infrastructure-initialization)
  - [The Key Pair to Connect to the EC2](#3-the-key-pair-to-connect-to-the-ec2)
- [Data Retrieval and Infrastructure Initialization](#data-retrieval-and-infrastructure-initialization)
  - [Create S3 Bucket](#1-execute-the-following-command-to-create-an-s3-bucket-this-bucket-will-be-used-for-storing-our-data-and-model-artifacts)
  - [Download and Prepare Data](#2-if-you-have-the-kaggle-api-set-up-download-and-extract-the-data-into-the-data-directory-using)
  - [Add ID Column and Upload Data to S3](#3-then-we-will-add-an-id-column-to-the-data-and-then-upload-it-to-the-s3-bucket-run)
  - [Terraform Infrastructure Setup](#4-for-executing-the-terraform-plan-of-the-project-use)
  - [Create Planned Services](#5-then-run-below-to-create-the-planned-services)
- [The Key Pair to Connect to the EC2](#the-key-pair-to-connect-to-the-ec2)
- [VM Connection and Setup](#4-vm-connection-and-setup)
- [Docker Create and Run](#5-docker-create-and-run)
- [Train the Model and Deploy the Model](#6-train-the-model-and-deploy-the-model)
- [Model Monitoring](#7-model-monitoring)
- [Clean Up](#8-clean-up)


### 1. Clone the Project and Configuration Setup

First, clone the project and navigate to the cloned directory:

```
git clone https://github.com/Chalermdej-l/Mlop_Project.git
cd MLop_Project
```

Update the `.env` file with the necessary credentials mentioned in the `Prerequisite` section.

![Configuration Setup](/image/reproduce/1.png)

For setting up AWS credentials to access the project, run:

Run the following command:

```
make awssetup
```

![AWS Configuration](/image/reproduce/2.png)

Provide the following details:
- AWS Access Key
- AWS Secret Access Key
- Default Region Name

### 2. Data Retrieval and Infrastructure Initialization

Execute the following command to create an S3 bucket. This bucket will be used for storing our data and model artifacts:

```
make s3create
```


![S3 Bucket Creation](/image/reproduce/3.png)

If you have the [Kaggle](https://www.kaggle.com/) API set up, download and extract the data into the `data` directory using:

```
kaggle datasets download -d henriqueyamahata/bank-marketing -p data --unzip –force
```

If you don't have a Kaggle API key, manually download the dataset from [Bank Marketing](https://www.kaggle.com/datasets/henriqueyamahata/bank-marketing?select=bank-additional-full.csv) and place it in the `data` folder.

Then we will add an "id" column to the data and then upload it to the S3 bucket, run:

```
make getdata
```

For executing the Terraform plan of the project, use:

```
make infra-setup
```

The resulting output should resemble:

![Terraform Output](/image/reproduce/4.png)


Then run below to create the plan services
```
make infra-create 
```

Terraform will create:

[RDS Postggress](https://ap-southeast-1.console.aws.amazon.com/rds/home?region=ap-southeast-1#databases)

![Terraform Output](/image/reproduce/5.png)

[EC2 Instance](https://ap-southeast-1.console.aws.amazon.com/ec2/home?region=ap-southeast-1#Instances)

![Terraform Output](/image/reproduce/6.png)

## 3. The Key Pair to Connect to the EC2

The code will also output the endpoint of each resource for connection later:

![Terraform Output](/image/reproduce/7.png)

Run the following command to prepare the environment:

```
make infra-prep
```

This command will output the endpoint in an output.json file, populate the DBS_ENDPOINT, AWS_DB_ML, AWS_DB_MONITOR in the .env file, and output the private and public key into the key folder:

![Terraform Output](/image/reproduce/8.png)

## 4. VM Connection and Setup

Open another terminal and navigate to the project and run the following command to connect to the EC2. This terminal will now be referred to as `cloud terminal`, and the first terminal as `local terminal`:

```
make vm-connect 
```

![Terraform Output](/image/reproduce/9.png)

Go back to the `local terminal` and run:


```
make vm-copy
```


This command will copy files from the local machine to the VM for deployment.

Go back to the `cloud terminal` and run the following commands to update the VM and install Python and Make:

```
cd mlproject
sudo apt-get update -y
sudo apt install python3-pip -y
sudo pip install make
```

After this is done, run:

```
make vm-setup
```

This will install Docker. Then run the following commands to install Docker Compose:


```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose –version
```

The output should look like below:

![Terraform Output](/image/reproduce/10.png)

## 5. Docker Create and Run

Create the Docker image by running:


```
make dockercreate
```

And start up the image by:


```
make dockerup
```

This command will start our MLFLOW and GRAFANA Images.

Go to [Prefect](https://app.prefect.cloud/), where there will now be 2 deployments:

- MLOP-MonitorML will run daily to generate the metric using Evendily and store the data in the Postgres database.
- MLOP-TrainML will run monthly to train with the latest data in production. The data will be fetched from the database, ensuring that the model is trained with up-to-date data.

![Terraform Output](/image/reproduce/11.png)

### 6. Train the model and deploy the model

Run the MLOP-TrainML job to start training 

The job will fetch the data from the s3 bucket and train the model using xgbooster model under “ML-xgb” experiment name from the experiment this model performs the best. 
The experiment will be logged to the mlflow  host on our ec2 instance

We can access the mlflow using the ec2 endpoint port 3000 the ec2 endpoint can be received in our .env file DBS_ENDPOINT value and copy the endpoint

![Terraform Output](/image/reproduce/12.png)

Example http://xxx-xx-xxx-xxx-xx.ap-southeast-1.compute.amazonaws.com:5000/

![Terraform Output](/image/reproduce/13.png)

Once the job finishes training 

![Terraform Output](/image/reproduce/14.png)

Go back to the `local terminal` and run 

```
db_endpoint=$(terraform output -state=infra/terraform.tfstate DBS_ENDPOINT)
db_endpoint=$(echo $db_endpoint | tr -d '"')
model_id=$(python code/deploymodel.py $db_endpoint)
```


This code will find the best performance model base on Acuary and F1 score and output the model_id


```
ssh -i key/private.pem ubuntu@${db_endpoint} "cd mlproject && RUN_ID=${model_id} docker-compose --profile webapp up --detac"
```
We will then use this model id and run it in our docker image front-end API as the production model.

![Terraform Output](/image/reproduce/15.png)


Once the docker is up we can pass the request to this endpoint the API endpoint will be using port 9696
Example http://xxx-xx-xxx-xxx-xx.ap-southeast-1.compute.amazonaws.com:9696/

Run this command to send out a request to our frontend 

```
python code/api_test.py $db_endpoint
```
The output should return the prediction result like below
![Terraform Output](/image/reproduce/16.png)

Our frontend is now ready to accept requests

![Terraform Output](/image/reproduce/17.png)

### 7. Model Monitoring

After the user has sent the request will get log into the RDS Postgres database
we can then run the MLOP-MonitorML job to calculate the metric this job is scheduled to run daily to monitor the model performance 
Please go to prefect and run the job to produce data
![Terraform Output](/image/reproduce/18.png)

We can access the Grafana dashboard using endpoint 3000
Example http://xxx-xx-xxx-xxx-xx.ap-southeast-1.compute.amazonaws.com:3000/
![Terraform Output](/image/reproduce/19.png)

Log in using `admin` for both user and password

After login, we can monitor the model performance using the prepared dashboard metric to calculate daily
![Terraform Output](/image/reproduce/20.png)


### 8. Clean up

After done with the test you can run the below command to delete all created service 


```
make infra-down 
```
