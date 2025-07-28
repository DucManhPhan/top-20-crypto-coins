terraform {
  backend "s3" {
    key    = "crypto-coins/dev/terraform.tfstate"
    region = "ap-southeast-1"
  }
}

module "crypto_coins" {
  source = "../../base-deployment"

  # Environment-specific variables
  cmc_api_key_name    = "dev-cmc-api-key"
  cmc_api_key         = var.cmc_api_key
  dynamodb_table_name = "dev-crypto-coins"
  billing_mode        = "PAY_PER_REQUEST"
  hash_key            = "id"
  range_key           = "timestamp"
}

variable "cmc_api_key" {
  description = "CoinMarketCap API Key"
  type        = string
  sensitive   = true
}