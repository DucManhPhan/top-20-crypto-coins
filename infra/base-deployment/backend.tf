terraform {
  backend "s3" {
    key    = "crypto-coins/terraform.tfstate"
    region = "ap-southeast-1"
    encrypt = true
  }
}