output "api_keys_parameter_name" {
  value       = aws_ssm_parameter.api_keys.name
}

output "api_keys_parameter_arn" {
  value       = aws_ssm_parameter.api_keys.arn
}

output "generated_api_keys" {
  value       = random_password.api_keys[*].result
  sensitive   = true
}
