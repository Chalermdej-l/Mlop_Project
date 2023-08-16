resource "aws_ecr_repository" "mlflow_repro" {
  name = "mlflow_repro"
}

output "ecr_repo_url" {
  value = aws_ecr_repository.mlflow_repro.repository_url
}

# Push Docker image to ECR after ECR repository is created
resource "null_resource" "push_image" {
  triggers = {
    ecr_repo_url = aws_ecr_repository.mlflow_repro.repository_url
  }

  depends_on = [aws_ecr_repository.mlflow_repro]

