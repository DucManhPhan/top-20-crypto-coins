# GitHub Workflows

This directory contains separate workflow files for better organization and maintainability.

## Workflow Files

### 1. `test.yml` - Unit Testing
- **Triggers**: Push to main/develop, PRs to main
- **Purpose**: Run unit tests and coverage reports
- **Dependencies**: None

### 2. `code-quality.yml` - Code Quality Checks
- **Triggers**: Push to main/develop, PRs to main  
- **Purpose**: Code formatting, linting, security checks, Terraform validation
- **Dependencies**: None

### 3. `terraform.yml` - Infrastructure Deployment
- **Triggers**: Push to main, manual dispatch
- **Purpose**: Deploy/destroy AWS infrastructure
- **Dependencies**: None (runs independently)

### 4. `integration-test.yml` - Integration Testing
- **Triggers**: After successful terraform deployment
- **Purpose**: Test deployed Lambda function and verify data
- **Dependencies**: Terraform workflow completion

### 5. `deploy.yml` - Main Pipeline Orchestrator
- **Triggers**: Push to main, PRs to main
- **Purpose**: Provide overview and coordination
- **Dependencies**: None

## Workflow Execution Flow

```
PR Created/Updated:
├── test.yml (Unit Tests)
├── code-quality.yml (Linting/Formatting)
└── deploy.yml (Summary)

Push to main:
├── test.yml (Unit Tests)
├── code-quality.yml (Code Quality)
├── terraform.yml (Deploy Infrastructure)
└── integration-test.yml (Test Deployment)
```

## Manual Operations

Use `terraform.yml` workflow dispatch for:
- `plan`: Review infrastructure changes
- `apply`: Deploy infrastructure manually
- `destroy`: Remove all AWS resources

## Benefits of Separation

- **Parallel execution**: Tests and quality checks run simultaneously
- **Easier maintenance**: Each workflow has single responsibility
- **Better debugging**: Isolated failure points
- **Flexible triggers**: Different workflows for different events
- **Reusability**: Individual workflows can be triggered independently