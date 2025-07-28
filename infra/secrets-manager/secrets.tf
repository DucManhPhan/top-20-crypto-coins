
resource "aws_secretsmanager_secret" "cmc_api_key" {
  name = var.cmc_api_key_name

  tags = {
    Name        = "coinmarketcap-api-key"
    Environment = "production"
    Project     = "crypto-coins-tracker"
    Purpose     = "api-credentials"
    Sensitive   = "true"
  }
}

resource "aws_secretsmanager_secret_version" "cmc_api_key_version" {
  secret_id     = aws_secretsmanager_secret.cmc_api_key.id
  secret_string = var.cmc_api_key
}