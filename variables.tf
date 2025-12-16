variable "aws_region" {
  description = "AWS region where resources will be created"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name (e.g., dev, staging, production)"
  type        = string
  default     = "production"
}

variable "bucket_name" {
  description = "Name of the S3 bucket for media assets"
  type        = string
}

variable "days_to_transition_ia" {
  description = "Number of days after which objects transition to Standard-IA"
  type        = number
  default     = 30
}

variable "enable_versioning" {
  description = "Enable versioning for the S3 bucket"
  type        = bool
  default     = true
}

variable "additional_tags" {
  description = "Additional tags to apply to resources"
  type        = map(string)
  default     = {}
}

variable "force_destroy" {
  description = "Allow Terraform to destroy bucket even if it contains objects (use with caution)"
  type        = bool
  default     = false
}
