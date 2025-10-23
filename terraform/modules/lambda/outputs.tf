output "lambda_function_name" {
  value       = aws_lambda_function.app.function_name
}

output "lambda_function_url" {
  value       = aws_lambda_function_url.app.function_url
}

output "api_gateway_url" {
  value       = aws_apigatewayv2_api.lambda.api_endpoint
}

output "custom_domain_url" {
  value       = "https://${var.domain_name}"
}

output "api_gateway_domain_name_config" {
  value = {
    target_domain_name = aws_apigatewayv2_domain_name.api.domain_name_configuration[0].target_domain_name
    hosted_zone_id     = aws_apigatewayv2_domain_name.api.domain_name_configuration[0].hosted_zone_id
  }
}
