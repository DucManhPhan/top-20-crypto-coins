
module "secrets_manager" {
  source = "../secrets-manager"
  cmc_username = var.cmc_username
  cmc_password = var.cmc_password
}

module "dynamodb" {
  source = "../dynamodb"
}