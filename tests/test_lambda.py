import json
import os
import sys
import pytest
import boto3
from moto import mock_aws
from unittest.mock import patch, MagicMock

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))
import top_20_crypto_coins  # noqa: E402


@pytest.fixture
def mock_env():
    """Mock environment variables"""
    os.environ["CMC_API_KEY_NAME"] = "test-api-key"
    os.environ["DYNAMODB_TABLE"] = "test-crypto-coins"


@mock_aws
def test_get_api_key_from_cmc(mock_env):
    """Test getting API key from Secrets Manager"""
    with patch.object(top_20_crypto_coins, 'CMC_API_KEY_NAME', 'test-api-key'):
        client = boto3.client("secretsmanager", region_name="ap-southeast-1")
        client.create_secret(Name="test-api-key", SecretString="test-key-123")

        result = top_20_crypto_coins.get_api_key_from_cmc()
        assert result == "test-key-123"


@mock_aws
def test_save_to_dynamodb(mock_env):
    """Test saving coins to DynamoDB"""
    with patch.object(top_20_crypto_coins, 'DYNAMODB_TABLE', 'test-crypto-coins'):
        # Create mock DynamoDB table
        dynamodb = boto3.resource("dynamodb", region_name="ap-southeast-1")
        table = dynamodb.create_table(
            TableName="test-crypto-coins",
            KeySchema=[
                {"AttributeName": "id", "KeyType": "HASH"},
                {"AttributeName": "timestamp", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "id", "AttributeType": "S"},
                {"AttributeName": "timestamp", "AttributeType": "N"},
            ],
            BillingMode="PAY_PER_REQUEST",
        )

        # Mock coin data
        coins = [
            {
                "id": 1,
                "name": "Bitcoin",
                "symbol": "BTC",
                "cmc_rank": 1,
                "quote": {
                    "USD": {
                        "price": 50000,
                        "market_cap": 1000000000,
                        "volume_24h": 50000000,
                        "percent_change_24h": 2.5,
                    }
                },
            }
        ]

        top_20_crypto_coins.save_to_dynamodb(coins)

        # Verify data was saved
        response = table.scan()
        assert len(response["Items"]) == 1
        assert response["Items"][0]["name"] == "Bitcoin"


@patch("urllib.request.urlopen")
@patch("top_20_crypto_coins.get_api_key_from_cmc")
def test_get_top_crypto_coins_success(mock_get_key, mock_urlopen, mock_env):
    """Test successful API call to get crypto coins"""
    mock_get_key.return_value = "test-key"

    # Mock API response
    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.read.return_value = json.dumps(
        {
            "data": [
                {
                    "id": 1,
                    "name": "Bitcoin",
                    "symbol": "BTC",
                    "cmc_rank": 1,
                    "quote": {"USD": {"price": 50000}},
                }
            ]
        }
    ).encode("utf-8")
    mock_urlopen.return_value.__enter__.return_value = mock_response

    result = top_20_crypto_coins.get_top_crypto_coins()
    assert len(result) == 1
    assert result[0]["name"] == "Bitcoin"


@patch("urllib.request.urlopen")
@patch("top_20_crypto_coins.get_api_key_from_cmc")
def test_get_top_crypto_coins_api_error(mock_get_key, mock_urlopen, mock_env):
    """Test API error handling"""
    mock_get_key.return_value = "test-key"

    # Mock API error response
    mock_response = MagicMock()
    mock_response.status = 400
    mock_response.read.return_value = json.dumps(
        {"status": {"error_message": "Invalid API key"}}
    ).encode("utf-8")
    mock_urlopen.return_value.__enter__.return_value = mock_response

    result = top_20_crypto_coins.get_top_crypto_coins()
    assert result == []


@patch("top_20_crypto_coins.save_to_dynamodb")
@patch("top_20_crypto_coins.get_top_crypto_coins")
def test_lambda_handler_success(mock_get_coins, mock_save, mock_env):
    """Test successful lambda handler execution"""
    mock_get_coins.return_value = [{"id": 1, "name": "Bitcoin"}]
    mock_save.return_value = None

    result = top_20_crypto_coins.lambda_handler({}, {})

    assert result["statusCode"] == 200
    assert "Saved data of 1 crypto coins successfully" in result["body"]


@patch("top_20_crypto_coins.get_top_crypto_coins")
def test_lambda_handler_no_data(mock_get_coins, mock_env):
    """Test lambda handler when no data is received"""
    mock_get_coins.return_value = []

    result = top_20_crypto_coins.lambda_handler({}, {})

    assert result["statusCode"] == 500
    assert "Cannot get data from CoinMarketCap" in result["body"]
