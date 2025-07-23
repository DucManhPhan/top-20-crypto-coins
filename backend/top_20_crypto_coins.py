import json
import os
import time
import boto3
import requests
from datetime import datetime

CMC_API_KEY_NAME = os.environ.get('CMC_API_KEY_NAME')
DYNAMODB_TABLE = os.environ.get('DYNAMODB_TABLE')
CMC_API_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

def lambda_handler(event, context):
    """
    AWS Lambda function handler to get top 20 crypto coins and save to DynamoDB
    """
    print(f"Starting to pull crypto coins from CoinMarketCap at {datetime.now().isoformat()}")

    try:
        coins = get_top_crypto_coins()
        
        if not coins:
            return {
                'statusCode': 500,
                'body': json.dumps('Cannot get data from CoinMarketCap')
            }

        save_to_dynamodb(coins)
        
        return {
            'statusCode': 200,
            'body': json.dumps(f'Saved data of {len(coins)} crypto coins successfully')
        }
    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }

def get_api_key_from_cmc():
    """
    Get API Key from CoinMarketCap
    """
    client = boto3.client('secretsmanager')
    try:
        response = client.get_secret_value(SecretId=CMC_API_KEY_NAME)
        secret = response['SecretString']

        return secret
    except Exception as e:
        print(f"Error when getting secret: {e}")
        raise e

def get_top_crypto_coins():
    """
    Get information of 20 crypto coins from CoinMarketCap API
    """
    apiKey = get_api_key_from_cmc()

    headers = {
        'X-CMC_PRO_API_KEY': apiKey,
        'Accept': 'application/json'
    }

    params = {
        'start': '1',
        'limit': '20',
        'convert': 'USD'
    }
    
    try:
        response = requests.get(CMC_API_URL, headers=headers, params=params)
        data = response.json()
        
        if response.status_code != 200:
            print(f"Error API: {data.get('status', {}).get('error_message', 'Unknown error')}")
            return []

        return data.get('data', [])
    except Exception as e:
        print(f"Error when calling API CoinMarketCap: {e}")
        return []

def save_to_dynamodb(coins):
    """
    Save the top 20 crypto coins information to DynamoDB
    """
    if not coins:
        print("There is no data to save.")
        return
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(DYNAMODB_TABLE)
    current_timestamp = int(time.time())
    
    try:
        for coin in coins:
            quote = coin.get('quote', {}).get('USD', {})
            
            item = {
                'coin_id': str(coin.get('id', '')),
                'timestamp': current_timestamp,
                'name': coin.get('name', ''),
                'symbol': coin.get('symbol', ''),
                'price_usd': float(quote.get('price', 0)),
                'market_cap': float(quote.get('market_cap', 0)),
                'volume_24h': float(quote.get('volume_24h', 0)),
                'percent_change_24h': float(quote.get('percent_change_24h', 0)),
                'rank': int(coin.get('cmc_rank', 0))
            }
            
            table.put_item(Item=item)
            print(f"Saved data of {coin.get('name', '')}")
    except Exception as e:
        print(f"Error when saving data into DynamoDB: {e}")
        raise e