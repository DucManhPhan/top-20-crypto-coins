import os
import pytest

@pytest.fixture(autouse=True)
def setup_test_env():
    """Setup test environment variables"""
    os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
    os.environ['CMC_API_KEY_NAME'] = 'test-api-key'
    os.environ['DYNAMODB_TABLE'] = 'test-crypto-coins'