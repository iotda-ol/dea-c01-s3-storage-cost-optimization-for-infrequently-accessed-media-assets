# Architecture Documentation

## System Architecture Overview

This document provides detailed architecture information for the S3 Storage Cost Optimization solution.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        AWS Cloud Infrastructure                      │
│                                                                       │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │                   Amazon S3 Bucket                          │    │
│  │                                                              │    │
│  │  ┌────────────────────────────────────────────────────┐   │    │
│  │  │          Encryption Layer (AES-256)                 │   │    │
│  │  │  ┌──────────────────────────────────────────────┐  │   │    │
│  │  │  │      Versioning Enabled                       │  │   │    │
│  │  │  │  ┌────────────────────────────────────────┐  │  │   │    │
│  │  │  │  │    Storage Lifecycle Management         │  │  │   │    │
│  │  │  │  │                                          │  │  │   │    │
│  │  │  │  │  Days 0-30:  S3 Standard               │  │  │   │    │
│  │  │  │  │    • Frequent access                    │  │  │   │    │
│  │  │  │  │    • Full performance                   │  │  │   │    │
│  │  │  │  │    • Millisecond latency               │  │  │   │    │
│  │  │  │  │                                          │  │  │   │    │
│  │  │  │  │           ↓ (Automatic)                │  │  │   │    │
│  │  │  │  │                                          │  │  │   │    │
│  │  │  │  │  Day 30+:  S3 Standard-IA              │  │  │   │    │
│  │  │  │  │    • Infrequent access                  │  │  │   │    │
│  │  │  │  │    • Same millisecond latency          │  │  │   │    │
│  │  │  │  │    • 46% cost reduction                │  │  │   │    │
│  │  │  │  └────────────────────────────────────────┘  │  │   │    │
│  │  │  │                                                │  │   │    │
│  │  │  │  Noncurrent Versions:                         │  │   │    │
│  │  │  │    • Transition to Standard-IA after 30 days  │  │   │    │
│  │  │  │    • Delete after 90 days                     │  │   │    │
│  │  │  └──────────────────────────────────────────────┘  │   │    │
│  │  │                                                      │   │    │
│  │  │  Block Public Access: ENABLED                      │   │    │
│  │  └────────────────────────────────────────────────────┘   │    │
│  │                                                              │    │
│  │  Tags:                                                       │    │
│  │    • Project: S3-Storage-Optimization                       │    │
│  │    • ManagedBy: Terraform                                   │    │
│  │    • Environment: [production/staging/dev]                  │    │
│  │    • Custom tags as configured                              │    │
│  └────────────────────────────────────────────────────────────┘    │
│                                                                       │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │              Optional: S3 Intelligent-Tiering               │    │
│  │                                                              │    │
│  │  Additional Optimization:                                    │    │
│  │    • Archive Access Tier after 90 days (no access)          │    │
│  │    • Deep Archive Access Tier after 180 days (no access)    │    │
│  └────────────────────────────────────────────────────────────┘    │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. S3 Bucket Core Configuration

**Resource:** `aws_s3_bucket.media_assets`

- **Purpose:** Primary storage for high-resolution media assets
- **Naming:** User-defined, globally unique bucket name
- **Region:** Configurable (default: us-east-1)
- **Durability:** 99.999999999% (11 9's)
- **Availability:** 99.9% (Standard), 99.9% (Standard-IA)

### 2. Encryption Configuration

**Resource:** `aws_s3_bucket_server_side_encryption_configuration.media_assets`

```
┌─────────────────────────────────┐
│    Server-Side Encryption       │
├─────────────────────────────────┤
│ Algorithm: AES-256              │
│ Bucket Key: Enabled             │
│ Key Management: AWS-managed     │
└─────────────────────────────────┘
```

**Features:**
- All objects encrypted at rest automatically
- Bucket Key reduces encryption costs by up to 99%
- No performance impact on read/write operations
- AWS-managed keys (SSE-S3) for simplicity

**Alternative Options (not implemented by default):**
- SSE-KMS: Customer-managed keys for compliance requirements
- SSE-C: Customer-provided keys

### 3. Versioning Configuration

**Resource:** `aws_s3_bucket_versioning.media_assets`

```
Object: image.jpg
├── Version 1 (Current) → S3 Standard → transitions to Standard-IA
├── Version 2 (Noncurrent) → transitions to Standard-IA after 30 days
└── Version 3 (Noncurrent) → deleted after 90 days
```

**Benefits:**
- Protection against accidental deletions
- Ability to restore previous versions
- Compliance with data retention requirements
- Separate lifecycle rules for noncurrent versions

### 4. Public Access Block

**Resource:** `aws_s3_bucket_public_access_block.media_assets`

All public access settings are blocked:
- ✅ `block_public_acls = true`
- ✅ `block_public_policy = true`
- ✅ `ignore_public_acls = true`
- ✅ `restrict_public_buckets = true`

**Security Impact:**
- Prevents accidental public exposure
- Enforces private bucket access
- Access must be explicitly granted via IAM

### 5. Lifecycle Policy Configuration

**Resource:** `aws_s3_bucket_lifecycle_configuration.media_assets`

#### Rule 1: Transition to Standard-IA

```
Timeline:
Day 0    Day 30                                          Day 365+
├────────┼────────────────────────────────────────────────────►
│        │
│ S3     │ S3 Standard-IA (46% cheaper, same latency)
│ Standard
│ ($0.023/GB)  ($0.0125/GB + $0.01/GB retrieval)
│        │
│        └─ Automatic transition trigger
```

**Configuration:**
```hcl
transition {
  days          = 30
  storage_class = "STANDARD_IA"
}
```

**Impact:**
- Applies to all current object versions
- Noncurrent versions also transition after 30 days
- No application changes required
- Transparent to end users

#### Rule 2: Noncurrent Version Management

```
Version Lifecycle:
Create   30 days          90 days
├────────┼─────────────────┼──────────►
│        │                 │
│ Current│ Noncurrent     │ Deleted
│ Version│ → Standard-IA  │
```

**Configuration:**
```hcl
noncurrent_version_transition {
  noncurrent_days = 30
  storage_class   = "STANDARD_IA"
}

noncurrent_version_expiration {
  noncurrent_days = 90
}
```

**Additional Cleanup:**
```hcl
abort_incomplete_multipart_upload {
  days_after_initiation = 7
}
```

### 6. Intelligent-Tiering (Optional Enhancement)

**Resource:** `aws_s3_bucket_intelligent_tiering_configuration.media_assets`

```
Access Pattern Timeline:
Active   90 days    180 days
├────────┼──────────┼───────────────►
│        │          │
│ Active │ Archive  │ Deep Archive
│ Tier   │ Access   │ Access
│        │ (cheaper)│ (cheapest)
```

**Configuration:**
```hcl
tiering {
  access_tier = "ARCHIVE_ACCESS"
  days        = 90
}

tiering {
  access_tier = "DEEP_ARCHIVE_ACCESS"
  days        = 180
}
```

**When to Use:**
- Unpredictable access patterns
- Mix of hot and cold data
- Want automated optimization beyond basic lifecycle

## Data Flow

### Upload Flow

```
┌──────────┐     ┌──────────┐     ┌──────────────┐     ┌──────────────┐
│  Client  │────▶│   IAM    │────▶│   S3 API     │────▶│   S3 Bucket  │
│   App    │     │  Policy  │     │  PutObject   │     │   Standard   │
└──────────┘     └──────────┘     └──────────────┘     └──────────────┘
                      ▲                                         │
                      │                                         ▼
                  Validate                              ┌──────────────┐
                  Permissions                           │   Encrypt    │
                                                        │   (AES-256)  │
                                                        └──────────────┘
                                                              │
                                                              ▼
                                                        ┌──────────────┐
                                                        │  Tag & Store │
                                                        └──────────────┘
```

### Access Flow

```
┌──────────┐     ┌──────────┐     ┌──────────────┐     ┌──────────────┐
│  Client  │────▶│   IAM    │────▶│   S3 API     │────▶│   S3 Bucket  │
│   App    │     │  Policy  │     │  GetObject   │     │ (Any Class)  │
└──────────┘     └──────────┘     └──────────────┘     └──────────────┘
     ▲                                                           │
     │                                                           ▼
     │                                                   ┌──────────────┐
     │                                                   │   Decrypt    │
     │                                                   │  & Retrieve  │
     │                                                   └──────────────┘
     │                                                           │
     └───────────────────────────────────────────────────────────┘
              Millisecond latency (both Standard and Standard-IA)
```

### Lifecycle Transition Flow

```
┌──────────────┐
│  S3 Bucket   │
│   Standard   │
└──────┬───────┘
       │
       │ (Daily evaluation at midnight UTC)
       │
       ▼
┌──────────────┐
│   Lifecycle  │
│   Engine     │
└──────┬───────┘
       │
       │ Check: Object age > 30 days?
       │
       ├─ No ─▶ Keep in Standard
       │
       └─ Yes ─▶ ┌──────────────┐
                 │ Transition   │
                 │ to           │
                 │ Standard-IA  │
                 └──────────────┘
```

## Storage Class Transition Matrix

| From | To | Minimum Days | Cost Impact | Latency Impact |
|------|----|--------------| ------------|----------------|
| Standard | Standard-IA | 30 | -46% storage, +$0.01/GB retrieval | None |
| Standard-IA | Glacier Instant | 30 | -68% storage, +$0.03/GB retrieval | None |
| Standard-IA | Glacier Flexible | 30 | -71% storage, +variable retrieval | Minutes-Hours |
| Glacier Flexible | Deep Archive | 90 | -72% storage, +$0.02/GB retrieval | 12-48 Hours |

**Our Implementation:** Standard → Standard-IA (optimal balance)

## Terraform Resource Dependencies

```
provider.tf
    ↓
variables.tf
    ↓
main.tf
    ├─▶ aws_s3_bucket
    │        ↓
    │   ┌────┴────┬───────────┬──────────────┬────────────┐
    │   ↓         ↓           ↓              ↓            ↓
    │   Versioning Encryption Lifecycle  Public_Block  Intelligent
    │   Config    Config      Config     Config        Tiering
    │
    └─▶ outputs.tf
```

**Dependency Chain:**
1. Provider configured
2. Variables defined
3. S3 bucket created
4. Dependent resources configured (versioning, encryption, etc.)
5. Outputs generated

## Security Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Security Layers                       │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  Layer 1: Network Security                               │
│    └─ Block Public Access (4 settings enabled)          │
│                                                           │
│  Layer 2: Identity & Access Management                   │
│    ├─ IAM Policies (user-defined)                       │
│    ├─ Bucket Policies (optional)                        │
│    └─ AWS STS for temporary credentials                 │
│                                                           │
│  Layer 3: Encryption                                     │
│    ├─ Server-Side Encryption (AES-256)                  │
│    ├─ Encryption in Transit (HTTPS enforced)            │
│    └─ Bucket Key (cost optimization)                    │
│                                                           │
│  Layer 4: Data Protection                                │
│    ├─ Versioning (accidental deletion protection)       │
│    └─ Lifecycle policies (automated management)         │
│                                                           │
│  Layer 5: Monitoring & Audit                             │
│    ├─ CloudTrail (optional, for S3 data events)         │
│    ├─ S3 Access Logs (optional)                         │
│    └─ CloudWatch Metrics                                 │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

## Cost Architecture

### Cost Components

```
Total S3 Cost = Storage Cost + Request Cost + Data Transfer Cost

1. Storage Cost
   ├─ S3 Standard (days 0-30): Objects × $0.023/GB/month
   └─ S3 Standard-IA (day 30+): Objects × $0.0125/GB/month

2. Request Cost
   ├─ PUT/POST/LIST: $0.005 per 1,000 requests
   └─ GET/SELECT: $0.0004 per 1,000 requests

3. Retrieval Cost (Standard-IA only)
   └─ $0.01 per GB retrieved

4. Data Transfer
   ├─ Data IN: Free
   ├─ Data OUT to Internet: $0.09/GB (first 10 TB)
   └─ Data OUT to AWS services (same region): Free
```

### Cost Optimization Features

```
┌─────────────────────────────────────────────────┐
│         Cost Optimization Mechanisms             │
├─────────────────────────────────────────────────┤
│ 1. Lifecycle Transition                          │
│    • Automatic move to cheaper storage           │
│    • 46% storage cost reduction                  │
│                                                   │
│ 2. Bucket Key                                    │
│    • Reduces encryption API calls                │
│    • Up to 99% reduction in encryption costs     │
│                                                   │
│ 3. Noncurrent Version Expiration                │
│    • Deletes old versions automatically          │
│    • Prevents cost accumulation                  │
│                                                   │
│ 4. Multipart Upload Cleanup                     │
│    • Aborts incomplete uploads                   │
│    • Prevents phantom storage costs              │
│                                                   │
│ 5. Tagging Strategy                              │
│    • Cost allocation by tag                      │
│    • Detailed cost tracking                      │
│                                                   │
│ 6. Intelligent-Tiering (Optional)               │
│    • Automatic tiering based on access           │
│    • No retrieval fees for tier changes          │
└─────────────────────────────────────────────────┘
```

## Performance Characteristics

### Latency Profile

| Storage Class | First Byte Latency | Throughput | Concurrent Requests |
|---------------|-------------------|------------|---------------------|
| S3 Standard | Milliseconds | 3,500 PUT/s, 5,500 GET/s per prefix | Unlimited |
| S3 Standard-IA | **Milliseconds** | Same as Standard | Unlimited |
| Glacier Instant | Milliseconds | Same as Standard | Unlimited |
| Glacier Flexible | Minutes to hours | N/A | Queued |
| Deep Archive | 12-48 hours | N/A | Queued |

**Key Point:** Standard-IA maintains identical performance to Standard.

### Scalability

```
Requests per Second per Prefix:
├─ PUT/COPY/POST/DELETE: 3,500/s
└─ GET/HEAD: 5,500/s

Total Throughput:
├─ No limits on number of prefixes
├─ Can scale to hundreds of thousands of requests per second
└─ Automatic scaling (no configuration needed)
```

## Monitoring Architecture

### Key Metrics to Track

```
┌────────────────────────────────────────────────────────┐
│              CloudWatch Metrics                         │
├────────────────────────────────────────────────────────┤
│                                                          │
│ Storage Metrics:                                        │
│  • BucketSizeBytes (by storage class)                  │
│  • NumberOfObjects                                      │
│                                                          │
│ Request Metrics:                                        │
│  • AllRequests                                          │
│  • GetRequests                                          │
│  • PutRequests                                          │
│  • 4xxErrors                                            │
│  • 5xxErrors                                            │
│                                                          │
│ Data Transfer Metrics:                                  │
│  • BytesDownloaded                                      │
│  • BytesUploaded                                        │
│                                                          │
│ Lifecycle Metrics:                                      │
│  • Transitions completed                                │
│  • Objects transitioned                                 │
│                                                          │
└────────────────────────────────────────────────────────┘
```

### Recommended Alarms

1. **High Error Rate**: 4xx/5xx errors > threshold
2. **Unexpected Cost**: Storage cost > budget
3. **Rapid Growth**: Storage size increase > expected rate
4. **Failed Transitions**: Lifecycle transitions failing

## DEA-C01 Alignment

### Exam Domain Coverage

```
┌────────────────────────────────────────────────────────┐
│       DEA-C01 Exam Domains Addressed                    │
├────────────────────────────────────────────────────────┤
│                                                          │
│ Domain 1: Collection (18%)                             │
│  ✓ Data storage solutions                              │
│  ✓ Appropriate service selection                       │
│                                                          │
│ Domain 2: Storage & Data Management (22%)              │
│  ✓ Storage class selection                             │
│  ✓ Lifecycle policies                                  │
│  ✓ Cost optimization                                   │
│  ✓ Data retention strategies                           │
│                                                          │
│ Domain 3: Processing (24%)                             │
│  ✓ Data access patterns                                │
│  ✓ Performance optimization                            │
│                                                          │
│ Domain 4: Analysis & Visualization (18%)               │
│  ✓ Data availability for analytics                     │
│  ✓ Query performance                                   │
│                                                          │
│ Domain 5: Security (18%)                               │
│  ✓ Encryption at rest                                  │
│  ✓ Access controls                                     │
│  ✓ Data protection (versioning)                        │
│                                                          │
└────────────────────────────────────────────────────────┘
```

## Disaster Recovery Architecture

### Backup Strategy

```
Primary Bucket
     │
     ├─ Versioning Enabled
     │   └─ Previous versions preserved (90 days)
     │
     ├─ Cross-Region Replication (Optional)
     │   └─ Secondary bucket in different region
     │
     └─ Lifecycle Management
         └─ Automated transitions (no manual intervention)
```

### Recovery Time Objective (RTO)

- **Version Restore**: Immediate (seconds)
- **Object Recovery**: Immediate (milliseconds)
- **Region Failover** (if CRR enabled): Minutes

### Recovery Point Objective (RPO)

- **Versioning**: Near-zero (every version saved)
- **Replication** (if enabled): < 15 minutes typical

## Future Enhancements

Potential additions to consider:

1. **Cross-Region Replication**
   - Geographic redundancy
   - Disaster recovery

2. **CloudFront Integration**
   - Content delivery network
   - Edge caching
   - Reduced origin requests

3. **S3 Event Notifications**
   - Lambda triggers
   - SNS/SQS integration
   - Automated processing

4. **Access Points**
   - Per-application access patterns
   - Simplified policy management

5. **Object Lock**
   - WORM (Write Once Read Many)
   - Compliance requirements

6. **S3 Select**
   - Query objects without retrieval
   - Cost optimization for analytics

---

This architecture is designed to be production-ready, cost-effective, and aligned with AWS best practices and DEA-C01 certification requirements.
