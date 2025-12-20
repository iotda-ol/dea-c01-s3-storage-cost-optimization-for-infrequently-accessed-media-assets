#!/bin/bash

# Deployment script for Terraform

set -e

echo "====================================="
echo "S3 Lifecycle Policy - Terraform"
echo "====================================="
echo ""

# Change to Terraform directory
cd deployment/terraform

# Default values
BUCKET_NAME=""
REGION="us-east-1"
STANDARD_IA_DAYS=30
GLACIER_DAYS=90
EXPIRATION_DAYS=365
ACTION="plan"

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --bucket-name)
      BUCKET_NAME="$2"
      shift 2
      ;;
    --region)
      REGION="$2"
      shift 2
      ;;
    --standard-ia-days)
      STANDARD_IA_DAYS="$2"
      shift 2
      ;;
    --glacier-days)
      GLACIER_DAYS="$2"
      shift 2
      ;;
    --expiration-days)
      EXPIRATION_DAYS="$2"
      shift 2
      ;;
    --action)
      ACTION="$2"
      shift 2
      ;;
    --help)
      echo "Usage: $0 [OPTIONS]"
      echo ""
      echo "Options:"
      echo "  --bucket-name NAME          S3 bucket name (required)"
      echo "  --region REGION             AWS region (default: us-east-1)"
      echo "  --standard-ia-days DAYS     Days before Standard-IA transition (default: 30)"
      echo "  --glacier-days DAYS         Days before Glacier transition (default: 90)"
      echo "  --expiration-days DAYS      Days before expiration (default: 365, 0=no expiration)"
      echo "  --action ACTION             Terraform action: plan, apply, or destroy (default: plan)"
      echo "  --help                      Show this help message"
      cd ../..
      exit 0
      ;;
    *)
      echo "Unknown option: $1"
      cd ../..
      exit 1
      ;;
  esac
done

# Validate required parameters
if [ -z "$BUCKET_NAME" ]; then
    echo "Error: --bucket-name is required"
    echo "Run with --help for usage information"
    cd ../..
    exit 1
fi

echo "Configuration:"
echo "  Bucket Name: $BUCKET_NAME"
echo "  Region: $REGION"
echo "  Standard-IA Days: $STANDARD_IA_DAYS"
echo "  Glacier Days: $GLACIER_DAYS"
echo "  Expiration Days: $EXPIRATION_DAYS"
echo "  Action: $ACTION"
echo ""

# Initialize Terraform
echo "Initializing Terraform..."
terraform init

# Run Terraform action
case $ACTION in
  plan)
    echo ""
    echo "Running Terraform plan..."
    terraform plan \
      -var="bucket_name=$BUCKET_NAME" \
      -var="aws_region=$REGION" \
      -var="standard_ia_transition_days=$STANDARD_IA_DAYS" \
      -var="glacier_transition_days=$GLACIER_DAYS" \
      -var="expiration_days=$EXPIRATION_DAYS"
    ;;
  apply)
    echo ""
    echo "Applying Terraform configuration..."
    terraform apply \
      -var="bucket_name=$BUCKET_NAME" \
      -var="aws_region=$REGION" \
      -var="standard_ia_transition_days=$STANDARD_IA_DAYS" \
      -var="glacier_transition_days=$GLACIER_DAYS" \
      -var="expiration_days=$EXPIRATION_DAYS" \
      -auto-approve
    echo ""
    echo "Deployment completed!"
    ;;
  destroy)
    echo ""
    echo "Destroying Terraform resources..."
    terraform destroy \
      -var="bucket_name=$BUCKET_NAME" \
      -var="aws_region=$REGION" \
      -var="standard_ia_transition_days=$STANDARD_IA_DAYS" \
      -var="glacier_transition_days=$GLACIER_DAYS" \
      -var="expiration_days=$EXPIRATION_DAYS" \
      -auto-approve
    echo ""
    echo "Resources destroyed!"
    ;;
  *)
    echo "Error: Unknown action '$ACTION'. Must be 'plan', 'apply', or 'destroy'."
    cd ../..
    exit 1
    ;;
esac

cd ../..
