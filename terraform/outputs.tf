output "lambda_function_name" {
  value       = module.lambda.lambda_function_name
}

output "lambda_function_url" {
  value       = module.lambda.lambda_function_url
}

output "api_gateway_url" {
  value       = module.lambda.api_gateway_url
}

output "custom_domain_url" {
  value       = module.lambda.custom_domain_url
}

output "route53_nameservers" {
  value       = module.route53.route53_nameservers
}

output "generated_api_keys" {
  value       = module.secrets.generated_api_keys
  sensitive   = true
}
