include .env

# AWS command
awssetup:
	export ACCESS_KEY=${ACCESS_KEY}
	export ACCESS_SCRECT=${ACCESS_SCRECT}
	export AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION}

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

# Docker 
dockerupml:
	docker-compose --profile mlflow up --detach 

dockerupweb:
	docker-compose --profile webapp up --detach 

dockerupmoni:
	docker-compose --profile monitor up --detach 

dockerdown:
	docker-compose down --remove-orphans

dockerdownweb:
	docker compose -f docker-compose.yml --profile webapp down

dockerdownml:
	docker compose -f docker-compose.yml --profile webapp down

dockercreate:
	# docker build -f dockerfile -t mlflow .
	docker build -f dockerimage/sqlalchemy.dockerfile -t mlflow .
	docker build -f dockerimage/webapp.dockerfile -t webapp .

dockerprune:
	docker system prune --force

# Script
train:
	python code/train.py

testweb:
	python test/testweb.py

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
