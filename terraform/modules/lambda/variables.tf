variable "app_name" {
  type        = string
}

variable "turso_database_url" {
  type        = string
  sensitive   = true
}

variable "turso_auth_token" {
  type        = string
  sensitive   = true
}

variable "api_keys_parameter_arn" {
  type        = string
}

variable "api_keys_parameter_name" {
  type        = string
}

variable "domain_name" {
  type        = string
}

variable "acm_certificate_arn" {
  type        = string
}

variable "route53_zone_id" {
  type        = string
}
