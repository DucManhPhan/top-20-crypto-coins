
variable "cmc_api_key_name" {
  description = "Name of the secret in AWS Secrets Manager"
  type        = string
}

variable "dynamodb_table_name" {
  description = "Name of the DynamoDB table"
  type        = string
  default     = "crypto_coins"
}
