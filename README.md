


<br>

## Table of Contents
- [Given problem](#given-problem)
- [The structure of the project](#the-structure-of-the-project)
- [How to run the project](#how-to-run-the-project)
- []()
- []()
- [Wrapping up](#wrapping-up)


<br>

## Given problem

1. Study terraform and its CLI commands.
2. Create a terraform project that create these resources on AWS provider:

    - IAM role.
    - Lambda
    - Secret
    - S3 resource / DynamoDB

3. Lambda should be able to run by manually trigger & by schedule (every 4 hours) to pull top 20 crytpo coins pricing from CoinMarketCap (using free tier API) and write it to S3/DynamoDB table.
4. CoinMarketCap API creds should be stored in Secrets, and Lambda should be consume API creds from it.
5. All resources should be created/destroyed from Terraform CLI commands (terraform apply, terraform destroy).


<br>

## The structure of the project




<br>

## How to run the project




<br>

## Wrapping up



