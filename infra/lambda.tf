data "aws_ecr_repository" "my_repository" {
  name = "your-ecr-repo-name"  # Replace with your ECR repository name
}

resource "aws_lambda_function" "my_lambda" {
  function_name = "my-lambda-function"
  role          = aws_iam_role.lambda_role.arn
  handler       = "lambda_handler"  # Update with the actual handler name if different

  image_uri = "${data.aws_ecr_repository.my_repository.repository_url}:${data.aws_ecr_repository.my_repository.image_tag}"

  package_type = "Image"
  timeout      = 10
}

resource "aws_iam_role" "lambda_role" {
  name = "lambda-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole",
      Effect = "Allow",
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_policy_attachment" "lambda_policy_attachment" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"  # Basic Lambda execution policy
  roles      = [aws_iam_role.lambda_role.name]
}

# If you need to provide additional permissions to your Lambda function, attach custom policies here.

# Outputs
output "lambda_function_name" {
  value = aws_lambda_function.my_lambda.function_name
}

output "lambda_function_arn" {
  value = aws_lambda_function.my_lambda.arn
}
