# API Reference

## Core Modules

### `src.core.lifecycle_manager.LifecycleManager`

#### Class: `LifecycleManager`

Manages S3 bucket lifecycle policies for storage cost optimization.

**Methods:**

##### `__init__(s3_client)`
Initialize the LifecycleManager.
- **Parameters:**
  - `s3_client`: Boto3 S3 client or S3ClientWrapper instance

##### `create_media_lifecycle_policy(bucket_name, standard_ia_days=30, glacier_days=90, expiration_days=None, prefix="", tags=None)`
Create a lifecycle policy optimized for media assets.
- **Parameters:**
  - `bucket_name` (str): Name of the S3 bucket
  - `standard_ia_days` (int): Days before transition to Standard-IA (default: 30)
  - `glacier_days` (int): Days before transition to Glacier (default: 90)
  - `expiration_days` (int, optional): Days before object expiration
  - `prefix` (str): Object prefix filter (default: "")
  - `tags` (dict, optional): Tag filters for lifecycle rule
- **Returns:** Dict containing the lifecycle configuration

##### `apply_lifecycle_policy(bucket_name, lifecycle_config)`
Apply a lifecycle policy to an S3 bucket.
- **Parameters:**
  - `bucket_name` (str): Name of the S3 bucket
  - `lifecycle_config` (dict): Lifecycle configuration dictionary
- **Returns:** bool (True if successful)

##### `get_lifecycle_policy(bucket_name)`
Retrieve the current lifecycle policy of a bucket.
- **Parameters:**
  - `bucket_name` (str): Name of the S3 bucket
- **Returns:** Dict or None

##### `delete_lifecycle_policy(bucket_name)`
Delete the lifecycle policy from a bucket.
- **Parameters:**
  - `bucket_name` (str): Name of the S3 bucket
- **Returns:** bool (True if successful)

---

### `src.core.s3_client.S3ClientWrapper`

#### Class: `S3ClientWrapper`

A wrapper class for boto3 S3 client with enhanced functionality.

**Methods:**

##### `__init__(region_name=None, aws_access_key_id=None, aws_secret_access_key=None, profile_name=None)`
Initialize the S3 client wrapper.
- **Parameters:**
  - `region_name` (str, optional): AWS region name
  - `aws_access_key_id` (str, optional): AWS access key ID
  - `aws_secret_access_key` (str, optional): AWS secret access key
  - `profile_name` (str, optional): AWS profile name from credentials file

##### `bucket_exists(bucket_name)`
Check if an S3 bucket exists and is accessible.
- **Parameters:**
  - `bucket_name` (str): Name of the S3 bucket
- **Returns:** bool

##### `create_bucket(bucket_name, region=None)`
Create an S3 bucket.
- **Parameters:**
  - `bucket_name` (str): Name of the S3 bucket
  - `region` (str, optional): AWS region for bucket creation
- **Returns:** bool

##### `upload_file(file_path, bucket_name, object_key, metadata=None, storage_class='STANDARD')`
Upload a file to S3.
- **Parameters:**
  - `file_path` (str): Local file path
  - `bucket_name` (str): S3 bucket name
  - `object_key` (str): S3 object key
  - `metadata` (dict, optional): Custom metadata
  - `storage_class` (str): S3 storage class (default: 'STANDARD')
- **Returns:** bool

##### `get_object_storage_class(bucket_name, object_key)`
Get the storage class of an S3 object.
- **Parameters:**
  - `bucket_name` (str): S3 bucket name
  - `object_key` (str): S3 object key
- **Returns:** str or None

##### `list_objects(bucket_name, prefix="", max_keys=1000)`
List objects in an S3 bucket.
- **Parameters:**
  - `bucket_name` (str): S3 bucket name
  - `prefix` (str): Object key prefix filter (default: "")
  - `max_keys` (int): Maximum number of keys to return (default: 1000)
- **Returns:** List of object dictionaries

---

### `src.core.storage_optimizer.StorageOptimizer`

#### Class: `StorageOptimizer`

Analyzes S3 storage patterns and provides cost optimization recommendations.

**Methods:**

##### `__init__(s3_client)`
Initialize the StorageOptimizer.
- **Parameters:**
  - `s3_client`: Boto3 S3 client or S3ClientWrapper instance

##### `analyze_bucket_storage(bucket_name, prefix="")`
Analyze storage distribution across storage classes.
- **Parameters:**
  - `bucket_name` (str): Name of the S3 bucket
  - `prefix` (str): Object prefix filter (default: "")
- **Returns:** Dict containing storage analysis results

##### `calculate_cost_savings(current_storage_gb, current_class, target_class)`
Calculate potential cost savings from storage class transition.
- **Parameters:**
  - `current_storage_gb` (float): Current storage size in GB
  - `current_class` (str): Current storage class
  - `target_class` (str): Target storage class
- **Returns:** Dict with cost savings calculation

##### `recommend_lifecycle_policy(bucket_name, access_pattern='media')`
Generate lifecycle policy recommendations based on usage patterns.
- **Parameters:**
  - `bucket_name` (str): Name of the S3 bucket
  - `access_pattern` (str): Type of access pattern (media/archive/backup, default: 'media')
- **Returns:** Dict containing recommended policy

##### `get_optimization_report(bucket_name, prefix="")`
Generate a comprehensive optimization report for a bucket.
- **Parameters:**
  - `bucket_name` (str): Name of the S3 bucket
  - `prefix` (str): Object prefix filter (default: "")
- **Returns:** Dict containing comprehensive report

---

## Configuration Modules

### `src.config.settings.Settings`

#### Class: `Settings`

Application settings manager with support for environment variables and config files.

**Methods:**

##### `__init__(config_file=None)`
Initialize settings.
- **Parameters:**
  - `config_file` (str, optional): Path to JSON configuration file

##### `load_from_file(config_file)`
Load configuration from JSON file.
- **Parameters:**
  - `config_file` (str): Path to JSON configuration file

##### `load_from_env()`
Load configuration from environment variables.

##### `get(key_path, default=None)`
Get configuration value using dot notation.
- **Parameters:**
  - `key_path` (str): Dot-separated path (e.g., 'aws.region')
  - `default`: Default value if key not found
- **Returns:** Configuration value

##### `set(key_path, value)`
Set configuration value using dot notation.
- **Parameters:**
  - `key_path` (str): Dot-separated path
  - `value`: Value to set

##### `to_dict()`
Export configuration as dictionary.
- **Returns:** Configuration dictionary

##### `save_to_file(config_file)`
Save configuration to JSON file.
- **Parameters:**
  - `config_file` (str): Path to save configuration

---

## Utility Modules

### `src.utils.logger`

#### Functions:

##### `setup_logger(name, level='INFO', log_format=None, log_file=None)`
Set up a logger with consistent formatting.
- **Parameters:**
  - `name` (str): Logger name
  - `level` (str): Logging level (default: 'INFO')
  - `log_format` (str, optional): Custom log format string
  - `log_file` (str, optional): File path for file logging
- **Returns:** Configured logger instance

##### `get_logger(name)`
Get an existing logger or create a default one.
- **Parameters:**
  - `name` (str): Logger name
- **Returns:** Logger instance

---

### `src.utils.validators`

#### Functions:

##### `validate_bucket_name(bucket_name)`
Validate S3 bucket name according to AWS rules.
- **Parameters:**
  - `bucket_name` (str): S3 bucket name to validate
- **Returns:** bool

##### `validate_lifecycle_config(lifecycle_config)`
Validate S3 lifecycle configuration.
- **Parameters:**
  - `lifecycle_config` (dict): Lifecycle configuration dictionary
- **Returns:** tuple (is_valid, error_message)

##### `validate_days_config(standard_ia_days, glacier_days, expiration_days=None)`
Validate lifecycle transition days configuration.
- **Parameters:**
  - `standard_ia_days` (int): Days before transition to Standard-IA
  - `glacier_days` (int): Days before transition to Glacier
  - `expiration_days` (int, optional): Days before expiration
- **Returns:** tuple (is_valid, error_message)

##### `validate_storage_class(storage_class)`
Validate S3 storage class name.
- **Parameters:**
  - `storage_class` (str): Storage class name
- **Returns:** bool

---

### `src.utils.formatters`

#### Functions:

##### `format_bytes(bytes_value, precision=2)`
Format bytes into human-readable format.
- **Parameters:**
  - `bytes_value` (int/float): Size in bytes
  - `precision` (int): Decimal precision (default: 2)
- **Returns:** Formatted string (e.g., "1.50 GB")

##### `format_cost(cost, currency='USD')`
Format cost value for display.
- **Parameters:**
  - `cost` (int/float): Cost value
  - `currency` (str): Currency code (default: 'USD')
- **Returns:** Formatted cost string (e.g., "$12.50")

##### `format_percentage(value, precision=2)`
Format percentage value.
- **Parameters:**
  - `value` (int/float): Percentage value
  - `precision` (int): Decimal precision (default: 2)
- **Returns:** Formatted percentage string

##### `format_duration(days)`
Format duration in days to human-readable format.
- **Parameters:**
  - `days` (int): Number of days
- **Returns:** Formatted duration string

---

## Media Management Modules

### `src.media_management.media_processor.MediaProcessor`

#### Class: `MediaProcessor`

Processes and manages media assets for S3 storage.

**Methods:**

##### `__init__(s3_client)`
Initialize the MediaProcessor.
- **Parameters:**
  - `s3_client`: S3ClientWrapper instance

##### `classify_media_type(file_path)`
Classify media file based on extension.
- **Parameters:**
  - `file_path` (str): Path to media file
- **Returns:** MediaType enum value

##### `get_file_metadata(file_path)`
Extract metadata from a file.
- **Parameters:**
  - `file_path` (str): Path to file
- **Returns:** Dict containing file metadata

##### `upload_media_asset(file_path, bucket_name, prefix="", storage_class='STANDARD', add_metadata=True)`
Upload a media asset to S3 with appropriate metadata.
- **Parameters:**
  - `file_path` (str): Local file path
  - `bucket_name` (str): S3 bucket name
  - `prefix` (str): S3 key prefix (default: "")
  - `storage_class` (str): Initial storage class (default: 'STANDARD')
  - `add_metadata` (bool): Whether to add file metadata (default: True)
- **Returns:** bool

##### `batch_upload_media(directory, bucket_name, prefix="", storage_class='STANDARD', media_types=None)`
Batch upload media files from a directory.
- **Parameters:**
  - `directory` (str): Local directory path
  - `bucket_name` (str): S3 bucket name
  - `prefix` (str): S3 key prefix (default: "")
  - `storage_class` (str): Initial storage class (default: 'STANDARD')
  - `media_types` (list, optional): Filter by media types (None = all)
- **Returns:** Dict with upload statistics

##### `recommend_storage_class(file_path, access_frequency='high')`
Recommend storage class based on file characteristics.
- **Parameters:**
  - `file_path` (str): Path to file
  - `access_frequency` (str): Expected access frequency (default: 'high')
- **Returns:** Recommended storage class string

---

### `src.media_management.metadata_manager.MetadataManager`

#### Class: `MetadataManager`

Manages metadata and tags for S3 objects.

**Methods:**

##### `__init__(s3_client)`
Initialize the MetadataManager.
- **Parameters:**
  - `s3_client`: S3ClientWrapper instance

##### `tag_object(bucket_name, object_key, tags)`
Add tags to an S3 object.
- **Parameters:**
  - `bucket_name` (str): S3 bucket name
  - `object_key` (str): S3 object key
  - `tags` (dict): Dictionary of tag key-value pairs
- **Returns:** bool

##### `get_object_tags(bucket_name, object_key)`
Get tags from an S3 object.
- **Parameters:**
  - `bucket_name` (str): S3 bucket name
  - `object_key` (str): S3 object key
- **Returns:** Dict of tags or None

##### `update_object_metadata(bucket_name, object_key, metadata)`
Update metadata for an S3 object.
- **Parameters:**
  - `bucket_name` (str): S3 bucket name
  - `object_key` (str): S3 object key
  - `metadata` (dict): New metadata dictionary
- **Returns:** bool

##### `batch_tag_objects(bucket_name, prefix, tags)`
Batch tag objects with a specific prefix.
- **Parameters:**
  - `bucket_name` (str): S3 bucket name
  - `prefix` (str): Object key prefix
  - `tags` (dict): Tags to apply
- **Returns:** Dict with operation statistics

##### `create_lifecycle_tags(access_pattern='media', retention_years=1)`
Create recommended tags for lifecycle management.
- **Parameters:**
  - `access_pattern` (str): Type of access pattern (default: 'media')
  - `retention_years` (int): Retention period in years (default: 1)
- **Returns:** Dict of recommended tags
