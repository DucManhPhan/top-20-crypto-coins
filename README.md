


<br>

## Table of Contents
- [Given problem](#given-problem)
- [The structure of the project](#the-structure-of-the-project)
- [How to run the project](#how-to-run-the-project)
- [Schema of crypto-coins table](#schema-of-crypto-coins-table)
- []()
- []()
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

### Cài đặt

1. Clone repository này về máy của bạn
2. Cài đặt Terraform (phiên bản 1.0.0 trở lên)
3. Cài đặt AWS CLI và cấu hình credentials

### Cấu hình API key

1. Đăng ký tài khoản CoinMarketCap và lấy API key
2. Tạo file `terraform.tfvars` từ file mẫu `terraform.tfvars.example`:
   ```bash
   cd infra/base-deployment
   cp terraform.tfvars.example terraform.tfvars
   ```
3. Cập nhật giá trị API key trong file `terraform.tfvars`:
   ```
   cmc_password = "your_actual_api_key_here"
   ```

### Triển khai

1. Di chuyển vào thư mục `infra/base-deployment`:
   ```bash
   cd infra/base-deployment
   ```

2. Khởi tạo Terraform:
   ```bash
   terraform init
   ```

3. Kiểm tra các tài nguyên sẽ được tạo:
   ```bash
   terraform plan
   ```

4. Triển khai các tài nguyên:
   ```bash
   terraform apply
   ```

5. Để xóa các tài nguyên khi không cần nữa:
   ```bash
   terraform destroy
   ```

<br>

## Schema of crypto-coins table

Below is the schema of the table `crypto_coins`:

```json
{
  "id": "string", // Primary key - ID của a coin CoinMarketCap
  "timestamp": "number", // Sort key - The time that get data from CoinMarketCap (Unix timestamp)
  "name": "string", // The name of a coin like Bitcoin, Ethereum, ...
  "symbol": "string", // The symbol of a coin like BTC, ETH, ...
  "price_usd": "number", // The price by USD
  "market_cap": "number", // The market cap of a coin
  "volume_24h": "number", // The volume during 24h
  "percent_change_24h": "number", // The percent changes during 24h
  "rank": "number" // The rank of a coin in CoinMarketCap
}
```


<br>

## Wrapping up



