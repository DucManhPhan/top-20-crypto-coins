terraform {
  backend "s3" {
    key    = "crypto-coins/staging/terraform.tfstate"
    region = "ap-southeast-1"
  }
}

module "crypto_coins" {
  source = "../../base-deployment"

  # Environment-specific variables
  cmc_api_key_name    = "staging-cmc-api-key"
  cmc_api_key         = var.cmc_api_key
  dynamodb_table_name = "staging-crypto-coins"
  billing_mode        = "PROVISIONED"
  read_capacity       = 5
  write_capacity      = 5
  hash_key            = "id"
  range_key           = "timestamp"
}

variable "cmc_api_key" {
  description = "CoinMarketCap API Key"
  type        = string
  sensitive   = true
}