terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-east-1"
}

variable "bucket_name" {
  description = "Name of the S3 bucket for media assets"
  type        = string
  validation {
    condition     = can(regex("^[a-z0-9][a-z0-9.-]*[a-z0-9]$", var.bucket_name))
    error_message = "Bucket name must follow S3 naming conventions."
  }
}

variable "standard_ia_transition_days" {
  description = "Days before transitioning to Standard-IA"
  type        = number
  default     = 30
}

variable "glacier_transition_days" {
  description = "Days before transitioning to Glacier"
  type        = number
  default     = 90
}

variable "expiration_days" {
  description = "Days before object expiration (0 for no expiration)"
  type        = number
  default     = 365
}

resource "aws_s3_bucket" "media_assets" {
  bucket = var.bucket_name

  tags = {
    Name              = var.bucket_name
    Purpose           = "MediaAssetStorage"
    CostOptimization  = "Enabled"
  }
}

resource "aws_s3_bucket_versioning" "media_assets" {
  bucket = aws_s3_bucket.media_assets.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "media_assets" {
  bucket = aws_s3_bucket.media_assets.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "media_assets" {
  bucket = aws_s3_bucket.media_assets.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_lifecycle_configuration" "media_assets" {
  bucket = aws_s3_bucket.media_assets.id

  rule {
    id     = "MediaAssetCostOptimization"
    status = "Enabled"

    filter {
      prefix = "media/"
    }

    transition {
      days          = var.standard_ia_transition_days
      storage_class = "STANDARD_IA"
    }

    transition {
      days          = var.glacier_transition_days
      storage_class = "GLACIER"
    }

    dynamic "expiration" {
      for_each = var.expiration_days > 0 ? [1] : []
      content {
        days = var.expiration_days
      }
    }

    noncurrent_version_transition {
      noncurrent_days = 30
      storage_class   = "STANDARD_IA"
    }

    noncurrent_version_transition {
      noncurrent_days = 90
      storage_class   = "GLACIER"
    }

    noncurrent_version_expiration {
      noncurrent_days = 120
    }
  }
}

resource "aws_s3_bucket_policy" "media_assets" {
  bucket = aws_s3_bucket.media_assets.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "DenyInsecureTransport"
        Effect    = "Deny"
        Principal = "*"
        Action    = "s3:*"
        Resource = [
          aws_s3_bucket.media_assets.arn,
          "${aws_s3_bucket.media_assets.arn}/*"
        ]
        Condition = {
          Bool = {
            "aws:SecureTransport" = "false"
          }
        }
      }
    ]
  })
}

output "bucket_name" {
  description = "Name of the S3 bucket"
  value       = aws_s3_bucket.media_assets.id
}

output "bucket_arn" {
  description = "ARN of the S3 bucket"
  value       = aws_s3_bucket.media_assets.arn
}

output "bucket_domain_name" {
  description = "Domain name of the S3 bucket"
  value       = aws_s3_bucket.media_assets.bucket_domain_name
}
