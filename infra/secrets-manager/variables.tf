
variable "cmc_api_key_name" {
  description = "Name of the CoinMarketCap's API Key in AWS Secrets Manager"
  type        = string
}

variable "cmc_api_key" {
  description = "The API Key of CoinMarketCap API"
  type        = string
}