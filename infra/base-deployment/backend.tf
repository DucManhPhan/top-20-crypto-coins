terraform {
  backend "s3" {
    bucket = "terraform-state-crypto-coins-bucket-manhpd5"
    key    = "crypto-coins/terraform.tfstate"
    region = "ap-southeast-1"
    encrypt = true
  }
}