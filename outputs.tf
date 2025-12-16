output "bucket_id" {
  description = "The name of the S3 bucket"
  value       = aws_s3_bucket.media_assets.id
}

output "bucket_arn" {
  description = "The ARN of the S3 bucket"
  value       = aws_s3_bucket.media_assets.arn
}

output "bucket_domain_name" {
  description = "The bucket domain name"
  value       = aws_s3_bucket.media_assets.bucket_domain_name
}

output "bucket_regional_domain_name" {
  description = "The bucket region-specific domain name"
  value       = aws_s3_bucket.media_assets.bucket_regional_domain_name
}

output "lifecycle_rules" {
  description = "Summary of lifecycle rules applied"
  value = {
    transition_to_standard_ia_days = var.days_to_transition_ia
    storage_class                  = "STANDARD_IA"
    noncurrent_version_expiration  = "90 days"
  }
}

output "encryption_status" {
  description = "Encryption configuration status"
  value       = "AES256 server-side encryption enabled"
}

output "versioning_status" {
  description = "Bucket versioning status"
  value       = var.enable_versioning ? "Enabled" : "Disabled"
}

output "cost_optimization_summary" {
  description = "Cost optimization strategy summary"
  value = {
    initial_storage_class  = "S3 Standard"
    transition_after_days  = var.days_to_transition_ia
    target_storage_class   = "S3 Standard-IA"
    access_latency         = "Millisecond latency maintained"
    estimated_cost_savings = "Up to 46% storage cost reduction after transition"
  }
}
