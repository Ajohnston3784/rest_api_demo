terraform {
  required_version = ">=1.2.0"
  backend "s3" {
    bucket         = "quotes-api-terraform-state"
    key            = "ecr/terraform.tfstate"
    region         = "us-east-2"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}