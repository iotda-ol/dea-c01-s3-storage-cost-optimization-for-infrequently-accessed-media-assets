# S3 Bucket for High-Resolution Media Assets
resource "aws_s3_bucket" "media_assets" {
  bucket        = var.bucket_name
  force_destroy = var.force_destroy

  tags = merge(
    {
      Name        = var.bucket_name
      Purpose     = "Media Asset Storage with Cost Optimization"
      StorageType = "High-Resolution Media"
    },
    var.additional_tags
  )
}

# Enable Versioning
resource "aws_s3_bucket_versioning" "media_assets" {
  bucket = aws_s3_bucket.media_assets.id

  versioning_configuration {
    status = var.enable_versioning ? "Enabled" : "Disabled"
  }
}

# Server-Side Encryption Configuration (AES-256)
resource "aws_s3_bucket_server_side_encryption_configuration" "media_assets" {
  bucket = aws_s3_bucket.media_assets.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
    bucket_key_enabled = true
  }
}

# Block Public Access
resource "aws_s3_bucket_public_access_block" "media_assets" {
  bucket = aws_s3_bucket.media_assets.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Lifecycle Policy: Transition to Standard-IA after 30 days
resource "aws_s3_bucket_lifecycle_configuration" "media_assets" {
  bucket = aws_s3_bucket.media_assets.id

  rule {
    id     = "transition-to-standard-ia"
    status = "Enabled"

    # Apply to all objects in the bucket
    filter {
      prefix = ""
    }

    transition {
      days          = var.days_to_transition_ia
      storage_class = "STANDARD_IA"
    }

    # Transition noncurrent versions to Standard-IA after 30 days
    noncurrent_version_transition {
      noncurrent_days = var.days_to_transition_ia
      storage_class   = "STANDARD_IA"
    }
  }

  rule {
    id     = "delete-old-noncurrent-versions"
    status = "Enabled"

    filter {
      prefix = ""
    }

    # Delete noncurrent versions after 90 days to reduce costs
    noncurrent_version_expiration {
      noncurrent_days = 90
    }

    # Abort incomplete multipart uploads after 7 days
    abort_incomplete_multipart_upload {
      days_after_initiation = 7
    }
  }
}

# Intelligent-Tiering configuration for additional optimization (optional)
# NOTE: This is commented out by default to avoid conflicts with the explicit
# lifecycle policy above. Intelligent-Tiering and explicit lifecycle rules can
# compete with each other. Use Intelligent-Tiering if you have unpredictable
# access patterns and want fully automated optimization. Otherwise, rely on the
# explicit lifecycle policy for predictable transitions.
#
# To enable Intelligent-Tiering, uncomment the resource below and comment out
# or remove the lifecycle configuration resource above.
#
# resource "aws_s3_bucket_intelligent_tiering_configuration" "media_assets" {
#   bucket = aws_s3_bucket.media_assets.id
#   name   = "EntireBucket"
#
#   status = "Enabled"
#
#   # Archive access tier - move objects not accessed for 90 days
#   tiering {
#     access_tier = "ARCHIVE_ACCESS"
#     days        = 90
#   }
#
#   # Deep archive access tier - move objects not accessed for 180 days
#   tiering {
#     access_tier = "DEEP_ARCHIVE_ACCESS"
#     days        = 180
#   }
# }
