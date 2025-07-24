data "archive_file" "make_zip" {
  type        = "zip"
  source_file = "../../backend/top_20_crypto_coins.py"
  output_path = "top_20_crypto_coins.zip"
}

resource "null_resource" "build_lambda_layer" {
  provisioner "local-exec" {
    command     = "python create_lambda_layer.py"
    working_dir = "${path.module}/lambda-layer"
  }
  
  triggers = {
    requirements = filemd5("${path.module}/lambda-layer/requirements.txt")
    script       = filemd5("${path.module}/lambda-layer/create_lambda_layer.py")
  }
}

resource "aws_lambda_layer_version" "lambda_layer" {
  filename            = "${path.module}/lambda-layer.zip"
  layer_name          = "crypto-coins-dependencies"
  source_code_hash    = filebase64sha256("${path.module}/lambda-layer.zip")

  compatible_runtimes = ["python3.9"]
  description         = "Dependencies for crypto coins Lambda function"
  
  depends_on = [null_resource.build_lambda_layer]
}

resource "aws_lambda_function" "top_20_crypto_coins" {
  function_name    = "top_20_crypto_coins"
  filename         = data.archive_file.make_zip.output_path
  source_code_hash = data.archive_file.make_zip.output_base64sha256
  layers           = [aws_lambda_layer_version.lambda_layer.arn]
  handler          = "top_20_crypto_coins.lambda_handler"
  runtime          = "python3.9"
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

# Allow CloudWatch Events to call Lambda
resource "aws_lambda_permission" "allow_cloudwatch" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.top_20_crypto_coins.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.every_four_hours.arn
}

# CloudWatch Event Rule to run Lambda every 4 hours
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