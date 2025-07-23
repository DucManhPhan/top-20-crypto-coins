variable "dynamodb_table_name" {
  type = string
  description = "Name of the DynamoDB table"
}

variable "billing_mode" {
  type = string
  description = "Billing mode for the DynamoDB table (e.g., PAY_PER_REQUEST, PROVISIONED)"
  default = "PROVISIONED"
}

variable "read_capacity" {
  type = number
  description = "Read capacity units for the DynamoDB table"
  default = 10
}

variable "write_capacity" {
  type = number
  description = "Write capacity units for the DynamoDB table"
  default = 10
}

variable "hash_key" {
  type = string
  description = "Hash key for the DynamoDB table"
}

variable "range_key" {
  type = string
  description = "Range key for the DynamoDB table"
}