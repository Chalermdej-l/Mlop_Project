
provider "aws" {
  region = var.aws_region
}


# ride_events
module "db" {
  source = "../infra/modules/db"   
  db_intance_type      = var.db_intance_type
  db_identifier_moni   = var.db_identifier_moni
  db_name_moni         = var.db_name_moni
  db_username          = var.db_username
  db_password          = var.db_password
  aws_region_sn        = var.aws_region_sn
  aws_region_sn2       = var.aws_region_sn2
  db_name_ml           = var.db_name_ml
  db_identifier_ml     = var.db_identifier_ml
}

module "lambda" {
  source = "./modules/lambda"   
  S3_BUCKET           = var.S3_BUCKET
  db_name_moni        = var.db_name_moni
  db_username         = var.db_username
  db_password         = var.db_password
  region              = var.aws_region
  aws_db_monitor      = substr(module.db.AWS_DB_MONITOR, 0, length(module.db.AWS_DB_MONITOR) - 5)
  repository_url      = module.ecr.ecr_repo_url
  registry_id         = module.ecr.ecr_registry_url
}


module "gateway" {
  source = "./modules/gateway"     
  lambda_uri = module.lambda.lambda_function_invokearn
}

module "ecr" {
  source = "../infra/modules/ecr"     
}

module "ec2" {
  source = "../infra/modules/ec2"   
}


output "private_key_pem" {
  value = module.ec2.private_key_pem
  sensitive = true
}

output "public_key_openssh" {
  value = module.ec2.public_key_openssh
  sensitive = true
}
output "DBS_ENDPOINT" {
  value = module.ec2.DBS_ENDPOINT
}

output "lambda_function_arn" {
  value = module.lambda.lambda_function_arn
}

output "ecr_registry_url" {
  value = module.ecr.ecr_registry_url
}
output "ecr_repo_url" {
  value = module.ecr.ecr_repo_url
}
output "AWS_DB_ML" {
  value = module.db.AWS_DB_ML
}
output "AWS_DB_MONITOR" {
  value = module.db.AWS_DB_MONITOR
}

output "api_gateway_endpoint" {
  value = module.gateway.api_gateway_endpoint
}
