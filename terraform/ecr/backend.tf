terraform {
  backend "s3" {
    bucket         = "quotes-api-terraform-state"
    key            = "ecr/terraform.tfstate"
    region         = "us-east-2"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }
}
