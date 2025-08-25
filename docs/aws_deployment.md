## AWS Deployment

### Infrastructure Overview
The application is deployed on AWS using the following components:

- **ECS Fargate**: Runs the containerized FastAPI application
- **ECR**: Stores the Docker images
- **Application Load Balancer**: Handles incoming traffic
- **VPC**: Isolated network with public and private subnets
- **CloudWatch**: Application logging and monitoring

### Prerequisites for Deployment
1. AWS Account with appropriate permissions
2. AWS CLI installed and configured
3. Terraform installed
4. GitHub repository secrets configured:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `AWS_REGION` (set to us-east-2)

### Infrastructure as Code
The Terraform configuration in the `/terraform` directory defines:

1. **Networking**:
   - VPC with public and private subnets
   - NAT Gateway for private subnet internet access
   - Security groups for ALB and ECS tasks

2. **Container Infrastructure**:
   - ECR repository for Docker images
   - ECS Fargate cluster
   - Task definitions and service configurations
   - Application Load Balancer

3. **Security**:
   - IAM roles and policies
   - Security groups
   - Load balancer HTTPS configuration

### Deployment Process
The deployment is automated via GitHub Actions:

1. Push changes to the `main` branch
2. GitHub Actions workflow:
   - Builds Docker image
   - Tags with timestamp and commit SHA
   - Pushes to ECR
   - Applies Terraform configuration
   - Updates ECS service

### Accessing the Deployed API
Once deployed, the API is accessible through the ALB:

```bash
# Get the ALB DNS name from Terraform output
export API_URL=$(terraform -chdir=terraform output -raw alb_dns_name)

# Test the API
curl -H "Authorization: Bearer $JWT" http://$API_URL/v1/quotes
```

The API documentation is available at:
- Swagger UI: `http://$API_URL/docs`
- ReDoc: `http://$API_URL/redoc`

### Managing Deployments
Each deployment creates a uniquely tagged Docker image in ECR:
- Format: `YYYYMMDD-HHMMSS-commit_sha`
- Example: `20250825-143022-a1b2c3d`

To roll back to a previous version:
1. Find the desired image tag in ECR
2. Update the Terraform variable `image_tag`
3. Run Terraform apply

### Infrastructure Costs
The deployment is optimized for AWS free tier:
- Uses 1 Fargate container (free tier eligible)
- Application Load Balancer (free tier eligible)
- Minimal CloudWatch logging
- ECR image storage (minimal cost)
