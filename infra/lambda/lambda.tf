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

# TESTING ONLY: CloudWatch Event Rule to run Lambda once after 5 minutes
# This rule will trigger the Lambda function once, 5 minutes after deployment
# DELETE THIS SECTION after testing and uncomment the 4-hour schedule below for production use
resource "aws_cloudwatch_event_rule" "run_once_after_five_minutes" {
  name                = "run-once-after-five-minutes"
  description         = "Fires once after 5 minutes from creation"
  schedule_expression = "at(${timeadd(timestamp(), "5m")})" # Runs once 5 minutes from now
}

# TESTING ONLY: Target for the one-time execution rule
# DELETE THIS SECTION after testing and uncomment the 4-hour schedule below
resource "aws_cloudwatch_event_target" "run_lambda_once" {
  rule      = aws_cloudwatch_event_rule.run_once_after_five_minutes.name
  target_id = "top_20_crypto_coins"
  arn       = aws_lambda_function.top_20_crypto_coins.arn
}

# Allow CloudWatch Events to call Lambda
# NOTE: Keep this permission resource but update the source_arn when switching to the 4-hour schedule
resource "aws_lambda_permission" "allow_cloudwatch" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.top_20_crypto_coins.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.run_once_after_five_minutes.arn
}

# PRODUCTION CONFIGURATION: CloudWatch Event Rule to run Lambda every 4 hours
# UNCOMMENT THIS SECTION after testing and DELETE the 5-minute one-time execution above
# resource "aws_cloudwatch_event_rule" "every_four_hours" {
#   name                = "every-four-hours"
#   description         = "Fires every 4 hours"
#   schedule_expression = "rate(4 hours)"
# }
# 
# resource "aws_cloudwatch_event_target" "run_lambda_every_four_hours" {
#   rule      = aws_cloudwatch_event_rule.every_four_hours.name
#   target_id = "top_20_crypto_coins"
#   arn       = aws_lambda_function.top_20_crypto_coins.arn
# }
#
# IMPORTANT: When uncommenting this section, update the source_arn in the aws_lambda_permission resource above