locals {
  app_name = "bot-or-not"
}

module "secrets" {
  source = "./modules/secrets"

  app_name = local.app_name
}

module "route53" {
  source = "./modules/route53"

  app_name                 = local.app_name
  domain_name              = var.domain_name
  api_gateway_domain_name  = module.lambda.api_gateway_domain_name_config
}

module "lambda" {
  source = "./modules/lambda"

  app_name                = local.app_name
  turso_database_url      = var.turso_database_url
  turso_auth_token        = var.turso_auth_token
  api_keys_parameter_arn  = module.secrets.api_keys_parameter_arn
  api_keys_parameter_name = module.secrets.api_keys_parameter_name
  domain_name             = var.domain_name
  acm_certificate_arn     = module.route53.acm_certificate_arn
  route53_zone_id         = module.route53.route53_zone_id
}
