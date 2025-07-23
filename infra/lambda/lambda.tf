data "archive_file" "make_zip" {
  type        = "zip"
  source_file = "../../backend/top_20_crypto_coins.py"
  output_path = "top_20_crypto_coins.zip"
}

resource "aws_lambda_function" "top_20_crypto_coins" {
  function_name    = "top_20_crypto_coins"
  filename         = data.archive_file.make_zip.output_path
  source_code_hash = data.archive_file.make_zip.output_base64sha256
  handler          = "top_20_crypto_coins.lambda_handler"
  runtime          = "python3.13"
  role             = aws_iam_role.lambda_iam_role.arn
  timeout          = 30
  memory_size      = 128
  
  environment {
    variables = {
      CMC_API_KEY_NAME = var.cmc_api_key_name
      DYNAMODB_TABLE   = var.dynamodb_table_name
    }
  }
}

# CloudWatch Event Rule to run Lambda after 4 hours
resource "aws_cloudwatch_event_rule" "every_four_hours" {
  name                = "every-four-hours"
  description         = "Fires every 4 hours"
  schedule_expression = "rate(4 hours)"
}

resource "aws_cloudwatch_event_target" "run_lambda_every_four_hours" {
  rule      = aws_cloudwatch_event_rule.every_four_hours.name
  target_id = "top_20_crypto_coins"
  arn       = aws_lambda_function.top_20_crypto_coins.arn
}

# Allow CloudWatch Events to call Lambda
resource "aws_lambda_permission" "allow_cloudwatch" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.top_20_crypto_coins.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.every_four_hours.arn
}