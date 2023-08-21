include .env

MLFLOW_URI=$(shell docker inspect   -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}'  mlproject_mlserver_1)
API_URL=$(shell terraform output -state=infra/terraform.tfstate DBS_ENDPOINT)

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
	MLFLOW_URI="http://$(MLFLOW_URI):5000" docker-compose --profile mlflow-agent up --detach 

dockerupml:
	make dockerupmlserver
	make dockerupagent

dockerup:
	make dockerupml
	docker-compose --profile webapp up --detach 
	docker-compose --profile monitor up --detach 
	
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

dockercreate:
	docker build -f dockerimage/sqlalchemy.dockerfile -t mlflow .
	docker build --build-arg Prefect_Workspace=${Prefect_Workspace} --build-arg Prefect_API_KEY=${Prefect_API_KEY} -f dockerimage/prefect.dockerfile -t python_prefect_agent .
	docker build -f dockerimage/webapp.dockerfile -t webapp .

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
	terraform output -raw -state=infra/terraform.tfstate private_key_pem > key/private.pem
	terraform output -raw -state=infra/terraform.tfstate public_key_openssh > key/public.txt
	terraform output -state=infra/terraform.tfstate -json > output.json
	python code/output.py
# vm
vm-connect:
	ssh -i key/private.pem ubuntu@${DBS_ENDPOINT}

vm-copy:
	scp -i key/private.pem -r ./requirement ubuntu@${DBS_ENDPOINT}:/home/ubuntu/mlproject/requirement
	scp -i key/private.pem -r ./code ubuntu@${DBS_ENDPOINT}:/home/ubuntu/mlproject/code
	scp -i key/private.pem -r ./dockerimage ubuntu@${DBS_ENDPOINT}:/home/ubuntu/mlproject/dockerimage
	scp -i key/private.pem -r ./.env ubuntu@${DBS_ENDPOINT}:/home/ubuntu/mlproject/.env
	scp -i key/private.pem -r ./docker-compose.yml ubuntu@${DBS_ENDPOINT}:/home/ubuntu/mlproject/docker-compose.yml
	scp -i key/private.pem -r ./Makefile ubuntu@${DBS_ENDPOINT}:/home/ubuntu/mlproject/Makefile
	scp -i key/private.pem -r ./config ubuntu@${DBS_ENDPOINT}:/home/ubuntu/mlproject/config

vm-setup:
	sudo apt-get update -y
	sudo apt install docker.io -y
	sudo chmod 666 /var/run/docker.sock

# Script
testapi:
	python code/api_test.py '$(API_URL)'

getdata:
	kaggle datasets download -d henriqueyamahata/bank-marketing -p data --unzip --force
	python code/genmeta.py
	aws s3 mb s3://${S3_BUCKET_DATA}
	aws s3 cp data/bank-additional-full.csv s3://${S3_BUCKET_DATA}

deploy-api:
	db_endpoint='ec2-13-229-243-71.ap-southeast-1.compute.amazonaws.com'
	model_id=$(python code/deploymodel.py "$db_endpoint")
	ssh -i key/private.pem ubuntu@${db_endpoint} " 
	cd mlproject
	RUN_ID=${model_id} docker-compose --profile webapp up --detac
	"
