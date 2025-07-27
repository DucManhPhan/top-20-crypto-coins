
# CoinMarketCap API Key configuration
cmc_api_key_name = "cmc_api_key_v9"
cmc_api_key = "<value_of_your_cmc_api_key>"

# DynamoDB's configuration
dynamodb_table_name = "crypto_coins"
billing_mode = "PROVISIONED"
read_capacity = 10
write_capacity = 10
hash_key = "id"
range_key = "timestamp"