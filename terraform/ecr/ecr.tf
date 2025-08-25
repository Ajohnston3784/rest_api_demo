# ECR Repository
resource "aws_ecr_repository" "app" {
  name = var.repository_name
  force_delete = true

  image_scanning_configuration {
    scan_on_push = true
  }
}

output "repository_url" {
  value = aws_ecr_repository.app.repository_url
  description = "The URL of the ECR repository"
}
