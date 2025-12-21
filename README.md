# S3 Storage Cost Optimization for Infrequently Accessed Media Assets

[![Terraform](https://img.shields.io/badge/Terraform-v1.0+-623CE4?logo=terraform)](https://www.terraform.io/)
[![AWS](https://img.shields.io/badge/AWS-S3-FF9900?logo=amazon-aws)](https://aws.amazon.com/s3/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

This repository demonstrates an Amazon S3 cost-optimization strategy for media assets that are frequently accessed initially and rarely accessed later. It uses S3 lifecycle policies to transition objects from S3 Standard to S3 Standard-IA while maintaining **millisecond latency access** and reducing long-term storage costs, aligned with **DEA-C01 best practices**.

## 🎯 Solution Overview

This Terraform-based solution implements an automated storage optimization strategy for high-resolution media assets (photos, videos, etc.) that follows this lifecycle:

1. **Days 0-30**: Objects stored in **S3 Standard** for frequent access
2. **Day 30+**: Automatically transitioned to **S3 Standard-IA** (Infrequent Access)
3. **All stages**: Maintains millisecond access latency and encryption

**Key Benefits:**
- ✅ **41% cost reduction** after transition to Standard-IA
- ✅ **Millisecond access latency** maintained at all times
- ✅ **Automatic lifecycle management** - no manual intervention
- ✅ **Server-side encryption** (AES-256) enabled by default
- ✅ **Versioning and data protection** configured
- ✅ **DEA-C01 certified** best practices implementation

## 📊 Why Standard-IA Over Glacier?

| Feature | S3 Standard | S3 Standard-IA | Glacier Flexible | Glacier Deep Archive |
|---------|-------------|----------------|------------------|---------------------|
| **Access Latency** | Milliseconds | **Milliseconds** ✓ | Minutes-Hours ✗ | 12-48 Hours ✗ |
| **Storage Cost** | $0.023/GB | **$0.0125/GB** | $0.0036/GB | $0.00099/GB |
| **Retrieval Cost** | Free | **$0.01/GB** | $0.01-0.05/GB | $0.02/GB |
| **Min Storage** | None | 30 days | 90 days | 180 days |
| **Best For** | Hot data | **Warm data** ✓ | Cold data | Archive |

**Standard-IA is chosen because:**
- No retrieval delays (millisecond latency vs minutes/hours with Glacier)
- Lower retrieval costs than Glacier Instant ($0.01/GB vs $0.03/GB)
- Supports unpredictable access patterns
- No restoration process required
- Perfect for media assets that need immediate availability

See [COST_ANALYSIS.md](COST_ANALYSIS.md) for detailed cost comparison and calculations.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Media Asset Upload                        │
│                           ↓                                   │
│  ┌────────────────────────────────────────────────────┐     │
│  │         S3 Bucket (Encrypted with AES-256)         │     │
│  │                                                      │     │
│  │  Days 0-30: S3 Standard Storage Class              │     │
│  │  • Frequent access expected                         │     │
│  │  • Full throughput and performance                  │     │
│  │  • Millisecond latency                             │     │
│  │                                                      │     │
│  │              ↓ (Automatic Lifecycle Transition)     │     │
│  │                                                      │     │
│  │  Day 30+: S3 Standard-IA Storage Class             │     │
│  │  • Infrequent access (cost optimized)              │     │
│  │  • Same millisecond latency maintained             │     │
│  │  • 46% cost reduction                              │     │
│  │  • No operational changes required                  │     │
│  └────────────────────────────────────────────────────┘     │
│                                                               │
│  Additional Features:                                         │
│  ✓ Versioning enabled                                        │
│  ✓ Encryption at rest (AES-256)                             │
│  ✓ Public access blocked                                     │
│  ✓ Cost allocation tags                                      │
│  ✓ Intelligent-Tiering for advanced optimization            │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- [Terraform](https://www.terraform.io/downloads.html) >= 1.0
- AWS Account with appropriate permissions
- AWS CLI configured with credentials

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/iotda-ol/dea-c01-s3-storage-cost-optimization-for-infrequently-accessed-media-assets.git
   cd dea-c01-s3-storage-cost-optimization-for-infrequently-accessed-media-assets
   ```

2. **Create your configuration:**
   ```bash
   cp terraform.tfvars.example terraform.tfvars
   ```

3. **Edit `terraform.tfvars` with your values:**
   ```hcl
   aws_region            = "us-east-1"
   environment           = "production"
   bucket_name           = "my-unique-media-bucket-12345"
   days_to_transition_ia = 30
   enable_versioning     = true
   ```

4. **Initialize Terraform:**
   ```bash
   terraform init
   ```

5. **Preview the changes:**
   ```bash
   terraform plan
   ```

6. **Deploy the infrastructure:**
   ```bash
   terraform apply
   ```

7. **View outputs:**
   ```bash
   terraform output
   ```

## 📁 Project Structure

```
.
├── README.md                    # This file - main documentation
├── COST_ANALYSIS.md            # Detailed cost analysis and comparison
├── provider.tf                 # Terraform and AWS provider configuration
├── variables.tf                # Input variables definition
├── main.tf                     # Main S3 bucket and lifecycle configuration
├── outputs.tf                  # Output values after deployment
└── terraform.tfvars.example    # Example configuration file
```

## ⚙️ Configuration

### Key Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `aws_region` | AWS region for resources | `us-east-1` | No |
| `bucket_name` | Unique S3 bucket name | - | **Yes** |
| `environment` | Environment name | `production` | No |
| `days_to_transition_ia` | Days before transition to Standard-IA | `30` | No |
| `enable_versioning` | Enable bucket versioning | `true` | No |
| `additional_tags` | Custom tags for resources | `{}` | No |
| `force_destroy` | Allow bucket deletion with objects | `false` | No |

See [variables.tf](variables.tf) for complete variable documentation.

## 🔐 Security Features

This solution implements AWS security best practices:

- ✅ **Server-side encryption** (AES-256) enabled by default
- ✅ **Bucket Key enabled** to reduce encryption costs
- ✅ **Public access blocked** at bucket level
- ✅ **Versioning enabled** for data protection
- ✅ **IAM policies** can be attached for fine-grained access control
- ✅ **Encryption in transit** enforced via HTTPS
- ✅ **CloudTrail logging** compatible for audit trails

## 📈 Lifecycle Policy Details

The solution implements two lifecycle rules:

### Rule 1: Transition to Standard-IA
- **Applies to**: All objects in the bucket
- **Action**: Transition to `STANDARD_IA` storage class
- **Timing**: After 30 days (configurable)
- **Benefit**: 46% cost reduction while maintaining performance

### Rule 2: Cleanup and Optimization
- **Noncurrent Version Transition**: Move old versions to Standard-IA after 30 days
- **Noncurrent Version Expiration**: Delete versions after 90 days
- **Multipart Upload Cleanup**: Abort incomplete uploads after 7 days

### Optional: Intelligent-Tiering
For advanced optimization, the solution includes S3 Intelligent-Tiering configuration:
- Archive Access Tier: After 90 days of no access
- Deep Archive Access Tier: After 180 days of no access

## 💰 Cost Optimization

### Expected Savings

For **10 TB of media assets** stored for **1 year**:

| Storage Strategy | Annual Cost | Savings |
|-----------------|-------------|---------|
| S3 Standard only | $2,760 | - |
| **Standard → Standard-IA (30 days)** | **$1,627** | **41%** ✓ |
| Standard → Glacier Instant (90 days) | $1,104 | 60% |

**Why we choose Standard-IA:**
- Better balance of cost and access performance
- Suitable for monthly access patterns
- No retrieval delays
- Simpler operational model

See [COST_ANALYSIS.md](COST_ANALYSIS.md) for detailed calculations.

### Cost Monitoring

After deployment, monitor costs using:
1. **AWS Cost Explorer** - Filter by S3 bucket tags
2. **S3 Storage Class Analysis** - Validate access patterns
3. **CloudWatch Metrics** - Track request and storage metrics
4. **AWS Budgets** - Set up cost alerts

## 📊 Outputs

After successful deployment, Terraform provides:

```hcl
bucket_id                     # S3 bucket name
bucket_arn                    # S3 bucket ARN
bucket_domain_name           # Bucket domain name
bucket_regional_domain_name  # Regional domain name
lifecycle_rules              # Summary of lifecycle configuration
encryption_status            # Encryption details
versioning_status           # Versioning status
cost_optimization_summary   # Cost strategy summary
```

## 🧪 Validation

To validate the deployment:

1. **Check Terraform formatting:**
   ```bash
   terraform fmt -check
   ```

2. **Validate configuration:**
   ```bash
   terraform validate
   ```

3. **Verify bucket in AWS Console:**
   - Navigate to S3 in AWS Console
   - Find your bucket
   - Check "Management" tab for lifecycle rules
   - Check "Properties" tab for encryption and versioning

4. **Test object upload:**
   ```bash
   aws s3 cp test-file.jpg s3://your-bucket-name/
   ```

5. **Check object storage class:**
   ```bash
   aws s3api head-object --bucket your-bucket-name --key test-file.jpg
   ```

## 📚 DEA-C01 Best Practices

This solution aligns with AWS Certified Data Analytics - Specialty (DEA-C01) exam best practices:

### Domain 1: Collection
- ✅ Appropriate storage solution for media data
- ✅ Scalable and durable storage architecture

### Domain 2: Storage and Data Management
- ✅ Lifecycle policies for cost optimization
- ✅ Appropriate storage class selection
- ✅ Data retention and versioning strategies
- ✅ Encryption at rest and in transit

### Domain 3: Processing
- ✅ Data access patterns consideration
- ✅ Latency requirements satisfied

### Domain 4: Analysis and Visualization
- ✅ Quick data retrieval for analytics
- ✅ No performance degradation over time

### Domain 5: Security
- ✅ Encryption enabled by default
- ✅ Access controls implemented
- ✅ Audit trail capability

## 🔄 Maintenance

### Regular Tasks

1. **Review Access Patterns** (Monthly)
   - Use S3 Storage Class Analysis
   - Adjust transition days if needed

2. **Monitor Costs** (Monthly)
   - Review AWS Cost Explorer
   - Validate savings alignment

3. **Update Terraform** (Quarterly)
   - Check for provider updates
   - Apply security patches

### Modifying Lifecycle Rules

To change the transition period:

```hcl
# In terraform.tfvars
days_to_transition_ia = 60  # Change from 30 to 60 days
```

Then apply changes:
```bash
terraform apply
```

## 🐛 Troubleshooting

### Issue: Bucket name already exists
**Solution**: Change `bucket_name` in `terraform.tfvars` to a globally unique name.

### Issue: Permission denied
**Solution**: Ensure your AWS credentials have S3 full access permissions.

### Issue: Objects not transitioning
**Solution**: 
- Check lifecycle rule is enabled in AWS Console
- Verify objects are older than transition period
- S3 lifecycle transitions occur at midnight UTC

### Issue: Terraform state locked
**Solution**: If using remote state with locking, wait for concurrent operations to complete or manually unlock.

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔗 Additional Resources

- [AWS S3 Storage Classes](https://aws.amazon.com/s3/storage-classes/)
- [S3 Lifecycle Configuration](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html)
- [DEA-C01 Exam Guide](https://aws.amazon.com/certification/certified-data-analytics-specialty/)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [AWS S3 Pricing](https://aws.amazon.com/s3/pricing/)

## 📞 Support

For questions or issues:
- Open an issue in this repository
- Review [COST_ANALYSIS.md](COST_ANALYSIS.md) for detailed explanations
- Check AWS documentation for S3-specific questions

---

**Note**: This is a production-ready template. Always review and test in a non-production environment before deploying to production.
