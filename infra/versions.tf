terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    tls = {
      source  = "hashicorp/tls"
      version = "~> 4.0"
    }
  }

  # Create the bucket and DynamoDB table before `terraform init`:
  #   aws s3api create-bucket --bucket mlop-terraform-state --region ap-southeast-1
  #   aws dynamodb create-table --table-name mlop-terraform-locks \
  #     --attribute-definitions AttributeName=LockID,AttributeType=S \
  #     --key-schema AttributeName=LockID,KeyType=HASH \
  #     --billing-mode PAY_PER_REQUEST
  backend "s3" {
    bucket         = "mlop-terraform-state"
    key            = "mlop/terraform.tfstate"
    region         = "ap-southeast-1"
    dynamodb_table = "mlop-terraform-locks"
    encrypt        = true
  }
}
