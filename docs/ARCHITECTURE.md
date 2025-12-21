# S3 Storage Cost Optimization - Architecture Documentation

## Overview

This project provides a modular, reusable framework for optimizing S3 storage costs through intelligent lifecycle policies and storage class transitions. It is specifically designed for media assets that are frequently accessed initially and rarely accessed later.

## Architecture

### Modular Structure

The project follows a highly modular architecture with clear separation of concerns:

```
src/
├── core/                    # Core business logic
│   ├── lifecycle_manager.py # Lifecycle policy management
│   ├── s3_client.py        # S3 client wrapper
│   └── storage_optimizer.py # Storage analysis and optimization
├── config/                  # Configuration management
│   ├── settings.py         # Settings loader
│   └── constants.py        # Application constants
├── utils/                   # Reusable utilities
│   ├── logger.py           # Logging utilities
│   ├── validators.py       # Validation functions
│   └── formatters.py       # Output formatters
└── media_management/        # Media-specific functionality
    ├── media_processor.py  # Media upload and processing
    └── metadata_manager.py # Metadata and tagging
```

## Core Modules

### 1. Lifecycle Manager (`src/core/lifecycle_manager.py`)

**Purpose**: Manages S3 bucket lifecycle policies for automated storage class transitions.

**Key Features**:
- Create optimized lifecycle policies for media assets
- Apply/retrieve/delete lifecycle configurations
- Support for multiple transition rules
- Tag-based filtering

**Reusable Methods**:
```python
create_media_lifecycle_policy(bucket_name, standard_ia_days, glacier_days, ...)
apply_lifecycle_policy(bucket_name, lifecycle_config)
get_lifecycle_policy(bucket_name)
delete_lifecycle_policy(bucket_name)
```

### 2. S3 Client Wrapper (`src/core/s3_client.py`)

**Purpose**: Provides enhanced S3 operations with built-in error handling and logging.

**Key Features**:
- Bucket existence checking
- Bucket creation
- File upload with metadata
- Object listing and classification
- Storage class inspection

**Reusable Methods**:
```python
bucket_exists(bucket_name)
create_bucket(bucket_name, region)
upload_file(file_path, bucket_name, object_key, ...)
get_object_storage_class(bucket_name, object_key)
list_objects(bucket_name, prefix)
```

### 3. Storage Optimizer (`src/core/storage_optimizer.py`)

**Purpose**: Analyzes storage patterns and provides cost optimization recommendations.

**Key Features**:
- Storage distribution analysis
- Cost savings calculations
- Lifecycle policy recommendations
- Comprehensive optimization reports

**Reusable Methods**:
```python
analyze_bucket_storage(bucket_name, prefix)
calculate_cost_savings(current_storage_gb, current_class, target_class)
recommend_lifecycle_policy(bucket_name, access_pattern)
get_optimization_report(bucket_name, prefix)
```

## Configuration Module

### Settings (`src/config/settings.py`)

**Purpose**: Centralized configuration management with environment variable support.

**Features**:
- JSON configuration file support
- Environment variable overrides
- Dot-notation access (e.g., `settings.get('aws.region')`)
- Configuration validation

### Constants (`src/config/constants.py`)

**Purpose**: Defines reusable enumerations and constants.

**Includes**:
- Storage class enumerations
- Lifecycle action types
- Media type classifications
- Default transition days
- Storage class constraints

## Utilities Module

### Logger (`src/utils/logger.py`)

**Purpose**: Provides consistent logging across the application.

**Features**:
- Console and file logging
- Configurable log levels
- Standardized formatting

### Validators (`src/utils/validators.py`)

**Purpose**: Validation functions for S3 operations.

**Validates**:
- S3 bucket names (AWS naming rules)
- Lifecycle configurations
- Transition day configurations
- Storage class names

### Formatters (`src/utils/formatters.py`)

**Purpose**: Format data for human-readable output.

**Functions**:
- Byte size formatting (e.g., "1.50 GB")
- Cost formatting (e.g., "$12.50 USD")
- Percentage formatting
- Duration formatting

## Media Management Module

### Media Processor (`src/media_management/media_processor.py`)

**Purpose**: Handles media-specific operations.

**Features**:
- Automatic media type classification
- Metadata extraction
- Single and batch uploads
- Storage class recommendations

### Metadata Manager (`src/media_management/metadata_manager.py`)

**Purpose**: Manages S3 object metadata and tags.

**Features**:
- Object tagging
- Tag retrieval
- Metadata updates
- Batch tagging operations
- Lifecycle-optimized tag creation

## Best Practices

### 1. Modularity
- Each module has a single, well-defined responsibility
- Modules are independent and reusable
- Clear interfaces between components

### 2. Reusability
- All core functionality is exposed through reusable classes and functions
- Configuration is externalized
- Utilities are generic and widely applicable

### 3. Error Handling
- Comprehensive error handling in all modules
- Detailed logging for debugging
- Graceful degradation

### 4. Configuration
- Support for multiple configuration sources
- Environment variable overrides
- Sensible defaults

### 5. Testing
- Unit tests for core functionality
- Mock-based testing for AWS services
- Clear test structure

## Deployment Options

### CloudFormation
- Infrastructure as Code template
- Automated S3 bucket creation
- Pre-configured lifecycle policies
- Security best practices (encryption, public access blocking)

### Terraform
- Multi-cloud compatible IaC
- Modular resource definitions
- Variable-driven configuration
- State management

## Usage Patterns

### Basic Usage
```python
from src.core.s3_client import S3ClientWrapper
from src.core.lifecycle_manager import LifecycleManager

# Initialize
s3_client = S3ClientWrapper(region_name='us-east-1')
lifecycle_mgr = LifecycleManager(s3_client)

# Create and apply policy
config = lifecycle_mgr.create_media_lifecycle_policy(
    bucket_name='my-bucket',
    standard_ia_days=30,
    glacier_days=90
)
lifecycle_mgr.apply_lifecycle_policy('my-bucket', config)
```

### Cost Analysis
```python
from src.core.storage_optimizer import StorageOptimizer

optimizer = StorageOptimizer(s3_client)
report = optimizer.get_optimization_report('my-bucket')
print(f"Potential savings: ${report['potential_savings']['annual_savings']}")
```

### Media Upload
```python
from src.media_management.media_processor import MediaProcessor

processor = MediaProcessor(s3_client)
results = processor.batch_upload_media(
    directory='/path/to/media',
    bucket_name='my-bucket',
    prefix='media'
)
```

## Storage Class Transition Strategy

### Recommended Timeline
1. **Day 0-30**: STANDARD
   - High-frequency access expected
   - Low latency required
   
2. **Day 30-90**: STANDARD_IA
   - Access frequency decreases
   - 50% storage cost reduction
   - Same retrieval performance
   
3. **Day 90+**: GLACIER
   - Rare access
   - 80% storage cost reduction
   - Archive storage for compliance

### Cost Savings Example
For 1TB of media assets:
- STANDARD: $23/month
- STANDARD_IA: $12.50/month (46% savings)
- GLACIER: $4/month (83% savings)

Annual savings by transitioning to STANDARD_IA after 30 days: ~$126
Annual savings by transitioning to GLACIER after 90 days: ~$228

## Extensibility

The modular architecture supports easy extension:

1. **New Storage Classes**: Add to `constants.py` and update `StorageOptimizer`
2. **Custom Policies**: Create new policy builders in `LifecycleManager`
3. **Additional Media Types**: Extend `MediaType` enum and `MEDIA_EXTENSIONS`
4. **Custom Validators**: Add to `validators.py` module
5. **New Formatters**: Add to `formatters.py` module

## Security Considerations

- Encryption at rest (AES256)
- Encryption in transit (HTTPS only)
- Public access blocking
- IAM-based access control
- No hardcoded credentials
- Secure credential management via AWS SDK
