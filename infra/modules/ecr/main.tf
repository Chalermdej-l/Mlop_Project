resource "aws_ecr_repository" "mlflow_repro" {
  name = "mlflow_repro"
}

output "ecr_repo_url" {
  value = aws_ecr_repository.mlflow_repro.repository_url
}

output "ecr_registry_url" {
  value = aws_ecr_repository.mlflow_repro.registry_id
}
