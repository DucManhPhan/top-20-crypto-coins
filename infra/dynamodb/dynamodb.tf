resource "aws_dynamodb_table" "dynamodb" {
  name = var.dynamodb_table_name
  billing_mode = var.billing_mode
  read_capacity = var.read_capacity
  write_capacity = var.write_capacity
  hash_key = var.hash_key
  range_key = var.range_key

  attribute {
    name = var.hash_key
    type = "S"  # String type for id
  }

  attribute {
    name = var.range_key
    type = "N"  # Number type for timestamp
  }

  point_in_time_recovery {
    enabled = true
  }

  tags = {
    Name = "CryptoCoinsPricing"
    Description = "Table storing top 20 crypto coins pricing data from CoinMarketCap"
  }
}