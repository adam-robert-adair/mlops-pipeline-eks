variable "project" {
  type        = string
  description = "Project name prefix"
  default     = "mlops-pipeline-eks"
}

variable "environment" {
  type        = string
  description = "Environment name"
  default     = "dev"
}

variable "aws_region" {
  type        = string
  description = "AWS region"
  default     = "us-east-1"
}

variable "oidc_provider_arn" {
  type        = string
  description = "EKS OIDC provider ARN for IRSA trust"
}

variable "oidc_provider_url" {
  type        = string
  description = "EKS OIDC provider URL without https://"
}

variable "mlflow_namespace" {
  type        = string
  description = "Namespace that runs MLflow service account"
  default     = "mlops"
}

variable "mlflow_service_account" {
  type        = string
  description = "MLflow Kubernetes service account name"
  default     = "mlflow"
}

variable "argo_namespace" {
  type        = string
  description = "Namespace for Argo workflows"
  default     = "mlops"
}

variable "argo_service_account" {
  type        = string
  description = "Argo service account name"
  default     = "argo-workflow"
}

variable "budget_limit_usd" {
  type        = string
  description = "Monthly budget alert amount in USD"
  default     = "20"
}

variable "alert_email" {
  type        = string
  description = "Email for AWS budget notifications"
}
