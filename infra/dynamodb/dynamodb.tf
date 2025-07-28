resource "aws_dynamodb_table" "dynamodb" {
  name           = var.dynamodb_table_name
  billing_mode   = var.billing_mode
  read_capacity  = var.read_capacity
  write_capacity = var.write_capacity
  hash_key       = var.hash_key
  range_key      = var.range_key

  attribute {
    name = var.hash_key
    type = "S" # String type for id
  }

  attribute {
    name = var.range_key
    type = "N" # Number type for timestamp
  }

  point_in_time_recovery {
    enabled = true
  }

  tags = {
    Name         = "CryptoCoinsPricing"
    Environment  = "production"
    Project      = "crypto-coins-tracker"
    Owner        = "data-team"
    Purpose      = "crypto-data-storage"
    BackupPolicy = "automated"
    Description  = "Table storing top 20 crypto coins pricing data from CoinMarketCap"
  }
}

# DynamoDB Backup Vault for automated backups
resource "aws_backup_vault" "crypto_coins_backup_vault" {
  name        = "crypto-coins-backup-vault"
  kms_key_arn = aws_kms_key.backup_key.arn

  tags = {
    Name        = "crypto-coins-backup-vault"
    Environment = "production"
    Project     = "crypto-coins-tracker"
    Purpose     = "data-backup"
  }
}

# KMS key for backup encryption
resource "aws_kms_key" "backup_key" {
  description             = "KMS key for crypto coins backup encryption"
  deletion_window_in_days = 7

  tags = {
    Name        = "crypto-coins-backup-key"
    Environment = "production"
    Project     = "crypto-coins-tracker"
    Purpose     = "backup-encryption"
  }
}

resource "aws_kms_alias" "backup_key_alias" {
  name          = "alias/crypto-coins-backup"
  target_key_id = aws_kms_key.backup_key.key_id
}

# IAM role for AWS Backup
resource "aws_iam_role" "backup_role" {
  name = "crypto-coins-backup-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "backup.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Name        = "crypto-coins-backup-role"
    Environment = "production"
    Project     = "crypto-coins-tracker"
    Purpose     = "backup-service-role"
  }
}

resource "aws_iam_role_policy_attachment" "backup_policy" {
  role       = aws_iam_role.backup_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSBackupServiceRolePolicyForBackup"
}

# Backup plan for DynamoDB
resource "aws_backup_plan" "crypto_coins_backup_plan" {
  name = "crypto-coins-backup-plan"

  rule {
    rule_name         = "daily_backup"
    target_vault_name = aws_backup_vault.crypto_coins_backup_vault.name
    schedule          = "cron(0 2 * * ? *)"

    lifecycle {
      cold_storage_after = 30
      delete_after       = 120
    }

    recovery_point_tags = {
      Environment = "production"
      Project     = "crypto-coins-tracker"
      BackupType  = "automated"
    }
  }

  tags = {
    Name        = "crypto-coins-backup-plan"
    Environment = "production"
    Project     = "crypto-coins-tracker"
    Purpose     = "automated-backup"
  }
}

# Backup selection for DynamoDB table
resource "aws_backup_selection" "crypto_coins_backup_selection" {
  iam_role_arn = aws_iam_role.backup_role.arn
  name         = "crypto-coins-backup-selection"
  plan_id      = aws_backup_plan.crypto_coins_backup_plan.id

  resources = [
    aws_dynamodb_table.dynamodb.arn
  ]

  condition {
    string_equals {
      key   = "aws:ResourceTag/BackupPolicy"
      value = "automated"
    }
  }
}