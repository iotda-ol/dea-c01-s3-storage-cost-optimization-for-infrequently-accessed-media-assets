#!/bin/bash

# Deployment script for CloudFormation template

set -e

echo "====================================="
echo "S3 Lifecycle Policy - CloudFormation"
echo "====================================="
echo ""

# Default values
BUCKET_NAME=""
REGION="us-east-1"
STACK_NAME="s3-media-asset-optimization"
STANDARD_IA_DAYS=30
GLACIER_DAYS=90
EXPIRATION_DAYS=365

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
    --stack-name)
      STACK_NAME="$2"
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
    --help)
      echo "Usage: $0 [OPTIONS]"
      echo ""
      echo "Options:"
      echo "  --bucket-name NAME          S3 bucket name (required)"
      echo "  --region REGION             AWS region (default: us-east-1)"
      echo "  --stack-name NAME           CloudFormation stack name"
      echo "  --standard-ia-days DAYS     Days before Standard-IA transition (default: 30)"
      echo "  --glacier-days DAYS         Days before Glacier transition (default: 90)"
      echo "  --expiration-days DAYS      Days before expiration (default: 365, 0=no expiration)"
      echo "  --help                      Show this help message"
      exit 0
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# Validate required parameters
if [ -z "$BUCKET_NAME" ]; then
    echo "Error: --bucket-name is required"
    echo "Run with --help for usage information"
    exit 1
fi

echo "Configuration:"
echo "  Bucket Name: $BUCKET_NAME"
echo "  Region: $REGION"
echo "  Stack Name: $STACK_NAME"
echo "  Standard-IA Days: $STANDARD_IA_DAYS"
echo "  Glacier Days: $GLACIER_DAYS"
echo "  Expiration Days: $EXPIRATION_DAYS"
echo ""

# Deploy CloudFormation stack
echo "Deploying CloudFormation stack..."

aws cloudformation deploy \
  --template-file deployment/cloudformation/s3-lifecycle-template.yaml \
  --stack-name "$STACK_NAME" \
  --region "$REGION" \
  --parameter-overrides \
    BucketName="$BUCKET_NAME" \
    StandardIATransitionDays="$STANDARD_IA_DAYS" \
    GlacierTransitionDays="$GLACIER_DAYS" \
    ExpirationDays="$EXPIRATION_DAYS" \
  --capabilities CAPABILITY_IAM

echo ""
echo "Deployment completed!"
echo ""
echo "Stack outputs:"
aws cloudformation describe-stacks \
  --stack-name "$STACK_NAME" \
  --region "$REGION" \
  --query 'Stacks[0].Outputs' \
  --output table
