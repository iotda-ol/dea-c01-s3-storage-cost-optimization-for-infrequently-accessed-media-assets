# Configuration Template

This is a template for the application configuration file.

Copy this file to `config.json` and customize as needed:

```bash
cp config.template.json config.json
```

## Configuration Options

### AWS Settings
- **region**: AWS region to use (default: "us-east-1")
- **profile**: AWS CLI profile name (default: null, uses default profile)

### Lifecycle Settings
- **standard_ia_days**: Days before transitioning to Standard-IA (min: 30)
- **glacier_days**: Days before transitioning to Glacier (min: 90)
- **deep_archive_days**: Days before transitioning to Deep Archive (min: 180)
- **expiration_days**: Days before object expiration (0 = no expiration)

### Logging Settings
- **level**: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- **format**: Python logging format string

### Monitoring Settings
- **enabled**: Enable monitoring (true/false)
- **interval_hours**: Monitoring check interval in hours

## Environment Variables

You can override any configuration value using environment variables:

- `AWS_REGION` - AWS region
- `AWS_PROFILE` - AWS profile name
- `STANDARD_IA_DAYS` - Days before Standard-IA transition
- `GLACIER_DAYS` - Days before Glacier transition
- `EXPIRATION_DAYS` - Days before expiration
- `LOG_LEVEL` - Logging level

Environment variables take precedence over configuration file values.
