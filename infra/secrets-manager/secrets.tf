
resource "aws_secretsmanager_secret" "cmc_api_key" {
  name = "${var.cmc_api_key_name}"
}

resource "aws_secretsmanager_secret_version" "cmc_api_key_version" {
  secret_id     = aws_secretsmanager_secret.cmc_api_key.id
  secret_string = "${var.cmc_api_key}"
}