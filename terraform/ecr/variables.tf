variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-2"
}

variable "repository_name" {
  description = "Name of the ECR repository"
  type        = string
  default     = "quotes-api-demo-repo"
}
