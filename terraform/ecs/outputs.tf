output "alb_dns_name" {
  value       = aws_lb.app.dns_name
  description = "DNS name of the load balancer"
}
