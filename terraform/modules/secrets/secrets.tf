resource "random_password" "api_keys" {
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
