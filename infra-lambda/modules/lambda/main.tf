resource "aws_lambda_function" "lambda_with_docker" {
  function_name = "Bank_Deposit_Prediction"
  role          = aws_iam_role.lambda_role.arn
  package_type  = "Image"
  image_uri = "${var.repository_url}:webapp"

  environment {
    variables = {
      RUN_ID          = "None" 
      EXPERIMENT_ID   = "1" 
      S3_BUCKET       = var.S3_BUCKET
      DB_NAME_GRAFANA = var.db_name_moni
      AWS_USER_DB     = var.db_username
      AWS_PASS_DB     = var.db_password
      AWS_DB_MONITOR  = var.aws_db_monitor
    }

}
}

resource "aws_iam_role" "lambda_role" {
  name = "lambda_role_for_ecr_access"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

output "lambda_function_arn" {
  value = aws_lambda_function.lambda_with_docker.arn
}

output "lambda_function_invokearn" {
  value = aws_lambda_function.lambda_with_docker.invoke_arn
}

