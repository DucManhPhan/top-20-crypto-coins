output "lambda_function_arn" {
  description = "ARN of the Lambda function"
  value       = aws_lambda_function.top_20_crypto_coins.arn
}

output "lambda_alias_arn" {
  description = "ARN of the Lambda alias"
  value       = aws_lambda_alias.live.arn
}

output "lambda_function_name" {
  description = "Name of the Lambda function"
  value       = aws_lambda_function.top_20_crypto_coins.function_name
}

output "lambda_layer_arn" {
  value = aws_lambda_layer_version.lambda_layer.arn
}