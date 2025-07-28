output "backup_vault_arn" {
  description = "ARN of the backup vault"
  value       = aws_backup_vault.crypto_coins_backup_vault.arn
}

output "backup_plan_arn" {
  description = "ARN of the backup plan"
  value       = aws_backup_plan.crypto_coins_backup_plan.arn
}

output "dynamodb_table_arn" {
  description = "ARN of the DynamoDB table"
  value       = aws_dynamodb_table.dynamodb.arn
}