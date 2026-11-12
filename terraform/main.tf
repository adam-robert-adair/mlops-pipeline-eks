provider "aws" {
  region = var.aws_region
}

data "aws_caller_identity" "current" {}

data "aws_iam_policy_document" "mlflow_irsa_assume_role" {
  statement {
    actions = ["sts:AssumeRoleWithWebIdentity"]

    condition {
      test     = "StringEquals"
      variable = "${var.oidc_provider_url}:sub"
      values   = ["system:serviceaccount:${var.mlflow_namespace}:${var.mlflow_service_account}"]
    }

    principals {
      type        = "Federated"
      identifiers = [var.oidc_provider_arn]
    }
  }
}

data "aws_iam_policy_document" "argo_irsa_assume_role" {
  statement {
    actions = ["sts:AssumeRoleWithWebIdentity"]

    condition {
      test     = "StringEquals"
      variable = "${var.oidc_provider_url}:sub"
      values   = ["system:serviceaccount:${var.argo_namespace}:${var.argo_service_account}"]
    }

    principals {
      type        = "Federated"
      identifiers = [var.oidc_provider_arn]
    }
  }
}

locals {
  name_prefix = "${var.project}-${var.environment}"
}

resource "aws_s3_bucket" "data" {
  bucket = "${local.name_prefix}-data"
}

resource "aws_s3_bucket_versioning" "data" {
  bucket = aws_s3_bucket.data.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "data" {
  bucket = aws_s3_bucket.data.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "data" {
  bucket                  = aws_s3_bucket.data.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket" "artifacts" {
  bucket = "${local.name_prefix}-artifacts"
}

resource "aws_s3_bucket_versioning" "artifacts" {
  bucket = aws_s3_bucket.artifacts.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "artifacts" {
  bucket = aws_s3_bucket.artifacts.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "artifacts" {
  bucket                  = aws_s3_bucket.artifacts.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_ecr_repository" "pipeline" {
  name                 = "${local.name_prefix}-pipeline"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_ecr_repository" "serving" {
  name                 = "${local.name_prefix}-serving"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_iam_role" "mlflow_irsa" {
  name               = "${local.name_prefix}-mlflow-irsa"
  assume_role_policy = data.aws_iam_policy_document.mlflow_irsa_assume_role.json
}

resource "aws_iam_role" "argo_irsa" {
  name               = "${local.name_prefix}-argo-irsa"
  assume_role_policy = data.aws_iam_policy_document.argo_irsa_assume_role.json
}

data "aws_iam_policy_document" "mlflow_s3_access" {
  statement {
    actions = ["s3:ListBucket"]
    resources = [
      aws_s3_bucket.artifacts.arn,
      aws_s3_bucket.data.arn,
    ]
  }

  statement {
    actions = ["s3:GetObject", "s3:PutObject", "s3:DeleteObject"]
    resources = [
      "${aws_s3_bucket.artifacts.arn}/*",
      "${aws_s3_bucket.data.arn}/*",
    ]
  }
}

resource "aws_iam_policy" "mlflow_s3_access" {
  name   = "${local.name_prefix}-mlflow-s3"
  policy = data.aws_iam_policy_document.mlflow_s3_access.json
}

resource "aws_iam_role_policy_attachment" "mlflow_s3_access" {
  role       = aws_iam_role.mlflow_irsa.name
  policy_arn = aws_iam_policy.mlflow_s3_access.arn
}

resource "aws_budgets_budget" "monthly" {
  name              = "${local.name_prefix}-budget"
  budget_type       = "COST"
  limit_amount      = var.budget_limit_usd
  limit_unit        = "USD"
  time_period_start = "2024-01-01_00:00"
  time_unit         = "MONTHLY"

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 80
    threshold_type             = "PERCENTAGE"
    notification_type          = "ACTUAL"
    subscriber_email_addresses = [var.alert_email]
  }
}
