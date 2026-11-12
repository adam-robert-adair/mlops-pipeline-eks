output "data_bucket" {
  value = aws_s3_bucket.data.bucket
}

output "artifact_bucket" {
  value = aws_s3_bucket.artifacts.bucket
}

output "pipeline_ecr_repository_url" {
  value = aws_ecr_repository.pipeline.repository_url
}

output "serving_ecr_repository_url" {
  value = aws_ecr_repository.serving.repository_url
}

output "mlflow_irsa_role_arn" {
  value = aws_iam_role.mlflow_irsa.arn
}

output "argo_irsa_role_arn" {
  value = aws_iam_role.argo_irsa.arn
}
