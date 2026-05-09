terraform {
  backend "s3" {
    bucket  = "terraformstatesbackend"
    key     = "damolak-app/terraform.tfstate"
    region  = "us-east-1"
    encrypt = true
  }
}
