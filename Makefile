include .env

MLFLOW_URI=$(shell docker inspect   -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}'  mlop_project-mlserver-1)
DBS_ENDPOINT=$(shell terraform output -state=infra/terraform.tfstate instance_dns_name)
AWS_DB_ML=$(shell terraform output -state=infra/terraform.tfstate rds_endpoint_ml | tr -d ':5432')
AWS_DB_MONITOR=$(shell terraform output -state=infra/terraform.tfstate rds_endpoint_moni | tr -d ':5432')

# AWS command
awssetup:
	aws configure

s3create:
	aws s3 mb s3://${S3_BUCKET}

s3list:
	#'----------------------'
	#'All Bucket List:'
	aws s3 ls 
	#'----------------------'
	#'All Item in ${S3_BUCKET}:'
	aws s3 ls ${S3_BUCKET}
	#'----------------------'

s3delete:
	aws s3 rb s3://${S3_BUCKET} --force
	aws s3 rb s3://${S3_BUCKET_DATA} --force

# Docker 
dockerupmlserver:
	docker-compose --profile mlflow up --detach 

dockerupagent:
	DBS_ENDPOINT=$(DBS_ENDPOINT) AWS_DB_ML=$(AWS_DB_ML) AWS_DB_MONITOR=$(AWS_DB_MONITOR) MLFLOW_URI="http://$(MLFLOW_URI):5000" docker-compose --profile mlflow-agent up --detach 

dockerupml:
	make dockerupmlserver
	make dockerupagent
	
dockerupweb:
	docker-compose --profile webapp up --detach 

dockerupmoni:
	docker-compose --profile monitor up --detach 

dockerdown:
	docker-compose down --remove-orphans

dockerdownweb:
	docker-compose -f docker-compose.yml --profile webapp down

dockerdownmoni:
	docker-compose -f docker-compose.yml --profile monitor down

dockerdownml:
	docker-compose -f docker-compose.yml --profile mlflow down
	docker-compose -f docker-compose.yml --profile mlflow-agent down

dockercreate-web:
	docker build -f dockerimage/webapp.dockerfile -t webapp .
	
dockercreate-back:
	docker build -f dockerimage/sqlalchemy.dockerfile -t mlflow .
	docker build --build-arg Prefect_Workspace=${Prefect_Workspace} --build-arg Prefect_API_KEY=${Prefect_API_KEY} -f dockerimage/prefect.dockerfile -t python_prefect_agent .

dockerprune:
	docker system prune --force

# Terraform
infra-setup:
	terraform -chdir=./infra init 
	terraform -chdir=./infra plan -var-file=variables.tfvars

infra-down:
	terraform -chdir=./infra destroy -var-file=variables.tfvars -auto-approve

infra-create:
	terraform -chdir=./infra apply -var-file=variables.tfvars -auto-approve

infra-prep:
	python infra/code/createtable.py ${DB_NAME_MONI} ${AWS_USER_DB} ${AWS_PASS_DB} ${AWS_DB_MONITOR} 5432

infra-key:
	terraform output -raw -state=infra/terraform.tfstate private_key_pem > key/private.pem
	terraform output -raw -state=infra/terraform.tfstate public_key_openssh > key/public.txt
	
infra-output:
	terraform output -state=infra/terraform.tfstate -json > output.json
	python code/output.py
# vm
vm-connect:
	ssh -i key/private.pem ubuntu@${DBS_ENDPOINT}
vm-setup:
	mkdir mlproject
vm-copy:
	scp -i key/private.pem -r ./requirement ubuntu@${DBS_ENDPOINT}:/home/ubuntu/mlproject/requirement
	scp -i key/private.pem -r ./code ubuntu@${DBS_ENDPOINT}:/home/ubuntu/mlproject/code
	scp -i key/private.pem -r ./dockerimage ubuntu@${DBS_ENDPOINT}:/home/ubuntu/mlproject/dockerimage
	scp -i key/private.pem -r ./.env ubuntu@${DBS_ENDPOINT}:/home/ubuntu/mlproject/.env
	scp -i key/private.pem -r ./docker-compose.yml ubuntu@${DBS_ENDPOINT}:/home/ubuntu/mlproject/docker-compose.yml
	scp -i key/private.pem -r ./Makefile ubuntu@${DBS_ENDPOINT}:/home/ubuntu/mlproject/Makefile

# Script
train:
	python code/train.py

testweb:
	python code/test/web_test.py

# Other
# https://www.kaggle.com/datasets/henriqueyamahata/bank-marketing?select=bank-additional-full.csv
# Prerequisite: Have an kaggle account + key.json download < Kaggle key might expire need to regen first
getdata:
	kaggle datasets download -d henriqueyamahata/bank-marketing -p data --unzip --force
	python code/genmeta.py
	aws s3 mb s3://${S3_BUCKET_DATA}
	aws s3 cp data/bank-additional-full.csv s3://${S3_BUCKET_DATA}

mlup:
	mlflow server --backend-store-uri postgresql://root:root@127.0.0.1:5432/${DB_NAME} --default-artifact-root s3://${S3_BUCKET}

prefectlogin:
	prefect cloud login --key ${Prefect_API_KEY} --workspace ${Prefect_Workspace}

# Need to execute manual
docker-awspush:
	repo_url=$(echo $(terraform output -state=infra/terraform.tfstate ecr_repo_url) | tr -d '"')
	regis_url=$(echo $(terraform output -state=infra/terraform.tfstate ecr_registry_url) | tr -d '"')
	region="ap-southeast-1"
	aws ecr get-login-password --region ${region} | docker login --username AWS --password-stdin "${regis_url}.dkr.ecr.${region}.amazonaws.com"
	docker tag webapp:latest ${repo_url}:webapp
	docker push ${repo_url}:webapp

db-endpiont:
	terraform output -state=infra/terraform.tfstate rds_endpoint_ml
	terraform output -state=infra/terraform.tfstate rds_endpoint_moni

