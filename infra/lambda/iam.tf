
resource "aws_iam_role" "lambda_iam_role" {
    name = "lambda_iam_role"
    assume_role_policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
        {
            Action = "sts:AssumeRole"
            Effect = "Allow"
            Principal = {
            Service = "lambda.amazonaws.com"
            }
        }
        ]
    })
}

resource "aws_iam_policy_attachment" "dynamodb_policy" {
    name       = "dynamodb_policy"
    roles      = [aws_iam_role.lambda_iam_role.name]
    policy_arn = "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
}

resource "aws_iam_policy_attachment" "secretsmanager_policy" {
    name       = "secretsmanager_policy"
    roles      = [aws_iam_role.lambda_iam_role.name]
    policy_arn = "arn:aws:iam::aws:policy/SecretsManagerReadWrite"
}

resource "aws_iam_policy_attachment" "cloudwatch_logs_policy" {
    name       = "cloudwatch_logs_policy"
    roles      = [aws_iam_role.lambda_iam_role.name]
    policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}