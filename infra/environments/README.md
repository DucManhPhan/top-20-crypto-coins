# Multi-Environment Infrastructure

This directory contains environment-specific Terraform configurations for the crypto coins project.

## Environment Structure

```
environments/
├── dev/          # Development environment
├── staging/      # Staging environment  
└── prod/         # Production environment
```

## Environment Configurations

### Development (dev)
- **DynamoDB**: PAY_PER_REQUEST billing
- **Lambda**: Basic configuration
- **Resources**: `dev-` prefix
- **Auto-deploy**: On push to `develop` branch

### Staging (staging)
- **DynamoDB**: PROVISIONED (5 RCU/WCU)
- **Lambda**: Production-like settings
- **Resources**: `staging-` prefix
- **Auto-deploy**: On push to `main` branch

### Production (prod)
- **DynamoDB**: PROVISIONED (20 RCU/WCU)
- **Lambda**: Optimized configuration
- **Resources**: `prod-` prefix
- **Deploy**: Manual approval required

## Deployment Flow

```
develop branch → dev environment (auto)
main branch → staging environment (auto) → prod environment (manual approval)
```

## Manual Deployment

Use GitHub Actions workflow dispatch to deploy to any environment:
1. Go to Actions tab
2. Select "Multi-Environment CI/CD Pipeline"
3. Choose environment and action
4. Run workflow

## State Management

Each environment has separate Terraform state files:
- `crypto-coins/dev/terraform.tfstate`
- `crypto-coins/staging/terraform.tfstate`
- `crypto-coins/prod/terraform.tfstate`

## Resource Naming

Resources are prefixed with environment name:
- Dev: `dev-crypto-coins`, `dev-cmc-api-key`
- Staging: `staging-crypto-coins`, `staging-cmc-api-key`
- Prod: `prod-crypto-coins`, `prod-cmc-api-key`