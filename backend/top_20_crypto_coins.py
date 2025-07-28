import json
import os
import time
import boto3
import urllib.request
import urllib.parse
from datetime import datetime
from decimal import Decimal

CMC_API_KEY_NAME = os.environ.get("CMC_API_KEY_NAME")
DYNAMODB_TABLE = os.environ.get("DYNAMODB_TABLE")
CMC_API_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"


def lambda_handler(event, context):
    """
    AWS Lambda function handler to get top 20 crypto coins and save to DynamoDB
    """
    print(
        f"[LAMBDA_HANDLER] Starting to pull crypto coins from CoinMarketCap "
        f"at {datetime.now().isoformat()}"
    )
    print(
        f"[LAMBDA_HANDLER] Environment variables - CMC_API_KEY_NAME: "
        f"{CMC_API_KEY_NAME}, DYNAMODB_TABLE: {DYNAMODB_TABLE}"
    )

    try:
        print("[LAMBDA_HANDLER] Step 1: Getting crypto coins from API")
        coins = get_top_crypto_coins()

        if not coins:
            print("[LAMBDA_HANDLER] No coins data received from API")
            return {
                "statusCode": 500,
                "body": json.dumps("Cannot get data from CoinMarketCap"),
            }

        print(
            f"[LAMBDA_HANDLER] Step 2: Received {len(coins)} coins, saving to DynamoDB"
        )
        save_to_dynamodb(coins)

        print("[LAMBDA_HANDLER] Step 3: Successfully completed processing")
        return {
            "statusCode": 200,
            "body": json.dumps(f"Saved data of {len(coins)} crypto coins successfully"),
        }
    except Exception as e:
        print(f"[LAMBDA_HANDLER] Error in main flow: {e}")
        return {"statusCode": 500, "body": json.dumps(f"Error: {str(e)}")}


def get_api_key_from_cmc():
    """
    Get API Key from CoinMarketCap
    """
    print(f"[GET_API_KEY] Getting API key from Secrets Manager: " f"{CMC_API_KEY_NAME}")
    client = boto3.client("secretsmanager")
    try:
        response = client.get_secret_value(SecretId=CMC_API_KEY_NAME)
        secret = response["SecretString"]
        print("[GET_API_KEY] Successfully retrieved API key")
        return secret
    except Exception as e:
        print(f"[GET_API_KEY] Error when getting secret: {e}")
        raise e


def get_top_crypto_coins():
    """
    Get information of 20 crypto coins from CoinMarketCap API using urllib
    """
    print("[GET_CRYPTO_COINS] Starting to get crypto coins data")
    apiKey = get_api_key_from_cmc()

    # Build URL with parameters
    params = {"start": "1", "limit": "20", "convert": "USD"}
    url = CMC_API_URL + "?" + urllib.parse.urlencode(params)
    print(f"[GET_CRYPTO_COINS] API URL: {url}")

    try:
        # Create request with headers
        req = urllib.request.Request(url)
        req.add_header("X-CMC_PRO_API_KEY", apiKey)
        req.add_header("Accept", "application/json")
        print("[GET_CRYPTO_COINS] Making API request to CoinMarketCap")

        # Make the request
        with urllib.request.urlopen(req) as response:  # nosec B310
            print(f"[GET_CRYPTO_COINS] API Response Status: {response.status}")
            response_data = response.read().decode("utf-8")
            data = json.loads(response_data)

            if response.status != 200:
                error_msg = data.get("status", {}).get("error_message", "Unknown error")
                print(f"[GET_CRYPTO_COINS] API Error: {error_msg}")
                return []

            coins_data = data.get("data", [])
            print(f"[GET_CRYPTO_COINS] Successfully received {len(coins_data)} coins")

            return coins_data
    except Exception as e:
        print(f"[GET_CRYPTO_COINS] Error when calling API CoinMarketCap: {e}")
        return []


def save_to_dynamodb(coins):
    """
    Save the top 20 crypto coins information to DynamoDB
    """
    print(
        f"[SAVE_TO_DYNAMODB] Starting to save {len(coins)} coins to "
        f"DynamoDB table: {DYNAMODB_TABLE}"
    )

    if not coins:
        print("[SAVE_TO_DYNAMODB] No data to save")
        return

    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(DYNAMODB_TABLE)
    current_timestamp = int(time.time())
    print(f"[SAVE_TO_DYNAMODB] Using timestamp: {current_timestamp}")

    try:
        saved_count = 0
        for coin in coins:
            coin_name = coin.get("name", "Unknown")
            coin_id = coin.get("id", "Unknown")
            print(
                f"[SAVE_TO_DYNAMODB] Processing coin {saved_count + 1}/"
                f"{len(coins)}: {coin_name} (ID: {coin_id})"
            )

            quote = coin.get("quote", {}).get("USD", {})

            item = {
                "id": str(coin.get("id", "")),
                "timestamp": current_timestamp,
                "name": coin.get("name", ""),
                "symbol": coin.get("symbol", ""),
                "price_usd": Decimal(str(quote.get("price", 0))),
                "market_cap": Decimal(str(quote.get("market_cap", 0))),
                "volume_24h": Decimal(str(quote.get("volume_24h", 0))),
                "percent_change_24h": Decimal(str(quote.get("percent_change_24h", 0))),
                "rank": int(coin.get("cmc_rank", 0)),
            }

            table.put_item(Item=item)
            saved_count += 1
            price = quote.get("price", "N/A")
            print(f"[SAVE_TO_DYNAMODB] Successfully saved {coin_name} (${price})")

        print(f"[SAVE_TO_DYNAMODB] Completed saving {saved_count} coins to DynamoDB")
    except Exception as e:
        print(f"[SAVE_TO_DYNAMODB] Error when saving data into DynamoDB: {e}")
        raise e
