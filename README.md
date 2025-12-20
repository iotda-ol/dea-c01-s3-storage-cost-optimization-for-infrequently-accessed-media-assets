# S3 Storage Cost Optimization for Infrequently Accessed Media Assets

[![AWS](https://img.shields.io/badge/AWS-S3-orange)](https://aws.amazon.com/s3/)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

This repository demonstrates an Amazon S3 cost-optimization strategy for media assets that are frequently accessed initially and rarely accessed later. It uses S3 lifecycle policies to transition objects from S3 Standard to S3 Standard-IA and eventually to Glacier, maintaining low-latency access while reducing long-term storage costs, aligned with DEA-C01 best practices.

## 🎯 Key Features

- **Maximum Modularity**: Highly organized, reusable code structure with clear separation of concerns
- **Comprehensive Modules**: Core lifecycle management, storage optimization, media processing, and utilities
- **Multiple Deployment Options**: CloudFormation and Terraform templates included
- **Cost Analysis Tools**: Built-in storage analysis and savings calculators
- **Extensive Documentation**: API reference, architecture docs, and usage examples
- **Production-Ready**: Includes logging, validation, error handling, and security best practices
- **Testing Infrastructure**: Unit tests and integration test structure

## 📁 Project Structure

```
.
├── src/                          # Source code (highly modular)
│   ├── core/                     # Core business logic
│   │   ├── lifecycle_manager.py  # S3 lifecycle policy management
│   │   ├── s3_client.py         # Enhanced S3 client wrapper
│   │   └── storage_optimizer.py  # Cost optimization and analysis
│   ├── config/                   # Configuration management
│   │   ├── settings.py          # Settings loader (file + env vars)
│   │   └── constants.py         # Application constants and enums
│   ├── utils/                    # Reusable utilities
│   │   ├── logger.py            # Logging utilities
│   │   ├── validators.py        # Validation functions
│   │   └── formatters.py        # Output formatters
│   └── media_management/         # Media-specific functionality
│       ├── media_processor.py    # Media upload and processing
│       └── metadata_manager.py   # Metadata and tagging
├── examples/                     # Usage examples
│   ├── basic_usage.py           # Basic lifecycle management
│   ├── media_upload.py          # Media asset upload
│   └── cost_analysis.py         # Cost analysis and reporting
├── tests/                        # Test suite
│   ├── unit/                    # Unit tests
│   └── integration/             # Integration tests (structure)
├── deployment/                   # Infrastructure as Code
│   ├── cloudformation/          # CloudFormation templates
│   └── terraform/               # Terraform configurations
├── scripts/                      # Utility scripts
│   ├── setup.sh                 # Environment setup
│   ├── deploy-cloudformation.sh # CloudFormation deployment
│   └── deploy-terraform.sh      # Terraform deployment
├── docs/                         # Documentation
│   ├── ARCHITECTURE.md          # Architecture overview
│   └── API_REFERENCE.md         # API documentation
├── requirements.txt              # Python dependencies
├── requirements-dev.txt          # Development dependencies
└── README.md                     # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- AWS account with appropriate permissions
- AWS CLI configured with credentials

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/iotda-ol/dea-c01-s3-storage-cost-optimization-for-infrequently-accessed-media-assets.git
   cd dea-c01-s3-storage-cost-optimization-for-infrequently-accessed-media-assets
   ```

2. **Run the setup script**
   ```bash
   chmod +x scripts/setup.sh
   ./scripts/setup.sh
   ```

   Or manually:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

3. **Configure AWS credentials**
   ```bash
   aws configure
   ```

### Basic Usage

```python
from src.core.s3_client import S3ClientWrapper
from src.core.lifecycle_manager import LifecycleManager
from src.core.storage_optimizer import StorageOptimizer

# Initialize S3 client
s3_client = S3ClientWrapper(region_name='us-east-1')

# Create lifecycle policy
lifecycle_mgr = LifecycleManager(s3_client)
policy = lifecycle_mgr.create_media_lifecycle_policy(
    bucket_name='my-media-bucket',
    standard_ia_days=30,  # Transition to Standard-IA after 30 days
    glacier_days=90,      # Transition to Glacier after 90 days
    expiration_days=365   # Delete after 1 year
)

# Apply the policy
lifecycle_mgr.apply_lifecycle_policy('my-media-bucket', policy)

# Analyze potential savings
optimizer = StorageOptimizer(s3_client)
report = optimizer.get_optimization_report('my-media-bucket')
print(f"Annual savings: ${report['potential_savings']['annual_savings']}")
```

## 📊 Storage Cost Optimization Strategy

### Lifecycle Transition Timeline

| Time Period | Storage Class | Use Case | Cost Reduction |
|-------------|--------------|----------|----------------|
| Day 0-30 | STANDARD | Frequent initial access | Baseline |
| Day 30-90 | STANDARD_IA | Declining access | ~46% savings |
| Day 90+ | GLACIER | Archive/compliance | ~83% savings |

### Cost Example (1TB of data)

- **STANDARD**: $23.00/month
- **STANDARD_IA**: $12.50/month (46% savings)
- **GLACIER**: $4.00/month (83% savings)

**Annual savings** by implementing lifecycle policies: **$126 - $228/year per TB**

## 🔧 Modules Overview

### Core Modules

- **`lifecycle_manager`**: Create, apply, and manage S3 lifecycle policies
- **`s3_client`**: Enhanced S3 client with error handling and logging
- **`storage_optimizer`**: Analyze storage patterns and calculate cost savings

### Configuration

- **`settings`**: Centralized configuration with environment variable support
- **`constants`**: Reusable enums and constants

### Utilities

- **`logger`**: Consistent logging across modules
- **`validators`**: S3 bucket name and policy validation
- **`formatters`**: Human-readable output formatting

### Media Management

- **`media_processor`**: Media file classification and batch upload
- **`metadata_manager`**: Object tagging and metadata management

## 📦 Deployment

### Using CloudFormation

```bash
./scripts/deploy-cloudformation.sh \
  --bucket-name my-media-bucket \
  --region us-east-1 \
  --standard-ia-days 30 \
  --glacier-days 90 \
  --expiration-days 365
```

### Using Terraform

```bash
./scripts/deploy-terraform.sh \
  --bucket-name my-media-bucket \
  --region us-east-1 \
  --action apply
```

## 🧪 Testing

Run unit tests:
```bash
python -m pytest tests/unit/ -v
```

Run tests with coverage:
```bash
python -m pytest tests/unit/ --cov=src --cov-report=html
```

## 📚 Documentation

- **[Architecture Guide](docs/ARCHITECTURE.md)**: Detailed architecture and design patterns
- **[API Reference](docs/API_REFERENCE.md)**: Complete API documentation
- **Examples**: See `examples/` directory for usage examples

## 🔒 Security Features

- Encryption at rest (AES256)
- Encryption in transit (HTTPS only)
- Public access blocking
- IAM-based access control
- No hardcoded credentials
- Secure credential management via AWS SDK

## 🌟 Best Practices Implemented

### Code Organization
- **Maximum modularity** with single-responsibility modules
- **Reusable components** throughout the codebase
- **Clear folder structure** minimizing loose files
- **Well-documented** code with docstrings

### AWS Best Practices
- DEA-C01 aligned lifecycle policies
- Cost-optimized storage class transitions
- Proper bucket security configuration
- Infrastructure as Code for repeatability

### Development Best Practices
- Comprehensive error handling
- Extensive logging for debugging
- Input validation
- Type hints for better IDE support
- Unit tests for core functionality

## 💡 Use Cases

1. **Media Asset Management**: Optimize costs for video, image, and audio storage
2. **Backup Retention**: Implement retention policies with automatic archival
3. **Log Archival**: Archive application logs with lifecycle policies
4. **Compliance Data**: Store compliance data with automated tiering
5. **Document Storage**: Manage document lifecycle from active to archived

## 🤝 Contributing

Contributions are welcome! Please ensure:
- Code follows the existing modular structure
- All modules have appropriate docstrings
- Unit tests are included for new functionality
- Documentation is updated

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔗 Related Resources

- [AWS S3 Lifecycle Configuration](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html)
- [S3 Storage Classes](https://aws.amazon.com/s3/storage-classes/)
- [DEA-C01 Certification](https://aws.amazon.com/certification/certified-data-engineer-associate/)
- [AWS Cost Optimization](https://aws.amazon.com/pricing/cost-optimization/)

## ✨ Acknowledgments

Built following AWS best practices for cost optimization and designed to demonstrate maximum code modularity and reusability.
