# Deployment Guide

This guide provides step-by-step instructions for deploying the S3 storage optimization solution.

## Prerequisites

Before you begin, ensure you have:

1. **AWS Account** with appropriate permissions
   - S3 full access (or at minimum: `s3:CreateBucket`, `s3:PutBucketPolicy`, `s3:PutLifecycleConfiguration`, etc.)
   - IAM permissions to create/manage resources

2. **Terraform** installed (version >= 1.0)
   ```bash
   # Check if Terraform is installed
   terraform version
   
   # If not installed, download from:
   # https://www.terraform.io/downloads.html
   ```

3. **AWS CLI** configured with credentials
   ```bash
   # Verify AWS CLI configuration
   aws sts get-caller-identity
   
   # Configure if needed
   aws configure
   ```

4. **Git** (for cloning the repository)

## Step-by-Step Deployment

### Step 1: Clone the Repository

```bash
git clone https://github.com/iotda-ol/dea-c01-s3-storage-cost-optimization-for-infrequently-accessed-media-assets.git
cd dea-c01-s3-storage-cost-optimization-for-infrequently-accessed-media-assets
```

### Step 2: Create Configuration File

```bash
# Copy the example configuration
cp terraform.tfvars.example terraform.tfvars

# Edit the configuration with your values
nano terraform.tfvars  # or use your preferred editor
```

**Required Configuration:**

```hcl
# terraform.tfvars

# Choose your AWS region
aws_region = "us-east-1"

# Set your environment
environment = "production"  # or "staging", "dev", etc.

# IMPORTANT: Must be globally unique across ALL AWS accounts
bucket_name = "your-company-media-assets-20231216"

# Transition period (days)
days_to_transition_ia = 30

# Enable versioning for data protection
enable_versioning = true

# Add custom tags for cost allocation
additional_tags = {
  CostCenter = "Marketing"
  Team       = "Digital-Media"
  Application = "Media-Asset-Management"
}

# CAUTION: Only set to true for non-production testing
force_destroy = false
```

### Step 3: Initialize Terraform

```bash
# Initialize Terraform and download required providers
terraform init
```

**Expected Output:**
```
Initializing the backend...
Initializing provider plugins...
- Finding hashicorp/aws versions matching "~> 5.0"...
- Installing hashicorp/aws v5.x.x...

Terraform has been successfully initialized!
```

### Step 4: Validate Configuration

```bash
# Validate the configuration syntax
terraform validate

# Format the Terraform files (optional but recommended)
terraform fmt
```

### Step 5: Review the Execution Plan

```bash
# Generate and show an execution plan
terraform plan
```

**Review the plan carefully:**
- Check that the bucket name is correct
- Verify the lifecycle rules
- Confirm the encryption settings
- Review the tags

**Expected Resources to be Created:**
```
Plan: 6 to add, 0 to change, 0 to destroy.

Resources:
  + aws_s3_bucket.media_assets
  + aws_s3_bucket_versioning.media_assets
  + aws_s3_bucket_server_side_encryption_configuration.media_assets
  + aws_s3_bucket_public_access_block.media_assets
  + aws_s3_bucket_lifecycle_configuration.media_assets
  + aws_s3_bucket_intelligent_tiering_configuration.media_assets
```

### Step 6: Deploy the Infrastructure

```bash
# Apply the configuration
terraform apply
```

You will be prompted to confirm:
```
Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes
```

Type `yes` and press Enter.

**Expected Output:**
```
Apply complete! Resources: 6 added, 0 changed, 0 destroyed.

Outputs:
bucket_id = "your-company-media-assets-20231216"
bucket_arn = "arn:aws:s3:::your-company-media-assets-20231216"
...
```

### Step 7: Verify Deployment

#### A. View Terraform Outputs

```bash
# Display all outputs
terraform output

# Display specific output
terraform output bucket_id
terraform output cost_optimization_summary
```

#### B. Verify in AWS Console

1. Navigate to [AWS S3 Console](https://s3.console.aws.amazon.com/s3/)
2. Find your bucket
3. Click on the bucket name
4. Check the following tabs:

   **Properties Tab:**
   - ✅ Default encryption: Enabled (SSE-S3)
   - ✅ Versioning: Enabled
   - ✅ Bucket Key: Enabled

   **Management Tab:**
   - ✅ Lifecycle rules: 2 rules configured
     - Rule 1: `transition-to-standard-ia`
     - Rule 2: `delete-old-noncurrent-versions`

   **Permissions Tab:**
   - ✅ Block public access: All options enabled

#### C. Test with AWS CLI

```bash
# Upload a test file
echo "Test content" > test-file.txt
aws s3 cp test-file.txt s3://your-bucket-name/

# Verify the upload
aws s3 ls s3://your-bucket-name/

# Check object metadata
aws s3api head-object \
  --bucket your-bucket-name \
  --key test-file.txt

# Expected output should show:
# - ServerSideEncryption: AES256
# - StorageClass: STANDARD (initially)
```

### Step 8: Verify Lifecycle Policy (Optional)

```bash
# Get the lifecycle configuration
aws s3api get-bucket-lifecycle-configuration \
  --bucket your-bucket-name

# Output shows the configured rules in JSON format
```

## Post-Deployment Tasks

### 1. Set Up Monitoring

Configure CloudWatch alarms for:
- Bucket size metrics
- Request metrics
- 4xx/5xx error rates

```bash
# Enable request metrics (optional, has cost)
aws s3api put-bucket-metrics-configuration \
  --bucket your-bucket-name \
  --id EntireBucket \
  --metrics-configuration Id=EntireBucket,Filter={}
```

### 2. Configure Access Policies (If Needed)

If applications need to access the bucket, create IAM policies:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject"
      ],
      "Resource": "arn:aws:s3:::your-bucket-name/*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:ListBucket"
      ],
      "Resource": "arn:aws:s3:::your-bucket-name"
    }
  ]
}
```

### 3. Set Up Cost Tracking

1. Enable **Cost Allocation Tags** in AWS Billing Console
   - Navigate to Billing → Cost Allocation Tags
   - Activate your custom tags

2. Create **AWS Budgets** for S3 costs
   - Set monthly budget threshold
   - Configure email alerts

3. Use **AWS Cost Explorer**
   - Filter by S3 service and bucket tags
   - Create custom reports

### 4. Enable S3 Storage Class Analysis (Recommended)

```bash
aws s3api put-bucket-analytics-configuration \
  --bucket your-bucket-name \
  --id StorageAnalytics \
  --analytics-configuration '{"Id":"StorageAnalytics","StorageClassAnalysis":{"DataExport":{"OutputSchemaVersion":"V_1","Destination":{"S3BucketDestination":{"Format":"CSV","Bucket":"arn:aws:s3:::your-bucket-name","Prefix":"storage-analysis/"}}}}}'
```

This provides recommendations on optimal lifecycle policies based on actual access patterns.

## Updating the Infrastructure

### Modify Configuration

1. Edit `terraform.tfvars`:
   ```bash
   nano terraform.tfvars
   ```

2. Change desired values (e.g., increase transition days):
   ```hcl
   days_to_transition_ia = 60  # Changed from 30 to 60
   ```

3. Apply changes:
   ```bash
   terraform plan   # Review changes
   terraform apply  # Apply changes
   ```

### Common Updates

**Change Transition Period:**
```hcl
# In terraform.tfvars
days_to_transition_ia = 45
```

**Add Custom Tags:**
```hcl
additional_tags = {
  CostCenter = "IT"
  Project    = "MediaCDN"
  Owner      = "john.doe@example.com"
}
```

**Disable Versioning (Not Recommended for Production):**
```hcl
enable_versioning = false
```

## Disaster Recovery and Backup

### State File Backup

Terraform state files are critical. Consider:

1. **Local State Backup:**
   ```bash
   # Backup state file
   cp terraform.tfstate terraform.tfstate.backup
   ```

2. **Remote State Backend (Recommended):**
   
   Add to `provider.tf`:
   ```hcl
   terraform {
     backend "s3" {
       bucket         = "your-terraform-state-bucket"
       key            = "s3-media-assets/terraform.tfstate"
       region         = "us-east-1"
       encrypt        = true
       dynamodb_table = "terraform-lock"
     }
   }
   ```

### S3 Bucket Backup Strategy

For critical media assets:
- Enable **Cross-Region Replication (CRR)**
- Use **S3 Versioning** (already enabled)
- Consider **AWS Backup** for additional protection

## Decommissioning

### Option 1: Preserve Data (Recommended)

```bash
# Disable lifecycle policies first
aws s3api delete-bucket-lifecycle \
  --bucket your-bucket-name

# Download all objects
aws s3 sync s3://your-bucket-name/ ./backup/

# Then destroy infrastructure
terraform destroy
```

### Option 2: Complete Removal

```bash
# WARNING: This deletes all objects and the bucket
terraform destroy

# Confirm when prompted
```

**Note:** If `force_destroy = false` (default), you must empty the bucket manually before destroying.

## Troubleshooting

### Issue 1: Bucket Name Already Exists

**Error:**
```
Error: creating Amazon S3 Bucket: BucketAlreadyExists
```

**Solution:**
Change `bucket_name` in `terraform.tfvars` to a unique value.

### Issue 2: Insufficient Permissions

**Error:**
```
Error: AccessDenied: Access Denied
```

**Solution:**
Ensure your AWS credentials have appropriate S3 permissions:
```bash
# Check current identity
aws sts get-caller-identity

# Attach required policy to your IAM user/role
```

### Issue 3: Lifecycle Policy Not Applying

**Problem:** Objects not transitioning after specified days.

**Solution:**
- Lifecycle transitions occur at midnight UTC
- Check object creation date vs transition date
- Verify lifecycle rule is enabled in AWS Console
- Objects smaller than 128 KB may not transition to Standard-IA

### Issue 4: Terraform State Locked

**Error:**
```
Error: Error acquiring the state lock
```

**Solution:**
```bash
# Wait for other operations to complete, or
# Force unlock (use with caution)
terraform force-unlock <LOCK_ID>
```

### Issue 5: Cannot Delete Non-Empty Bucket

**Error:**
```
Error: deleting Amazon S3 Bucket: BucketNotEmpty
```

**Solution:**
Either:
- Set `force_destroy = true` in `terraform.tfvars` and re-apply
- Or manually empty the bucket:
  ```bash
  aws s3 rm s3://your-bucket-name/ --recursive
  ```

## Security Checklist

Before deploying to production:

- [ ] Review and customize IAM policies
- [ ] Enable CloudTrail logging for S3 data events
- [ ] Configure S3 Access Logs (if needed)
- [ ] Review bucket policies
- [ ] Verify public access is blocked
- [ ] Confirm encryption is enabled
- [ ] Set up AWS Config rules for compliance monitoring
- [ ] Enable AWS GuardDuty for threat detection
- [ ] Document access procedures

## Cost Estimation

Use AWS Pricing Calculator for accurate estimates:

**Example Calculation (10 TB, 1 year):**

| Month | Storage (GB) | Class | Cost/Month | Running Total |
|-------|--------------|-------|------------|---------------|
| 1 | 10,000 | Standard | $230 | $230 |
| 2 | 10,000 | Standard-IA | $125 | $355 |
| 3 | 10,000 | Standard-IA | $125 | $480 |
| ... | ... | ... | ... | ... |
| 12 | 10,000 | Standard-IA | $125 | $1,627 |

**Annual Cost:** $1,627 (vs $2,760 with Standard only)

## Support and Resources

- **AWS Support:** https://aws.amazon.com/support/
- **Terraform Documentation:** https://www.terraform.io/docs/
- **S3 User Guide:** https://docs.aws.amazon.com/s3/
- **Cost Optimization:** See [COST_ANALYSIS.md](COST_ANALYSIS.md)

## Next Steps

1. **Upload Media Assets**
   ```bash
   aws s3 sync ./media-files/ s3://your-bucket-name/
   ```

2. **Monitor Initial Period** (30 days)
   - Track storage metrics
   - Monitor access patterns
   - Verify lifecycle transitions

3. **Analyze and Optimize**
   - Review S3 Storage Class Analysis reports
   - Adjust lifecycle policies if needed
   - Optimize based on actual usage

4. **Scale and Enhance**
   - Configure CDN (CloudFront) if needed
   - Set up replication for DR
   - Implement additional security controls

---

**Congratulations!** Your S3 storage optimization solution is now deployed and ready to save costs while maintaining high performance.
