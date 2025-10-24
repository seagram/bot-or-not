resource "random_password" "api_keys" {
  # creates 6 random api keys
  # instead of storing 6 different ones in AWS Secrets manager
  # which would be $2.5 CAD a month
  # store as one comma seperated string in parameter store for free
  count   = 6
  length  = 32
  special = false
}

resource "aws_ssm_parameter" "api_keys" {
  name        = "/${var.app_name}/api-keys"
  type        = "SecureString"
  value       = join(",", random_password.api_keys[*].result)

  tags = {
    Name        = "${var.app_name}-api-keys"
    Environment = "production"
  }
}
