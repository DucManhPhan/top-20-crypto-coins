resource "aws_secretsmanager_secret" "cmc_api" {
  name = "cmc_api_creds"
}

resource "aws_secretsmanager_secret_version" "cmc_api_version" {
  secret_id     = aws_secretsmanager_secret.cmc_api.id
  secret_string = jsonencode({
    username = var.cmc_username
    password = var.cmc_password
  })
}