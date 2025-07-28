
module "secrets_manager" {
  source = "../secrets-manager"

  cmc_api_key      = var.cmc_api_key
  cmc_api_key_name = var.cmc_api_key_name
}

module "dynamodb" {
  source = "../dynamodb"

  dynamodb_table_name = var.dynamodb_table_name
  billing_mode        = var.billing_mode
  read_capacity       = var.read_capacity
  write_capacity      = var.write_capacity
  hash_key            = var.hash_key
  range_key           = var.range_key
}

module "lambda" {
  source = "../lambda"

  cmc_api_key_name    = var.cmc_api_key_name
  dynamodb_table_name = var.dynamodb_table_name
}